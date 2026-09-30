# bio-atac-seq-single-cell-atac fix pass - 2026-09-30

The shipped `signac_workflow.R` failed on its documented input. It now runs on its three documented arguments and stops clearly if metadata columns are missing; the SnapATAC2 2.10.0 doc errors and the AMULET numpy note are corrected. Cell Ranger ATAC/ARC and the AMULET BAM route were not executed, and the chr1 slice needed relaxed QC thresholds.

- Final candidate audit: `audits/skills/bio-atac-seq-single-cell-atac/candidate@4ced0da507d6-reaudit-run`
- Result: **86/100, Production Ready**; no open P0.
- Candidate identity: `4ced0da507d684d209beb4676ce6d206fc6d1730ff2e45d8ff965c3e2d78f286`.

The provider binding record is the canonical proof that the committed shelf bytes match this independently audited candidate.
