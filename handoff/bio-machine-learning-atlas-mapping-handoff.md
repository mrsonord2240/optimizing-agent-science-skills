# Handoff: bio-machine-learning-atlas-mapping / fix-scientific-skill

- Updated: 2026-10-03
- Lane: 3 (batch 3b-1)
- Status: phase-failed (re-audit rejected the exact bytes; not candidate-ready)
- Owner leaving: final re-audit worker (lane 3b-1, independent)
- Next role: fix-scientific-skill

## Source identity

- Origin: GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:machine-learning/atlas-mapping
- Working tree: F:\OpenScience\wt\ml-lane3-normalize\skills\bio-machine-learning-atlas-mapping (branch normalize/ml-lane3 off 29f5446; Skill dirs untracked by design)
- Candidate tree hash: ba864911e88a7d48e4576f9f7f4f1668ef0ed85ddd429c151bbb6ebfc39cd094 (files=7, bytes=39154); preflight PASS before and after, no pycache; Skill bytes not edited
- Applicable audit: audits/skills/bio-machine-learning-atlas-mapping/candidate@ba864911e88a-reaudit-lane3b-20261003/ (final 84, Limited Release; static 85, exec avg 83.3, L1 32.8, L2 50.5, assertions 25/28 = 89.3%, research veto PASS). Run root: F:\OpenScience\audits\bio-machine-learning-atlas-mapping\reaudit-lane3b-20261003\

## Completed this phase

- Readiness: NOT candidate-ready. Gates missed: assertion pass rate 89.3% (< 90) and execution average 83.3 (< 85).
- Reproduced every AM-001 number (kNN gate 1.67% / 1.59% / 76.3% Unknown; 604/630 monocytes called DC; curated DC 0.160 / 0.525; derived DC 0.730 missed, T 0.563 false flag, T 0.605 baseline; T NOT CHECKED with curated). Own distance gate (p99) 0.0% both hold-outs.
- SKILL.md python blocks ran as written (rc ok, DataFrame proba, accuracy 0.972). Canonical run deterministic vs tooling run (labels identical, latent diff 0.0).
- AM-002..005 verified fixed. Heavy-optional and prose-only methods are labelled not executed.
- Published record, regenerated views, `npm run audits:check` clean.

## Required next actions

1. AM-006 (P1): `scripts/label_marker_check.py` default (reference-derived) mode prints "Flagged labels: none" on the Monocytes hold-out. Make `--markers` required, or print a loud UNRELIABLE banner and qualify the all-clear; one SKILL.md sentence. Small local script change.
2. AM-007 (P2, text only): retitle "Out-of-Distribution Gating (the step that makes labels trustworthy)"; add the marker check and its limitation to usage-guide.md (steps 5-6, Tips); state the distance-gate threshold (p99; at p95 it flags 25% Mono / 99% B at 8-14% overall false flags) in the table note; note curated T-cell markers are absent from the shipped 1604-gene set.
3. After the fix, a tooling-delta is likely unnecessary (script change only); re-audit in delta-or-full mode per orchestrator.

## Open findings and blockers

| ID | Severity | State | Evidence | Required disposition |
|---|---|---|---|---|
| AM-006 | P1 | open (residual of AM-001) | record scripts/evidence/marker_derived_{mono,bcell}.tsv | script guard |
| AM-007 | P2 | open | viewer.md ledger | text |
| AM-001 | P1 | superseded by AM-006/AM-007 (prose claim cleared, gate unchanged by design) | | |
| AM-002..005 | P2 | resolved | | |

Blockers: none. Restricted-access items: none. Not executed by design: scPoli, popV, treeArches/scHPL, foundation models (heavy-optional); Symphony, Azimuth (prose only).

## Environment and evidence

- Tool inventory: F:\OpenScience\audits\bio-machine-learning-atlas-mapping\TOOLS.md (sha256 0818c47cd78b8dc26256c0fd3e0d28c04a1602c0ef60b5cbd2c74669aad225d1); environment fingerprint 20291632e93a3881e9704027dfe1d61f2f02fb40d64667ea992bb557bbb336a6, unchanged
- Run evidence: reaudit-lane3b-20261003\scripts\evidence\; harness scripts\run_case.py, run_skill_snippets.py, distance_gate_check.py
- Tooling impact: none expected for the fix (a runtime-light script edit); uncertain only if label_marker_check.py changes its interface

## Worktree safety

- Run-owned changes: reaudit-lane3b-20261003\, audits/skills/bio-machine-learning-atlas-mapping/candidate@ba864911e88a-reaudit-lane3b-20261003/, regenerated audits/{INDEX,BACKLOG,STATUS}.md and STATUS.html, this handoff
- Pre-existing/user-owned: records test/validate.bats; shelf .vscode/; sibling Skill dirs; untouched
- Records state: uncommitted (orchestrator commits)
- Product commits/pushes: none

## Transition assertion

- Next-phase prerequisites met: yes
