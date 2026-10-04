# Handoff: bio-machine-learning-atlas-mapping / orchestrator (commit, intake)

- Updated: 2026-10-03
- Lane: 3 (delta re-audit lane E2, description trim)
- Status: candidate-ready
- Owner leaving: delta re-audit worker E2 (fresh auditor)
- Next role: orchestrator (commit exact bytes to make them ready); optional AM-009 text fix then delta re-audit

## Source identity

- Origin: GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:machine-learning/atlas-mapping
- Working tree: F:\OpenScience\wt\ml-lane3-normalize\skills\bio-machine-learning-atlas-mapping (untracked by design)
- Candidate tree hash: becbe61423e78eaae064b907ae4dc929d87852078244bf2586f218ca69b7eab3, files=7, bytes=39428 (skill_preflight --offline PASS before and after)
- Applicable audit: F:\optimizing-agent-science-skills\audits\skills\bio-machine-learning-atlas-mapping\candidate@becbe61423e7-reaudit-delta2-20261003 (supersedes candidate@8b4d96ad2465-final-reaudit-lane3b-20261003, certified identity 8b4d96ad2465)

## Completed this phase

- Delta qualified: only SKILL.md differs, by the `description:` line; reverting edits.json reproduces 8b4d96ad2465 exactly. Frontmatter parses as one string.
- New P2 AM-009: the trimmed trigger reads like shelf sibling bio-single-cell-cell-annotation and the body has no hand-off to it. agent_specific 17 to 16; static 88 to 87.
- Score 86 (was 87): static 87 = 34.8, execution 85.7 = 51.4; still Production Ready, candidate-ready.
- AM-008 unchanged.

## Required next actions

1. Orchestrator: commit the exact bytes above and proceed to intake. Do not edit Skill bytes without a new audit.
2. Open findings below are unchanged except where marked new.

## Open findings and blockers

| ID | Severity | State | Evidence | Required disposition |
|---|---|---|---|---|
| AM-008 | P2 | open, unchanged | certified record (driven_marker_runs.log) | script guard plus n_listed column |
| AM-009 | P2 | open, new | published viewer.md and report.json | add a mechanism clause to the description (fixed-reference projection with OOD gating) and a Related Skills hand-off to bio-single-cell-cell-annotation; text only |

## Environment and evidence

- TOOLS.md: F:\OpenScience\audits\bio-machine-learning-atlas-mapping\TOOLS.md (unchanged)
- Run evidence: F:\OpenScience\audits\bio-machine-learning-atlas-mapping\reaudit-delta2-20261003\ (scripts/qualify_delta2.py, logs/qualify.json); certified execution evidence reused, nothing rerun
- Not executed: as certified; tools\smoke_irfinder.sh not run
- Tooling impact: none (frontmatter text only)

## Worktree safety

- Run-owned changes: the run dir, the published record, this handoff, regenerated audit views
- Pre-existing/user-owned: records test/validate.bats, shelf .vscode/; sibling Skill dirs untouched
- Records state: uncommitted (orchestrator commits)
- Product commits/pushes: none

## Transition assertion

- Next-phase prerequisites met: yes
