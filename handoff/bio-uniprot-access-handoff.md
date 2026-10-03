# Handoff: bio-uniprot-access / prepare-scientific-skill-tooling

- Updated: 2026-10-02T23:28:06-07:00
- Lane: 1
- Status: ready-for-phase
- Owner leaving: normalize worker (Sonnet), lane 1, batch database-access
- Next role: prepare-scientific-skill-tooling

## Source identity

- Origin: GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:database-access/uniprot-access (4 files, 30741 bytes, sha256-manifest-v1 5ed6f8e13e0bcecd97c6a7f05555b81a9fda8fac6e906669446c41d83fa0faa8)
- Working tree: F:\OpenScience\wt\dbaccess-uniprot-access\skills\bio-uniprot-access
- Branch/worktree: fix/dbaccess-uniprot-access at 2f38178 (shelf main)
- Candidate tree hash: 7f82b9d5aae0ba064038b97d399123a2be4d845124d1d4cf13a0918dd4e48240 (sha256-manifest-v1, files=5, bytes=24298; `python tools/skill_preflight.py` = PASS)
- Applicable audit: none

## Completed this phase

- Frontmatter made Marketplace-complete: `category: Data Analysis`, `license: MIT`, `author: GPTomics` (matches shelf siblings bio-entrez-fetch / bio-biomart-queries).
- All files rewritten UTF-8, LF, no BOM; no __pycache__, dot paths, or nested LICENSE.
- Structure: SKILL.md (endpoints, query syntax, fields, schema paths, isoforms, ID mapping, failure modes) + usage-guide.md; all inline code consolidated into `scripts/uniprot_client.py`.
- Structure: `examples/` (2 demos) import the client; JSON-schema code listing condensed to a path table.
- Version drift against live services fixed (below). Preflight PASS with only the expected no-Skill-root-LICENSE warn (sibling convention; license in frontmatter). No near-duplicate warnings.

## Runnable-surface inventory

- `scripts/uniprot_client.py` (library). Functions: fetch_entry_json, search_tsv, stream_tsv, map_ids (async submit/poll/fetch with timeout), resolve_obsolete, list_isoforms, fetch_isoform_fasta, xref_summary, download_proteome, uniref_cluster.
- `examples/uniprot_query.py` (entry, kinase TSV search, full human Swiss-Prot stream ~20K rows, Ensembl->UniProt ID mapping), `examples/isoforms_and_xrefs.py` (proteome download left as a printed suggestion).

## Dependency clues

- Python: requests 2.31+, pandas 2.2+ (env: 2.34.2 / 2.3.3). No key. Host rest.uniprot.org. Bio.ExPASy mentioned in prose only (Biopython 1.88 in env).

## Version drift resolved

- Tested release `2024_06` -> `2026_03` (live `X-UniProt-Release`); P04637 entry fetch and result-fields endpoint verified live. Swiss-Prot/TrEMBL counts left as '2024' figures.
- Field-list link corrected to /configure/uniprotkb/result-fields.

## Required next actions

1. Tooling: build/refresh the env for the dependencies above (staging at F:\OpenScience\audit-envs\database-access\, not modified here), map each surface to coverage, record the TOOLS.md fingerprint.
2. Exercise the client functions and examples against live services; settle the ambiguities below before audit.
3. The 2026-10-02 spot checks were ad hoc curl/Python calls, not audit evidence.

## Open findings and blockers

| ID | Severity | State | Evidence | Required disposition |
|---|---|---|---|---|
| N1 | P2 | open | this handoff | `uniref_cluster` returns `identity` from `entryType` (probably a mislabel); `map_ids` reads one results page (pagination for large jobs unchecked); both left as-is for audit. |

## Environment and evidence

- Tool inventory: none yet (tooling phase)
- Run evidence: preflight output only; spot checks not retained
- Restricted-access items: none
- Tooling impact: changed (new importable client under scripts/; examples rewired to import it)

## Worktree safety

- Run-owned changes: untracked `skills/bio-uniprot-access/` in F:\OpenScience\wt\dbaccess-uniprot-access (nothing staged or committed)
- Pre-existing/user-owned changes: none
- Records state: this handoff file only
- Product commits/pushes: none

## Transition assertion

- Next-phase prerequisites met: yes
