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

## P2 batch -- 2026-09-21

Worktree `F:\OpenScience\wt\metabolomics-normalization-qc`, branch `fix/metabolomics-normalization-qc` (from staging `431aa55`). Env `untargeted-metabolomics-analyst` (R 4.4.3, imputeLCMD 2.1, matrixStats 1.5.0, via `rs.sh`). Commits: `f584469` (fix), `980965f` (scripts/). SKILL.md 265 -> 262 lines: under the split threshold, no `references/` split.

| finding | priority | change | verified (ran / help / docs) | notes |
|---|---|---|---|---|
| Permutation guardrail still trips at its nominal ~5% rate on clean data; no caveat | P2 | New "Guardrail" paragraph after the PQN block in SKILL.md (permutation test, and one TRIPPED verdict can be chance: corroborate against a measured dilution quantity); `examples/normalize_data.R` verdict text says the same | ran | Example re-run; 8 seeds of the null (no group effect) give r_grp -0.25..0.30, 1/8 at p<0.05 (seed 5, p=0.047), consistent with the caveat |
| Non-positive intensities upstream of QRILC not in Common Errors | P2 | Common Errors row for `NA/NaN/Inf in 'y'`; pre-check `stopifnot(min(feature_matrix, na.rm=TRUE) > 0)` added to the "Verify around every QRILC call" line | ran | Reproduced with `impute.QRILC(log2(m))` on a matrix holding one 0: `try-error`, message `NA/NaN/Inf in 'y'`; after replacing the 0, imputation returns 0 NAs, min imputed 14.08 |
| (found while verifying, not in the audit) `examples/normalize_data.R` tripped its own guardrail on every seed | P1-grade defect in a shipped example | `fold <- ifelse(group[i]=='case', effect, 1)` returns `effect[1]` (length-1 test), so the 1.5x case effect hit all 200 features, not 20 -> `if/else rep(1, n_features)`. Drift `1 + slope*order` went negative (1192 negative intensities in the matrix) -> `exp(slope*order)` | ran | Before: seeds 1-12 all r_grp 0.39-0.69, p=0.001, r_dil 0.68-0.88. After: r_dil 0.95-1.00 on 8 seeds, held-out QC RSD drops 8/8 (e.g. 0.271 -> 0.235), r_grp near 0. The 2026-09-16 entry above that says the example "correctly still trips on its built-in true confound" was the ifelse bug, not a confound: superseded |
| (redundancy pass) usage-guide restated SKILL.md | -- | See table below | grep | |
| (scripts/) `robust_dratio_filter()` 17-line block | -- | -> `scripts/robust_dratio_filter.R` (function plus CLI); SKILL.md keeps a 2-line `source()` and the CLI usage line | ran | Rscript and `source()`: planted data, 30 clean features kept 30/30, 30 noisy (technical SD 1.5 vs 0.05) kept 0/30 |

Other code blocks (QCRSC, shiftCor, pqn_normalisation, QRILC/missForest) are 5-13 line API illustrations and stay inline.

### Deleted passage -> new home

| deleted from usage-guide.md | new home |
|---|---|
| Prerequisites: install command | SKILL.md Version Compatibility, "Install:" line |
| Prerequisites: conceptual inputs (table + metadata, matrix type, randomization) | SKILL.md, "Inputs:" line |
| What the Agent Will Do (7 steps) | already in SKILL.md Pipeline Order / decision trees; deleted |
| Tip: "QCs cluster tightly", RSD ~0% failure mode, correct only drifting features, closure, filter-before-impute, randomize | already in SKILL.md (Insight, Drift decision tree, Per-Method Failure Modes, Pipeline Order); deleted |
| Tip: lead with D-ratio; state the data stage of a CV | SKILL.md Filter section (D-ratio) plus pipeline row 3 now says "always state the data stage a CV was computed on" |
| Tip: permutation test instead of fixed r cutoff (n~40) | SKILL.md Guardrail paragraph |
| Tip: within-study relative intensities, reference material before cross-study claims | SKILL.md after Pipeline Order |

### Left unfixed

None of the 2 audit P2s. Not touched: 45 benign `simpleLoess` warnings when the example fits LOESS on 6 QC points (span 0.75); output is correct and they are suppressed by no one, but silencing them would hide the very "too few QCs" condition the Skill warns about.

### Files changed

- `metabolomics/normalization-qc/SKILL.md`, `usage-guide.md`, `examples/normalize_data.R`, `scripts/robust_dratio_filter.R` (new)
