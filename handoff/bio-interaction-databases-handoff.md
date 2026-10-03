# Handoff: bio-interaction-databases / prepare-scientific-skill-tooling

- Updated: 2026-10-02T23:28:06-07:00
- Lane: 1
- Status: ready-for-phase
- Owner leaving: normalize worker (Sonnet), lane 1, batch database-access
- Next role: prepare-scientific-skill-tooling

## Source identity

- Origin: GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:database-access/interaction-databases (4 files, 35295 bytes, sha256-manifest-v1 e347b6761590b98eec7044ca28716da2576c696da27c6acf3b4a5101227a0d56)
- Working tree: F:\OpenScience\wt\dbaccess-interaction-databases\skills\bio-interaction-databases
- Branch/worktree: fix/dbaccess-interaction-databases at 2f38178 (shelf main)
- Candidate tree hash: 588996fc143fb0dc98a5558fce2db091e0905415fb9a80a8c4bc49419690be42 (sha256-manifest-v1, files=5, bytes=31873; `python tools/skill_preflight.py` = PASS)
- Applicable audit: none

## Completed this phase

- Frontmatter made Marketplace-complete: `category: Data Analysis`, `license: MIT`, `author: GPTomics` (matches shelf siblings bio-entrez-fetch / bio-biomart-queries).
- All files rewritten UTF-8, LF, no BOM; no __pycache__, dot paths, or nested LICENSE.
- Structure: SKILL.md (decision matrix, per-resource semantics, licenses, failure modes) + usage-guide.md; STRING/BioGRID/SIGNOR/OmniPath/aggregation code consolidated into `scripts/interaction_clients.py`.
- Structure: `examples/` (2 demos) import the client; PHYSICAL_LT_SYSTEMS is defined once.
- Version drift against live services fixed (below). Preflight PASS with only the expected no-Skill-root-LICENSE warn (sibling convention; license in frontmatter). No near-duplicate warnings.

## Runnable-surface inventory

- `scripts/interaction_clients.py` (library). Functions: string_network, string_resolve_ids, biogrid_lt_physical, signor_for_gene, omnipath_interactions, aggregate_networks, summary, multi_source_edges.
- `examples/string_network.py` (STRING tiers/channels/centrality), `examples/interaction_query.py` (DiGraph union; writes `aggregated_interactions.csv` to CWD).

## Dependency clues

- Python: requests 2.31+, pandas 2.2+, networkx 3.2+ (env: 2.34.2 / 2.3.3 / 3.4.2). `omnipath` pip client is mentioned only in usage-guide (not installed, not required). R STRINGdb/OmnipathR mentioned only.
- BioGRID needs a free access key (HTTP 401 without); STRING/OmniPath/SIGNOR keyless. Hosts: version-12-5.string-db.org, omnipathdb.org, signor.uniroma2.it, webservice.thebiogrid.org.

## Version drift resolved

- STRING pin `version-12-0` -> `version-12-5` (live `/api/json/version` = 12.5; network TSV columns unchanged, verified). Claim 'version-11-5 deprecated/404' was false (host still answers with older data); reworded in SKILL.md and usage-guide.
- Version Compatibility rewritten with live observations dated 2026-10-02.

## Required next actions

1. Tooling: build/refresh the env for the dependencies above (staging at F:\OpenScience\audit-envs\database-access\, not modified here), map each surface to coverage, record the TOOLS.md fingerprint.
2. Exercise the client functions and examples against live services; settle the ambiguities below before audit.
3. The 2026-10-02 spot checks were ad hoc curl/Python calls, not audit evidence.

## Open findings and blockers

| ID | Severity | State | Evidence | Required disposition |
|---|---|---|---|---|
| N1 | P2 | open | this handoff | SIGNOR contract (behavioral): `organism=human&entity=TP53` returns 'No result found.'; `organism=9606&entity=TP53` returns header-less rows in a different column layout and seemingly ignores `entity`; `organism=9606&id=P04637` filters. `signor_for_gene` parsing (header skip, cols 0-3, 7) is likely wrong. Left unchanged, flagged in SKILL.md; needs audit/fix decision. |
| N2 | P2 | open | this handoff | BioGRID path untested (no key). OmniPath `types=post_translational` + `license=academic` returned data in a spot check. |

## Environment and evidence

- Tool inventory: none yet (tooling phase)
- Run evidence: preflight output only; spot checks not retained
- Restricted-access items: BioGRID API key
- Tooling impact: changed (new importable client under scripts/; examples rewired to import it)

## Worktree safety

- Run-owned changes: untracked `skills/bio-interaction-databases/` in F:\OpenScience\wt\dbaccess-interaction-databases (nothing staged or committed)
- Pre-existing/user-owned changes: none
- Records state: this handoff file only
- Product commits/pushes: none

## Transition assertion

- Next-phase prerequisites met: yes
