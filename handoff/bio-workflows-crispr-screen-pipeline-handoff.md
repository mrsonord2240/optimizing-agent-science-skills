# Handoff: bio-workflows-crispr-screen-pipeline / reaudit-scientific-skill (delta mode)

- Updated: 2026-10-04
- Lane: 1
- Status: candidate-ready (delta re-audit passed)
- Owner leaving: delta re-audit worker
- Next role: orchestrator (commit to make `ready`, then intake)

## Identity

- Candidate: e609525649bd5394ec66676a9025250ab8c27db23039968d44c6dfeb0c872c81 (skill_preflight --offline --shape PASS, 19 files)
- Path: F:\OpenScience\wt\recut-crispr-pipeline\skills\bio-workflows-crispr-screen-pipeline (branch recut/crispr-screen-pipeline, bytes uncommitted)
- Certified base: 05e557c86e77... (reaudit-002); manifest diff: only scripts/qc.py and routes/qc.md differ, both as briefed
- Origin: GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:workflows/crispr-screen-pipeline

## Report and evidence

- Published: audits\skills\bio-workflows-crispr-screen-pipeline\candidate@e609525649bd-reaudit-delta-001\ (report.json, viewer.md, source-identity.json, scripts/)
- Raw: F:\OpenScience\fix-evidence\recut-crispr-pipeline\reaudit-delta-001\
- audits:index and audits:check pass; STATUS regenerated

## Readiness

Final 89 (carried 88), static 90, execution average 88.9, Layer 1 35.4, Layer 2 53.4, assertions 28/29 (96.6%). No veto, no open P0/P1. Routing check not rerun (routes, names, arguments unchanged); reaudit-002 routing carries.

## Executed (qc.py)

HAP1 FAIL exit 1; A375 default pattern groups, FAIL 0.780 exit 1; ungroupable names INCOMPLETE exit 1; ungroupable plus failed gate FAIL exit 1; `pattern=` override PASS exit 0; old-default names (_r1, _rep1, _A, _1, T18A) still group, PASS exit 0.

## Findings

| ID | State |
|---|---|
| N-01 P1 | resolved |
| F-16 P2 | resolved |
| F-10 P2 | open, deferred (drugz paired, static-only) |
| F-11 P2 | open, deferred (no Skill-root LICENSE) |
| F-15 residue, chronos NEGv1 header | open P2, disclosed in TOOLS.md |

## State

- Tooling impact: none
- Worktree: candidate bytes uncommitted; records show new untracked run dir plus modified INDEX.md, BACKLOG.md (STATUS files regenerated)
- Pre-existing/user-owned: test\validate.bats untouched
- Product commits/pushes: none
