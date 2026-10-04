# Handoff: bio-data-visualization-volcano-and-ma-plots / orchestrator (candidate-ready)

- Updated: 2026-10-03
- Lane: 1
- Status: candidate-ready (delta re-audit, description trim)
- Owner leaving: delta re-audit worker (lane E1, run delta-desc-20261003)
- Next role: orchestrator (commit at run close, local intake; or fix-scientific-skill for the open P2 first)

## Source identity

- Origin: GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:data-visualization/volcano-and-ma-plots
- Working tree: F:\OpenScience\wt\normalize-dv-lane1\skills\bio-data-visualization-volcano-and-ma-plots
- Branch/worktree: normalize/dv-lane1 off 29f5446 (Skill dir untracked by design)
- Candidate tree hash: 0bc1e67d46d6b7cfdffd1d42ef1f35779a7f0fe712d8460e3ee602684bd4aeeb, files=7, bytes=37711 (preflight PASS at start and end)
- Certified baseline: a86f2698a953bfc46b2db74122acd9d20a49a5e0195bace6e3663282a44d8d83 (F:\optimizing-agent-science-skills\audits\skills\bio-data-visualization-volcano-and-ma-plots\candidate@a86f2698a953-delta-dv1-20261003)
- Applicable audit: F:\optimizing-agent-science-skills\audits\skills\bio-data-visualization-volcano-and-ma-plots\candidate@0bc1e67d46d6-delta-desc-20261003

## Completed this phase

- Delta qualified: reverting edits.json on a scratch copy reproduces the certified identity; only SKILL.md line 3 (`description:`) differs; new frontmatter parses as one YAML string.
- Decision: candidate-ready for the exact new identity, 89 Production Ready (static 89, execution 88.8, assertions 23/24); static score did not move; no veto, no open P0 or P1. Open P2 unchanged.
- Description verdict: accurate and a sufficient trigger; no new finding.
- Record: F:\optimizing-agent-science-skills\audits\skills\bio-data-visualization-volcano-and-ma-plots\candidate@0bc1e67d46d6-delta-desc-20261003 (supersedes candidate@a86f2698a953-delta-dv1-20261003); views regenerated, `npm run audits:check` passes.

## Required next actions

1. Orchestrator: include this identity in the run-close shelf commit and local intake.
2. Remaining P2 below goes to a later fix run; none blocks readiness.

## Open findings and blockers

| ID | Severity | State | Evidence | Required disposition |
|---|---|---|---|---|
| VOL-010 | P2 | open | certifying record, input 2 | needs code: y_cap labels overlap on the cap; next fix run |

## Environment and evidence

- Tool inventory: F:\OpenScience\audit-envs\data-visualization\TOOLS-bio-data-visualization-volcano-and-ma-plots.md; fingerprint 8923551f7fdd6c7e0d23acaa651c76b899b97a6c94500f4e0fe61dd1fd81f721 (unchanged; no behaviour ran differently)
- Run evidence: F:\OpenScience\audits\bio-data-visualization-volcano-and-ma-plots\delta-desc-20261003 (scripts/, scripts/logs/qualify.log, scratch/ revert copy)
- Fix log: F:\OpenScience\audits\bio-data-visualization-volcano-and-ma-plots\fix-description-20261003\fix-log.md
- Restricted-access items: none
- Tooling impact: none

## Worktree safety

- Run-owned changes: run directory above only; Skill bytes not edited
- Pre-existing/user-owned changes: records test/validate.bats, shelf .vscode/ (untouched)
- Records state: uncommitted F:\optimizing-agent-science-skills\audits\skills\bio-data-visualization-volcano-and-ma-plots\candidate@0bc1e67d46d6-delta-desc-20261003, plus regenerated audits/INDEX.md, BACKLOG.md, STATUS.md, STATUS.html (shared with other workers)
- Product commits/pushes: none

## Transition assertion

- Next-phase prerequisites met: yes
