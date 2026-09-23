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

## 2026-09-21, P2 batch fix + split + scripts

Worktree `F:\OpenScience\wt\causal-genomics-mediation-analysis`, branch `fix/causal-genomics-mediation-analysis`, from staging `431aa55`. Commits: `816010d` fix, `a19fec3` split, `247c841` example fix, `e46d106` scripts. Env `mendelian-randomization-analyst` (R 4.4.3, EValue 4.1.4, HIMA 2.3.4, mediation 4.5.1, CMAverse 0.1.0, MVMR, TwoSampleMR). Audit had 1 P2 (input 12); not fixed by the earlier fix (E-value block still had `hi=NULL`).

| finding | priority | change | verified (ran / help / docs) | notes |
|---|---|---|---|---|
| `evalues.RR(acme_rr, lo=acme_lower_rr, hi=NULL)` crashes (`hi` defaults to `NA`) | P2 | SKILL.md E-value block: dropped `hi`, comment explains the crash | ran | Own script: old form -> try-error; new form returns E-values 1.9245 / 1.4317, asserted equal to `RR+sqrt(RR(RR-1))` for RR 1.30 / 1.10; `args(evalues.RR)` shows `hi = NA` |
| (found) Common Errors row said `hima()` RHS vars may be "numeric or factor", contradicting the HIMA factor-rejection section | internal contradiction | Row now says numeric or dummy-coded via `model.matrix()` and points to `references/hima-ewas.md` | ran earlier (2026-09-17 `test_hima_fix.R`) | |
| (found) `examples/eqtl_mediation.R` multi-gene loop crashed: `object 'med_form' not found` (bootstrap `mediate()` re-evaluates the model call outside the function) | shipped example crashes | Formula and data baked into the `lm`/`glm` calls with `bquote()` | ran | Before: exit 1; after: exit 0, two-gene results table printed |
| (found) HIMA inline block did `na.omit(dat)` but passed the un-subset `M_matrix` (row mismatch when any NA) | wrong-behavior in shipped snippet | Now in `scripts/hima_ewas.R`, which subsets `M_matrix` with the same `complete.cases` mask | ran | Synthetic n=300, p=500, 6 planted mediators, one NA row, 3-level character covariate: recovers exactly cg1-cg6, 0 false positives; also serial and `ncore=2` |
| (found) Deleted single-mediator block fed a logit outcome to `medsens()` (Common Errors says logit fails) | wrong snippet | Block replaced by pointer to `examples/eqtl_mediation.R` and `examples/sensitivity_analysis.R` (probit) | ran | Both examples exit 0 |

Fixed 1/1 audit P2, plus 4 defects found.

### Left unfixed
None from the audit. Not moved to `scripts/` (under 15 lines, or unrunnable here): the two-step MR sketch (13 lines, needs OpenGWAS auth), the medDML call and the E-value block (short).

### Redundancy pass
Already done 2026-09-17 (usage-guide.md 71 lines, each fact once); skipped.

### Split (SKILL.md 496 -> 270 lines, before the scripts commit)
Verbatim moves, verified by multiset comparison of non-blank lines (only the 7 decision-tree rows that gained a pointer differ) and `parse()` of every moved R fence.

| old location (SKILL.md) | new home |
|---|---|
| `## 4-Way Decomposition Framework`; `### Exposure-induced M-Y confounder`; `### 4-Way Decomposition with Exposure-Mediator Interaction` | `references/cmaverse-4way.md` |
| `### HIMA covariate or data.pheno error`; `### HIMA mediator-type vs outcome-type mismatch`; `### High-Dimensional EWAS Mediation (HIMA2)` | `references/hima-ewas.md` |
| `### Two-step MR instrument independence`; `### MR-Mediation: Two-Step vs MVMR-Mediation`; `### MR-Mediation: Total Minus Direct via MVMR` | `references/mr-mediation.md` |
| `### Time-Varying Mediation Methods`; `### Double-ML Doubly-Robust Mediation` | `references/time-varying-and-dml.md` |
| `## Reconciliation: Observational vs MR Mediation`; `## Anticipated Reviewer Pushback` | `references/reconciliation-and-reviewers.md` |

### Scripts (SKILL.md 270 -> 257 lines)

| old location | disposition |
|---|---|
| `references/hima-ewas.md` HIMA `hima()` block | -> `scripts/hima_ewas.R` (invocation left in the reference) |
| `SKILL.md` single-mediator block | duplicate of `examples/eqtl_mediation.R` + `sensitivity_analysis.R`; deleted, pointer |
| `references/cmaverse-4way.md` `cmest` block | duplicate of `examples/cmaverse_4way.R`; deleted, pointer |
| `references/mr-mediation.md` MVMR block | duplicate of `examples/mvmr_mediation.R`; deleted, pointer |

All four examples were run (exit 0) to back the pointers.

## 2026-09-21, final pass -- Phase 1 (fixer+auditor, checkpoint before re-audit)

Worktree unchanged (`F:\OpenScience\wt\causal-genomics-mediation-analysis`, branch
`fix/causal-genomics-mediation-analysis`), tip `e46d106`. No entry for this Skill in
`fixes/README.md`'s revisit list, and every prior fix-log finding above was already resolved. This
phase re-verified every runnable block independently (fresh synthetic data, fresh scratchpad scripts,
not reusing the earlier fix passes' own verification scripts) rather than finding new defects:
`examples/eqtl_mediation.R`, `examples/sensitivity_analysis.R`, `examples/cmaverse_4way.R`,
`examples/mvmr_mediation.R`, `scripts/hima_ewas.R` (via its documented CLI invocation, fresh n=300/
p=500/6-planted-mediator/NA-row/3-level-covariate dataset, recovered exactly 6/6), the
`references/hima-ewas.md` inline `model.matrix()` block (independent n=250/p=200/5-planted dataset,
recovered exactly 5/5), the `references/time-varying-and-dml.md` medDML block (fresh n=800 data,
confirmed `$results` shape/names and by-name extraction), the `SKILL.md` E-value block (confirmed the
fixed form works and the pre-fix `hi=NULL` form still crashes as documented), and the Common Errors
claim that `medsens()` rejects a logit-link fit (reconfirmed verbatim). No package installs were
needed; everything used was already in the `mendelian-randomization-analyst` env.

No new fixes made -- nothing broken was found. One pre-existing, already-documented blocker
reconfirmed rather than newly discovered: the two-step MR code sketch in `references/mr-mediation.md`
needs a live OpenGWAS JWT token (unauthenticated `extract_instruments()` still 401s, reconfirmed live
this session); its five called functions all exist in TwoSampleMR 0.7.9 with matching signatures and
the block parses clean, so only the network call is gated, not the code. Full detail:
`F:\OpenScience\audits\_final_pass\bio-causal-genomics-mediation-analysis\CHECKPOINT.md`.

### Left unfixed
Same as before (two-step MR sketch, needs OpenGWAS auth). Nothing else.
