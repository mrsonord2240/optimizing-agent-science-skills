# bio-machine-learning-biomarker-discovery fix pass - 2026-10-03

The stability-selection snippet depended on feature units and reported 35 stable probes under permuted labels. `scripts/stability_selection.py` now standardizes inside each subsample, fixes a per-subsample feature budget, is seeded end to end, and reports a permuted-label null count beside the real one (0 in all 11 permutations on full Golub). `LogisticRegressionCV` scoring is pinned to `accuracy` with a measured signature-size table, the scaler sits inside the leakage-safe pipeline, a nested `GridSearchCV` snippet and an in-fold mRMR example were added, and script print statements match what runs. The `penalty=` argument deprecated in scikit-learn 1.8 was replaced. The frontmatter description was reduced to its trigger.

- Final candidate audit: `audits/skills/bio-machine-learning-biomarker-discovery/candidate@27580088c038-reaudit-lane3a1-20261003`
- Result: **88/100, Production Ready**; open P2s RA-001 (unstratified subsamples raise a misleading error with 8 or fewer positives) and RA-002 (`roc_auc` signature size varies across partitions).
- Candidate identity: `27580088c038f830586abc45faa573419e8cf255ef355932b40840c41eda3134`.

The provider binding record is the canonical proof that the committed shelf bytes match this independently audited candidate.
