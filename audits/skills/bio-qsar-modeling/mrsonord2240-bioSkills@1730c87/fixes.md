# bio-qsar-modeling — audit fix pass (2026-09-24)

Source: `chemoinformatics/qsar-modeling` in `mrsonord2240/bioSkills`, branch
`fix/bio-qsar-modeling-audit-20260924`, exact commit
`1730c878987bce00f2a0c88b9f02534e22a560da`.

The 2026-09-16 audit had three P1 and four P2 findings. All seven are fixed and
were re-audited at the exact commit. The pre-fix report and run are retained at
`F:\OpenScience\audits\_pre-fix-20260924\bio-qsar-modeling\`.

| finding | priority | change | verified (ran / help / docs) | notes |
|---|---|---|---|---|
| Prediction omitted the training featurizer and failed at 517 vs 300 inputs | P1 | Added `--molecule-featurizers rdkit_2d` to the prediction command and named the mismatch/recovery rule. | ran | Chemprop 2.3.1 prediction against the four audited checkpoints wrote 200 rows and `pred_0_unc`; no tensor-shape failure. |
| Leverage and Mahalanobis were presented as raw-fingerprint AD methods | P1 | AD table now limits leverage/Mahalanobis to low-dimensional, conditioned descriptor or PCA space; raw sparse ECFP leverage is prohibited and has a documented `0 <= h <= 1` sanity bound. | ran | The real ECFP regression reproduced 319/323 invalid raw leverage values and a 1.14e8 condition number; PCA Mahalanobis completed. |
| Scaffold/time split caveat was disconnected from conformal exchangeability | P1 | Connected split choice to exchangeability, required held-out empirical coverage, and named Mondrian/group-conditional variants. | ran | MAPIE 0.8.6 full hERG run completed with `n_jobs=-1`; recorded coverage was 0.861 at nominal 0.90, 0.926 at 0.95, and 0.715 at 0.80. |
| Common Errors prescribed nonexistent `--seed` | P2 | Replaced it with `--data-seed 42 --pytorch-seed 42`, explained distinct randomness sources, and added both to the training example. | help / ran | Chemprop 2.3.1 `train --help` accepts both flags; the exact prediction run used the compatible model path. |
| Conformal example hid its compute cost | P2 | Added `n_jobs=-1`, documented that `cv=5` fits six base estimators, and pointed to split conformal when repeated fitting is too costly. | ran | Full 2,579 x 2,048 MAPIE re-run completed from the exact-commit snippet. |
| Missing-AD symptom incorrectly required an MAE degradation | P2 | Rephrased the symptom around explained variance/rank ordering and directs stratified R2 or Spearman, not MAE alone. | ran | On the real novel series, MAE was 1.01x familiar compounds while R2 was 0.015 versus 0.621; the corrected wording matches the observed signal. |
| `pred_*_unc` was called standard deviation although Chemprop emits variance | P2 | Corrected the AD row and prediction guidance; documents squared units and explicit square-root conversion when standard deviation is wanted. | ran | Exact Chemprop output has non-negative, non-constant `pred_0_unc` values (0.00000400 to 0.02355900). |

Deleted from `usage-guide.md`:

- The prerequisites/version block; its version constraints are in `SKILL.md` →
  **Version Compatibility**.
- The duplicated Tips block; its split, calibration, conformal, uncertainty, and
  baseline rules remain in the corresponding `SKILL.md` sections.

## Exact-commit re-audit

- Report: `F:\OpenScience\audits\bio-qsar-modeling\eval_report_bio-qsar-modeling_result.json`
- Viewer: `F:\OpenScience\audits\bio-qsar-modeling\eval_viewer_bio-qsar-modeling.md`
- Execution: `F:\OpenScience\audits\bio-qsar-modeling\run\exact-commit-1730c87\`

Result: **96/100, Production Ready, deployable; 7/7 inputs executed; 31/31
assertions passed; no veto; no open P0/P1/P2 findings.**
