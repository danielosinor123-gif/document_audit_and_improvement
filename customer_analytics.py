"""Customer analytics: CLV, segmentation, RFM, churn, and dashboarding.

CONTEXT BREADCRUMBS:
- What this project does:        documents/product_overview.md
- How the pieces fit together:   documents/technical_architecture.md
- Why pandas/numpy/matplotlib:   documents/package_recommendations.md
- Why the RFM reference date is  documents/decisions.md  (Decision 2)
  frozen at 2024-01-01, why
  churn uses rule thresholds
  (Decision 3), and what the
  0.7 CLV factor means
  (Decision 4)
- Full code audit:               assessment_notes.md

CustomerAnalytics builds on DataProcessor (imported directly from
data_processor.py, so both files must live in the same directory): it
turns the cleaned purchase DataFrame into customer lifetime value
estimates, value segments, churn-risk labels, insights, and a PNG
dashboard.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import seaborn as sns
from data_processor import DataProcessor

class CustomerAnalytics:
    def __init__(self, data_file):
        # Tight coupling: DataProcessor is constructed internally rather
        # than injected. Dependency injection would make this class easier
        # to test in isolation (see assessment_notes.md).
        self.processor = DataProcessor()
        # NOTE: if load_data fails it returns an EMPTY DataFrame, which is
        # assigned here as-is; downstream groupby calls then raise a
        # confusing KeyError (see assessment_notes.md).
        self.df = self.processor.load_data(data_file)
        self.segments = {}
        
    def calculate_clv(self, months=12):
        """Per-customer CLV proxy, sorted descending.

        DECISION 4 (documents/decisions.md): this is an ad-hoc estimate,
        not a standard CLV model - (spend/months) * (orders/months) *
        months * 0.7. The 0.7 factor is a conservative discount. Because
        segmentation uses CLV quantiles, the factor does not change
        segment membership, only the absolute reported value.
        """
        monthly_revenue = self.df.groupby('customer_id')['purchase_amount'].sum() / months
        frequency = self.df.groupby('customer_id').size() / months
        clv = monthly_revenue * frequency * months * 0.7
        return clv.sort_values(ascending=False)
    
    def segment_customers(self):
        """Split customers into value tiers by CLV percentile.

        high_value: CLV > 80th percentile; medium_value: 40th-80th;
        low_value: <= 40th. Result is cached in self.segments.
        """
        clv = self.calculate_clv()
        high_value = clv[clv > clv.quantile(0.8)]
        medium_value = clv[(clv > clv.quantile(0.4)) & (clv <= clv.quantile(0.8))]
        low_value = clv[clv <= clv.quantile(0.4)]
        
        self.segments = {
            'high_value': high_value.index.tolist(),
            'medium_value': medium_value.index.tolist(),
            'low_value': low_value.index.tolist()
        }
        return self.segments
    
    def rfm_analysis(self):
        """Recency/Frequency/Monetary scoring into quintiles.

        DECISION 2 (documents/decisions.md): recency is measured against a
        HARD-CODED "now" of 2024-01-01 for reproducibility - the same data
        always produces the same scores, but values drift as real time
        passes. frequency uses .rank(method='first') before qcut so ties
        get distinct quintile edges instead of qcut raising on duplicate
        bin edges. R scores are inverted (5 = most recent).
        """
        now = pd.to_datetime('2024-01-01')
        rfm = self.df.groupby('customer_id').agg({
            'purchase_date': lambda x: (now - pd.to_datetime(x.max())).days,
            'order_id': 'count',
            'purchase_amount': 'sum'
        }).reset_index()
        
        rfm.columns = ['customer_id', 'recency', 'frequency', 'monetary']
        
        rfm['r_score'] = pd.qcut(rfm['recency'], 5, labels=[5,4,3,2,1])
        rfm['f_score'] = pd.qcut(rfm['frequency'].rank(method='first'), 5, labels=[1,2,3,4,5])
        rfm['m_score'] = pd.qcut(rfm['monetary'], 5, labels=[1,2,3,4,5])
        
        rfm['rfm_score'] = rfm['r_score'].astype(str) + rfm['f_score'].astype(str) + rfm['m_score'].astype(str)
        
        return rfm
    
    def predict_churn(self):
        """Rule-based churn risk: high / medium / low per customer.

        DECISION 3 (documents/decisions.md): transparent thresholds on the
        RFM output (recency > 90 & frequency < 3 -> high; recency > 60 &
        frequency < 5 -> medium) instead of a trained model - the dataset
        is small and unlabeled, and explicit rules are fully auditable.
        """
        rfm = self.rfm_analysis()
        churn_risk = []
        
        for _, row in rfm.iterrows():
            if row['recency'] > 90 and row['frequency'] < 3:
                risk = 'high'
            elif row['recency'] > 60 and row['frequency'] < 5:
                risk = 'medium'
            else:
                risk = 'low'
            churn_risk.append(risk)
            
        rfm['churn_risk'] = churn_risk
        return rfm[['customer_id', 'churn_risk']]
    
    def generate_insights(self):
        segments = self.segment_customers()
        churn = self.predict_churn()
        
        insights = {
            'total_customers': len(self.df['customer_id'].unique()),
            'high_value_customers': len(segments['high_value']),
            'high_churn_risk': len(churn[churn['churn_risk'] == 'high']),
            'avg_clv': self.calculate_clv().mean(),
            'revenue_concentration': (self.df[self.df['customer_id'].isin(segments['high_value'])]['purchase_amount'].sum() / 
                                    self.df['purchase_amount'].sum()) * 100
        }
        
        return insights
    
    def create_dashboard(self, save_path='customer_dashboard.png'):
        """Render and save the 2x2 analytics dashboard.

        Panels: CLV distribution (histogram), customer segments (pie),
        monthly revenue trend (line), churn-risk distribution (bar).
        Saved at dpi=300 and the figure is closed to avoid leaks.
        """
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        
        clv = self.calculate_clv()
        axes[0,0].hist(clv, bins=30, alpha=0.7)
        axes[0,0].set_title('Customer Lifetime Value Distribution')
        axes[0,0].set_xlabel('CLV ($)')
        
        segments = self.segment_customers()
        segment_sizes = [len(segments[key]) for key in segments.keys()]
        axes[0,1].pie(segment_sizes, labels=segments.keys(), autopct='%1.1f%%')
        axes[0,1].set_title('Customer Segments')
        
        monthly_revenue = self.df.groupby(pd.to_datetime(self.df['purchase_date']).dt.to_period('M'))['purchase_amount'].sum()
        axes[1,0].plot(monthly_revenue.index.astype(str), monthly_revenue.values)
        axes[1,0].set_title('Monthly Revenue Trend')
        axes[1,0].tick_params(axis='x', rotation=45)
        
        churn = self.predict_churn()
        churn_counts = churn['churn_risk'].value_counts()
        axes[1,1].bar(churn_counts.index, churn_counts.values)
        axes[1,1].set_title('Churn Risk Distribution')
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return save_path

def main():
    """Entry point: prints the insights report and saves the dashboard.

    Expects sample_data.csv in the current working directory; on the
    bundled sample it reports 38 customers, 8 high-value, and 19 at high
    churn risk.
    """
    analytics = CustomerAnalytics('sample_data.csv')
    
    print("Customer Analytics Report")
    print("=" * 40)
    
    insights = analytics.generate_insights()
    for key, value in insights.items():
        print(f"{key.replace('_', ' ').title()}: {value}")
    
    dashboard_file = analytics.create_dashboard()
    print(f"\nDashboard saved to: {dashboard_file}")
    
    segments = analytics.segment_customers()
    print(f"\nHigh value customers: {len(segments['high_value'])}")
    
    churn_prediction = analytics.predict_churn()
    high_risk_customers = churn_prediction[churn_prediction['churn_risk'] == 'high']
    print(f"Customers at high churn risk: {len(high_risk_customers)}")

if __name__ == "__main__":
    main() 
