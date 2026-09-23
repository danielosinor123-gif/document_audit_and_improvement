# Customer Analytics Tool - Product Overview

## Purpose
The Customer Analytics Tool loads raw customer purchase data from CSV or Excel files, cleans it into a validated dataset, and derives business intelligence from it: customer lifetime value, value segments, churn-risk labels, and a visual dashboard. It answers "who are our best customers, who is slipping away, and what is the revenue trend?" without needing a data-science platform.

## Core Features
1. **Data loading and cleaning** (`DataProcessor.load_data` / `clean_data`) - enforces five required columns, coerces dates/amounts, filters to the 2020-2024 window, removes IQR outliers. Matters because every downstream number depends on it.
2. **Segmentation and RFM analysis** (`CustomerAnalytics.segment_customers` / `rfm_analysis`) - high/medium/low value tiers by CLV percentile and quintile RFM scores. Matters because it directs marketing spend.
3. **Churn prediction and dashboard** (`CustomerAnalytics.predict_churn` / `create_dashboard`) - transparent recency/frequency risk rules plus a 2x2 PNG dashboard (CLV distribution, segments, monthly revenue trend, churn distribution). Matters because stakeholders can read it at a glance.

## Success Criteria
- **How do we know it's working?** `python customer_analytics.py` runs on `sample_data.csv` without errors, prints the insights report (38 customers, 8 high-value, 19 high churn risk on the sample), and produces `customer_dashboard.png`.
- **What does "done" look like?** A new team member can drop in their own CSV with the five required columns and get insights and a dashboard without reading the source - and the documentation in `docs/` and `documents/` explains every non-obvious behavior.
