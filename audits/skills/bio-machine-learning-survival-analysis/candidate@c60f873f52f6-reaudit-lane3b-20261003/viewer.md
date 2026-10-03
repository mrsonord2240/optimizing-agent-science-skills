> **Audit record for `bio-machine-learning-survival-analysis`**
> - Audited working candidate `c60f873f52f63ad78a5009b351f8451510f86bbae3f7d46886c03e3bcf9eaf39`; exact candidate provenance is in [source-identity.json](source-identity.json).
> - Derived from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/machine-learning/survival-analysis), authored by [GPTomics](https://github.com/GPTomics) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-10-03 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test inputs and provenance are described in the published scripts/inputs and audit body; raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-machine-learning-survival-analysis

Generated: 2026-10-03  
Audit type: independent final re-audit (full mode), lane 3b-2  
Exact candidate content SHA-256: `c60f873f52f63ad78a5009b351f8451510f86bbae3f7d46886c03e3bcf9eaf39` (5 files, 33891 bytes); provenance in [source-identity.json](source-identity.json).  
Prior audit: `2dc45fa24b13` (77, Limited Release; SA-001, SA-002 P1; SA-003 to SA-005 P2).

## Summary

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---:|---:|---:|---:|---|
| 1 | Canonical | 34 | 50 | 84 | 5/5 | ✅ COMPLETED |
| 2 | Variant A | 35 | 51 | 86 | 5/5 | ✅ COMPLETED |
| 3 | Edge | 35 | 52 | 87 | 4/4 | ✅ COMPLETED |
| 4 | Variant B | 34 | 49 | 83 | 4/5 | ✅ COMPLETED |
| 5 | Stress | 35 | 52 | 87 | 5/5 | ✅ COMPLETED |

**Static score:** 87 / 100
**Execution average:** 85.4 / 100 (Layer 1 34.6/40, Layer 2 50.8/60)
**Assertion pass rate:** 23/24
**Final score:** 86 / 100 (34.8 + 51.2) — ⭐ Production Ready
**Research veto:** PASS. **Skill veto:** PASS.
**Readiness: candidate-ready for this exact identity.** All floors met (static >= 80, execution >= 85, Layer 1 >= 32, Layer 2 >= 48, assertions >= 90%); no open P0 or P1.

## Prior findings

| ID | Prior | Verdict | Measured here |
|---|---|---|---|
| SA-001 | P1 | resolved | KM baseline = hand table (1, 0.8, 0.8, 0.5333, 0.5333) = independent numpy KM (0 difference) = lifelines KM (1.6e-15). IBS on GBSG2 0.1775 from the Skill, 0.1775 from an independent numpy Graf IBS, old event-only formula 0.2627. Synthetic 0.2148 vs old 0.2576. Same estimator, grid and split as the models (main() feeds one integrated_brier_score call signature). |
| SA-002 | P1 | resolved | fit_coxnet_cv has no test argument; a spy on Coxnet fit/predict saw 507 calls, all on training rows. Permuting, noising or truncating the test set: alpha 0.396820 (GBSG2) and 0.182652 (p>>n) and all coefficients identical; the SKILL.md fitting block with a corrupted test partition: identical. Positive control moves alpha (0.399, 0.253). p>>n: 161 nonzero / Uno C 0.708 (path-end) -> 6 nonzero / 0.791. |
| SA-003 | P2 | resolved | Both python blocks run unmodified and chained (3.6 s): alpha 0.3968, Uno C 0.669, AUC 0.728, IBS 0.161 vs 0.178. |
| SA-004 | P2 | resolved | sksurv cumulative_incidence_competing_risks == lifelines AJ == hand table; max difference 2.5e-16 on 40 horizons; no Fine-Gray or CIF-Brier module in either package. |
| SA-005 | P2 | resolved | R-only and prose-only methods labelled not executed; pandas<3 attributed to lifelines alone (metadata checked); pycox described as smoke-tested only (0.615 / 0.620 reproduced). |
| SA-006 | P2 | new, open, text only | Common Errors time-grid row states the wrong bound (see Recommendations). |

## Executed versus static-only

| Surface | Classification | Evidence |
|---|---|---|
| scripts/cox_regression.py, --data synthetic and gbsg2 | executed twice each, deterministic | scripts/evidence/ra_cox_*.log |
| fit_coxnet_cv on p>>n and test-set invariance | executed | scripts/ra_sa002_coxnet_leak.py, evidence/ra_sa002.log, ra_pgtn_run.log |
| KM baseline and IBS | executed against hand table and independent implementations | scripts/ra_sa001_km_ibs.py |
| SKILL.md python blocks | executed verbatim | scripts/ra_run_skill_snippets.py |
| scripts/competing_risks_cif.py, AJ vs sksurv vs hand | executed; script bytes identical to the audited identity | scripts/ra_competing_and_sign.py, evidence/ra_competing_script.log |
| lifelines and sksurv concordance direction | executed | scripts/ra_competing_and_sign.py |
| pycox DeepSurv and DeepHit | smoke rerun (30 epochs, CPU); prose only in the Skill | evidence/ra_pycox_smoke.log, ra_pycox_attrs.log |
| Harrell versus Uno under censoring | reused from the initial audit (Skill text unchanged) | initial record scripts/metric_directions.py |
| Fine-Gray (cmprsk), CIF Brier (riskRegression), randomForestSRC, landmarking, calibration curves/ICI, nested CV, boosting, survival SVM, Cox-Time | static-only; the Skill labels them not bundled or not executed | n/a |

## Static categories

- functional_suitability: 11/12 — SA-001 and SA-002 corrected and verified; prediction-versus-inference scope is drawn well; calibration, nested CV and boosting remain prose-only (labelled).

- reliability: 9/12 — Hard failures from sksurv are informative and the Common Errors table covers the main traps; scripts do no explicit input or time-range validation and one table row misstates the range limit (SA-006).

- performance_context: 7/8 — SKILL.md is 212 lines with failure modes in a reference; scripts run in about 4 s.

- agent_usability: 14/16 — Both code blocks now run chained and verbatim; IPCW training-y order, bool event and the sign trap are prevented explicitly.

- human_usability: 7/8 — Description, usage-guide prompts and the boundary to clinical-biostatistics/survival-analysis match how users ask.

- security: 11/12 — No credentials, network or shell execution; synthetic or bundled data only.

- maintainability: 10/12 — Script now exposes fit_coxnet_cv and km_baseline_surv and the SKILL.md blocks mirror it; no automated tests ship.

- agent_specific: 18/20 — Precise description with sibling hand-offs, progressive disclosure, seeded scripts, and prose-only or R-only methods now labelled not executed.

## Detailed outputs

### Input 1 — Canonical: SKILL.md fit and evaluation blocks run verbatim on GBSG2 (686 patients), stratified held-out split

**Status:** COMPLETED — Both python blocks run unmodified in one namespace (3.6 s, rc 0): alpha 0.3968, 3 of 9 nonzero, Uno C 0.669, mean AUC(t) 0.728, IBS 0.161 vs KM-only 0.178.  
**Scores:** Basic 34/40 | Specialized 50/60 | Total 84/100

**Assertions:**

- PASS — Fitting block (Surv.from_arrays, CV-selected Coxnet at one alpha, RSF) runs on real data (Ran on 480 training patients; coxnet.alphas_ has one entry)
- PASS — Evaluation block copy-runs as written after the fitting block (SA-003) (t_horizon, y_train, y_test all defined by the blocks; no NameError)
- PASS — Held-out Uno C is in a plausible range for GBSG2 (0.669 Coxnet; script gives RSF 0.686)
- PASS — Model IBS beats the censoring-aware KM-only IBS on the same grid and split (0.161 vs 0.178; KM equals hand table, an independent numpy KM and lifelines to 1.6e-15)
- PASS — IPCW metrics receive the training y first and score the held-out set (concordance_index_ipcw(y_train, y_test, ...) on the 30% split)

### Input 2 — Variant A: scripts/cox_regression.py on synthetic and GBSG2: Coxnet vs RSF, Uno C, AUC(t), IBS vs KM baseline (SA-001)

**Status:** COMPLETED — Both modes rc 0 in about 4 s with no warnings under -W default and identical output on a second run. KM baseline IBS 0.178 (GBSG2) and 0.215 (synthetic) equal an independent numpy Graf IBS on an independent numpy KM to 4 decimals; the old event-only formula gives 0.263 and 0.258.  
**Scores:** Basic 35/40 | Specialized 51/60 | Total 86/100

**Assertions:**

- PASS — Script runs end to end without warnings and is seeded (-W default, two runs identical for both --data modes)
- PASS — Printed Kaplan-Meier baseline IBS equals the IBS of a true KM curve (GBSG2 0.1775 vs own numpy IBS 0.1775 vs lifelines-KM 0.1775; synthetic 0.2148 all three)
- PASS — KM baseline uses the same estimator, time grid and held-out split as the models (km_baseline_surv(y_train, times, len(y_test)) feeds the same integrated_brier_score(y_train, y_test, ., times) call as the models)
- PASS — A hand-computed KM table matches km_baseline_surv ((1,1)(2,0)(3,1)(4,0)(5,0): 1, 0.8, 0.8, 0.5333, 0.5333; the naive formula gives 0.5, 0, 0)
- PASS — Models recover the planted signal and the direction of risk is correct (Coxnet Uno C 0.803 and RSF 0.784 on 5-of-40 planted features; 6 of 40 coefficients nonzero)

### Input 3 — Edge: Competing risks: scripts/competing_risks_cif.py, hand-computed Aalen-Johansen table, sksurv equivalence

**Status:** COMPLETED — Script and failure-modes.md are byte-identical to the audited identity. Five-subject hand table: CIF1 0.2, 0.2, 0.4, 0.4, 0.4 and 1-KM 0.2, 0.2, 0.4667 equal lifelines AJ and sksurv cumulative_incidence_competing_risks exactly; on the script data the two implementations differ by 2.5e-16 over 40 horizons; 1-KM 0.517 vs CIF 0.250 at t=3.  
**Scores:** Basic 35/40 | Specialized 52/60 | Total 87/100

**Assertions:**

- PASS — Script runs and shows 1-KM above the Aalen-Johansen CIF (0.517 vs 0.250 with 63% competing events; no warnings)
- PASS — lifelines AalenJohansenFitter and sksurv cumulative_incidence_competing_risks equal the hand table (SA-004) (Exact at all 5 times, cause 1 and cause 2; row 0 sums to 1.0 at t=5)
- PASS — 1-KM >= CIF at every time, strictly above after a competing event (0 violations on 40 horizons; hand table 0.4667 vs 0.4)
- PASS — Skill states which competing-risks methods have no Python implementation and labels them not executed (SA-004, SA-005) (No module with fine/gray/subdist in lifelines or sksurv; Fine-Gray, CIF Brier and randomForestSRC named as R and not bundled or executed)

### Input 4 — Variant B: Metric-direction traps, dependency statements and deep-model claims (lifelines 1-C, sksurv, pandas cap, pycox)

**Status:** COMPLETED — lifelines concordance_index with +partial hazard 0.337 vs -partial hazard 0.663 (sum 1.0), sksurv 0.663. Installed metadata: scikit-survival requires pandas>=2.2 (no cap) and scikit-learn <1.10,>=1.9; lifelines requires pandas <3. pycox DeepSurv C-td 0.615 and DeepHit 0.620 reproduced (30 epochs, CPU), DeepHit.predict_cif and compute_baseline_hazards exist. One wording inaccuracy found (SA-006).  
**Scores:** Basic 34/40 | Specialized 49/60 | Total 83/100

**Assertions:**

- PASS — lifelines concordance sign trap reproduces on held-out GBSG2 and the Skill says to negate (0.337 with +ph, 0.663 with -ph; the Skill's Common Errors row prescribes the negation)
- PASS — Skill's pandas and scikit-learn constraint statements match installed package metadata (SA-005) (pandas<3 attributed to lifelines alone; scikit-survival has no pandas cap)
- PASS — Deep-survival claims are labelled as smoke-tested only, with no pycox code bundled (SA-005) (Taxonomy paragraph says smoke-tested, 30 epochs CPU, GBSG2, nothing bundled; rerun matches (0.615 / 0.620))
- FAIL — Common Errors row on time-grid range states the actual sksurv limit (Row says 'beyond largest uncensored test time'; sksurv accepts times up to the largest test time of any status (t=2324 > largest uncensored 2093 ran, AUC 0.742) and errors only at or above 2556)
- PASS — Harrell-versus-Uno censoring claim is stated at a usable strength (Reused unchanged evidence from the initial audit (Harrell 0.734, Uno 0.727, truth 0.723 at 74% censoring); the Skill text for this claim is unchanged)

### Input 5 — Stress: p>>n Coxnet (n=150, p=1000) and test-set invariance of alpha selection (SA-002)

**Status:** COMPLETED — Before/after reproduced: path-end default predict 161 nonzero, Uno C 0.708; fit_coxnet_cv alpha 0.1827, 6 nonzero, Uno C 0.791 (2.2 s). Every X row seen by Coxnet fit/predict inside fit_coxnet_cv (507 calls) is a training row; permuting, replacing with noise or truncating the test set leaves alpha and coefficients identical; shrinking the training set moves them.  
**Scores:** Basic 35/40 | Specialized 52/60 | Total 87/100

**Assertions:**

- PASS — The documented configuration yields a sparse penalized signature in p>>n (6 of 1000 nonzero at the CV alpha vs 161 at the old path-end default)
- PASS — Held-out Uno C at the CV alpha is at or above the old default (0.791 vs 0.708)
- PASS — Alpha selection uses training data only (by construction) (fit_coxnet_cv(X_train, y_train, l1_ratio, n_splits, seed) takes no test argument; data-flow spy found 0 test-only rows)
- PASS — Changing or permuting the TEST set does not change alpha or coefficients; changing TRAIN does (GBSG2 alpha 0.396820 and p>>n 0.182652 identical in all three perturbations and in the SKILL.md fitting block with corrupted test data; positive control moved alpha to 0.399 and 0.253)
- PASS — Evaluation is on held-out data with no selection leakage into the test split (alpha, path and folds derived from training rows only)

## Recommendations

- P2 SA-006 (text only): reword the Common Errors row 'times for AUC/IBS out of range' to 'at or beyond the largest test follow-up time (event or censored)'. Observed: times up to 2324 (past the largest uncensored 2093) ran; 2556 (the maximum, a censored subject) raised ValueError.

## Notes

- No Skill bytes changed; the manifest was verified with tools/skill_preflight.py before and after (PASS; the no-Skill-root-LICENSE warning is expected, the frontmatter says MIT and the repository licence applies).
- Environment fingerprint 20291632e93a3881e9704027dfe1d61f2f02fb40d64667ea992bb557bbb336a6 and both freeze hashes re-hashed identical to TOOLS.md.
- The fixer's recorded taskkill of unidentified python.exe PIDs stands as recorded; this audit killed no process.
- TOOLS.md still cites old survival_real.py lifelines figures (0.308 / 0.692); this run measures 0.337 / 0.663, the same as the initial audit (same trap, different model settings).
