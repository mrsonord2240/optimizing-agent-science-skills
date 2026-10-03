# Handoff: bio-ensembl-rest / prepare-scientific-skill-tooling

- Updated: 2026-10-02T23:28:06-07:00
- Lane: 1
- Status: ready-for-phase
- Owner leaving: normalize worker (Sonnet), lane 1, batch database-access
- Next role: prepare-scientific-skill-tooling

## Source identity

- Origin: GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:database-access/ensembl-rest (5 files, 27828 bytes, sha256-manifest-v1 14d9f986c8416cc32ab91bdbb854b3d1b4a94f50761e3b5001b9cb3b2557d52c)
- Working tree: F:\OpenScience\wt\dbaccess-ensembl-rest\skills\bio-ensembl-rest
- Branch/worktree: fix/dbaccess-ensembl-rest at 2f38178 (shelf main)
- Candidate tree hash: 3d116ba2e1c5bbcc610914c9e3364af733acbcf69c0c20cc39abc149099e40b2 (sha256-manifest-v1, files=6, bytes=24508; `python tools/skill_preflight.py` = PASS)
- Applicable audit: none

## Completed this phase

- Frontmatter made Marketplace-complete: `category: Data Analysis`, `license: MIT`, `author: GPTomics` (matches shelf siblings bio-entrez-fetch / bio-biomart-queries).
- All files rewritten UTF-8, LF, no BOM; no __pycache__, dot paths, or nested LICENSE.
- Structure: SKILL.md (frontmatter + routing, divisions/pinning/rate limits/VEP/Compara/failure modes) + usage-guide.md; inline code and three copies of `get_with_retry` moved into `scripts/ensembl_client.py`.
- Structure: `examples/` (3 demos) now import the client; no helper duplication remains.
- Version drift against live services fixed (below). Preflight PASS with only the expected no-Skill-root-LICENSE warn (sibling convention; license in frontmatter). No near-duplicate warnings.

## Runnable-surface inventory

- `scripts/ensembl_client.py` (importable library; no CLI, no import-time side effects). Functions: get_with_retry, symbol_to_id, gene_info, sequence_for_id, genes_in_region, vep_region/vep_hgvs/vep_id, orthologs_by_symbol, paralogs_by_symbol, ld_pairwise, batch_symbols.
- `examples/lookup_and_overlap.py`, `examples/vep_annotation.py`, `examples/compara_homology.py`: live-API demos that run at module level.
- SKILL.md mentions POST `/lookup/id` batching (`{"ids": [...]}`) with no code; `/xrefs`, `/genetree`, `/regulatory`, `/variation`, `/ga4gh` are listed only.

## Dependency clues

- Python: requests 2.31+ (env has 2.34.2). No key. Network: rest.ensembl.org, e110/e111/grch37 archive hosts.
- Archive hosts 301-redirect (e110 -> jul2023.rest.ensembl.org); requests follows. Rate limit 15 req/sec, 55K/hour.

## Version drift resolved

- Divisions: `rest.ensemblgenomes.org` no longer resolves (DNS failure); `rest.ensembl.org` serves all divisions (`/info/divisions`). Rewrote divisions table, failure modes, usage-guide.
- Versions: 'release 110+' replaced by live release 116 (`/info/data`); live lookup/VEP/homology/archive redirect spot-checked 2026-10-02. e110 pin kept.

## Required next actions

1. Tooling: build/refresh the env for the dependencies above (staging at F:\OpenScience\audit-envs\database-access\, not modified here), map each surface to coverage, record the TOOLS.md fingerprint.
2. Exercise the client functions and examples against live services; settle the ambiguities below before audit.
3. The 2026-10-02 spot checks were ad hoc curl/Python calls, not audit evidence.

## Open findings and blockers

| ID | Severity | State | Evidence | Required disposition |
|---|---|---|---|---|
| N1 | P2 | open | this handoff | Archive pins: verify e111/e116 redirects and reproducibility (only the e110 redirect target was observed). |

## Environment and evidence

- Tool inventory: none yet (tooling phase)
- Run evidence: preflight output only; spot checks not retained
- Restricted-access items: none
- Tooling impact: changed (new importable client under scripts/; examples rewired to import it)

## Worktree safety

- Run-owned changes: untracked `skills/bio-ensembl-rest/` in F:\OpenScience\wt\dbaccess-ensembl-rest (nothing staged or committed)
- Pre-existing/user-owned changes: none
- Records state: this handoff file only
- Product commits/pushes: none

## Transition assertion

- Next-phase prerequisites met: yes
