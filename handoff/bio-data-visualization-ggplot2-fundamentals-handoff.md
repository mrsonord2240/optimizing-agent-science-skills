# Handoff: bio-data-visualization-ggplot2-fundamentals / orchestrator (candidate-ready)

- Updated: 2026-10-03
- Lane: 1
- Status: candidate-ready (delta re-audit, description trim)
- Owner leaving: delta re-audit worker (lane E1, run delta-desc-20261003)
- Next role: orchestrator (commit at run close, local intake; or fix-scientific-skill for the open P2 first)

## Source identity

- Origin: GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:data-visualization/ggplot2-fundamentals
- Working tree: F:\OpenScience\wt\normalize-dv-lane1\skills\bio-data-visualization-ggplot2-fundamentals
- Branch/worktree: normalize/dv-lane1 off 29f5446 (Skill dir untracked by design)
- Candidate tree hash: 9d1247b0d8cd48c336a6e7ca866603cc3499b667e759af8f866583d076f0507b, files=5, bytes=23077 (preflight PASS at start and end)
- Certified baseline: 228c088cf299564fd21d2b9d79a3963e5c0b4a500158bcb4732a1b277e6160e6 (F:\optimizing-agent-science-skills\audits\skills\bio-data-visualization-ggplot2-fundamentals\candidate@228c088cf299-delta-dv1-20261003)
- Applicable audit: F:\optimizing-agent-science-skills\audits\skills\bio-data-visualization-ggplot2-fundamentals\candidate@9d1247b0d8cd-delta-desc-20261003

## Completed this phase

- Delta qualified: reverting edits.json on a scratch copy reproduces the certified identity; only SKILL.md line 3 (`description:`) differs; new frontmatter parses as one YAML string.
- Decision: candidate-ready for the exact new identity, 90 Production Ready (static 90, execution 90.6, assertions 21/22); static score did not move; no veto, no open P0 or P1. Open P2 unchanged.
- Description verdict: accurate and a sufficient trigger; no new finding.
- Record: F:\optimizing-agent-science-skills\audits\skills\bio-data-visualization-ggplot2-fundamentals\candidate@9d1247b0d8cd-delta-desc-20261003 (supersedes candidate@228c088cf299-delta-dv1-20261003); views regenerated, `npm run audits:check` passes.

## Required next actions

1. Orchestrator: include this identity in the run-close shelf commit and local intake.
2. Remaining P2 below goes to a later fix run; none blocks readiness.

## Open findings and blockers

| ID | Severity | State | Evidence | Required disposition |
|---|---|---|---|---|
| GG-010 | P2 | open | certifying record, input 3 | needs code: NA label among smallest padj stops create_volcano; next fix run |

## Environment and evidence

- Tool inventory: F:\OpenScience\audit-envs\data-visualization\TOOLS-bio-data-visualization-ggplot2-fundamentals.md; fingerprint 8923551f7fdd6c7e0d23acaa651c76b899b97a6c94500f4e0fe61dd1fd81f721 (unchanged; no behaviour ran differently)
- Run evidence: F:\OpenScience\audits\bio-data-visualization-ggplot2-fundamentals\delta-desc-20261003 (scripts/, scripts/logs/qualify.log, scratch/ revert copy)
- Fix log: F:\OpenScience\audits\bio-data-visualization-ggplot2-fundamentals\fix-description-20261003\fix-log.md
- Restricted-access items: none
- Tooling impact: none

## Worktree safety

- Run-owned changes: run directory above only; Skill bytes not edited
- Pre-existing/user-owned changes: records test/validate.bats, shelf .vscode/ (untouched)
- Records state: uncommitted F:\optimizing-agent-science-skills\audits\skills\bio-data-visualization-ggplot2-fundamentals\candidate@9d1247b0d8cd-delta-desc-20261003, plus regenerated audits/INDEX.md, BACKLOG.md, STATUS.md, STATUS.html (shared with other workers)
- Product commits/pushes: none

## Transition assertion

- Next-phase prerequisites met: yes
