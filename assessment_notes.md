# Assessment Notes - document_audit_and_improvement

AI-assisted code review (via Cursor) of the inherited customer data analytics project.
Files reviewed: `data_processor.py`, `customer_analytics.py`, `requirements.txt`, `sample_data.csv`.

## Step 1: What the files do (Cursor's explanation)

### `data_processor.py` (123 lines)
`DataProcessor` handles the data-engineering half of the project:

- **`load_data(file_path)`** - loads a `.csv` (pandas `read_csv`) or `.xlsx`
  (`read_excel`) file and immediately runs `clean_data`. Any failure prints an
  error and returns an empty `DataFrame`.
- **`clean_data(df)`** - enforces five required columns
  (`customer_id`, `order_id`, `purchase_date`, `purchase_amount`,
  `product_category`), drops rows with missing required values, coerces
  `purchase_date` to datetime and `purchase_amount` to numeric, keeps only
  amounts > 0 inside the 2020-2024 window, removes IQR outliers on
  `purchase_amount` (1.5x multiplier), prints a cleaning summary, and returns
  the frame reset-indexed.
- **`validate_data(df)`** - five quality checks (empty dataset, fewer than 10
  unique customers, date range narrower than 30 days, non-positive amounts,
  duplicate customer/order pairs). Prints warnings or a pass message and
  returns a boolean.
- **`get_data_summary(df)`** - returns a dict of headline metrics (rows,
  unique customers/orders, date range, total revenue, average order value,
  product categories).
- **`create_customer_summary(df)`** - per-customer rollup (order count, spend
  sum/mean/std, first/last purchase, category diversity, days-as-customer).

### `customer_analytics.py` (132 lines)
`CustomerAnalytics` builds on top of `DataProcessor` (imported directly):

- **`calculate_clv(months=12)`** - computes a customer lifetime value proxy:
  `(total spend / months) * (orders / months) * months * 0.7`, sorted
  descending.
- **`segment_customers()`** - splits customers into `high_value` (CLV above
  the 80th percentile), `medium_value` (40th-80th), and `low_value` (below the
  40th) and caches the result in `self.segments`.
- **`rfm_analysis()`** - Recency/Frequency/Monetary scoring: recency is days
  since each customer's last purchase measured against a **hard-coded**
  "now" of 2024-01-01; R/F/M scores use `pd.qcut` into quintiles (R is
  inverted so 5 = most recent); produces a concatenated `rfm_score` string.
- **`predict_churn()`** - rule-based risk classification: `recency > 90 and
  frequency < 3` -> high, `recency > 60 and frequency < 5` -> medium,
  otherwise low.
- **`generate_insights()`** - aggregates headline numbers (total customers,
  high-value count, high churn-risk count, average CLV, revenue
  concentration percentage held by high-value customers).
- **`create_dashboard(save_path)`** - a 2x2 matplotlib figure (CLV histogram,
  segment pie chart, monthly revenue trend, churn-risk bar chart) saved to
  `customer_dashboard.png` at dpi=300.

### Verified run
Running `python customer_analytics.py` against the bundled `sample_data.csv`
succeeds: 38 customers, 8 high-value, 19 at high churn risk, average CLV
~61.47, revenue concentration ~37.4%, and the dashboard PNG is produced.

## Areas of confusion / unclear model responses

1. **The CLV formula is dimensionally odd.** Cursor's first explanation
   described it as a "standard CLV calculation", which is not accurate:
   `monthly_revenue * frequency * months` multiplies dollars-per-month by
   orders-per-month, which is not a recognized CLV model. It reads more like
   an ad-hoc proxy with a 0.7 confidence factor. The formula was verified
   line-by-line rather than trusted from the first response.
2. **The RFM "now" is frozen at 2024-01-01.** This is easy to miss - recency
   is measured against a constant, not the current date, so results drift as
   real time passes. Worth flagging to anyone reusing this code.
3. **`warnings.filterwarnings('ignore')` is global.** Both date coercion
   (`errors='coerce'`) and numeric coercion silently produce `NaN` rows, and
   the global filter hides any remaining pandas warnings. Errors from invalid
   rows only surface later as dropped-row counts.
4. **Hard-coded cleaning window (2020-2024).** `clean_data` silently drops
   purchases outside this range. Data from 2025+ would vanish with no
   explicit warning - only the removed-row count hints at it.
5. **No empty-frame guard in `CustomerAnalytics`.** If `load_data` fails and
   returns an empty `DataFrame`, the constructor still assigns it and every
   downstream `groupby` raises a `KeyError` - a confusing failure mode.
6. **`create_customer_summary` is dead code in practice.** Nothing in either
   file's main flow calls it. It is presumably intended for future use.
7. **Segment boundaries.** `medium_value` uses `> 0.4 and <= 0.8` quantiles -
   exactly which percentile boundaries belong to which segment is easy to
   misstate; verified against the source.
8. **Tight coupling.** `CustomerAnalytics` constructs its own `DataProcessor`
   internally rather than receiving one - dependency injection would make the
   classes easier to test in isolation.

## Summary

The project is small, working, and readable, but undocumented. The main risks
for future maintainers are the silent data-shedding behaviors (global warning
suppression, hard-coded date window, coercion `NaN` drops) and the non-standard
CLV formula. Documentation should make these behaviors explicit.
