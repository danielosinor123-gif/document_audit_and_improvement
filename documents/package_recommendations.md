# Package Recommendations

## Recommended Packages
- **pandas**: the backbone of the project - file loading (`read_csv`, `read_excel`), cleaning (`dropna`, `to_datetime`, `to_numeric`), grouping (`groupby.agg`), quantile segmentation (`quantile`), and quintile scoring (`qcut`). Already in `requirements.txt` (>= 1.5.0) and irreplaceable here without a rewrite.
- **numpy**: provides the numeric dtypes the cleaning logic relies on (`select_dtypes(include=[np.number])`) and numeric NaN handling. Pinned at >= 1.21.0; installed alongside pandas by default.
- **matplotlib**: renders the 2x2 dashboard (histogram, pie, line, bar) and saves it to `customer_dashboard.png` at dpi=300. Already required (>= 3.5.0).
- **seaborn**: imported by `customer_analytics.py` and pinned in `requirements.txt` (>= 0.11.0). Recommended to keep: it can style the dashboard (`sns.set_theme()`) and, if correlation or distribution plots are added later, its `heatmap`/`histplot` APIs are the fastest path.
- **openpyxl**: enables the `.xlsx` loading path in `DataProcessor.load_data` (pandas delegates Excel reading to it). Required for any Excel input (>= 3.0.0).

## Evaluation Criteria
- **How were these packages evaluated?** They were audited against what the code actually imports and calls: every package in `requirements.txt` maps to real usage except seaborn (imported but not yet called), which is retained deliberately. Maturity, pandas ecosystem compatibility, and MIT/BSD-style licensing were the tiebreakers.
- **What are the key decision factors?** (1) Actual usage in the source, (2) stability of the APIs the code depends on (`qcut`, `groupby.agg`, `to_period`), (3) install weight - only five packages are needed, so keeping the footprint small matters, (4) whether a package removes a hand-rolled implementation (see Alternatives).

## Alternatives Considered
- **polars**: Pros - dramatically faster on large datasets, lazy evaluation, stricter schema enforcement. Cons - the codebase uses pandas idioms throughout (`qcut`, `groupby.agg` with lambdas, `dt.to_period`), so adopting it means a full rewrite; overkill for the current data sizes.
- **scipy.stats**: Pros - statistically robust alternatives to the hand-rolled IQR outlier filter (e.g., z-scores, median absolute deviation). Cons - adds a heavy dependency for one small function; the IQR filter (see `decisions.md`) is simple, explicit, and sufficient for this dataset size.
- **plotly / dash**: Pros - interactive dashboards in the browser instead of a static PNG. Cons - much heavier dependency, requires a serving story; the current static PNG satisfies the "glanceable summary" goal.
- **scikit-learn**: Pros - a real churn model (logistic regression / gradient boosting) instead of the rule-based thresholds. Cons - the sample dataset is tiny and unlabeled for supervised learning; the transparent rules are easier to explain to stakeholders and to audit.
