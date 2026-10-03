> **Audit record for `bio-machine-learning-survival-analysis`**
> - Audited working candidate `eac9a589b7bdc8b56d0f832c060d837a502e4e4c3fd355310ed00582195d71fb`; exact candidate provenance is in [source-identity.json](source-identity.json).
> - Derived from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/machine-learning/survival-analysis), authored by [GPTomics](https://github.com/GPTomics) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-10-03 by Claude (Anthropic) delta re-audit worker D2, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test inputs and provenance are described in the published scripts/inputs and audit body; raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer - bio-machine-learning-survival-analysis

Generated: 2026-10-03
Audit type: independent delta re-audit (text-only change to certified bytes), lane D2
Exact candidate content SHA-256: `eac9a589b7bdc8b56d0f832c060d837a502e4e4c3fd355310ed00582195d71fb` (5 files, 34007 bytes; `skill_preflight --offline` PASS before and after, candidate bytes untouched)
Certified baseline: `c60f873f52f6` (86, Production Ready), record `candidate@c60f873f52f6-reaudit-lane3b-20261003`
Scores carry forward from the certified report; only the reliability category and the one assertion touched by the change were re-scored.

## Result

**Static 88/100; Execution average 85.6/100; Final 86.6 (87); assertion pass rate 24/24; Layer 1 34.6/40; Layer 2 51.0/60.**
Grade: Production Ready. Skill veto PASS; Research veto PASS. Decision: candidate-ready for exact identity `eac9a589b7bd`. No open finding remains from the certified record.

## Delta qualification

- Four files (references/failure-modes.md, scripts/competing_risks_cif.py, scripts/cox_regression.py, usage-guide.md) are byte-identical to the certified per-file sha256 values. Only SKILL.md differs (20410 to 20526 bytes); no script or executable statement changed.
- Limitation: the pre-fix SKILL.md bytes were not retained anywhere (no copy of sha256 81ae775e... found under the OpenScience or records trees), so the scratch-copy revert to the certified identity could not be reproduced. The fix log's single-row claim is therefore corroborated by the size delta (+116 bytes, one table row) and by the verbatim run of both SKILL.md python blocks, which reproduce the certified output exactly (alpha 0.3968, 3 of 9 nonzero; Uno C 0.669, mean AUC 0.728, IBS 0.161 vs KM 0.178; scripts/rd_run_skill_snippets.py).

## Changed claim versus measured values

Row: "`times` for AUC/IBS out of range - a time at or above the largest test time of any status (censored or not); times below it are accepted, even past the largest uncensored time - Keep `times` strictly below the largest test time".

GBSG2, stratified 70/30 split, seed 0: largest test time 2556 (censored), largest uncensored 2093.

| Grid end t | cumulative_dynamic_auc | integrated_brier_score |
|---|---|---|
| 2092 (below largest uncensored) | 0.738 | 0.207 |
| 2324 (past largest uncensored) | 0.742 | 0.211 |
| 2555 (one below max) | 0.749 | 0.209 |
| 2556 (max, censored) | ValueError [8; 2556[ | ValueError [8; 2556[ |
| 2566 | ValueError | ValueError |

Verdict: the row is correct for both metrics. Untested corner: a largest test time that is an event (the error message and bound are generic for test follow-up).

## Finding dispositions

| ID | Verdict |
|---|---|
| SA-006 | resolved |
| SA-001 to SA-005 | unchanged, resolved in the certified record |

No open finding remains.

## Not executed

Unchanged from the certified record: Fine-Gray, CIF Brier, randomForestSRC, landmarking, calibration curves, nested CV, boosting, survival SVM, Cox-Time (the Skill labels them not bundled or not executed). pycox and the scripts were not re-run (bytes unchanged).

## Evidence

Run root `F:\OpenScience\audits\bio-machine-learning-survival-analysis\reaudit-delta-20261003\` (scripts/rd_times_range.py, rd_run_skill_snippets.py; logs/). Environment: survival-venv, scikit-survival 0.28.0, unchanged per TOOLS.md.
