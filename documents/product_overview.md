# Customer Analytics Tool - Product Overview

## Purpose
The Customer Analytics Tool loads raw customer purchase data from CSV or Excel files, cleans and validates it, and turns it into actionable business intelligence: customer lifetime value estimates, customer segments, churn-risk predictions, and a visual dashboard. It lets a small team answer "who are our best customers, who is slipping away, and what is our revenue trend?" without a data-science platform.

## Core Features
1. **Data loading and cleaning** (`DataProcessor.load_data` / `clean_data`) - reliably turns messy CSV/Excel exports into a validated, analysis-ready dataset by enforcing required columns, coercing types, filtering to the 2020-2024 window, and removing IQR outliers. Matters because every downstream number is only as good as this step.
2. **Customer segmentation and RFM analysis** (`CustomerAnalytics.segment_customers` / `rfm_analysis`) - splits customers into high/medium/low value tiers by CLV percentile and scores each customer on recency, frequency, and monetary value. Matters because it tells marketing where to focus spend.
3. **Churn prediction and dashboard** (`CustomerAnalytics.predict_churn` / `create_dashboard`) - flags customers at high/medium/low churn risk with simple recency/frequency rules and renders a 2x2 dashboard image (CLV distribution, segments, monthly revenue trend, churn distribution). Matters because it turns the analysis into something a non-technical stakeholder can read at a glance.

## Success Criteria
- **How do we know it's working?** `python customer_analytics.py` runs against `sample_data.csv` without errors, prints the insights report (38 customers, 8 high-value, 19 high churn risk on the bundled sample), produces `customer_dashboard.png`, and `DataProcessor.validate_data` reports passing (or explainable) checks.
- **What does "done" look like?** A new team member can load their own CSV with the five required columns, get a cleaned dataset, and generate insights and a dashboard without reading the source code - and the documentation (`product_overview.md`, `technical_architecture.md`, `package_recommendations.md`, `decisions.md`) explains every non-obvious behavior.
