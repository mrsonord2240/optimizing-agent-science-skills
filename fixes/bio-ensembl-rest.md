# bio-ensembl-rest fix pass - 2026-10-03

The quickstart requested a protein sequence with a gene ID, which returns 400; it now uses a protein ID and the client has a `multiple_sequences` option. The VEP example used HGVS `c.803G>A` with the wrong reference base, the usage guide gave a GRCh37 coordinate against the GRCh38 host, and the regulatory and homology routes in the endpoint table returned 404. The client now has a 30 s timeout, retries 429, 5xx and timeouts, rejects non-JSON bodies, and raises `EnsemblError`. The paralog section and stale confidence text in the Compara example were corrected.

- Final candidate audit: `audits/skills/bio-ensembl-rest/candidate@dabba949803e-reaudit-run`
- Result: **87/100, Production Ready**; no open P0.
- Candidate identity: `dabba949803e4c58bd3cc906389087520b3e5f5c32702fb6535c749131c0487b`.
- Open P2: `examples/compara_homology.py` was not reproduced by the re-auditor on the final bytes (five attempts failed on Ensembl 500, 503 and timeouts; the same calls passed as live probes and the fixer's run on identical files passed); the VEP example prints one line per transcript.

The provider binding record is the canonical proof that the committed shelf bytes match this independently audited candidate.
