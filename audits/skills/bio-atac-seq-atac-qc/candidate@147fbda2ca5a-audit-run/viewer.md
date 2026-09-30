> **Audit record for `bio-atac-seq-atac-qc`**
> - Audited working candidate `147fbda2ca5adf8924015bcb5564ce43b76eef574246c38d93409f4637bf995f`; exact candidate provenance is in [source-identity.json](source-identity.json).
> - Derived from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/atac-seq/atac-qc), authored by [GPTomics](https://github.com/GPTomics) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-30 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test inputs and provenance are described in the published scripts/inputs and audit body; raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Audit viewer: bio-atac-seq-atac-qc (initial audit, 2026-09-30)

Candidate `sha256-manifest-v1 147fbda2ca5adf8924015bcb5564ce43b76eef574246c38d93409f4637bf995f` (8 files), origin `GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:atac-seq/atac-qc`. Diagnostic score only; not a readiness claim.

**Result: 71 / 100, Beta Only, not deployable.** Static 76 (x0.4 = 30.4), execution average 67.0 (x0.6 = 40.2), assertions 21/34. Skill veto PASS, research veto PASS. Category Data Analysis, mode B, 7 inputs.

## Inputs

| # | Type | Input | Status | Total |
|---|---|---|---|---|
| 1 | Canonical | ENCODE-style TSS enrichment, real GM12878 chr1 slice | COMPLETED | 78 |
| 2 | Canonical | NRF/PBC on real unfiltered and filtered BAMs | COMPLETED | 56 |
| 3 | Variant A | ATACseqQC R script with IDR peaks | COMPLETED | 75 |
| 4 | Variant B | aggregate_qc.py and MultiQC hand-off | COMPLETED | 63 |
| 5 | Variant B | deepTools/Picard/samtools/MultiQC recipes | COMPLETED | 84 |
| 6 | Variant B | preseq on paired-end ATAC BAM | PARTIAL | 61 |
| 7 | Edge | planted-truth silent-failure probes | COMPLETED | 52 |

## Findings (ordered ledger)

| ID | Severity | Summary |
|---|---|---|
| ATAC-QC-001 | P1 | library_complexity.py computes single-end read-start NRF/PBC; unfiltered rep1 NRF 0.353 vs fragment-level 0.619 (0.779 at MAPQ>=30); deduplicated BAM 0.573 vs 1.000 |
| ATAC-QC-002 | P2 | MAPQ>=30, chrM exclusion documented but not applied (planted: NRF 0.34 vs 1.0) |
| ATAC-QC-003 | P2 | aggregate_qc.py is long-format, not per-sample/MultiQC; MultiQC reads metrics as samples; missing metrics skipped; string values crash |
| ATAC-QC-004 | P2 | encode_tss_enrichment.py: minus-strand gene interval scores 1.0 vs 21.0; absent chromosome or empty BED returns 0.0, exit 0 |
| ATAC-QC-005 | P2 | bigWig recipe undocumented; same data scores 11.3 to 16.0 by recipe; pyTSSe equivalence unvalidated |
| ATAC-QC-006 | P2 | preseq recipe omits -P for paired-end; c_curve -s 1e6 header-only below 1M fragments |
| ATAC-QC-007 | P2 | R script does not classify periodicity; nuclear_reads_M includes chrM and duplicates |
| ATAC-QC-008 | P3 (report: P2) | R script .bed.gz narrowPeak fails cryptically; hg38 hard-coded |
| ATAC-QC-009 | P3 (report: P2) | PBC2 emitted as non-standard JSON Infinity |
| ATAC-QC-010 | P3 (report: P2) | Pearson vs Spearman contradiction; unverified Landt 2012 attribution; missing Picard command and preseq prerequisite |

Report recommendations carry P3 findings as P2 (schema allows P0-P2 only); findings.json keeps ledger P3. Full text with root cause and fix: `findings.json`. Report: `report.json`.

## Execution classification

Executed: all four scripts, samtools/Picard/deepTools/MultiQC recipes, preseq. Static-only: chrM fraction (slice has no chrM), FRiP from freshly called MACS peaks, fastqc/macs2 MultiQC modules, sex-chromosome snippets, spike-in and cell-cycle prose. See `execution-classifications.json`.

## Observations not filed as findings

- TSS script took 52 s for 300 TSS outside the sparse slice bigWig vs 2.3 s in-slice; this is a property of the sliced fixture, not shown to affect dense whole-genome bigWigs.
- The shipped R PDF is valid (%PDF-1.4, 1 page) but no PDF rasterizer exists here; a same-call PNG re-plot was inspected (NFR peak near 50 bp, mono near 200 bp, di near 400 bp, legible).
- Real-slice TSS enrichment 11.38 matched deepTools 11.39; ATACseqQC 23.54 is 2.07x, consistent with the Skill claim.
- Earlier tooling note that name-sorted -P failure was a Skill defect is retracted: preseq -P needs coordinate-sorted input.

## Reproduction

Scripts in `scripts/`, outputs in `out/`, environment per `TOOLS.md` (WSL env bio-atac-seq-atac-qc, Windows-native R for the R script). Independent reference: `scripts/frag_nrf.py`.
