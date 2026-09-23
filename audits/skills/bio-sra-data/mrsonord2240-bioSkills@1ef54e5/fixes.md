# bio-sra-data fixes (2026-09-17)

Worktree `F:\OpenScience\wt\db-sra`, branch `fix/db-sra`, based on staging `main` @
`581dcd89a7450785c2451a0543ee822049fbf934`. Fixer: Claude Opus 5 (1M context). Runtime: native
Windows `curl` 8.19.0, `bash` 5.3.9 (Cygwin, via the harness's Bash tool), and the shared
`pysradb` 2.5.1 (`F:\OpenScience\audit-envs\database-access\Scripts\python.exe`, no version
change). No installs. Verification scripts: scratchpad `test_ena_single.sh`/`test_batch.sh`
(deleted after confirming, since the same fix landed in the shipped files).

| finding | priority | change | verified (ran / help / docs) | notes |
|---|---|---|---|---|
| ENA-mirror off-by-one column bug: SKILL.md's "preferred default" snippet and `examples/download_batch.sh` both assumed `fields=fastq_ftp,fastq_md5` maps to columns 1,2; ENA always prepends `run_accession` as column 1, so real data is at 2,3 (2,3,4 for the batch script's extra `read_count`). Failed 100% of the time (4/4 real accessions) as shipped. | P0 | Both files: replaced the fixed `cut -f1`/`cut -f2` index with a header-based lookup (`tr '\t' '\n' \| grep -nx '<field>' \| cut -d: -f1`) that finds the right column by its documented ENA field name instead of a position, so it stays correct even if ENA reorders or adds columns | ran | Live ENA portal API, real accessions: single-accession fix on ERR10419835 and SRR12345678 both downloaded both mates with MD5 matching ENA's declared checksums exactly (URLs: `https://ftp.sra.ebi.ac.uk/vol1/fastq/ERR104/035/ERR10419835/ERR10419835_{1,2}.fastq.gz`, `https://ftp.sra.ebi.ac.uk/vol1/fastq/SRR123/078/SRR12345678/SRR12345678_{1,2}.fastq.gz`); batch fix run against the shipped `examples/download_batch.sh` on the auditor's exact 3-accession list (ERR10419835, ERR10419931, ERR10419946) reached 3/3 OK, MD5-verified, matching the auditor's own one-line-fix result |
| No dbGaP / controlled-access guidance anywhere (grep-confirmed absent); an agent would attempt a controlled-access human accession the same way as a public one | P0 | Added a "Controlled-access (dbGaP) data" section to SKILL.md (after the decision matrix, before the accession-hierarchy table): how to recognize a controlled-access accession, why this unauthenticated Skill is out of scope for it, the `--ngc <repository-key>.ngc` prefetch mechanism, and an explicit stop-and-ask-the-user boundary before any human accession not already known-public. Added matching Common-errors row (authorization error / omitted `fastq_ftp` -> stop, don't retry as network issue) | docs | No controlled-access data was or should be accessed to verify this (per the brief); text checked against the mechanism NCBI documents for dbGaP SRA access (`--ngc` repository-key flag) |
| `pigz` called with no Windows fallback in `download_single.sh`, `download_batch.sh`(N/A, no pigz call)/`prefetch_large.sh` and 3 SKILL.md code patterns; no official pigz build exists for Windows | P1 | Added `command -v pigz \|\| gzip` fallback in `download_single.sh`, `prefetch_large.sh`, and the 3 pigz call sites in SKILL.md's code patterns; documented the gap once in the "fasterq-dump vs fastq-dump" section instead of repeating the explanation at each call site | ran (`bash -n` on both changed `.sh` files) + docs (no official pigz Windows build, confirmed via `TOOLS.md`'s tooling pass and absence from PATH here) | `gzip` confirmed present via Git-for-Windows (`/usr/bin/gzip`) |
| ENA mirror and SRA-direct presented as freely interchangeable for "the same" run; real read-count discrepancy (13,911 vs 14,052 pairs on ERR10419835) | P1 | Added a note under "ENA mirror: direct FASTQ URLs" that the two archives can legitimately disagree on read count (ENA re-calls from BAM/CRAM) and that a pipeline should validate each source against its own metadata, not the other's | docs | Cited the audit's own independently cross-checked numbers (`TOOLS.md`'s ENA-vs-SRA-direct real finding); not re-run (would require the full FASTQ pull the audit already did) |
| SKILL.md tells users to check size with `pysradb metadata` first; audit's `TOOLS.md` claimed pysradb's detailed metadata "has no byte-size column" | P1 | **Corrected the audit's own claim rather than repeating it.** Split the `--max-size` size-check guidance into two paths that were being conflated: `prefetch --max-size` governs the `.sra` file (SRA-toolkit path) and `pysradb`'s `total_size` column *is* a usable, accurate proxy for it; ENA's `fastq_bytes` governs the FASTQ download (ENA-mirror path) and is what a user on that path should check instead. SKILL.md now names the right field for the right path instead of asserting pysradb has "no byte-size column" | ran | Live, cross-checked against real files, not just column names: (1) `pysradb.SRAweb().sra_metadata('PRJEB37378', detailed=True)` on real accession ERR10419835 -> `total_size=1,744,967`, `public_size=1,040,291` (both columns 6,508/6,508 populated, not sparse); (2) a real `prefetch ERR10419835 --max-size 100G` run (native `sratoolkit.3.4.1-win64\bin\prefetch.exe`) -> actual downloaded/verified `.sra` size **1,742,656 bytes** ("1758833 bytes were streamed from 1742656"); `total_size` matches this to within 0.13%, confirming it tracks `.sra` size, not FASTQ size. (3) ENA `fastq_bytes` on the same accession -> `1,090,725;1,125,857` (sum 2,216,582), a different, larger number -- confirming the two fields answer different questions and neither is simply "missing" as the audit's `TOOLS.md` claimed |
| No confirmation step before large downloads | P2 | Added one sentence to the `--max-size` section: state expected size and get explicit confirmation before any download above ~10 GB, using the same `fastq_bytes`/`run_total_bases` check just documented | docs | Directly composes with the P1 fix above; no new mechanism needed |

All 6 dispatched findings fixed (2 P0, 3 P1, 1 P2). Nothing left unfixed. Nothing needs Sam.

## Redundancy pass (2026-09-17)

Scope: `SKILL.md` and `usage-guide.md`, per the brief's "Remove redundancy, every pass" rule (the
audit did not flag duplication directly, but the rule is unconditional).

**Deleted passage -> new home** (checked present at destination before commit):

| Deleted from usage-guide.md | New home | Note |
|---|---|---|
| "Prerequisites" `conda install sra-tools` / `pip install pysradb` / `fasterq-dump --version` block | Pointer to SKILL.md's "Required Setup" (already there, identical) | |
| "Prerequisites" one-liner "For AWS STRIDES, install aws-cli and run from EC2 in us-east-1 for free egress" | SKILL.md's "Required Setup" STRIDES paragraph -- the "install aws-cli" instruction was the one fact not already in SKILL.md (which only showed an `aws s3 ls` example), so it was added there rather than dropped; the "run in the bucket's region for free egress" half was already covered by SKILL.md's Cloud (STRIDES) access section | genuinely new fact moved, not deleted |
| "What the Agent Will Do" 8-step list | SKILL.md's decision matrix, `--max-size` section, fasterq-dump section, 10x section, Cloud (STRIDES) access, and Failure modes (all already there) | Replaced with a one-line pointer naming those sections, matching the pattern used for the STRIDES/business-hours items |
| Tips bullets 1-5, 7-9 (ENA default, `--max-size` trap, scratch overhead, `--include-technical`, STRIDES egress, Aspera dates, vdb-config persistence, NCBI Datasets CLI scope) | SKILL.md's ENA mirror section, `--max-size` section, fasterq-dump section, 10x section, Cloud (STRIDES) access, Decision matrix, Failure modes ("vdb-config not persisted"), and Related Skills (already there, same content) | Verbatim or near-verbatim restatements; no new fact |
| Tips bullet 6 ("For finding accessions: efetch ... pysradb's metadata is more ergonomic") | SKILL.md's SRA-accession-hierarchy "Conversion is via..." line (already states both paths) | Same content, no new fact -- the "more ergonomic" opinion was not load-bearing |
| Related Skills line `read-alignment/bwa-alignment` (present only in usage-guide.md, missing from SKILL.md -- itself a drift bug) | Added to SKILL.md's own Related Skills list | Fixed the inconsistency between the two lists rather than deleting the fact |

Untouched: "Overview", "Quick Start", "Example Prompts" -- the brief's allowed usage-guide.md
categories; no agent-facing SKILL.md restatement found in them. `usage-guide.md`: 82 -> 54 lines.
`SKILL.md`: 372 -> 417 lines (net +45: two P0 sections, three P1 notes/fixes, one P2 sentence, one
Related-Skills line, minus nothing removed since SKILL.md had no internal duplication to collapse).

Shipped `examples/` scripts are out of the redundancy rule (a runnable file beside an inline
SKILL.md block is not a duplicate) -- `download_batch.sh`, `download_single.sh` and
`prefetch_large.sh` were fixed in place for the same bugs their SKILL.md counterparts had;
`find_sra_runs.py` was untouched (no defect; not exercised by any P0/P1/P2 finding).

# bio-sra-data fixes (2026-09-18) -- second fix round

Worktree `F:\OpenScience\wt\db-sra2`, branch `fix/db-sra2`, based on staging `main` @ `1f07281`.
Fixer: Claude Sonnet 5. Current score going in: 82, Limited Release (deployable, no open P0).
Findings from `audits/BACKLOG.md`; a third listed finding ("No Skill change needed", auditor
methodology note) was out of scope and is not addressed here.

| finding | priority | change | verified | notes |
|---|---|---|---|---|
| Header-based ENA column lookup (correctly fixed in the 2026-09-17 round to be name-based, not positional) fails ungracefully when the requested field is genuinely absent -- inline SKILL.md snippet has no `set -e`/guard so it silently prints a false "md5 OK" with zero files downloaded; `download_batch.sh`'s `set -euo pipefail` plus `grep -nx`'s non-match exit status aborts the ENTIRE batch before the script's own pre-existing `if [ -z "${URLS}" ]` guard is ever reached | P1 | Added `set -euo pipefail` to the SKILL.md inline snippet (it had none) and, in both the SKILL.md snippet and `download_batch.sh`, changed `FTP_COL=$(...)`/`MD5_COL=$(...)` to `... || true` (so a `grep -nx` non-match no longer trips `set -e` via the pipefail-propagated exit status) followed by an explicit `if [ -z "${FTP_COL}" ] || [ -z "${MD5_COL}" ]` check right after: the SKILL.md snippet (single accession) prints the message to stderr and `exit 1`; `download_batch.sh` prints it, records the accession to `failed.txt`, and `continue`s to the next accession | ran | Built a synthetic ENA-response fixture (a real 4-column TSV header/row with `fastq_ftp` entirely stripped, matching how ENA actually omits it for controlled-access runs) and a fake `curl` serving it plus two good fixtures, in scratchpad. Pre-fix (git HEAD): inline snippet on the bad fixture -> `cut: option requires an argument`, `md5 OK`, exit 0, **zero files written** (the exact false-positive named in the finding); `download_batch.sh` on a 3-accession batch (good, bad, good) -> aborted at the bad accession, exit 1, third accession never attempted. Post-fix: inline snippet on the bad fixture -> prints the accession-attributed message, exit 1, no files; `download_batch.sh` on the same 3-accession batch -> skips only the bad accession, finishes `OK: 2/3`, both good accessions' files present and MD5-verified. `bash -n` passed on both changed `.sh` files |
| dbGaP boundary (SKILL.md's own "Controlled-access (dbGaP) data" section) is advisory text only -- no shipped script detects or names an absent `fastq_ftp` as that signal, so the code silently swallows the exact condition the prose describes | P1 | Once the guard above exists, pointed its message directly at the section: `"fastq_ftp not found in ENA response for $ACC -- may indicate controlled-access (dbGaP) data, see SKILL.md 'Controlled-access (dbGaP) data' section"` (accession-attributed via `${SRR}`/`${ACC}`), in both files | ran | Same fixture run as above -- the message actually prints for the missing-field case in both the inline snippet and the batch script, naming the section by its exact heading text |

Both dispatched findings fixed (2/2 P1). Nothing left unfixed. Nothing needs Sam.

Redundancy check: re-read `usage-guide.md` against the current `SKILL.md` -- still clean from the
2026-09-17 pass (overview/quick-start/example-prompts/related-skills only, with a pointer to
SKILL.md's decision-matrix/`--max-size`/dbGaP/failure-modes sections for agent-facing detail). No
new duplication introduced by this round's two-line guard, since it lives once in SKILL.md's inline
snippet and once in `download_batch.sh` (a shipped script, exempt from the redundancy rule as a
runnable file beside an inline block). `download_single.sh` and `prefetch_large.sh` were not
touched -- neither does ENA column lookup, so the finding doesn't apply to them.

Commit: `086e443` on `fix/db-sra2`.


## 2026-09-21 -- P2 batch (fix/database-access-sra-data, from staging 431aa55)

Audit: `eval_report_bio-sra-data_result.json`, 1 P2. Env: `database-access` (pysradb 2.5.1, curl, bash; the audit's fake-curl fixtures copied to scratchpad). Commits: `cc3e896` fix, `07df97a` + `1ef54e5` redundancy, `6b6bbb0` scripts.

| finding | priority | change | verified (ran / help / docs) | notes |
| --- | --- | --- | --- | --- |
| ENA guard prints "fastq_ftp not found" even when `fastq_md5` is the missing column | P2 | Message built from whichever of `FTP_COL`/`MD5_COL` is empty (both named when both are); dbGaP hint reworded to "a missing fastq_ftp may indicate controlled-access". Applied to the SKILL.md inline block and `examples/download_batch.sh` | ran: fixtures CONTROLLEDTEST1 (ftp absent -> "fastq_ftp"), CONTROLLEDTEST2 (md5 absent -> "fastq_md5"), EMPTYRESP1 (-> "fastq_ftp, fastq_md5"), each exit 1 with zero files; live ERR10419835 md5 OK on both mates; mixed batch [CONTROLLEDTEST2, ERR10419835, CONTROLLEDTEST1] -> OK 1/3, both bad accessions in failed.txt | the inline block was later replaced by a pointer to the example (see scripts table) |

Redundancy pass: `usage-guide.md` already held only overview/prompts/related Skills (its one stale section name, "Failure modes", was repointed to "Common errors"). Inside SKILL.md, a disagreement was resolved: the trap paragraph says ~3x scratch plus ~3x output; the failure mode said "4-5x compressed size". Kept the trap paragraph's figures.

### Deleted passage -> new home

| deleted | new home |
| --- | --- |
| Code pattern "prefetch + fasterq-dump" (25 lines) | `examples/download_single.sh` (pointer line) |
| Code pattern "Cloud (STRIDES) via AWS" and "10x single-cell with technical reads" | `examples/prefetch_large.sh` (4th arg `yes` = `--include-technical`); pointer section "Cloud (STRIDES) and 10x single-cell" |
| Code pattern "Single SRR via ENA mirror" (44 lines) | `examples/download_batch.sh` with a one-line accessions file (pointer + failed.txt caveat) |
| Code pattern "Batch via pysradb metadata" (30 lines) | `scripts/pysradb_resolve.py` |
| Failure mode prefetch --max-size silent skip | "prefetch and the --max-size trap" section + Common errors row (now carries the fix) |
| Failure mode scratch exhaustion | uncompressed-scratch trap paragraph (now also names `fastq-dump --gzip` and the "out of disk space" symptom) + Common errors row |
| Failure mode 10x technical reads missing | "Single-cell / 10x quirks" (now names the R2-only / CellRanger symptom) + Common errors row |
| Failure mode SRA-direct slowness | Common errors row (business-hours detail, run off-peak) |
| Failure mode Aspera deprecation | decision matrix row + new Common errors row |
| Failure mode cloud egress | Required Setup sentence + Common errors row |
| Failure mode vdb-config not persisted | Common errors row (persist `user-settings.mkfg`, or `--temp`/`-O`) |
| Required Setup `aws s3 ls` block | Cloud (STRIDES) access section |
| "Ignore SKILL.md's own older claim that this column doesn't exist" | deleted (stale self-reference; the total_size fact stays) |

### Runnable code moved to scripts/

| old location | new |
| --- | --- |
| SKILL.md "Batch via pysradb metadata" | `scripts/pysradb_resolve.py` (functions verbatim, plus a CLI entry). Ran: `GSE110009` -> 74 SRRs, `ERR10419835` -> 1; `batch_resolve(['ERR10419835','NOTREAL1'])` -> 1-row frame with `total_size` |
| SKILL.md ENA single-run block | not a script: duplicated `examples/download_batch.sh`, so deleted and pointed there. Ran the exact pointer command on live ERR10419835: OK 1/1, both md5 OK |

SKILL.md 426 -> 249 lines; under 300, so no `references/` split.

### Left unfixed

None; all 1 P2 fixed.

### Noticed, not changed

- `examples/download_batch.sh` exits 0 even when accessions fail (only `failed.txt` and the summary say so). Caveat now stated in SKILL.md; the script's behaviour is unchanged.
