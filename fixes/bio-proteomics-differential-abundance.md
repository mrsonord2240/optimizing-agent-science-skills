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

---

# Pass 3 — 2026-09-15 (re-audit at 82, Limited Release, CORE floor 85)

Branch `fix/proteomics-3` (worktree `F:\OpenScience\external\bioSkills-wt-prot3`), branched from
`fix/proteomics-2` @ `d1b8fdc`. Commit `e8d2cd4`. Evidence: the re-audit at
`F:\OpenScience\audits\bio-proteomics-differential-abundance\` (2026-09-15 14:45/14:47). Runtime: R 4.4.3
via `r.sh` (limma 3.62.2, DEqMS 1.24.0, proDA 1.20.0, ashr 2.2.63), Python 3.12 shared venv.

| finding | priority | change | verified (ran / help / docs) | notes |
|---|---|---|---|---|
| No guard for paired/blocked designs: the per-condition valid-value filter does not make the contrast estimable, so limma tested rows with 0 residual df or partly NA coefficients, and the Skill's own `stopifnot(all(fit2$df.residual > 0))` in the DEqMS block fired (Input 8) | P1 | estimability filter after `lmFit` — `fit <- fit[fit$df.residual > 0 & rowSums(is.na(fit$coefficients)) == 0, ]` — plus Approach text, a Common Errors row, and the same two lines in `examples/limma_analysis.R` | ran on `data/paired_donor_log2.csv` (6 donors x Unstim/LPS): realized FDR **12.0% -> 4.8%** (63 calls, 3 null), 18 zero-df and 120 partial-NA rows dropped, and the DEqMS block then runs verbatim (stopifnot passes) at 4.8% | internal contradiction: the DEqMS `stopifnot` asserts exactly what the upstream filter was supposed to guarantee. The audit's own alternative (>=2 complete donor pairs) only reached 7.2% |
| regression check on the same change | — | — | ran on the 4 v 4 batch data: 1300 -> 1297 rows, still **99 calls / 3.0% FDR**, DEqMS 99 / 3.0%, `treat(1.2)` 83 / 0 null — identical to the audit's Input 1 numbers | also removes the rows behind the unexplained `Partial NA coefficients for 3 probe(s)` warning the auditor docked a code point for |
| Decision tree called proDA the "correct verdict for undetected in one group" (Input 3) | P2 | that row and the proDA Approach now say proDA is honest but underpowered for on/off proteins at n=3-5, and those belong in a separate undetected list | ran independently rather than reading the auditor's output file: proDA 1.20.0 `~condition + batch` on the 4 v 4 data called **0 of 11** true on/off proteins, best `adj_pval` 0.17 | a claim contradicted by what the audit actually ran |
| Python path dropped untestable proteins silently, contradicting the limma Approach's own "report proteins removed by the filter separately" (Input 4) | P2 | `differential_abundance()` returns a second frame of untestable proteins with `n_case` / `n_ctrl` (SKILL.md block and Approach, and `examples/differential_abundance.py` including its `__main__`) | ran on `data/plasma_12v12.csv`: 826 tested / 39 called / 0 false positives unchanged, **74 untestable now reported**, of which `{on_off: 8, down: 3, up: 1}` and the rest null — exactly the set the audit found dropped | internal contradiction between the two workflows |
| `usage-guide.md` contradicted the calibrated SKILL.md — downshift "manufactures systematic false positives ... collapsed within-group variance" and the double filter "inflates realized FDR above 50%" — and the SKILL.md header line still said imputation "manufactures false positives" (Input 7) | P2 | carried the calibrated wording (run-wide sigma, FC set by the imputation constant, no FDR guarantee, regime-specific inflation) into the usage guide's Missing-Value Handling and Tips, and into the SKILL.md header line | text only; wording taken from the already-verified SKILL.md Insight 1 and `treat()` Approach | a stale-text supersede, no method change |

Also: both examples re-run — `limma_analysis.R` exit 0 (400 tested / 41 significant / 37 treat, identical to
the audit's smoke test) and `parse()` clean; `differential_abundance.py` exit 0 (400 / 43 / 0 untestable) and
`py_compile` clean. All six SKILL.md blocks re-extracted after editing and run verbatim. Pure ASCII.

## Left unfixed

- **P2 — msqrob2 / MSstats feature-level blocks (Input 9).** Still new content: two new workflow sections
  rather than a correction to anything present. Note for a later pass: msqrob2 **1.14.1 is now installed**
  in `F:\OpenScience\audit-envs\mass-spec-proteomics-analyst\R-lib` (the re-audit ran with it absent), so
  such a block could now be verified by running it. The audit's alternative — deleting msqrob2/MSstats from
  the description and decision tree — would narrow real coverage, so I did not take it. **Needs Sam's call.**
