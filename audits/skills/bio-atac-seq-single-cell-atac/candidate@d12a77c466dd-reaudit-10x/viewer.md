> **Audit record for `bio-atac-seq-single-cell-atac`**
> - Audited working candidate `d12a77c466ddc748e86d80ac482766aa212e3b31aa1d6bd3388a827bf59dbec0`; exact candidate provenance is in [source-identity.json](source-identity.json).
> - Derived from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/atac-seq/single-cell-atac), authored by [GPTomics](https://github.com/GPTomics) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-30 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test inputs and provenance are described in the published scripts/inputs and audit body; raw run outputs are not published. Local paths below refer to the auditor's workstation.

> **Audit record for `bio-atac-seq-single-cell-atac`**
> - Audited working candidate `d12a77c466ddc748e86d80ac482766aa212e3b31aa1d6bd3388a827bf59dbec0`; provenance in [source-identity.json](source-identity.json).
> - Derived from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/atac-seq/single-cell-atac), authored by [GPTomics](https://github.com/GPTomics) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-30 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Raw run outputs are not published; local paths refer to the auditor's workstation.

# Final re-audit: bio-atac-seq-single-cell-atac (10x ARC / AMULET update)

- Phase: final re-audit, independent (did not write, fix, tool or earlier audit this Skill). Candidate identity verified live before and after execution: sha256-manifest-v1 `d12a77c4...bf59dbec0`, 6 files, 38,010 bytes, no `__pycache__`.
- Decision: **candidate-ready**. Final 88 (static 90, execution average 87.1, Layer 1 34.9, Layer 2 52.3), assertions 30/31, no veto, no open P0/P1. Supersedes `4ced0da5...` (86).
- Cell Ranger itself was not run; the Skill says so (SKILL.md version paragraph) and claims only that outputs were read from public 10x datasets.

## Retested changed surfaces

| Surface | Input | Result |
|---|---|---|
| `signac_workflow.R` ARC branch | ARC 2.0.0 PBMC 3k per_barcode_metrics.csv + h5 + whole-genome fragments | exit 0, 14 min; 2392/2687 cells, 8 clusters, LSI1-depth r -0.96, all kept cells is_cell=1, ACT 19607x2392; UMAP and QC figures inspected |
| same, ATAC 2.1.0 | 10k PBMC v2 singlecell.csv + chr1 fragments | defaults 7008/10246 (12 clusters); relaxed `1 1000` 9884 (16 clusters) |
| same, ATAC 1.0.1 | PBMC 5k chr1 | defaults 40/1472; relaxed 788/1472 (identical to prior baseline) |
| AMULET BAM, ARC flags | chr1 CB-tagged BAM slice | exit 0; 2711 cells, 21 multiplets |
| AMULET fragments, ARC derived csv | whole-genome ARC fragments | exit 0; 2711 cells, 66 multiplets |
| AMULET fragments, ATAC 2.1.0 | chr1 fragments | exit 0; 10246 cells, 146 multiplets |
| AMULET misuse | ARC BAM with ATAC default indices; raw ARC csv on fragment route | both exit 1 with errors, no silent success |

Regressions rerun against live bytes: Multiome WNN (2557 cells, weights 0.475/0.525), cell-cycle LSI regression (0.264 to 0), SnapATAC2 2.10.0 block (697 cells, 6 clusters), ArchR empty-ArrowFiles guard, PEAKVI alignment (0.099 unaligned vs 0.034 aligned). Static: links resolve, audit narration absent from shipped text, frontmatter valid.

## Are the ARC approximations honest and adequate?

- Mito fraction: adequate. ARC `atac_mitochondrial_reads / atac_raw_reads` matches the 10x ATAC `mitochondrial / total` definition; observed 0-0.0499.
- Blacklist ratio: disclosed as a substitution, but not adequate as a filter. It is peak-level (57 of 128,741 ARC peaks overlap the list) and peaked at 0.004, so the 0.05 cut never removes a cell; the official ATAC 1.0.1 column reaches 0.18 and ATAC 2.1.0's column is all zero. See finding RA-1.

## Findings

| ID | Sev | State | Note |
|---|---|---|---|
| RA-1 | P2 | open, non-blocking | State that ARC/ATAC 2.x blacklist QC is effectively inert (one sentence in SKILL.md) |

Non-blocking observations: `FractionCountsInRegion` is soft-deprecated in Signac 1.17 (still works, silent); the `tooling-10x` data README wrongly says ARC fragments use `atac_barcode` (measured: `barcode`).

Evidence: `reaudit-10x/logs/`, `reaudit-10x/scripts/`; environments `bio-atac-seq-single-cell-atac-{r,py,amulet}` (TOOLS.md rows 15-16).
