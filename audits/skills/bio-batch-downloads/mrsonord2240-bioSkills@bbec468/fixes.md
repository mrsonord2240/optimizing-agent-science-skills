# Fix log: bio-batch-downloads

2026-09-19 — fixer pass on `fix/db-batch-downloads` (worktree `F:\OpenScience\wt\db-bd`),
commit `bbec468378279e944fe74c3a4612d7d0d204cb6a`, base `mrsonord2240/bioSkills@1332462`.
Source audit: `F:\OpenScience\audits\bio-batch-downloads\` (79/100, Reject, Research Veto M4).

| finding | priority | change | verified | notes |
| --- | --- | --- | --- | --- |
| `examples/robust_download.py`'s `checkpointed_download()` crashes with `TypeError: a bytes-like object is required, not 'str'` on the documented WebEnv-expiry recovery path | P0 | Added `if isinstance(body, bytes): body = body.decode('utf-8', errors='replace')` after `body = h.read()`, matching SKILL.md's own already-correct inline pattern | ran | Live-reproduced the audit's forged-WebEnv/QueryKey test against a real BRCA1 query (368 records): before the fix, TypeError; after, the `<ERROR>` body is detected, `refresh_session()` runs, and the download completes 368/368. |
| Same file's worked example query (`hemoglobin[Gene Name]`, mouse) returns Count=0 live | P0 (same finding, tied fix) | Swapped for `BRCA1[GENE] AND Homo sapiens[ORGN] AND biomol_mrna[PROP] AND srcdb_refseq[PROP]` (368 hits) | ran | Confirmed live 2026-09-19; also re-ran the script's default (non-crash) invocation end to end — completes cleanly, 368 records written. |
| `examples/batch_fasta.py`'s unguarded `SeqIO.parse('insulin_mrna.fasta', ...)` crashes `FileNotFoundError` because its own query (`insulin[Gene Name]`) returns Count=0 and `history_server_download()` returns early without creating the file | P0 | Guarded the integrity-check block on `elapsed == 0` (prints a message, skips parsing instead of crashing); replaced the query with `INS[GENE]` (verified 4 hits) | ran | Live-reproduced the crash on the original code, then ran the fixed script end to end: `history-server: 4 records`, 4 real INS transcripts parsed, no crash. |
| SKILL.md's decision matrix has a hard cap (≤4 workers) but only a soft "consider" for record counts far beyond its documented brackets — no explicit refuse/escape-hatch for a literal "download the entire database" request | P1 | Added a decision-matrix row: for >1,000,000 sequences or a literal "entire database" request, refuse the EFetch-loop approach outright and point only to bulk FTP mirrors / Datasets CLI | docs | Matches the audit's own Input 7 finding and the existing worker-cap phrasing pattern already in the same document. |
| Neither SKILL.md nor usage-guide.md warns that `[GENE]`/`[Gene Name]` field tags need the official gene symbol, not a descriptive word — the exact root cause of both P0 stale queries | P2 | Added a one-line note in SKILL.md near the decision matrix | ran | Verified live: `insulin[Gene Name]`=0 vs `INS[GENE]`=4; `hemoglobin[Gene Name]`=0 vs (not retested for Hba-a1, used BRCA1 instead for the P0 fix). |
| Mandatory redundancy pass | — | Moved `pip install biopython` / `conda install ncbi-datasets-cli` (previously only in usage-guide.md's Prerequisites) into SKILL.md's Required Setup; deleted usage-guide.md's "What the Agent Will Do" (10 steps) and "Tips" (7 bullets) sections — every point in both fully restated SKILL.md's decision matrix, rate-limit math, WebEnv lifecycle, retmax cap, Datasets CLI guidance, and integrity-check pattern verbatim or near-verbatim; nothing in either section was unique. usage-guide.md's Prerequisites now points to SKILL.md instead of repeating the setup code. | inspection | usage-guide.md now holds only Overview, Prerequisites (pointer), Quick Start, Example Prompts, Related Skills, matching the doctrine. |

## Unfixed

None. All P0s and the P1 from the audit's `recommendations[]` were fixed; the one P2 was cheap and fixed too.

## Environment

Verification ran against live NCBI E-utilities via `F:\OpenScience\audit-envs\database-access\Scripts\python.exe` (biopython 1.88, per that env's `TOOLS.md`). No packages installed or changed.
