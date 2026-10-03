# Handoff: bio-ortholog-inference / fix-scientific-skill

- Updated: 2026-10-03
- Lane: 3
- Status: ready-for-phase
- Owner leaving: fix worker (Sonnet), lane 3, batch database-access
- Next role: reaudit-scientific-skill (tooling delta done 2026-10-03)

## Source identity

- Origin: GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:database-access/ortholog-inference
- Working tree: F:\OpenScience\wt\dbaccess-ortholog-inference\skills\bio-ortholog-inference (branch fix/dbaccess-ortholog-inference at 2f38178; Skill dir untracked and uncommitted by design)
- Fixed candidate identity: aa32b51586699da5ed4708ce63e6cbc9eb19751ed79f94b5ff5d73208e252495 (sha256-manifest-v1, 7 files, 34073 bytes; preflight --offline PASS, no warnings)
- Superseded: f6d4ccc5903d157167ae1106f009ecf5d36a0e1d3c56c8a691e63625fcc2e9ac (6 files, 27397 bytes)
- Audit fixed against: F:\optimizing-agent-science-skills\audits\skills\bio-ortholog-inference\candidate@f6d4ccc5903d-initial-audit-run\report.json (69, Beta Only)
- Last edit after the final full example run: one-character spacing fix in the examples/compara_orthologs.py print format; syntax-checked, not rerun.

## Finding ledger

| ID | State | Change | Evidence (fix-run = F:\OpenScience\audits\bio-ortholog-inference\fix-run\) |
|---|---|---|---|
| OI-01 | fixed | `orthodb_orthologs` parses data[].genes[].gene_id.id null-safely, [] on null data, raises via get_with_retry on errors | verify_fix_output.txt (null group -> [], p53 group -> mouse Trp53/22059) |
| OI-02 | fixed | one `get_with_retry`: session, (10,45) timeout, retry 429/5xx/connection with backoff, used by every helper; `batch_compara` catches RequestException | example_cross_resource.txt (Ensembl read timeout became "UNAVAILABLE", exit 0); verify_fix_output.txt (unreachable host raises RequestException in 9 s) |
| OI-03 | fixed | Compara confidence claims removed from SKILL.md, docstrings, usage-guide, examples; type/taxonomy_level/identity documented; `taxonomy_level` added to rows | verify2_output.txt, example_compara_orthologs_run2.txt |
| OI-04 | fixed | SKILL.md documents /search as full text; new `orthodb_search`, `orthodb_group_has_gene`; example filters exact name then verifies human member | example_cross_resource_run2.txt (verified 4289813at2759, mouse 22059/Trp53); verify_fix_output.txt (TIGAR group rejected) |
| OI-05 | fixed | cross_resource.py isolates each leg (unavailable vs empty), uses TP53/P04637 and `rel_type='1:1'`; `oma_orthologs` gains `rel_type` | example_cross_resource_run2.txt (all three legs OK), verify_fix_output.txt (BRCA1 -> 0 documented as no OMA call) |
| OI-06 | fixed | `/tab?id=<og>` is the live form (`query=` 404); doc corrected | curl probe this phase (tab?id returns TSV, tab?query 404) |
| OI-07 | fixed | PANTHER route documented with real fields (orthologType=LDO), evidence-code claim removed, "client does not wrap PANTHER" stated | panther_verify.txt (200, ortholog LDO, mouse Tp53 P02340) |
| OI-08 | fixed | Skill-root LICENSE added (upstream repo MIT, byte-identical to bioSkills-Improved\LICENSE); `oma_orthologs` docstring uses species.taxon_id | preflight PASS, no warning |
| B1 | deferred-with-rationale | OMA gateway flakiness is service-side; Skill now retries and prefers rel_type=1:1; OMA ran clean 3 times this phase | example_cross_resource_run2.txt |
| B2 | deferred-with-rationale | eggNOG API refuses scripts; Skill already labels it unverified; not executed | TOOLS.md |

No new findings. Residual: Ensembl homology calls are slow or time out intermittently (one compara_orthologs.py run raised after 4 attempts on HTTP 500; later run passed); service-side.

## Changed files

scripts/ortholog_clients.py, SKILL.md, usage-guide.md, examples/cross_resource.py, examples/compara_orthologs.py, LICENSE (new). examples/kegg_orthology.py unchanged but re-run through the new client (exit 0, KO K04451, 548 members, 446 species).

## Execution record

- Interpreter: F:\OpenScience\audit-envs\database-access\Scripts\python.exe (py3.12.13, requests 2.34.2, pandas 3.0.5), PYTHONDONTWRITEBYTECODE=1; no packages installed, no pycache in the Skill tree.
- Scripts and outputs: fix-run\run_examples.sh, verify_fix.py, verify2.py, panther.py and the matching *_output / example_*.txt files.
- compara_orthologs.py: exit 0 (BRCA1 1:1 mouse ENSMUSG00000017146, MARCHF1 -> ENSG00000145416, zebrafish batch TP53/ATM 1:1).

## Tooling impact: changed

Reason: client behavior changed (timeouts, retry, OrthoDB parser, new helpers `orthodb_search` and `orthodb_group_has_gene`, `rel_type` argument) with no new dependency or runtime. Affected surfaces: Compara resolve/orthologs/one2one/batch, OrthoDB orthologs and search, OMA orthologs/HOG, KEGG helpers, examples/cross_resource.py. Nothing to install.

## Tooling (delta, 2026-10-03)

- TOOLS.md: F:\OpenScience\audits\bio-ortholog-inference\TOOLS.md (refreshed surface map; OrthoDB, OMA, retry and example rows replaced). Shared: F:\OpenScience\audit-envs\database-access\TOOLS.md.
- Fingerprint verified live: database-access-venv py3.12.13 | requests 2.34.2 pandas 3.0.5 numpy 2.5.3 networkx 3.7 | pip-freeze sha256 5fdd1350df2cf397.
- Identity unchanged (preflight --offline PASS): aa32b51586699da5ed4708ce63e6cbc9eb19751ed79f94b5ff5d73208e252495, files=7, bytes=34073.
- Installed: nothing. Downloaded: nothing. Live spot check: Compara, OrthoDB search/groups, KEGG pass; OMA HTTP 502 after 4 retries (service-side).
- Not made ready: OMA (flaky, rerun later), eggNOG (refuses scripts).

## Worktree safety

- Run-owned: the Skill tree above (untracked) and F:\OpenScience\audits\bio-ortholog-inference\fix-run\
- Pre-existing/user-owned: test\validate.bats (untouched); other lanes' worktrees, handoffs, records untouched
- Product commits/pushes/staging: none

## Transition assertion

- Next-phase prerequisites met: yes
