# bio-local-blast fix log

2026-09-24. Final-pass correction for `database-access/local-blast`, branch
`agent/final-pass-bio-local-blast-20260924`, commit
`95cc27bafcad6395ddac4c678b3224d951ff86f6`, based on staging `main`
`9bcf426`. The prior re-audit correctly found that the first taxonomy fix had
introduced a P2 documentation error. This pass is directed rather than
independent (`auditor_independent: false`).

| finding | priority | change | verified | notes |
| --- | --- | --- | --- | --- |
| v4 was incorrectly described as unable to store per-sequence taxids | P2 | Corrected the v4/v5 table and all matching prose: v4 can retain `-taxid`/`-taxid_map` assignments and report `staxids`, but only v5 supports `-taxids`/`-taxidlist` filtering. Updated the shipped `run_blast.sh` comment too. | ran | Built a v4 protein DB with `-taxid_map`; `blastp` returned `9606` and `7227` in `staxids`. |
| v4 filtering behavior was conflated with the v5-without-taxonomy-data no-op | P2 | Split the failure mode and common-errors rows. The v5 missing-`taxdb.tar.gz` case remains an exit-0, unfiltered result; the v4 case now directs rebuild-as-v5 and names its loud nonzero error. | ran | With `taxdb.bti`, `taxdb.btd`, and `taxonomy4blast.sqlite3` present, a v4 `-taxidlist` query exited 2 with `Taxonomy filtering is not supported in v4 BLAST dbs` and wrote no result rows. |

Regression evidence: reran archived Inputs 1-8 with BLAST+ 2.17.0+ (custom v5 DB/search, dc-megablast, v5 taxonomy no-op then recovery, short primers, RBH extraction, clinical scope boundary, thread/hitlist behavior, and v4 taxid-map behavior); Input 9's stale runner referenced a deleted worktree, so its shipped-means-present checks were rerun directly against this worktree. The bundled `blast_wrapper.py` also passed against real BLAST+ output. Two fresh current-source checks covered the v4 hard-error path with all taxonomy data installed and the corrected docs/examples/link surface.

2026-09-17. Fixer for `database-access/local-blast`, branch `fix/db-blast` off staging `main` at
`581dcd89a7450785c2451a0543ee822049fbf934`. Audit: `F:\OpenScience\audits\bio-local-blast\`
(87/100, Limited Release, deployable, one open P0). BLAST+ version invoked throughout: 2.17.0+
(`F:\OpenScience\audit-envs\database-access\tools\blast\ncbi-blast-2.17.0+\bin\`).

| finding | priority | change | verified | notes |
| --- | --- | --- | --- | --- |
| `-taxids`/`-taxidlist` silently no-op without `taxdb.tar.gz` | P0 | Rewrote "Database format: v5 vs v4" (SKILL.md): dropped the false "v5 needs no companion file" claim, added the `taxdb.tar.gz` fetch command, the auto-fetched ~98MB `taxonomy4blast.sqlite3` note, and a "detect the no-op by row count, not exit code" instruction. Reconciled the "v4 database" Failure-mode section and the Common-errors table row to name the same cause. Fixed the same false claim repeated in `examples/create_database.sh`'s echo text. | ran | Reproduced the auditor's exact result independently: built a v5 DB with `-taxid_map` (2 sequences, human/fly-tagged), ran `-taxidlist human_only.txt` -> printed `requires additional data files`, exit 0, still 2 rows (fly hit not excluded). Downloaded `taxdb.tar.gz` (65MB) from `https://ftp.ncbi.nlm.nih.gov/blast/db/taxdb.tar.gz`, extracted, reran the same command -> 1 row, `sscinames` resolved to `Homo sapiens`, fly hit correctly excluded. `taxonomy4blast.sqlite3` (98.5MB) auto-fetched by blastp during the retry, confirmed present on disk. |
| No escape hatch for diagnostic/clinical misuse | P1 | Added a "Practice boundaries" section to SKILL.md (after the tool/Python line, before Installation): local BLAST reports similarity not diagnosis; route diagnostic/treatment questions to a clinical genetics workflow. | docs | New guidance, not a runnable command; matches the Skill's existing short-paragraph voice (cf. the "biggest mistakes" intro paragraph). |
| "Taxonomy filter no-op" troubleshooting row gave an incomplete fix | P1 | Same edit as the P0 row above — the Common-errors table row and the Failure-modes section both now name `taxdb.tar.gz` alongside v4-vs-v5, so "Upgrade to v5" is no longer presented as sufficient on its own. | ran | Verified by the same before/after row-count test above (v5 DB alone did not fix it; `taxdb.tar.gz` did). |
| RBH pattern doesn't show blastdbcmd extraction chaining | P2 | Added 4 lines after SKILL.md's RBH `awk` pattern: which `rbh.tsv` column is a species-B vs species-A accession, and the two `blastdbcmd -entry_batch` calls to extract each side. | ran | Reproduced SKILL.md's own RBH awk pattern on `species_A.fasta`/`species_B.fasta` (6 pairs incl. the planted paralog trap), confirmed column 1 = B accessions (6/6 extracted from `B_db`), column 2 = A accessions (6/6 extracted from `A_db`). |
| BLAST `-out` files are CRLF on Windows, pipelines emit LF | P2 | Added a Common-errors table row: normalize with `tr -d '\r'` before diffing/scripting against a raw `-out` file. | ran | Confirmed `blastp -out unfiltered.tsv` on the Windows native `.exe` is CRLF-terminated (`file` + a Python byte-count check: 2/2 lines CRLF, 0 LF-only). |

## Redundancy pass

`usage-guide.md`'s "Tips" section (6 bullets) restated SKILL.md content verbatim or near-verbatim.
Deleted the whole section and replaced it with a one-line pointer into SKILL.md, per the
every-fact-once rule (applies regardless of audit findings).

- "Soft masking (default) is correct..." -> already in SKILL.md's "Soft vs hard masking" section (untouched). Deleted, no move needed.
- "`pident` in `-outfmt 6` is identity over the HSP..." -> already in SKILL.md's "Output format reference" -> "Field key fields for analysis". Deleted, no move needed.
- "Build databases with `-blastdb_version 5` so `-taxids` works. v4 databases require `taxonomy4blast.sqlite3`..." -> superseded by the corrected "Database format: v5 vs v4" section (this was itself part of the same false-claim pattern as the P0). Deleted.
- "For >100K query batches, DIAMOND... MMseqs2..." -> duplicate of both SKILL.md's "Thread scaling" section and usage-guide's own "Prerequisites" paragraph (line 15, kept — it serves the human-picking-a-skill purpose, a different audience than the Tips list). Deleted from Tips only.
- "Reciprocal best hit (RBH)... mis-pairs paralogs; use OrthoFinder or OMA" -> already in SKILL.md's RBH code-pattern caveat. Deleted, no move needed.
- "For very large database downloads, run `update_blastdb.pl --decompress` overnight" -> unique content (agent-actionable, not previously in SKILL.md). Moved into SKILL.md's "Prebuilt NCBI databases" section, appended after the sizes list.
- "The BLAST+ Bio.Blast.Applications wrappers were deprecated in BioPython 1.85..." -> the version number (1.85) was unique content not in SKILL.md (SKILL.md only said "deprecated and removed"). Moved into SKILL.md's tool-list line: `... deprecated and removed in BioPython 1.85 -- do not use`.

## Left unfixed

None of the five findings were left unfixed. Everything else in the audit (dc-megablast vs
megablast, blastn-short, thread capping, the bundled `blast_wrapper.py`) reproduced exactly as
documented and was left byte-identical, per the audit's own "leave alone" list.
