> **Audit record for `bio-machine-learning-biomarker-discovery`**
> - Audited working candidate `e0d8efc0e1b0610d8c273b1e3837670cd94969cdec2b38614f6796efe08fed71`; exact candidate provenance is in [source-identity.json](source-identity.json).
> - Derived from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/machine-learning/biomarker-discovery), authored by [GPTomics](https://github.com/GPTomics) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-10-03 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test inputs and provenance are described in the published scripts/inputs and audit body; raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer: bio-machine-learning-biomarker-discovery

Generated: 2026-10-03  
Phase: bounded diagnostic initial audit (lane 3a)  
Exact candidate: `e0d8efc0e1b0610d8c273b1e3837670cd94969cdec2b38614f6796efe08fed71` (files=5, bytes=29728)

## Outcome

Diagnostic score is **81/100**; the numeric band is Limited Release but the assertion-pass-rate floor (68%) forces a one-tier downgrade to **Beta Only**. Both veto gates pass. The bundled scripts and the leakage-safe pattern are sound and reproduce the Skill's central claim on real Golub data. The open weaknesses are the stability snippet (scale-dependent, not null-calibrated), an unexplained normalizer scoring change that moves signature size three-fold, and small script/snippet inconsistencies. No safety assertion (fabrication, PHI, destructive action) failed. This is an initial diagnostic audit, not certification: route six open findings to `fix-scientific-skill`, then independently re-audit.

## Summary table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---:|---|---:|---:|---:|---:|:---:|
| 1 | Canonical | 34 | 49 | 83 | 4/5 | ✅ |
| 2 | Variant A | 35 | 50 | 85 | 4/4 | ✅ |
| 3 | Variant B | 34 | 49 | 83 | 3/4 | ✅ |
| 4 | Edge | 28 | 34 | 62 | 1/5 | ⚠️ |
| 5 | Stress | 35 | 51 | 86 | 3/4 | ✅ |
| 6 | Scope Boundary | 30 | 43 | 73 | 2/3 | ⚠️ |

**Execution average:** 78.7/100  
**Assertion pass rate:** 17/25 (68.0%)  
**Static score:** 85/100  
**Arithmetic:** 85 x 0.4 = 34.0; 78.7 x 0.6 = 47.2; 34.0 + 47.2 = 81.2 -> **81/100**  
**Grade:** Beta Only (score band Limited Release; one-tier downgrade for missed floors: assertion_rate>=80%(LR)/90%(PR))

## Veto gates

Skill veto: **PASS**. Research veto: **PASS**.

- T1 stability: PASS. Both bundled scripts and every SKILL.md snippet ran to completion on sklearn 1.9.1 / numpy 2.5.3 / Boruta 0.4.3; no crash or dependency conflict.
- T2 contract: PASS. No structured API contract; documented output shapes held (coef_ is (1, p) with use_legacy_attributes=False; support_/support_weak_ masks).
- T3 determinism: PASS. Both scripts are seeded and byte-identical across two runs. Only the SKILL.md stability snippet is unseeded (61 vs 64 stable probes, Nogueira 0.519 vs 0.527): Monte-Carlo noise filed as BD-004, not a veto.
- T4 security: PASS. No code execution of user strings, no network, no credentials, no destructive operations.
- M1 scientific integrity: PASS. Citations spot-checked (Ambroise 2002, Ein-Dor 2005/2006, Venet 2011, Nogueira 2018, Goring 2001, Squair 2021) match their titles and journals; no invented numbers. The Nogueira formula in the snippet matches the published estimator (unbiased variance, ddof=1).
- M2 practice boundaries: PASS. Research-use selection guidance; the Skill routes unbiased performance to model-validation and refuses to read selected genes as the biomarkers. No diagnostic or treatment claims.
- M3 methodological ground: PASS. Core thesis verified on real data: selection-before-CV gives 0.85 mean AUC (min 0.79) on 10 label permutations of Golub versus 0.49 in-pipeline. The stability snippet is a scale/null-calibration weakness (BD-001), not a principled fallacy, because the Skill states stability is reported next to accuracy rather than as proof.
- M4 code usability: PASS. All four snippets and both scripts executed; the one tooling-reported ConvergenceWarning lead did not reproduce on the real-label pipeline (it appears only under permuted labels).

## Inputs

### Input 1 (Canonical): SKILL.md leakage-safe Pipeline on real Golub ALL/AML (72 x 7,129), with permutation nulls

Status COMPLETED. Pipeline AUC 0.920 +/- 0.126 (raw) vs 0.990 +/- 0.030 with a scaler in the pipeline; 10 label permutations: selection-before-CV 0.846 mean (min 0.788), in-pipeline 0.492 (0.417-0.645).

Specialized dimensions: methodological_validity 17, code_executability 12, data_quality_control 7, reproducibility 8, security 5.

- PASS: CV AUC is computed on held-out folds with SelectKBest inside the Pipeline (evidence/c1.json verbatim_raw)
- PASS: In-pipeline AUC under permuted labels is chance (mean 0.492 over 10 permutations)
- PASS: Selection-before-CV reproduces the optimism the Skill warns about (mean 0.846, min 0.788 (tooling single draw: 0.79 vs 0.56))
- PASS: Snippet runs without ConvergenceWarning on real labels (tooling lead) (not reproduced: 0 warnings on real labels, 3 only under permuted labels (evidence/warn_probe.json))
- FAIL: Snippet standardizes, as the Skill says the L1/elastic penalty requires, and labels its estimate accurately (no scaler: AUC 0.92 vs 0.99; print label says "Nested-safe" for a single-level fixed-k CV)

### Input 2 (Variant A): BorutaPy snippet on Golub (top-1,000 variance probes, label-free filter) with null and in-split held-out check

Status COMPLETED. Real labels: 90 confirmed / 20 tentative in 96 s. Permuted labels: 2 confirmed. Boruta fit on a 60% training split only: 61-74 confirmed, held-out AUC 1.0 on three splits.

Specialized dimensions: methodological_validity 17, code_executability 13, data_quality_control 7, reproducibility 8, security 5.

- PASS: Snippet returns confirmed and tentative masks on numpy input (evidence/c2.json real_labels)
- PASS: Permuted labels confirm (almost) nothing (2 of 1,000 probes)
- PASS: Boruta restricted to the training split still yields a held-out-valid signature (held-out AUC 1.0 x3 (Golub is near-separable; not evidence of calibration))
- PASS: Skill keeps performance claims on the Pipeline pattern, not on the discovery fit (explicit sentence after the leakage-safe block)

### Input 3 (Variant B): Elastic-net LogisticRegressionCV snippet (scoring=neg_log_loss, use_legacy_attributes=False) on Golub, scoring comparison

Status COMPLETED. Runs with FutureWarning escalated: no warnings, coef_ shape (1, 1000), scalar l1_ratio_/C_. Signature size by scoring on 1,000 probes: neg_log_loss 329, accuracy (origin default) 152, roc_auc 96. Held-out pipeline AUC 1.0; permuted-label AUC 0.44.

Specialized dimensions: methodological_validity 16, code_executability 13, data_quality_control 7, reproducibility 8, security 5.

- PASS: Snippet runs on sklearn 1.9.1 with no FutureWarning/DeprecationWarning (evidence/c3.json scoring_variants)
- PASS: Scaler and C/l1_ratio tuning inside the pipeline give a held-out AUC with a chance-level null (AUC 1.0 real, 0.44 permuted)
- PASS: Repeated identical fits select the same set (328 = 328, identical (saga, no random_state))
- FAIL: The Skill states why neg_log_loss was chosen and what it does to signature size (sibling Skill explains the sklearn warning; this one is silent while size moves 96 -> 329)

### Input 4 (Edge): Subsampling stability snippet with Nogueira index: determinism, scale, permuted-label null, empty selection

Status COMPLETED. Raw Golub probes, C=0.1: 61 then 64 stable (Nogueira 0.519, 0.527). Same C on standardized probes: 0 stable, Nogueira 0.18. Permuted labels on raw probes: 35 stable, Nogueira 0.38. C=1e-7: NaN index.

Specialized dimensions: methodological_validity 11, code_executability 9, data_quality_control 5, reproducibility 4, security 5.

- PASS: Snippet runs and returns a stable set and a Nogueira index (evidence/c4.json verbatim_raw_run1)
- FAIL: Identical re-run reproduces the result (seed management) (np.random.choice is unseeded: 61 vs 64 stable features)
- FAIL: Permuted labels produce no stable features (35 stable probes (pi>0.6) from noise labels on raw intensities)
- FAIL: Result is invariant to the units of the input, consistent with the Skill standardize-first rule (raw: 61 stable; standardized same C: 0 stable)
- FAIL: Empty selection is reported, not silent NaN (prints "Nogueira stability = nan")

### Input 5 (Stress): Both bundled scripts twice under -W default; correctness of their printed narrative

Status COMPLETED. lasso_biomarker.py: noise AUC 1.00 selection-before-CV vs 0.57 in-pipeline, stable set g0-g4, Nogueira 0.22. boruta_feature_selection.py: 5/5 module members. Byte-identical across two runs, no warnings. Claim "a minimal-optimal selector would keep ~1" not reproduced: CV-chosen L1 logistic keeps 5/5 (4/5 at C=0.05).

Specialized dimensions: methodological_validity 15, code_executability 14, data_quality_control 8, reproducibility 9, security 5.

- PASS: Both scripts exit 0 with no warnings under -W default (evidence/*.run1.err empty)
- PASS: Outputs are byte-identical across two runs (cmp identical for both)
- PASS: Selection and scaling stay inside the fold; performance numbers come from held-out folds (honest estimate is a Pipeline in cross_val_score)
- FAIL: Printed narrative matches measured behaviour (module claim "~1" not reproduced (evidence/c6.json); comment "~0.7+" vs observed 1.00)

### Input 6 (Scope Boundary): mRMR (advertised, table-only) and R glmnet (prose-only) surfaces

Status COMPLETED. mrmr_classif(DataFrame, Series, K=5) returns 5 probes; numpy input raises AttributeError exactly as the Common Errors row says. mRMR top-20 chosen on permuted labels over the full matrix then CV: AUC 0.94 (the leakage the Skill describes), but the Skill gives no in-fold mRMR pattern.

Specialized dimensions: methodological_validity 14, code_executability 10, data_quality_control 7, reproducibility 7, security 5.

- PASS: mRMR Common Errors row (pandas backend) is accurate (numpy input -> AttributeError)
- FAIL: Skill gives a runnable in-fold mRMR pattern for an advertised method (no mRMR snippet; description and usage-guide advertise it)
- PASS: R glmnet is not presented as executed or bundled (one prose row; no R code claimed (static-only))

## Finding ledger (fixer order)

| ID | Sev | Fix touches | Summary |
|---|---|---|---|
| BD-001 | P1 | SKILL.md snippet + prose; scripts/ unchanged (lasso_biomarker.py uses N(0,1) data, C=1) | Stable set and index depend on feature units; 35 "stable" probes from permuted labels. |
| BD-002 | P2 | SKILL.md prose only | Scoring change correct per sklearn but unstated; signature size varies 3x with it. |
| BD-003 | P2 | SKILL.md snippet (+ one line of prose); scripts/ unchanged | Missing scaler costs 0.07 AUC; "Nested-safe" label overstates a non-nested estimate. |
| BD-004 | P2 | SKILL.md snippet only | Run-to-run variation and silent NaN. |
| BD-005 | P2 | scripts/boruta_feature_selection.py and scripts/lasso_biomarker.py (print strings/comments; runnable bytes change) | Unsupported "~1" and stale "~0.7+" narrative in the two scripts. |
| BD-006 | P2 | SKILL.md snippet or sentence; scripts/ unchanged | No runnable in-fold mRMR despite advertising it. |

## Lead verification

- **neg_log_loss / use_legacy_attributes=False**: correct and consistent (SKILL.md is the only call site; the scripts do not use LogisticRegressionCV). sklearn 1.9.1 emits the FutureWarning for the old defaults and names neg_log_loss as the 1.11 default. Not stated in this Skill and it moves signature size (BD-002).
- **No scaler in SelectKBest+LR**: confirmed as an omission (BD-003). The lbfgs ConvergenceWarning did **not** reproduce on real labels (7,129 and 3,564 probes, 0 warnings); it occurs only under permuted labels.
- **Leakage inside vs outside the fold**: reproduced on 10 permutations (0.846 vs 0.492). Both bundled scripts and every snippet keep selection and scaling in a Pipeline or declare themselves discovery-only; no performance number comes from selection data.
- **Tooling Golub AUC 1.000**: not used as evidence; all Golub numbers here come from this run with no supervised step before the split.
- **mrmr-selection**: installed and working (evidence/c5.json).

## Coverage and evidence

Environment: `F:\OpenScience\audit-envs\cheminformatics-hit-triage-analyst` (native Windows venv, sklearn 1.9.1, numpy 2.5.3, Boruta 0.4.3, mrmr-selection 0.2.8), fingerprint sha256 20291632e93a3881e9704027dfe1d61f2f02fb40d64667ea992bb557bbb336a6. Input: Golub 1999 ALL/AML (OpenML 1104) from staging `public-data`; label-free variance filter only. Executed: SelectKBest pipeline, BorutaPy, elastic-net LogisticRegressionCV, stability/Nogueira, mrmr_classif, both bundled scripts. Static-only: R glmnet (prose, no code; light-optional). No blocked surface; no input missing. Scripts: `scripts/run_cases.py` (cases c1-c7), `scripts/warn_probe.py`, builders. No audit-local repair was made; the candidate bytes were not modified (identity re-verified after execution).
