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
