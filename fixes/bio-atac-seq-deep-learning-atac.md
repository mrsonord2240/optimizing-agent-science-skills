# bio-atac-seq-deep-learning-atac fix pass - 2026-09-30

The documented log2FC formula was about 5x too small and the shipped script failed at once for lack of a `prep nonpeaks` step. The formula now matches an independent recomputation on 200 real SNPs, and the pipeline ran from a fresh directory to exit 0 with a working RESUME tail. Full-scale chromBPNet training, scBasset beyond TF 2.15 and Borzoi are labelled infeasible, not claimed.

- Final candidate audit: `audits/skills/bio-atac-seq-deep-learning-atac/candidate@3a9d1b4cab32-reaudit-run`
- Result: **88/100, Production Ready**; no open P0.
- Candidate identity: `3a9d1b4cab32a0a18917e8ee70b552a395e832da48a98902b90001a5190dea87`.

The provider binding record is the canonical proof that the committed shelf bytes match this independently audited candidate.
