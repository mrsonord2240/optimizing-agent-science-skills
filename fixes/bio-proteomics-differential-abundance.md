# bio-proteomics-differential-abundance fixes (2026-09-15)

Branch `fix/proteomics` (worktree `F:\OpenScience\external\bioSkills-wt-proteomics`). Runtime: R via `r.sh` (limma 3.62.2, DEqMS 1.24.0, proDA 1.20.0, ashr 2.2.63) and the candidate venv (pandas 3.0.5, scipy 1.18.1, statsmodels 0.15.0). SKILL.md blocks were extracted and run on the audit data (`proteinGroups.txt` 4 v 4 with batch, `three_arm_log2.csv`, `plasma_12v12.csv`).

| finding | priority | change | verified (ran / help / docs) | notes |
|---|---|---|---|---|
| proDA block calls a coefficient that does not exist | P1 | `test_diff(fit, 'conditionTreatment')`, design `~condition + batch`; Common Errors row | ran: 1500 rows, 40 at adj_pval < 0.05 | |
| limma and DEqMS blocks break on real MaxQuant matrices | P1 | Valid-value filter (>= 2 per group) before `lmFit` with Approach text; `stopifnot(all(fit2$df.residual > 0))` before `spectraCounteBayes`; two Common Errors rows | ran: 1500 -> 1300 rows, `eBayes(trend, robust)` OK, 99 calls / 3 null; DEqMS with no recycling warning | |
| `treat()` silently drops trend and robust | P1 | `treat(fit2, lfc, trend = TRUE, robust = TRUE)` into `fit_treat` (SKILL.md and example); Approach and Common Errors | ran: `fit_treat$s2.prior` varies with intensity (df.prior median 153.8), 83 calls; example 37 | ashr and DEqMS keep using the eBayes `fit2` |
| Downshift and double-filter FDR claims overstated | P1 | Insight 1, downshift failure mode, double-filter Approach/Symptom and two threshold rows: sigma is the run-wide SD, imputed FC is set by the constant (wing), no FDR guarantee; >50% FDR regime-specific | method change on audit run evidence: Input 3 (downshift 0-1 false positives, 62-68 vs 104 calls, logFC vs AveExpr r = -0.96) and Input 7 (double filter 1.3-3.8% realized FDR) | recommendation against imputation and double filtering kept |
| Example "median centering" scales log values | P1 | `sweep()` subtraction of column medians plus global median | ran: `examples/limma_analysis.R` exit 0 (41 significant, 37 treat); `parse()` OK | |
| msqrob2 and MSstats promised but not provided | P2 | none | -- | adding code blocks is new content |
| Design rename hard-codes two groups | P2 | `colnames(design)[seq_len(nlevels(cond))] <- levels(cond)`; Common Errors row | ran on three-arm data: design Control, DrugA, DrugB, batchD2, batchD3; `makeContrasts` + `eBayes` OK on 1074 rows | |
| No stop condition for n=1 or clinical questions | P2 | Scope sentence; `ValueError` when no protein has >= 2 values per group (SKILL.md block and example); Common Errors row | ran: n=1 case raises the ValueError; 12 v 12 tests 826 proteins; example exit 0, `py_compile` OK | |
| Silent defaults in ashr and proDA outputs | P2 | Drop NA rows before `ash()`; comment not to report proDA `diff` for proteins unobserved in a group | ran: 1300 shrunk, 0 zero PosteriorMean | |

Also: MSstats taxonomy row now says AFT censored imputation exists only in `dataProcess(MBimpute = TRUE)`, matching the quantification fix; version line changed to the checked versions.

Left unfixed:
- P2 msqrob2 / MSstats code blocks: new content, out of scope.
