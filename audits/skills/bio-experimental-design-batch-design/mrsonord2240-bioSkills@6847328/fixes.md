# bio-experimental-design-batch-design — 2026-09-16

Scope override from Sam: fix all three open findings (1 P1, 2 P2). Commit `e543a0a` on
`fix/r2-metab-a` (worktree `F:\OpenScience\wt\metab-a`).

| finding | priority | change | verified (ran / help / docs) | notes |
| --- | --- | --- | --- | --- |
| SVA block fails on matrices with missing values | P1 | Added explicit NA/Inf detection before `num.sv()`/`sva()` in SKILL.md's "Detecting Hidden Batch Effects" block: message the missing-value fraction, filter to complete-observation features (stated bias caveat), or impute first via normalization-qc (Option B, not executed here — left as a named alternative). `stopifnot` guards the matrix is finite before proceeding. Added a Common Errors row. | ran | Reproduced the original failure and the fix on the audit's real synthetic MaxQuant `proteinGroups.txt` (1500x8, 2120 NA): fixed block now runs on the NA-present matrix (738/1500 complete features, n_sv=1, cor(SV1, day B2)=1.00) and on a fully complete matrix (same n_sv/cor) — both via `rs.sh` with sva 3.54.0. `examples/batch_design.R` extended to inject NAs into its simulated matrix and run the fixed block on both versions inline; full script exits 0. |
| No verification step after optimization | P2 | Added a `table(condition, batch)` check after `bc$get_samples()` in the constrained-assignment block: hard `stopifnot(all(tab > 0))` against confounding (empty cell), a soft `warning()` when the split is avoidably uneven (imbalance > 1), and the `max_iter` argument on `optimize_design()`. Same pattern repeated in the new bridge-channel block. | ran | designit 0.5.0 via `rs.sh` on the SKILL.md 24-sample/3-batch example: converged to a perfect 4/4/4, `stopifnot` passed, no warning fired. |
| Bridge/reference-channel layout not shown | P2 | New "Reference / Bridge Channel Layout" section: `BatchContainer$new(dimensions = list(plex=, channel=), exclude = data.frame(plex=, channel=))` reserves one channel per plex; occupancy/confounding `stopifnot` checks; a run-order-randomization note for LC-MS. | ran | designit 0.5.0 via `rs.sh` on 60 samples / 4 plexes x 16 channels: channel 16 stays empty in every plex, 15 biological positions per plex, condition split converges to 7/8/7/8 (the achievable optimum vs. the audit's accepted 7/7/7/9), both `stopifnot` checks pass. |

No findings left unfixed.

Verification commands were run through `F:\OpenScience\audit-envs\untargeted-metabolomics-analyst\rs.sh` (R 4.4.3, R-lib with designit 0.5.0 / sva 3.54.0 already installed per that candidate's `TOOLS.md`); no packages were installed or changed. `Rscript -e "parse(...)"` confirms `examples/batch_design.R` parses; the same script was executed end to end (exit 0).
