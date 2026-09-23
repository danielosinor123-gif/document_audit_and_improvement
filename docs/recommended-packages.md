# Recommended Packages List

## Recommended Packages
- **pandas** (>= 1.5.0): backbone of the project - `read_csv`/`read_excel` loading, `dropna`/`to_datetime`/`to_numeric` cleaning, `groupby.agg` rollups, `quantile` segmentation, `qcut` RFM scoring.
- **numpy** (>= 1.21.0): numeric dtypes for the cleaning logic (`select_dtypes(include=[np.number])`) and NaN handling.
- **matplotlib** (>= 3.5.0): renders the 2x2 dashboard and saves it to `customer_dashboard.png` at dpi=300.
- **seaborn** (>= 0.11.0): already imported and pinned - keep it for theme styling and any future heatmap/distribution plots.
- **openpyxl** (>= 3.0.0): enables the `.xlsx` loading path (pandas delegates Excel reads to it).

## Evaluation Criteria
- **How were these packages evaluated?** Audited against actual usage in the source: every entry in `requirements.txt` maps to real usage except seaborn (imported, not yet called), which is retained deliberately. Maturity, pandas-ecosystem compatibility, and permissive licensing were the tiebreakers.
- **What are the key decision factors?** (1) actual usage in the source, (2) stability of the APIs the code depends on (`qcut`, `groupby.agg`, `to_period`), (3) install weight - five packages keeps the footprint small, (4) whether a package removes a hand-rolled implementation.

## Alternatives Considered
- **polars**: Pros - much faster on large data, lazy evaluation, strict schemas. Cons - the codebase is pandas-idiomatic throughout (`qcut`, `groupby.agg` lambdas, `dt.to_period`), so it means a full rewrite; overkill at current data sizes.
- **scipy.stats**: Pros - robust outlier alternatives to the hand-rolled IQR filter. Cons - heavy dependency for one small function; the IQR filter is simple and sufficient here.
- **plotly / dash**: Pros - interactive browser dashboards. Cons - heavy, needs a serving story; the static PNG satisfies the goal.
- **scikit-learn**: Pros - a real churn model instead of rule thresholds. Cons - the dataset is tiny and unlabeled; transparent rules are easier to audit and explain.
