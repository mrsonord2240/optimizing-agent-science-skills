# Handoff: bio-atac-seq-single-cell-atac / fix-scientific-skill

- Updated: 2026-09-30 (PDT)
- Lane: 2
- Status: ready-for-phase
- Owner leaving: audit-scientific-skill worker (initial audit)
- Next role: fix-scientific-skill

## Source identity

- Origin: GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:atac-seq/single-cell-atac (subtree ef5b1305663382e0228349bd42d9768afc19dcb8)
- Working tree: `F:\OpenScience\wt\atac-single-cell-atac`; candidate `skills\bio-atac-seq-single-cell-atac` (untracked, unedited)
- Branch/worktree: fix/atac-single-cell-atac, starting commit 3186916
- Candidate tree hash: `sha256-manifest-v1 da2da9c8bbafb674486ac581373867852f7b577f77626b19e63cc8dcecf55d08` (6 files; re-verified after execution; no __pycache__)
- Applicable audit: `F:\OpenScience\audits\bio-atac-seq-single-cell-atac\initial-audit-20260930\report.json` (sha256 `b46e78b6...56a4`), same identity. Static 75, execution avg 68.9, assertions 22/36, final 71; Research Veto code_usability FAIL (SCATAC-001) so grade Reject. Not published to records.

## Completed this phase

- Verified identity live; ran 8 inputs on real PBMC data (signac as-shipped, patched, WNN, SnapATAC2, ArchR, CallPeaks+scDblFinder, AMULET, PEAKVI) plus QC-claim and cell-cycle probes.
- Wrote report.json (schema-validated, P0/P1/P2 only), viewer.md, findings.json, source-identity.json, scripts/ in the run dir.
- Tooling defects T1-T6 and N1/N3/N4 confirmed or folded into SCATAC ids below.

## Required next actions

1. SCATAC-001: fix `scripts/signac_workflow.R` annotation (UCSC seqlevels + `genome(ann) <- 'hg38'`), rerun end to end.
2. SCATAC-002/003/011: fix SnapATAC2 block (list assignment or drop, `snap.pp.knn` before leiden, macs3 `n_jobs=1`/main guard); rerun.
3. SCATAC-004: one canonical QC rule set; align SKILL.md, script (implement or exclude mito/doublet rows), usage-guide.
4. SCATAC-005/008: AMULET command + numpy<1.24 env; depth-conditional tool choice.
5. SCATAC-006/007: magrittr in WNN block; replace ScaleData cell-cycle fix.
6. SCATAC-009 to 015: P3 wording, guards, prerequisites, citations.

## Open findings and blockers

| ID | Severity | State | Evidence | Required disposition |
|---|---|---|---|---|
| SCATAC-001 | P0 | open | out/signac_asis.log | Fix annotation genome; rerun script |
| SCATAC-002 | P1 | open | out/snap.log | obs['sample_id'] assignment |
| SCATAC-003 | P1 | open | out/snap.log | add snap.pp.knn |
| SCATAC-004 | P1 | open | out/qccsv.log | reconcile QC thresholds |
| SCATAC-005 | P2 | open | out/amulet*.log | AMULET command and numpy pin |
| SCATAC-006 | P2 | open | out/probe.log | magrittr for WNN |
| SCATAC-007 | P2 | open | out/probe.log | cell-cycle regression method |
| SCATAC-008 | P2 | open | out/qccsv.log | depth-conditional doublet default |
| SCATAC-009 | P3 | open | out/signac_depth_cor.png | DepthCor sign wording |
| SCATAC-010 | P3 | open | out/archr.log | ArrowFiles guard |
| SCATAC-011 | P3 | open | out/snap_macs3_*.log | macs3 n_jobs/main guard |
| SCATAC-012 | P3 | open | out/peakvi_mm.log | peak-set alignment note |
| SCATAC-013 | P3 | open | out/probe.log | prerequisites |
| SCATAC-014 | P3 | open | out/probe.log | cite or soften claims |
| SCATAC-015 | P3 | blocked | TOOLS.md | cellranger-arc columns (10x registration) |
| B1 | blocker | restricted | TOOLS.md | Cell Ranger ATAC/ARC; AMULET BAM/jar route not executed (no CB-tagged BAM) |

Chr1 slice cannot meet documented QC thresholds (runs used relaxed thresholds); this limits QC-band, doublet-recall and clustering-biology conclusions but not the defects above (see viewer.md).

## Environment and evidence

- Tool inventory: `F:\OpenScience\audits\bio-atac-seq-single-cell-atac\TOOLS.md` (sha256 `a3c94d91...f986`); env fingerprint in source-identity.json (`environment_fingerprint_sha256`)
- Run evidence: `F:\OpenScience\audits\bio-atac-seq-single-cell-atac\initial-audit-20260930\{scripts,out}`; work dir `F:\OpenScience\audit-envs\bio-atac-seq-single-cell-atac\audit-initial-20260930`
- Restricted-access items: B1, SCATAC-015
- Tooling impact: none for these fixes; SCATAC-005 fix needs the `-amulet` env; a cellranger-arc metadata check would need 10x registration

## Worktree safety

- Run-owned changes: `F:\OpenScience\audits\bio-atac-seq-single-cell-atac\initial-audit-20260930\**`, `F:\OpenScience\audit-envs\bio-atac-seq-single-cell-atac\audit-initial-20260930\**`, this handoff
- Pre-existing/user-owned changes: `F:\optimizing-agent-science-skills\tools\run_mercury_worker.py`, `tools\test_run_mercury_worker.py`; other lanes' handoffs untouched
- Records state: uncommitted, not published (orchestrator publishes)
- Product commits/pushes: none

## Transition assertion

- Next-phase prerequisites met: yes
