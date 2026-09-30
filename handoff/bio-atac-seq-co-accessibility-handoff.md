# Handoff: bio-atac-seq-co-accessibility / orchestrator (commit + intake)

- Updated: 2026-09-30T04:50:00-07:00
- Lane: 3
- Status: candidate-ready
- Owner leaving: reaudit-scientific-skill worker (independent; did not fix or initially audit)
- Next role: optimize-scientific-skills orchestrator (commit exact bytes, then Marketplace intake)

## Source identity

- Origin: GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:atac-seq/co-accessibility
- Working tree: F:\OpenScience\wt\atac-co-accessibility\skills\bio-atac-seq-co-accessibility
- Branch/worktree: fix/atac-co-accessibility, start 3186916 (staged/modified, uncommitted)
- Candidate tree hash: sha256-manifest-v1 `0aac567b1870fb501220470d665c600af91f274cfa816e649bdcad81db8c8afa` (5 files, 37512 bytes); recomputed live before and after re-audit, unchanged
- Applicable audit: F:\OpenScience\audits\bio-atac-seq-co-accessibility\reaudit-run\ (this identity); prior 3c8089b0... at ..\report.json (63/100)

## Completed this phase

- Independent re-audit: score 85 (84.6 unrounded), Production Ready under schema rounding; static 82, execution avg 86.3, L1 34.7, L2 51.6, assertions 31/32, no veto, no open P0/P1. Margin over the 85 gate is thin.
- Every claimed fix (COACC-001..013) re-verified on my own runs: pattern .mtx CLI, enhancer names vs independent BED recomputation, unordered pairs, window=1e6, guards, SimpleList, arc plot, tss_bed=NULL, seed byte-identity.
- Canonical smokes: 3-chromosome real PBMC Multiome slice (5.2 min) and 30 Mb PBMC 5k slice (5.2 min, 6,035 strong / 2,027 enhancer-gene); planted-truth synthetic recovery exact; Hi-C snippet vs planted BEDPE; ArchR verbatim.
- SCENIC+ verified not claimed as executed (SKILL.md and method-reference.md label static review only).
- Nothing published, committed, or pushed.

## Required next actions

1. Orchestrator: publish the record with `publish_audits.py --run-dir F:\OpenScience\audits\bio-atac-seq-co-accessibility\reaudit-run --artifact scripts/<each>` (records repo; I did not publish), run `npm run audits:index` and `audits:check`.
2. Commit exact candidate bytes on the optimized shelf, then intake. Optional first: a tiny fixer pass for COACC-014/015 would change the identity and require a new re-audit; not required.

## Open findings and blockers

| ID | Severity | State | Evidence | Required disposition |
|---|---|---|---|---|
| COACC-012 | P3 | deferred | ..\TOOLS.md; SKILL.md Status column | SCENIC+ restricted static-only; rerun needs Python <=3.11 env, pybedtools, cisTarget DBs |
| COACC-014 | P2 | open (non-blocking) | reaudit-run\logs\fn_zero.log | Zero-read cell halts with cryptic 'attempt to set an attribute on NULL'; add colSums guard |
| COACC-015 | P3 | open (non-blocking) | usage-guide.md line 30 | Prompt says tssRegion=c(-2000, 500); script uses TSS +/- 2 kb |

Failed or blocked surfaces: zero-read cell (failed, loud); whole-genome run (blocked, resource-infeasible; only chr1 30 Mb and 3 chromosomes run); SCENIC+ (static-only restricted). LinkPeaks and alpha/permutation evidence reused (script unchanged, env fingerprint identical; LinkPeaks not rerun after doc-only edits).

## Environment and evidence

- Tool inventory: F:\OpenScience\audits\bio-atac-seq-co-accessibility\TOOLS.md; live conda-list sha256 `2fcd3fc2...` equal; cicero 1.3.9, monocle3 1.3.1, ArchR 1.0.3, R 4.4.3
- Run evidence: reaudit-run\{report.json,findings.json,viewer.md,source-identity.json,execution-classifications.json,logs\,scripts\,evidence\}; heavy work F:\OpenScience\audit-envs\bio-atac-seq-co-accessibility\work\reaudit
- report.json validated by reaudit-run\scripts\validate_report.py (VALID; P2 only recommendations)
- Restricted-access items: COACC-012 (SCENIC+)
- Tooling impact: none

## Worktree safety

- Run-owned changes: reaudit-run\ under the audits dir, audit-envs work\reaudit, this handoff
- Pre-existing/user-owned changes: F:\optimizing-agent-science-skills\tools\run_mercury_worker.py, tools\test_run_mercury_worker.py (untouched)
- Records state: uncommitted, unpublished
- Product commits/pushes: none

## Transition assertion

- Next-phase prerequisites met: yes
