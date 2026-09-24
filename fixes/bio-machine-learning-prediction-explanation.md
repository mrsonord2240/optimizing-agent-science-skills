# bio-machine-learning-prediction-explanation — fix log (2026-09-24)

Skill: `machine-learning/prediction-explanation`
Branch/worktree: `fix/bio-machine-learning-prediction-explanation` / `F:\OpenScience\wt\bio-machine-learning-prediction-explanation`
Base: staging `main` at `d4f4651`
Fix commit: `0b6111d93747a933ebcd75d67aad6cb575b5c1fb` — `fix: correct correlated TreeSHAP guidance`

## Resolved audit findings

| Priority | Finding | Fix | Exact-commit evidence |
|---|---|---|---|
| P1 | The text claimed `tree_path_dependent` TreeSHAP could credit a feature absent from every fitted-tree split. | Replaced it with the supported claim: modes can split credit differently among correlated features used by the trees; an all-tree-unused feature receives zero under both modes. | Depth-1 A-only tree: B/C exactly zero in both modes. Depth-2 A/B tree: B path-dependent 0.3925 vs interventional 0.3511. |
| P2 | Module aggregation required an unspecified `clusters` map. | Added an executable Spearman absolute-correlation, average-linkage, declared-cut `fcluster` recipe and required reporting/sensitivity analysis. | The exact snippet was executed with pandas 3.0.5 (including its writable-array compatibility detail); all columns mapped once and correlated A/B shared a module. |
| P2 | Background and LIME text overstated ranking instability. | Replaced absolutes with a rank-overlap measurement requirement. Updated the LIME example to emit mean pairwise top-5 overlap. | The background probe measured a valid 3/3 top-3 overlap (stable here); the bundled LIME example ran and printed the requested overlap metric. |

The held-out permutation regression also remains valid: A importance was 0.2227 with its correlated copy B available and 0.4888 after B was removed.

## Re-audit

Exact-commit result: **96/100 — ⭐ Production Ready**, deployable; static 97/100, dynamic 95.4/100, assertions **16/16**. Structural and research vetoes pass. No P0/P1/P2 recommendations remain.

Environment: `F:\OpenScience\audit-envs\cheminformatics-hit-triage-analyst\Scripts\python.exe` (Python 3.12.13; shap 0.52.0; lime 0.2.0.1; scikit-learn 1.9.1; pandas 3.0.5; scipy 1.18.1).

Evidence and refreshed report:

- `F:\OpenScience\audits\bio-machine-learning-prediction-explanation\run\reaudit-20260924\reaudit_prediction_explanation.py`
- `F:\OpenScience\audits\bio-machine-learning-prediction-explanation\run\reaudit-20260924\exact-0b6111d.stdout.txt`
- `F:\OpenScience\audits\bio-machine-learning-prediction-explanation\eval_report_bio-machine-learning-prediction-explanation_result.json`
- `F:\OpenScience\audits\bio-machine-learning-prediction-explanation\eval_viewer_bio-machine-learning-prediction-explanation.md`

Standing use limits are intentional, not open defects: SHAP/LIME explain the fitted model, not biology, causation, or a validated biomarker panel; real analyses must report baseline, module, and LIME sensitivity.
