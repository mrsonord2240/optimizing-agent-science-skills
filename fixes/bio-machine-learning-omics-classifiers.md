# bio-machine-learning-omics-classifiers fix pass - 2026-10-03

`class_weight='balanced'` was recommended although it inflates predicted risk (4.2x at 8% prevalence); the Skill now says reweighting needs recalibration and that it changes ranking only for tree ensembles. The batch snippet returned NaN beyond two batches and was not leave-one-batch-out; `scripts/batch_checks.py` now uses `LeaveOneGroupOut` and reports one-class batches. The elastic net is dense under the pinned `neg_log_loss` scoring, so the sparse-signature claim was dropped and a lasso plus 1-SE snippet gives the short list. Isotonic calibration is used only with at least 1,000 calibration samples and 100 in the rarer class, with a warning on a degenerate calibrator; early stopping uses a three-way split; the XGBoost demo now learns (best round 223) and warns if its best round is 0. A later text-only pass reduced the frontmatter description to its trigger.

- Final candidate audit: `audits/skills/bio-machine-learning-omics-classifiers/candidate@a2d417f41e37-reaudit-delta-20261003`
- Result: **88/100, Production Ready**; open P2s OC-012 (several quoted figures are single-setup values) and OC-013 (the trimmed description overlaps model-validation on "suspiciously perfect AUC").
- Candidate identity: `a2d417f41e37007d7a2a3ea4d76b744cf1be42485be95576f42dee806584616f`.

The provider binding record is the canonical proof that the committed shelf bytes match this independently audited candidate.
