# bio-atac-seq-enhancer-gene-linking fix pass - 2026-09-30

`run_abc.sh` crashed at `predict.py` on ABC v1.1.2 and main. It now runs end to end and reproduces ABC's own tables on real K562 Hi-C (1,674,535 rows, 1,353 links); `combine_predictions.py` is new and the install commands were corrected. The 58 GB average Hi-C was never fetched, so that branch is labelled mechanics-only.

- Final candidate audit: `audits/skills/bio-atac-seq-enhancer-gene-linking/candidate@44385431f019-reaudit-run`
- Result: **88/100, Production Ready**; no open P0.
- Candidate identity: `44385431f01902a0e18e305b483538009282bb44c5f19de4b53d5facd2b38976`.

The provider binding record is the canonical proof that the committed shelf bytes match this independently audited candidate.
