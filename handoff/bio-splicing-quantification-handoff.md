# Handoff: bio-splicing-quantification / orchestrator (commit, intake)

- Updated: 2026-10-03
- Lane: 2 (delta re-audit lane E2, description trim)
- Status: done (shelf e58c885, intake accepted at validator a1d820d, exported to bioSkills-Improved fff47bd; worktree removed)
- Owner leaving: delta re-audit worker E2 (fresh auditor)
- Next role: none; open P2s wait for a later refinement run

## Source identity

- Origin: GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:alternative-splicing/splicing-quantification
- Working tree: F:\OpenScience\wt\norm-bio-splicing-quantification\skills\bio-splicing-quantification (untracked by design)
- Candidate tree hash: 1010225625de8bd6106b0c187dd8b1459d3ae84e91abeb44a7df95a8bdef792d, files=5, bytes=41707 (skill_preflight --offline PASS before and after)
- Applicable audit: F:\optimizing-agent-science-skills\audits\skills\bio-splicing-quantification\candidate@1010225625de-reaudit-delta2-20261003 (supersedes candidate@247bcf26db18-run-reaudit-2, certified identity 247bcf26db18)

## Completed this phase

- Delta qualified: only SKILL.md differs, by exactly the `description:` line; reverting edits.json on a scratch copy reproduces 247bcf26db18 exactly. Frontmatter parses (PyYAML) as one string.
- Trimmed description judged accurate and sufficient; no finding. Siblings (differential, long-read, single-cell, qc, outlier, variant-prediction, isoform-switching, sashimi) checked.
- Score unchanged: 85 (static 84 = 33.6, execution 86.4 = 51.84; sum 85.44, margin 0.44 over the gate). No category moved.
- Open P2s unchanged.

## Required next actions

1. Orchestrator: commit the exact bytes above and proceed to intake. Do not edit Skill bytes without a new audit.
2. Open findings below are unchanged except where marked new.

## Open findings and blockers

| ID | Severity | State | Evidence | Required disposition |
|---|---|---|---|---|
| SQ-12 | P2 | open, unchanged | certified report | code fix in parse_rmats_output for a header-only file |
| SQ-14 | P2 | open, unchanged | certified viewer.md | reword condition: IncFormLen maxima for exons >= readLength - 1; SkipFormLen stays readLength - 1 |

## Environment and evidence

- TOOLS.md: F:\OpenScience\audits\bio-splicing-quantification\TOOLS.md (unchanged)
- Run evidence: F:\OpenScience\audits\bio-splicing-quantification\reaudit-delta2-20261003\ (scripts/qualify_delta2.py, logs/qualify.json); certified execution evidence reused, nothing rerun
- Not executed: as certified; tools\smoke_irfinder.sh not run
- Tooling impact: none (frontmatter text only)

## Worktree safety

- Run-owned changes: the run dir, the published record, this handoff, regenerated audit views
- Pre-existing/user-owned: records test/validate.bats, shelf .vscode/; sibling Skill dirs untouched
- Records state: uncommitted (orchestrator commits)
- Product commits/pushes: none

## Transition assertion

- Next-phase prerequisites met: yes
