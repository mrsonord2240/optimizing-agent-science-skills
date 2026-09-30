# bio-atac-seq-co-accessibility fix pass - 2026-09-30

The CLI now accepts pattern-format `.mtx`, the enhancer column holds peak names instead of factor codes, `genome_df` is derived from the peaks so a chr1 run takes 8.5-14 minutes, and the wrong "Cicero 1.20+" claim is corrected. SCENIC+ stays static-only and LinkPeaks was not rerun after the doc changes. The whole-genome run is untested.

- Final candidate audit: `audits/skills/bio-atac-seq-co-accessibility/candidate@0aac567b1870-reaudit-run`
- Result: **85/100, Production Ready**; no open P0.
- Candidate identity: `0aac567b1870fb501220470d665c600af91f274cfa816e649bdcad81db8c8afa`.

The provider binding record is the canonical proof that the committed shelf bytes match this independently audited candidate.
