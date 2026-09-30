> **Audit record for `bio-atac-seq-co-accessibility`**
> - Audited working candidate `3c8089b0496fa6375512ece4b85ce85c10c47f3cb4a9c8e48c7288a62b9162e3`; exact candidate provenance is in [source-identity.json](source-identity.json).
> - Derived from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/atac-seq/co-accessibility), authored by [GPTomics](https://github.com/GPTomics) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-30 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test inputs and provenance are described in the published scripts/inputs and audit body; raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Audit viewer: bio-atac-seq-co-accessibility (initial audit, 2026-09-30)

Candidate `sha256-manifest-v1 3c8089b0496fa6375512ece4b85ce85c10c47f3cb4a9c8e48c7288a62b9162e3` (5 files), origin `GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:atac-seq/co-accessibility`. Diagnostic score only; not a readiness claim.

**Result: 63 / 100, Beta Only, not deployable.** Static 68 (x0.4 = 27.2), execution average 60.3 (x0.6 = 36.2), assertions 14/24. Skill veto PASS, research veto PASS. Category Data Analysis, mode D, 7 inputs.

## Inputs

| # | Type | Input | Status | Total |
|---|---|---|---|---|
| 1 | Canonical | Shipped Cicero function on real PBMC 5k chr1 slice (genome_df limited to chr1) | COMPLETED | 63 |
| 2 | Variant A | ArchR addCoAccessibility/getCoAccessibility as documented | COMPLETED | 78 |
| 3 | Variant B | Signac LinkPeaks on public 3k PBMC Multiome (tooling-phase run, log inspected) | COMPLETED | 64 |
| 4 | Edge | Documented CLI on a binarized peak matrix exported with writeMM | ERROR | 34 |
| 5 | Stress | Shipped function unmodified on the same 1,726-peak chr1 input | PARTIAL | 35 |
| 6 | Scope Boundary | Downstream snippets: Visualizing Connections and Hi-C concordance on real Cicero output | COMPLETED | 64 |
| 7 | Adversarial | Alpha block and permutation negative control (documented null) | COMPLETED | 84 |

## Findings (ordered ledger)

| ID | Severity | Summary |
|---|---|---|
| COACC-001 | P1 | Documented CLI fails on the natural binary peak matrix: readMM of a pattern-format .mtx returns ngTMatrix and new_cell_data_set stops |
| COACC-002 | P1 | enhancer column of the enhancer-gene CSV is 50 percent factor integer codes, and the table over-counts pairs (4,728 rows vs 3,083 correct unique triples) |
| COACC-003 | P2 | genome_df is hard-coded to all hg38 primary chromosomes; as shipped the function did not finish in 25 min on a 1,726-peak chr1-only input (8.5 min when restricted to chr1) |
| COACC-004 | P2 | 'Cicero 1.20+' is wrong for the monocle3 API the code uses; the Bioconductor cicero (1.30.0 on Bioc 3.23) depends on monocle 2 |
| COACC-005 | P2 | Cicero output holds every peak pair in both orientations, so reported 'Total/Strong connections', arcs, and per-row concordance are double-counted |
| COACC-006 | P2 | 'genomic_distance_max' (default 500 kb) is not an argument of run_cicero or generate_cicero_models; the real controls are window and distance_constraint |
| COACC-007 | P2 | Connection scores are described as 0-1, but observed scores span -0.88 to 0.93 and 34.7 percent of non-NA rows are negative (660 NA rows) |
| COACC-008 | P2 | The documented plotTracks(track) call errors as written and the full strong set draws an unreadable hairball |
| COACC-009 | P2 | Enhancer-gene mapping depends on an unshipped TSS BED, silently skips otherwise, labels promoter peaks as enhancers, and the peak-name contract is undocumented |
| COACC-010 | P3 | ArchR getCoAccessibility(returnLoops=TRUE) returns a SimpleList (loops in element 1), not a GRanges as the text says |
| COACC-011 | P3 | Hi-C concordance ('~30-50%'), '10-50% of peaks have a strong connection', and '> 50K cells slow' are stated without a source or executed support |
| COACC-012 | P3 | SCENIC+ '1.0+/1.0' is an alpha (v1.0a2, Python <=3.11.8), and 'use the published Docker image' is not evidenced in the repository README |
| COACC-013 | P3 | Description advertises Hi-C comparison, Multiome LinkPeaks, SCENIC+ and reference databases, but only the Cicero function ships as code |

Report recommendations carry P3 findings under P2 (schema allows P0-P2 only); findings.json keeps ledger severities. Full text with evidence and fix: `findings.json`. Report: `report.json`.

## Execution classification

Executed: shipped function (chr1-only genome), alpha block and permutation control, visualization, Hi-C snippet, ArchR, LinkPeaks (tooling-phase run, log inspected). Failed: CLI on pattern .mtx; shipped function unmodified (25 min timeout, bounded). Blocked: SCENIC+ (pybedtools build; static review only). Static-only: reference databases, HiChIP/ABC/CRISPRi prose. See `execution-classifications.json`.

## Observations not filed as findings

- Two unseeded runs of the shipped function on the same machine were identical (99,284 rows, Pearson 1.0000, strong-set Jaccard 1.0000), so no determinism finding is filed; the Skill's 'set seed' advice is unnecessary here but the script does not set one.
- The permutation control is clean (36 residual strong pairs of 11,794 real).
- Integer-format .mtx loads through new_cell_data_set; the CLI failure is specific to logical/pattern input.
- The CLI when fed an integer matrix was not run end to end because the unmodified genome default exceeds the time budget.
- Real chr1 slice: strong pairs are proximal (71 percent < 250 kb) with distance-decay mean scores.

## Reproduction

Scripts and logs in `runs/`, tooling evidence in `evidence/`, environment per `TOOLS.md` (WSL env `bio-atac-seq-co-accessibility`, R 4.4.3, cicero 1.3.9 GitHub monocle3 branch, monocle3 1.3.1, ArchR 1.0.3, Signac 1.17.1).
