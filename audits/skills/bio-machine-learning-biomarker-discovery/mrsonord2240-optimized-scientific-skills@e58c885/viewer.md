> - Provider binding: exact committed bytes at [mrsonord2240/optimized-scientific-skills@e58c885](https://github.com/mrsonord2240/optimized-scientific-skills/tree/e58c8855faaf8dcba2341453d73b62bcade3e78c/skills/bio-machine-learning-biomarker-discovery) match audited candidate `27580088c038f830586abc45faa573419e8cf255ef355932b40840c41eda3134` byte for byte. The scientific report was neither re-executed nor rewritten.

> **Audit record for `bio-machine-learning-biomarker-discovery`**
> - Audited working candidate `27580088c038f830586abc45faa573419e8cf255ef355932b40840c41eda3134`; exact candidate provenance is in [source-identity.json](source-identity.json).
> - Derived from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/machine-learning/biomarker-discovery), authored by [GPTomics](https://github.com/GPTomics) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-10-03 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test inputs and provenance are described in the published scripts/inputs and audit body; raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer: bio-machine-learning-biomarker-discovery

Generated: 2026-10-03  
Phase: independent final re-audit (lane 3a-1, full mode)  
Exact candidate: `27580088c038f830586abc45faa573419e8cf255ef355932b40840c41eda3134` (files=6, bytes=37081)

## Outcome

Independent final re-audit of the exact candidate: score **88/100**, **Production Ready**, static 91, execution average 85.6, Layer 1 34.1, Layer 2 51.4, assertions 27 of 29 (93.1 percent), both vetoes PASS, no open P0 or P1. All six initial findings (BD-001 P1, BD-002 to BD-006 P2) are resolved on re-test: BD-001 stability selection is seeded, per-subsample standardized, budgeted by q, bit-reproducible, unit-invariant and null-calibrated; BD-002 the scoring pin and size table reproduce exactly; BD-003 to BD-006 verified. Two new P2 observations (RA-001 rare-class robustness, RA-002 partition caveat) do not block readiness and are both fixable with text only. The candidate bytes were not modified; identity re-verified after execution.

## Summary table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---:|---|---:|---:|---:|---:|:---:|
| 1 | Canonical | 36 | 55 | 91 | 5/5 | ✅ |
| 2 | Variant A | 35 | 52 | 87 | 4/4 | ✅ |
| 3 | Variant B | 35 | 51 | 86 | 5/5 | ✅ |
| 4 | Edge | 36 | 56 | 92 | 5/5 | ✅ |
| 5 | Stress | 35 | 54 | 89 | 4/4 | ✅ |
| 6 | Adversarial | 28 | 40 | 68 | 1/3 | ❌ |
| 7 | Scope Boundary | 34 | 52 | 86 | 3/3 | ✅ |

**Execution average:** 85.6/100  
**Assertion pass rate:** 27/29 (93.1%)  
**Static score:** 91/100  
**Arithmetic:** 91 x 0.4 = 36.4; 85.6 x 0.6 = 51.4; 36.4 + 51.4 = 87.8 -> **88/100**  
**Grade:** Production Ready (score band Production Ready)

## Veto gates

Skill veto: **PASS**. Research veto: **PASS**.

- T1 stability: PASS. All six SKILL.md python blocks and all three scripts ran rc 0 under -W error::FutureWarning at 1,000 probes and (blocks 0-5, stability script) at the full 7,129 probes on sklearn 1.9.1 / numpy 2.5.3 / Boruta 0.4.3 / mrmr-selection 0.2.8; zero warnings or tracebacks.
- T2 contract: PASS. Documented outputs held: stability_selection returns (frequencies, Nogueira index) with a NaN index and the snippet message when nothing is selected; coef_ is (1, p); support_/support_weak_ masks; MRMRSelect.cols_.
- T3 determinism: PASS. stability_selection is deterministic: identical seed gives bit-identical frequencies (raw and rescaled, 1,000 and 7,129 probes; my own synthetic data too), seed 1 or 7 differs (maxdiff 0.15-0.16). Both bundled scripts are seeded.
- T4 security: PASS. No network, credentials, shell-out or destructive operation; scripts write nothing.
- M1 scientific integrity: PASS. Every number stated in SKILL.md for stability selection and scoring was re-measured and matches (see Lead verification); citations are named works; the Meinshausen-Buhlmann bound is quoted correctly as q^2/((2*pi_thr-1)*p) under exchangeability.
- M2 practice boundaries: PASS. Research-use selection guidance; routes unbiased performance to model-validation, refuses to read a minimal-optimal list as "the biomarkers", states that stability is not evidence of signal and that the Golub numbers are one dataset and partition.
- M3 methodological ground: PASS. Selection, scaling and tuning verified to be fit on training rows only (held-out rows replaced by garbage with labels flipped leave scaler, selected columns, coefficients, best_params_ and inner CV scores bit-identical); the select-before-CV leak is real (positive control) and reproduced on permuted labels; the null control for stability selection holds on real and self-built data.
- M4 code usability: PASS. All shipped runnable surfaces execute; one robustness gap (rare-class labels give a misleading ValueError, RA-001) fails loudly, never silently.

## Inputs

### Input 1 (Canonical): Leakage-safe Pipeline, nested GridSearchCV and in-fold MRMRSelect (SKILL.md blocks 0-2) on Golub, with held-out perturbation and permuted-label null

Status COMPLETED. Blocks 0-2 rc 0 under -W error::FutureWarning at 1,000 probes (2/14/20 s) and 7,129 probes (7/90/78 s): AUC 0.990 +/- 0.030, nested 0.99, mRMR 1.0. Perturbing held-out rows (values and labels) on folds 0 and 3 left scaler mean, selected columns, coefficients, best_params_, inner CV scores and mRMR cols_ bit-identical; the same perturbation changes a select-on-all-rows control (6 of 20 columns). Permuted labels, 5 draws, 1,000 probes: select-before-CV AUC 0.66 mean (0.55-0.78) vs in-pipeline 0.48 vs nested 0.47.

Specialized dimensions: methodological_validity 18, code_executability 14, data_quality_control 9, reproducibility 9, security 5.

- PASS: Scaler and SelectKBest inside the Pipeline are fit on training rows only (leakage_tests.py: scaler.mean_, get_support() and coef_ identical after held-out rows replaced by N(500,300) with labels flipped (folds 0, 3))
- PASS: Nested GridSearchCV never lets tuning see the outer test fold (best_params_ and inner mean_test_score identical after the same perturbation; outer fold score changes (1.0 -> 0.4/0.8))
- PASS: MRMRSelect runs and selects inside the fold (cols_ identical after perturbation; K=20; AUC 1.0)
- PASS: The leaky select-before-CV gap reproduces on permuted labels (0.66 vs 0.48 (1,000 probes, k=20); script p=5000 shows 1.00 vs 0.56; positive control confirms test power)
- PASS: Every block runs warning-free under -W error::FutureWarning at both sizes (logs/snip012_1000.log, snip012_full.log)

### Input 2 (Variant A): BorutaPy snippet and boruta_feature_selection.py

Status COMPLETED. SKILL.md block 3: real labels 90 confirmed / 20 tentative at 1,000 probes (71 s; 96 s at 7,129); permuted labels (default_rng(1)) 8 confirmed. Script: 5/5 module members confirmed by Boruta, L1 4/5, both counts computed and printed.

Specialized dimensions: methodological_validity 17, code_executability 13, data_quality_control 8, reproducibility 9, security 5.

- PASS: Snippet returns confirmed/tentative masks on numpy input without warnings (logs/boruta_inspect.log, snip3_1000.log, snip3_full.log)
- PASS: Permuted labels confirm few features (8 of 1,000 probes (0.8 percent) with perc=100)
- PASS: Script printed counts equal what runs (BD-005) (prints Boruta 5/5 and L1 4/5 from computed values; the old "~1" claim is gone)
- PASS: Script is seeded and warning-free (logs/boruta_1000.log rc 0)

### Input 3 (Variant B): Elastic-net LogisticRegressionCV with scoring pinned to accuracy: stated size table and partition dependence

Status COMPLETED. Stated table reproduced exactly on the stated partition (1,000 probes, cv=5): selected 601 / 203 / 148 for neg_log_loss / roc_auc / accuracy; permuted labels 16 / 0 / 0; outer AUC 0.991 / 0.983 / 0.991. Other inner partitions (shuffled seeds 1, 2): neg_log_loss 436 / 437, roc_auc 53 / 96, accuracy 150 / 150. sklearn 1.9.1 emits the FutureWarning naming the 1.11 default change to neg_log_loss. Block 4: 39 s at 1,000 and 278 s at 7,129 under load.

Specialized dimensions: methodological_validity 17, code_executability 13, data_quality_control 8, reproducibility 8, security 5.

- PASS: Stated 601/203/148 and permuted 16/0/0 reproduce (logs/bd002.log STATED PARTITION)
- PASS: Stated held-out AUC 0.991/0.983/0.991 reproduces and is within 0.01 (same log)
- PASS: The sklearn 1.11 default-change statement is accurate and the pin is explicit (scoring_default_warn.py: FutureWarning text names accuracy -> neg_log_loss in 1.11)
- PASS: The Skill does not overgeneralize the size table from one partition (text says one dataset and partition and to re-check on your data; accuracy is the most partition-stable (148-150) so the pin is defensible for a compact signature, though roc_auc size swings 53-203 (RA-002))
- PASS: Snippet runs warning-free at both sizes (logs/snip4_1000.log, snip4_full.log)

### Input 4 (Edge): scripts/stability_selection.py on Golub: determinism, unit invariance, permuted-label null and every stated number at both sizes

Status COMPLETED. 1,000 probes (q=14): real labels 2 / 2 / 2 stable (raw / standardized / rescaled), Nogueira 0.25; 11 permutations: 0 stable in 10, one probe (454) at 0.81 in perm_109. 7,129 probes (q=37): 5 / 5 / 5 stable (probes 1778, 1833, 2287, 4846, 4950), Nogueira 0.228; 0 stable in all 11 permutations, highest frequency 0.57 (the snippet permutation; the 10 staged sets reach 0.52). Same seed bit-identical, seed 1 differs (maxdiff 0.16 / 0.15). One call 1-3 s and 15-24 s.

Specialized dimensions: methodological_validity 18, code_executability 14, data_quality_control 9, reproducibility 10, security 5.

- PASS: Identical seed gives identical frequencies; a different seed differs (determinism_1000.log, determinism_full.log: maxdiff 0.0 vs 0.16/0.15)
- PASS: Real-label counts 2/2/2 and 5/5/5 across raw, standardized and rescaled input match SKILL.md (stab_1000.log, stab_full.log; frequencies identical)
- PASS: Permuted null matches the stated 0-in-10-of-11 (1,000) and 0-in-all-11 with highest 0.57 (7,129) (NULL SUMMARY lines in both logs)
- PASS: Empty selection is reported rather than silent NaN (q=0 returns a NaN index; the snippet prints "no features selected")
- PASS: Wording is honest: approximate invariance, non-zero null possible, count over runs (one probe at 0.81 in a 1,000-probe permutation is exactly the case the text warns about)

### Input 5 (Stress): Independent self-built null: pure-noise features, planted true features, units, determinism (n=100-120, p=2000)

Status COMPLETED. Pure-noise X and y, 8 draws, q=19: 0 stable in all (max frequency 0.22-0.57; EV bound is 1). Planted 5 of 2000 (moderate signal), 6 draws: 0-2 of 5 recovered, 0 false. Planted beta 2.5 (n=120), 6 draws: 1/4/0/4/1/4 of 5 recovered, 0 false stable; permuted-label nulls gave 0 stable in 5 draws and 1 (frequency 0.74) in one. Rescaled exp(N(0,2))*X+5, standardized and x1000 inputs give identical frequencies (maxdiff 0.00).

Specialized dimensions: methodological_validity 18, code_executability 13, data_quality_control 9, reproducibility 9, security 5.

- PASS: Near-zero stable features under pure noise (0 stable in 8 independent draws; mean 0.0 vs bound EV=1)
- PASS: Planted features dominate the stable set and no false feature is called stable on real signal (strong planting: 14 true vs 0 false over 6 draws; moderate: 7 true vs 0 false)
- PASS: Unit invariance on raw, standardized, rescaled and x1000 input (maxdiff 0.00 in all comparisons)
- PASS: Recall is not oversold (recall is low to moderate (0-4 of 5): the Skill claims control of false selections and says a count not clearly above its null is not a signature; it makes no recall claim)

### Input 6 (Adversarial): Rare-class labels in stability_selection (n=72, p=300, subsamples of 36 are not stratified)

Status PARTIAL. With 20 positives of 72 the function runs and recovers the 3 planted features. With 8, 4 or 2 positives some n/2 subsample lacks a class and the call raises a ValueError whose text blames liblinear "multiclass classification (n_classes >= 3)", which misleads: the cause is a single-class subsample. The failure is loud, never silent.

Specialized dimensions: methodological_validity 13, code_executability 10, data_quality_control 6, reproducibility 6, security 5.

- PASS: Rare-class input fails loudly rather than returning wrong frequencies (ValueError raised (logs/imbalance.log))
- FAIL: The error message identifies the cause (single-class subsample) (message cites multiclass/liblinear, not class absence)
- FAIL: SKILL.md or the script docstring states the both-classes-per-subsample requirement (not stated; subsampling is unstratified (RA-001))

### Input 7 (Scope Boundary): lasso_biomarker.py narrative, R glmnet prose row, constant-column and empty-selection guards

Status COMPLETED. lasso_biomarker.py: noise AUC 1.00 select-before-CV vs 0.56 in-pipeline; stable [g0,g1,g2,g3] under the reworded label "[planted signal: g0..g4; a missing one was not recovered]" (4 of 5, now stated honestly); permuted 0; rescaled 4 (same set True); identical when run from the Skill directory. Constant column handled (frequency 0). glmnet is one troubleshooting row, no R code, nothing claimed executed.

Specialized dimensions: methodological_validity 16, code_executability 14, data_quality_control 8, reproducibility 9, security 5.

- PASS: Script print labels match what runs (BD-005 incl. the lasso reword) (output shows 4 stable and the label says a missing one was not recovered; Boruta script prints 5/5 and 4/5 from computed values)
- PASS: R glmnet is not presented as executed or bundled (single prose row in Common Errors, no code; static-only (no explicit "not executed" marker, noted as a deduction))
- PASS: Degenerate inputs (constant column, q=0) do not crash or silently mislead (frequency 0.0 for the constant feature; q=0 gives a NaN index and the snippet prints "no features selected")

## Finding ledger (fixer order)

| ID | Sev | Fix touches | Summary |
|---|---|---|---|
| RA-001 | P2 | SKILL.md prose (a docstring note would change script bytes) | Rare-class labels raise a misleading ValueError; requirement undocumented. |
| RA-002 | P2 | SKILL.md prose only | roc_auc size swings 53-203 over partitions; accuracy 148-150. |

## Lead verification

- **BD-001 resolved.** Determinism: seed 0 twice bit-identical, seed 1 or 7 differs (1,000 and 7,129 probes; own data). Null: 0 stable in 8 own pure-noise draws; 0 stable in 10 of 11 (1,000) and 11 of 11 (7,129) permuted Golub sets. Planted: 0 false stable in 12 self-built draws on real signal; recall 0-4 of 5 (q caps recall, the Skill claims no recall). Units: raw, standardized, rescaled and x1000 give identical frequencies. All stated numbers match: 2/2/2, 5/5/5, one probe at 0.81 (1,000), highest frequency 0.57 (7,129; the staged ten reach 0.52, the snippet permutation 0.57).
- **BD-002 resolved.** 601/203/148, permuted 16/0/0 and AUC 0.991/0.983/0.991 reproduce on the stated partition. Pinning accuracy is defensible for a compact signature: size is stable across partitions (148-150) while roc_auc varies 53-203 and neg_log_loss 436-601; the presentation says one dataset and partition and the 1.11 default change is real (FutureWarning in 1.9.1). neg_log_loss in omics-classifiers is a deliberate difference for calibrated probabilities. See RA-002.
- **BD-003 resolved** (scaler inside the Pipeline, label reads "In-pipeline CV AUC (k fixed)", nested GridSearchCV verified to nest by perturbation). **BD-004 resolved** (seeded, "no features selected" guard). **BD-005 resolved** (lasso label reworded and matches the 4-of-5 output; Boruta script prints computed 5/5 and 4/5). **BD-006 resolved** (MRMRSelect fit inside the fold, cols_ unchanged by held-out perturbation).
- **Description** parses as YAML, is a "Use when" trigger covering selector choice, candidate biomarkers and reproducibility; it separates the Skill from model-validation (performance estimation), prediction-explanation (SHAP), omics-classifiers (build a classifier), survival-analysis and atlas-mapping. No finding.
- **Cost note** matches the tooling logs within load noise: elastic-net 39 s / 278 s here (33 / 250 s in the tooling log) vs "about 34 / 263 s"; stability call 1-3 s and 15-24 s vs 1-6 / 15-24 s.

## Coverage and evidence

Environment: `F:\OpenScience\audit-envs\cheminformatics-hit-triage-analyst` (native Windows venv, sklearn 1.9.1, numpy 2.5.3, Boruta 0.4.3, mrmr-selection 0.2.8), fingerprint sha256 20291632e93a3881e9704027dfe1d61f2f02fb40d64667ea992bb557bbb336a6, unchanged. Input: Golub ALL/AML (72 x 7,129) and the staged 1,000-probe subset from `derived\biomarker-discovery`; synthetic data built by this audit, planted truth labelled. Executed: all six SKILL.md python blocks at 1,000 probes and at 7,129 probes (blocks 0-5), scripts/stability_selection.py via staged drivers at both sizes (every stated number), determinism at both sizes, lasso and Boruta scripts, own null/planted/invariance/imbalance/leakage/scoring-partition tests (scripts/). Static-only: R glmnet (prose row, nothing claimed executed). No blocked surface, no input missing, no tooling-delta needed. Run logs in `logs/`; runs executed concurrently on a shared machine, so times are upper-ish. The first leakage run (logs/leakage_run1_flawed_label_flip_changed_splits.log) was my own test bug (flipping held-out labels changed the stratified splits); it was fixed by passing fixed splits and rerun; only the corrected run is evidence.
