# Handoff: bio-machine-learning-atlas-mapping / orchestrator (commit and intake)

- Updated: 2026-10-03
- Lane: 3 (batch 3b-1)
- Status: candidate-ready
- Owner leaving: final re-audit worker (fresh auditor, final mode)
- Next role: orchestrator (commit the exact bytes; AM-008 optional, small script fix via fix-scientific-skill then delta re-audit)

## Source identity

- Origin: GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:machine-learning/atlas-mapping
- Working tree: F:\OpenScience\wt\ml-lane3-normalize\skills\bio-machine-learning-atlas-mapping (branch normalize/ml-lane3 off 29f5446; Skill dir untracked by design)
- Candidate tree hash: 8b4d96ad2465bd169dffb835c808d5783981f4acdc1f1e1121dbd9ab78dfbc04 (files=7, bytes=39831); preflight PASS offline before and after, no pycache
- Applicable audit: F:\optimizing-agent-science-skills\audits\skills\bio-machine-learning-atlas-mapping\candidate@8b4d96ad2465-final-reaudit-lane3b-20261003\ (published, audits:check clean)

## Completed this phase

- Readiness: candidate-ready. Final 87 (Production Ready), static 88, execution average 85.7, Layer 1 33.8, Layer 2 51.8, assertions 28/29 = 96.6%, no veto, no P0/P1.
- AM-006 closed: no-flag run rc 2, usage error, empty stdout, in all 4 runs; no reference-derived path in script, SKILL.md or usage-guide; curated runs flag DC 0.160 (Monocytes removed) and 0.525 (B removed), nothing at baseline (T 0.703).
- AM-007 closed: header plain, marker check in usage-guide, distance-gate p99/p95 numbers reproduce (0.0%; 25.4% and 99.4% held-out, 7.7% and 14.3% overall), UNVERIFIED line on every run (13 / 17 / 12 cells).
- AM-001 documented-limited; AM-002..005 not regressed (seeded reruns 2638/2638 identical, latent diff 0.0, query_annotated.h5ad written, DataFrame (2638, 8), snippets ran as written, not-executed labels present).
- New P2 AM-008 (open, non-blocking): all-unchecked marker file crashes with AttributeError (rc 1, fails closed) and listed-versus-used marker count is not shown.

## Required next actions

1. Orchestrator: commit the exact bytes above and proceed to intake. Do not edit Skill bytes without a new audit.
2. Optional: AM-008 fix is a small script change (guard empty result, add n_listed and low-count warning); needs a delta/full re-audit because it touches a script.

## Open findings and blockers

| ID | Severity | State | Evidence | Required disposition |
|---|---|---|---|---|
| AM-008 | P2 | open, non-blocking | scripts\evidence\driven_marker_runs.log in the published record | script guard plus n_listed column |
| AM-001 | P1 (prior) | documented-limited | SKILL.md measured table; summary_f_*.json | none; method limitation, disclosed |

Judgment notes: 0.6 cutoff margins 0.075 to 0.10 on one PBMC pair (disclosed as a priori, one pair); labels judged on one marker are visible only via n_markers; Skill would not lead an agent to trust a gated label.

## Environment and evidence

- Tool inventory: F:\OpenScience\audits\bio-machine-learning-atlas-mapping\TOOLS.md (sha256 35fbb5d8b27d7b76a9e1cfd1390ddc6315ef2156d15ff8f75c3e75d6516e9d40); environment fingerprint 20291632e93a3881e9704027dfe1d61f2f02fb40d64667ea992bb557bbb336a6 (unchanged; nothing installed)
- Run evidence: F:\OpenScience\audits\bio-machine-learning-atlas-mapping\final-reaudit-lane3b-20261003\ (scripts\evidence, logs, helpers)
- Restricted-access items: none. Not executed by design: scPoli, popV, treeArches/scHPL, foundation models (heavy-optional); Symphony, Azimuth (prose only); all labelled in the Skill
- Tooling impact: none

## Worktree safety

- Run-owned changes: final-reaudit-lane3b-20261003\ run dir; records audits\skills\bio-machine-learning-atlas-mapping\candidate@8b4d96ad2465-final-reaudit-lane3b-20261003\; regenerated audits\INDEX.md, BACKLOG.md, STATUS.md, STATUS.html; this handoff
- Pre-existing/user-owned untouched: records test\validate.bats; shelf .vscode\; sibling Skill dirs
- Records state: uncommitted (orchestrator commits)
- Product commits/pushes: none

## Transition assertion

- Next-phase prerequisites met: yes
