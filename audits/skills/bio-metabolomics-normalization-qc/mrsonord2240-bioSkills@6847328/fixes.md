# bio-metabolomics-normalization-qc fixes (2026-09-16)

Worktree `F:\OpenScience\wt\metab-a`, branch `fix/r2-metab-a` (based on `openscience-fixes` @
61e60d8). Runtime: R 4.4.3 / Bioconductor 3.20 via `F:\OpenScience\audit-envs\untargeted-metabolomics-analyst\rs.sh`;
pmp 1.18.0, imputeLCMD 2.1. Data: `F:\OpenScience\audits\bio-metabolomics-normalization-qc\data\make_synthetic.R`
(mirrors the audit's own synthetic generator; same input3/input4 scenarios reproduced independently).

## Research-veto pass -- 2026-09-16

| finding | priority | change | verified (ran / help / docs) | notes |
|---|---|---|---|---|
| `impute.QRILC` run on raw (non-log) intensities per the Skill's own documented pipeline order (impute step 5, before transform step 7) silently emits negative intensities | P0 (research veto) | "Impute by Missingness Mechanism" code block: `log2()` before `impute.QRILC`, `2^x` back-transform after; added `stopifnot(min(qrilc_imputed, na.rm=TRUE) >= 0)` guard line; Pipeline Order table gets a `5a` row clarifying this log/2^x round-trip is local to the QRILC call, not a reordering of step 7; Common Errors table gets a new row | ran | Reproduced the veto on the audit's own input3 scenario (15 MNAR + 15 MAR features, seed 5/9): old pattern gave min=-776.37, 123/310 imputed values negative. Fixed pattern: min=0.66 (>=0) on the original scale, 242/310 (78%) imputed values sit below each feature's detected range, consistent with QRILC's left-censored intent. Re-verified end-to-end in a QCRSC-guard -> PQN-factor -> QRILC-fixed chain on a fresh synthetic dataset (seed 7) with no errors. All new/changed R blocks in SKILL.md (5 total) parse-checked via `parse()`. |
| `QCRSC(minQC=5)` on a batch with fewer QCs neither errors nor warns; silently returns every feature as all-NA | P1 | Added a guard line after the `QCRSC` call (`stopifnot(any(rowSums(!is.na(out_mat)) > 0))`, handles both SummarizedExperiment and plain-matrix return); new Common Errors row | ran | Reproduced the audit's input4 scenario (3 QCs, `minQC=5`, seed 21): guard correctly evaluates to FALSE (catches the all-NA failure). Cross-checked on a normal run (8 QCs, seed 22): guard evaluates to TRUE, no false positive. |
| `pqn_normalisation()`'s documented return exposes no per-sample factor, so the Skill's own phenotype-correlation guardrail has no API to call | P1 | Added a code block after the `pqn_normalisation()` call showing the *actual* documented path: `attr(normalized, 'flags')[, 'pqn_coef']` for plain-matrix input, `colData(normalized)$pqn_coef` for SummarizedExperiment input | ran | Read `pmp::pqn_normalisation` source directly: it computes `coef_med` and stores it either in `colData` (SummarizedExperiment) or `attributes(df)$flags` (plain matrix) -- confirmed `attr(normalized,'flags')[,'pqn_coef']` exists on a real run and that `normalized * pqn_factor` reconstructs the original matrix to 2.8e-14 precision. Note: this is a better fix than the audit's own suggested manual median-quotient recomputation -- that recomputation used a median reference, but `pqn_normalisation` defaults to a *mean* reference (`ref_method='mean'`), so a hand-rolled median version would silently disagree with the real output by several percent; verified this discrepancy directly (max abs diff 7.83 on ~100-scale values) before choosing the `flags`-attribute path instead. |
| Fixed `\|r\| > 0.3` phenotype-correlation cutoff trips from estimator noise alone at typical n (audit: r=0.345 at n=40 with true correlation 0) | P2 | `examples/normalize_data.R`'s guardrail check replaced with a permutation test (999 label-shuffles, empirical p<0.05) instead of a fixed r cutoff; `usage-guide.md` Tips updated to mention permutation over a fixed threshold | ran | `Rscript -e "parse(...)"` clean; full example script re-run end-to-end (unrelated seed=1 dataset): correctly still trips (permutation p=0.001) on the example's built-in true confound, and the mechanism no longer depends on an arbitrary constant. |
| "ComBat under imbalance" failure-mode entry doesn't distinguish partial imbalance (didn't reproduce the effect at 85/15 in the audit) from near-total confounding (did reproduce at 100%) | P2 | Reworded the Trigger/Mechanism to note risk scales with degree of association (chi-square / Cramer's V), and that absence of the effect at mild imbalance isn't evidence of its absence at severe imbalance | docs (Nygaard 2016 cited by the Skill; audit's own input5 vs input6 contrast) | No new tool run needed -- this is a prose-scoping fix reconciling two already-executed audit findings (input5: perfect confound, FP rate inflated; input6: 85/15 imbalance, not inflated) that the Skill's prose previously treated as one regime. |

## Unfixed

None. All five recommendations in `eval_report_bio-metabolomics-normalization-qc_result.json`
(1 P0, 2 P1, 2 P2) and the single defect named in `AUDIT.md` (same P0) are addressed above.

## Files changed

- `metabolomics/normalization-qc/SKILL.md`
- `metabolomics/normalization-qc/examples/normalize_data.R`
- `metabolomics/normalization-qc/usage-guide.md`
