# bio-atac-seq-footprinting fix pass - 2026-09-30

The CTCF validation was silently skipped, the scPrinter route and the bioconda install (TOBIAS 0.13.3) were wrong, and the RGT data line was a no-op. Each tool now has a verified per-tool environment recipe and the CTCF guard and scPrinter bulk route run on real chr1 data. With bias correction removed the script still exits 0 without a warning (open P2). Single-cell scPrinter and seq2PRINT training are untested.

- Final candidate audit: `audits/skills/bio-atac-seq-footprinting/candidate@a71e561087bc-reaudit-run`
- Result: **86/100, Production Ready**; no open P0.
- Candidate identity: `a71e561087bc769f5b14f703c8c535d1fda3a7f90de84d2a4b0dc7ccfb2ade87`.

The provider binding record is the canonical proof that the committed shelf bytes match this independently audited candidate.
