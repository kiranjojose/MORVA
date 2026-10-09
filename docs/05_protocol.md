# 05 — Protocol (freeze before test evaluation)

## Split
Time blocks: train < `train_end` ≤ val < `val_end` ≤ test. A window belongs to a block only if its full span lies inside it. Report vessel overlap between blocks. Fit scalers and thresholds on train only.

## Frozen hypotheses
_Fill in and commit with date BEFORE any test run. Do not edit afterwards._

- H1: …
- H2: …
- H3: …
- Frozen on: ____ (commit hash: ____)

## Test-set rule
`vesselmind baselines --split test --confirm-test` (and model equivalents) are run once, after freezing. Any rerun is logged in the research log with the reason.
