Environment: shared `database-access` venv (py3.12.13, requests 2.34.2, pandas 3.0.5, numpy 2.5.3, networkx 3.7, pip-freeze sha256 5fdd1350df2cf397), PYTHONDONTWRITEBYTECODE=1; live services on 2026-10-03; nothing installed or downloaded; candidate read-only, no pycache.

| Surface | Class | Evidence |
|---|---|---|
| batch_compara statuses and column set (local stub, loopback) | executed | scripts/evidence/stub.txt |
| batch_compara live, unknown symbol NOTAGENE123 | executed | scripts/evidence/notagene.txt |
| get_with_retry (503, 429, 500, 404, refused connection) | executed on local stub, new bytes | scripts/evidence/run_reaudit.txt |
| resolve_symbol, compara_one2one, MARCH1/MARCHF1 | executed | run_reaudit.txt |
| compara_orthologs TP53 human to mouse inside run_reaudit | request timed out (Ensembl slow); same call succeeded in notagene.txt and compara.txt | run_reaudit.txt, notagene.txt |
| orthodb_*, /tab, /group | executed | run_reaudit.txt |
| oma_orthologs (rel_type), oma_hog_for_protein | executed (run_reaudit.txt line "OMA TP53 1:1" is a script slice artifact; 130 1:1 incl. P53_MOUSE shown in cross.txt) | run_reaudit.txt, cross.txt |
| ko_for_gene, genes_for_ko, ko_info | executed | run_reaudit.txt |
| PANTHER matchortho | liveness only | run_reaudit.txt |
| HomoloGene | retired, error body | run_reaudit.txt |
| Compara /homology/id route with and without species | executed (curl) | scripts/evidence/route.txt |
| eggNOG API | not executed: eggnogdb.org/api 403; eggnog6.embl.de TLS failure (prior run evidence, not re-probed) | reaudit-run run_extra.txt |
| examples/compara_orthologs.py | executed, exit 0 | scripts/evidence/compara.txt |
| examples/cross_resource.py | executed, exit 0 (Compara leg UNAVAILABLE after timeout, isolated) | scripts/evidence/cross.txt |
| examples/kegg_orthology.py | executed, exit 0 | scripts/evidence/kegg.txt |

The "SKILL.md route without species" line in run_reaudit.txt is the old script's deliberate probe of the species-less route (404); SKILL.md no longer documents it.
