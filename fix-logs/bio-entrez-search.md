# bio-entrez-search — final-pass fix log (2026-09-24)

Source branch: `agent/finalpass-bio-entrez-search-20260924`  
Source commit: `5442c26cef8f0f9eeca84dd1eccfe00eb63d4d07`  
Source path: `database-access/entrez-search`

| Priority | Finding | Correction | Verification |
|---|---|---|---|
| P2 | The 340-line entrypoint kept database field tables and recovery detail inline. | Moved conditional query-design and failure-recovery detail to linked `references/query-design-and-failures.md`; entrypoint is now 289 lines. | Reference link and source syntax checked; all archived live scenarios re-run. |
| P2 | Query-length advice was prose-only. | Added `validate_term` to setup guidance and runnable `examples/validate_term.py`; it rejects empty, overlong, and OR-heavy inputs before an API call. | Local source-derived fresh test: 4/4 assertions. |
| P1 | Exact-node organism guidance inverted `:exp` and `:noexp`. | Documented `:noexp` for an exact node and retained `:exp` as explicit expansion. | Fresh live nucleotide regression: expanded 92,281,225 vs exact-node 113; 2/2 assertions. |
| P1 | Several operational claims were overstated. | Corrected ESearch `retmax=0` return value, unset-email behavior, EPost batching language, and indexing-lag guidance. | Live Biopython/NCBI checks and source-example compilation. |

Final audit: nine archived logical inputs plus two fresh inputs, **38/38 assertions passed**. The raw
report and viewer are source-pinned at the commit above with `auditor_independent: false` and the
required final-pass note. No publish, merge, push, promotion, or shared index/backlog change was made.
