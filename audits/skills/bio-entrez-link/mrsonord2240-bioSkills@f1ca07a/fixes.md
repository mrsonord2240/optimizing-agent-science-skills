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

---

# bio-entrez-link — fix pass 2 (2026-09-21)

Re-audit 90.5, Production Ready, 2 open P2s. Worktree `F:\OpenScience\wt\database-access-entrez-link`, branch `fix/database-access-entrez-link` from staging `main` 431aa55. Env `database-access` (Python 3.12, Biopython 1.88), live public E-utilities, no API key.
Commits: a2a52de (fix), 7f7ee57 (split), d0f0472 (fix), 0c82195 (scripts), f1ca07a (fix). The two later fixes came after the split/scripts order the brief prescribes because they were found while running the moved snippets.

| finding | priority | change | verified (ran / help / docs) | notes |
| --- | --- | --- | --- | --- |
| No dbfrom/id namespace validation (audit input 9) | P2 | New `scripts/check_source_ids.py` (`describe_ids`, `checked_elink`, CLI): ESummary-resolves each UID in `dbfrom`, prints title/caption, exits non-zero on an unresolvable UID. New Workflow step 2; "Mismatched dbfrom and id namespace" failure mode rewritten (also warns that UIDs collide across databases) | ran live: gene 672/7157 labelled BRCA1/TP53; pubmed 31322957 (a foot-ankle paper) vs nucleotide 31322957 (AY286018, wallaby opsin) distinguishable by label; `pubmed 999999999999` and `gene 35412348` exit 1 with a message; `checked_elink('gene','protein',['672'])` -> 368 links | Validation can confirm resolution, not intent, so it prints the label for a human/agent comparison |
| P0 acheck fix has no regression test | P2 | `examples/discover_links.py`: asserts `LinkName` and `DbTo` on every LinkInfo entry, body moved under `if __name__ == '__main__'` | ran live: full output for gene 672, nucleotide, pubmed (59 lines, MenuTag `<none>` handled); mutated response (`LinkName` -> `Name`) trips the AssertionError with the key list | Guard is in the example, not a separate test file |
| (found) `discover_links.py` labelled nucleotide UID 31322957 as NM_007294.4 | P2 | It is AY286018 (Macropus opsin). Example now uses 1732746264 (esearch `NM_007294.4[Accession]`) | ran live, acheck returns 5+ linknames incl. `nuccore_nuccore_mrnaonly` with no MenuTag | |
| (found) "1-5 canonical isoforms / 500 proteins / 10-1000x" claims contradicted by the audit's own run | P2 | SKILL.md (intro, `gene_protein` row, `gene_protein_refseq` row, Wrong-linkname failure mode), `usage-guide.md` prompt, `basic_linking.py` label: measured BRCA1 368 RefSeq vs 1087 all (3.0x), TP53 25 RefSeq; `_refseq` returns every RefSeq isoform (all TaxId 9606) | ran live: `basic_linking.py` unchanged output; esummary of the 368 confirms isoform titles | |
| (found) Chunked EPost + `neighbor_history` links only the last chunk | P2 (silent wrong result) | `examples/chain_links.py::link_batch_via_history` unions chunk QueryKeys with ESearch `#1 OR #2`; demo uses 250 distinct UIDs and asserts >1000 linked proteins; new failure mode; "NCBI hard limit" wording for 200 dropped | ran live: last key only -> 197 proteins, first only -> 1177, union -> 1374 (197+1177); fixed example -> 1374, exit 0; single EPost of 1,500 UIDs succeeded (1496 records) | The audit's "QueryKey: 3" output looked fine but was the ELink result key over the last 50 IDs |
| (found) comma-joined `id` returns one merged LinkSet, contradicting "one LinkSet per input UID" | P2 (silent wrong result) | `batch_gene_protein` passes a list; Workflow step 6 and the indexing failure mode rewritten with both forms | ran live: list -> 2 linksets (368, 25); comma-joined -> 1 linkset (393); fixed snippet returns `{'672': 368, '7157': 25}` | `gene_to_structures` and `chain_links.py` keep the comma-joined form on purpose (they want the union) |

## Left unfixed

None of the audit's 2 P2s were left unfixed. Not done and why:
- `HTTPError 400` for a bad linkname was not reproduced live; carried over as written (folded into a failure mode).
- `Entrez.api_key` 10 req/s claim not tested (no key registered; not authenticated services).
- `references` link tables (`link_catalog.md`) not re-verified against live acheck beyond the entries the audit and this pass ran.

## Redundancy pass

Already done in the 2026-09-19 pass for `usage-guide.md`; nothing further there. Within SKILL.md:

| deleted passage | new home |
| --- | --- |
| "Common errors" table (5 rows) | `KeyError: 'LinkSetDb'` -> Failure modes "Empty LinkSetDb"; 414 -> "URL length limit"; 400 -> new "Invalid linkname (HTTP 400)"; 500-vs-5 -> "Wrong linkname multiplies the result set"; round-trip -> "Asymmetric link warning" |
| Failure mode "Asymmetric round-trip" | Merged into "Asymmetric link warning" (last sentence: original PMID may be missing, document asymmetry, use `*_rif`) |
| Old "Mismatched dbfrom" one-line fix | Replaced by the rewritten failure mode |

Verified by grep that each destination sentence exists.

## Split (7f7ee57)

SKILL.md 365 -> 177 lines (183 after the two later fixes). "Per-database link catalog" -> `references/link_catalog.md` (57 lines); "Code patterns" -> `references/code_patterns.md` (144 lines then; 109 after scripts step). Verbatim moves; Reference Files index plus pointers in Workflow steps 4 and 5. Multiset compare of non-blank lines: nothing lost except the two Workflow lines extended with pointers; fences balanced, python fences `ast.parse`.

## scripts/ (0c82195)

| old location | new |
| --- | --- |
| `references/code_patterns.md` `post_then_link` (24 lines) | duplicate of `examples/chain_links.py::link_batch_via_history`; deleted, pointer to the example |
| `references/code_patterns.md` `list_link_names` (+ loop) | duplicate of `examples/discover_links.py`; deleted, pointer to the example |
| (new) | `scripts/check_source_ids.py`, invoked as `python scripts/check_source_ids.py gene 672` (ran) |

No other block reaches ~15 lines (largest: `gene_to_structures`, 14); the remaining inline snippets ran live (`batch_gene_protein`, `gene_to_structures` 251 structures, `related_pubmed`, `bioproject_to_sra` 78 runs).
