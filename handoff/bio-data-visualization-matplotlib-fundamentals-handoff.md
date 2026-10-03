# Handoff: bio-data-visualization-matplotlib-fundamentals / orchestrator (candidate-ready)

- Updated: 2026-10-03
- Lane: 1
- Status: candidate-ready (delta re-audit)
- Owner leaving: delta re-audit worker (lane D1, run delta-dv1-20261003)
- Next role: orchestrator (commit at run close, local intake; or fix-scientific-skill for the open P2 first)

## Source identity

- Origin: GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:data-visualization/matplotlib-fundamentals
- Working tree: F:\OpenScience\wt\normalize-dv-lane1\skills\bio-data-visualization-matplotlib-fundamentals
- Branch/worktree: normalize/dv-lane1 off 29f5446 (Skill dir untracked by design)
- Candidate tree hash: 79a08cbdf5339dbf6f824d9532cc4720ef00102a9985831c5c56c051c8150611, files=5, bytes=24925 (preflight PASS at start and end)
- Certified baseline: f1efaf7eef6c18085eabaa140a3696db8e35e5d14624396d1f7c22643d398e7a (F:\optimizing-agent-science-skills\audits\skills\bio-data-visualization-matplotlib-fundamentals\candidate@f1efaf7eef6c-reaudit-dv2-20261003)
- Applicable audit: F:\optimizing-agent-science-skills\audits\skills\bio-data-visualization-matplotlib-fundamentals\candidate@79a08cbdf533-delta-dv1-20261003

## Completed this phase

- Delta qualified: reverting the fix-log edits on a scratch copy reproduces the certified identity; changed files differ only in prose, comments or string literals (diffs in scripts/diff_*.txt of the run).
- Decision: candidate-ready for the exact new identity, 90 Production Ready (static 89, execution 91.2, assertions 22/24), no veto, no open P0 or P1. MPL-010 closed (disclosure verified).
- MPL-011 is introduced by the delta wording (it copied the certifying record's own suggestion). Disclosure facts verified: private _figure, 0.13.2 only, 22 % reserve, 29-character title covers 13.0 mm.
- Record: F:\optimizing-agent-science-skills\audits\skills\bio-data-visualization-matplotlib-fundamentals\candidate@79a08cbdf533-delta-dv1-20261003 (supersedes candidate@f1efaf7eef6c-reaudit-dv2-20261003); views regenerated, `npm run audits:check` passes.

## Required next actions

1. Orchestrator: include this identity in the run-close shelf commit and local intake.
2. Remaining P2 below goes to a later fix run; none blocks readiness.

## Open findings and blockers

| ID | Severity | State | Evidence | Required disposition |
|---|---|---|---|---|
| MPL-011 | P2 | open (new) | scripts/logs/d1_legend_probe.log, d1_ink_probe.log, scripts/figures/right076_only.png | text-only: write the public route with left=0.13, bottom=0.17, right=0.76, top=0.97 in SKILL.md and the matplotlib_phd.py comment; with right=0.76 alone the x label is cut at the page edge |

## Environment and evidence

- Tool inventory: F:\OpenScience\audit-envs\data-visualization\TOOLS-bio-data-visualization-matplotlib-fundamentals.md; fingerprint 8923551f7fdd6c7e0d23acaa651c76b899b97a6c94500f4e0fe61dd1fd81f721 over snapshots\lane1_versions.txt (re-hashed identical at start and end)
- Run evidence: F:\OpenScience\audits\bio-data-visualization-matplotlib-fundamentals\delta-dv1-20261003 (scripts/, scripts/logs/, scratch/ revert copy)
- Fix log: F:\OpenScience\audits\bio-data-visualization-matplotlib-fundamentals\fix-textbatch-20261003\fix-log.md
- Restricted-access items: none
- Tooling impact: none

## Worktree safety

- Run-owned changes: run directory above only; Skill bytes not edited; no __pycache__ in the Skill tree
- Pre-existing/user-owned changes: records test/validate.bats, shelf .vscode/ (untouched)
- Records state: uncommitted F:\optimizing-agent-science-skills\audits\skills\bio-data-visualization-matplotlib-fundamentals\candidate@79a08cbdf533-delta-dv1-20261003, plus regenerated audits/INDEX.md, BACKLOG.md, STATUS.md, STATUS.html (shared with other workers)
- Product commits/pushes: none

## Transition assertion

- Next-phase prerequisites met: yes
