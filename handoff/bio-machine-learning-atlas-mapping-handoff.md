# Handoff: bio-machine-learning-atlas-mapping / prepare-scientific-skill-tooling (delta)

- Updated: 2026-10-03
- Lane: 3 (batch 3b-1)
- Status: ready-for-phase
- Owner leaving: fix worker (fix2-lane3b-20261003)
- Next role: prepare-scientific-skill-tooling (delta mode), then reaudit-scientific-skill with a fresh auditor

## Source identity

- Origin: GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:machine-learning/atlas-mapping
- Working tree: F:\OpenScience\wt\ml-lane3-normalize\skills\bio-machine-learning-atlas-mapping (branch normalize/ml-lane3 off 29f5446; Skill dir untracked by design)
- Candidate tree hash: 8b4d96ad2465bd169dffb835c808d5783981f4acdc1f1e1121dbd9ab78dfbc04 (files=7, bytes=39831); preflight PASS (offline and online), no pycache
- Previous: ba864911e88a... (failed re-audit 84, Limited Release): audits/skills/bio-machine-learning-atlas-mapping/candidate@ba864911e88a-reaudit-lane3b-20261003/

## Completed this phase

- AM-006 fixed: `scripts/label_marker_check.py` requires `--markers`; reference-derived mode removed; prints an UNVERIFIED count line (no all-clear when labels are unchecked). No-flag run exits 2 with an argparse error.
- AM-007 fixed: overclaiming header removed; distance-gate threshold (p99) and p95 cost stated in SKILL.md; marker check added to usage-guide step 6 and Tips; T-cell markers replaced by genes present in the 1604-gene set.
- Verified on staged pair + both hold-outs (full pipeline rerun): curated check flags DC 0.160 (Monocytes removed) and DC 0.525 (B cells removed), nothing at baseline; T cells now CHECKED (retained 0.703 / 0.696 / 0.701, not flagged). Unverified: Megakaryocytes only (13/17/12 cells, under 20-cell minimum).
- Kept: seeded script, identical outputs (labels/gate numbers identical to prior run: 1.67%, 1.59%, 76.3% Unknown, 604 monocytes called DC).
- Evidence: F:\OpenScience\audits\bio-machine-learning-atlas-mapping\fix2-lane3b-20261003\ (fix-log.md, scripts\summary_*.json, run_*.log)

## Required next actions

1. Tooling delta: confirm label_marker_check.py interface change (`--markers` required, `--n-markers` removed) and updated T-cell markers file against TOOLS.md coverage map; no new dependency.
2. Fresh re-audit of the exact new bytes.

## Open findings and blockers

| ID | Severity | State | Evidence | Disposition |
|---|---|---|---|---|
| AM-006 | P1 | fixed | fix2\scripts\summary_*.json (marker_derived = no-flag run, rc 2) | verify in re-audit |
| AM-007 | P2 | fixed | same; SKILL.md, usage-guide.md diff | verify in re-audit |
| AM-001 | P1 | superseded by AM-006/007 (gate unchanged, documented as limited) | | |
| AM-002..005 | P2 | resolved, not regressed | summary_*.json | |

Blockers: none. Not executed by design: scPoli, popV, treeArches/scHPL, foundation models; Symphony, Azimuth (prose only).

## Environment and evidence

- Tool inventory: F:\OpenScience\audits\bio-machine-learning-atlas-mapping\TOOLS.md; environment unchanged (single-cell-transcriptomics-analyst runtime)
- Changed files: SKILL.md, usage-guide.md, references/pbmc-markers.json, scripts/label_marker_check.py, scripts/scarches_annotation.py (print string only)
- Restricted-access items: none
- Tooling impact: changed (runnable surface scripts/label_marker_check.py interface changed; no dependency/runtime change)

## Worktree safety

- Run-owned changes: the five files above; fix2-lane3b-20261003\; this handoff
- Pre-existing/user-owned: records test/validate.bats; shelf .vscode/; sibling Skill dirs; untouched
- Records state: uncommitted
- Product commits/pushes: none

## Transition assertion

- Next-phase prerequisites met: yes
