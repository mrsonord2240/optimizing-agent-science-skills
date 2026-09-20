> **Audit record for `bio-alignment-sorting`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@cd9e0d2](https://github.com/mrsonord2240/bioSkills/tree/cd9e0d284852ed0c6989fedd401e74d00b863a51/alignment-files/alignment-sorting) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-20 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer - bio-alignment-sorting (RE-AUDIT of a fixed Skill)

Generated: 2026-09-20 | Source: `mrsonord2240/bioSkills@cd9e0d284852ed0c6989fedd401e74d00b863a51:alignment-files/alignment-sorting` (branch fix/af-sort, read from the worktree, copied into `run\skill\`; worktree and clone never written, no `__pycache__`) | Pre-fix: 76, Beta Only, not deployable (archived `_pre-fix-20260920\`).

Category: Data Analysis | Mode: B | Complexity: Moderate (rule gives N = 5) -> **N = 7 = 5 regression inputs from the first audit + 2 new inputs (6, 7)**.
Env: WSL `science`, env `alignment-files` (samtools 1.24, pysam 0.24.1, bwa 0.7.19, bcftools 1.24, Picard 3.5.0 side env, GATK 4.6.2.0, fgbio 4.1.1 side env, umi_tools 1.1.6, HTSeq 2.1.2). Every script that ran is in `run\` with its log (`log_*.txt`); the SKILL code blocks were extracted verbatim from the shipped SKILL.md (`run\extract_block.py`). Scratch `run\work\` (54 MB) deleted after the runs.

**Trap found while auditing:** `/mnt/openscience` is case-insensitive, so `n.bam` and `N.bam` are the same file. My first in02 run collapsed the -n/-N outputs into one file and gave a false result; every name-sort output now has distinct names (`*_nat`, `*_asc`). The fixer's log carries the same warning.

## Step 1 - Skill Veto: PASS
T1 Stability PASS (all code ran, failures were loud and deterministic) | T2 Contract PASS (frontmatter complete) | T3 Determinism PASS (record streams identical across `-@ 0/2/4/8`, spill, re-sort; BAM bytes differ only by `@PG CL`) | T4 Security PASS (no eval/exec, no credentials, script paths quoted, verified with spaces in paths).

## Step 2 - Static score: 86 / 100 (pre-fix 73)

| Category | Score | Note |
|---|---|---|
| Functional Suitability | 11/12 | coordinate, -n, -N, -t, template-coordinate, collate, merge, record check, downstream table, example. Picard row wording, CMCR row, -T wording |
| Reliability | 10/12 | example fail-loud, 8 verified Common Errors rows; failed run leaves a truncated BAM; check function errors on uBAM/CRAM |
| Performance/Context | 7/8 | SKILL 323 lines, usage-guide 65 lines, duplication gone |
| Agent Usability | 14/16 | tables with header lines, one rule paragraph for -n/-N |
| Human Usability | 6/8 | description omits merge/collate/verify |
| Security | 11/12 | THREADS unvalidated |
| Maintainability | 10/12 | roles separated; no shipped tests |
| Agent-Specific | 17/20 | idempotent, progressive; no hand-off |

## Step 4 - Inputs

```
Input 1 (Canonical)      : Coordinate-sort my shuffled BAMs, prove the order (not just the header), index, 8 threads / fixed memory / CRAM.        [regression + new text]
Input 2 (Variant A)      : Name sort + duplicate marking + paired FASTQ. Is sort -n lexicographic? What do I use for Picard?                       [regression + -n/-N]
Input 3 (Edge)           : Sort by cell barcode; BAM may be mislabelled/truncated/no @HD; tiny memory; template-coordinate for fgbio.           [regression]
Input 4 (Variant B)      : Merge per-lane BAMs: consistency check, dedup @RG/@PG, region merge, also the name-sorted versions.                  [regression]
Input 5 (Stress)         : Run the rewritten example, verify every downstream-table row with the real tools, threads/memory/-T/perf claims, judge the daggers. [regression + extension]
Input 6 (Adversarial)    : NEW  A collaborator sent BAM/CRAM files labelled SO:coordinate: verify at record level, incl. a ~1M-read file and planted defects; repair the bad ones.
Input 7 (Scope Boundary) : NEW  Align 2821 real pairs with the example script (plain/gz/spaces) and break it: partial index, unwritable output, unequal mates, empty FASTQ, bad threads.
```

## Summary table

| Input | Type | Basic /40 | Specialized /60 | Total | Assertions | Status |
|---|---|---|---|---|---|---|
| 1 | Canonical | 36 | 54 | 90 | 5/5 | ✅ executed |
| 2 | Variant A | 36 | 53 | 89 | 4/5 | ✅ executed |
| 3 | Edge | 35 | 52 | 87 | 5/5 | ✅ executed |
| 4 | Variant B | 35 | 53 | 88 | 5/5 | ✅ executed |
| 5 | Stress | 32 | 46 | 78 | 3/5 | ⚠️ executed (7 tools absent, not run) |
| 6 | Adversarial | 34 | 50 | 84 | 4/5 | ✅ executed |
| 7 | Scope Boundary | 35 | 52 | 87 | 3/4 | ✅ executed |

**Execution average 86.1** (L1 avg 34.7/40, L2 avg 51.4/60). **Assertion pass rate 29/34 = 85.3 %.**

## Detailed outputs

### Input 1 - Canonical (`in01_coordinate.sh`, `log_in01.txt`) - 20/20 checks
```
sorted.bam: coordinate_sorted=True, multiset md5 1267f5d9a548 == original sorted BAM; (contig,pos) sequence identical
sort --write-index -> wi.bam wi.bam.csi (no .bai); idxstats chr22 5642 mapped
-@ 8 -m 4G / -T /tmp/sort_tmp / -l 1 / -O bam: identical records; CRAM 5644 records, SO:coordinate, .crai
1000G 9601 records sorted+indexed; real UMI BAM (no @HD) sorted, indexes
SKILL 'Verify Records' block: sorted.bam indexable; shuffled: "Unsorted positions on sequence #1: 3489 followed by 3461"; umi_unsorted: "...3477 followed by 3470"
pysort.py (SKILL is_coordinate_sorted + ensure_coordinate_sorted verbatim): sorted True | shuffled False | ensure(liar) -> liar_fixed.bam, indexes
```
First-audit defect (ensure_coordinate_sorted returned a mislabelled BAM) is fixed.

### Input 2 - Variant A (`in02_namesort_dup.sh`, `log_in02.txt`) - 16/16 checks
```
-n : @HD SO:queryname SS:queryname:natural          half1 read1 read2 read3 ... read9 read10 ...
-N : @HD SO:queryname SS:queryname:lexicographical  half1 read1 read10 read100 read1000 read101 read11 ...
Picard SortSam queryname order == -N order; python natural-key sort == -n; python bytes sort == -N == Picard
Picard MarkDuplicates on planted -n : IllegalArgumentException "Alignments added out of order in SAMFileWriterImpl.addAlignment ... Sort order is queryname"
Picard MarkDuplicates on planted -N : READ_PAIR_DUPLICATES 50, 100 reads flagged
ValidateSamFile: -n RECORD_OUT_OF_ORDER 3 ; -N no ERROR lines (only the NM warning; no reference given)
Real BAMs (RNA, 1000G, human): -n order != -N order; Validate -n=RECORD_OUT_OF_ORDER, -N clean
Zero-padded names q001..q040 (natural==ASCII): Picard MarkDuplicates on -n output rc=0 (accepted)   <- table says "-n output is rejected"
collate / sort -n / sort -N pipelines: 100 dup reads each; real human 1656 == Picard 1656; FASTQ 250/250 names identical
```

### Input 3 - Edge (`in03_edge.sh`, `log_in03.txt`) - 11/11 checks
```
-t CB header SO:unsorted SS:unsorted:CB:coordinate; CB non-decreasing; position secondary; real UMI RX 15788/15788 ASCII non-decreasing
index errors: -t "NO_COOR reads not in a single block at the end"; -n/-N "Chromosome blocks not continuous" (all three also say 'cannot be indexed')
liar.bam: samtools index rejects, is_coordinate_sorted False, ensure -> re-sorted, indexes
contigswap.bam (chr2 block before chr1): samtools index WRITTEN (documented), is_coordinate_sorted False (old awk snippet's false pass is gone)
quickcheck: truncated rc 16, zero-byte rc 4 ; truncated input sort rc 1 "truncated file. Aborting" ; killed sort -> 0-byte file, quickcheck rc 4
-m 100K: "less than the minimum required (1M)" ; -m 1M spill "merging from 14 files" == in-memory sort ; temp files cleaned
template-coordinate on synthetic (no MC): "no MC tag. Please run samtools fixmate on file first." ; after fixmate -m: header SO:unsorted SS:unsorted:template-coordinate GO:query
```

### Input 4 - Variant B (`in04_merge.sh`, `log_in04.txt`) - 11/11 checks
```
consistency loop: 1 line consistent | 2 lines coordinate+name | 2 lines for -n + -N (SS: differs)
merge -c -p: 6144 records, 1 @RG ; RG collision: -c collapses L1/sampleA and L1/sampleB into one, B reads labelled L1 ; addreplacerg remedy -> 2 @RG
coordinate+name merge: rc 0, header SO:coordinate, coordinate_sorted=False, samtools index fails
merge -n / -N: qname_natural=True / qname_ascii=True, headers keep SS ; plain merge of name-sorted inputs: not name-ordered
Picard: RECORD_OUT_OF_ORDER on merge -n output, none on merge -N output
-R indexed: 3232 == sum of per-file counts ; unindexed: "Could not retrieve index file" rc 1 ; pysam.merge == CLI
```
(Merging the human BAM with the planted BAM gives Picard MATES_ARE_SAME_END errors because the two files share 200 read names; a property of my input choice, not of the Skill.)

### Input 5 - Stress (`in05a..f`, logs `log_in05*.txt`, `log_t_collate_tmpfs.txt`)
**5a rewritten example, clean copy, 100 real SARS-CoV-2 pairs**
```
no args rc 1 + usage ; no bwa index: "ERROR: no bwa index for ref.fa; run: bwa index ref.fa" rc 1, no output
after bwa index: PE rc 0, 200 records == raw bwa count, flagstat 200 primary, SO:coordinate, .bai ; SE rc 0, 100 records
missing R1 / R2 / ref: "ERROR: input not found: ..." rc 1, no BAM ; truncated gz: gzip error, rc 1
PATH-shim bwa exits 3 after 60 lines: script rc 3, no "Done" ; shim exit 0 after 60 lines: "quiet.bam has 57 primary records, expected 100 input reads" rc 1
SKILL Python snippet (extracted): CalledProcessError on bad input and on the shim crash
```
**5b downstream table (real tools):** index refuses name-sorted; fixmate takes -n and -N (100 dups each); markdup needs fixmate + coordinate (quoted messages); Picard -n dies, -N works (real human: 1656 == coordinate-input Picard); MarkDuplicatesSpark 100 dups on coordinate, -n and -N; bcftools "The input is not sorted (reads out of order)"; HaplotypeCaller and Mutect2 "some input files are not indexed"; umi_tools 15788 -> 5689 (needs index); fgbio GroupReadsByUmi 2823 MI groups for unsorted/coordinate/template-coordinate/name/fixmate input; HTSeq `-p` = `--samout-format`; DNA BAM one-gene GTF: `-r pos` 2820, name-sorted `-r name` 2820, coordinate `-r name` 5599 (SKILL numbers reproduce; GTF not stated in SKILL).
**5c/5d performance:** on WSL-native ext4 (`log_in05c_tmpfs.txt`): -l 0 50.7 MB (+3819 %, 39.2x) 0.22 s, -l 1 +5.8 % 0.26 s, -l 6 0.36 s, -l 9 -4.5 % 3.71 s (10.3x slower) - table holds. `t_collate_tmpfs.sh`: sort -n 0.66 s, collate 0.658 s (SKILL 0.66 / 0.74 reproduces). On the /mnt 9p mount collate is 3.2 s vs sort -n 0.77 s (temp files) and -l 0 is slower than -l 6 (I/O bound): the SKILL says nothing about the filesystem.
**5e threads/memory/-T:** peak threads 2/6/7/11 for `-@` 0/2/4/8 (SKILL "N+1 total" is looser than that); max RSS with `-m 20M`: 49 MB at `-@ 0`, 83 MB at `-@ 3` (about (N+1) x m plus ~30 MB base); spilled output == in-memory output; `-T tdir/pfx` gives `pfx.0007.bam` etc.; **`-T existing_dir` is used as a directory (`existing_dir/samtools.PID.tmp.NNNN.bam`), not as a prefix.**
**5f dagger rows:** `which`: featureCounts, salmon, RSEM, sniffles, cuteSV, manta, delly ABSENT (marking honest). **fgbio and gatk present**, so the footnote "tool not installed" is false for CallMolecularConsensusReads and Mutect2. Mutect2: coordinate+indexed rc 0, name-sorted and unindexed "not indexed" rc 2 (row verified). CallMolecularConsensusReads (fgbio 4.1.1): GroupReadsByUmi output as written and template-coordinate sorted -> 5646 consensus reads; **coordinate-sorted, `sort -t MI` and ungrouped input -> Fatal "not sorted correctly. Please sort with fgbio SortBam -s TemplateCoordinate"**. Row "grouped by MI tag" is incomplete. Verdict on the daggers: honest and sufficient for the seven absent tools; wrong for the two that could be run.

### Input 6 - Adversarial (NEW, `in06_record_order_check.sh`, `log_in06.txt`)
```
POSITIVES (real): 1000G, planted, human DNA, RNA (1786 supplementary), ARTIC nanopore, 3 SARS-CoV-2 -> 8/8 True (samtools index agrees on all)
NEGATIVES: shuffled x2, header liars x2, -n, -N, -t RX, template-coordinate, collate, swap at start / middle / end, mapped-after-unmapped,
           2-contig real-read file with chrB block first -> 14/14 False; the good 2-contig file True
           samtools index accepts the contig-swapped file (index-test = indexable); is_coordinate_sorted False
960,100 records: sorted True 1.9 s, 27 MB max RSS ; shuffled False ; one swap ~1000 records from the end False in 2.0 s ; samtools index 1.4 s
ensure_coordinate_sorted on all 15 files: 0 failures (result passes check and indexes)
LIMITS: unaligned BAM -> ValueError "file has no sequences defined (mode='rb')"; CRAM without reference -> OSError "truncated file" (True once REF_PATH cache holds the M5 sequence)
```

### Input 7 - Scope Boundary (NEW, `in07_pipeline_real_hostile.sh`, `log_in07.txt`) - 14/14 checks
```
2821 real pairs from the nf-core human BAM (samtools collate | fastq), reference = human genome.fasta slice, bwa index
plain FASTQ paired -t 4 : rc 0, 5644 records of which primary (-F 0x900) 5642 == 2 x 2821 (script check does not false-alarm on the 2 supplementary lines)
gz == plain (cols 1-11 identical) ; SE 2821 primary ; spaces in every path rc 0 ; re-run over existing output identical, quickcheck ok
partial index (.sa removed): bwa "fail to open file .sa" rc 1, no Done ; unwritable output dir rc 1 ; unequal R1/R2 "2nd file has fewer sequences" rc 1
empty FASTQ rc 0, 0 records ; trailing blank line rc 0 ; all-N read and zero-length read rc 0 with right counts
THREADS "abc": rc 0, correct output (bwa tolerates it; script never validates)   SE + threads needs `"" 3`; `ref r1 out 3` fails loudly ("input not found: 3")
after a count-check or crash failure the truncated BAM (57 records) stays at OUTPUT
```

## Assertions (34): 29 PASS / 5 FAIL
FAIL: Picard wording accurate in all cases (2); dagger footnote true for every daggered row (5); CMCR row usable (5); check function handles uBAM/CRAM (6); no misleading output left after a failed run (7). No safety or scope assertion failed.

## Research Veto (category 3): PASS
M1 PASS (all re-run numbers/messages reproduced) | M2 PASS (file utility) | M3 PASS (rule verified; incomplete CMCR row fails loudly) | M4 PASS (all code ran; limits raise, they do not mislead).

## Step 8 - Final
```
Static 86 x 0.4 = 34.4 | Execution 86.1 x 0.6 = 51.7 | FINAL = 86.1 -> 86  (pre-fix 76)
Floors for Production Ready: static >= 80 OK | exec >= 85 OK | L1 34.7 >= 32 OK | L2 51.4 >= 48 OK | assertions 85.3 % >= 90 % NOT MET
=> downgraded one tier: GRADE ✅ Limited Release (floors for Limited: static>=70, exec>=75, L1>=28, L2>=42, assertions>=80 % all met). Deployable: true. Veto: none. Open P0: 0. Open P1: 1.
```

**What the fix broke:** nothing found. The -n/-N table, header lines, merge -n/-N, pipefail snippet, record-level check and rewritten example all held. New inaccuracies introduced by the fix are wording-level only (dagger footnote, Picard "-n rejected", "-T not a directory", "N+1 threads").

**Regression status of first-audit findings:** -n natural vs -N (P1) fixed and verified; example bwa index / pipefail / fail-loud (P1) fixed and verified; header trust / awk snippet / contig order (P1) fixed and verified; merge omissions, perf numbers, `-T`, `-m` floor, HTSeq `-p`, template-coordinate, `--write-index`, dedup (P2) fixed (residual wording gaps below); Input-5 unverified rows: hedged with daggers (7 honest, 2 wrong).

**Recommendations**
- [P1] Dagger footnote false for Mutect2 and fgbio CMCR; CMCR row must say template-coordinate (Input 5).
- [P2] Picard "-n output is rejected" only when natural and ASCII order differ (Input 2).
- [P2] `is_coordinate_sorted`: `check_sq=False` for uBAM, note CRAM needs a reference (Input 6).
- [P2] Failed `sort_pipeline.sh` run leaves a truncated BAM; THREADS unvalidated (Inputs 5, 7).
- [P2] `-T existing_dir` behaviour, threads "N+1", filesystem dependence of collate/-l 0 timings, HTSeq 2820/5599 conditions (Input 5).
- [P2] Description omits merge, collate and record verification.

Not verified here (no tool installed): featureCounts (`-p` and sort order), Salmon, RSEM, Sniffles, cuteSV, Manta, Delly. Their dagger rows are hedged correctly; I did not check them against documentation either.
