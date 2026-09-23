# Decision Log

Technical decisions made in the code, why they were made, and their consequences.
See `assessment_notes.md` for the full audit and `technical_architecture.md` for the architecture.

## Decision 1: IQR outlier removal on `purchase_amount` only

**Where**: `data_processor.py` - `DataProcessor.clean_data()` (the quartile/interquartile-range block).

**Decision**: Outliers are detected with the 1.5x IQR rule and applied **only** to the
`purchase_amount` column, filtering rows whose amount falls outside
`[Q1 - 1.5*IQR, Q3 + 1.5*IQR]`.

**Why**: Purchase amounts are the only field with a meaningful numeric tail in this
schema - extreme values there would distort revenue totals, average order value, and
every CLV/segmentation number downstream. Applying the filter to every numeric column
(such as `customer_id`-derived counts) could silently delete legitimate records. The
1.5 multiplier is the conventional "Tukey fence" choice: aggressive enough to remove
data-entry errors, conservative enough to keep genuine large purchases.

**Consequences**:
- Outlier rows are removed **silently** - only the `Outliers removed:` count in the
  cleaning summary reveals it.
- If a category-specific outlier pattern emerges (e.g., one category with naturally
  higher prices), a per-category IQR would be more accurate than the global one.

## Decision 2: Fixed reference date (2024-01-01) for RFM recency

**Where**: `customer_analytics.py` - `CustomerAnalytics.rfm_analysis()` (`now = pd.to_datetime('2024-01-01')`).

**Decision**: Recency is measured as days between each customer's last purchase and a
hard-coded constant "now" of 2024-01-01, rather than the actual current date.

**Why**: Reproducibility. A fixed reference date makes the RFM scores, churn-risk
labels, and dashboard deterministic - running the analysis twice on the same data
always produces the same report. This matters for auditing and for comparing runs
during development. The bundled `sample_data.csv` spans 2023, so 2024-01-01 keeps
recency values small and stable.

**Consequences**:
- Results drift as real time passes: the same file analyzed in 2026 reports larger
  recency values than in 2024, and more customers cross the churn thresholds.
- Production use should replace the constant with a configurable or current date -
  the trade-off is losing run-to-run determinism.

## Decision 3: Rule-based churn thresholds instead of a model

**Where**: `customer_analytics.py` - `CustomerAnalytics.predict_churn()`.

**Decision**: Churn risk is classified with transparent thresholds on the RFM output:
`recency > 90 and frequency < 3` -> high, `recency > 60 and frequency < 5` -> medium,
otherwise low.

**Why**: The dataset is small and unlabeled, so a supervised model cannot be trained
meaningfully. Explicit rules are fully auditable and explainable to non-technical
stakeholders, and they compose directly with the RFM features already computed.

**Consequences**:
- The thresholds are hard-coded and not learned from data; a real deployment would
  calibrate them against actual churn history.
- Adding a fourth risk tier or new features requires code changes, not retraining.

## Decision 4: The 0.7 confidence multiplier in CLV

**Where**: `customer_analytics.py` - `CustomerAnalytics.calculate_clv()`.

**Decision**: The CLV proxy is scaled by a fixed factor of 0.7 after the
revenue/frequency computation.

**Why**: The formula is an ad-hoc estimate rather than a standard CLV model (see
`assessment_notes.md`); the 0.7 factor acts as a conservative discount so the
reported numbers do not overstate customer value.

**Consequences**:
- All CLV values, the segmentation boundaries (which are relative quantiles, so
  unaffected), and the average-CLV insight inherit the discount.
- Because segmentation uses CLV *quantiles*, the multiplier does not change which
  segment a customer lands in - only the absolute reported value.
