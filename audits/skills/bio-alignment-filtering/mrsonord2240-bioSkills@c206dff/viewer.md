> **Audit record for `bio-alignment-filtering`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@c206dff](https://github.com/mrsonord2240/bioSkills/tree/c206dff76d081a5126f8497fbabe10995c9b6026/alignment-files/alignment-filtering) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-20 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-alignment-filtering
Generated: 2026-09-20  |  Source: `mrsonord2240/bioSkills@c206dff76d081a5126f8497fbabe10995c9b6026:alignment-files/alignment-filtering`  |  Category: Data Analysis  |  Mode: D  |  Complexity: Complex (N=7)

Environment: WSL `science` env `alignment-files` (samtools 1.24, pysam 0.24.1, bwa, bowtie2, hisat2, minimap2, STAR). Every script is in `run/`; logs in `run/out/`. The Skill folder was copied to `run/skill/` and run from there (no write inside `external\`, no `__pycache__`).

## Step 1 — Skill Veto: PASS (T1 stability, T2 contract, T3 determinism, T4 security)
Frontmatter has name/description/tool_type/primary_tool/license; no eval/exec/shell=True; samtools -s and the pysam recipe are deterministic; all files SKILL.md points at exist (the six Related Skills are sibling folders); `examples/filter_bam.py` exists but neither SKILL.md nor usage-guide.md links to it.

## Step 2 — Static score (25 criteria): 74 / 100
| Category | Score | Note |
|---|---|---|
| functional_suitability | 8/12 | Completeness 3, Correctness 2, Appropriateness 3. Flag arithmetic is exact, but the aligner MAPQ table, the -s 0.1 claim, the pysam BED and seed recipes, and the "Count unique" label are wrong. |
| reliability | 7/12 | Fault tolerance 2 (shipped script crashes on normal region strings; snippets silently mis-sample when target > total), error reporting 2 (raw tracebacks), recoverability 3 (writes new files; partial BAM left on index failure). |
| performance_context | 5/8 | Token cost 2 (usage-guide repeats most of SKILL.md, 411-line SKILL.md), execution efficiency 3 (streaming CLI, single pass). |
| agent_usability | 11/16 | Learnability 3, consistency 2 (SKILL.md -F 3332 vs usage-guide -F 2308; "Universal -q 1" vs the STAR row), feedback 3 (count before/after, quickcheck, flagstat), error prevention 3 (excellent SV warning; no unmarked-duplicate guard). |
| human_usability | 7/8 | Discoverability 4 (natural example prompts), forgiveness 3. |
| security | 11/12 | No credentials, no shell=True or eval, argparse; -o silently overwrites existing outputs. |
| maintainability | 8/12 | Modularity 2 (duplicated content in two docs; example script not referenced from either), modifiability 3, testability 3 (deterministic, count-before/after advice, no sample inputs). |
| agent_specific | 17/20 | Trigger 3, progressive disclosure 3, composability 4 (Related Skills, pipe-friendly), idempotency 4, escape hatches 3. |

## Steps 3-4 — Classification and inputs
Category 3 Data Analysis; Mode D (CLI recipes plus one example script). Complexity Complex (many task types, branching by assay/aligner) -> 7 inputs.

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Executed | Status |
|---|---|---|---|---|---|---|---|
| 1 | Canonical | 35 | 53 | 88 | 4/5 PASS | True | ✅ |
| 2 | Variant A | 36 | 55 | 91 | 3/5 PASS | True | ✅ |
| 3 | Edge | 27 | 38 | 65 | 3/5 PASS | True | ⚠️ |
| 4 | Variant B | 28 | 37 | 65 | 3/5 PASS | True | ⚠️ |
| 5 | Stress | 26 | 40 | 66 | 3/5 PASS | True | ⚠️ |
| 6 | Scope Boundary | 33 | 51 | 84 | 3/5 PASS | True | ✅ |
| 7 | Adversarial | 27 | 42 | 69 | 3/5 PASS | True | ⚠️ |

**Execution Average: 75.4 / 100**  |  **Assertion Pass Rate: 22/35**  |  Layer 1 avg 30.3/40  |  Layer 2 avg 45.1/60

## Detailed Outputs

### Input 1 — Canonical: Standard quality filter (primary, mapped, non-dup, MAPQ>=30) on real 1000G and nf-core BAMs
**Prompt:** Filter this BAM to keep only high-quality reads: mapped, primary, not duplicates, MAPQ 30 or higher. Give me the samtools command and a pysam version and tell me how many reads survive.

**Executed:** True — in1_standard.py in WSL: samtools 1.24 and pysam 0.24.1 on HG00349 chr20 slice and human PE test BAM, output read back and compared record-by-record.

**Code:** `run/in1_standard.py`

**Output (trimmed to 38 of 38 lines, `run/out/in1_standard.txt`):**
```

===== 1000g
records 9601  expected -F3332 -q30: 9437  expected -F2308 -q30: 9538
flag mix: dup 101 secondary 6 supp 0 unmapped 38 mapq<30 59
PASS 1000g CLI -F 3332 -q 30 exit+file 
PASS 1000g -o x.bam without -b writes BGZF/BAM (magic 1f8b) b'\x1f\x8b\x08\x04'
PASS 1000g CLI records == hand-count 9437 vs 9437
PASS 1000g header kept (SQ/RG count) 
PASS 1000g quickcheck 
PASS 1000g usage-guide -F 2308 -q 30 == hand-count 9538
1000g: usage-guide "standard" -F 2308 keeps 101 duplicate-flagged reads that SKILL.md -F 3332 drops (9538 vs 9437)
1000g: pysam Basic Filtering writes 9441; CLI standard writes 9437; secondary/supp left in: 4
PASS 1000g pysam passes_filter == CLI -F 3332 -q 30 9437
PASS 1000g usage-guide AlignmentFilter count == hand-count 9437
PASS 1000g count_with_filter == samtools -c (before/after) 9601/9538
['9437 + 0 in total (QC-passed reads + QC-failed reads)', '9437 + 0 primary', '0 + 0 secondary', '0 + 0 supplementary']

===== human
records 5644  expected -F3332 -q30: 5640  expected -F2308 -q30: 5640
flag mix: dup 0 secondary 2 supp 0 unmapped 2 mapq<30 2
PASS human CLI -F 3332 -q 30 exit+file 
PASS human -o x.bam without -b writes BGZF/BAM (magic 1f8b) b'\x1f\x8b\x08\x04'
PASS human CLI records == hand-count 5640 vs 5640
PASS human header kept (SQ/RG count) 
PASS human quickcheck 
PASS human usage-guide -F 2308 -q 30 == hand-count 5640
human: usage-guide "standard" -F 2308 keeps 0 duplicate-flagged reads that SKILL.md -F 3332 drops (5640 vs 5640)
human: pysam Basic Filtering writes 5642; CLI standard writes 5640; secondary/supp left in: 2
PASS human pysam passes_filter == CLI -F 3332 -q 30 5640
PASS human usage-guide AlignmentFilter count == hand-count 5640
PASS human count_with_filter == samtools -c (before/after) 5644/5640
['5640 + 0 in total (QC-passed reads + QC-failed reads)', '5640 + 0 primary', '0 + 0 secondary', '0 + 0 supplementary']

===== planted_dups (no dup flags set)
planted_dups -F 1024 count = 500 (500 records, 100 are planted duplicate reads but UNMARKED)
PASS SKILL.md "Remove Duplicates" (-F 1024) on an unmarked BAM removes nothing 

FAILS: []
```

**Summary:** CLI and pysam recipes match a hand-count from raw flag/MAPQ integers on 9601- and 5644-record real BAMs (9437 and 5640 kept). SKILL.md (-F 3332) and usage-guide (-F 2308) define "standard" differently: 101 duplicate-flagged reads survive the usage-guide version.

**Scores:** Basic 35/40 | Specialized 53/60 | Total 88/100

**Assertions:**
- [PASS] samtools view -F 3332 -q 30 output equals an independent hand-count of records with (flag&3332)==0 and MAPQ>=30 — 9437/9437 (1000g) and 5640/5640 (human); -o x.bam without -b writes BGZF BAM; quickcheck OK
- [PASS] SKILL.md pysam passes_filter yields exactly the CLI standard-filter record set — Record-by-record (flag, MAPQ, qname) identical on both BAMs
- [PASS] usage-guide AlignmentFilter / count_with_filter agree with samtools counts — count_with_filter before/after 9601/9538 equals samtools view -c and -c -F 2308 -q 30
- [PASS] Filtered BAM keeps the header (SQ/RG) and is a valid BAM — RG dict identical to input; flagstat 9437 + 0 primary
- [FAIL] SKILL.md and usage-guide give one consistent definition of the "standard" filter — SKILL.md -F 3332 -q 30 vs usage-guide -F 2308 -q 30 (and "-F 2308 for most downstream analyses"); the latter leaves 101 duplicate-flagged reads in the 1000G BAM

### Input 2 — Variant A: Assay-aware flag recipes and flag arithmetic, exhaustive over all 4096 FLAG values (synthetic)
**Prompt:** I need the right samtools filter flags for germline calling, somatic calling, ChIP-seq, ATAC-seq, SV calling and coverage analysis, and I want to be sure the flag numbers are correct.

**Executed:** True — make_synthetic_flags.py (SYNTHETIC: one read per flag 0..4095, because no real BAM here holds supplementary or QC-fail reads) then in2_flags.py; ground truth is Python bit arithmetic plus `samtools flags`.

**Code:** `run/make_synthetic_flags.py, in2_flags.py`

**Output (trimmed to 45 of 70 lines, `run/out/in2_flags.txt`):**
```
wrote /mnt/openscience/audits/bio-alignment-filtering/run/data/synthetic_allflags.bam 4096 records
PASS mapped [-F 4] samtools=2048 bit-arithmetic=2048
PASS unmapped [-f 4] samtools=2048 bit-arithmetic=2048
PASS proper pair [-f 2] samtools=2048 bit-arithmetic=2048
PASS remove dup [-F 1024] samtools=2048 bit-arithmetic=2048
PASS primary -F 2304 [-F 2304] samtools=1024 bit-arithmetic=1024
PASS read1 [-f 64] samtools=2048 bit-arithmetic=2048
PASS read2 [-f 128] samtools=2048 bit-arithmetic=2048
PASS forward [-F 16] samtools=2048 bit-arithmetic=2048
PASS reverse [-f 16] samtools=2048 bit-arithmetic=2048
PASS MAPQ30 [-q 30] samtools=2081 bit-arithmetic=2081
PASS mapped+MAPQ30 [-F 4 -q 30] samtools=1041 bit-arithmetic=1041
PASS standard 3332 [-F 3332 -q 30] samtools=139 bit-arithmetic=139
PASS germline [-f 2 -F 3328 -q 20] samtools=171 bit-arithmetic=171
PASS somatic [-F 3328 -q 1] samtools=503 bit-arithmetic=503
PASS longread SNV [-F 3328 -q 5] samtools=469 bit-arithmetic=469
PASS SV -F 1024 [-F 1024] samtools=2048 bit-arithmetic=2048
PASS ChIP 1804 [-F 1804 -q 30] samtools=66 bit-arithmetic=66
PASS ATAC 1804 -f 2 [-F 1804 -q 30 -f 2] samtools=30 bit-arithmetic=30
PASS HISAT2 RNA [-F 256 -q 60] samtools=34 bit-arithmetic=34
PASS STAR -q 255 [-q 255] samtools=0 bit-arithmetic=0
PASS coverage 1284 [-F 1284 -q 1] samtools=505 bit-arithmetic=505
PASS usage 2308 [-F 2308] samtools=512 bit-arithmetic=512
PASS usage 2308 q30 [-F 2308 -q 30] samtools=260 bit-arithmetic=260
PASS usage -f 2 -F 3332 -q 20 [-f 2 -F 3332 -q 20] samtools=87 bit-arithmetic=87
PASS -f 3 [-f 3] samtools=1024 bit-arithmetic=1024
PASS -f 1 [-f 1] samtools=2048 bit-arithmetic=2048
PASS -G 3 (table: exclude reads with ALL bits set) [-G 3] samtools=3072 bit-arithmetic=3072
PASS tumor-normal -F 2308 count [-F 2308] samtools=512 bit-arithmetic=512
repeated -F: n= 1024  OR-semantics n= 1024  last-wins n= 2048  first-wins n= 2048
PASS repeated "-F 256 -F 2048" behaves as -F 2304 (SKILL.md line 84 claim) 
-F 16 ("Forward Strand Only") includes 1024 unmapped reads (flag&4) among 2048
FAIL -F 16 output contains no unmapped reads (would need -F 20) unmapped in output=1024
-f 64 ("Keep Read1 Only") includes 1536 secondary/supplementary and 1024 duplicate records among 2048
PASS 2304 = 256+2048 
PASS samtools flags 2304 names == claimed 0x900	2304	SECONDARY,SUPPLEMENTARY
PASS 3328 = 256+1024+2048 
PASS samtools flags 3328 names == claimed 0xd00	3328	SECONDARY,DUP,SUPPLEMENTARY
PASS 3332 = 4+256+1024+2048 
PASS samtools flags 3332 names == claimed 0xd04	3332	UNMAP,SECONDARY,DUP,SUPPLEMENTARY
PASS 1284 = 4+256+1024 
PASS samtools flags 1284 names == claimed 0x504	1284	UNMAP,SECONDARY,DUP
PASS 1804 = 4+8+256+512+1024 
PASS samtools flags 1804 names == claimed 0x70c	1804	UNMAP,MUNMAP,SECONDARY,QCFAIL,DUP
PASS 2308 = 4+256+2048 
```

**Summary:** 28/28 -f/-F/-G/-q recipes equal bit arithmetic over every flag value; every "N = a + b" breakdown and the flag table match `samtools flags`. Semantics gaps: "Forward Strand Only" (-F 16) also returns unmapped reads; the somatic recipe drops the supplementary reads its own rationale wants kept.

**Scores:** Basic 36/40 | Specialized 55/60 | Total 91/100

**Assertions:**
- [PASS] Every -f/-F/-G/-q recipe in SKILL.md and usage-guide selects exactly the records predicted by bit arithmetic — 28 recipes x 4096 flags; repeated "-F 256 -F 2048" is OR-ed (1024 records) in samtools 1.24
- [PASS] All flag-sum breakdowns (2304, 3328, 3332, 1284, 1804, 2308) are arithmetically right and match `samtools flags` names — 8 doc claims parsed by regex plus 6 explicit; all equal
- [PASS] Common FLAG table (12 rows) and usage-guide decode examples match samtools — names and hex identical, e.g. 99 = PAIRED,PROPER_PAIR,MREVERSE,READ1
- [FAIL] "Forward Strand Only" (-F 16) and "Keep Read1 Only" (-f 64) return only the reads their headings say — -F 16 returns 1024 unmapped records among 2048; -f 64 returns 1536 secondary/supplementary and 1024 duplicate records
- [FAIL] The somatic recipe (-F 3328 -q 1) is consistent with its stated rationale (chimeric reads may carry real somatic SNVs) — 3328 contains 2048, so 0 of 2048 supplementary records survive

### Input 3 — Edge: Region/BED filtering, shipped examples/filter_bam.py, CRAM output (real human PE BAM, real UMI BAM)
**Prompt:** Extract the reads overlapping these target regions (a BED with overlapping rows, and chr22:1952-2100 style regions) with samtools and with pysam, using the shipped example script if it helps; also write CRAM.

**Executed:** True — in3_regions.py in WSL from a copy of the Skill; truth = own overlap arithmetic (1-based inclusive regions, 0-based half-open BED); UMI BAM sorted+indexed into out/ (contig chr22:16570000-16610000).

**Code:** `run/in3_regions.py`

**Output (trimmed to 44 of 44 lines, `run/out/in3_regions.txt`):**
```
records 5644
PASS samtools region chr22:1952-2100 == 1-based-inclusive overlap 802 reads
PASS samtools region chr22:2500-2500 == 1-based-inclusive overlap 0 reads
PASS samtools region chr22:4617-4700 == 1-based-inclusive overlap 2 reads
PASS samtools region chr22:3000-3200 == 1-based-inclusive overlap 1806 reads
PASS samtools multi-region == union of overlaps (no duplicated records) 2608
PASS usage-guide arg order "view in.bam region -o out" works 
literal SKILL.md region chr1:1000000-2000000 -> 0 [main_samview] region "chr1:1000000-2000000" specifies an invalid region or unknown reference. Continue anyway. | records in output 0
PASS region on unindexed BAM gives an error [E::idx_find_and_load] Could not retrieve index file for '/mnt/openscience/audits/bio-alignment-filtering/run/out/in3/no
PASS samtools -L BED == 0-based half-open overlap, each read once 2608
pysam BED recipe wrote 3410 records; samtools -L wrote 2608; duplicated records 802
FAIL pysam BED recipe == samtools -L (reads overlapping two BED rows are written once) 
pysam BED recipe output coordinate-sorted: False
pysam read_bed on BED with track line -> IndexError list index out of range
samtools -L on same BED: rc 0 count 2608 
samtools -L with chr absent from header: rc 0 count 0
fb none: Kept: 5,642 | Removed: 2 |  | Indexing output... |  
PASS fb no-filter keeps all mapped (5642) Kept: 5,642 Removed: 2  Indexing output...
fb -q30 -d -p -P -> Kept: 5,638 | Removed: 6 |  | Indexing output... |  | samtools equiv count 5638
PASS fb -q 30 -d -p -P Kept == samtools -f2 -F3332 -q30 
PASS fb output indexed (.bai exists and opens) 
region  (start,end, samtools_n, script_n, only_samtools, only_script):
   (1952, 2012, 653, 653, 0, 0)
   (2000, 2060, 798, 798, 0, 0)
   (2500, 2560, 0, 0, 0, 0)
   (3000, 3060, 1794, 1794, 0, 0)
FAIL fb region start==read last base (chr22:2043-): script matches samtools (1-based) semantics reads samtools returns but script drops: 2
fb -r 'chr22': rc=1 ValueError: not enough values to unpack (expected 2, got 1)
fb -r 'chr22:1952': rc=1 ValueError: not enough values to unpack (expected 2, got 1)
fb -r 'chr22:1,952-2,100': rc=1 ValueError: invalid literal for int() with base 10: '1,952'
fb -r 'chr22:1952-2100': rc=0 Kept: 802 | Removed: 0 |  | Indexing output...
fb -r 'chr22:1-99999999': rc=0 Kept: 5,642 | Removed: 0 |  | Indexing output...
fb region on unindexed: rc 1 ValueError: fetch called on bamfile without index
fb on name-sorted input: rc 1 pysam.utils.SamtoolsError: 'samtools returned with error 1: stdout=, stderr=samtools index: failed to create index for "/mnt/openscience/audits/bio-alignment-filtering/run/out/in3/fb_ns.bam"\n' | output exists True
umi contig header: @SQ	SN:chr22:16570000-16610000	LN:40001
fb region on colon-named contig: rc 1 ValueError: too many values to unpack (expected 2)
samtools brace syntax {contig}:100-300 -> 0 0 
samtools without braces -> 0 0 
PASS usage-guide CRAM output (-C -T ref -F 4) 
PASS CRAM round trip count == 5642 mapped 5642
CRAM read without -T: rc 0 5642 
fb on CRAM without reference: rc 0 Kept: 5,642 | Removed: 0 |  | Indexing output...

FAILS: ['pysam BED recipe == samtools -L (reads overlapping two BED rows are written once)', 'fb region start==read last base (chr22:2043-): script matches samtools (1-based) semantics']
```

**Summary:** samtools region, multi-region, -L BED and CRAM output are right. The pysam BED recipe writes 802 duplicated records (3410 vs 2608) in unsorted order. The shipped filter_bam.py has a 1-based/0-based off-by-one at the region start and crashes on bare contig, comma coordinates and colon-containing contig names; on name-sorted input it writes the BAM then dies at index.

**Scores:** Basic 27/40 | Specialized 38/60 | Total 65/100

**Assertions:**
- [PASS] samtools view region, multi-region and usage-guide argument order return exactly the overlapping reads (1-based inclusive) — 4 regions + multi-region union equal overlap truth (802, 0, 2, 1806, 2608 reads)
- [PASS] samtools view -L targets.bed returns each overlapping read once — 2608 = truth with two overlapping BED rows
- [PASS] CRAM output (-C -T ref) round-trips with the mapped count — 5642 mapped records read back with -T
- [FAIL] The pysam "Filter from BED File" recipe returns the same reads as samtools -L — 3410 records vs 2608: 802 reads overlapping two BED rows are written twice; output not coordinate-sorted; BED with a track line raises IndexError
- [FAIL] examples/filter_bam.py --region uses the same coordinates as samtools and accepts normal region strings — chr22:2043-... drops 2 reads samtools returns (fetch is 0-based); "chr22", "chr22:1952", "chr22:1,952-2,100" and the colon-named contig raise ValueError

### Input 4 — Variant B: Reproducible and pair-consistent subsampling: samtools -s recipes, coverage matching, pysam crc32 recipe (real 1000G BAM)
**Prompt:** Give me a reproducible 10% subsample that keeps read pairs together, and also downsample to about 3,000 reads (or 1,000,000 if the BAM is big enough), with samtools and with pysam.

**Executed:** True — in4_subsample.sh runs SKILL.md and usage-guide snippets verbatim; in4_subsample_pysam.py runs the crc32 recipe with seeds 42, 1, 7, 100, 12345; man samtools-view (1.24) read for --subsample-seed auto.

**Code:** `run/in4_subsample.sh, in4_subsample_pysam.py, in4c_pair_consistency.py`

**Output (trimmed to 49 of 49 lines, `run/out/in4_subsample.txt`):**
```
full records: 9601  distinct templates: 4828
--- SKILL.md: 10% with seed 42 (twice)
subset records: 1016  identical rerun: yes
--- SKILL.md/usage-guide claim: bare -s 0.1 is non-reproducible
bare -s 0.1 records: 1015 / 1015  identical: yes
bare -s 0.1 vs -s 42.1 same reads? no
--- SKILL.md: sequential cuts with INDEPENDENT seeds
half1=4738 quarter(seed2.25 of half1)=1197 (12.5% of 9601 = 1200)
--- SKILL.md: SAME seed nested claim (-s 1.5 then -s 1.25 -> 25% of original)
nested=2256 direct -s 1.25 on original=2256 same reads: yes
--- SKILL.md: coverage-matching snippet, target < total (target=3000)
total(-F 2304)=9595 target=3000 frac=0.312663 -> -s 1.312663
matched records = 2851  (target 3000)
--- same snippet, target > total (target=20000)
frac=2.084419 -> -s 1.084419
matched_big records = 750  (input 9601; user wanted 20000 => keep-all)
--- SKILL.md: tumor-normal coverage matching (tumor=1000g slice, normal=human slice)
normal=5640 tumor=9557 tumor_matched(-F 2308 count)=5604 all=5628
--- usage-guide.md: downsample-to-target snippet (bc), target 1000000
total=9601 frac='104.155817' -> -s "42104.155817"
usage-guide result records = 1445 of 9601 (wanted 1,000,000 => all)
--- usage-guide.md snippet with feasible target 2000
frac='.208311' -> -s "42.208311"
records = 2072 (target 2000)
--- usage-guide 'samtools view -s 42.1 -o subset.bam' (no -b) is BAM? magic:
1f8b
records 9601 templates 4828 templates with 2 records 4767
PASS seed 42: mates kept together 
PASS seed 42: realised template fraction ~0.10 (0.08-0.12) 0.0938 (453 templates)
PASS seed 1: mates kept together 
PASS seed 1: realised template fraction ~0.10 (0.08-0.12) 0.0938 (453 templates)
PASS seed 7: mates kept together 
PASS seed 7: realised template fraction ~0.10 (0.08-0.12) 0.0938 (453 templates)
PASS seed 100: mates kept together 
PASS seed 100: realised template fraction ~0.10 (0.08-0.12) 0.0938 (453 templates)
PASS seed 12345: mates kept together 
PASS seed 12345: realised template fraction ~0.10 (0.08-0.12) 0.0938 (453 templates)
Jaccard overlap of kept-template sets between seeds (independent 10% samples would share ~5%):
  seed 42 vs 1: Jaccard 1.000
  seed 42 vs 7: Jaccard 1.000
  seed 42 vs 100: Jaccard 1.000
  seed 42 vs 12345: Jaccard 1.000
  seed 1 vs 7: Jaccard 1.000
  seed 100 vs 12345: Jaccard 1.000
FAIL different small seeds give (near-)independent samples (SKILL.md: "use different integer seeds for independent samples" applies to CLI; pysam recipe shares the seed arg) Jaccard 42 vs 1 = 1.000
PASS seed 42 reproducible 
fraction 0.5 realised 0.4957

FAILS: ['different small seeds give (near-)independent samples (SKILL.md: "use different integer seeds for independent samples" applies to CLI; pysam recipe shares the seed arg)']
```

**Summary:** samtools -s 42.1 is deterministic and pair-consistent; independent-seed and nested-seed claims hold (1197 vs 1200 expected). But "-s 0.1 is non-reproducible" is false (identical reruns), the pysam recipe ignores its seed (Jaccard 1.000 across 5 seeds), and both target-count snippets silently mis-sample when the target exceeds the read count (750 and 1445 records kept of 9601).

**Scores:** Basic 28/40 | Specialized 37/60 | Total 65/100

**Assertions:**
- [PASS] samtools view -s 42.1 is reproducible and keeps mates together, at about 10% of templates — 1016 records twice, cmp identical; in4c: 512 of 4828 templates (10.6%), 0 templates with partial records
- [PASS] Sequential cuts: independent seeds give 12.5%, same seed nests (SKILL.md claims) — quarter=1197 vs 1200 expected; -s 1.25 on half1 == -s 1.25 on original (2256 both)
- [PASS] Coverage-matching snippet reaches the requested read count when the target is below the total — 2851 kept for target 3000 (-5%, template-hash variance); tumor-normal block 5628 vs 5640
- [FAIL] Claim "bare -s 0.1 is non-reproducible; production pipelines should reject it" is true — Two runs of -s 0.1 are byte-identical (1015 records); seed 0 is deterministic, only --subsample-seed auto is header-derived
- [FAIL] The pysam pair-consistent recipe honours its `seed` variable — zlib.crc32(qname) ^ seed only flips low bits: seeds 42/1/7/100/12345 keep the identical 453 templates (Jaccard 1.000)

### Input 5 — Stress: Aligner-aware MAPQ thresholds tested on 5 aligners (synthetic repeat genome) plus a real STAR RNA-seq BAM
**Prompt:** Which -q threshold should I use to drop ambiguous alignments and to keep high-confidence ones for BWA, Bowtie2, HISAT2, STAR and minimap2 output?

**Executed:** True — make_repeat_genome.py (SYNTHETIC 60 kb genome, repeat families x2/x3/x5/x8, 2720 SE reads) aligned with bwa mem 0.7.19, bowtie2 2.5.5, hisat2 2.2.3, minimap2 2.31 -ax sr, STAR 2.7.11b; retention counted with samtools view -F 2308 -q N. pbmm2 row not run (long-read only).

**Code:** `run/make_repeat_genome.py, in5_align.sh, in5_mapq_analysis.py`

**Output (trimmed to 60 of 65 lines, `run/out/in5_mapq.txt`):**
```
== REAL STAR RNA-seq BAM: MAPQ vs NH (primary records)
  MAPQ 0 NH 5 : 10
  MAPQ 0 NH 6 : 18
  MAPQ 1 NH 3 : 174
  MAPQ 1 NH 4 : 118
  MAPQ 3 NH 2 : 954
  MAPQ 255 NH 1 : 5768
  -q 1: keeps 7014/7042 primary; of which NH>1 (multi-mapped) = 1246 (multi total 1274)
  -q 3: keeps 6722/7042 primary; of which NH>1 (multi-mapped) = 954 (multi total 1274)
  -q 255: keeps 5768/7042 primary; of which NH>1 (multi-mapped) = 0 (multi total 1274)

== SYNTHETIC reads per class {'u': 2000, 'A2': 80, 'B3': 120, 'C5': 200, 'D8': 320}

-- bwa: MAPQ histogram of primary alignments per class
    u   unique          {60: 2000}
    A2  x2 exact        {0: 80}
    D8  x8 exact        {0: 320}
    B3  x3 1% diverged  {13: 1, 24: 2, 25: 5, 26: 14, 28: 5, 29: 1, 31: 2, 32: 1, 33: 4, 34: 2, 35: 2, 36: 3, 37: 10, 38: 26, 42: 1, 43: 2, 47: 4, 49: 4, 51: 13, 52: 2, 56: 4, 59: 1, 60: 11}
    C5  x5 2% diverged  {0: 11, 2: 3, 3: 1, 5: 2, 6: 2, 7: 4, 8: 5, 9: 10, 10: 17, 12: 1, 20: 4, 22: 2, 23: 1, 24: 4, 25: 19, 26: 38, 27: 4, 28: 2, 29: 1, 31: 2, 32: 1, 33: 2, 35: 1, 36: 1, 37: 5, 38: 13, 39: 1, 41: 1, 42: 1, 43: 1, 44: 1, 45: 1, 47: 2, 49: 7, 51: 9, 52: 1, 54: 1, 56: 1, 59: 1, 60: 16}
   retained after "drop ambiguous" -q 1: {'u': '2000/2000', 'A2': '0/80', 'D8': '0/320', 'B3': '120/120', 'C5': '189/200'}
   retained after "high confidence" -q 30: {'u': '2000/2000', 'A2': '0/80', 'D8': '0/320', 'B3': '92/120', 'C5': '69/200'}

-- bowtie2: MAPQ histogram of primary alignments per class
    u   unique          {23: 5, 40: 153, 42: 1842}
    A2  x2 exact        {1: 80}
    D8  x8 exact        {0: 1, 1: 319}
    B3  x3 1% diverged  {7: 2, 11: 3, 12: 4, 15: 4, 16: 3, 17: 11, 18: 7, 25: 7, 30: 9, 31: 39, 32: 19, 35: 11, 40: 1}
    C5  x5 2% diverged  {0: 1, 1: 7, 6: 41, 7: 1, 11: 5, 12: 14, 15: 3, 16: 1, 17: 11, 18: 16, 25: 9, 26: 1, 30: 19, 31: 12, 32: 31, 33: 1, 35: 22, 37: 4, 40: 1}
   retained after "drop ambiguous" -q 1: {'u': '2000/2000', 'A2': '80/80', 'D8': '319/320', 'B3': '120/120', 'C5': '199/200'}
   retained after "high confidence" -q 23: {'u': '2000/2000', 'A2': '0/80', 'D8': '0/320', 'B3': '86/120', 'C5': '100/200'}

-- star: MAPQ histogram of primary alignments per class
    u   unique          {3: 5, 255: 1995}
    A2  x2 exact        {1: 1, 3: 79}
    D8  x8 exact        {0: 320}
    B3  x3 1% diverged  {3: 1, 255: 119}
    C5  x5 2% diverged  {3: 11, 255: 189}
   retained after "drop ambiguous" -q 255: {'u': '1995/2000', 'A2': '0/80', 'D8': '0/320', 'B3': '119/120', 'C5': '189/200'}
   retained after "high confidence" -q 255: {'u': '1995/2000', 'A2': '0/80', 'D8': '0/320', 'B3': '119/120', 'C5': '189/200'}
   (universal "-q 1" would retain): {'u': '2000/2000', 'A2': '80/80', 'D8': '0/320', 'B3': '120/120', 'C5': '200/200'}

-- hisat2: MAPQ histogram of primary alignments per class
    u   unique          {60: 1995}
    A2  x2 exact        {0: 5, 1: 75}
    D8  x8 exact        {0: 20, 1: 299}
    B3  x3 1% diverged  {60: 120}
    C5  x5 2% diverged  {0: 2, 1: 4, 60: 193}
   retained after "drop ambiguous" -q 1: {'u': '1995/2000', 'A2': '75/80', 'D8': '299/320', 'B3': '120/120', 'C5': '197/200'}
   retained after "high confidence" -q 60: {'u': '1995/2000', 'A2': '0/80', 'D8': '0/320', 'B3': '120/120', 'C5': '193/200'}

-- minimap2: MAPQ histogram of primary alignments per class
    u   unique          {1: 1, 13: 2, 18: 1, 19: 1, 20: 1, 21: 1, 24: 1, 26: 1, 27: 1, 29: 2, 30: 1, 31: 3, 32: 1, 33: 1, 35: 3, 37: 1, 40: 3, 41: 1, 42: 1, 43: 2, 44: 3, 45: 2, 47: 3, 48: 1, 49: 3, 50: 2, 51: 4, 52: 3, 53: 2, 54: 10, 55: 2, 56: 1, 57: 2, 58: 1, 59: 4, 60: 1927}
    A2  x2 exact        {0: 80}
    D8  x8 exact        {0: 320}
    B3  x3 1% diverged  {32: 1, 40: 1, 43: 1, 44: 1, 49: 1, 50: 1, 53: 1, 54: 1, 59: 1, 60: 111}
    C5  x5 2% diverged  {0: 7, 1: 6, 3: 2, 4: 1, 6: 3, 7: 3, 8: 1, 9: 1, 10: 1, 15: 1, 17: 1, 18: 1, 19: 1, 30: 1, 31: 2, 32: 1, 34: 1, 35: 3, 36: 5, 38: 4, 43: 1, 44: 1, 47: 3, 48: 2, 55: 2, 57: 1, 58: 1, 60: 143}
   retained after "drop ambiguous" -q 1: {'u': '1999/2000', 'A2': '0/80', 'D8': '0/320', 'B3': '120/120', 'C5': '193/200'}
   retained after "high confidence" -q 60: {'u': '1927/2000', 'A2': '0/80', 'D8': '0/320', 'B3': '111/120', 'C5': '143/200'}

== Verdict per SKILL.md claim: fraction of TRULY AMBIGUOUS EXACT-repeat reads (A2+D8) that survive
```

**Summary:** "Drop ambiguous: -q 1" is wrong for Bowtie2 (399/400 exact-repeat reads kept, MAPQ 1) and HISAT2 (374/400 kept), and the "Universal -q 1 ... works for all aligners" line contradicts the STAR row (real STAR BAM: -q 1 keeps 1246 of 1274 multi-mapped primaries). BWA, minimap2 and STAR -q 255 rows are right.

**Scores:** Basic 26/40 | Specialized 40/60 | Total 66/100

**Assertions:**
- [PASS] BWA-MEM and minimap2 "-q 1" drops truly ambiguous (exact-repeat) reads — 0/400 exact-repeat reads survive on both; BWA unique reads all MAPQ 60
- [PASS] STAR "-q 255" keeps only uniquely mapped reads — Real STAR BAM: MAPQ 255 <=> NH==1 (5768 records; -e [NH]==1 identical)
- [PASS] HISAT2 "-q 60" high-confidence threshold keeps unique and drops repeats — 1995/2000 unique kept, 0/400 exact-repeat kept
- [FAIL] Bowtie2 "-q 1" drops ambiguous reads — Bowtie2 gives exact-repeat reads MAPQ 1 (319/320) and 0: -q 1 keeps 399/400
- [FAIL] "-q 1 ... works for all aligners" (Universal) holds — HISAT2 keeps 374/400 (MAPQ 1 = multi-mapped), STAR real BAM keeps 1246/1274 multi-mapped (MAPQ 1 and 3)

### Input 6 — Scope Boundary: Expression (-e) and read-group filtering, composite "insert size + soft clip + NM" request (real BAMs)
**Prompt:** Keep reads with NM <= 3, less than 20% soft clipping, insert size 100-500 bp and MAPQ >= 30; also restrict to one read group (library A).

**Executed:** True — in6_expr.py in WSL on nf-core human BAM (NM/AS tags), HG00349 BAM (2 RGs), STAR RNA BAM; SYNTHETIC 9-read BAM for reads lacking RG; samtools 1.24 man page (expression variables, -r) read.

**Code:** `run/in6_expr.py`

**Output (trimmed to 28 of 28 lines, `run/out/in6_expr.txt`):**
```
PASS -e '[NM] >= 2' == tag truth 229 vs 229 
verbatim SKILL.md cigar expr (rname chr1) -> rc 0 rows 0 stderr: 
PASS SKILL.md `cigar=~"^[0-9]+S"` expression is accepted by samtools 1.24 
adapted to chr22: rc 0 n 16 truth (leading soft clip) 16 err 
PASS cigar=~ leading soft-clip == CIGAR truth 
PASS -e 'sclen > 0' == reads with any soft clip 28 vs 28
PASS -F 2308 -q 30 -e '[NM] <= 5 && [AS] >= 100' == truth 4206 vs 4206
'sclen / qlen < 0.2': samtools 5628 truth (mapped reads, <20% soft-clipped) 5628 ; unmapped kept: 0
PASS -e 'sclen / qlen < 0.2' == truth on mapped reads 
reads with >=20% soft clip dropped by it: 14
PASS -e '![NM]' returns only reads missing NM (2 unmapped) 2 vs 2
-e on absent tag [XY]: rc 0 rows 0 (silently empty, no warning): ''
1000g RG IDs: ['SRR702039', 'SRR702040']  LB values: {'IWG_IND-TG.HG00349-5_1pA'}
PASS -r SRR702039 == RG tag truth 4438
PASS -r SRR702040 == RG tag truth 5163
SKILL.md example uses a LIBRARY-style name (-r library_A): `-r IWG_IND-TG.HG00349-5_1pA` (a real LB value) returns 0 reads
`-l IWG_IND-TG.HG00349-5_1pA` (the actual library option, not in the Skill) returns 9601 of 9601
PASS -R rg_list.txt (one ID per line) == truth 4438
SYNTHETIC: 3 reads RG=a, 3 RG=b, 3 no RG; `-r a` returns 6 -> ['s0', 's1', 's2', 's6', 's7', 's8']
FAIL -r a returns only RG a reads (SKILL.md: "single read group") 6 (samtools 1.24 man: reads with no RG are also output)
composite: naive tlen>=100&&tlen<=500 keeps 2109 ; truth positive-tlen only 2109 ; abs(tlen) truth 4225
PASS naive positive-tlen expression matches its own truth 
FAIL naive tlen expression keeps BOTH mates of each in-range pair (would need abs) 2109 vs 4225
PASS symmetric tlen expression == abs(tlen) truth 4225
after composite filter: templates with one mate only = 41 of 2133
PASS real STAR BAM: -e '[NH]==1' == -q 255 (SKILL.md STAR sentinel claim) 5768 vs 5768

FAILS: ['-r a returns only RG a reads (SKILL.md: "single read group")', 'naive tlen expression keeps BOTH mates of each in-range pair (would need abs)']
```

**Summary:** All -e recipes (NM, AS, cigar=~, sclen/qlen, ![NM]) equal tag/CIGAR truth; -R works. `-r library_A` is a library-style label but -r takes an RG ID (a real LB value returns 0 reads; `-l` is not mentioned), and -r also emits reads with no RG tag. A composite tlen expression needs a symmetric tlen test that the Skill does not show (naive keeps 2109 vs 4225).

**Scores:** Basic 33/40 | Specialized 51/60 | Total 84/100

**Assertions:**
- [PASS] -e recipes ([NM]>=2, cigar=~"^[0-9]+S", sclen/qlen<0.2, combined -F -q -e) equal tag/CIGAR truth — 229, 16, 5628 and 4206 records equal pysam truth; verbatim `rname=="chr1"` correctly returns 0 on a chr22 BAM
- [PASS] "![NM]" selects only reads missing NM (1.16+ claim) and -e [NH]==1 equals -q 255 on real STAR data — 2 reads (the unmapped pair); 5768 = 5768
- [PASS] -r <RG ID> and -R file select exactly that read group — SRR702039 4438, SRR702040 5163, -R file 4438 equal RG-tag truth
- [FAIL] The "Filter by Read Group" example `-r library_A` selects a library — -r matches RG ID only: a real LB value returns 0 of 9601 reads while -l returns all; -l is not documented
- [FAIL] `-r` returns only the named read group — Synthetic 3 RG-a + 3 RG-b + 3 no-RG reads: `-r a` returns 6 (samtools 1.24 also outputs untagged reads)

### Input 7 — Adversarial: "Remove duplicates, keep unique high-confidence proper pairs, then run Manta" on an unmarked-duplicate BAM
**Prompt:** Clean my BAM: remove duplicates, keep only unique high-confidence properly paired primary reads. I will run Manta on it afterwards.

**Executed:** True — in7_adversarial.sh in WSL: planted_dups.bam, collate/fixmate -m/sort/markdup, synthetic all-flag BAM, real STAR BAM. Manta not installed, so "zero SV calls" was not executed; only the flag-level cause (supplementary reads removed) was verified.

**Code:** `run/in7_adversarial.sh`

**Output (trimmed to 24 of 24 lines, `run/out/in7_adversarial.txt`):**
```
== A. 'Remove Duplicates' (SKILL.md: samtools view -F 1024) on a BAM whose duplicates are UNMARKED
records=500  dup-flagged(-f 1024)=0  after -F 1024: 500
   ground truth (planted): 50 pairs = 100 duplicate reads => expected 400 after true dedup
== B. Following the Related Skill order (mark first, then filter)
after markdup: dup-flagged=100  after -F 1024: 400  (expected 100 / 400)
   is any hint in SKILL.md/usage-guide to check dup flags exist before -F 1024?
/mnt/openscience/audits/bio-alignment-filtering/run/skill/SKILL.md:290:**Approach:** Define a predicate checking mapped status, primary alignment, duplicate flag, and MAPQ; stream reads through it.
/mnt/openscience/audits/bio-alignment-filtering/run/skill/SKILL.md:410:- duplicate-handling - Mark duplicates before filtering
== C. SV request: SKILL.md says SV callers need supplementary (2048) reads; -F 3332 / -F 2304 / -F 2308 remove them
supplementary records in synthetic set: 2048
  -F 1024 keeps supp: 1024
  -F 3332 -q 30 keeps supp: 0
  -F 2308 (usage-guide 'most downstream analyses') keeps supp: 0
  somatic recipe -F 3328 -q 1 keeps supp: 0  (SKILL.md text: 'chimeric reads at SVs may carry real somatic SNVs')
== D. Orphaned mates after read-level filtering (1000g slice), -F 3332 -q 30
single-record templates whose flag says paired+mate-mapped: before filter 59 of 4827 templates; after -F 3332 -q 30: 53 of 4763
   flagstat singletons after filter:
9344 + 0 properly paired (99.01% : N/A)
9401 + 0 with itself and mate mapped
36 + 0 singletons (0.38% : N/A)
   mentions of fixmate/orphan/singleton in the Skill files:
   (none)
== E. 'Count unique: -F 2304 (primary only)' label vs real uniqueness: STAR real BAM primary records with NH>1 under -F 2304
   -F 2304 records: 7042   of which NH>1: 1274   (-q 255 records: 5768)
```

**Summary:** The SV warning is correct and reproduced (-F 1024 keeps supplementary reads; -F 3332/-F 2308 remove all). But "Remove Duplicates" (-F 1024) on the planted BAM with unmarked duplicates keeps 500 of 500 with no warning (only a Related-Skills line says to mark first); after markdup it keeps the correct 400. "Count unique: -F 2304 (primary only)" is mislabelled: 1274 of 7042 STAR primaries are multi-mapped.

**Scores:** Basic 27/40 | Specialized 42/60 | Total 69/100

**Assertions:**
- [PASS] SV guidance is right: -F 1024 keeps supplementary reads while -F 3332 / -F 2304 / -F 2308 remove every one — 1024 of 2048 kept vs 0; the Skill says so explicitly with the cost of the mistake
- [PASS] Mark-then-filter (Related Skill order) removes exactly the planted 50 pairs — samtools markdup flags 100; -F 1024 leaves 400 of 500
- [FAIL] The Skill tells the user to check that duplicates are actually flagged before -F 1024 — -F 1024 on the unmarked BAM leaves 500 of 500; only "duplicate-handling - Mark duplicates before filtering" in Related Skills
- [FAIL] Every filter row is labelled with what it does ("Count unique: -F 2304 (primary only)") — -F 2304 keeps 7042 records including 1274 with NH>1; uniqueness needs -q 255 / NH==1
- [PASS] The Skill flags the conflict between a proper-pair filter and SV calling — Assay table lists Manta/GRIDSS/Delly with "-F 1024 only"; -f 2 is not recommended for SV

## Shipped-means-present and snippet smoke test
All 6 Related Skills exist as sibling folders; `examples/filter_bam.py` exists. `run/snippets_smoke.py` ran all 42 fenced blocks verbatim from a copy: 36 clean, 6 warned/failed for fixture reasons only (chr1 regions on a chr22 BAM, `conda` absent), see `run/out/snippets_smoke.txt`. Clean exit was never taken as proof; correctness is asserted in inputs 1-7.

## Research Veto: PASS (M1-M4)
- scientific_integrity: PASS — No fabricated citations, p-values or results; all numeric claims in outputs come from executed runs.
- practice_boundaries: PASS — File-processing Skill with no diagnostic or prescriptive content about individuals; no disclaimer required.
- methodological_ground: PASS — The wrong -q 1 rows for Bowtie2/HISAT2 mis-state aligner MAPQ semantics (reported as P1) but do not invert a conclusion or breach an ethical requirement.
- code_usability: PASS — All 42 snippets and the shipped script parse and run on valid inputs; failures are edge-case (region parsing) or silent-wrong (BED duplicates) and are reported as P1 rather than unrunnable code.

## Step 8 — Final
Static 74 x 0.4 = 29.6; Execution 75.4 x 0.6 = 45.2; **Final 75 / 100**.
Floors (Limited Release): static >= 70 ok (74); execution >= 75 ok (75.4); L1 >= 28 ok (30.3); L2 >= 42 ok (45.1); **assertion pass rate >= 80% NOT met (22/35 = 62.9%)** -> downgraded one tier: **Beta Only, deployable false**, no veto, no P0.

### Key strengths
- Flag arithmetic is exact: 28 recipes checked over all 4096 FLAG values and every "N = a + b" breakdown matches samtools 1.24.
- Assay-aware table and the explicit "keep supplementary for SV callers" warning are correct and reproduced on data.
- samtools -s subsampling advice (QNAME hash, pair consistency, nested vs independent seeds) is accurate and verified on a real BAM.
- -e expression recipes (NM, AS, cigar, sclen/qlen, ![NM]) equal independent tag/CIGAR truth, and the STAR MAPQ sentinel claim matches a real STAR BAM.

### Recommendations

**[P1] Aligner table: "-q 1 drops ambiguous" wrong for Bowtie2, HISAT2**  (inputs [5])
- Problem: On exact-repeat reads -q 1 keeps 399/400 (Bowtie2, MAPQ 1) and 374/400 (HISAT2, MAPQ 1); the "Universal -q 1 works for all aligners" line also fails on real STAR data (1246 of 1274 multi-mapped primaries kept) and contradicts the STAR row.
- Root cause: MAPQ 0 is treated as the only ambiguous value, but Bowtie2 and HISAT2 use MAPQ 1 (and STAR 1/3) for multi-mappers.
- Fix: Set "Drop ambiguous" to -q 2 for Bowtie2, -q 2 (or -q 60) for HISAT2, -q 4 or -q 255 for STAR, keep -q 1 for BWA/minimap2, and delete or rewrite the "Universal" block.

**[P1] pysam BED recipe duplicates reads and returns unsorted output**  (inputs [3])
- Problem: A read overlapping two BED rows is written once per row (3410 records vs 2608 from samtools -L, 802 duplicates); output is not coordinate-sorted; a BED with a track or blank line raises IndexError.
- Root cause: One fetch() per interval with no de-duplication or sort, and a fragile BED parser.
- Fix: Merge intervals first (or track written (qname, flag, pos) keys), skip track/browser/blank lines, and say to sort/index the output, or point to `samtools view -L`.

**[P1] examples/filter_bam.py region handling is off-by-one and brittle**  (inputs [3])
- Problem: --region is documented as chr:start-end but passed to fetch() as 0-based start, so reads ending exactly at the start base are dropped (2 lost at chr22:2043); bare contig, "chr22:1952", comma coordinates and colon-containing contig names raise ValueError; name-sorted input writes the BAM then fails at pysam.index.
- Root cause: region.split(":") and map(int, ...) with no parsing, no coordinate convention, and no sort check.
- Fix: Use pysam fetch(region=...) (samtools syntax) or start-1, accept commas and bare contigs, and check header SO:coordinate before indexing. Reference the script from SKILL.md.

**[P1] Subsampling: false "-s 0.1 non-reproducible", dead pysam seed, silent target>total**  (inputs [4])
- Problem: Bare -s 0.1 is deterministic (identical reruns), yet both docs say to reject it; the pysam crc32 recipe ignores its seed (identical 453 templates for 5 seeds); the coverage-matching and usage-guide bc snippets keep 750 and 1445 of 9601 reads when the target exceeds the read count.
- Root cause: Seed semantics were assumed rather than tested; the fraction is spliced textually into the -s argument with no >=1 guard.
- Fix: State that seed 0 is deterministic and that `--subsample-seed auto` derives a seed from the header; mix the seed into the hash (e.g. crc32(f"{seed}:{qname}")) ; add `[ frac >= 1 ]` -> copy the file.

**[P1] "Remove Duplicates" gives no guard when duplicates are unmarked**  (inputs [7])
- Problem: samtools view -F 1024 on the planted-duplicate BAM keeps 500 of 500 with no warning; the correct 400 appears only after collate/fixmate/sort/markdup.
- Root cause: The recipe assumes FLAG 0x400 is already set; the only hint is a Related-Skills line.
- Fix: Add a check (`samtools view -c -f 1024`; if 0, run duplicate-handling first) next to the -F 1024 recipe and in the usage-guide "What the Agent Will Do" steps.

**[P2] SKILL.md and usage-guide disagree on the standard filter**  (inputs [1])
- Problem: SKILL.md standard = -F 3332 -q 30; usage-guide standard = -F 2308 -q 30 and "use -F 2308 for most downstream analyses", which keeps duplicate-flagged reads (101 in the 1000G BAM). The usage-guide repeats most of SKILL.md.
- Root cause: Two copies of the recipes maintained separately.
- Fix: Keep one definition in SKILL.md and reduce the usage-guide to prompts and a pointer.

**[P2] Mislabelled rows: "Count unique -F 2304", "Forward Strand Only -F 16"**  (inputs [2, 7])
- Problem: -F 2304 keeps multi-mapped primaries (1274 of 7042 STAR records have NH>1); -F 16 also returns unmapped reads and -f 64 returns secondary, supplementary and duplicate records.
- Root cause: Headings describe intent, not the flag arithmetic.
- Fix: Rename "Count unique" to "Count primary alignments" (unique = -q 255 / NH==1) and add -F 20 / -F 2308 to the strand and read1/read2 recipes.

**[P2] Somatic recipe drops the reads its rationale wants kept**  (inputs [2, 7])
- Problem: -F 3328 removes all supplementary reads while the Why column says chimeric reads at SVs may carry real somatic SNVs.
- Root cause: 3328 copied from the germline row.
- Fix: Use -F 1280 -q 1 (keep supplementary) or drop the chimeric rationale.

**[P2] Read-group example and undocumented options**  (inputs [6])
- Problem: `-r library_A` is a library-style label but -r takes an RG ID (a real LB value returns 0 reads); -r also outputs reads with no RG tag; -l, -P (fetch pairs) and --subsample-seed auto are not mentioned.
- Root cause: Options not checked against the samtools man page.
- Fix: Rename the example to an RG ID, add `-l LIB`, note the no-RG behaviour, and mention -P for region queries with mates outside the region.

**[P2] Version-introduction claims unverified**  (inputs [])
- Problem: "-e since 1.12", "sclen and null-tag handling in 1.16" and the pbmm2/Mutect2/Strelka2 recipe rationale could not be verified (installed samtools 1.24 has no NEWS file; caller tools not run).
- Root cause: Version notes copied from memory.
- Fix: Cite the samtools NEWS entries or drop the version numbers.
