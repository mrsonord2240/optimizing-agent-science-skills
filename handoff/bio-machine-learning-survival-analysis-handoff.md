# Handoff: bio-machine-learning-survival-analysis / prepare-scientific-skill-tooling

- Updated: 2026-10-03
- Lane: 3
- Status: ready-for-phase
- Owner leaving: normalize worker (lane 3, machine-learning batch)
- Next role: prepare-scientific-skill-tooling

## Source identity

- Origin: GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:machine-learning/survival-analysis
- Source identity (skill_preflight, measured on F:\OpenScience\bioSkills-Improved): 0bb20cee2b407e12bb5750d39c28288692e98753e5a2653f659303b3775537a0 (files=4, bytes=27071)
- Working tree: F:\OpenScience\wt\ml-lane3-normalize\skills\bio-machine-learning-survival-analysis
- Branch/worktree: normalize/ml-lane3 from 29f5446 (sparse cone: the four machine-learning Skills of this batch; shared with the three sibling Skills)
- Candidate tree hash: 2dc45fa24b1316256e951edee5cb62a428151ed508104a0dc2aa75033405182b (files=5, bytes=27923), taken from `python tools/skill_preflight.py`
- Preflight: PASS; warn: no Skill-root LICENSE (manifest must cite repository license evidence; frontmatter `license: MIT` is present, shelf root LICENSE is MIT, GPTomics)
- Applicable audit: none

## Completed this phase

- Directory named to the Skill ID; frontmatter gains `category: Data Analysis` (name, license, author unchanged).
- `examples/*.py` moved to `scripts/` with only version headers and deprecated-API fixes changed; SKILL.md routes to each with a run line.
- "Per-Method Failure Modes" (and reconciliation table where present) moved to `references/failure-modes.md`, routed from SKILL.md with a read-when line.
- Version drift resolved: compat line (sksurv 0.28, lifelines 0.30, sklearn 1.9, numpy 2.5, pandas 2.3); added note that sksurv 0.28 pins sklearn 1.9.x and lifelines needs pandas <3 (isolated env required).
- Scripts re-run against the current environments (see Environment); LF, UTF-8 no BOM, no pycache.

## Structural summary

- `SKILL.md` (core workflow, taxonomy, decision tree, thresholds, common errors, citations), `usage-guide.md` (unchanged), `references/failure-modes.md`, `scripts/` (2 files).
- Scientific content, defaults, thresholds, and citations unchanged.

## Runnable-surface inventory

- `scripts/cox_regression.py` - synthetic Coxnet + RSF, Uno C / AUC(t) / IBS vs KM baseline, CPU, seconds; ran OK.
- `scripts/competing_risks_cif.py` - synthetic 1-KM vs Aalen-Johansen CIF, CPU, seconds; ran OK.
- pycox DeepSurv/DeepHit, Fine-Gray, landmarking, lifelines C-index appear as prose or one-line fixes only (no code; pycox untested).

Dependency clues: scikit-survival (pins scikit-learn 1.9.x), lifelines (pandas <3), pandas; optional pycox + torch.

## Required next actions

1. Tooling worker: map the surfaces above to the staged environment and record coverage; flag any surface needing public inputs.
2. Do not edit Skill bytes without re-running preflight and updating the identity above.

## Open findings and blockers

| ID | Severity | State | Evidence | Required disposition |
|---|---|---|---|---|
| none | - | - | - | No blocker. Notes for audit: The pandas <3 constraint comes from lifelines pins per the staging TOOLS.md, not re-verified here. pycox 0.3 unchecked against current torch. |

## Environment and evidence

- Tool inventory: F:\OpenScience\audit-envs\cheminformatics-hit-triage-analyst\tools\survival-venv\ (scikit-survival 0.28.0, lifelines 0.30.3, scikit-learn 1.9.1, numpy 2.5.3, pandas 2.3.3); pycox not installed (torch-pinned, optional)
- Run evidence: scripts executed in place from the worktree with `PYTHONDONTWRITEBYTECODE=1`; no transcripts saved.
- Restricted-access items: none
- Tooling impact: changed (scripts moved from `examples/` to `scripts/`; deprecated sklearn API replaced)

## Worktree safety

- Run-owned changes: F:\OpenScience\wt\ml-lane3-normalize\skills\bio-machine-learning-survival-analysis\ (untracked, new to the shelf); this handoff
- Pre-existing/user-owned changes: records repo untracked `test/validate.bats` and a modified `handoff/bio-splicing-quantification-handoff.md` (another worker); shelf untracked `.vscode/`; none touched
- Records state: uncommitted handoff file
- Product commits/pushes: none

## Transition assertion

- Next-phase prerequisites met: yes
