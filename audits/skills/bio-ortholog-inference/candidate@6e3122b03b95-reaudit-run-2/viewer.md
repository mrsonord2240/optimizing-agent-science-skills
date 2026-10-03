> **Audit record for `bio-ortholog-inference`**
> - Audited working candidate `6e3122b03b95f6b9666a03f538ff5e07657ad733c2f0b9a2c7f1de1749993bbb`; exact candidate provenance is in [source-identity.json](source-identity.json).
> - Derived from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/database-access/ortholog-inference), authored by [GPTomics](https://github.com/GPTomics) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-10-03 by Independent final re-auditor agent, lane 2 (not the fixer, tooler or prior auditor), commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test inputs and provenance are described in the published scripts/inputs and audit body; raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Re-audit: bio-ortholog-inference

Identity sha256-manifest-v1 6e3122b03b95f6b9666a03f538ff5e07657ad733c2f0b9a2c7f1de1749993bbb (7 files, 35,212 bytes), verified with `skill_preflight.py --offline` before and after. Independent of the fixer, the tooler and the prior auditor. Per-file hashes against the prior run: SKILL.md, usage-guide.md, scripts/ortholog_clients.py and examples/compara_orthologs.py changed; LICENSE, cross_resource.py and kegg_orthology.py identical.

**Score 87/100, Production Ready. Candidate-ready.** Static 86, execution average 87.8, Layer 1 average 35.4, Layer 2 average 52.4, assertions 25/25. No veto, no open P0.

| # | Input | Total |
|---|---|---|
| 1 | compara_orthologs.py (per-symbol outcome, partial-batch flag) | 88 |
| 2 | cross_resource.py (OMA and OrthoDB legs live; Compara leg isolated after a timeout) | 87 |
| 3 | kegg_orthology.py | 90 |
| 4 | Client retry/timeout guards, OrthoDB null parser, batch status schema (local stub) | 88 |
| 5 | Documented routes and claims (homology/id with species, OrthoDB, PANTHER, OMA, HomoloGene, unknown symbol) | 86 |

Fixed and verified: OI-09 (route now `/homology/id/<species>/<id>`; species form 200, bare form 404), OI-10 (stub shows found / request failed / no ortholog returned with a fixed column set; live example reports MDM2 request failed and BRCA1 no ortholog returned and flags PARTIAL BATCH), eggNOG note (states 403 and TLS failure). OI-01 to OI-08 did not regress.

Unknown-symbol question: `batch_compara(['TP53','NOTAGENE123'])` labels NOTAGENE123 `request failed` with the HTTP 400 text in `error`. The docstring says HTTP errors count as request failed, so the label is accurate to the code but can read as a transient outage. P2, not a blocker.

New findings, both P2: OI-11 (the three statuses are not described in SKILL.md and its batch snippet filters on `type`, which still drops failed symbols silently); OI-12 (unknown symbol labelled request failed; see above).

Not executed: eggNOG API (eggnogdb.org/api 403, eggnog6.embl.de TLS failure; not re-probed this pass, carried from the prior run). PANTHER is liveness only (no client function). Ensembl homology was slow and intermittent (45 s read timeouts on MDM2, one Compara leg of cross_resource); reported as service-side.

Evidence: scripts/evidence/.
