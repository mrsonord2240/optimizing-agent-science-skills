# Handoff: bio-ortholog-inference / prepare-scientific-skill-tooling

- Updated: 2026-10-02T23:28:06-07:00
- Lane: 1
- Status: ready-for-phase
- Owner leaving: normalize worker (Sonnet), lane 1, batch database-access
- Next role: prepare-scientific-skill-tooling

## Source identity

- Origin: GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:database-access/ortholog-inference (5 files, 32293 bytes, sha256-manifest-v1 fff8c2b2953d822bf41a5bc7038253cf0de5aa4f99277806bea3fc58bcb762f2)
- Working tree: F:\OpenScience\wt\dbaccess-ortholog-inference\skills\bio-ortholog-inference
- Branch/worktree: fix/dbaccess-ortholog-inference at 2f38178 (shelf main)
- Candidate tree hash: f6d4ccc5903d157167ae1106f009ecf5d36a0e1d3c56c8a691e63625fcc2e9ac (sha256-manifest-v1, files=6, bytes=27397; `python tools/skill_preflight.py` = PASS)
- Applicable audit: none

## Completed this phase

- Frontmatter made Marketplace-complete: `category: Data Analysis`, `license: MIT`, `author: GPTomics` (matches shelf siblings bio-entrez-fetch / bio-biomart-queries).
- All files rewritten UTF-8, LF, no BOM; no __pycache__, dot paths, or nested LICENSE.
- Structure: SKILL.md (decision matrix, per-resource API notes, confidence semantics, failure modes) + usage-guide.md; Compara/OrthoDB/OMA/KEGG code consolidated into `scripts/ortholog_clients.py`.
- Structure: `examples/` (3 demos) import the client; duplicated retry helpers removed.
- Version drift against live services fixed (below). Preflight PASS with only the expected no-Skill-root-LICENSE warn (sibling convention; license in frontmatter). No near-duplicate warnings.

## Runnable-surface inventory

- `scripts/ortholog_clients.py` (library). Functions: get_with_retry, resolve_symbol, compara_orthologs, compara_one2one, batch_compara, orthodb_groups, orthodb_orthologs, oma_orthologs, oma_hog_for_protein, oma_hog_members, ko_for_gene, genes_for_ko, ko_info.
- `examples/compara_orthologs.py`, `examples/cross_resource.py`, `examples/kegg_orthology.py`: live-API demos that run at module level.
- PANTHER, eggNOG, HomoloGene are prose only (no code).

## Dependency clues

- Python: requests 2.31+, pandas 2.2+ (env: 2.34.2 / 2.3.3). No keys. Hosts: rest.ensembl.org, data.orthodb.org/v12, omabrowser.org/api, rest.kegg.jp, pantherdb.org.
- Ensembl 15 req/sec limit; eggNOG-mapper (local tool) is named as the batch path but not scripted.

## Version drift resolved

- HomoloGene: E-utilities `db=homologene` now returns 'Database not supported'; 'still queryable' replaced with 'retired' (SKILL.md, usage-guide).
- eggNOG: `http://eggnog6.embl.de/api/` 301s to `eggnogdb.org/api/`, which gave 403 to a script; marked unverified. PANTHER base http -> https. Ensembl 'release 112+' -> 116 checked live.

## Required next actions

1. Tooling: build/refresh the env for the dependencies above (staging at F:\OpenScience\audit-envs\database-access\, not modified here), map each surface to coverage, record the TOOLS.md fingerprint.
2. Exercise the client functions and examples against live services; settle the ambiguities below before audit.
3. The 2026-10-02 spot checks were ad hoc curl/Python calls, not audit evidence.

## Open findings and blockers

| ID | Severity | State | Evidence | Required disposition |
|---|---|---|---|---|
| N1 | P2 | open | this handoff | OMA REST gave HTTP 502 for `/protein/P38398/` and `[]` (HTTP 200) for `/protein/P38398/orthologs/` on 2026-10-02: transient outage vs changed contract unresolved; re-test in tooling. |
| N2 | P2 | open | this handoff | eggNOG API access (403) and PANTHER ortholog endpoint shapes unexercised; OrthoDB `/search` returned `{'data': [og ids]}` as documented, `/orthologs` shape unchecked. |

## Environment and evidence

- Tool inventory: none yet (tooling phase)
- Run evidence: preflight output only; spot checks not retained
- Restricted-access items: none
- Tooling impact: changed (new importable client under scripts/; examples rewired to import it)

## Worktree safety

- Run-owned changes: untracked `skills/bio-ortholog-inference/` in F:\OpenScience\wt\dbaccess-ortholog-inference (nothing staged or committed)
- Pre-existing/user-owned changes: none
- Records state: this handoff file only
- Product commits/pushes: none

## Transition assertion

- Next-phase prerequisites met: yes
