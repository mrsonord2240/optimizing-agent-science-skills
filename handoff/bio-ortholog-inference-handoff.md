# Handoff: bio-ortholog-inference / prepare-scientific-skill-tooling (delta, after fix-run-2)

- Updated: 2026-10-03
- Lane: 2
- Status: ready-for-phase
- Next role: reaudit-scientific-skill
- Tooling impact: changed (batch_compara status/error columns, examples/compara_orthologs.py output); no new dependency, runtime, input or service.

## Tooling

- TOOLS.md: F:\OpenScience\audits\bio-ortholog-inference\TOOLS.md (refreshed for identity 6e3122b0...; delta section added, unchanged surfaces listed)
- Fingerprint (verified live): py3.12.13 | requests 2.34.2 pandas 3.0.5 numpy 2.5.3 networkx 3.7 | pip-freeze sha256 5fdd1350df2cf397 (raw pip-freeze bytes)
- Interpreter: F:\OpenScience\audit-envs\database-access\Scripts\python.exe, PYTHONDONTWRITEBYTECODE=1
- Delta evidence: fix-run-2\stub.txt (all three statuses), compara_run2.txt (live partial batch); one live attempt this pass: human->mouse [TP53, NOTAGENE123] -> TP53 found, NOTAGENE123 request failed (HTTP 400; invalid symbol reports as failure, not "no ortholog returned").
- Installed or downloaded this pass: nothing. Preflight --offline PASS after the pass (identity unchanged).
- Blockers unchanged: Ensembl homology intermittent (500/503/45 s timeouts), OMA 502s, eggNOG refuses scripts (not executed), PANTHER liveness only.

## Candidate

- Identity (preflight --offline PASS): sha256-manifest-v1 6e3122b03b95f6b9666a03f538ff5e07657ad733c2f0b9a2c7f1de1749993bbb, files=7, bytes=35212
- Path: F:\OpenScience\wt\dbaccess-ortholog-inference\skills\bio-ortholog-inference (untracked, uncommitted by design; no pycache)
- Prior rejected identity: aa32b51586699da5ed4708ce63e6cbc9eb19751ed79f94b5ff5d73208e252495 (84, Limited Release)
- Evidence: F:\OpenScience\audits\bio-ortholog-inference\fix-run-2\

## Findings

- OI-01..OI-08: fixed (earlier ledger, unchanged).
- OI-09: fixed. SKILL.md line 86 now `/homology/id/<species>/<ensembl_gene_id>`. Tree sweep: no other occurrence. Live: route.txt (species form 200, bare form 404).
- OI-10: fixed at client level. scripts/ortholog_clients.py `batch_compara` returns one or more rows per input symbol with `status` = found / no ortholog returned / request failed (message in `error`); fixed column set so an all-failed batch still has `type`. examples/compara_orthologs.py prints per-symbol outcome and a PARTIAL BATCH flag. Evidence: stub.txt (no network), compara_run2.txt (live: MDM2 request failed, BRCA1 no ortholog returned, flagged partial).
- eggNOG note: fixed in SKILL.md line 103 and usage-guide.md line 74 (eggnogdb.org/api 403; eggnog6.embl.de TLS failure; still unverified).

## Changed files

SKILL.md, usage-guide.md, scripts/ortholog_clients.py, examples/compara_orthologs.py

## Execution record

- stub.txt: batch_compara statuses on a local fake (found / request failed / no ortholog returned; all-failed batch keeps columns).
- compara_run1.txt: killed by my 500 s timeout (Ensembl slow), no verdict. compara_run2.txt: exit 0, partial batch reported correctly.
- kegg.txt exit 0; cross.txt exit 0 (Compara, OMA, OrthoDB all returned for TP53).
- No edit after these runs except this handoff.

## Remaining

- Ensembl homology intermittently slow (45 s read timeouts); service-side.
- eggNOG API refuses scripts; not executed. PANTHER liveness only.
- SKILL.md snippet at line ~52 filters on `type`, still valid with the new table.

## Worktree safety

Only the four files above edited in the Skill tree. test\validate.bats, published records and other Skills untouched. No staging, commit or push.
