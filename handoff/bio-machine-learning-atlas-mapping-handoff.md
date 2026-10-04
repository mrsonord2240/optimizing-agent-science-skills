# Handoff: bio-machine-learning-atlas-mapping / orchestrator (commit, intake)

- Updated: 2026-10-03
- Lane: 3 (delta re-audit lane E4, description reword for AM-009)
- Status: done (shelf e58c885, intake accepted at validator a1d820d, exported to bioSkills-Improved fff47bd; worktree removed)
- Owner leaving: delta re-audit worker E4 (fresh auditor)
- Next role: none; open P2s wait for a later refinement run

## Source identity

- Origin: GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:machine-learning/atlas-mapping
- Working tree: F:\OpenScience\wt\ml-lane3-normalize\skills\bio-machine-learning-atlas-mapping (untracked by design)
- Candidate tree hash: a579d86464c9fd84579b6645107d0f6c72b87f091da33839966cc6b08c8a75ef, files=7, bytes=39483 (skill_preflight --offline PASS before and after)
- Applicable audit: F:\optimizing-agent-science-skills\audits\skills\bio-machine-learning-atlas-mapping\candidate@a579d86464c9-reaudit-delta3-20261003 (supersedes candidate@becbe61423e7-reaudit-delta2-20261003)

## Completed this phase

- Delta qualified: only SKILL.md differs, by the `description:` line; reverting edits.json (fix-description2-20261003) reproduces becbe61423e7 exactly. Frontmatter parses as one string; conforms to the `Use when <task>.` rule.
- AM-009 resolved: new trigger ("projecting ... into an existing reference atlas embedding without retraining the reference ...") separates it from bio-single-cell-cell-annotation. agent_specific 16 to 17, rubric 8.1 = 3; static 87 to 88.
- "Without retraining the reference" is accurate for scArches surgery (independent check: reference model and all encoder tensors bit-identical after surgery; only decoder first-layer batch columns and decoder batch-norm affine params change by scvi default). Not true of fine-tuned foundation models or classifiers, which the body labels separately.
- Score 87: static 88 = 35.2, execution 85.7 = 51.4, sum 86.62; Production Ready, candidate-ready.
- AM-008 unchanged.

## Required next actions

1. Orchestrator: commit the exact bytes above and proceed to intake. Do not edit Skill bytes without a new audit.
2. Optional, non-blocking: one Related Skills line in the body pointing classifier-only annotation (CellTypist, SingleR) to bio-single-cell-cell-annotation; needs a delta re-audit.

## Open findings and blockers

| ID | Severity | State | Evidence | Required disposition |
|---|---|---|---|---|
| AM-008 | P2 | open, unchanged | certified record (driven_marker_runs.log) | script guard plus n_listed column |

## Environment and evidence

- TOOLS.md: F:\OpenScience\audits\bio-machine-learning-atlas-mapping\TOOLS.md (unchanged)
- Run evidence: F:\OpenScience\audits\bio-machine-learning-atlas-mapping\reaudit-delta3-20261003\ (scripts/qualify_delta3.py, scripts/frozen_ref_check.py, logs/); certified execution evidence reused
- Not executed: as certified (Symphony, Azimuth, scPoli, popV, treeArches, foundation models are prose-only)
- Tooling impact: none (frontmatter text only)

## Worktree safety

- Run-owned changes: the run dir, the published record, this handoff, regenerated audit views
- Pre-existing/user-owned: records test/validate.bats, shelf .vscode/; sibling Skill dirs untouched
- Records state: uncommitted (orchestrator commits)
- Product commits/pushes: none

## Transition assertion

- Next-phase prerequisites met: yes
