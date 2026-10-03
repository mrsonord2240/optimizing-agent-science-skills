> **Audit record for `bio-ortholog-inference`**
> - Audited working candidate `aa32b51586699da5ed4708ce63e6cbc9eb19751ed79f94b5ff5d73208e252495`; exact candidate provenance is in [source-identity.json](source-identity.json).
> - Derived from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/database-access/ortholog-inference), authored by [GPTomics](https://github.com/GPTomics) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-10-03 by Independent re-auditor agent (not the fixer), commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test inputs and provenance are described in the published scripts/inputs and audit body; raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Re-audit: bio-ortholog-inference

Identity sha256-manifest-v1 aa32b51586699da5ed4708ce63e6cbc9eb19751ed79f94b5ff5d73208e252495 (7 files, 34,073 bytes), verified with `skill_preflight.py --offline` before and after. Independent of the fixer and the initial auditor.

**Score 84/100, Limited Release. Not candidate-ready** (final score below the 85 gate). Static 82, execution average 85.4, Layer 1 average 34.6, Layer 2 average 50.8, assertions 23/25 (92%). No veto, no open P0.

| # | Input | Total |
|---|---|---|
| 1 | compara_orthologs.py on the final bytes (exit 0, first attempt) | 81 |
| 2 | cross_resource.py (Compara, OMA 1:1, OrthoDB verified group) | 87 |
| 3 | kegg_orthology.py | 90 |
| 4 | Client retry/timeout guards (local stub) and OrthoDB null parser | 88 |
| 5 | Documented routes and claims (OrthoDB, PANTHER, OMA, HomoloGene, Compara homology/id) | 81 |

Findings OI-01 to OI-08: all reproduced as fixed. B1 (OMA flakiness): OMA answered 200 on every call this pass (TP53 1:1, BRCA1 empty, HOG, example); not reproduced. B2 (eggNOG): still refuses scripts (eggnogdb.org/api 403, eggnog6.embl.de TLS failure); not executed.

New findings, all P2:
- OI-09: SKILL.md lists `/homology/id/<ensembl_gene_id>`; it returns 404 (checked with requests and curl). `/homology/id/<species>/<id>` returns 200.
- OI-10: `compara_orthologs.py` prints 1:1 rows and a count but not the symbols that failed or returned nothing. In the five-gene zebrafish batch MDM2 timed out (45 s read timeout, recorded in the error column) and BRCA1 returned no rows; neither is shown, and `1:1 calls: 2` reads as complete.
- eggNOG redirect note in SKILL.md is stale (old host now fails TLS).

Gap: the Ensembl homology endpoint was slow (read timeouts of 45 s on BRCA1 and MDM2 to zebrafish; TP53 human to mouse timed out once in the first sweep and passed on the follow-up). Not a Skill defect.

Evidence: scripts/evidence/ (run_reaudit.txt, run_extra.txt, run_batch5.txt, example_*.txt); scripts/.
