# bio-causal-genomics-mediation-analysis fixes (2026-09-17)

Worktree `F:\OpenScience\wt\mr-med`, branch `fix/mr-mediation`, based on `openscience-fixes` @
`558aea5`. Fixer: Claude Sonnet 5. Runtime: R 4.4.3 via
`F:\OpenScience\audit-envs\mendelian-randomization-analyst\r.sh`; HIMA 2.3.4 and CMAverse 0.1.0
already installed there (candidate `mendelian-randomization-analyst`, no version changes made).
Verification scripts: scratchpad `mr-med/` (`test_hima_fix.R`, `test_cmaverse_names.R`,
`check_source.R`), independent of the audit's own scripts in `F:\OpenScience\audits\...\run\`.

| finding | priority | change | verified (ran / help / docs) | notes |
|---|---|---|---|---|
| HIMA covariate fix in SKILL.md (`factor()`) is backwards on HIMA >= 2.3 | P1 | `HIMA covariate or data.pheno error` section (SKILL.md): mechanism now names `process_var()`'s real requirement (numeric/dummy, not factor); fix rewritten to dummy-code with `model.matrix()` before calling `hima()` | ran | Own script (`test_hima_fix.R`) on synthetic n=300/p=2000/8-true-mediator data with a 3-level `batch` covariate: `factor(batch)` -> `Error: Non-numeric variable(s) detected: batch...` (confirms the documented fix is backwards); `model.matrix()` dummy-coded version succeeds and recovers 5/8 planted mediators, 0 false positives |
| HIMA return type documented as `data.frame`; actually a list | P1 | Code comment after the `hima()` call (SKILL.md) rewritten to state the real list-of-class-"hima" structure and show `result$ID`/`length(result$ID)`; added a new Common Errors row for the silent-`NULL` failure mode | ran | Same script: `class(result)` = `"hima"`, `is.list(result)` TRUE; precisely checked with `identical()` -- `nrow(result)` and `rownames(result)` are both `NULL` (not `NA` as the audit's report stated; corrected to the verified fact) with no error thrown |
| CMAverse component names in SKILL.md prose (`intref`/`intmed`) stale vs verified output (`ERintref`/`ERintmed`) | P2 | Decision-tree row, 4-way "Goal" line, and the CMAverse column-name paragraph (SKILL.md) updated to the ER-prefixed names for the binary/logistic case; same fix applied to the shipped `examples/cmaverse_4way.R`, which carried the identical stale comment | ran | Own script (`test_cmaverse_names.R`), logistic outcome, `EMint=TRUE`, CMAverse 0.1.0: confirmed columns `Rcde Rpnde Rtnde Rpnie Rtnie Rte ERcde ERintref ERintmed ERpnie ERcde(prop) ERintref(prop) ERintmed(prop) ERpnie(prop) pm int pe`; bare `intref`/`intmed` absent |
| No practice-boundary section for clinical-adjacent use | P2 | Added a `## Scope` section (SKILL.md): population-level ACME/CDE/PIE estimates do not license an individual treatment decision; decline and redirect to the treating clinician | docs (matches the pattern already used in `copy-number/germline-cnv-interpretation` and confirmed correct by the audit's own Input 6 transcript) | |
| No data-safety note for individual-level genomic mediator data | P2 | Same `## Scope` section: de-identify individual-level genotype/expression/methylation mediator data before analysis; don't echo raw per-subject values in errors/logs | docs | |
| (Found while fixing) SKILL.md's HIMA install note said GitHub-only, archived from CRAN, needs `scalreg` | not in `recommendations[]`, but explicitly flagged in TOOLS.md note 2 | Tool Install Notes row rewritten: HIMA is back on CRAN, `BiocManager::install('qvalue')` then `install.packages('HIMA')`, no `scalreg`; Version Compatibility line updated the same way | ran | `packageDescription("HIMA")$Repository` = `"CRAN"`, Version 2.3.4, `scalreg` not installed, `qvalue` present from Bioconductor 3.20 -- independent of TOOLS.md's own account |
| (Found while fixing) SKILL.md's and the shipped example's CMAverse "verify column names" instruction pointed at `summary(result)$results`, which doesn't exist | internal defect, same area as the P2 above | Both places corrected to `summary(result)$summarydf` | ran | `test_cmaverse_names.R`: `summary(result)$results` is `NULL`; `summary(result)$summarydf` holds the real 17-row table with the confirmed names above |

All 5 `recommendations[]` entries (2 P1, 3 P2) fixed, plus two defects found while fixing (stale HIMA
install note, wrong `summary()` accessor in both SKILL.md and the shipped example). Nothing left
unfixed. Both changed R snippets and the changed example script re-verified: `test_hima_fix.R` and
`test_cmaverse_names.R` were run to completion against the fixed logic (not merely parsed), and
`examples/cmaverse_4way.R` still parses (`Rscript -e "parse(...)"`) after the edit.

Nothing needs Sam.

## 2026-09-17, second pass (re-audit of `7f94fdd`, 88/100 Production Ready)

Worktree unchanged (`F:\OpenScience\wt\mr-med`, branch `fix/mr-mediation`), starting at `7f94fdd`.
Re-audit evidence: `F:\OpenScience\audits\bio-causal-genomics-mediation-analysis\` (inputs 8-9, new
this round). Both new findings are in the medDML section, never exercised by the pre-fix audit.
Verification: own script `verify_meddml.R` (scratchpad), independent of the audit's `run/input8_meddml_doubleml.R` -- same causalweight 1.1.4, different seeds/covariate draws.

| finding | priority | change | verified (ran / help / docs) | notes |
|---|---|---|---|---|
| medDML's real output columns undocumented in SKILL.md | P2 | "Double-ML Doubly-Robust Mediation" code block (SKILL.md): added a comment after the `medDML()` call giving the real `$results` shape (3x6 matrix, rows `effect`/`se`/`p-val` x columns `total, dir.treat, dir.control, indir.treat, indir.control, Y(0,M(0))`) and name-based extraction lines; prose below the block now names what `dir.treat`/`dir.control`/`indir.treat`/`indir.control` mean | ran | `verify_meddml.R`, n=800 named covariates, causalweight 1.1.4: confirmed exact column/row names by `colnames()`/`rownames()`, then extracted `results['effect','total']` = 0.5340 and `results['effect','indir.treat']` = 0.2927 by name |
| medDML crashes with unhelpful `subscript out of bounds` on sparse/collinear covariates, undocumented | P2 | New Common Errors row (SKILL.md): names the cause (`hdm::rlassologit`'s internal cross-fitted Lasso needs named columns and enough independent variation) and the fix (named columns via `as.matrix(dat[, covariates])`, n >= ~500, drop near-collinear covariates) | ran | `verify_meddml.R`: n=150, 2 unnamed near-collinear columns via bare `cbind()` -> `subscript out of bounds`, reproducing the audit's Input 8 Part C; n=800 with named `age`/`sex`/`bmi` columns converges cleanly (same script, both parts) |

2/2 P2s fixed. New code block re-verified with `Rscript -e "parse(text=...)"` (PARSE OK) after editing SKILL.md. Nothing left unfixed from this round's `recommendations[]`.

### Redundancy pass (same session, per `FIX_BRIEF.md` "Remove redundancy, every pass")

Before (post-P2-fix commit): SKILL.md 492 lines, usage-guide.md 127 lines.
After: SKILL.md 494 lines, usage-guide.md 71 lines.
(SKILL.md net +2: several genuinely guide-only facts were folded into existing sections as they
were found by grep verification, offset by deleting nothing from SKILL.md itself -- no internal
SKILL.md repetition of the "Tips list re-saying a failure-mode section" shape described in the
brief was found; its several tables/sections that repeat the same numeric thresholds (sims,
rho_crit, E-value, conditional F) serve distinct functional roles -- decision default, failure-mode
fix, checklist, lookup table, reviewer-rebuttal script -- not one list echoing another, so left as
is.)

Deleted-passage -> new-home map. Every usage-guide.md passage was checked by `grep` against
SKILL.md's actual text, not by section title alone -- three facts that looked like duplicates by
keyword match on a first pass turned out to be partially new on closer check and were folded in
rather than dropped:

| deleted from usage-guide.md | disposition | new home / note |
|---|---|---|
| Prerequisites install block (`install.packages(...)`, `remotes::install_github(...)`) | superseded, not moved | `## Tool Install Notes` already had every package correctly -- **except** the guide's own HIMA line (`remotes::install_github('YinanZheng/HIMA')`), which was the *stale, pass-1-superseded* GitHub install path; SKILL.md's table already carries the pass-1-verified CRAN install. Disagreement resolved in favor of SKILL.md (audit-verified, `checked 2026-09-17`); guide now points at the table instead of repeating (and re-breaking) it. |
| Compute-time estimates (bootstrap minutes, HIMA 30-60min, BAMA 1-6h, medDML 10-30min) | moved | New `Compute time` column on `## Tool Install Notes` -- not previously in SKILL.md at all |
| "What the Agent Will Do" 8-step pipeline | deleted | Every step already covered: 1-2 by `## Decision Tree by Scenario`, 4 by `## Quantitative Thresholds`, 5 by `## Required Reporting for Publication`, 6 by the HIMA decision-tree row + FDR threshold row, 7 by `## Quantitative Thresholds` (conditional F rows) + Two-step MR sections, 8 by `## Common Errors`. Confirmed each by grep before deleting. |
| Tips list (13 bullets) | 10 deleted as duplicate, 3 folded in | Verified bullet-by-bullet, not by topic-title match. Pure duplicates (grep-confirmed against SKILL.md's own wording): sequential-ignorability-always, HIMA1-vs-HIMA2 + version pin, HIMA outcome-family limits (`HIMA-Pois`/`HIMA-Cox` -- present in the Algorithmic Taxonomy "Fails when" column, missed on a first `hima_pois` casing-specific grep), 1000/5000 sims floor, proportion-mediated convention, difference-vs-product, rare-outcome OR, exposure-induced-confounder->msm, observational-vs-MR comparison, MVMR conditional F, medsens probit. Folded in as new content: (1) BCa case-sensitivity (`'bca'` not `'BCa'`) -- appended to the "Bootstrap iterations too low" Fix line; (2) cell-composition confounder with the Houseman/RPC method name and the `COV.XM`/`COV.MY` argument names -- SKILL.md only had the generic word "cell composition" with no actionable detail, appended to the "HIMA mediator-type vs outcome-type mismatch" Fix; (3) measurement-error correction mechanism (regression calibration = replace mediator with conditional expectation) -- SKILL.md's Reviewer Pushback row only named the method, not the mechanism, expanded in place. |
| "BAMA when-to-prefer" bullet | moved | New paragraph after `## Decision Tree by Scenario`'s table -- SKILL.md had no BAMA-vs-HIMA2 preference rule before |
| Mediational E-value formula (`E = RR + sqrt(RR*(RR-1))`) | moved | Appended to `### Mediational E-Value for Sensitivity` -- SKILL.md named the method but never gave the formula |
| Cohort Considerations section (UK Biobank / FinnGen / ALSPAC) | deleted, not moved | Human-facing framing ("which cohort/biobank fits"), not something the agent acts on mid-analysis; no SKILL.md section referenced it and it names no agent-actionable threshold or command. Kept out per the brief's "only what is for the human choosing the Skill" rule -- borderline, logged here in case Sam disagrees. |

One disagreement found and resolved (HIMA install path, row 1 above) -- kept SKILL.md's version
because it is the one pass-1 already verified by running (`packageDescription("HIMA")$Repository`).
Every other deleted passage was confirmed already present in SKILL.md, or moved, by grep before
removal from usage-guide.md.
