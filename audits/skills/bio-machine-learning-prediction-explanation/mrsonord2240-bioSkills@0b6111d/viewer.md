> **Audit record for `bio-machine-learning-prediction-explanation`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@0b6111d](https://github.com/mrsonord2240/bioSkills/tree/0b6111d93747a933ebcd75d67aad6cb575b5c1fb/machine-learning/prediction-explanation) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-24 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-machine-learning-prediction-explanation

Generated: 2026-09-24
Audit type: exact-commit focused re-audit (not independent)
Source: `mrsonord2240/bioSkills@0b6111d93747a933ebcd75d67aad6cb575b5c1fb:machine-learning/prediction-explanation`

## Result

**96/100 — ⭐ Production Ready; deployable.**

Structural veto: PASS. Research veto: PASS. Static: 97/100. Dynamic: 95.4/100. Assertions: **16/16**. All five prior P1/P2 items are resolved; no open P0/P1/P2 recommendations remain.

| Input | Exact-commit check | Score | Assertions | Result |
|---|---|---:|---:|---|
| 1 | Stated Spearman/average-linkage module construction | 96 | 3/3 | ✅ |
| 2 | TreeSHAP unused-feature boundary and used-feature credit split | 96 | 5/5 | ✅ |
| 3 | Held-out permutation dilution with correlated predictors | 93 | 1/1 | ✅ |
| 4 | Background rank-overlap measurement | 96 | 3/3 | ✅ |
| 5 | LIME seed-sensitivity reporting and bundled examples | 96 | 4/4 | ✅ |

## What changed and was proved

- The former P1 statement that path-dependent TreeSHAP gives an entirely unused correlated feature nonzero credit is gone. A depth-1 tree using A alone gave correlated B and irrelevant C exactly zero under both modes. With a depth-2 tree that uses A and B, B's mean absolute attribution differs by estimand: 0.3925 path-dependent versus 0.3511 interventional.
- The former P2 missing module-map construction is now an executable Spearman correlation / average-linkage / `fcluster` recipe. It ran on pandas 3.0.5 after copying the correlation matrix to a writable NumPy array; A and B correctly shared a module.
- The background and LIME P2 wording now instructs measurement rather than promising universal movement. The background probe measured a top-3 overlap of 3/3 in this model, demonstrating why the text no longer overstates instability. The bundled LIME example now prints mean pairwise top-5 overlap.
- Permutation importance still shows the documented correlation dilution: held-out A importance was 0.2227 with correlated B available, then 0.4888 after B was removed.

## Evidence

Environment: `F:\OpenScience\audit-envs\cheminformatics-hit-triage-analyst\Scripts\python.exe` — Python 3.12.13, shap 0.52.0, lime 0.2.0.1, scikit-learn 1.9.1, pandas 3.0.5, scipy 1.18.1.

- `run/reaudit-20260924/reaudit_prediction_explanation.py` — focused five-input exact-commit test driver.
- `run/reaudit-20260924/exact-0b6111d.stdout.txt` — all focused checks and both bundled examples passed.
- `run/reaudit-20260924/exact-0b6111d.stderr.txt` — only SHAP's documented background subsampling notices.
- `run/reaudit-20260924/source_syntax.stdout.txt` — both shipped Python examples compile cleanly without writing source caches.

The score is an exact-commit re-audit rather than an independent blind audit. It deliberately preserves the method's standing limits: explanations are model-internal, not biology/causation/validated biomarker selection; baseline, module, and LIME sensitivity must be reported for a real analysis.
