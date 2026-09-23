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

# bio-experimental-design-batch-design — 2026-09-21

P2 fix batch (re-audit findings, 3 P2). Branch `fix/experimental-design-batch-design` (worktree
`F:\OpenScience\wt\experimental-design-batch-design`), commits `50189f4` (fix), `d1c2afc` (usage-guide
redundancy), `d2e88b3` (scripts/). SKILL.md 283 -> 227 lines; under the 300-line threshold, no
`references/` split. Env: `untargeted-metabolomics-analyst` via `rs.sh` (R 4.4.3, designit 0.5.0, sva 3.54.0); nothing installed.

| finding | priority | change | verified (ran / help / docs) | notes |
| --- | --- | --- | --- | --- |
| Bridge block lacks the soft imbalance warning | P2 | One shared `check_balance()` (hard confound stop + `max-min > 1` warning) now used by the primary and bridge layouts; lives in `scripts/check_balance.R` | ran | Real designit run on 60 samples / 4 plexes: bridge layout converged to case 9/8/7/6, ctrl 6/7/8/9 and the warning fired (spread 3; site spread 2), both inline and via `bridge_layout.R`. Audit's 8/8/8/6 / 7/7/7/9 table warns; a fully confounded table stops. |
| Balance check shown only for condition | P2 | `check_balance(assignment, 'batch', c('condition','sex'))` loops every covariate; a confounded second covariate stops naming it | ran | 24-sample run: condition and sex both 4/4/4; synthetic table with site aliased to plex stops with "site is confounded with plex". |
| OSAT named, no OSAT code | P2 | Claim deleted (description, Version Compatibility, tool bullet, code comment, Yan 2012 reference, usage-guide install line). OSAT absent from the env and installs barred | grep (no OSAT left except designit's `osat_score_generator`) | Chose delete over write: not installed here. |
| (own) stale "see Input 2 above" audit reference in SKILL.md | -- | removed | read | |

Also: added a checked-on install line (designit 0.5.0, sva 3.54.0, 2026-09-21).

## Left unfixed
None.

## Deleted passage -> new home
| deleted | new home |
| --- | --- |
| usage-guide "Prerequisites" install block | SKILL.md Version Compatibility "Install:" line (usage-guide points there) |
| usage-guide "Tips" (6 bullets) | SKILL.md: Single Most Important Insight, Confounding vs Blocking, Per-Method Failure Modes, Reproducibility Metadata, Decision Tree (scRNA-seq row) |
| usage-guide "What the Agent Will Do" | SKILL.md Decision Tree, Constrained Assignment, SVA, Downstream Correction, Reproducibility Metadata |
| SKILL.md SVA block's Option A/B code comments | SKILL.md SVA section prose (Option A/B bullets) plus `run_sva_safely()` in `examples/batch_design.R` |

## Moved code (runnable code goes in scripts/)
| old location | script |
| --- | --- |
| SKILL.md "Constrained Sample-to-Batch Assignment" designit block | `scripts/assign_batches.R` (ran: layout 8 per batch, cells 4/4/4) |
| SKILL.md "Verify the optimized layout" `check_balance()` | `scripts/check_balance.R` (ran: warns / stops as above) |
| SKILL.md "Reference / Bridge Channel Layout" block | `scripts/bridge_layout.R` (ran: 15 per plex, channel 16 empty, warning fires) |
| SKILL.md SVA missing-value block | not moved: duplicates `examples/batch_design.R` `run_sva_safely()`; SKILL.md points to it (example re-run, exit 0); 4-line num.sv/sva core kept inline |
