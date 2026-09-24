# bio-admet-prediction fix pass — 2026-09-24

Source worktree: `F:\OpenScience\wt\bio-admet-prediction` on branch
`fix/bio-admet-prediction`, rooted at staging `main` `d4f4651`.

Commit: `5889856f17650bafa9b1169bafb5dedb97db79d6` — `fix: make bio ADMET prediction route executable`

## Resolved findings

| Previous finding | Priority | Resolution | Exact-commit evidence |
|---|---:|---|---|
| No executable ADMET prediction route; ADMETlab was declared primary but shipped no request | P1 | Primary tool is now the bundled offline ADMET-AI 2.x route, with endpoint selection validated against the installed package. ADMETlab is explicitly optional/current-contract hosted integration. | `run/fix_reaudit_5889856.out`: committed source produced hERG, AMES, DILI, BBB and five CYP endpoints for 293 accepted compounds. |
| Runnable OOD mitigation unavailable; offline point predictions included salts/metals without a signal | P1 | Added a visible input/similarity gate: invalid/disconnected, inorganic and metal-containing input rejects; large or low-similarity organic chemistry is retained as `manual_review`. Threshold is derived from a relevant reference set, not hard-coded. | Same output: cisplatin and sodium chloride reject; macrocycle, peptide, PROTAC and paclitaxel route to manual review. |
| Chemprop reproducibility advice used invalid `--seed` | P2 | Replaced it with Chemprop 2.3.1 `--data-seed 42 --pytorch-seed 42`. | `run/chemprop_2_3_1_seed_help_5889856.out`. |
| ADMETlab result loader accepted unrelated CSV and gave no actionable missing-file/column errors | P2 | Loader now requires a structure column, validates optional current task ID and uncertainty-like columns, and emits named errors. | Exact-commit run passes a valid fixture and rejects missing file, absent uncertainty, and wrong contract. |
| ADMET-AI pin admitted the v1/v2 divergence noted by the Skill | P2 | Pin and compatibility text now target `admet-ai>=2,<3`, tested at 2.0.1, and repeats the version-divergence warning. | Exact-commit script prints `admet_ai_version=2.0.1`. |

## Verification and re-audit

Used `F:\OpenScience\audit-envs\cheminformatics-hit-triage-analyst\tools\admet-ai-venv`
(ADMET-AI 2.0.1) plus the Chemprop 2.3.1 sibling. All changed code and all resolved
claims were executed from commit `5889856`; unchanged prior evidence is explicitly retained
only for unchanged sections.

- Exact script: `F:\OpenScience\audits\bio-admet-prediction\run\fix_reaudit.py`
- Exact output: `F:\OpenScience\audits\bio-admet-prediction\run\fix_reaudit_5889856.out`
- Refreshed report/viewer: `F:\OpenScience\audits\bio-admet-prediction\eval_report_bio-admet-prediction_result.json` and `eval_viewer_bio-admet-prediction.md`
- Pre-fix report/viewer retained with `_pre_fix_d91ed3d` names in the same audit directory.

Re-audit result: **95/100, Production Ready, deployable**; **30/30 assertions pass**;
Skill Veto and Research Veto pass; no P0/P1/P2 remains open.
