# bio-machine-learning-model-validation — fix pass

- Source commit: `d86eb5194220abbd15e2f8f110390da88a31e5aa` (`Clarify model-validation effect sizes and reporting`)
- Worktree: `F:\OpenScience\worktrees\bio-machine-learning-model-validation-fixpass`
- Exact-commit re-audit: **96/100, Production Ready, 31/31 assertions, 0 P0 / 0 P1 / 0 P2**

## Fixed

- Made the leakage taxonomy's impact guidance explicitly non-ranked and distinguished low-impact global scaling from potentially high-impact fitted transforms and selection leakage.
- Conditioned nested-versus-flat CV optimism on search, signal, and sample properties, with explicit reporting fields.
- Replaced the unconditional SMOTE/no-AUC-gain claim with severe-imbalance and resampling-ratio context; required original-prevalence assessment/recalibration.
- Added an auditable TRIPOD+AI-oriented validation-report skeleton and exposed it in the usage guide.

## Validation evidence

- `F:\OpenScience\audits\bio-machine-learning-model-validation\run\fix_pass_validation.py`
- `F:\OpenScience\audits\bio-machine-learning-model-validation\run\fix_pass_validation_d86eb51.out` — 21/21 checks, bundled example byte-compiled and executed.
- `F:\OpenScience\audits\bio-machine-learning-model-validation\run\inputs_all_d86eb51_serial.out` — all seven original audit inputs rerun in scikit-learn 1.9.1.
- `F:\OpenScience\audits\bio-machine-learning-model-validation\eval_report_bio-machine-learning-model-validation_result.json`
- `F:\OpenScience\audits\bio-machine-learning-model-validation\eval_viewer_bio-machine-learning-model-validation.md`

## Non-blocking follow-up

- Add X/y/groups preflight validation only if the guidance evolves into an executable validator.
- Split report details into a reference only if the current inline report skeleton proves too large.
