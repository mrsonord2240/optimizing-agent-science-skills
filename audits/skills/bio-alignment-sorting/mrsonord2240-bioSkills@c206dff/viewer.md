> **Audit record for `bio-alignment-sorting`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@c206dff](https://github.com/mrsonord2240/bioSkills/tree/c206dff76d081a5126f8497fbabe10995c9b6026/alignment-files/alignment-sorting) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-20 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-alignment-sorting

Generated: 2026-09-20 | Source: `mrsonord2240/bioSkills@c206dff76d081a5126f8497fbabe10995c9b6026:alignment-files/alignment-sorting` (staging HEAD 9193f86; `git diff c206dff HEAD -- alignment-files/alignment-sorting` empty) | First audit, read-only.

Category: Data Analysis | Mode: B (CLI + one shipped script) | Complexity: Moderate (3 files, several task types: sort / collate / merge / tag sort / verify / pipeline) -> N = 5.
Env: WSL `science`, env `alignment-files`: samtools 1.24, pysam 0.24.1, bwa 0.7.19, bcftools 1.24, Picard 3.5.0, GATK 4.6.2.0, umi_tools 1.1.6, fgbio 4.1.1, HTSeq 2.1.2. Every script that ran is in `run\`; raw logs are `run\log_in0*.txt`. Skill copied into `run\skill\` and `run\work\in5a\skillcopy`; the external clone was only read (no `__pycache__`, no `.pyc` — checked with `find`).

## Step 1 — Skill Veto: PASS

| Dim | Result | Reason |
|---|---|---|
| T1 Stability | PASS | Every command and snippet ran repeatedly; no crashes or loops; the example fails loudly (not randomly) when `bwa index` is missing |
| T2 Contract | PASS | Frontmatter has `name`, `description`, `license`, `tool_type`, `primary_tool` |
| T3 Determinism | PASS | Record streams identical across `-@ 0/4/8`, across spill-to-disk, and on re-sort; `merge -s 7` reproducible (BAM bytes differ between runs only through the `@PG CL:` output filename) |
| T4 Security | PASS | No eval/exec of user strings, no credentials, nothing destructive; script variables are quoted |

## Step 2 — Static score: 73 / 100

| Category | Score | Note |
|---|---|---|
| Functional Suitability | 9/12 | Coverage good; `sort -n` mislabelled lexicographic, `-N`/`--template-coordinate` absent, merge gaps |
| Reliability | 7/12 | 3-row Common Errors table; no pipefail, no bwa-index step, no quickcheck |
| Performance/Context | 5/8 | SKILL.md (323 lines) and usage-guide (180) repeat nearly every command |
| Agent Usability | 11/16 | Clear; terminology drifts; little explicit verification output |
| Human Usability | 6/8 | Good trigger phrasing; merge/collate not in description |
| Security | 11/12 | Clean; example does not check inputs exist |
| Maintainability | 8/12 | Duplication between the two docs |
| Agent-Specific | 16/20 | Precise trigger, idempotent, composable; no out-of-scope guidance; 'trust the header' escape hatch is wrong |

## Step 3/4 — Generated test inputs

```
Skill: bio-alignment-sorting | Category: 3 Data Analysis | Mode: B | Complexity: Moderate -> 5 inputs
Input 1 (Canonical) : "My aligner output is unsorted. Coordinate-sort it, confirm the sort order, and index it. Use 8 threads and a fixed memory budget, and give me CRAM too."
Input 2 (Variant A) : "Sort by read name and run the duplicate-marking workflow, then extract paired FASTQ. Is `sort -n` a strict lexicographic order like the table says?"
Input 3 (Edge)      : "Sort by cell barcode. My BAM might have no @HD or a wrong one, or be truncated; how do I verify the sort order for real, and what if I give it tiny memory?"
Input 4 (Variant B) : "Merge these per-lane BAMs: check they are consistently sorted, dedup @RG/@PG, merge a region, and also merge the name-sorted versions."
Input 5 (Stress)    : "Run the shipped sort_pipeline.sh from a clean copy, check every row of the downstream sort-order table with the real tools, and confirm the speed/compression claims."
```

## Summary table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|
| 1 | Canonical | 35 | 53 | 88 | 5/5 PASS | ✅ executed |
| 2 | Variant A | 29 | 42 | 71 | 3/5 PASS | ⚠️ executed |
| 3 | Edge | 29 | 42 | 71 | 4/5 PASS | ⚠️ executed |
| 4 | Variant B | 34 | 51 | 85 | 4/5 PASS | ✅ executed |
| 5 | Stress | 29 | 42 | 71 | 2/5 PASS | ❌ partial (some table rows not installable) |

**Execution average: 77.2 / 100** (Layer 1 avg 31.2/40, Layer 2 avg 46.0/60). **Assertion pass rate: 18/25 = 72 %.**
Executed 5/5 (input 5 partially: Salmon, RSEM, Sniffles/cuteSV/Manta/Delly, featureCounts, Mutect2 and fgbio CallMolecularConsensusReads rows were not run).

## Detailed outputs

### Input 1 — Canonical (`run\in01_coordinate.sh`, log `run\log_in01.txt`)

**Data:** real nf-core human PE BAM shuffled (5644 rec), real 1000G chr20 slice shuffled (9601 rec, full GRCh38 header), real UMI BAM (15788 rec, no `@HD`).
**Code (SKILL, verbatim):** `samtools sort -o sorted.bam input.bam`; `-@ 8 -m 4G`; `-T /tmp/sort_tmp`; `-l 1`; `-O bam`; `-O cram --reference ref.fa`; `pysam.sort(...)` x2; SKILL `get_sort_order`; usage-guide `ensure_coordinate_sorted`.
**Printed / asserted (excerpt):**
```
[PASS] @HD says SO:coordinate (@HD VN:1.6 SO:coordinate)
n=5644 coordinate_sorted=True multiset_md5=2a119357...   (independent pysam walk)
[PASS] record multiset == original coord-sorted BAM (1267f5d9a548)
[PASS] idxstats chr22 mapped (5642) ; unmapped placed (*) (2)
[PASS] -@ 8 -m 4G / -T /tmp/sort_tmp / -l 1 / -O bam : same records
[PASS] CRAM record count (5644) ; CRAM @HD SO:coordinate ; CRAM index made
   (CRAM without --reference: only "[W::cram_get_ref] Failed to populate reference" warnings, file still written)
[PASS] 1000G coordinate order (tid,pos, unmapped last) ; multiset ; index
umi_unsorted: samtools index -> "[E::hts_idx_push] Unsorted positions on sequence #1: 3477 followed by 3470"
pysam.sort == CLI: True | pysam.sort(-@ -m -T) == CLI: True
umi_unsorted: unknown / shuffled_real: unsorted / sorted.bam: coordinate   (get_sort_order)
== assertions: PASS=15 FAIL=0 ==
```
**Scores:** Basic 35/40 | Specialized 53/60 | Total 88. Note: `-T` given an existing directory also works (used as prefix).

### Input 2 — Variant A (`run\in02_namesort_dup.sh`, log `run\log_in02.txt`)

**Data:** `derived/planted_dups.bam` (real reads, 50 planted pairs), real human PE BAM, synthetic `synth_multi.unsorted.bam` (names read1..read1000, SYNTHETIC).
**Code:** SKILL "Re-sort by Name for Duplicate Marking" (4 commands), the collate|fixmate -m -u|sort -u|markdup pipeline (SKILL line 98-101), usage-guide `sort -n -@ 4 | fixmate -m -@ 4 | sort -@ 4 | markdup -@ 4`, `collate -o out.bam in.bam`, `collate -O -u | fastq ... -n -`, and `sort -n` vs `-N` vs Picard SortSam vs ValidateSamFile.
**Printed / asserted (excerpt):**
```
markdup -s: EXAMINED 500  DUPLICATE PAIR: 100        Picard: READ_PAIRS_EXAMINED 250, READ_PAIR_DUPLICATES 50
[PASS] SKILL workflow duplicate reads flagged (100) ; collate pipeline (100) ; usage-guide pipeline (100)
real human BAM: samtools dup-flagged 1656   Picard 1656
fixmate -m on coordinate-sorted input: "[bam_mating_core] ERROR: Coordinate sorted, require grouped/sorted by queryname."
-- n_nat: @HD VN:1.6 SO:queryname SS:queryname:natural    qname_natural=True  qname_ascii=False
-- n_asc: @HD VN:1.6 SO:queryname SS:queryname:lexicographical   qname_ascii=True
-- n_pic: @HD VN:1.6 SO:queryname                          qname_ascii=True
half1 read1 read2 read3 ... read9 read10 read11 ...      <- sort -n (natural)
half1 read1 read10 read100 read1000 read101 read11 ...   <- sort -N == Picard
Picard ValidateSamFile on `sort -n` output: ERROR:RECORD_OUT_OF_ORDER 3 ; on `sort -N`: no ordering error
nf-core name.sorted.bam is also natural (qname_natural=True)
collate: @HD SO:unsorted GO:query ; no QNAME split across blocks ; 250 R1 == 250 R2, names identical in order
```
**Finding:** SKILL table row "`sort -n` | Full lexicographic sort by QNAME | Strict total order by name" and "use sort -n only when a tool requires true lexicographic order" are wrong for samtools 1.24; `-N` is never mentioned.
**Scores:** Basic 29/40 | Specialized 42/60 | Total 71.

### Input 3 — Edge (`run\in03_edge.sh`, log `run\log_in03.txt`)

**Data:** synthetic 3-contig BAM with CB tags/unmapped pairs (SYNTHETIC), real UMI BAM (RX), real 1000G BAM, `liar.bam` (real reads shuffled, header forced to SO:coordinate), truncated/junk copies, 384k-record BAM for a killed sort, 48k-record BAM for spill.
**Code:** `samtools sort -t CB`, `-t RX`, `-t CB -n`; SKILL awk verification snippet (verbatim); usage-guide `ensure_coordinate_sorted`; failure modes with captured exit codes; `-m` spill; `--template-coordinate`.
**Printed / asserted (excerpt):**
```
sort -t CB: header SO:unsorted SS:unsorted:CB:coordinate ; CB non-decreasing True ; position secondary True
samtools index on tag-sorted output: "[E::hts_idx_push] NO_COOR reads not in a single block at the end"  (cannot be indexed; SKILL silent)
ensure_coordinate_sorted(liar.bam) returned: liar.bam  (no re-sort)   ->   samtools index liar.bam: FAILED
awk snippet: sorted 0 | shuffled 1 | liar 1 | 1000G multi-contig 0
awk snippet on chr2-before-chr1 file: 0 (false pass);  order_check: coordinate_sorted=False
missing input rc=1; non-BAM rc=1 "failed to read header"; header-only BAM rc=0 (0 records); truncated: rc=1 "samtools sort: truncated file. Aborting"
killed sort: 0-byte killed.bam, quickcheck rc=4
-m 100K -> "[bam_sort] -m setting (100K bytes) is less than the minimum required (1M)"   (not in SKILL)
-m 1M on 48005 records: "merging from 14 files and 1 in-memory blocks" ; output == in-memory sort ; temp files removed
-@ 0/4/8 record streams identical
sort --template-coordinate: works with or without fixmate (SKILL never gives this command though it recommends the order for fgbio)
== assertions: PASS=10 FAIL=0 ==   (informational lines do not count; findings are in the JSON)
```
**Scores:** Basic 29/40 | Specialized 42/60 | Total 71.

### Input 4 — Variant B (`run\in04_merge.sh`, log `run\log_in04.txt`)

**Data:** real human + planted BAMs (6144 merged), SYNTHETIC `rgcollide_A/B.bam` (same RG ID L1, different SM/PU), name-sorted variants.
**Code:** SKILL consistency loop, `merge -c -p -@ 8`, `merge -@ 4`, `-b files.txt`, `-f`, `-R`, `pysam.merge('-c','-p','-f', ...)`, `addreplacerg` remedy.
**Printed / asserted (excerpt):**
```
consistent dir: 1 line (SO:coordinate) ; mixed dir: 2 lines (SO:coordinate / SO:queryname SS:queryname:natural)
merge -c -p: 6144 records, SO:coordinate, coordinate_sorted=True, @RG 1 ; without -c: @RG ID:1 and ID:1-0E8E8F08, second file's reads relabelled
rgcollide: -c -p -> ONE @RG (SM:sampleA), B reads labelled RG:Z:L1 ; without -c -> L1 / L1-0E8E8F08
addreplacerg then merge -c -p: two @RG, B reads RG:Z:L1B
merge coordinate + name-sorted, no -n: rc=0, no warning, header SO:coordinate, coordinate_sorted=False; samtools index: "Unsorted positions on sequence #1"
merge -n of two name-sorted BAMs keeps natural order ; plain merge does not
-b == positional (cols 1-11) ; no -f onto existing -> "File 'merged_b.bam' exists. Please apply '-f' to overwrite." ; -R chr22:2000-3000 = 3232 = sum of per-file counts
-R on unindexed inputs: "Could not retrieve index file" rc=1
pysam.merge == CLI merge: True n=6144 ; missing inputs raise SamtoolsError
== assertions: PASS=10 FAIL=0 ==
```
**Scores:** Basic 34/40 | Specialized 51/60 | Total 85.

### Input 5 — Stress (`run\in05a_pipeline_example.sh`, `in05b_downstream_matrix.sh`, `in05c_compression.sh`, `in05d_speed_repro.sh`; logs `run\log_in05*.txt`)

**5a — shipped example from a clean copy** (real SARS-CoV-2 100 pairs vs `genome.fasta`):
```
skillcopy/{SKILL.md, usage-guide.md, examples/sort_pipeline.sh}  bash -n ok
no args: Usage line, rc=1
un-indexed reference: "[E::bwa_idx_load_from_disk] fail to locate the index files" rc=1 (nothing in the docs says to bwa index)
after bwa index, PE: rc=0, 200 records, SO:coordinate, .bai, flagstat 200 mapped == raw bwa count ; SE: 100 records
`bwa -t $THREADS` but `samtools sort -@ 4` hard-coded
missing FASTQ: rc=1 (both stages fail) ; truncated gz: rc=0, 47 of 100 reads (bwa itself returns 0)
SIMULATED bwa crash (PATH shim, 60 lines then exit 3): script rc=0, "Done", crash.bam 57 of 100 reads ; with set -eo pipefail rc=3
SKILL python subprocess check=True pattern: raises on a missing FASTQ (both stages fail) -- same latent no-pipefail weakness
```
**5b — downstream table rows actually run:**
```
samtools index on name-sorted: refused ("Unsorted positions") ; markdup w/o fixmate: "no ms score tag" ; markdup on name-sorted: "queryname sorted, must be sorted by coordinate"
Picard MarkDuplicates on samtools -n output: IllegalArgumentException "Alignments added out of order ... Sort order is queryname" ; on -N output: 100 dups
GATK MarkDuplicatesSpark: coordinate 100 dups, queryname(-n) 100 dups
bcftools mpileup on name-sorted: "[E::bam_plp_push] The input is not sorted (reads out of order)" rc=1 (partial 106-line VCF vs 1147 sorted)
GATK HaplotypeCaller on name-sorted: "Traversal by intervals was requested but some input files are not indexed" rc=2 ; coordinate: 5 records
umi_tools dedup: unindexed or name-sorted -> "fetch called on bamfile without index" ; sorted+indexed 15788 -> 5689
fgbio GroupReadsByUmi (needs name-sorted input for SetMateInformation first): unsorted / coordinate / template-coordinate / name-sorted all 2823 MI groups, 15766 records ; help text confirms "Accepts reads in any order ... recommended template-coordinate ... samtools sort --template-coordinate"
HTSeq: coordinate -r pos 2884 ; name-sorted -r name 2884 ; coordinate with -r name 5709 (+ "claims to have an aligned mate which could not be found") ; htseq-count -p is --samout-format (SKILL row says "-p for paired")
NOT run: featureCounts, Salmon, RSEM, Sniffles, cuteSV, Manta, Delly, Mutect2, CallMolecularConsensusReads (not installed / no input; help text only)
```
**5c/5d — performance claims** (real 1000G reads x20 = 192k records, `-@ 0`, best of 3; redundant data so sizes are extreme):
```
-l 0 +3819% size 0.67 s | -l 1 +5.8% 0.34 s | -l 6 baseline 0.40 s | -l 9 -4.5% 3.83 s (+853%)   (SKILL: -l 0 +200-400%, -l 1 ~+30%/+10% time, -l 9 -2-5%/+50-100% time)
fixmate|sort: default-compression pipe 0.84 s vs -u pipe 0.72 s (direction as claimed)
sort -n 0.76 s | sort -N 0.57 s | collate 3.09 s | collate -u -O 3.22 s  -> collate ~4x SLOWER (SKILL: 3-10x faster)
re-sort of a sorted BAM: record stream unchanged (idempotent); @PG grows 14 -> 15 -> 16
```
**Scores:** Basic 29/40 | Specialized 42/60 | Total 71.

## Assertions (25) — 18 PASS / 7 FAIL

FAIL: name-order description (2.3), Picard accepts `-n` output (2.4), header-trust is safe (3.2), merge documents -n/-R (4.5), example runs from a clean copy (5.1), example propagates aligner failure (5.2), performance claims reproduce (5.4). No safety or scope assertion failed.

## Research Veto (category 3): PASS

Scientific Integrity PASS (no fabricated data; unsourced perf numbers recorded as P2) | Practice Boundaries PASS (file utility, no clinical output) | Methodological Ground PASS (name-order error fails loudly in Picard, does not silently corrupt an analysis) | Code Usability PASS (all code ran; `bwa index` prerequisite undocumented -> P1).

## Step 8 — Final

```
Static 73 x 0.4 = 29.2 | Execution 77.2 x 0.6 = 46.3 | FINAL = 75.5 -> 76
Floors for Limited Release (>=75): static >=70 OK | exec >=75 OK | L1 avg 31.2 >=28 OK | L2 avg 46.0 >=42 OK | assertions 72 % >= 80 % NOT MET
=> downgraded one tier: GRADE ⚠️ Beta Only. Deployable: false. Veto: none.
```

**Key strengths:** every core sort/merge/collate/pysam command reproduced ground truth (planted dups = Picard; real BAM 1656 = Picard); accurate warnings (merge does not validate sort order, RG collisions, no in-Python sorted()); downstream table held for every row that could be run; sorting is deterministic and idempotent.

**Recommendations**
- [P1] `sort -n` described as lexicographic; it is natural order (Inputs 2, 5). Picard MarkDuplicates crashes on `-n` output; `-N` never mentioned. Fix: document `-n` natural vs `-N` ASCII/Picard-compatible, the SS: header tag, and correct the RSEM/Salmon advice.
- [P1] Shipped example needs an undocumented `bwa index` and masks a mid-stream aligner failure (Input 5). Fix: `set -eo pipefail`, index/input checks, read-count sanity check.
- [P1] 'Trust the @HD SO: header' is unsafe; verification is header-only (Input 3). Fix: record-level check or index attempt as the test, `samtools quickcheck`, drop 'authoritative'.
- [P2] Merge omissions: `-n/-N/-t`, `-R` needs indexed inputs, 'Safe Merge' label vs `-c` collapse (Input 4).
- [P2] Unreproduced perf numbers and small flag inaccuracies: collate '3-10x', compression table, `-T` is a prefix, `-m` >= 1M floor, (threads+1) x `-m`, HTSeq `-p` (Inputs 2, 3, 5).
- [P2] Missing `--template-coordinate`, `--write-index`, 'cannot be indexed' note for -n/-N/-t (Inputs 3, 5).
- [P2] SKILL.md and usage-guide.md duplicate each other (dedup).

No P0: no veto fired, no safety assertion failed, no missing primary file (Related Skills folders and `examples/sort_pipeline.sh` all exist).
