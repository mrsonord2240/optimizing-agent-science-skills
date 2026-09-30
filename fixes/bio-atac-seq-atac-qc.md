# bio-atac-seq-atac-qc fix pass - 2026-09-30

NRF/PBC were computed per read start instead of per fragment, so they were not comparable to ENCODE thresholds. They now count fragments (paired) with MAPQ and chrM filtering, MultiQC-parsable aggregation, strand-aware TSS scoring, corrected preseq and bamCoverage recipes, and a peak import that accepts `.bed.gz`. The fragment-size PDF was never rendered.

- Final candidate audit: `audits/skills/bio-atac-seq-atac-qc/candidate@cf524ad680cf-reaudit-run`
- Result: **86/100, Production Ready**; no open P0.
- Candidate identity: `cf524ad680cfbb3cdba3190cbd3f0a05d8e5e0fd4728e53edb12a6791645dd99`.

The provider binding record is the canonical proof that the committed shelf bytes match this independently audited candidate.
