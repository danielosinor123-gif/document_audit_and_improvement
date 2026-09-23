# Technical Scoping Document

## Major Moving Parts
- **`DataProcessor`** (`data_processor.py`): Data engineering - CSV/Excel loading, schema enforcement (five required columns: `customer_id`, `order_id`, `purchase_date`, `purchase_amount`, `product_category`), cleaning (type coercion, 2020-2024 date window, amounts > 0, IQR outlier removal on `purchase_amount`), five validation checks, headline summaries, and per-customer rollups.
- **`CustomerAnalytics`** (`customer_analytics.py`): Business analytics - CLV estimation (ad-hoc proxy with a 0.7 factor), quantile segmentation, RFM scoring via `pd.qcut` against a fixed reference date, rule-based churn prediction, insight aggregation, and matplotlib dashboard rendering. Constructs its own `DataProcessor` internally.
- **`main()`** (`customer_analytics.py`): Entry point - runs the full flow against `sample_data.csv` and prints the report.

## Data Flow
```
sample_data.csv / .xlsx
   -> DataProcessor.load_data()      (pandas read_csv / read_excel)
   -> DataProcessor.clean_data()     (required columns, dropna, coercion,
                                       2020-2024 window, amounts > 0, IQR filter)
   -> cleaned DataFrame              (both classes operate on this in memory)
        -> validate_data()           (quality checks -> bool)
        -> calculate_clv()           (per-customer CLV series)
             -> segment_customers()  (high/medium/low tiers)
             -> rfm_analysis()       (R/F/M quintile scores)
                  -> predict_churn() (risk labels)
        -> generate_insights()       (printed report)
        -> create_dashboard()        (customer_dashboard.png, 2x2 figure)
```

## Key Dependencies
- **External APIs**: none - fully local, file-based.
- **Required libraries**: `pandas` (>= 1.5.0), `numpy` (>= 1.21.0), `matplotlib` (>= 3.5.0), `seaborn` (>= 0.11.0), `openpyxl` (>= 3.0.0) - see `requirements.txt`.
- **File formats**: input `.csv` / `.xlsx` with the five required columns; output `.png`.

## Technical Constraints
- **Performance**: everything is held in memory; datasets larger than RAM would need chunked loading or a database layer.
- **Platform**: pure Python 3.x, cross-platform, headless-friendly (dashboard saved to file).
- **Integration**: both `.py` files must live in the same directory (`customer_analytics.py` imports `DataProcessor` directly); `main()` expects `sample_data.csv` in the working directory; the 2020-2024 cleaning window and the 2024-01-01 RFM reference date are hard-coded constants (see `documents/decisions.md`).
