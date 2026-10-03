# Handoff: bio-splicing-quantification / orchestrator (commit, intake)

- Updated: 2026-10-03
- Lane: 2 (delta re-audit lane D2)
- Status: candidate-ready
- Owner leaving: delta re-audit worker D2 (fresh auditor)
- Next role: orchestrator (commit exact bytes to make them ready); fix-scientific-skill for SQ-12 and SQ-14 when scheduled

## Source identity

- Working tree: F:\OpenScience\wt\norm-bio-splicing-quantification\skills\bio-splicing-quantification (untracked by design)
- Candidate identity: 247bcf26db1833bc443dc9d651595ef84068f43a2593067f7c3bda72bd7e7adc, files=5, bytes=42306 (preflight PASS before and after)
- Applicable audit: F:\optimizing-agent-science-skills\audits\skills\bio-splicing-quantification\candidate@247bcf26db18-run-reaudit-2 (supersedes candidate@0c0354add99b-run-reaudit-1)

## Completed this phase

- Delta qualified: 4 of 5 files byte-identical to the certified manifest; reversing the one SQ-13 sentence reproduces SKILL.md sha256 899e98ff...b622f exactly.
- Score 85 (static 84, execution 86.4, assertions 35/37, L1 34.9, L2 51.6); narrow margin over the 85 gate.
- SQ-13 resolved (719 of 958 chrX SE rows at 148/74, max 148/74, PSI formula still reproduces IncLevel).
- New P2 SQ-14 (text only): the new clause "reached only for exons at least read-length long" is inexact (SkipFormLen is 74 in all 958 rows including a 1 nt exon; a 74 nt exon already gives 148).

## Open findings

| ID | Severity | State | Evidence | Required disposition |
|---|---|---|---|---|
| SQ-12 | P2 | open, untouched | run-reaudit-1 report | code fix in parse_rmats_output for a header-only file |
| SQ-14 | P2 | open, new | run-reaudit-2\viewer.md | reword condition: IncFormLen maxima for exons >= readLength - 1; SkipFormLen stays readLength - 1 |
| other P2s | P2 | unchanged | certified record | as recorded |

## Environment and evidence

- TOOLS.md: F:\OpenScience\audits\bio-splicing-quantification\TOOLS.md (environments unchanged)
- Run evidence: F:\OpenScience\audits\bio-splicing-quantification\run-reaudit-2\ (reused rMATS outputs of run-reaudit-1)
- Not executed: as certified (MAJIQ V3, VAST-TOOLS, Shiba and others, labelled); IRFinder smoke not run
- Tooling impact: none

## Worktree safety

- Run-owned changes: run-reaudit-2 run dir, published record, this handoff, regenerated audit views
- Pre-existing/user-owned: records test/validate.bats, shelf .vscode/
- Product commits/pushes: none

## Transition assertion

- Next-phase prerequisites met: yes
