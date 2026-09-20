# Fix log: bio-duplicate-handling (alignment-files/duplicate-handling)

## 2026-09-20 (branch `fix/af-dup`, worktree `F:\OpenScience\wt\af-dup`, from staging main 85a3e4d)

First audit: 77, Limited Release, deployable, 26/32 assertions, no veto/P0. Fixer pass clears every P1/P2 in the report
(3 P1 + 4 P2 = 7/7) and the tool mentions that had no runnable code. Not re-scored here.

Tool versions used (WSL `science`): samtools 1.24, pysam 0.24.1, Picard 3.5.0, fgbio 4.1.1, umi_tools 1.1.6, samblaster 0.1.26,
sambamba 1.0.1, mapDamage 2.2.2, bwa-mem2 2.3. New: biobambam2 2.0.185 and pbmarkdup 1.2.0 in a **new own env**
`af-dup-extra` (`/home/sci/micromamba/envs/af-dup-extra`; `micromamba create`, nothing existing touched; not in TOOLS.md, that
file is outside my write scope). Data: `planted_dups.bam` (truth 100 reads = 50 pairs), `test.paired_end.sorted.bam`
(1656 flagged), `test.paired_end.umi_unsorted.bam` (real UMI BAM), `HG00349` 1000G slice (101 pre-flagged), synthetic
20-clone HiFi set (below). Scratch: `/home/sci/dupfix` (WSL), audit data copied read-only.

| finding | priority | change | verified | notes |
| --- | --- | --- | --- | --- |
| Duplex consensus crashes after adjacency grouping | P1 | UMI section split into two branches: adjacency -> `CallMolecularConsensusReads`; `--strategy=paired` -> `CallDuplexConsensusReads`; decision-table ctDNA row names `--strategy=paired`; MQ prerequisite (`fixmate -m` or `SetMateInformation`) stated; consensus reads are unmapped (re-align) | ran the literal SKILL.md block: consensus 5646, duplex 4042, `MI /A\|/B` on 15766/15766 grouped-paired records; adjacency->duplex still throws `StringIndexOutOfBoundsException` (reproduced); consensus BAM has 0 mapped reads | audit note (TOOLS #6) says fixmate -m output fails GroupReadsByUmi; on 4.1.1 it works (fixmate -m adds MQ: 9 of 15788 reads lack MQ afterwards vs 15788 before; both routes give 15766 records / 2823 MI groups) |
| umi_tools example omits sort/index and `--paired` | P1 | New "umi_tools dedup" subsection: sorted+indexed input, `--paired`, separate bulk-paired command with `sort`+`index`, scRNA tag pre-check (`grep -c CB:Z:`) and `test count > 0` guard | ran literal block: unsorted -> `fetch called on bamfile without index`; sorted, no `--paired` -> 2805; `--paired` -> 5689; scRNA block on a BAM without CB/UB writes 0 records and the guard returns 1 | `--per-cell` with absent tags still exits 0 in umi_tools itself; the guard is in the block |
| Optimized pipeline fails from clean dir and hides it | P1 | Pipeline block: `set -euo pipefail`, `mkdir -p tmpdir`, record-count/non-empty assertion. `examples/markdup_pipeline.sh` rewritten: `pipefail`, `mktemp -d` + trap, `-d` (env `OPTICAL_DIST`, default 2500) and `--use-read-groups`, stats beside the output (`<out>.markdup_stats.txt`, not cwd), output written to temp then `mv`, record-count assertion (exit 3), >50% duplicates warning, assay gate | SKILL.md block run literally from a clean dir: planted 100, human 1656, indexed; without the mkdir line now exit 1 (was 0); example: planted 100 / human 1656, missing input exit 1 with no out.bam left, empty input exit 3, ASSAY unset/rnaseq exit 2, amplicon BAM -> 1980/2000 + warning, BAM without @RG still 100 | the leftover 501-byte marked.bam in the SKILL.md block (no temp-then-mv there) is covered by the Common Errors line "delete the partial output" |
| Common Errors table and pitfall do not match 1.24 | P2 | Table replaced with verbatim samtools 1.24 messages (4 samtools + collate tmpdir + fgbio MQ + umi_tools index + Picard @RG NPE); pitfall no longer claims silent under-marking | each message reproduced from a run: `no ms score tag`, `no MC tag` (MC stripped via pysam), `Coordinate sorted, require grouped/sorted by queryname`, `queryname sorted, must be sorted by coordinate`, `Cannot open intermediate file "tmpdir/collate.0000.bam"`, fgbio MQ (audit log), Picard NPE | "mate not found" / "not coordinate sorted" deleted (not emitted by 1.24) |
| No guidance on `-c` or read groups for Picard | P2 | `-c` paragraph after the pitfall; `bwa-mem2 mem -R '@RG...'` in the samblaster example; Picard/@RG line in Common Errors | 1000G slice: 101 pre-flagged -> no `-c` 111, `-c` 101, Picard 101; Picard on BAM without @RG -> NPE; bwa-mem2 `-R` -> `@RG` present, Picard ran, metrics for `lib1` | |
| usage-guide repeats SKILL.md and contradicts it | P2 | usage-guide cut to overview/prereqs/prompts/what-agent-does; NextSeq/HiSeq `-d` contradiction gone (SKILL.md table is the only copy); rate denominator unified to primary alignments (`-F 2304`) in the bash formula and pysam snippet; unsupported "`-@ 8` fixes high memory" tip deleted (replaced with a `-T PREFIX` note) | bash formula and pysam snippet both give 29.35% on the human BAM (samtools primary-only check 29.3512); 20.00% on planted | see "Deleted passages" |
| Workflow steps do not gate on assay | P2 | Step 0 in the workflow "Approach" and in usage-guide "What the Agent Will Do"; example script refuses NO assays and requires `ASSAY=` | example run: exit 2 for unset and `rnaseq`; amplicon BAM under `wgs` warns at 99% | |
| (own finding) Named tools with no runnable code | P2, "Missing referenced executables" | Runnable blocks written for `biobambam2 bammarkduplicates2`, `sambamba markdup`, `pbmarkdup`, `mapDamage --rescale`, Picard `UmiAwareMarkDuplicatesWithMateCigar` (chose "write it": all installable or installed). Checked-on versions line added | biobambam2: planted 100 flagged, Picard-style metrics READ_PAIR_DUPLICATES 50, human 1656; sambamba: 100 and 1656; pbmarkdup (synthetic 50 HiFi reads, 10 planted duplicates, as unaligned PacBio BAM and FASTQ): 10/50 flagged, `--rmdup` 40, `--dup-file` 10; mapDamage on the human BAM: `in.rescaled.bam` written, 5644 records = input; Picard UmiAware on the UMI BAM: 10127 flagged (samtools `--barcode-tag RX` 9879, umi_tools removed 10099) | pbmarkdup writes uncompressed text for `.fq.gz`/`.fastq.gz` outputs (not documented in the Skill); BAM path used in the doc |

Also collapsed inside SKILL.md (each fact once): the second `-d` example under "samtools markdup", the standalone
"Multi-threaded" markdup block, the "Count Duplicates" block, and the whole "Quick Reference" table (all restated blocks
already in the file); "Filter Commands" now holds the count commands too.

## Deleted passages and where the content lives now

| deleted | now |
| --- | --- |
| usage-guide "The Standard Workflow" diagram | SKILL.md "Duplicate Marking Workflow" |
| usage-guide "Common Commands" (step-by-step, pipeline, mark vs remove, statistics, optical `-d 100/2500`, rate) | SKILL.md workflow, "samtools markdup", "Optical Distance Is Platform-Specific" (the `-d` matrix; the guide's "NextSeq -d 2500 / HiSeq 100" line lost, table wins), "Duplicate Statistics" |
| usage-guide "Python with pysam" (`mark_duplicates`, `duplicate_rate`, `remove_duplicates`) | SKILL.md "pysam Python Alternative" (same three operations; the rate snippet now skips secondary/supplementary like the deleted `duplicate_rate`) |
| usage-guide "Expected Duplicate Rates" incl. "high rate suggests low complexity / over-amplification / low input" | SKILL.md decision table (per-assay rates); the causes moved to "Percentage Duplicates" |
| usage-guide "Troubleshooting" (mate not found, no MC tag, not coordinate sorted, high memory) | SKILL.md "Common Errors" (verbatim messages); high-memory tip deleted as unsupported (maxRSS rose 7.4 -> 13.8 MB with `-@ 8`), `-T PREFIX` note instead |
| usage-guide "Tips" (7 bullets) | already in SKILL.md: full workflow, RNA-seq no-remove, `-m` essential, `-d 2500`, keep marked BAM ("Lossy Operations"), samblaster ("Alternative: From Aligner") |
| SKILL.md "Optical Duplicate Distance" and "Multi-threaded" (markdup) subsections | one-line pointer under "Write Stats to File" -> optical section / pipeline |
| SKILL.md "Count Duplicates" block | "Filter Commands" |
| SKILL.md "Quick Reference" table | "samtools markdup", "Duplicate Statistics", "Filter Commands" |
| SKILL.md Common Errors rows `mate not found`, `no MC tag` (for missing -m), `not coordinate sorted` | replaced by the verbatim-message rows |
| SKILL.md fgbio block `AnnotateBamWithUmis -> GroupReadsByUmi --strategy=adjacency -> duplex` | split into the single-strand and duplex branches; `AnnotateBamWithUmis` kept as the optional first step |

## Findings left unfixed

- `macs3 --keep-dup auto` (ChIP row) and the ATAC Tn5 +4/-5 shift: pointers to a downstream peak-calling/footprinting
  step of other Skills, not duplicate-handling routines; macs3 is not installed. Left as prose pointers.
- "~30% faster than `sort -n | fixmate | sort | markdup`" and biobambam2 "Fastest": unmeasured claims the audit also
  listed as not verified; my toy inputs cannot time them. Left as is.
- Real Cell Ranger CB/UB umi_tools dedup: no such data on the machine. The block is the tag-guarded original plus the
  index requirement (checked on the RX BAM with CB/UB deliberately absent).
- PacBio-specific pbmarkdup was run on synthetic HiFi-style reads only, no real HiFi amplicon BAM available.
- `TOOLS.md` in the alignment-files env does not list `af-dup-extra`; outside my write scope.
