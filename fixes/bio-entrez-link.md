# bio-entrez-link — fix pass (2026-09-19)

Source audited: `GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:database-access/entrez-link`.
Score 80/100, Beta Only, not deployable. Fixed on `fix/db-entrez-link` in
`F:\OpenScience\wt\db-el` against `mrsonord2240/bioSkills` staging `main` (03f5057).

| finding | priority | change | verified | notes |
| --- | --- | --- | --- | --- |
| `cmd='acheck'` discovery crashes: `KeyError: 'Name'` (current Biopython 1.88/NCBI keys `LinkInfo` entries as `LinkName`) | P0 | `examples/discover_links.py` line 15, and both inline `acheck` snippets in `SKILL.md` (~line 85, ~line 254): `i['Name']`/`ls["Name"]` -> `i['LinkName']`/`ls["LinkName"]` | ran (live NCBI, `database-access` shared venv, Biopython 1.88) | all three occurrences of the bug fixed; `discover_links.py` now runs end-to-end for gene 672 (33 linknames), nucleotide 31322957 (5), pubmed 35412348 (11) |
| `LinkInfo` entries can omit `MenuTag`/`HtmlTag` entirely, unguarded (confirmed: `nuccore_nuccore_mrnaonly`, `pubmed_pmc_local`) | P1 | Same three code sites: index access -> `.get('MenuTag', '<none>')` / `.get('HtmlTag', '<none>')` | ran (live NCBI) — nucleotide UID 31322957 case, which has 1/5 entries missing `MenuTag`, now prints `<none>` instead of raising | `discover_links.py` docstring updated to state the guard explicitly |
| Canonical asymmetric-round-trip example (PMID 35412348) shows 0/0 on live data, no longer demonstrates the asymmetry | P1 | Swapped the demo to TP53 (Gene UID 7157) `gene_pubmed_rif` vs `gene_pubmed` in `usage-guide.md`'s "Asymmetric round-trip awareness" prompt and in `examples/basic_linking.py`'s round-trip section (with a comment explaining why the PMID was dropped); also replaced a Quick Start bullet that referenced the same stale PMID with a generic phrasing | ran (live NCBI): 9982 curated vs 20402 all, RIF verified as proper subset | `basic_linking.py`'s unrelated `neighbor_score` demo (still on PMID 35412348) was untouched — that call doesn't depend on gene links and was not flagged |
| No guardrail for clinically-actionable link tables (`gene_clinvar`, `gene_omim`, `gene_gtr`, `gene_medgen_diseases` — e.g. 16,064 real ClinVar records for BRCA1) | P1 | Added a "Clinically-actionable link tables" section to `SKILL.md` (after "Asymmetric link warning"): non-diagnostic caveat + clinician/genetic-counselor referral instruction when these linknames are surfaced for a patient-framed request | docs-only; text placement verified adjacent to the per-database catalog rows for clinvar/omim | previously this behavior relied entirely on general safety training per the audit |
| Related Skills omits local-blast/remote-homology as the correct redirect for similarity-search requests | P2 (cheap) | Added a one-line entry to both `SKILL.md` and `usage-guide.md` Related Skills sections | confirmed both `database-access/local-blast/` and `database-access/remote-homology/` exist as sibling Skills | |
| `neighbor_score` scale (raw NCBI magnitude, tens of millions) undocumented | P2 (cheap) | Added a one-line note under the `related_pubmed`/`neighbor_score` code pattern in `SKILL.md` | matches live value observed (`Score=29748057`) in this pass's own verification run | |

## Redundancy pass (FIX_BRIEF "remove redundancy every pass")

- `usage-guide.md`'s "What the Agent Will Do" (7-step workflow) was agent-facing decision-flow content that belongs in `SKILL.md`, not the human-facing guide — moved verbatim to a new `SKILL.md` "## Workflow" section (after "Required Setup"); `usage-guide.md` now points to it.
- `usage-guide.md`'s "Prerequisites" section duplicated `SKILL.md`'s "Required Setup" `Entrez.email`/`api_key` snippet exactly; its one non-duplicate line (`pip install biopython`) moved into `SKILL.md`'s "Required Setup"; the section was replaced with a pointer.
- `usage-guide.md`'s "Tips" list (7 bullets) was entirely already stated in `SKILL.md` (linkname primacy, RIF curation, single-vs-multi-input indexing already in Failure Modes, `neighbor_score`/`Score` field, `neighbor_history` for large batches, asymmetric-tables-are-a-feature, `homologene` deprecation) — deleted. One phrase not present elsewhere ("prefer Ensembl Compara or OrthoFinder for current orthology") was folded into `SKILL.md`'s `homologene` table row before deleting the source bullet.

## Left unfixed

None of the P0/P1/cheap-P2 findings were left unfixed.

Co-authored by Claude Sonnet 5.
