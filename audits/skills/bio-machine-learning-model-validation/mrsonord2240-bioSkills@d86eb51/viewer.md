> **Audit record for `bio-machine-learning-model-validation`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@d86eb51](https://github.com/mrsonord2240/bioSkills/tree/d86eb5194220abbd15e2f8f110390da88a31e5aa/machine-learning/model-validation) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor.
> - Performed on 2026-09-24 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Exact-Commit Re-Audit — bio-machine-learning-model-validation

Evaluated 2026-09-24 at source commit `d86eb5194220abbd15e2f8f110390da88a31e5aa`.

**Result: 96/100 — ✅ Production Ready.** Static: 96/100. Dynamic: 95.4/100. Assertions: **31/31 passed**. Veto gates: PASS. Open P0/P1/P2: **0/0/0**.

## Evidence

- Environment: `F:\OpenScience\audit-envs\cheminformatics-hit-triage-analyst` with scikit-learn 1.9.1.
- Full seven-input harness: `run/inputs_all.py`, output `run/inputs_all_d86eb51_serial.out`. It re-ran the nested/flat CV, leakage, grouped CV, calibration API, decision curve, SMOTE, and LOO cases. Expected constant-feature and LOO scoring warnings are retained in the log.
- Exact-commit fix pass: `run/fix_pass_validation.py`, output `run/fix_pass_validation_d86eb51.out`. All 21 source/example checks passed; the bundled example byte-compiled and ran end to end.

## Resolved findings

1. The taxonomy now declares its impact column **not a ranking**. It separates often-small global scaling effects from potentially high-impact fitted normalization, correction, PCA, or imputation, and calls out selection's pure-noise failure mode.
2. Nested/flat-CV guidance now explains that optimism varies with candidate count/correlation, signal, and sample size, and specifies the numbers a report should include.
3. SMOTE guidance now names severe imbalance as the strongest-risk regime, no longer promises no AUC gain, and requires evaluation/recalibration at original deployment prevalence.
4. The skill now provides a checkable TRIPOD+AI-oriented validation-report skeleton; the usage guide makes this a concrete agent deliverable.

## Re-run observations

- Nested AUC was 0.753 ± 0.030 versus flat 0.762 (+0.009), now described appropriately as a context-specific magnitude.
- Pure-noise selection leakage was 0.904 AUC outside-fold versus 0.547 inside a pipeline.
- At 24.7% prevalence, SMOTE changed AUC 0.783 to 0.810 and mean predicted risk 0.247 to 0.275. This supports the revised conditional wording and original-prevalence check.
- The bundled severe-imbalance example again showed mean risk 0.24 against prevalence 0.10.

## Remaining non-blocking recommendations

- Add runtime preflight checks for X/y/groups if this becomes an executable validator rather than guidance.
- Split report-specific details into a separate reference only if that reporting workflow grows beyond the inline skeleton.
