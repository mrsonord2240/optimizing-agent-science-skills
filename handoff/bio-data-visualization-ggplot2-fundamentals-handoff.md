# Handoff: bio-data-visualization-ggplot2-fundamentals / orchestrator (candidate-ready)

- Updated: 2026-10-03
- Lane: 1
- Status: candidate-ready (delta re-audit)
- Owner leaving: delta re-audit worker (lane D1, run delta-dv1-20261003)
- Next role: orchestrator (commit at run close, local intake; or fix-scientific-skill for the open P2 first)

## Source identity

- Origin: GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:data-visualization/ggplot2-fundamentals
- Working tree: F:\OpenScience\wt\normalize-dv-lane1\skills\bio-data-visualization-ggplot2-fundamentals
- Branch/worktree: normalize/dv-lane1 off 29f5446 (Skill dir untracked by design)
- Candidate tree hash: 228c088cf299564fd21d2b9d79a3963e5c0b4a500158bcb4732a1b277e6160e6, files=5, bytes=23322 (preflight PASS at start and end)
- Certified baseline: be703ae7f69598daa981d477afa71a873d0616a2f2830936b575c014a1f3f120 (F:\optimizing-agent-science-skills\audits\skills\bio-data-visualization-ggplot2-fundamentals\candidate@be703ae7f695-reaudit-dv2-20261003)
- Applicable audit: F:\optimizing-agent-science-skills\audits\skills\bio-data-visualization-ggplot2-fundamentals\candidate@228c088cf299-delta-dv1-20261003

## Completed this phase

- Delta qualified: reverting the fix-log edits on a scratch copy reproduces the certified identity; changed files differ only in prose, comments or string literals (diffs in scripts/diff_*.txt of the run).
- Decision: candidate-ready for the exact new identity, 90 Production Ready (static 90, execution 90.6, assertions 21/22), no veto, no open P0 or P1. GG-011 and GG-012 closed.
- No new findings. Envelope numbers re-run on ggplot2 4.0.3 (probe log identical to the certifying probe); ggplot2 3.5.2 rows carried (no script byte changed).
- Record: F:\optimizing-agent-science-skills\audits\skills\bio-data-visualization-ggplot2-fundamentals\candidate@228c088cf299-delta-dv1-20261003 (supersedes candidate@be703ae7f695-reaudit-dv2-20261003); views regenerated, `npm run audits:check` passes.

## Required next actions

1. Orchestrator: include this identity in the run-close shelf commit and local intake.
2. Remaining P2 below goes to a later fix run; none blocks readiness.

## Open findings and blockers

| ID | Severity | State | Evidence | Required disposition |
|---|---|---|---|---|
| GG-010 | P2 | open | certifying record, input 3 | needs code: NA label among smallest padj stops create_volcano; next fix run |

## Environment and evidence

- Tool inventory: F:\OpenScience\audit-envs\data-visualization\TOOLS-bio-data-visualization-ggplot2-fundamentals.md; fingerprint 8923551f7fdd6c7e0d23acaa651c76b899b97a6c94500f4e0fe61dd1fd81f721 over snapshots\lane1_versions.txt (re-hashed identical at start and end)
- Run evidence: F:\OpenScience\audits\bio-data-visualization-ggplot2-fundamentals\delta-dv1-20261003 (scripts/, scripts/logs/, scratch/ revert copy)
- Fix log: F:\OpenScience\audits\bio-data-visualization-ggplot2-fundamentals\fix-textbatch-20261003\fix-log.md
- Restricted-access items: none
- Tooling impact: none

## Worktree safety

- Run-owned changes: run directory above only; Skill bytes not edited; no __pycache__ in the Skill tree
- Pre-existing/user-owned changes: records test/validate.bats, shelf .vscode/ (untouched)
- Records state: uncommitted F:\optimizing-agent-science-skills\audits\skills\bio-data-visualization-ggplot2-fundamentals\candidate@228c088cf299-delta-dv1-20261003, plus regenerated audits/INDEX.md, BACKLOG.md, STATUS.md, STATUS.html (shared with other workers)
- Product commits/pushes: none

## Transition assertion

- Next-phase prerequisites met: yes
