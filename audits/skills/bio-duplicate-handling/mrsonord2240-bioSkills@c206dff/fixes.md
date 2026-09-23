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

## 2026-09-21 (branch `fix/alignment-files-duplicate-handling`, worktree `F:\OpenScience\wt\alignment-files-duplicate-handling`, from staging main 431aa55)

Production Ready batch: the 5 open P2s from the re-audit, then the split and the `scripts/` move. Commits: 535e20f (fix),
9be7866 (split), 8573e10 (scripts), 9480764 (one duplicate sentence). Not re-scored here. Tools (WSL `science`): samtools 1.24,
pysam 0.24.1, umi_tools 1.1.6, fgbio 4.1.1. Data: audit-env `planted_dups.bam` (truth 100 reads), `test.paired_end.sorted.bam`,
`test.paired_end.umi_unsorted.bam`, `test.rna.paired_end.sorted.bam`, 1000G slice. Fixed 5/5.

| finding | priority | change | verified | notes |
| --- | --- | --- | --- | --- |
| Unmeasured "~30% faster" / biobambam2 "Fastest" | P2 | percentage and "Fastest" deleted; the audit's measured run (800k reads, 4 threads, 6.4 s vs 4.6 s, plain chain faster) stated instead, no 30x claim | audit input 9 timing log (3 reps, equal flagged counts); I did not re-time | biobambam2 speed cell now "Fast" |
| umi_tools counts vary by 1 without `--random-seed` | P2 | `--random-seed=1` in both umi_tools invocations (now in `scripts/umi_tools_dedup.sh`), sentence saying the unseeded count moves by ~1 | ran: seeded 5689 x4, unseeded 5688 in 1 of 6 runs (audit: 3 of 6) | 5689 vs 2805 figures kept |
| `--strategy=paired` input requirement not stated | P2 | duplex text now says RX must be `UMI1-UMI2` and single-UMI libraries use the adjacency branch | ran: single-UMI RX -> `IllegalArgumentException: Paired strategy used but umi did not contain 2 segments`; adjacency + `CallMolecularConsensusReads` on it -> 5626 records; dash RX + paired -> 15766 grouped | |
| Assay gate relies on the declared `ASSAY` | P2 | `examples/markdup_pipeline.sh` also refuses (exit 2) a BAM with STAR/HISAT2 in `@PG` or >1% N-CIGARs in the first 100000 records; `ALLOW_SPLICED=1` overrides; flagged percentage always printed | ran: real RNA-seq BAM under `ASSAY=wgs` exit 2 (805 of 8828 spliced, @PG STAR); with `@PG` stripped still exit 2 by CIGARs; `ALLOW_SPLICED=1` exit 0, 2570 flagged; human 1656 (29.35%), planted 100 (20.00%), 1000G 111 unchanged; rnaseq exit 2, missing input exit 1, empty input exit 3 | SKILL.md Approach line mentions the second check |
| Description omits assay/UMI caveat | P2 | clause "Not for RNA-seq, amplicon or UMI libraries (see the decision table)" | read | |
| (structural) SKILL.md 423 lines | split rule | `references/umi-dedup.md`, `references/alternative-markers.md`, `references/pysam.md` (verbatim), Reference Files index, decision-table pointers. **423 -> 297 lines**, 291 after scripts | every non-blank original line present in SKILL.md or a reference (only the 5 pointer-bearing table rows differ); fences balanced; 23 bash blocks `bash -n`, 3 python `ast.parse` | usage-guide pointer updated |
| (structural) runnable code to `scripts/` | Sam 2026-09-21 | see table below | each script run from the Skill dir as the docs invoke it: pysam_markdup planted 100 / human 1656, dup_rate 29.35% (equals samtools `-F 2304`) and 20.00%, umi bulk-paired 5689, scrna without CB exit 2 and with synthetic CB/UB 698 records, fgbio single 5646 / duplex 4042 (0 mapped), bad mode exit 1 | scRNA branch tested on synthetic CB/UB tags only (no real 10x BAM) |

Redundancy pass: done 2026-09-20 (usage-guide is overview/prompts/what-the-agent-does, pointing at SKILL.md). This pass only
collapsed one repeat: the example script's command line, given in both the workflow Approach and Pipeline Version.

## Code moved to `scripts/` (old location -> script)

| old location | now |
| --- | --- |
| references/pysam.md "Full Pipeline" (was SKILL.md pysam section) | `scripts/pysam_markdup.py` (args in/out, temp dir, record-count check) |
| references/pysam.md "Check Duplicate Flag" | `scripts/dup_rate.py` (arg BAM; guards zero primary reads) |
| references/umi-dedup.md umi_tools scRNA and bulk-paired blocks | `scripts/umi_tools_dedup.sh scrna\|bulk-paired in out` (CB pre-check now exits 2; bulk sorts/indexes a temp copy) |
| references/umi-dedup.md fgbio single-strand and duplex blocks | `scripts/fgbio_consensus.sh single\|duplex in out` (fixmate -m, grouping strategy chosen by mode; comments on the crash and the `A-B` requirement kept in header and reference) |
| SKILL.md "Pipeline Version (Optimized)" (17-line copy of the example) | deleted; 4-stage pipe fragment kept, pointer to `examples/markdup_pipeline.sh` (pipefail, tmp dir, index and record-count check live there) |

Left inline (under ~15 lines): pysam filter-out-duplicates, Picard UmiAware, samblaster/Picard/biobambam2/sambamba/mapDamage/pbmarkdup blocks, samtools one-liners.

## Deleted passages -> new home (this pass)

| deleted | now |
| --- | --- |
| "~30% faster ... on typical 30x WGS" | replaced by the measured 800k-read result in "Pipeline Version" |
| SKILL.md "Pipeline Version" full block (set -euo pipefail, mkdir tmpdir, index, sanity test) | `examples/markdup_pipeline.sh` (same checks) |
| SKILL.md sections UMI-Aware Deduplication, Alternative: From Aligner, pysam Full Pipeline/Check/Filter | `references/umi-dedup.md`, `references/alternative-markers.md`, `references/pysam.md` (stubs and Reference Files index remain) |

## Findings left unfixed

None of the 5 P2s. Carried over from 2026-09-20 and still true: macs3 `--keep-dup auto` and the ATAC Tn5 shift are pointers to other
Skills (audit confirmed the macs3 pointer is valid); no real Cell Ranger CB/UB BAM or real HiFi amplicon BAM on the machine;
`af-dup-extra` is not in `TOOLS.md` (outside my write scope; the coordinator recorded it as note 19). Also seen, not fixed: on a
missing input the example leaves an empty `<out>.markdup_stats.txt` (samtools markdup opens it before the pipe fails); the BAM
itself is not written.

## 2026-09-21 final pass, Phase 1 (branch `fix/alignment-files-duplicate-handling`, same worktree, commit 2d29a1e)

Combined fixer+auditor final pass (`FINAL_PASS_BRIEF.md`). Walked every runnable block in `SKILL.md`, `references/*.md`,
`scripts/*` and `examples/markdup_pipeline.sh` on the audit env's data (WSL `science`, env `alignment-files` + side envs
`af-picard3`, `af-fgbio2`, `af-mapdamage`, `af-dup-extra`), not just what earlier passes touched.

| finding | priority | change | verified | notes |
| --- | --- | --- | --- | --- |
| Missing/empty input leaves an empty `<out>.markdup_stats.txt` (seen, not fixed, 2026-09-20) | P2 | `examples/markdup_pipeline.sh`: `-f` stats now written to `$TMP/markdup_stats.txt` and `mv`d beside `$OUTPUT` only after the record-count check passes, same pattern already used for `marked.bam` | missing input and a 0-byte input now leave neither `out.bam` nor `out.markdup_stats.txt` (previously an empty stats file was left); full assay-gate suite re-run after the change (rnaseq/no-ASSAY refusal, wgs on planted_dups.bam 100/500=20.00%, real spliced RNA-seq BAM refused then `ALLOW_SPLICED=1`->2570/7042=36.50%, 1000G slice 111/9595=1.16%) all still pass, stats file present on every success path | commit 2d29a1e |
| scRNA `umi_tools dedup` claim only had synthetic CB/UB data behind it | resolved, no code change | streamed a real region (`1:1000000-1300000`) of the public 10x `pbmc_1k_v3` `possorted_genome_bam.bam` via `samtools view` HTTP range access (its `.bai` is public, no auth) instead of downloading the 4.7 GB file | 11845 records, 11588 with `CB:Z:`, 11838 with `UB:Z:`; `scripts/umi_tools_dedup.sh scrna` on it: 11845 -> 9798 (257 reads skipped for missing tags, tool's own warning) | no Skill text changed; this backs the existing claim with real data instead of only the synthetic substitute |

Re-verified without changes needed (matches every previously logged figure, run fresh this pass): SKILL.md 5-step reference
pipeline (100/500), all fixmate/markdup variants (basic, `-r`, `-s`, `-f`, `--use-read-groups`), Duplicate Statistics/Filter
Commands, all three Common Errors messages, `references/pysam.md` filter snippet (500->400), `scripts/pysam_markdup.py` +
`scripts/dup_rate.py` (100/20.00%), `scripts/umi_tools_dedup.sh bulk-paired` (5689) and `scripts/fgbio_consensus.sh single`/`duplex`
(5646/4042), `references/alternative-markers.md` biobambam2 (100, READ_PAIR_DUPLICATES 50), sambamba (100), samblaster (redone with
separated stdout/stderr this time: "50 of 250 read ids" = 100), Picard UmiAware (10127), and `mapDamage` (no `--rescale`, stats/plots
only, on the human BAM: completed in ~5 min, wrote `misincorporation.txt`/`Fragmisincorporation_plot.pdf` etc. — confirms the
2026-09-20 `--rescale` run's environment still works).

### Still blocked (checkpoint, needs Sam's decision)

- **PacBio HiFi amplicon `pbmarkdup`**: still only verified on the synthetic 50-read HiFi-style BAM/FASTQ from 2026-09-20 (10/50
  planted duplicates recovered). No real public HiFi amplicon BAM/FASTQ on this machine; searched PacBio's own `pbmarkdup` and
  `pbAA` GitHub repos this pass (both closed-source, no test data shipped) and found nothing small enough to fetch. Needs a small
  (<50 MB) public HiFi amplicon BAM or FASTQ. Everything else about the Skill's `pbmarkdup` row is otherwise ready.
- macs3/ATAC Tn5 shift, `af-dup-extra`/`TOOLS.md`, and the speed claims are no longer open items (see checkpoint file for why).

Full detail: `F:\OpenScience\audits\_final_pass\bio-duplicate-handling\CHECKPOINT.md`.
