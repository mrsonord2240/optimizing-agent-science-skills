# Handoff: bio-uniprot-access / fix-scientific-skill

- Updated: 2026-10-03
- Lane: 2
- Status: ready-for-phase
- Owner leaving: fix worker (Sonnet), lane 2, batch database-access light
- Next role: prepare-scientific-skill-tooling (delta mode), then reaudit-scientific-skill

## Source identity

- Origin: GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:database-access/uniprot-access
- Working tree: F:\OpenScience\wt\dbaccess-uniprot-access\skills\bio-uniprot-access (untracked by design)
- Branch/worktree: fix/dbaccess-uniprot-access at 2f38178
- Audited candidate: 7f82b9d5aae0ba064038b97d399123a2be4d845124d1d4cf13a0918dd4e48240 (audit score 61, Beta Only)
- New candidate identity: e5b597f3d58d78960d6e5d99216956fc3b4ff9e29ee1e0096b28f1366caf5899 (sha256-manifest-v1, files=5, bytes=29226); preflight --offline PASS, no pycache

## Finding ledger

| ID | Sev | State | Change / evidence |
|---|---|---|---|
| UNI-001 | P1 | fixed | map_ids reads /idmapping/stream (44 rows incl BRCA2), merges unmapped inputs into failedIds, FAILED raises, Swiss-Prot target documented; verify.py |
| UNI-002 | P1 | fixed | download_proteome uses uniprotkb/stream?query=proteome:UPID&format=fasta&compressed=true (UP000000625: 4403 records, valid gzip); endpoint table fixed |
| UNI-003 | P1 | fixed | isoforms_and_xrefs.py joins ids; example exits 0 |
| UNI-004 | P1 | fixed | xref:pdb -> database:pdb (904 hits); ft_active_site -> ft_act_site (accepted live) |
| UNI-005 | P2 | fixed | search_tsv(with_total=True) + truncation warning; example prints N of total; KW-0418; corpus sizes 576K / 149M (2026_03) |
| UNI-006 | P2 | fixed | inactive entry raises ValueError with reason; failure-mode text corrected (secondary redirects, deleted = 200 Inactive) |
| UNI-007 | P2 | fixed | uniref_cluster: identity=50 (int), representative=P04637, representative_member_id=P53_HUMAN |
| UNI-008 | P2 | fixed | _request helper: 60 s timeout, retry 429/5xx with Retry-After, connection retries; poll uses monotonic clock and FAILED check. stream_tsv still buffers in memory (documented; not needed for readiness) |
| UNI-009 | P2 | deferred-with-rationale | no Skill-root LICENSE; preflight warns only, manifest cites repo license evidence; adding a file needs upstream license text/holder (licensing decision), not needed for readiness |

Claim-family sweep done (rg for xref:pdb, active_site, 250M, 570K, fasta.gz, results/{jobId}, 404 or 301, KeyError): survivors are intentional warnings (SKILL.md) and the client docstring.

## Changed files

scripts/uniprot_client.py, SKILL.md, usage-guide.md, examples/isoforms_and_xrefs.py, examples/uniprot_query.py.

## Execution record

- F:\OpenScience\audits\bio-uniprot-access\fix-run\verify.py and verify_output.txt: 15 checks, ALL OK against UniProt 2026_03 (live), env database-access-venv py3.12.13, requests 2.34.2, pandas 3.0.5; both examples run end to end, resolve_obsolete regression passes, retry helper tested with a stubbed 429.
- Original audit evidence: F:\OpenScience\audits\bio-uniprot-access\initial-audit-run\ (scripts there not rerun; verify.py covers the same claims with assertions)

## Tooling impact: changed

No new dependency, runtime, model or data. Runnable surfaces changed: map_ids, resolve_obsolete, search_tsv, fetch_entry_json, uniref_cluster, download_proteome (new route), both examples. TOOLS.md surface notes are stale (proteome route, map_ids truncation, example failure); delta pass should refresh them. Human-proteome download still not staged (UP000000625 used).

## Blockers

None.

## Worktree safety

- Run-owned changes: the five Skill files above (untracked), fix-run dir above
- Pre-existing/user-owned: F:\optimizing-agent-science-skills\test\validate.bats (untouched)
- Product commits/pushes/staging: none. Other lanes' worktrees untouched.

## Transition assertion

- Next-phase prerequisites met: yes
