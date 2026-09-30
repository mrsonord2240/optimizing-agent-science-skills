> **Audit record for `bio-atac-seq-single-cell-atac`**
> - Audited working candidate `da2da9c8bbafb674486ac581373867852f7b577f77626b19e63cc8dcecf55d08`; exact candidate provenance is in [source-identity.json](source-identity.json).
> - Derived from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/atac-seq/single-cell-atac), authored by [GPTomics](https://github.com/GPTomics) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-30 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test inputs and provenance are described in the published scripts/inputs and audit body; raw run outputs are not published. Local paths below refer to the auditor's workstation.

> **Audit record for `bio-atac-seq-single-cell-atac`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version derived from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/atac-seq/single-cell-atac) (MIT).
> - Audit method: skill-auditor@1.0 (AIPOCH, MIT), rubric zip sha256 `e54e9ff8...f0de`.
> - Performed 2026-09-30 by a Claude (Anthropic) audit agent. Initial diagnostic audit only; not a certification.
> - Data: 10x PBMC 5k scATAC (Cell Ranger ATAC 1.0.1) chr1:1-30Mb slice, 10x PBMC granulocyte-sorted 3k Multiome counts (full genome), whole-genome `singlecell.csv`; all inputs are real public data except a synthetic S.score covariate used only in the ScaleData probe (labelled). Paths refer to the auditor's workstation.

# Eval Viewer - bio-atac-seq-single-cell-atac

Candidate: `sha256-manifest-v1 da2da9c8bbafb674486ac581373867852f7b577f77626b19e63cc8dcecf55d08` (6 files), branch `fix/atac-single-cell-atac` @ 3186916, untracked and unedited.
Category: 3 - Data Analysis - Mode D - Complex, N = 8.
Environment: WSL `science`, micromamba `bio-atac-seq-single-cell-atac-r` (R 4.4.3, Signac 1.17.1, Seurat 5.5.1, ArchR 1.0.3, scDblFinder 1.23.4), `-py` (SnapATAC2 2.10.0, scvi-tools 1.5.1, macs3 3.0.4, torch 2.14 + RTX 5070 Ti) and `-amulet` (numpy 1.23.5, OpenJDK 17). Fingerprint recorded in `source-identity.json`.
Code: `scripts/run_audit.sh` (driver; `launch_all.sh` ran the ten steps in parallel), the R/Python step scripts, `singlecell_csv_qc.py`, `probe_static_claims.R`, `peakvi_feature_mismatch.py`, `snap_macs3_default.py`. Output: `out/`. `run_audit.sh` was extended with extra steps while the first launch was running; the first-launch step results are unaffected (a trailing shell parse error in those logs is harmless).

## Summary Table

| Input | Type | Executed | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|---|
| 1 | Canonical (signac_workflow.R as shipped) | yes, fails | 14 | 26 | 40 | 1/4 | error |
| 2 | Variant A (script, patched copy + QC/cell-cycle probes) | yes | 30 | 42 | 72 | 3/5 | warn |
| 3 | Variant A (Multiome WNN) | yes | 33 | 48 | 81 | 4/5 | pass |
| 4 | Variant B (SnapATAC2 block) | yes, 2 doc errors | 24 | 38 | 62 | 2/5 | partial |
| 5 | Variant B (ArchR block) | yes | 32 | 46 | 78 | 4/5 | pass |
| 6 | Variant B (Signac CallPeaks + scDblFinder) | yes | 32 | 46 | 78 | 4/4 | pass |
| 7 | Variant B (AMULET fragment route) | yes, pinned env | 27 | 36 | 63 | 1/4 | warn |
| 8 | Variant B (PEAKVI mapping) | yes | 32 | 45 | 77 | 3/4 | pass |

**Execution Average: 68.9 / 100** - **Assertion Pass Rate: 22/36 (61.1 %)**
**Static: 75/100** - **Final: 71**. The numeric score falls in the Beta Only band, but the Research Veto (code usability) fires on the primary shipped script, so the grade is forced to **Reject**, deployable: no. The veto rests on a single defect with a small fix (SCATAC-001); the rest of the ledger is independent of it.

Surface classifications: signac_workflow.R as shipped (**failed**), same script patched (executed, 2 edits), Multiome WNN (executed), SnapATAC2 (executed with 2 doc errors), ArchR (executed), Signac CallPeaks (executed), scDblFinder amulet() and ATAC mode (executed), AMULET fragment route (executed, numpy<1.24 env), AMULET BAM/jar route (**blocked**: no CB-tagged BAM staged; not exercised), PEAKVI query mapping (executed, bounded to 30 epochs), tabix indexing (executed, region count 100,839 = independent awk count), Cell Ranger ATAC / cellranger-arc and scATAC-pro/chromap (**blocked**, 10x registration; static-only), cell-cycle regression (executed probe, fails), sex-chromosome QC and chromVAR/AddMotifs prose (static-only; XIST coordinates verified), chromBPNet (not applicable).

## Input 1 - Canonical: signac_workflow.R as shipped

`Rscript scripts/signac_workflow.R filtered_peak_bc_matrix.h5 fragments.tsv.gz singlecell.csv` on the PBMC 5k slice stops after about 3 minutes: `Annotation genome does not match genome of the object` (SCATAC-001). Same result in the tooling run and in this audit. Nothing is written. The script is byte-identical to the upstream example.

**Scores:** 14 + 26 = **40**. Assertions 1/4.

## Input 2 - Variant A: patched script and Signac claim probes

Two-line patch (UCSC seqlevels, `genome(ann) <- 'hg38'`), TSS threshold relaxed from > 4 to > 1: 458 of 1472 cells kept (documented TSS > 4 keeps 13; the chr1 slice is about 3% of the genome, so the documented depth/TSS bars are unreachable here). Assays ATAC + ACT (2027 x 458), UMAP 458 x 2, one cluster (too shallow to split), TSS 1.0-6.4, nucleosome signal 0.36-1.99. LSI1-depth correlation +0.88 (Skill says about -1). QC violins and UMAP rendered and read; legible, the UMAP is a single blob. Real Cell Ranger metadata (5,335 called cells): 7.2% below 1000 fragments, median 10.7K. `ScaleData(vars.to.regress=)` fails on the ATAC assay and `RunSVD` reads the data layer (SCATAC-007).

**Scores:** 30 + 42 = **72**. Assertions 3/5.

## Input 3 - Variant A: Multiome WNN

Real 3k Multiome, 2,557 cells after QC, 12 WNN clusters, modality weights median RNA 0.475 / ATAC 0.525, ARI(wnn,RNA) 0.822, ARI(wnn,ATAC 2:30) 0.858, marker means fit T/monocyte/B/NK, LSI1-depth -0.96, UMAP-depth 0.098 (1:30) vs 0.045 (2:30). UMAP panel inspected. Snippet needs `magrittr` (SCATAC-006).

**Scores:** 33 + 48 = **81**. Assertions 4/5.

## Input 4 - Variant B: SnapATAC2

`import_fragments` ok (2,973 barcodes, 2.10.0 has no `import_data`). `obs['sample_id']='rep1'` fails (SCATAC-002); `tl.leiden` needs `pp.knn` (SCATAC-003). After fixes with a relaxed filter (documented 1000/4 keeps 0 on the slice): 697 cells, 6 clusters, macs3 ok with `n_jobs=1`, gene matrix 697 x 60,606. Default parallel macs3 in a plain script fails (SCATAC-011).

**Scores:** 24 + 38 = **62**. Assertions 2/5.

## Input 5 - Variant B: ArchR

Documented thresholds return no Arrow file on this slice (SCATAC-010); relaxed gives 403 cells, 402 after doublet filtering, 5 clusters (25/53/119/118/87) that overlap in the UMAP at this depth, 7,788 reproducible peaks (macs3 via `pathToMacs2`), PeakMatrix 7788 x 402, GeneScoreMatrix 24919 x 402. Exit 0, 37 min on a shared machine.

**Scores:** 32 + 46 = **78**. Assertions 4/5.

## Input 6 - Variant B: Signac CallPeaks and scDblFinder

CallPeaks per Signac cluster (847/558/67): 7,959 peaks, width median 150, chr1 only; 23.8% overlap the 10x peak list (lenient `-p 0.01`). scDblFinder ATAC mode 1369 singlet / 103 doublet (score-depth cor 0.81 on the shallow slice); `amulet()` 834 cells, 47 with q < 0.05.

**Scores:** 32 + 46 = **78**. Assertions 4/4.

## Input 7 - Variant B: AMULET

Fragment route: 5,335 cells, 426 merged regions, 55 multiplets (1.03%) in a numpy 1.23.5 env; `np.object` fails on numpy 2.5.3. No command or pin in the Skill (SCATAC-005). BAM/jar route not executed. Recall cannot be judged on a chr1 slice; median depth is far below the AMULET optimum (SCATAC-008).

**Scores:** 27 + 36 = **63**. Assertions 1/4.

## Input 8 - Variant B: PEAKVI reference mapping

`load_query_data` + 30-epoch training + latent on GPU: 368 x 6 finite; median query-reference distance 0.034 vs 0.033. This is a random split of one dataset, so it shows mechanics only. A first attempt died with a transient `CUDA_ERROR_UNKNOWN` while other jobs held the GPU; the rerun passed. Peak-count mismatch is rejected; same-count name mismatch only warns (SCATAC-012).

**Scores:** 32 + 45 = **77**. Assertions 3/4.

## Does the chr1 slice limit the conclusions?

Yes for calibration, no for the defects. The slice (about 3% of the genome, median about 650 valid fragments per cell) cannot meet the documented QC thresholds, so Signac, SnapATAC2 and ArchR ran relaxed, and their clustering, TSS-enrichment behaviour, doublet recall and per-cluster peak counts say little about the Skill's numeric claims. The whole-genome Cell Ranger metadata and the full-genome Multiome counts covered the QC-table and WNN claims. Every P0-P2 finding is an API, environment or documentation defect that does not depend on depth. Depth-dependent claims (QC bands, AMULET recall, S-phase effect, MACS3 read minimum) remain unverified and are marked as such.

## Static review highlights

- Frontmatter, trigger description, license, provenance, progressive disclosure and versions (all current) are sound.
- Contradictory QC rule sets (SCATAC-004) and a script that omits mito and doublet steps the workflow requires.
- AMULET ranked primary without depth condition; no invocation (SCATAC-005, SCATAC-008).
- Prose-only surfaces, static-only: sex-chromosome QC (XIST coordinates verified), chromVAR/AddMotifs, cellranger-arc metadata.

## Findings ledger (open)

| ID | Severity | Title |
|---|---|---|
| SCATAC-001 | P0 | signac_workflow.R fails: annotation genome mismatch |
| SCATAC-002 | P1 | SnapATAC2 block: obs['sample_id'] assignment raises |
| SCATAC-003 | P1 | SnapATAC2 block: leiden needs snap.pp.knn first |
| SCATAC-004 | P1 | QC thresholds conflict across SKILL.md, script and usage guide |
| SCATAC-005 | P2 | AMULET: no invocation, undocumented numpy<1.24 pin |
| SCATAC-006 | P2 | Multiome WNN snippet fails without magrittr |
| SCATAC-007 | P2 | Cell-cycle 'ScaleData regress S.score' fix cannot work |
| SCATAC-008 | P2 | 'AMULET primary' default conflicts with typical depth |
| SCATAC-009 | P3 | DepthCor '~ -1' comment is sign-dependent |
| SCATAC-010 | P3 | ArchR createArrowFiles returns nothing quietly |
| SCATAC-011 | P3 | snap.tl.macs3 default parallelism fails in a plain script |
| SCATAC-012 | P3 | PEAKVI mapping omits the peak-set alignment requirement |
| SCATAC-013 | P3 | Install guidance incomplete |
| SCATAC-014 | P3 | Uncited or unverified quantitative and biological claims |
| SCATAC-015 | P3 | singlecell.csv columns untested beyond Cell Ranger ATAC 1.0.1 |

## Limitations

chr1:1-30Mb slice of one PBMC sample, hg38 only; whole-genome scATAC fragments not run. Cell Ranger ATAC/ARC (10x registration) and the AMULET BAM route were not run. PEAKVI 200-epoch run and cross-study atlas transfer not run. AMULET depth thresholds checked against the paper text only. Diagnostic score only; not a certification.
