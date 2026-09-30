# bio-atac-seq-atac-peak-calling fix pass - 2026-09-30

The two pseudoreplicates shared 50% of their reads, so the script failed good libraries (ratio 2.066; 1.09-1.16 with disjoint halves). The script now reports ENCODE-style Nt/N1/N2/Np ratios and passes the same GM12878 chr1 library, while a genuinely failing library still fails. The install recipe was corrected (IDR in its own environment) and verified in fresh environments; ROSE remains static-only.

- Final candidate audit: `audits/skills/bio-atac-seq-atac-peak-calling/candidate@b19054ded9df-reaudit-run`
- Result: **87/100, Production Ready**; no open P0.
- Candidate identity: `b19054ded9df6cf3d48b45b6f38c7b209454bb2627f95b5f7d73c794a02720c2`.

The provider binding record is the canonical proof that the committed shelf bytes match this independently audited candidate.
