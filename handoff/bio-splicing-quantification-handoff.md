# Handoff: bio-splicing-quantification / orchestrator (commit and intake)

- Updated: 2026-10-03
- Lane: 2
- Status: candidate-ready
- Owner leaving: final re-audit worker (lane 2, run-reaudit-1)
- Next role: orchestrator (commit the Skill bytes to make them `ready`, then Marketplace intake)

## Source identity

- Origin: GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:alternative-splicing/splicing-quantification
- Working tree: F:\OpenScience\wt\norm-bio-splicing-quantification\skills\bio-splicing-quantification (untracked/uncommitted by design)
- Branch/worktree: normalize/bio-splicing-quantification, started at 29f5446
- Candidate tree hash: 0c0354add99bca532a1c7168b94a08a1923249a1a7adfddd7f7e9997953355bf (files=5, bytes=42079); `skill_preflight --offline` PASS at start and end (one expected no-Skill-root-LICENSE warning); bytes untouched
- Applicable audit: F:\optimizing-agent-science-skills\audits\skills\bio-splicing-quantification\candidate@0c0354add99b-run-reaudit-1 (this identity, 85 / Production Ready); supersedes candidate@1e34dbd9664e-run-initial-1 (64, Reject)

## Completed this phase

- Independent final re-audit: decision **candidate-ready** for the exact identity. Static 84, execution average 86.3 (7 inputs), final 85.4 (85), Layer 1 34.9, Layer 2 51.4, assertions 34/36 (94.4%), Skill veto PASS, Research veto PASS. Margin over the 85 gate is narrow.
- SQ-01..SQ-11 all reproduced as fixed on fresh real tool output (fresh rMATS 4.4.0 runs; independent stdlib oracle: 30 real-output cases of 5 event types x JC/JCEC x min reads 0/10/20 with zero error; 10 engineered NA/low-read combinations; SUPPA2, regtools/leafcutter XS, IRFinder BuildRefFromSTARRef plus FastQ SE/PE all re-run). SQ-08 fixed with a caveat (SQ-13).
- Published record, regenerated INDEX/BACKLOG/STATUS (`npm run audits:index`, `audits:check` clean)
- MAJIQ V3/VOILA (restricted licence) and VAST-TOOLS (heavy optional) confirmed labelled not executed in the Skill; not attempted

## Required next actions

1. Orchestrator: commit the Skill bytes (shelf repo) and the records change; run Marketplace intake
2. Optional later fix pass for SQ-12 and SQ-13 (P2, do not block); any byte change needs a new identity and at least delta-mode review

## Open findings and blockers

| ID | Severity | State | Evidence | Required disposition |
|---|---|---|---|---|
| SQ-12 | P2 | open (new) | run-reaudit-1\evidence\39_adversarial.log | `parse_rmats_output` raises raw KeyError on a header-only (zero-event) rMATS file; return an empty frame or a clear error |
| SQ-13 | P2 | open (new) | run-reaudit-1\evidence\32_snippet_and_forms.log | JC IncFormLen 148/74 holds for 719 of 958 real SE rows; say "for exons and introns longer than a read" |
| SQ-01..SQ-11 | P1/P2 | resolved | record viewer.md disposition table | none |

Blockers: none. Not executed by design: MAJIQ V3/VOILA, VAST-TOOLS; also Shiba, MicroExonator, S-IRFindeR, iREAD, IRFinder-S 2.0 (installable is 1.3.1); all labelled in the Skill.

## Environment and evidence

- Tool inventory: F:\OpenScience\audits\bio-splicing-quantification\TOOLS.md (sha256 13b0c7a4...fadcec; environment fingerprint combined 20c07bbbf63a972c04364225b028c9c83e0ee45a0ee9ee775cc56d7a8c26ad3c, re-verified unchanged at start)
- Run evidence: F:\OpenScience\audits\bio-splicing-quantification\run-reaudit-1\ (scripts\ published; evidence\ logs and out\ raw local); prior: run-initial-1, run-fix-1, run-tooling-delta-1
- Restricted-access items: MAJIQ V3 (licence form), VAST-TOOLS (VASTDB 6.7 GB heavy optional)
- Tooling impact: none (no environment, package or staging change; `smoke_irfinder.sh` not rerun; IRFinder reference rebuilt only under run-reaudit-1\out)

## Worktree safety

- Run-owned changes: run-reaudit-1\ (audits root), records audits\skills\bio-splicing-quantification\candidate@0c0354add99b-run-reaudit-1\, regenerated audits\INDEX.md BACKLOG.md STATUS.md STATUS.html, this handoff
- Pre-existing/user-owned changes: records test/validate.bats (untracked), shelf .vscode/ (untracked); untouched
- Records state: uncommitted
- Product commits/pushes: none

## Transition assertion

- Next-phase prerequisites met: yes (candidate-ready; orchestrator commits and runs intake)
