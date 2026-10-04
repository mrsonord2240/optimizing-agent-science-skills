# bio-machine-learning-survival-analysis fix pass - 2026-10-03

The Kaplan-Meier baseline score in `scripts/cox_regression.py` ignored censored patients (0.263 on GBSG2 where the true value is 0.178), which made the baseline look worse than it is. It is now a censoring-aware baseline on the same estimator, time grid and held-out split as the model. The Coxnet example predicted at the least-penalized alpha (161 non-zero coefficients, held-out Uno C 0.708); alpha is now chosen by cross-validation on training data only (6 non-zero, 0.791). The false claim that random survival forests give cumulative incidence was removed, methods that were not run are labelled, the pandas<3 cap is attributed to lifelines alone, and every snippet runs as written. Later text-only passes corrected the time-grid error row and reduced the frontmatter description to its trigger.

- Final candidate audit: `audits/skills/bio-machine-learning-survival-analysis/candidate@6fb42410e7b7-reaudit-delta2-20261003`
- Result: **87/100, Production Ready**; no open findings.
- Candidate identity: `6fb42410e7b70eff829bac23fce3c05a0a9941abff229c15570619de1f7f62d3`.

The provider binding record is the canonical proof that the committed shelf bytes match this independently audited candidate.
