# Technical Architecture

## Major Components
- **`DataProcessor`** (`data_processor.py`): Data engineering - file loading (CSV/Excel), schema enforcement (five required columns), cleaning (type coercion, date-window filtering, IQR outlier removal), validation checks, headline data summaries, and per-customer aggregate rollups.
- **`CustomerAnalytics`** (`customer_analytics.py`): Business analytics - CLV estimation, quantile-based customer segmentation, RFM scoring, rule-based churn prediction, insight aggregation, and matplotlib dashboard rendering. Depends on `DataProcessor` (constructs one internally in `__init__`).
- **`main()`** (`customer_analytics.py`): Entry point - instantiates `CustomerAnalytics` against `sample_data.csv`, prints the insights report, saves the dashboard, and prints segment/churn counts.

## Data Flow
```
sample_data.csv (or .xlsx)
        |
        v
DataProcessor.load_data()          -- pandas read_csv / read_excel
        |
        v
DataProcessor.clean_data()         -- required columns enforced, dropna,
        |                             to_datetime / to_numeric coercion,
        |                             2020-2024 window, amounts > 0,
        |                             IQR outlier removal (purchase_amount)
        v
cleaned DataFrame  <---------------- both classes operate on this in memory
        |
        +--> DataProcessor.validate_data()    -- quality checks (bool)
        +--> DataProcessor.get_data_summary() -- headline metrics dict
        +--> DataProcessor.create_customer_summary() -- per-customer rollup
        |
        v
CustomerAnalytics.calculate_clv()  -- per-customer CLV series
        |
        +--> segment_customers()  -- high/medium/low tiers (cached in self.segments)
        +--> rfm_analysis()       -- recency/frequency/monetary + qcut scores
                |
                +--> predict_churn()  -- risk labels per customer
        |
        v
generate_insights()  --> printed report
create_dashboard()   --> customer_dashboard.png (2x2 matplotlib figure)
```

## Key Dependencies
- **External APIs**: none - everything runs locally on files.
- **Required libraries** (see `requirements.txt`):
  - `pandas` (>= 1.5.0) - loading, cleaning, grouping, qcut scoring
  - `numpy` (>= 1.21.0) - numeric dtypes
  - `matplotlib` (>= 3.5.0) - dashboard rendering and PNG export
  - `seaborn` (>= 0.11.0) - imported (available for styling; not yet used directly)
  - `openpyxl` (>= 3.0.0) - Excel (.xlsx) read support
- **File formats**: input `.csv` and `.xlsx`; output `.png` (dashboard). Input must contain the five required columns: `customer_id`, `order_id`, `purchase_date`, `purchase_amount`, `product_category`.

## Technical Constraints
- **Performance requirements**: everything is held in memory (`pandas` DataFrames); the sample loads in seconds. Datasets far larger than available RAM would need chunked loading or a database layer.
- **Platform limitations**: pure Python, cross-platform; matplotlib's default backend writes the dashboard to a file so it works headless. Python 3.x required (f-strings, `pd.qcut` behavior).
- **Integration requirements**: `customer_analytics.py` imports `DataProcessor` directly, so both files must live in the same directory/package. `main()` expects `sample_data.csv` in the current working directory. The cleaning window (2020-01-01 to 2024-12-31) and the RFM reference date (2024-01-01) are hard-coded constants - see `decisions.md`.
