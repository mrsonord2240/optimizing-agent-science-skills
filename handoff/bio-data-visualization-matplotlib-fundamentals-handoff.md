# Handoff: bio-data-visualization-matplotlib-fundamentals / orchestrator (candidate-ready)

- Updated: 2026-10-03
- Lane: 1
- Status: candidate-ready (delta re-audit, description trim)
- Owner leaving: delta re-audit worker (lane E1, run delta-desc-20261003)
- Next role: orchestrator (commit at run close, local intake; or fix-scientific-skill for the open P2 first)

## Source identity

- Origin: GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:data-visualization/matplotlib-fundamentals
- Working tree: F:\OpenScience\wt\normalize-dv-lane1\skills\bio-data-visualization-matplotlib-fundamentals
- Branch/worktree: normalize/dv-lane1 off 29f5446 (Skill dir untracked by design)
- Candidate tree hash: f5acfdfb52509e5422c25f3dec2481ef4f182e5c0730398f2bd5bcd2d7fb2a90, files=5, bytes=24583 (preflight PASS at start and end)
- Certified baseline: 79a08cbdf5339dbf6f824d9532cc4720ef00102a9985831c5c56c051c8150611 (F:\optimizing-agent-science-skills\audits\skills\bio-data-visualization-matplotlib-fundamentals\candidate@79a08cbdf533-delta-dv1-20261003)
- Applicable audit: F:\optimizing-agent-science-skills\audits\skills\bio-data-visualization-matplotlib-fundamentals\candidate@f5acfdfb5250-delta-desc-20261003

## Completed this phase

- Delta qualified: reverting edits.json on a scratch copy reproduces the certified identity; only SKILL.md line 3 (`description:`) differs; new frontmatter parses as one YAML string.
- Decision: candidate-ready for the exact new identity, 90 Production Ready (static 89, execution 91.2, assertions 22/24); static score did not move; no veto, no open P0 or P1. Open P2 unchanged.
- Description verdict: accurate and a sufficient trigger; no new finding.
- Observation (not a finding): the description's 'single-cell embeddings' example overlaps dimensionality-reduction-plots, and seaborn is no longer named; adjust only if Sam wants.
- Record: F:\optimizing-agent-science-skills\audits\skills\bio-data-visualization-matplotlib-fundamentals\candidate@f5acfdfb5250-delta-desc-20261003 (supersedes candidate@79a08cbdf533-delta-dv1-20261003); views regenerated, `npm run audits:check` passes.

## Required next actions

1. Orchestrator: include this identity in the run-close shelf commit and local intake.
2. Remaining P2 below goes to a later fix run; none blocks readiness.

## Open findings and blockers

| ID | Severity | State | Evidence | Required disposition |
|---|---|---|---|---|
| MPL-011 | P2 | open | candidate@79a08cbdf533-delta-dv1-20261003 scripts/logs/d1_legend_probe.log, d1_ink_probe.log | text-only: write the public route with left=0.13, bottom=0.17, right=0.76, top=0.97 in SKILL.md and the matplotlib_phd.py comment; with right=0.76 alone the x label is cut at the page edge |

## Environment and evidence

- Tool inventory: F:\OpenScience\audit-envs\data-visualization\TOOLS-bio-data-visualization-matplotlib-fundamentals.md; fingerprint 8923551f7fdd6c7e0d23acaa651c76b899b97a6c94500f4e0fe61dd1fd81f721 (unchanged; no behaviour ran differently)
- Run evidence: F:\OpenScience\audits\bio-data-visualization-matplotlib-fundamentals\delta-desc-20261003 (scripts/, scripts/logs/qualify.log, scratch/ revert copy)
- Fix log: F:\OpenScience\audits\bio-data-visualization-matplotlib-fundamentals\fix-description-20261003\fix-log.md
- Restricted-access items: none
- Tooling impact: none

## Worktree safety

- Run-owned changes: run directory above only; Skill bytes not edited
- Pre-existing/user-owned changes: records test/validate.bats, shelf .vscode/ (untouched)
- Records state: uncommitted F:\optimizing-agent-science-skills\audits\skills\bio-data-visualization-matplotlib-fundamentals\candidate@f5acfdfb5250-delta-desc-20261003, plus regenerated audits/INDEX.md, BACKLOG.md, STATUS.md, STATUS.html (shared with other workers)
- Product commits/pushes: none

## Transition assertion

- Next-phase prerequisites met: yes
