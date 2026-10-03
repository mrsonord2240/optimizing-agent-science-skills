# bio-uniprot-access fix pass - 2026-10-03

`map_ids` read only the first results page, so a three-gene Ensembl mapping returned 25 of 44 rows and silently lost BRCA2; it now streams the full result and reports unmapped inputs. The proteome download used a route that returns 400 and now uses the UniProtKB stream route. The isoform example crashed on a list, `xref:pdb` and `ft_active_site` were invalid query fields, an inactive accession raised `KeyError`, and `uniref_cluster` mislabelled identity and representative. The client gained a shared request helper with timeouts, retries on 429/5xx and a `FAILED` job check. A later text-only pass corrected the documented size of the human proteome download, which includes unreviewed TrEMBL entries.

- Final candidate audit: `audits/skills/bio-uniprot-access/candidate@7a203a5063ea-delta-reaudit-run`
- Result: **88/100, Production Ready**; no open findings.
- Candidate identity: `7a203a5063ea1cdad2c32516c1cc1740eb13c1e5008d53c5950e81b8cfdf7f5b`.

The provider binding record is the canonical proof that the committed shelf bytes match this independently audited candidate.
