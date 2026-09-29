# Finding ledger — bio-codon-usage final re-audit

Exact candidate: `sha256-manifest-v1:3186a1debc804852b3ea016b9aeabebc4436a04791b84b13dba8669878d7e4dd`

| ID | Initial severity | Final state | Independent final evidence |
|---|---|---|---|
| CODON-001 | P0 | Closed | All four table-2 TGA/TGG x AGA/AGG cases preserve `MW*`; table mismatch is rejected. |
| CODON-002 | P0 | Closed | Exact 1.85 stop, pseudocount, tie, and zero-denominator semantics pass; the guard reports exclusions before calling the live implementation. |
| CODON-003 | P1 | Closed | Strict rejection and permissive exact-discard reporting pass, and counts/frequencies/RSCU share identical validation state. |
| CODON-004 | P1 | Closed | The false helper and trigger claim are absent; standard Nc is an explicit external-tool boundary and fresh codonW controls remain reproducible. |

No new P0, P1, or P2 finding was identified. No audit-local repair was attempted.
