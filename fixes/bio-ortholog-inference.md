# bio-ortholog-inference fix pass - 2026-10-03

`orthodb_orthologs` parsed the wrong response structure and now reads the nested group and gene records null-safely. Every helper goes through one retrying client with timeouts, and the cross-resource example isolates each resource so one outage no longer aborts the run. Compara `confidence` claims were removed because the service returns no such key. OrthoDB `/search` is full text (TP53 returned TIGAR first), so the Skill now verifies the group contains the query gene. The OrthoDB `/tab` form, the PANTHER evidence-code claim, the Ensembl homology route and the eggNOG note were corrected. `batch_compara` now returns one row per input symbol with a status of found, no ortholog returned, or request failed, so a partial batch cannot read as complete.

- Final candidate audit: `audits/skills/bio-ortholog-inference/candidate@6e3122b03b95-reaudit-run-2`
- Result: **87/100, Production Ready**; no open P0.
- Candidate identity: `6e3122b03b95f6b9666a03f538ff5e07657ad733c2f0b9a2c7f1de1749993bbb`.
- Open P2: OI-11, `SKILL.md` does not name the three batch statuses and its snippet filters on `type`; OI-12, an unknown symbol is reported as request failed.
- Not executed: the eggNOG API refuses scripted access (403, TLS failure) and stays labelled unverified.

The provider binding record is the canonical proof that the committed shelf bytes match this independently audited candidate.
