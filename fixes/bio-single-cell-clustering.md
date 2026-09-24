# bio-single-cell-clustering fix pass

Source commit: `a409b098b3602b13d7c40610f1c6bc09057258ac`

Fixed all findings from the 2026-09-16 audit:

- Replaced the circular marker-overlap stop rule with explicit covariate-alignment and bootstrap-Jaccard checks, plus formal split-test and independent-replication gates before calling a cluster a population.
- Added the runnable `examples/validate_partition.py` helper with label/PCA/resolution guards.
- Corrected Seurat 5 Leiden guidance to `leidenbase` by default, retained the `igraph` alternative, and limited reticulate/`leidenalg` to older Seurat installations.
- Resolved elbow-versus-PC-range ambiguity: use the elbow as a floor and retain only structure stable across nearby PC values.
- Added a sweep-report contract and an explicit scSHC formal-test call that fails clearly when the optional package is unavailable.

Focused exact-commit re-audit: 7/7 executed, 28/28 assertions passed, 95/100 Production Ready. Canonical report and viewer: `F:\OpenScience\audits\bio-single-cell-clustering\`.
