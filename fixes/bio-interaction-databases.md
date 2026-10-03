# bio-interaction-databases fix pass - 2026-10-03

`signor_for_gene` always returned an empty table; it now resolves the symbol to a UniProt accession and parses SIGNOR's headerless 29-column layout (TP53: 333 rows), and raises on an unparseable answer. The OmniPath `license=commercial` parameter is ignored by the server, so academic-only resources leaked through; the client now filters by each resource's licence purpose. The STRING example used a removed field, `escore > 0.4` was presented as the physical network, the aggregate score was invented, BioGRID errors leaked the access key in the request URL, and `aggregate_networks` unioned unequal scopes and admitted self-loops that pushed density above 1. Requests now have timeouts and STRING pacing. Self-interactions (homodimers) are excluded from the aggregate and documented as such.

- Final candidate audit: `audits/skills/bio-interaction-databases/candidate@f4d95b083e70-delta-reaudit-run`
- Result: **87/100, Production Ready**; no open P0.
- Candidate identity: `f4d95b083e70343c570554032b0592bc13d99f578274465d12367b91bf286c2d`.
- Open P2: IDM-013, `examples/interaction_query.py` keeps the last SIGNOR record per gene pair, so exported effect and mechanism can differ between runs.

The provider binding record is the canonical proof that the committed shelf bytes match this independently audited candidate.
