# Handoff: bio-ensembl-rest / fix-scientific-skill

- Updated: 2026-10-03
- Lane: 4
- Status: ready-for-phase
- Owner leaving: fix worker (lane 4)
- Next role: reaudit-scientific-skill

## Source identity

- Origin: GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:database-access/ensembl-rest
- Working tree: F:\OpenScience\wt\dbaccess-ensembl-rest\skills\bio-ensembl-rest (branch fix/dbaccess-ensembl-rest at 2f38178; Skill dir untracked, uncommitted)
- Audited identity: 3d116ba2e1c5bbcc610914c9e3364af733acbcf69c0c20cc39abc149099e40b2 (audit: audits\skills\bio-ensembl-rest\candidate@3d116ba2e1c5-initial-audit-run\report.json, 70 Beta Only)
- Candidate identity (preflight --offline PASS): sha256-manifest-v1 dabba949803e4c58bd3cc906389087520b3e5f5c32702fb6535c749131c0487b, files=7, bytes=28785

## Finding ledger

| ID | Sev | State | Change / evidence |
|---|---|---|---|
| ENS-001 | P1 | fixed | SKILL.md snippet, example and usage-guide use ENSP00000269305; client gains `multiple_sequences=` (15 records for ENSG00000139618). Evidence: fix-evidence\bio-ensembl-rest\example_lookup_and_overlap.txt, verify.txt |
| ENS-002 | P1 | fixed | vep_annotation.py uses ENST00000366667:c.803C>T (missense_variant). example_vep_annotation.txt, verify.txt |
| ENS-003 | P1 | fixed | usage-guide uses GRCh38 17:43044295 T>A and points GRCh37 coordinates to the grch37 host (splice_region_variant there; 400 on GRCh38 host). verify.txt |
| ENS-004 | P1 | fixed | Regulatory row now `/overlap/region/...?feature=regulatory` (34 features); homology row now `/homology/id/{species}/{id}` (200; no-species 404). verify.txt |
| ENS-005 | P2 | fixed | Docs say 400 `No valid lookup found`; Homo_sapiens noted as accepted. SKILL.md + usage-guide.md |
| ENS-006 | P2 | fixed | Client: 30 s timeout, retry 429/5xx/timeouts, non-JSON check, `EnsemblError`, error body in HTTPError, batch_symbols catches both. Verified: e90 HTML -> EnsemblError, e116 503 -> EnsemblError after 3 tries, timeout path, batch. Docs note temporary archive outage. verify.txt |
| ENS-007 | P2 | fixed | compara example prints "none returned" for empty paralogs; semantics text matches service. example_compara_homology.txt (exit 0 on third attempt; first two hit 503/ReadTimeout on the flaky homology endpoint) |
| ENS-008 | P2 | fixed | Skill-root LICENSE (upstream MIT, LF) copied from origin checkout; preflight no longer warns. |

No new findings. Residual: e116 archive host still returned 503 (service outage, not a fix failure); the e110/e111 archive paths were re-exercised via lookup_and_overlap (e110 OK).

## Changed files

SKILL.md, usage-guide.md, scripts/ensembl_client.py, examples/lookup_and_overlap.py, examples/vep_annotation.py, examples/compara_homology.py, LICENSE (new).

## Evidence

- F:\OpenScience\fix-evidence\bio-ensembl-rest\ (verify.py, verify.txt, example_*.txt); interpreter database-access venv py3.12.13, requests 2.34.2, PYTHONDONTWRITEBYTECODE=1.
- Inputs/tools: F:\OpenScience\audits\bio-ensembl-rest\TOOLS.md (delta-refreshed)

## Tooling impact: none per fixer; recorded as changed by the delta pass

Same requests dependency and venv; no new runtime, executable path or service. The client surface grew (`multiple_sequences=`, `EnsemblError`, retry), so TOOLS.md now lists it.

## Tooling (delta, 2026-10-03)

- TOOLS.md: F:\OpenScience\audits\bio-ensembl-rest\TOOLS.md (refreshed; example failures and sequence/VEP rows replaced). Shared: F:\OpenScience\audit-envs\database-access\TOOLS.md.
- Fingerprint verified live: database-access-venv py3.12.13 | requests 2.34.2 pandas 3.0.5 numpy 2.5.3 networkx 3.7 | pip-freeze sha256 5fdd1350df2cf397.
- Identity unchanged (preflight --offline PASS): dabba949803e4c58bd3cc906389087520b3e5f5c32702fb6535c749131c0487b, files=7, bytes=28785.
- Installed: nothing. Downloaded: nothing. Live spot check: symbol lookup, protein sequence, multiple_sequences (15), VEP HGVS, LD pass.
- Not made ready: e116 archive host (503, service-side); Ensembl homology intermittently 500/timeout.

## Worktree safety

- Run-owned: Skill tree (untracked), F:\OpenScience\fix-evidence\bio-ensembl-rest\, this handoff
- Pre-existing/user-owned: F:\optimizing-agent-science-skills\test\validate.bats (untouched)
- No product commit, push, or staging; no pycache in the Skill tree.

## Transition assertion

- Next-phase prerequisites met: yes
