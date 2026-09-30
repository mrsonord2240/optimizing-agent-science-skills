# Handoff: bio-atac-seq-atac-qc / orchestrator (publish, commit)

- Updated: 2026-09-30
- Lane: 2
- Status: candidate-ready
- Owner leaving: reaudit-scientific-skill worker (independent; did not fix or initially audit)
- Next role: orchestrator (commit to optimized shelf, publish records, intake)

## Source identity

- Origin: GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:atac-seq/atac-qc
- Working tree: F:\OpenScience\wt\atac-atac-qc\skills\bio-atac-seq-atac-qc (untracked, branch fix/atac-atac-qc from 3186916)
- Candidate identity: sha256-manifest-v1 cf524ad680cfbb3cdba3190cbd3f0a05d8e5e0fd4728e53edb12a6791645dd99 (8 files, 44,977 bytes), unchanged before/after
- Applicable audit: F:\OpenScience\audits\bio-atac-seq-atac-qc\reaudit-run\ (86/100 Production Ready)

## Completed this phase

- Retested all ATAC-QC-001..010 myself; all closed; no new findings.
- Real GM12878 slice + planted truth; fragment NRF/PBC equals independent counter; TSS 11.381 vs deepTools 11.391; R script, aggregate+MultiQC, CLI recipes, preseq -P run.
- Metrics: static 86, exec avg 85.3, L1 34.7, L2 50.6, assertions 33/35, no veto/P0.

## Required next actions

1. Orchestrator: commit exact bytes, publish reaudit-run (report.json, viewer.md, source-identity.json, scripts) with tools/publish_audits.py, run npm run audits:index, audits:check.
2. Optional P2 after-action (not blocking): render fragment-size PDF; TSS out-of-coverage slowness note; ship tiny fixtures.

## Open findings and blockers

| ID | Severity | State | Evidence | Required disposition |
|---|---|---|---|---|
| none | - | - | reaudit-run\findings.json | ATAC-QC-001..010 closed |

Not executed / gaps: fragment-size PDF not rendered; non-hg38 TxDb only via hg19 on synthetic reads; mt fraction only synthetic; lc_extrap run at -e 20M; MACS/FRiP-from-fresh-peaks static-only (execution-classifications.json).

## Environment and evidence

- Tool inventory: F:\OpenScience\audits\bio-atac-seq-atac-qc\TOOLS.md (env lock e29e33c2...09ac, unchanged)
- Run evidence: reaudit-run\out\ (t_lc, t_tss, t_agg, t_cli logs, R\, cli\), reaudit-run\scripts\
- Restricted-access items: none
- Tooling impact: none

## Worktree safety

- Run-owned changes: F:\OpenScience\audits\bio-atac-seq-atac-qc\reaudit-run\, this handoff
- Pre-existing/user-owned changes: F:\optimizing-agent-science-skills\tools\run_mercury_worker.py, tools\test_run_mercury_worker.py (untouched)
- Records state: uncommitted, unpublished
- Product commits/pushes: none

## Transition assertion

- Next-phase prerequisites met: yes
