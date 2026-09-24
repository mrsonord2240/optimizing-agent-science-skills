# Forest and funnel plots — fix pass

## Source commits

- `f7117159cfbea4ed10d900c62e87c940e6812cbe` — core reliability and workflow pass.
- `3473a8f48eccab6c73436a627c3e8568f3736eef` — final plot-bound correction; exact re-audit target.

## Corrected findings

- Replaced the broken `bquote(paste(...))` pooled-row footer with a scalar label that renders tau-squared, I-squared, and Q p-value.
- Derived forest bounds from every study CI plus the pooled and prediction intervals, preventing clipped whiskers.
- Encoded the k<3 stop, k<5 HKSJ/I-squared behavior, and k<10 Egger withholding.
- Distinguished adjusted `ggforest()` covariate displays from actual treatment-by-subgroup interaction analysis; added sparse-stratum stops.
- Made the shipped R example self-contained through the Cox and MR sections, avoided `mr_input` name shadowing, and made MR method comparison outlier-safe with `snp_estimates = FALSE`.
- Corrected the `netmeta` description and removed unsupported promises of MR p-values on the forest plot.

## Exact-commit result

`3473a8f48eccab6c73436a627c3e8568f3736eef` re-audited at **95/100 — Production Ready**.

- Veto gates: PASS.
- Exact-source contract: 13/13 PASS.
- Dynamic assertions: 25/25 PASS.
- Full shipped R workflow passed with warnings promoted to errors; BCG forest and funnel PNGs visually inspected.
- Open P0/P1/P2 recommendations: none.

## Evidence

- Report: `F:\OpenScience\audits\bio-data-visualization-forest-funnel-plots\eval_report_bio-data-visualization-forest-funnel-plots_result.json`
- Viewer: `F:\OpenScience\audits\bio-data-visualization-forest-funnel-plots\eval_viewer_bio-data-visualization-forest-funnel-plots.md`
- Exact execution: `F:\OpenScience\audits\bio-data-visualization-forest-funnel-plots\run\exact-commit-3473a8f\exact_execution.log`
