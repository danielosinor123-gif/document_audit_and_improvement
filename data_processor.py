import pandas as pd
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

class DataProcessor:
    def __init__(self):
        self.required_columns = ['customer_id', 'order_id', 'purchase_date', 'purchase_amount', 'product_category']
        
    def load_data(self, file_path):
        try:
            if file_path.endswith('.csv'):
                df = pd.read_csv(file_path)
            elif file_path.endswith('.xlsx'):
                df = pd.read_excel(file_path)
            else:
                raise ValueError("Unsupported file format")
                
            return self.clean_data(df)
        except Exception as e:
            print(f"Error loading data: {e}")
            return pd.DataFrame()
    
    def clean_data(self, df):
        original_rows = len(df)
        
        missing_cols = [col for col in self.required_columns if col not in df.columns]
        if missing_cols:
            raise ValueError(f"Missing required columns: {missing_cols}")
        
        df = df.dropna(subset=self.required_columns)
        
        df['purchase_date'] = pd.to_datetime(df['purchase_date'], errors='coerce')
        df = df.dropna(subset=['purchase_date'])
        
        df['purchase_amount'] = pd.to_numeric(df['purchase_amount'], errors='coerce')
        df = df[df['purchase_amount'] > 0]
        
        df['customer_id'] = df['customer_id'].astype(str)
        df['order_id'] = df['order_id'].astype(str)
        
        df = df[df['purchase_date'] >= '2020-01-01']
        df = df[df['purchase_date'] <= '2024-12-31']
        
        q1 = df['purchase_amount'].quantile(0.25)
        q3 = df['purchase_amount'].quantile(0.75)
        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        
        outliers_removed = len(df[(df['purchase_amount'] < lower_bound) | (df['purchase_amount'] > upper_bound)])
        df = df[(df['purchase_amount'] >= lower_bound) & (df['purchase_amount'] <= upper_bound)]
        
        print(f"Data cleaning summary:")
        print(f"Original rows: {original_rows}")
        print(f"Final rows: {len(df)}")
        print(f"Rows removed: {original_rows - len(df)}")
        print(f"Outliers removed: {outliers_removed}")
        
        return df.reset_index(drop=True)
    
    def validate_data(self, df):
        validation_errors = []
        
        if df.empty:
            validation_errors.append("Dataset is empty")
            
        if len(df['customer_id'].unique()) < 10:
            validation_errors.append("Too few unique customers")
            
        date_range = (df['purchase_date'].max() - df['purchase_date'].min()).days
        if date_range < 30:
            validation_errors.append("Date range too narrow")
            
        if df['purchase_amount'].min() <= 0:
            validation_errors.append("Invalid purchase amounts found")
            
        duplicate_orders = df[df.duplicated(['customer_id', 'order_id'], keep=False)]
        if not duplicate_orders.empty:
            validation_errors.append(f"Found {len(duplicate_orders)} duplicate orders")
            
        if validation_errors:
            print("Validation warnings:")
            for error in validation_errors:
                print(f"- {error}")
        else:
            print("Data validation passed")
            
        return len(validation_errors) == 0
    
    def get_data_summary(self, df):
        summary = {
            'total_rows': len(df),
            'unique_customers': len(df['customer_id'].unique()),
            'unique_orders': len(df['order_id'].unique()),
            'date_range': f"{df['purchase_date'].min().date()} to {df['purchase_date'].max().date()}",
            'total_revenue': df['purchase_amount'].sum(),
            'avg_order_value': df['purchase_amount'].mean(),
            'product_categories': df['product_category'].unique().tolist()
        }
        return summary
    
    def create_customer_summary(self, df):
        customer_summary = df.groupby('customer_id').agg({
            'order_id': 'count',
            'purchase_amount': ['sum', 'mean', 'std'],
            'purchase_date': ['min', 'max'],
            'product_category': lambda x: len(x.unique())
        }).reset_index()
        
        customer_summary.columns = [
            'customer_id', 'total_orders', 'total_spent', 'avg_order_value',
            'spending_volatility', 'first_purchase', 'last_purchase', 'categories_purchased'
        ]
        
        customer_summary['days_as_customer'] = (
            customer_summary['last_purchase'] - customer_summary['first_purchase']
        ).dt.days
        
        customer_summary['spending_volatility'] = customer_summary['spending_volatility'].fillna(0)
        
        return customer_summary 
