# Fresh R runtime results

Environment: R 4.4.3; ape 5.8-1; phytools 2.5-2; geiger 2.0.12; corHMM 2.8; OUwie 3.0.3. Full session info: `r-sessionInfo.txt`; inputs/outputs: `r-run/`; executable audit harness: `../retest_r.R`.

- Stochastic mapping: fresh 30-tip binary trait fixture, explicit seed 20260928, ARD selected, 1,000 maps and 59 node posterior rows. Missing taxa case failed with named missing tips and row-alignment recovery advice. Missing seed stopped before input processing and requested exactly one seed.
- Continuous BM: fresh 35-tip Brownian fixture, six finite AIC values; BM selected; 34 ancestral node estimates and 34 `fastAnc` 95% confidence intervals.
- OU: the selected OU route invoked real `OUwie.anc` on the actual OUwie fitted object in OUwie 3.0.3, returning 29 point estimates. Result status is `exploratory_point_estimates_only`; uncertainty is `NULL` and labelled “not provided by OUwie.anc”. This was not assessed as an uncertainty-bearing ASR output.
- OUwie diagnostic: unmodified default `check.identify=TRUE` on a single-regime OU1 fixture reproduced “missing value where TRUE/FALSE needed”; candidate's documented `check.identify=FALSE` validation route completed.
- Transformed winners: independently forced EB, lambda, kappa, and delta winners each failed closed with explicit “not implemented”/no-original-tree-substitution language.

These are direct retests, not inherited fix-phase passes. The R harness uses deterministic fixtures and reports assertions inline; R/package versions and artifacts are preserved for reproducibility.
