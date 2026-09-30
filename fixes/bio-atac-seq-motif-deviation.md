# bio-atac-seq-motif-deviation fix pass - 2026-09-30

The bulk script failed as shipped (no depth input) and runs were not reproducible. It now takes `depth.tsv` and `set.seed`, giving byte-identical outputs on two runs; the removed `RunChromVAR` route calls chromVAR directly (identical on Signac 1.16.0 and 1.17.1). The ArchR NA z-score failure is guarded by dropping low-read cells; full-scale recurrence is unproven.

- Final candidate audit: `audits/skills/bio-atac-seq-motif-deviation/candidate@fb58807b04cb-reaudit-run`
- Result: **86/100, Production Ready**; no open P0.
- Candidate identity: `fb58807b04cb2e753dce4d199ef54c057c2d762635c526a0e7aef124e2a19c4e`.

The provider binding record is the canonical proof that the committed shelf bytes match this independently audited candidate.
