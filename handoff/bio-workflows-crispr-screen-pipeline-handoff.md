# Handoff: bio-workflows-crispr-screen-pipeline / reaudit-scientific-skill (delta mode)

- Updated: 2026-10-04
- Lane: 1
- Status: fixed, awaiting delta re-audit
- Owner leaving: fix-scientific-skill worker (fix-003)
- Next role: reaudit-scientific-skill, delta mode (qc.py verdict logic + routes/qc.md prose)

## Source identity

- Origin: GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:workflows/crispr-screen-pipeline
- Working tree: F:\OpenScience\wt\recut-crispr-pipeline\skills\bio-workflows-crispr-screen-pipeline (branch recut/crispr-screen-pipeline, bytes uncommitted)
- Candidate identity: e609525649bd5394ec66676a9025250ab8c27db23039968d44c6dfeb0c872c81 (skill_preflight --offline --shape PASS, 19 files; warn: no Skill-root LICENSE)
- Prior certified identity: 05e557c86e77... (audits\skills\bio-workflows-crispr-screen-pipeline\candidate@05e557c86e77-reaudit-002\)

## Findings

| ID | Severity | State | Evidence |
|---|---|---|---|
| N-01 | P1 | fixed | fix-003\work\a375.log, bad.log, hap1.log, rrapass.log, cnpass.log |
| F-16 | P2 | fixed | routes/qc.md |
| F-10 | P2 | deferred-with-rationale | not needed for readiness |
| F-11 | P2 | deferred-with-rationale | not needed for readiness |
| F-15 residue, chronos NEGv1 header | P2 | unchanged | TOOLS.md Delta-001/002 |

## Changes

- scripts/qc.py (7 lines out, 9 in): default pattern also strips `R<n>` after a digit before `_`; ungroupable replicates give `QC INCOMPLETE`, exit 1 (FAIL wins if a gate failed); docstring updated.
- routes/qc.md: VISPR source for 0.8, 0.85 removed, outlier advice conditional, INCOMPLETE mentioned.
- Exact strings: F:\OpenScience\fix-evidence\recut-crispr-pipeline\fix-003\edits.json ; ledger.md beside it.

## Execution

HAP1 FAIL exit 1 (0.789); A375 default pattern FAIL exit 1 (0.780); ungroupable names INCOMPLETE exit 1; resampled HAP1 and A375 QC-passing tables PASS exit 0. Routing check not rerun (routes unchanged).

## Tooling and safety

- Tooling impact: none
- Pre-existing/user-owned: test\validate.bats untouched
- Product commits/pushes: none; records state uncommitted
- Transition: next-phase prerequisites met: yes
