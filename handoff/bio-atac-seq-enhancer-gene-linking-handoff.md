# Handoff: bio-atac-seq-enhancer-gene-linking / orchestrator (commit, then intake)

- Updated: 2026-09-30T06:30-07:00
- Lane: 2
- Status: candidate-ready
- Owner leaving: reaudit-scientific-skill worker (independent)
- Next role: optimize-scientific-skills orchestrator (commit to optimized shelf); no fix needed

## Source identity

- Origin: GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:atac-seq/enhancer-gene-linking
- Working tree: F:\OpenScience\wt\atac-enhancer-gene-linking\skills\bio-atac-seq-enhancer-gene-linking
- Branch/worktree: fix/atac-enhancer-gene-linking, start 3186916 (Skill files untracked)
- Candidate tree hash: sha256-manifest-v1 `44385431f01902a0e18e305b483538009282bb44c5f19de4b53d5facd2b38976` (6 files, 35,507 bytes), verified live before and after execution
- Applicable audit: F:\OpenScience\audits\bio-atac-seq-enhancer-gene-linking\reaudit-run\ (report.json, viewer.md, source-identity.json). Prior initial audit identity 67cda9c3... (59, rejected).

## Completed this phase

- Decision candidate-ready: final 88, static 87, execution avg 89.2, Layer 1 36.5, Layer 2 52.75, assertions 31/33, no veto, no open P0. Schema validated (P0/P1/P2 only).
- EGL-001..012 retested independently; P0 usage example reproduces ABC's own tables exactly. See reaudit-run\viewer.md.
- combine_predictions.py, powerlaw, ATAC-only, MACS3 peaks, avg (substitute), v1.1.2, guards all run with output assertions.

## Required next actions

1. Orchestrator: commit the exact bytes to the optimized shelf (state ready), then intake. Records not yet published (uncommitted).
2. Optional non-blocking: EGL-013 P2 CR fix in run_abc.sh threshold lookup would change identity and need a fresh audit; only do it if desired.

## Open findings and blockers

| ID | Severity | State | Evidence | Required disposition |
|---|---|---|---|---|
| EGL-013 | P2 | open, non-blocking | reaudit-run\logs\check_powerlaw_v112.log | strip CR in awk threshold lookup (ABC v1.1.2 CRLF table) |
| B-1 | restricted | blocked, resource-infeasible | TOOLS.md | ENCODE average Hi-C ENCFF134PUN (58 GB) not fetched; avg on real data not counted executed; substitute chr22 K562 covers mechanics only |

## Environment and evidence

- Tool inventory: F:\OpenScience\audits\bio-atac-seq-enhancer-gene-linking\TOOLS.md (main 0d625a92..., re2g 3680ac7e..., create-command env 3f3bd2ef... reused)
- Run evidence: F:\OpenScience\audits\bio-atac-seq-enhancer-gene-linking\reaudit-run\ (scripts\, logs\, evidence\schema-validation.json, work\combine)
- Restricted-access items: B-1
- Tooling impact: none

## Worktree safety

- Run-owned changes: reaudit-run\ and this handoff only
- Pre-existing/user-owned changes: F:\optimizing-agent-science-skills\tools\run_mercury_worker.py, tools\test_run_mercury_worker.py (untouched)
- Records state: uncommitted, not published
- Product commits/pushes: none

## Transition assertion

- Next-phase prerequisites met: yes
