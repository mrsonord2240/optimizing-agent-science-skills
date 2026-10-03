# Handoff: bio-machine-learning-atlas-mapping / prepare-scientific-skill-tooling (delta)

- Updated: 2026-10-03T16:00:00-04:00
- Lane: 3 (batch 3b-1)
- Status: ready-for-phase
- Owner leaving: fix-scientific-skill worker (lane 3b-1)
- Next role: prepare-scientific-skill-tooling (delta mode), then reaudit-scientific-skill

## Source identity

- Origin: GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:machine-learning/atlas-mapping
- Working tree: F:\OpenScience\wt\ml-lane3-normalize\skills\bio-machine-learning-atlas-mapping
- Branch/worktree: normalize/ml-lane3 from 29f5446 (Skill dirs untracked by design)
- Candidate tree hash: ba864911e88a7d48e4576f9f7f4f1668ef0ed85ddd429c151bbb6ebfc39cd094 (files=7, bytes=39154), `skill_preflight.py` PASS, no pycache
- Applicable audit: audits\skills\bio-machine-learning-atlas-mapping\candidate@d4048dcc887b-initial-lane3b-20261003\ (identity d4048dcc887b, 77, Limited Release); now superseded by the bytes above

## Completed this phase

- Changed: SKILL.md, references/failure-modes.md, scripts/scarches_annotation.py (seed, writes query_annotated.h5ad, input contract), scripts/ood_gating_demo.py (relabel, scope); new scripts/label_marker_check.py, references/pbmc-markers.json.
- AM-001 via route 2: no gate defensible on Monocyte hold-out (kNN 1.6% gated, distance 0.0%, DC 95.9%); limitation + measured table + marker-agreement check documented.
- Executed on the staged real pair (4 full runs, 6 marker checks, demo). Fix log: F:\OpenScience\audits\bio-machine-learning-atlas-mapping\fix-lane3b-20261003\fix-log.md

## Required next actions

1. Tooling delta: record new surface `scripts/label_marker_check.py` (+ `references/pbmc-markers.json`), changed scripts; rerun `fix-lane3b-20261003/scripts/run_holdout.py`. No new dependency.
2. Re-audit by a fresh auditor on the new identity; check the marker-check numbers (Monocytes/B-cell hold-outs) and the claim table in SKILL.md.

## Open findings and blockers

| ID | Severity | State | Evidence | Disposition |
|---|---|---|---|---|
| AM-001 | P1 | fixed (limitation documented + marker check) | fix-log.md, holdout_*.json, logs\marker_*.log | gate itself not improved; for re-audit |
| AM-002 | P2 | fixed | SKILL.md | not-executed label added |
| AM-003 | P2 | fixed | SKILL.md | DataFrame documented |
| AM-004 | P2 | fixed | SKILL.md, script docstring | snippet self-contained |
| AM-005 | P2 | fixed | holdout_none1/none2.json | seeded, identical output |

Caveats: marker check is group-level, curated T-cell markers absent from HVG set (NOT CHECKED), 0.6 threshold validated only on one PBMC pair. Blockers: none.

## Environment and evidence

- Tool inventory: F:\OpenScience\audits\bio-machine-learning-atlas-mapping\TOOLS.md (sha256 2004cafd57d3d4dcbc1bf03b9c312ccdb1f61d222ee7b64d94c8442b6e1f8c96)
- Run evidence: F:\OpenScience\audits\bio-machine-learning-atlas-mapping\fix-lane3b-20261003\ (fix-log.md, holdout_*.json, logs\, scripts\, work\)
- Restricted-access items: none
- Tooling impact: changed (scarches_annotation.py and ood_gating_demo.py edited; label_marker_check.py new surface; no new dependency)

## Worktree safety

- Run-owned changes: the Skill dir above; the run dir above; this handoff
- Pre-existing/user-owned changes: records test/validate.bats; shelf .vscode/; sibling workers' Skill dirs; none touched
- Records state: uncommitted
- Product commits/pushes: none

## Transition assertion

- Next-phase prerequisites met: yes
