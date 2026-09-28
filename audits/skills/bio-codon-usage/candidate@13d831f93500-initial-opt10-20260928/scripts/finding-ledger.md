# Finding ledger — bio-codon-usage initial audit

Exact candidate: `sha256-manifest-v1:13d831f93500607c6f8cd7ce8b0ece7238af8400c80b750a3a6d95d2e5b4dc77`

| Order | ID | Severity | State | Evidence | Required disposition |
|---:|---|---|---|---|---|
| 1 | CODON-001 | P0 | open | `evidence/audit-results.json` table-2 probes | Make max-CAI optimization table-aware end to end or reject nonstandard DNA optimization; prove table-2 protein preservation. |
| 2 | CODON-002 | P0 | open | `evidence/audit-results.json` CAI semantics | Correct 1.85 stop, pseudocount, tie-warning, and zero-denominator claims; ship guarded regressions. |
| 3 | CODON-003 | P1 | open | `evidence/audit-results.json` boundary probes | Enforce a shared strict/permissive CDS validator and report every discard or rejection. |
| 4 | CODON-004 | P1 | open | `outputs/nc-heterogeneous.out`, `outputs/nc-public_thra.out` | Implement standard Nc or remove/rename the advertised Nc capability; retain exact estimator labels. |

No audit-local repair was attempted because each finding changes a scientific method, analytical contract, or validation boundary and therefore exceeds the minor-repair budget.
