# Independent re-audit findings

Candidate: `bio-clip-seq-ago-clip-mirna-targets`
Identity: `sha256-manifest-v1 e5366d51226e2ad2c96030cb26581bc84808194b7a17ef7bb376d337280d1b30` (10 files; 989-byte manifest)

| ID | Severity | Prior disposition | Independent result | Evidence |
|---|---|---|---|---|
| AGO-004 | P0 | Fixed | PASS. Two fresh workflows ran at the pinned Hyb commit; 111 accepted rows and 2/2 support per read matched. All structured outputs and non-stdout files were identical. The only stdout difference was its first timestamp line. | `evidence/hyb-repeatability.json`, `evidence/hyb-pinned-manifest-check.json`, `work/workflow-a`, `work/workflow-b` |
| AGO-005 | P1 | Fixed locally; upstream ambiguity retained | PASS. Protocol-declared 9-nt and 10-nt R2-prefix UMIs succeeded with provenance. Missing, invalid, blank, and too-long declarations failed without outputs. Upstream prose/default discrepancy remains disclosed. | `evidence/umi-contract-independent.json` |
| AGO-009 | P0 | Fixed | PASS. Finite acceptance, below-threshold exclusion, all tested Python NaN/infinity spellings (including sign and case variants), malformed/missing values, non-finite thresholds, and absence of result files after invalid cases were independently exercised. | `evidence/consensus-parser-independent.json`, `evidence/float-spellings-independent.json`, `evidence/shipped-tests.stderr` |

No open finding or new required recommendation remains for the audited candidate bytes. Deferred biological and remote surfaces remain documented in `evidence/deferred-limitations.md`.
