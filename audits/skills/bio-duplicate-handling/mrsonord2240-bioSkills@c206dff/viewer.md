> **Audit record for `bio-duplicate-handling`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@c206dff](https://github.com/mrsonord2240/bioSkills/tree/c206dff76d081a5126f8497fbabe10995c9b6026/alignment-files/duplicate-handling) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-20 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer - bio-duplicate-handling
Generated: 2026-09-20  |  Source: `mrsonord2240/bioSkills@c206dff76d081a5126f8497fbabe10995c9b6026:alignment-files/duplicate-handling`  |  Category: Data Analysis  |  Mode: B  |  Complexity: Complex (N=7)

**Final: 77 / 100 - ✅ Limited Release - deployable: true - veto: none**  (static 73 x 0.4 = 29.2; execution avg 79.1 x 0.6 = 47.5)

Executed 7/7 inputs. 7/7 inputs executed. Not executed (no tool/data): biobambam2 bammarkduplicates2, pbmarkdup, mapDamage --rescale row, macs3 --keep-dup, ATAC Tn5 shift, real Cell Ranger CB/UB umi_tools dedup, Picard UmiAwareMarkDuplicatesWithMateCigar (help only; class exists, marked EXPERIMENTAL).

Complexity rationale: several task types (mark, remove, optical, multi-library, UMI, assay decision, pysam) and branching by assay/platform, so Complex -> 7 inputs, although the Skill has only one usage-guide and one example.

## Step 1 - Skill Veto
Stability PASS (shipped example and every SKILL.md pipeline run; failures are loud or documented below), Contract PASS (name + description frontmatter), Determinism PASS (identical outputs on re-runs), Security PASS (no eval/exec, no credentials).

## Step 2 - Static (25 criteria)

| Category | Score | Note |
|---|---|---|
| functional_suitability | 9/12 | Completeness 3, Correctness 2, Appropriateness 4. Core mark/remove/stats/optical/multi-library/assay workflow verified by output; UMI duplex step, umi_tools prerequisites, error-string table and the 'silently marks nothing' pitfall are wrong |
| reliability | 7/12 | Fault tolerance 2, error reporting 2, recoverability 3. Optimized pipeline and shipped example have no pipefail/mkdir; error table paraphrases do not match the tool; default is mark-not-remove with a lossy-operation warning |
| performance_context | 5/8 | Token cost 2 (372-line SKILL.md plus a usage-guide that repeats most of it), execution efficiency 3 |
| agent_usability | 11/16 | Learnability 3, consistency 2 (usage-guide vs SKILL.md disagree on -d for NextSeq/HiSeq X and on rate denominators), feedback design 3, error prevention 3 (strong assay table; misses tmpdir, -c, RG for Picard, --paired) |
| human_usability | 6/8 | Discoverability 3 (description omits assay/UMI caveats), forgiveness 3 (accepts any-order input by name-sorting first) |
| security | 11/12 | No credentials or eval; example quotes its variables; lossy -r is flagged; example writes markdup_stats.txt to cwd |
| maintainability | 8/12 | Modularity 3, modifiability 2 (facts duplicated between SKILL.md and usage-guide), testability 3 (counts verifiable, one example, no test data) |
| agent_specific | 16/20 | Trigger 3, progressive disclosure 3, composability 4 (Related Skills all exist), idempotency 3 (re-mark without -c inflates), escape hatches 3 (assay table says NO for RNA/amplicon/UMI; workflow steps do not gate) |

**Static subtotal: 73 / 100**

Gate 8 (shipped means present): SKILL.md/usage-guide point only at `examples/markdup_pipeline.sh` (present) and Related Skills that all exist (alignment-sorting, alignment-filtering, alignment-amplicon-clipping, bam-statistics, variant-calling/variant-calling, read-qc/quality-reports). No missing primary file.

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Executed | Status |
|---|---|---|---|---|---|---|---|
| 1 | Canonical | 36 | 55 | 91 | 5/5 PASS | true | ✅ |
| 2 | Variant A | 30 | 44 | 74 | 3/4 PASS | true | ⚠️ |
| 3 | Edge | 32 | 44 | 76 | 3/5 PASS | true | ✅ |
| 4 | Variant B | 36 | 53 | 89 | 4/4 PASS | true | ✅ |
| 5 | Stress | 32 | 45 | 77 | 4/5 PASS | true | ✅ |
| 6 | Scope Boundary | 34 | 52 | 86 | 4/4 PASS | true | ✅ |
| 7 | Adversarial | 27 | 34 | 61 | 3/5 PASS | true | ⚠️ |

**Execution Average: 79.1 / 100**  |  Layer 1 avg 32.4/40, Layer 2 avg 46.7/60  |  **Assertion Pass Rate: 26/32**

Floors for Limited Release (static >= 70, exec >= 75, L1 >= 28, L2 >= 42, assertions >= 80%): all met (73, 79.1, 32.4, 46.7, 81.3%). Not met for Production Ready (static < 80, exec < 85, L2 < 48, assertions < 90%).

## Detailed Outputs

### Input 1 - Canonical: Standard fixmate-markdup workflow, count vs planted truth and 3 independent tools
**Prompt:** I have paired-end Illumina alignments (coordinate sorted). Mark the PCR duplicates with the standard fixmate/markdup workflow, index the result, and tell me how many reads were flagged and the duplicate rate.

**Executed:** true - in01_canonical.sh -> in01.log; planted_dups.bam and test.paired_end.sorted.bam, samtools 1.24, Picard 3.5.0, sambamba 1.0.1, samblaster 0.1.26

**Scripts:** `run/in01_canonical.sh`

**Output (`run/in01.log`, trimmed):**
```
samtools 1.24
Version:3.5.0
=========== planted_dups
[check] input records: 500  marked records: 500
[check] dup flag (0x400) reads: 100
[check] pct (SKILL.md formula):
20.00
[check] flagstat dup lines:
100 + 0 duplicates
100 + 0 primary duplicates
[check] markdup -s stats (SKILL.md 'Output Statistics'):
COMMAND: samtools markdup -s coordsort.bam marked_s.bam
READ: 500
WRITTEN: 500
EXCLUDED: 0
EXAMINED: 500
PAIRED: 500
SINGLE: 0
DUPLICATE PAIR: 100
DUPLICATE SINGLE: 0
DUPLICATE PAIR OPTICAL: 0
DUPLICATE SINGLE OPTICAL: 0
DUPLICATE NON PRIMARY: 0
DUPLICATE NON PRIMARY OPTICAL: 0
DUPLICATE PRIMARY TOTAL: 100
DUPLICATE TOTAL: 100
ESTIMATED_LIBRARY_SIZE: 538
[check] -r removal:
records after -r: 400
[check] nodup view -F 1024 count: 400
[picard] metrics:
LIBRARY	UNPAIRED_READS_EXAMINED	READ_PAIRS_EXAMINED	SECONDARY_OR_SUPPLEMENTARY_RDS	UNMAPPED_READS	UNPAIRED_READ_DUPLICATES	READ_PAIR_DUPLICATES	READ_PAIR_OPTICAL_DUPLICATES	PERCENT_DUPLICATION
testN	0	250	0	0	0	50	0	0.2
[picard] flagged reads: 100
[sambamba] flagged reads: 100
[samblaster] flagged reads: 100
samblaster: Outputting to stdout
samblaster: Loaded 1 header sequence entries.
samblaster: Marked          50 of        250 (20.000%) total read ids as duplicates using 4156k memory in 0.000S CPU seconds and 1S wall time.
[check] samtools vs picard flagged read (name,flag) set differences: 200
=========== test.paired_end.sorted
[check] input records: 5644  marked records: 5644
[check] dup flag (0x400) reads: 1656
[check] pct (SKILL.md formula):
29.34
... (33 more lines trimmed; full log in run/in01.log)
```

**Result:** SKILL.md steps 1-5 verbatim: planted BAM 100/100 flagged; real human BAM 1656 flagged, identical read set to Picard

**Scores:** Basic 36/40 | Specialized 55/60 | Total 91/100

**Assertions:**
- [PASS] samtools markdup after the SKILL.md workflow flags exactly the 100 planted duplicate reads - view -c -f 1024 = 100; flagstat '100 + 0 duplicates'; -s stats DUPLICATE PAIR 100 (truth: 50 pairs)
- [PASS] Independent tools agree: Picard 50 pairs (=100 reads), sambamba 100, samblaster 100 flagged - Picard READ_PAIR_DUPLICATES 50; samtools vs Picard flag different member of each identical pair (tie), counts equal
- [PASS] On the real human BAM samtools markdup and Picard flag the identical read set - 1656 flagged by samtools, Picard, sambamba, samblaster; (name,flag) set difference 0
- [PASS] -r removal returns total minus flagged and the marked output is indexed - 500->400 and 5644->3988 records; marked.bam.bai written
- [PASS] SKILL.md percentage one-liner agrees with flagstat / Picard PERCENT_DUPLICATION - 20.00% (100/500); 29.34% vs Picard 0.2936 (2 secondary + 2 unmapped in denominator)

### Input 2 - Variant A: Optimized piped workflow + optical distance on a NovaSeq-style request
**Prompt:** This is a NovaSeq 6000 WGS run. Give me the fast piped duplicate-marking command with 4 threads, optical duplicates at the right distance, per-read-group handling and a stats file, then tell me how many duplicates are optical vs PCR.

**Executed:** true - in02_pipeline_optical.sh -> in02.log; synth_optical.bam is SYNTHETIC (00_make_synth.py). Note: -d on the real BAM (names testN:n) only prints 'cannot decipher read name' warnings, flags unchanged (1656)

**Scripts:** `run/in02_pipeline_optical.sh`, `run/00_make_synth.py`

**Output (`run/in02.log`, trimmed):**
```
### 2a. pipeline verbatim, tmpdir does NOT exist beforehand
[E::hts_open_format] Failed to open file "tmpdir/collate.0000.bam" : No such file or directory
samtools collate: Cannot open intermediate file "tmpdir/collate.0000.bam": No such file or directory
pipeline exit codes: 1 0 0 0
-rw-r--r-- 1 sci sci 677 Sep 20 04:09 markdup_stats.txt
-rw-r--r-- 1 sci sci 501 Sep 20 04:09 marked.bam
### 2b. same, after mkdir tmpdir
[bam_sort_core] merging from 0 files and 4 in-memory blocks...
samtools markdup: warning, 10 decipher read name warnings.  New warnings will not be reported.
samtools markdup: warning, number of failed attempts to get coordinates from read names = 200
pipeline exit codes: 0 0 0 0
[check] dup flag reads: 100 (truth 100)
COMMAND: samtools markdup -@ 4 -d 2500 --use-read-groups -f markdup_stats.txt - marked.bam
READ: 500
WRITTEN: 500
EXCLUDED: 0
EXAMINED: 500
PAIRED: 500
SINGLE: 0
DUPLICATE PAIR: 100
DUPLICATE SINGLE: 0
DUPLICATE PAIR OPTICAL: 0
DUPLICATE SINGLE OPTICAL: 0
DUPLICATE NON PRIMARY: 0
DUPLICATE NON PRIMARY OPTICAL: 0
DUPLICATE PRIMARY TOTAL: 100
DUPLICATE TOTAL: 100
ESTIMATED_LIBRARY_SIZE: 538
READ GROUP: 1
READ: 500
WRITTEN: 500
EXCLUDED: 0
EXAMINED: 500
PAIRED: 500
SINGLE: 0
DUPLICATE PAIR: 100
DUPLICATE SINGLE: 0
DUPLICATE PAIR OPTICAL: 0
DUPLICATE SINGLE OPTICAL: 0
DUPLICATE NON PRIMARY: 0
DUPLICATE NON PRIMARY OPTICAL: 0
DUPLICATE PRIMARY TOTAL: 100
DUPLICATE TOTAL: 100
ESTIMATED_LIBRARY_SIZE: 538
[check] SKILL.md dt-tag counting one-liner:
... (17 more lines trimmed; full log in run/in02.log)
```

**Result:** Verbatim 'Pipeline Version (Optimized)' fails from a clean directory (tmpdir/ not created), pipeline exit 0, 501-byte empty BAM; works after mkdir; optical logic correct

**Scores:** Basic 30/40 | Specialized 44/60 | Total 74/100

**Assertions:**
- [FAIL] The verbatim optimized pipeline runs from a clean working directory - samtools collate: Cannot open intermediate file tmpdir/collate.0000.bam; downstream stages exit 0 and write an empty 501-byte marked.bam (per-stage exit codes 1 0 0 0, no pipefail)
- [PASS] After creating tmpdir the pipeline flags exactly the planted 100 reads - 100 flagged; stats file has ALL block + 'READ GROUP: 1' block, DUPLICATE TOTAL 100
- [PASS] Optical claims hold: -d 0 emits no dt tag, -d emits dt:Z:SQ/LB, counts match Picard - synthetic Illumina names, truth 4 dup pairs: samtools OPTICAL reads 0/2/4 at -d 0/100/2500 = Picard optical pairs 0/1/2; dt tags 4 SQ + 4 LB at 2500; -t adds 'do' tag
- [PASS] -f stats file and --use-read-groups are accepted by the installed samtools and do not change the flagged count - samtools 1.24 markdup --help lists both; 100 flagged

### Input 3 - Edge: Wrong-order pipelines and the Common Errors / Critical pitfall text
**Prompt:** samtools markdup errors out or marks nothing on my BAM and I'm not sure of the sort order I used. What is wrong, how do I fix it, and can I drop secondary/unmapped reads with fixmate on the way?

**Executed:** true - in03_edge_wrong_order.sh, in03b_fixmate_r.sh, 03_strip_tags.py -> in03.log, in03b.log. Side finding: re-marking an already-flagged BAM without -c gave 111 flagged vs 101 with -c and Picard (1000G slice); SKILL.md never mentions -c

**Scripts:** `run/in03_edge_wrong_order.sh`, `run/in03b_fixmate_r.sh`, `run/03_strip_tags.py`

**Output (`run/in03.log`, trimmed):**
```
### 3a. markdup on raw coordinate-sorted BAM (no fixmate at all)
samtools markdup: error, no ms score tag. Please run samtools fixmate on file first.
samtools markdup: error, no ms score tag. Please run samtools fixmate on file first.
   -> exit=1  output_exists=yes  dup_flagged=0
### 3b. fixmate WITHOUT -m, then coordinate sort, then markdup
samtools markdup: error, no ms score tag. Please run samtools fixmate on file first.
samtools markdup: error, no ms score tag. Please run samtools fixmate on file first.
   -> exit=1  output_exists=yes  dup_flagged=0
### 3c. fixmate -m on COORDINATE-sorted input (skipped the name sort)
[bam_mating_core] ERROR: Coordinate sorted, require grouped/sorted by queryname.
   -> exit=1  output_exists=yes  dup_flagged=NA
### 3d. fixmate -m ok, but skip the coordinate re-sort (markdup on name-sorted)
samtools markdup: error, queryname sorted, must be sorted by coordinate.
   -> exit=1  output_exists=yes  dup_flagged=NA
### 3e. tags lost in a Python round-trip: strip ms,MC from a correct fixmate -m + coordinate-sorted BAM
stripped ['ms', 'MC'] from 500 records -> cs_strip.bam
samtools markdup: error, no MC tag. Please run samtools fixmate on file first.
samtools markdup: error, unable to assign pair hash key.
   -> exit=1  output_exists=yes  dup_flagged=0
   strip only MC:
stripped ['MC'] from 500 records -> cs_mc.bam
samtools markdup: error, no MC tag. Please run samtools fixmate on file first.
samtools markdup: error, unable to assign pair hash key.
   -> exit=1  output_exists=yes  dup_flagged=0
   strip only ms:
stripped ['ms'] from 500 records -> cs_ms.bam
samtools markdup: error, no ms score tag. Please run samtools fixmate on file first.
samtools markdup: error, no ms score tag. Please run samtools fixmate on file first.
   -> exit=1  output_exists=yes  dup_flagged=0
### 3f. correct pipeline control
   -> exit=0  output_exists=yes  dup_flagged=100
### 3g. re-run markdup on already-marked output (idempotency) and -c clearing
   -> exit=0  output_exists=yes  dup_flagged=100
   -> exit=0  output_exists=yes  dup_flagged=100
### 3h. pre-marked real BAM (1000G HG00349 slice: 101 pre-flagged dups): re-mark without and with -c
   preflagged: 101
   markdup (no -c): 111
   markdup -c    : 101
   picard        : 101  (IWG_IND-TG.HG00349-5_1pA	4759	50)
   supplementary/secondary in slice: 0; with -S: 112
```

**Output (`run/in03b.log`, trimmed):**
```
input: 5644 records; secondary 2; unmapped 2
fixmate -r -m output: 5640 records; secondary 0; unmapped 0
EXCLUDED: 0
EXAMINED: 5640
DUPLICATE TOTAL: 1656
flagged: 1656  (without -r: 1656)
{
    "COMMAND": "samtools markdup --json fr.cs.bam j.bam",
    "READ": 5640,
    "WRITTEN": 5640,
    "EXCLUDED": 0,
```

**Result:** All prerequisites correct (ms+MC tags, name-sort before fixmate, coord-sort before markdup) but the documented error strings and the 'silently marks almost nothing' pitfall do not match samtools 1.24

**Scores:** Basic 32/40 | Specialized 44/60 | Total 76/100

**Assertions:**
- [PASS] Stated prerequisites are correct: fixmate -m needs name-grouped input, markdup needs ms+MC tags and coordinate order - each violation stops the tool: no ms score tag / no MC tag / queryname sorted, must be sorted by coordinate / fixmate 'Coordinate sorted, require grouped/sorted by queryname'
- [FAIL] Documented Common Errors strings match the real messages - table says 'mate not found', 'no MC tag' (for missing -m) and 'not coordinate sorted'; real: 'Coordinate sorted, require grouped/sorted by queryname', 'no ms score tag', 'queryname sorted, must be sorted by coordinate'
- [FAIL] Critical pitfall 'lost tags silently produce a markdup output that marks almost nothing' is accurate - stripping ms and/or MC makes samtools 1.24 exit 1 with an error (output left with 0 flagged); not silent
- [PASS] Wrong-order pipelines never yield a silently wrong duplicate count - every wrong order (3a-3e) exits 1 with dup_flagged 0; correct order control flags 100
- [PASS] fixmate -r -m removes secondary and unmapped reads as claimed - 5644 -> 5640 records, 0 secondary, 0 unmapped; markdup still flags 1656

### Input 4 - Variant B: pysam alternative for the workflow and duplicate rate
**Prompt:** Do the duplicate marking in Python with pysam instead of the shell, filter out the duplicates, and give me the duplicate rate.

**Executed:** true - in04_pysam.py -> in04.log; pysam 0.24.1 (embeds samtools 1.24)

**Scripts:** `run/in04_pysam.py`

**Output (`run/in04.log`, trimmed):**
```
[E::hts_open_format] Failed to open file "nope.bam" : No such file or directory
pysam 0.24.1 samtools 1.24
===== planted_dups: truth flagged reads = 100
Total: 500
Duplicates: 100
Rate: 20.00%
ASSERT PASS SKILL.md pysam pipeline flags 100 reads == truth 100
ASSERT PASS pysam.index wrote marked.bam.bai
ASSERT PASS pysam count == samtools view -c -f 1024
ASSERT PASS SKILL.md filter keeps 400 == total-dups 400
ASSERT PASS usage-guide mark_duplicates() flags truth
ASSERT PASS mark_duplicates() cleaned its temp files
usage-guide duplicate_rate: {'total': 500, 'duplicates': 100, 'rate': 20.0}
ASSERT PASS duplicate_rate total 500 == primary count 500
ASSERT PASS remove_duplicates output == samtools view -F 1024
SKILL.md rate (all records): 20.00%  usage-guide rate (primary only): 20.00%
===== test.paired_end.sorted: truth flagged reads = 1656
Total: 5644
Duplicates: 1656
Rate: 29.34%
ASSERT PASS SKILL.md pysam pipeline flags 1656 reads == truth 1656
ASSERT PASS pysam.index wrote marked.bam.bai
ASSERT PASS pysam count == samtools view -c -f 1024
ASSERT PASS SKILL.md filter keeps 3988 == total-dups 3988
ASSERT PASS usage-guide mark_duplicates() flags truth
ASSERT PASS mark_duplicates() cleaned its temp files
usage-guide duplicate_rate: {'total': 5642, 'duplicates': 1656, 'rate': 29.3512938674229}
ASSERT PASS duplicate_rate total 5642 == primary count 5642
ASSERT PASS remove_duplicates output == samtools view -F 1024
SKILL.md rate (all records): 29.34%  usage-guide rate (primary only): 29.35%
===== failure behaviour: pysam.markdup on coordinate-sorted input without fixmate
ASSERT PASS raised SamtoolsError : 'samtools returned with error 1: stdout=, stderr=samtools markdup: error, no ms score tag. Please run samtools fixmate o
===== failure behaviour: mark_duplicates() on a missing input
ASSERT PASS raised SamtoolsError : 'samtools returned with error 1: stdout=, stderr=samtools sort: can\'t open "nope.bam": No such file
===== pysam.markdup return value on success (stderr/-s stats capture)
pysam.markdup('-s',...) returned: None
```

**Result:** All SKILL.md and usage-guide pysam snippets run verbatim and match samtools counts; only the rate denominators differ between the two documents

**Scores:** Basic 36/40 | Specialized 53/60 | Total 89/100

**Assertions:**
- [PASS] SKILL.md pysam pipeline (sort -n, fixmate -m, sort, markdup, index) flags the truth counts - 100/100 planted and 1656/1656 real; marked.bam.bai written
- [PASS] usage-guide mark_duplicates() flags truth and cleans its temp files - 100 and 1656 flagged, no temp_* left
- [PASS] Python errors surface as exceptions with tool stderr, not silent output - SamtoolsError on markdup without ms tag and on missing input
- [PASS] The 'production tools, not hand-rolled' warning is present and the filter/rate helpers are consistent with samtools - remove_duplicates == view -F 1024; duplicate_rate total == primary count (5642). SKILL.md rate counts all records (29.34%) vs usage-guide primary-only (29.35%): trivial

### Input 5 - Stress: Shipped example, usage-guide pipelines, failure exits, aligner+samblaster alternative
**Prompt:** Use the shipped markdup_pipeline.sh (and the usage-guide pipeline) on my BAM, and also show me how to mark duplicates inline during alignment with bwa-mem2 and samblaster.

**Executed:** true - in05_shipped_example.sh, in05b_aligner_alternatives.sh -> in05.log, in05b.log. Not executed: biobambam2 bammarkduplicates2, pbmarkdup (not installed). Side findings: usage-guide 'markdup -@ 8 reduces high memory' unsupported (maxRSS 7.4 MB at -@0 vs 13.8 MB at -@8, tiny input); picard MarkDuplicates NullPointerException on a BAM without @RG

**Scripts:** `run/in05_shipped_example.sh`, `run/in05b_aligner_alternatives.sh`

**Output (`run/in05.log`, trimmed):**
```
bash -n: syntax OK
### 5a. example on planted_dups.bam (truth 100)
WRITTEN: 500
EXCLUDED: 0
EXAMINED: 500
PAIRED: 500
SINGLE: 0
DUPLICATE PAIR: 100
DUPLICATE SINGLE: 0
DUPLICATE PAIR OPTICAL: 0
DUPLICATE SINGLE OPTICAL: 0
DUPLICATE NON PRIMARY: 0
DUPLICATE NON PRIMARY OPTICAL: 0
DUPLICATE PRIMARY TOTAL: 100
DUPLICATE TOTAL: 100
ESTIMATED_LIBRARY_SIZE: 538
Indexing...
Done: out.bam
Duplicate statistics:
500 + 0 in total (QC-passed reads + QC-failed reads)
100 + 0 duplicates
100 + 0 primary duplicates
exit=0
[check] dup flagged: 100 ; index exists: out.bam.bai
markdup_stats.txt
out.bam
out.bam.bai
### 5b. example on real human BAM (truth 1656)
exit=0
[check] dup flagged: 1656
### 5c. example with a MISSING input file
samtools sort: can't open "nonexistent.bam": No such file or directory
[bam_mating_core] ERROR: Couldn't read header
[W::hts_set_opt] Cannot change block size for this format
samtools sort: failed to read header from "-"
samtools markdup: error reading header
Indexing...
samtools index: "out.bam" is in a format that cannot be usefully indexed
script exit=1
output left behind: -rw-r--r-- 1 sci sci 28 Sep 20 04:11 out.bam
### 5d. example with a CORRUPT (truncated) input
samtools sort: truncated file. Aborting
[bam_mating_core] ERROR: Couldn't read header
[W::hts_set_opt] Cannot change block size for this format
samtools sort: failed to read header from "-"
... (34 more lines trimmed; full log in run/in05.log)
```

**Output (`run/in05b.log`, trimmed):**
```
wrote R1.fq/R2.fq: 100 real pairs + 20 synthetic clone pairs
index files: 5
### SKILL.md 'BWA-MEM2 with samblaster' verbatim (ref.fa R1.fq R2.fq)
exit codes 0 0 0
samblaster: Loaded 1 header sequence entries.
[check] records 240; flagged 40 (truth: 40 reads = 20 pairs, if all clones align properly)
240 + 0 in total (QC-passed reads + QC-failed reads)
40 + 0 duplicates
40 + 0 primary duplicates
240 + 0 properly paired (100.00% : N/A)
[check] flagged read names all clones? 40 of 40
### cross-check: samtools pipeline on the same alignments (no samblaster)
  samtools markdup flagged 40
[E::hts_open_format] Failed to open file "p_pic.bam" : No such file or directory
samtools view: failed to open "p_pic.bam" for reading: No such file or directory
  picard flagged 
### SKILL.md Picard command (java -jar picard.jar ...) -> the equivalent picard wrapper with the same key=value args, OPTICAL_DUPLICATE_PIXEL_DISTANCE=2500
  error lines: 1
[E::hts_open_format] Failed to open file "pk.bam" : No such file or directory
samtools view: failed to open "pk.bam" for reading: No such file or directory
  flagged 
### class names in tool table exist in Picard 3.5.0
/home/sci/micromamba/envs/af-picard3/bin/picard: line 5: warning: setlocale: LC_ALL: cannot change locale (en_US.UTF-8): No such file or directory
(pbmarkdup / biobambam2 not installed in env: table rows for those are NOT executed)
```

**Result:** Example and usage-guide pipelines correct (100/1656); example fails only by accident (index step) and leaves a 28-byte out.bam; samblaster path 40/40; Picard alternative NPEs on the RG-less BAM the aligner example produces

**Scores:** Basic 32/40 | Specialized 45/60 | Total 77/100

**Assertions:**
- [PASS] Shipped examples/markdup_pipeline.sh, run from a copy, flags the truth counts and prints stats - planted 100 (threads 2), real 1656; bash -n OK; usage 1-arg path exit 1
- [PASS] Failures of the example surface as a non-zero exit - missing, truncated and unwritable-output inputs all end exit 1, but only because the later 'samtools index' fails: the script has no pipefail and the tee pipeline itself returns 0; a 28-byte junk out.bam is left behind
- [FAIL] Example mirrors the Skill's own advice (explicit -d, pipefail, tmp handling) - no -d although SKILL.md says -d 0 disables optical detection; no pipefail; markdup_stats.txt written to cwd
- [PASS] bwa-mem2 | samblaster | samtools sort flags exactly the planted clone pairs - SYNTHETIC 20 clone pairs + 100 real pairs: 40 flagged, 40 of 40 are clones; samtools markdup gives 40 too
- [PASS] usage-guide 'Pipeline (No Intermediate Files)', step-by-step, -s/-f variants and rate one-liner give the truth counts - 100 flagged, exit codes 0 0 0 0, rate 20.00%, DUPLICATE TOTAL 100

### Input 6 - Scope Boundary: Assay decision: bulk RNA-seq, amplicon panel, pooled multi-library
**Prompt:** I have a bulk RNA-seq BAM, an amplicon-panel BAM and a pooled 2-library WGS BAM. Remove the duplicates from all three.

**Executed:** true - in06_assay_scope.sh, 00b_make_synth2.py -> in06.log; synth_multilib/samelib_2rg/amplicon are SYNTHETIC. Not executed: ATAC/Tn5 shift, ChIP macs3 keep-dup, aDNA mapDamage rows, Cell Ranger/STARsolo BAMs (no such data)

**Scripts:** `run/in06_assay_scope.sh`, `run/00b_make_synth2.py`

**Output (`run/in06.log`, trimmed):**
```
wrote synth_samelib_2rg.bam (60 pairs) and synth_amplicon.bam (1000 pairs)
### 6a. multi-library pooled marking: synth_multilib.bam (60 pairs, 30 coordinate-colliding pairs from DIFFERENT libraries). Truth: 0 duplicates
  default samtools markdup:        flagged reads 60 (over-marking, SKILL.md predicts this)
  --use-read-groups:               flagged reads 0
  Picard (library aware):          flagged reads 0
### 6b. same library, two RG IDs (two lanes): synth_samelib_2rg.bam. Truth: 30 dup pairs = 60 reads. SKILL.md: RG-ID keyed samtools vs LB keyed Picard
  default:            flagged 60
  --use-read-groups:  flagged 0
  Picard:             flagged 60
### 6c. amplicon panel (no UMI), synthetic 1000 pairs / 10 amplicons: SKILL.md says markdup erases the dataset
  flagged reads 1980 of 2000; non-dup reads left: 20
  markdup -r leaves 20 records (coverage collapse from 100x to ~1x per amplicon)
### 6d. real ARTIC amplicon nanopore BAM (single-end, long reads) through fixmate|markdup as the Skill's workflow would
  exit=0  flagged 3981 of 4916
  max read length in BAM: 2528  (markdup -l default 300)
  with -l 3000: flagged 3981
### 6e. bulk RNA-seq real PE BAM (SKILL.md: do NOT mark; duplicates are biological)
  flagged 2570 of 8828 records
  Picard flagged 2570
  500bp bin 25000: 6489 primary reads, 2443 flagged (38%) -> highest-expression locus loses signal
  500bp bin 24500: 101 primary reads, 17 flagged (17%) -> highest-expression locus loses signal
  500bp bin 3000: 63 primary reads, 12 flagged (19%) -> highest-expression locus loses signal
  [SKILL.md] table: bulk RNA-seq NO -> Skill body still lets 'mark duplicates' proceed for any BAM; is there a gate/stop? (inspection of SKILL.md: table only, no assay check in workflow)
```

**Result:** Decision table and multi-library claims verified by output (RG-ID vs LB claim included); amplicon 1980/2000 flagged, RNA 2570/8828 flagged with 38% of reads at the top locus; no assay gate in the workflow steps

**Scores:** Basic 34/40 | Specialized 52/60 | Total 86/100

**Assertions:**
- [PASS] Multi-library over-marking prediction and --use-read-groups fix are correct - synthetic 2-library BAM, truth 0 dups: default 60 flagged, --use-read-groups 0, Picard 0
- [PASS] '--use-read-groups keys on RG ID, Picard on LB' is accurate - synthetic 2 RG / 1 LB BAM, truth 60: --use-read-groups 0, default 60, Picard 60
- [PASS] 'Amplicon panel: markdup erases the dataset' is accurate - synthetic 10 amplicons x 100 pairs: 1980 of 2000 reads flagged, -r leaves 20; real ARTIC nanopore amplicon BAM 3981 of 4916 flagged
- [PASS] 'Bulk RNA-seq: NO' is supported and the Skill steers the agent away from it - real RNA BAM 2570 of 8828 flagged (Picard 2570 too); 2443 of 6489 primary reads (38%) at the highest-expression 500 bp bin flagged; decision table precedes the workflow

### Input 7 - Adversarial: UMI paired-end capture BAM: umi_tools, samtools --barcode-tag, fgbio grouping, consensus and duplex
**Prompt:** My paired-end capture BAM has duplex UMIs in the RX tag. Deduplicate it with the UMIs and call consensus reads, duplex if possible.

**Executed:** true - in07_umi.sh, in07b_fgbio.sh -> in07.log, in07b.log; real nf-core UMI BAM (unsorted, no @HD, dash-joined RX). Side findings: umi_tools --per-cell with no CB tag returns an empty BAM with exit 0; fgbio GroupReadsByUmi fails on the raw BAM (MQ tag not present) but works on samtools fixmate -m output here (4.1.1). Not executed: real Cell Ranger CB/UB dedup

**Scripts:** `run/in07_umi.sh`, `run/in07b_fgbio.sh`

**Output (`run/in07.log`, trimmed):**
```
records: 15788; with RX: 15788; sample RX: RX:Z:ATTTCAG-TATTATT
### 7a. flags in the SKILL.md umi_tools example exist in 1.1.6 help
  ok --extract-umi-method
  ok --umi-tag
  ok --cell-tag
  ok --per-cell
  ok --method
  ok --paired
  ok --stdin
  ok --stdout
    --method=METHOD     method to use for umi grouping [default=directional]
    --edit-distance-threshold=THRESHOLD
                        Edit distance theshold at which to join two UMIs when
                        grouping UMIs. [default=1]
    --spliced-is-unique
### 7b. umi_tools dedup verbatim-style on the UNSORTED BAM (Skill never says sort+index first)
              ^^^^^^^^^^^^^^
  File "pysam/libcalignmentfile.pyx", line 1104, in pysam.libcalignmentfile.AlignmentFile.fetch
ValueError: fetch called on bamfile without index
  exit=1
### 7c. sort+index, then umi_tools dedup WITHOUT --paired, and WITH --paired
  no --paired exit=0 records: 2805
  --paired   exit=0 records: 5689  (input 15788; TOOLS.md smoke: 15788 -> 5689)
  --method=unique records: 5927 (SKILL.md: unique treats 1-base UMI errors as distinct molecules -> should keep MORE)
### 7d. SKILL.md scRNA form (--cell-tag=CB --per-cell) on a BAM with no CB/UB tags: does it fail loudly?
  exit=0
### 7e. samtools markdup --barcode-tag RX (SKILL.md: exact-match UMI, added 1.16)
  without barcode: flagged 11783
  --barcode-tag RX: flagged 9879  (unique-molecule reads left: 5909)
  -r: records 5909
### 7f. fgbio flags in the SKILL.md commands vs 4.1.1 help
  -- AnnotateBamWithUmis
  -- GroupReadsByUmi
  -- CallMolecularConsensusReads
  -- CallDuplexConsensusReads
  -- SetMateInformation
```

**Output (`run/in07b.log`, trimmed):**
```
### 7g. GroupReadsByUmi straight on the raw unsorted UMI BAM, SKILL.md flags (--strategy=adjacency --edits=1)
[2026/09/20 04:15:26 | FgBioMain | Fatal] Mate mapping quality (MQ) tag not present on read 922332.
[2026/09/20 04:15:26 | FgBioMain | Fatal] #########################################################
[2026/09/20 04:15:26 | FgBioMain | Info] GroupReadsByUmi failed. Elapsed time: 0.03 minutes.
  exit=1  records: [main_samview] fail to read the header from "g_raw.bam".
### 7h. GroupReadsByUmi on samtools fixmate -m output (the Skill's own pipeline order)
[2026/09/20 04:15:28 | SamWriter | Info] Wrote         15,766 records.  Elapsed time: 00:00:00s.  Time for last 15,766:    0s.  Last read position: chr22:16570000-16610000:1,978.  Last read name: 922467
  exit=0
### 7i. with fgbio SetMateInformation first (input must be queryname-sorted: u.ns.bam from in07_umi.sh), then adjacency
[2026/09/20 04:15:31 | FgBioMain | Info] SetMateInformation completed. Elapsed time: 0.03 minutes.
[2026/09/20 04:15:34 | SamWriter | Info] Wrote         15,766 records.  Elapsed time: 00:00:00s.  Time for last 15,766:    0s.  Last read position: chr22:16570000-16610000:1,978.  Last read name: 922467
[2026/09/20 04:15:34 | FgBioMain | Info] GroupReadsByUmi completed. Elapsed time: 0.05 minutes.
  records 15766; MI groups: 2823; MI with /A|/B suffix: 0
### 7j. CallMolecularConsensusReads on adjacency groups (SKILL.md flags: --min-reads=1)
[2026/09/20 04:15:37 | CallMolecularConsensusReads | Info] Raw Reads Filtered Due to ZeroPostAfterTrimming: 0 (0.0000).
[2026/09/20 04:15:37 | CallMolecularConsensusReads | Info] Consensus reads emitted: 5,646.
[2026/09/20 04:15:37 | FgBioMain | Info] CallMolecularConsensusReads completed. Elapsed time: 0.05 minutes.
  exit=0 consensus records: 5646
### 7k. SKILL.md 'or for duplex': CallDuplexConsensusReads on the SAME adjacency-grouped BAM (SKILL.md flag form '--min-reads 1 1 0')
	at com.fulcrumgenomics.cmdline.FgBioMain.makeItSo(FgBioMain.scala:131)
	at com.fulcrumgenomics.cmdline.FgBioMain.makeItSoAndExit(FgBioMain.scala:99)
	at com.fulcrumgenomics.cmdline.FgBioMain$.main(FgBioMain.scala:49)
	at com.fulcrumgenomics.cmdline.FgBioMain.main(FgBioMain.scala)
  exit=1 duplex consensus records: [main_samview] fail to read the header from "duplex_bad.bam".
### 7l. same but grouped with --strategy=paired (what duplex calling needs)
[2026/09/20 04:15:43 | SamWriter | Info] Wrote         15,766 records.  Elapsed time: 00:00:00s.  Time for last 15,766:    0s.  Last read position: chr22:16570000-16610000:1,978.  Last read name: 922467
[2026/09/20 04:15:43 | FgBioMain | Info] GroupReadsByUmi completed. Elapsed time: 0.05 minutes.
  records 15766; MI with /A|/B suffix: 15766
[2026/09/20 04:15:46 | CallDuplexConsensusReads | Info] Raw Reads Filtered Due to PotentialCollision: 0 (0.0000).
[2026/09/20 04:15:46 | CallDuplexConsensusReads | Info] Consensus reads emitted: 4,042.
[2026/09/20 04:15:46 | FgBioMain | Info] CallDuplexConsensusReads completed. Elapsed time: 0.06 minutes.
  exit=0 duplex consensus records: 4042
### 7m. AnnotateBamWithUmis (-i -f -o) with a synthetic UMI fastq built from the RX tags
  umi.fastq reads: 7890
[2026/09/20 04:15:50 | AnnotateBamWithUmis | Info] Processed 15788 records with 0 missing UMIs.
[2026/09/20 04:15:50 | FgBioMain | Info] AnnotateBamWithUmis completed. Elapsed time: 0.04 minutes.
  exit=0 annotated records with RX: 15788
```

**Result:** umi_tools without --paired halves the output (2805 vs 5689) and errors on an unindexed BAM; the Skill's duplex step crashes (CallDuplexConsensusReads needs --strategy=paired); molecular consensus path works

**Scores:** Basic 27/40 | Specialized 34/60 | Total 61/100

**Assertions:**
- [PASS] Flags in the Skill's umi_tools, fgbio AnnotateBamWithUmis / GroupReadsByUmi / CallMolecularConsensusReads commands exist in the installed tools and run - umi_tools 1.1.6 help lists all flags; fgbio 4.1.1: annotate 15788 records, group 15766, 2823 MI groups, 5646 consensus reads
- [PASS] --method=directional default and 'unique keeps more molecules' claims are correct - help: default=directional; --paired unique 5927 vs directional 5689 records
- [FAIL] The duplex command after the Skill's own --strategy=adjacency grouping works - CallDuplexConsensusReads on adjacency-grouped BAM: StringIndexOutOfBoundsException, exit 1 (no MI /A /B suffix); after --strategy=paired: 4042 duplex reads
- [FAIL] The umi_tools example is safe for a real paired-end / unsorted BAM as written - unsorted BAM: 'fetch called on bamfile without index'; sorted+indexed but without --paired: 2805 records (mates dropped) vs 5689 with --paired; Skill states neither requirement
- [PASS] samtools markdup --barcode-tag RX behaves as described (exact-match UMI) - flags 9879 vs 11783 without the tag; -r leaves 5909 records

## Research Veto (Data Analysis)

| Dim | Result | Detail |
|---|---|---|
| scientific_integrity | PASS | No fabricated identifiers or results; every count reported in the audit traces to a logged command output. Unsupported statements (~30% faster, biobambam2 'fastest') are qualitative and were not executed. |
| practice_boundaries | PASS | Alignment-file processing only; no diagnostic or prescriptive clinical output. |
| methodological_ground | PASS | Assay-driven decision table is sound (verified for RNA-seq, amplicon and multi-library). Two factual errors (error strings; 'silently marks nothing') are not methodological fallacies. |
| code_usability | PASS | All Skill commands parse and use flags that exist in samtools 1.24, Picard 3.5.0, umi_tools 1.1.6, fgbio 4.1.1. Two documented commands fail on realistic input (clean-dir optimized pipeline, duplex after adjacency); recorded as P1, not unrunnable code. |

## Key Strengths
- Core mark/remove/stat workflow is exact: planted truth 100/100 and real-BAM 1656 reproduced by samtools, Picard, sambamba and samblaster, identical read set vs Picard
- Assay decision table is accurate and verified: amplicon 1980/2000 reads flagged, RNA-seq top locus 38% flagged, multi-library over-marking and the RG-ID vs LB distinction both reproduced
- Optical-duplicate section is correct: -d 0 disables detection, dt:Z:SQ/LB tags, per-platform distances give counts matching Picard on Illumina-named reads
- Every pysam snippet and the shipped example run verbatim from a copy and match samtools counts; all Related Skills and files exist

## Recommendations
**[P1] Duplex consensus step crashes after adjacency grouping** (observed in inputs [7])
- Problem: SKILL.md groups with --strategy=adjacency and then says 'or for duplex' CallDuplexConsensusReads on the same grouped.bam; on the real UMI BAM this throws StringIndexOutOfBoundsException (exit 1). With --strategy=paired the same call emits 4042 duplex reads.
- Root cause: Duplex calling needs MI tags with /A /B strand suffixes, which only the paired strategy writes; the Skill shares one grouping command between two consensus paths.
- Fix: Show two separate branches: adjacency -> CallMolecularConsensusReads, and 'GroupReadsByUmi --strategy=paired' -> CallDuplexConsensusReads. State the input prerequisites for GroupReadsByUmi (mate info via SetMateInformation on queryname-grouped input, or samtools fixmate -m output).

**[P1] umi_tools dedup example omits sort/index and --paired** (observed in inputs [7])
- Problem: The umi_tools command fails on an unsorted/unindexed BAM ('fetch called on bamfile without index') and, on a sorted paired-end BAM without --paired, silently outputs 2805 records instead of 5689 (mates dropped). Neither requirement is stated.
- Root cause: Example was written for single-end 10x BAMs and generalised to bulk/ctDNA capture BAMs without the prerequisites.
- Fix: Add: input must be coordinate-sorted and indexed; add --paired for paired-end libraries; note that --per-cell with absent CB/UB tags gives an empty BAM with exit 0, so check the tags first.

**[P1] Optimized pipeline fails from a clean directory and hides it** (observed in inputs [2, 5])
- Problem: 'samtools collate ... tmpdir/collate' fails when tmpdir/ does not exist; the pipe still exits 0 and writes an empty 501-byte marked.bam. The shipped markdup_pipeline.sh has the same no-pipefail structure and only exits non-zero because the later index step fails.
- Root cause: No mkdir for the temp dir and no 'set -o pipefail' or output check in either the SKILL.md pipeline or the shipped example.
- Fix: Add 'mkdir -p tmpdir' (or use mktemp -d) before the pipeline, 'set -o pipefail' in the example, and an assertion that the flagstat 'duplicates' line and record count are sane after marking.

**[P2] Common Errors table and Critical pitfall do not match samtools 1.24** (observed in inputs [3])
- Problem: Real messages are 'no ms score tag', 'Coordinate sorted, require grouped/sorted by queryname' and 'queryname sorted, must be sorted by coordinate'; the table lists 'mate not found', 'no MC tag' (for a missing -m) and 'not coordinate sorted'. The pitfall says missing tags silently mark almost nothing, but 1.24 exits 1 with an error.
- Root cause: Error strings were paraphrased or taken from older versions.
- Fix: Replace the table with the verbatim messages and delete or version-qualify the 'silently marks almost nothing' claim.

**[P2] No guidance on -c (re-marking) or read groups for Picard** (observed in inputs [3, 5])
- Problem: Re-running markdup on an already-flagged BAM without -c retained old flags (111 vs 101 from -c and Picard on the 1000G slice). Picard MarkDuplicates throws a NullPointerException on a BAM without @RG, which is what the Skill's own bwa-mem2 example produces (no -R).
- Root cause: Options in samtools markdup --help (-c, -S) and Picard's RG requirement are not covered.
- Fix: Add one line on -c for pre-marked or merged BAMs, add -R '@RG...' to the bwa-mem2 example, and note Picard needs @RG.

**[P2] usage-guide repeats SKILL.md and contradicts it** (observed in inputs [2, 4, 5])
- Problem: usage-guide says '-d 2500 for NovaSeq, NextSeq' and 'HiSeq -d 100' while SKILL.md gives NextSeq 500/550 and MiSeq 100, HiSeq 3000/4000/X 2500; duplicate-rate denominators differ (all records vs -F 256 vs primary only); the example script omits -d; the 'markdup -@ 8 fixes high memory' tip is unsupported (maxRSS rose 7.4 -> 13.8 MB).
- Root cause: Two documents restate the same facts and drifted apart.
- Fix: Keep the platform/-d matrix, workflow and rate formula only in SKILL.md, point usage-guide at it, and delete the memory tip or replace it with -T on a large scratch disk.

**[P2] Workflow steps do not gate on assay** (observed in inputs [6])
- Problem: The decision table says NO for bulk RNA-seq, amplicon and UMI assays (verified: 1980/2000 amplicon reads and 38% of reads at the top RNA locus get flagged), but the usage-guide 'What the Agent Will Do' and the shipped example run markdup on any BAM.
- Root cause: Assay check lives only in a table.
- Fix: Add step 0 to the workflow and to the example: confirm assay (RNA-seq, amplicon, UMI, scRNA), stop and hand off to the named tool if it is on the NO list.

## Verified-as-correct claims (by output)
- default `-d 0` disables optical detection; `dt:Z:SQ/LB` emitted with -d; `-t` adds `do` tag
- `--use-read-groups` keys on RG ID (Picard on LB): same-library 2-RG BAM 0 vs 60 flagged
- `fixmate -r -m` drops secondary/unmapped; `-f`, `-s`, `--json` stats
- `--barcode-tag RX`, `--read-coords`, `--barcode-name` exist in samtools 1.24 help
- pysam.fixmate/markdup/sort/index all work; errors raise SamtoolsError
- `--method=directional` is the umi_tools default; `unique` keeps more molecules

## Not verified
biobambam2, pbmarkdup, '~30% faster' pipeline claim, 'added in samtools 1.16' for --barcode-tag, Cell Ranger CB/UB dedup, ChIP/ATAC/aDNA rows (assay advice inspected, not executed).

## Cleanup
run/work/ (39 MB intermediates) deleted after the run; logs kept in run/*.log. No files written inside F:/OpenScience/external (no __pycache__ in the clone).
