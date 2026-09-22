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

## 2026-09-21: P2 batch pass

Worktree `F:\OpenScience\wt\database-access-batch-downloads`, branch `fix/database-access-batch-downloads`
(from staging `431aa55`), commit `8df2313`. Audit: `F:\OpenScience\audits\bio-batch-downloads\`
(2 P2). Env: `database-access` (biopython 1.88), live NCBI E-utilities, a handful of requests.

| finding | priority | change | verified (ran / help / docs) | notes |
| --- | --- | --- | --- | --- |
| ">100,000 sequences" matrix row ends mid-clause ("chunk if E-utils still") | P2 | Completed: "if E-utils is still the chosen path, chunk via the history server (single stream)" | read | Wording only; Input 9's soft-bracket behaviour unchanged. |
| No regression test for the bytes-decode and zero-count guards | P2 | Not added (see left unfixed). Ran both guards by hand instead, see below | ran | Mock: bytes `<ERROR>` body then good body -> re-ESearch, 3/3 written, no TypeError; persistent `<ERROR>` -> `RuntimeError` after `max_retries`, no checkpoint written. Live: SKILL.md snippet on BRCA1 RefSeq mRNA, 368/368, checkpoint removed. |
| Redundancy: inline `checkpointed_batch_download`, `epost_and_fetch`, `verify_fasta_count` duplicate `examples/` | (doctrine) | Deleted the three blocks; SKILL.md keeps Goal/Approach and points at the examples, with a usage snippet | ran (snippet) | The deleted inline `checkpointed_batch_download` had a defect the example does not: after `max_retries` failures it fell out of the retry loop and advanced `start`, silently skipping the chunk. Snippet sets `Entrez.email` after import because `robust_download` overwrites it with a placeholder at import time. |

Usage-guide: the 2026-09-19 pass already reduced it to overview, prompts, related Skills. Nothing to do.

### Length and scripts
SKILL.md 322 -> 239 lines, so no `references/` split. `scripts/`: no runnable block of ~15+ lines
remains inline (the asyncio block is labelled pseudo-code, `estimate_efetch_calls` is 2 lines); no
scripts commit.

### Left unfixed
- **No committed regression test (P2).** It would be a new pytest module with mocked Entrez handles: new
  content, and the Skill ships no test harness or pytest dependency. The guards it would cover are in
  `examples/robust_download.py` and `examples/batch_fasta.py`, which the audit and this pass ran.

### Deleted passage -> new home
| deleted (SKILL.md) | now |
| --- | --- |
| `checkpointed_batch_download()` inline block | `examples/robust_download.py` `checkpointed_download()`; SKILL.md "Production batch fetch" |
| `epost_and_fetch()` inline block | `examples/batch_by_ids.py` `chained_epost_fetch()`; SKILL.md "EPost large ID list" |
| `verify_fasta_count()` inline block | `examples/batch_by_ids.py` `verify_count()`; SKILL.md "Integrity check" |
