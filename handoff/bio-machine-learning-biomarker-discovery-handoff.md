# Handoff: bio-machine-learning-biomarker-discovery / prepare-scientific-skill-tooling

- Updated: 2026-10-03
- Lane: 3
- Status: ready-for-phase
- Owner leaving: normalize worker (lane 3, machine-learning batch)
- Next role: prepare-scientific-skill-tooling

## Source identity

- Origin: GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:machine-learning/biomarker-discovery
- Source identity (skill_preflight, measured on F:\OpenScience\bioSkills-Improved): eb2f24ca5af9bb405c7fb7849ab2ba5eb6c25863cca88ec360482b6d5f9e79ad (files=4, bytes=28762)
- Working tree: F:\OpenScience\wt\ml-lane3-normalize\skills\bio-machine-learning-biomarker-discovery
- Branch/worktree: normalize/ml-lane3 from 29f5446 (sparse cone: the four machine-learning Skills of this batch; shared with the three sibling Skills)
- Candidate tree hash: e0d8efc0e1b0610d8c273b1e3837670cd94969cdec2b38614f6796efe08fed71 (files=5, bytes=29728), taken from `python tools/skill_preflight.py`
- Preflight: PASS; warn: no Skill-root LICENSE (manifest must cite repository license evidence; frontmatter `license: MIT` is present, shelf root LICENSE is MIT, GPTomics)
- Applicable audit: none

## Completed this phase

- Directory named to the Skill ID; frontmatter gains `category: Data Analysis` (name, license, author unchanged).
- `examples/*.py` moved to `scripts/` with only version headers and deprecated-API fixes changed; SKILL.md routes to each with a run line.
- "Per-Method Failure Modes" (and reconciliation table where present) moved to `references/failure-modes.md`, routed from SKILL.md with a read-when line.
- Version drift resolved: compat line (numpy 2.5, pandas 3.0, sklearn 1.9, boruta 0.4.3, mrmr-selection 0.2.8); deprecated `penalty=` (sklearn 1.8, removal 1.10) replaced by `l1_ratio` in snippets/scripts; `LogisticRegressionCV` given explicit `scoring='neg_log_loss'` and `use_legacy_attributes=False`; BorutaPy numpy note narrowed to 0.3.x.
- Scripts re-run against the current environments (see Environment); LF, UTF-8 no BOM, no pycache.

## Structural summary

- `SKILL.md` (core workflow, taxonomy, decision tree, thresholds, common errors, citations), `usage-guide.md` (unchanged), `references/failure-modes.md`, `scripts/` (2 files).
- Scientific content, defaults, thresholds, and citations unchanged.

## Runnable-surface inventory

- `scripts/boruta_feature_selection.py` - synthetic, CPU, seconds; ran OK (5/5 module genes confirmed).
- `scripts/lasso_biomarker.py` - synthetic leakage + stability demo, CPU, seconds; ran OK, no sklearn warnings.
- SKILL.md inline snippets: Pipeline/SelectKBest, BorutaPy, LogisticRegressionCV elastic net, subsample stability + Nogueira index. mRMR and R glmnet appear only in prose/tables (no code).

Dependency clues: numpy, pandas, scikit-learn, Boruta, mrmr-selection (usage-guide `pip install` line).

## Required next actions

1. Tooling worker: map the surfaces above to the staged environment and record coverage; flag any surface needing public inputs.
2. Do not edit Skill bytes without re-running preflight and updating the identity above.

## Open findings and blockers

| ID | Severity | State | Evidence | Required disposition |
|---|---|---|---|---|
| none | - | - | - | No blocker. Notes for audit: `scoring='neg_log_loss'` is sklearn's announced 1.11 default (old default was accuracy); chosen to avoid the FutureWarning, flag if audit prefers accuracy/AUC. mrmr-selection API not exercised. |

## Environment and evidence

- Tool inventory: F:\OpenScience\audit-envs\cheminformatics-hit-triage-analyst\ shared venv (scikit-learn 1.9.1, numpy 2.5.3, pandas 3.0.5, Boruta 0.4.3); TOOLS.md there. mrmr-selection not installed there.
- Run evidence: scripts executed in place from the worktree with `PYTHONDONTWRITEBYTECODE=1`; no transcripts saved.
- Restricted-access items: none
- Tooling impact: changed (scripts moved from `examples/` to `scripts/`; deprecated sklearn API replaced)

## Worktree safety

- Run-owned changes: F:\OpenScience\wt\ml-lane3-normalize\skills\bio-machine-learning-biomarker-discovery\ (untracked, new to the shelf); this handoff
- Pre-existing/user-owned changes: records repo untracked `test/validate.bats` and a modified `handoff/bio-splicing-quantification-handoff.md` (another worker); shelf untracked `.vscode/`; none touched
- Records state: uncommitted handoff file
- Product commits/pushes: none

## Transition assertion

- Next-phase prerequisites met: yes
