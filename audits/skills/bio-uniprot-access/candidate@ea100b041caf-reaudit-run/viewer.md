> **Audit record for `bio-uniprot-access`**
> - Audited working candidate `ea100b041cafcbf60a8d1202d6ca09387fff80515d37b45d5998162fb799bcb1`; exact candidate provenance is in [source-identity.json](source-identity.json).
> - Derived from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/database-access/uniprot-access), authored by [GPTomics](https://github.com/GPTomics) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-10-03 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test inputs and provenance are described in the published scripts/inputs and audit body; raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Final re-audit: bio-uniprot-access

**Date:** 2026-10-03
**Candidate:** `F:\OpenScience\wt\dbaccess-uniprot-access\skills\bio-uniprot-access` (untracked, uncommitted by design)
**Exact identity:** `sha256-manifest-v1 ea100b041cafcbf60a8d1202d6ca09387fff80515d37b45d5998162fb799bcb1` (6 files, 30,291 bytes), unchanged before and after the run
**Result:** Candidate-ready: **86/100, Production Ready** (static 85, execution average 87.0). UniProt release 2026_03.

## Readiness gate

| Metric | Value | Requirement |
|---|---:|---:|
| Final score | 86 (34.0 + 52.2 = 86.2) | 85 |
| Static | 85 | 80 |
| Execution average | 87.0 | 85 |
| Layer 1 average | 34.8 / 40 | 32 |
| Layer 2 average | 52.2 / 60 | 48 |
| Assertions | 29 / 30 (97%) | 90% |
| Veto / open P0 | none / none | none |

## Initial findings

| ID | Sev | Disposition | Independent evidence |
|---|---|---|---|
| UNI-001 | P1 | verified-fixed | `evidence/idmap.txt`: 44 rows equal an independent stream pull (page one has 25); BRCA2 present; unmapped inputs in failedIds; TP53 TrEMBL count 18 as documented |
| UNI-002 | P1 | verified-fixed | `evidence/proteome.txt`: E. coli gzip with 4,403 records equal to the server; old route returns 400 as documented (human caveat is UNI-010) |
| UNI-003 | P1 | verified-fixed | `evidence/examples.txt`: isoforms_and_xrefs.py exits 0 |
| UNI-004 | P1 | verified-fixed | `evidence/search.txt`: database:pdb matches, xref:pdb 0; ft_act_site accepted, ft_active_site 400 |
| UNI-005 | P2 | verified-fixed | `evidence/search.txt`: 500 of 625 with a warning; stream returns 625; corpus sizes match 2026_03 |
| UNI-006 | P2 | verified-fixed | `evidence/entry.txt`: inactive accession raises ValueError with the reason; secondary redirects |
| UNI-007 | P2 | verified-fixed | `evidence/uniref.txt`: identity 50/90/100, representative P04637 / P53_HUMAN, member counts equal the server |
| UNI-008 | P2 | verified-fixed | `evidence/retry.txt`, `evidence/idmap.txt`: Retry-After honoured, exponential backoff, 60 s timeout, 5 attempts then raise; stuck job TimeoutError; FAILED RuntimeError |
| UNI-009 | P2 | verified-fixed | upstream MIT LICENSE at the Skill root; preflight PASS |

## New finding

- **UNI-010 (P2):** `download_proteome('UP000005640')` returns all UniProtKB entries in the proteome: 147,520 records (20,416 reviewed + 127,104 TrEMBL), 37.8 MB gzip, 86.7 MB raw. `examples/isoforms_and_xrefs.py` prints "~20 MB compressed; ~80 MB unpacked; ~20K proteins", and no text warns that TrEMBL is included. Evidence `evidence/proteome.txt`, `evidence/proteome_counts.txt`. The function itself is correct and the count equals the server's.

## Execution

Interpreter `F:\OpenScience\audit-envs\database-access\Scripts\python.exe` (py3.12.13, requests 2.34.2, pandas 3.0.5), no installs; inputs are public live API calls and the temporary proteome downloads were deleted. Every surface was executed; UniProt was healthy throughout.

| Surface | Status | Evidence |
|---|---|---|
| fetch_entry_json (primary, secondary, deleted, malformed, TrEMBL, no-gene entry) | executed | `evidence/entry.txt` |
| search_tsv / stream_tsv, query syntax and field claims | executed | `evidence/search.txt` |
| map_ids / resolve_obsolete, stuck and FAILED job guards (stubbed status) | executed | `evidence/idmap.txt` |
| list_isoforms, fetch_isoform_fasta, xref_summary | executed | `evidence/isoform.txt` |
| uniref_cluster (50/90/100) | executed | `evidence/uniref.txt` |
| download_proteome (E. coli, human) | executed | `evidence/proteome.txt` |
| retry helper (429, 503, 404, connection errors) | executed (stubbed transport) | `evidence/retry.txt` |
| examples/uniprot_query.py, examples/isoforms_and_xrefs.py | executed, exit 0 | `evidence/examples.txt` |

## Veto review

Skill veto PASS (stability, contract, determinism, security). Research veto PASS (scientific integrity, practice boundaries, methodological ground, code usability); see `report.json`.

## Per-input scores

| Input | Type | Basic /40 | Specialized /60 | Total | Assertions |
|---|---|---:|---:|---:|---:|
| 1 uniprot_query.py | Canonical | 36 | 54 | 90 | 5/5 |
| 2 isoforms and xrefs | Variant A | 35 | 52 | 87 | 5/5 |
| 3 ID mapping handling | Variant B | 36 | 54 | 90 | 5/5 |
| 4 search syntax and claims | Variant A | 36 | 54 | 90 | 5/5 |
| 5 proteome download | Stress | 31 | 46 | 77 | 4/5 |
| 6 entry edges, UniRef, retry | Edge | 35 | 53 | 88 | 5/5 |

Rerun: `Scripts\python.exe reaudit-run\scripts\reaudit_uni.py <idmap|entry|search|isoform|uniref|proteome|retry|examples>`.
