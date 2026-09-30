# Handoff: bio-atac-seq-atac-qc / fix-scientific-skill

- Updated: 2026-09-30T03:15:00-04:00
- Lane: 2
- Status: ready-for-phase
- Owner leaving: claude-sonnet-5-5 (initial audit phase)
- Next role: fix-scientific-skill

## Source identity

- Origin: GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:atac-seq/atac-qc
- Working tree: F:\OpenScience\wt\atac-atac-qc (skills\bio-atac-seq-atac-qc)
- Branch/worktree: fix/atac-atac-qc (starting commit 3186916406e9cc6b0e6dc24ffe47880951fc0f93)
- Candidate tree hash: sha256-manifest-v1 147fbda2ca5adf8924015bcb5564ce43b76eef574246c38d93409f4637bf995f (8 files; verified live before and after audit, bytes unchanged)
- Applicable audit: F:\OpenScience\audits\bio-atac-seq-atac-qc\audit-run\report.json (same identity; 71/100, Beta Only, not deployable; static 76, exec 67.0, assertions 21/34; skill and research veto PASS)

## Completed this phase

- Static review of all 8 files, 7 executed inputs on real ENCODE GM12878 chr1 slice plus planted-truth probes; report.json, viewer.md, findings.json, source-identity.json, execution-classifications.json written.
- Independent fragment-level NRF/PBC reference (scripts\frag_nrf.py) shows the shipped metric is not comparable to ENCODE thresholds.
- Known observations resolved: R script only on Windows-native R (confirmed); .bed.gz failure (confirmed, P3); TSS slowness (fixture artifact, not filed); c_curve -s 1e6 header-only (real when depth < step; filed with missing -P); no chrM in slice (mito surface static-only).
- Prior handoff claim that preseq -P fails is retracted: it needs a coordinate-sorted BAM.
- No audit-local repair made; Skill untouched.

## Required next actions

1. ATAC-QC-001 (P1): fragment-level NRF/PBC for paired-end in library_complexity.py; fix docs claims (dedup gives 1.0, definitions).
2. ATAC-QC-002, -004, -009: filters/options in library_complexity.py; TSS BED contract, strand column, used/skipped counts, nonzero exit on zero TSS; null for undefined PBC2.
3. ATAC-QC-003, -007, -008: align aggregate_qc.py and atac_qc_metrics.R with their documentation (or correct docs); narrowPeak format argument.
4. ATAC-QC-005, -006, -010: document bigWig recipe and pyTSSe claim, preseq -P and step, reconcile references and verify thresholds against current ENCODE pages.
5. Rerun affected cases with scripts in audit-run\scripts (frag_nrf.py, t_lc.py, t_tss.py, t_agg.sh, t_bw.sh, t_pre3.sh) and classify tooling impact for re-audit.

## Open findings and blockers

| ID | Severity | State | Evidence | Required disposition |
|---|---|---|---|---|
| ATAC-QC-001 | P1 | open | audit-run\out\run_all.log | fix + rerun real BAMs |
| ATAC-QC-002 | P2 | open | audit-run\out\run2.log | fix |
| ATAC-QC-003 | P2 | open | audit-run\out\run2.log | fix or correct docs |
| ATAC-QC-004 | P2 | open | audit-run\out\run2.log | fix |
| ATAC-QC-005 | P2 | open | audit-run\out\t_bw.log | document + validate |
| ATAC-QC-006 | P2 | open | audit-run\out\t_pre3.log | fix recipe |
| ATAC-QC-007 | P2 | open | findings.json | fix or rename |
| ATAC-QC-008 | P3 | open | audit-run\out\rbed | fix |
| ATAC-QC-009 | P3 | open | audit-run\out\run2.log | fix |
| ATAC-QC-010 | P3 | open | findings.json | reconcile refs |

Deferred/static-only surfaces: chrM fraction (slice lacks chrM), FRiP from fresh MACS peaks, fastqc/macs2 MultiQC modules, sex-chromosome snippets, spike-in and cell-cycle prose. No blockers.

## Environment and evidence

- Tool inventory: F:\OpenScience\audits\bio-atac-seq-atac-qc\TOOLS.md; env fingerprint sha256 e29e33c21ca3d6a660029311c4c9c7edbac105953734bd45b6a8f24799b009ac
- Run evidence: F:\OpenScience\audits\bio-atac-seq-atac-qc\audit-run\ (report.json, viewer.md, findings.json, source-identity.json, execution-classifications.json, scripts\, out\)
- Rubric: F:\optimizing-agent-science-skills\skill-auditor.zip extracted to audit-run\auditor
- Restricted-access items: none
- Tooling impact: none so far (R script still needs Windows-native R via audit-envs\atac-seq\r.sh; do not modify that env)

## Worktree safety

- Run-owned changes: F:\OpenScience\audits\bio-atac-seq-atac-qc\, this handoff
- Pre-existing/user-owned changes: tools\run_mercury_worker.py, tools\test_run_mercury_worker.py (untouched); candidate tree untracked in worktree from normalization
- Records state: not published (orchestrator publishes); publish with tools\publish_audits.py --run-dir audit-run
- Product commits/pushes: none

## Transition assertion

- Next-phase prerequisites met: yes
