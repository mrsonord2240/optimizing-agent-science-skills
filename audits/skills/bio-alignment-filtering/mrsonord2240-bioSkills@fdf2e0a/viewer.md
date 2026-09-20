> **Audit record for `bio-alignment-filtering`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@fdf2e0a](https://github.com/mrsonord2240/bioSkills/tree/fdf2e0a288f37dd697b40adf06cfcdc6341cc654/alignment-files/alignment-filtering) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-20 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-alignment-filtering (RE-AUDIT of the fixed Skill)

Generated: 2026-09-20 | Source: `mrsonord2240/bioSkills@fdf2e0a288f37dd697b40adf06cfcdc6341cc654:alignment-files/alignment-filtering` | Pre-fix: 75, Beta Only (assertions 22/35) | **Now: 87, Production Ready**

Auditor: third agent (different from the first auditor and from the fixer). Everything below was produced by runs in `run/`; the fix log was read, not trusted.

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|
| 1 | Canonical | 37 | 57 | 94 | 5/5 PASS | ✅ |
| 2 | Variant A | 37 | 57 | 94 | 5/5 PASS | ✅ |
| 3 | Edge | 34 | 51 | 85 | 4/5 PASS | ⚠️ |
| 4 | Variant B | 37 | 57 | 94 | 5/5 PASS | ✅ |
| 5 | Stress | 36 | 56 | 92 | 5/5 PASS | ✅ |
| 6 | Scope Boundary | 35 | 51 | 86 | 3/4 PASS | ⚠️ |
| 7 | Adversarial | 35 | 51 | 86 | 4/4 PASS | ✅ |
| 8 | Variant B | 34 | 52 | 86 | 4/4 PASS | ✅ |
| 9 | Scope Boundary | 34 | 50 | 84 | 4/5 PASS | ⚠️ |

**Execution Average: 89.0 / 100** | **Assertion Pass Rate: 39/42 (92.9%)** | Layer 1 avg 35.4/40, Layer 2 avg 53.6/60

**Static 84/100 x 0.4 = 33.6; Dynamic 89.0 x 0.6 = 53.4; FINAL 87 — ⭐ Production Ready; deployable = true; no veto; no open P0/P1 (5 P2).**

Floors (Production Ready): static >= 80 ok, execution >= 85 ok, L1 >= 32 ok, L2 >= 48 ok, assertions >= 90% ok. Executed 9/9 inputs.

## Regression: what the first audit found, and what my own runs show now

| # | First-audit finding (pri) | Result now | Evidence |
|---|---|---|---|
| 1 | Aligner table: `-q 1` "drops ambiguous" wrong for Bowtie2/HISAT2 (P1) | FIXED | r5: `-q 2` removes 400/400 exact-repeat reads on Bowtie2 and HISAT2; old `-q 1` kept 399 and 374 |
| 2 | "Universal -q 1" block contradicts the STAR row (P1) | FIXED | block deleted; text says no universal threshold; `-e [NH]==1` == `-q 255` on STAR (2303 = 2303), real BAM 5768 = 5768 |
| 3 | pysam BED recipe: duplicated, unsorted, `track` crash (P1) | FIXED, one over-claim left | r3: identical to `samtools -L` (content and order) on 81 fuzz BEDs without zero-width rows; zero-width rows differ (P2) |
| 4 | filter_bam.py: off-by-one, crashes on bare contig / commas / colon contig / name-sorted (P1) | FIXED | r3: 9 edge regions + 180 random regions on 3 real BAMs identical to samtools; bad regions exit cleanly |
| 5 | "-s 0.1 is non-reproducible" false (P1) | FIXED | r4: bare -s 0.1 byte-identical twice and == seed 0 (1015); auto seed 1001; NEWS 1.24 confirms default-seed change |
| 6 | pysam subsample ignores its seed (P1) | FIXED | r4: 6 seeds, Jaccard 0.044-0.069, rerun identical |
| 7 | Coverage matching keeps 8% when target > total (P1) | FIXED | r4: target 10M -> unchanged copy 9601; targets 3000/1000/6000 within 8% |
| 8 | `-F 1024` silently a no-op on unmarked BAM (P1) | FIXED | r1/r7: snippet marks 100 and leaves 400 on coordinate-sorted, name-sorted and shuffled input |
| 9 | SKILL.md `-F 3332` vs usage-guide `-F 2308` (P2) | FIXED | usage-guide has no competing filter |
| 10 | Mislabelled rows (Count unique, forward, read1) (P2) | FIXED | r2 |
| 11 | Somatic recipe drops the supplementary reads its rationale keeps (P2) | FLAG FIXED, RATIONALE STILL WRONG | r2 (503 supplementary kept); n10: Mutect2 filters MAPQ<20 itself (new P2) |
| 12 | `-r library_A`, `-r` emits untagged reads (P2) | FIXED, new wrong release number | r6; NEWS: `-n` is 1.23 not 1.24 (new P2) |
| 13 | Version claims unverified (P2) | PARTLY | n11: -e 1.12, sclen 1.16, seed 1.24 confirmed; `-n` wrong |

New defects introduced by the fix: none that broke anything. Two over-claims it added: "same records as samtools view -L" (false for zero-width rows) and "Samtools 1.24 adds -n" (1.23).

## Test inputs (9 = 7 regression + 2 new)

Complexity: Complex -> 9 inputs (precedent: bio-alignment-structural re-audit also ran 9). Category: Data Analysis. Mode: D (instructions, samtools CLI, one example script).


### Input 1 — Canonical: [regression] Standard quality filter + Remove-Duplicates pre-check on real 1000G, nf-core and planted-duplicate BAMs

**Prompt:** "Filter my BAM file to keep only high-quality reads, and remove the duplicates." (real 1000G HG00349 BAM, 9601 records / 101 dup-flagged; real nf-core human PE BAM, 5644 records; planted-duplicate BAM with 100 UNMARKED duplicate reads)

**Executed:** true (WSL science env alignment-files). **Scores:** Basic 37/40 | Specialized 57/60 | Total 94/100 ✅

**Result:** Standard filter (-F 3332 -q 30) equals a hand count on both real BAMs (9437 and 5640); pysam passes_filter identical record for record; the new duplicate pre-check marks 100 reads on the unmarked BAM and leaves 400.

**Assertions:**
- [PASS] The SKILL.md Standard Quality Filter block (-F 3332 -q 30) equals a hand count from raw FLAG/MAPQ integers on two real BAMs — 9437/9601 and 5640/5644 records; output is BGZF; quickcheck OK
- [PASS] The pysam passes_filter block is record-for-record identical to the CLI result — to_string() lists equal on both BAMs
- [PASS] The extracted Remove-Duplicates snippet marks first when no duplicate flag exists and then removes them — planted BAM: "marking first", 100 flagged (one template of each of the 50 planted pairs), 400 left, 0 dup-flagged; 1000G (already marked): straight -F 1024, 9500
- [PASS] The text is right that plain -F 1024 on an unmarked BAM keeps everything — 500 of 500 reproduced
- [PASS] usage-guide.md no longer contradicts SKILL.md about the "standard" filter — no -F 2308 or -F 3332 left in usage-guide.md

**Key output (trimmed; full text in `run/out/`):**

```
===== 1000g
records 9601 expected standard filter 9437 | dup-flagged 101
PASS 1000g SKILL.md standard-filter block == hand-count 9437 vs 9437 rc=0 err=
PASS 1000g -o filtered.bam (no -b) is BGZF
PASS 1000g quickcheck
PASS 1000g pysam passes_filter block == hand-count == CLI 9437
PASS 1000g CLI and pysam outputs record-for-record identical
PASS 1000g count-only == filtered size 9437
===== human
records 5644 expected standard filter 5640 | dup-flagged 0
PASS human SKILL.md standard-filter block == hand-count 5640 vs 5640 rc=0 err=
PASS human -o filtered.bam (no -b) is BGZF
PASS human quickcheck
PASS human pysam passes_filter block == hand-count == CLI 5640
PASS human CLI and pysam outputs record-for-record identical
PASS human count-only == filtered size 5640
===== Remove Duplicates pre-check (extracted from SKILL.md)
PASS planted (unmarked, 100 dup reads): snippet rc=0 and nodup.bam has 400 records, 0 dup-flagged rc=0 n=400 dupflag=0 stderr='no duplicate-flagged reads; marking first'
PASS unmarked BAM: the snippet announced that it is marking first no duplicate-flagged reads; marking first
PASS planted truth: 50 coordinate groups have 2 templates, exactly one flagged in each, singletons never flagged groups with 2 templates=50
PASS marked.bam is coordinate sorted, has 500 records
PASS 1000g (already marked, 101): snippet rc=0 and nodup.bam has 9500 records, 0 dup-flagged rc=0 n=9500 dupflag=0 stderr=''
human PE BAM dup-flagged records (natural): 0
PASS claim in text: "-F 1024 on unmarked BAM keeps 500 of 500" 500
PASS usage-guide.md no longer contains a competing -F 2308 "standard" filter
FAILS: []
```


### Input 2 — Variant A: [regression] Every flag/MAPQ recipe, exhaustive over all 4096 FLAG values (synthetic BAM) and the flag tables

**Prompt:** "Give me the samtools flags for: mapped only, primary only, read1 only, forward strand only, germline/somatic/ChIP/ATAC/RNA/SV prep." (SYNTHETIC BAM, one read per FLAG 0..4095)

**Executed:** true (WSL science env alignment-files). **Scores:** Basic 37/40 | Specialized 57/60 | Total 94/100 ✅

**Result:** 14 recipes harvested by regex from the fixed SKILL.md bash blocks and 9 assay-table recipes: all equal bit arithmetic over 4096 flags; relabelled forward/reverse/read1/read2 rows clean; all 7 breakdown lines equal `samtools flags`.

**Assertions:**
- [PASS] Every -f/-F/-G/-q recipe in the bash blocks equals bit arithmetic over all 4096 flag values — 14 recipes, all equal
- [PASS] Every assay-table recipe equals bit arithmetic — 9 recipes (germline, somatic, long-read, ChIP, ATAC, coverage, HISAT2, STAR, SV)
- [PASS] The relabelled rows return what their labels say (forward -F 20, reverse -f 16 -F 4, read1/read2 -f 64/128 -F 2308) — 0 unmapped in strand outputs; 0 secondary/supplementary/unmapped in read outputs
- [PASS] The somatic row keeps the supplementary reads its rationale keeps, while -F 2304/2308/3328/3332 remove them all — 503 supplementary kept by -F 1280 -q 1; 0 left by the other four
- [PASS] The FLAG table, `samtools flags 99` line and the 7 "N = a + b" breakdowns match samtools — 12 table rows, 7 breakdowns (bits and prose term counts)

**Key output (trimmed; full text in `run/out/`):**

```
14 distinct flag/MAPQ recipes harvested from SKILL.md bash blocks
PASS [Keep Only Mapped Reads] samtools view -F 4 n=2048
PASS [Keep Only Unmapped Reads] samtools view -f 4 n=2048
...
PASS forward -F 20: no unmapped, no reverse n=1024
PASS reverse -f 16 -F 4: all reverse, no unmapped n=1024
PASS read1 -f 64 -F 2308: only mapped primary read1 n=256
PASS read2 -f 128 -F 2308 n=256
PASS somatic -F 1280 -q 1 keeps supplementary (rationale in text) supp kept 503
PASS `samtools flags 99` line quoted in SKILL.md is the real output '0x63\t99\tPAIRED,PROPER_PAIR,MREVERSE,READ1'
7 flag-breakdown lines found
PASS 7 breakdown lines present (1280,1284,1804,2304,2308,3328,3332)
FAILS: []
```


### Input 3 — Edge: [regression] Region, -L BED, pysam region/BED recipes and the shipped examples/filter_bam.py (three real BAMs, fuzzed)

**Prompt:** "Extract reads from chr22:1,952-2,100, from my BED targets (with a track line), and run the shipped filter script on my name-sorted / unindexed / colon-contig BAMs." (real nf-core PE, spliced RNA-seq and 1000G BAMs; 81 random BEDs, 180 random regions)

**Executed:** true (WSL science env alignment-files). **Scores:** Basic 34/40 | Specialized 51/60 | Total 85/100 ⚠️

**Result:** The first-audit defects here (BED recipe duplicating and unsorting reads, filter_bam.py off-by-one and crashes) are fixed: recipe identical to samtools -L on 81 fuzz BEDs without zero-width rows; filter_bam.py equals samtools on every region form. Left: the recipe drops what samtools keeps for zero-width (start==end) rows (13/81 fuzz BEDs) and crashes on a space-delimited BED.

**Assertions:**
- [PASS] samtools region semantics quoted in the text hold (1-based inclusive, absent contig warns with rc 0, index required, -L skips track/#/browser lines, -P needs region or -L, CRAM needs -T) — 14 semantic checks pass
- [PASS] The pysam rule fetch(c, start-1, end) equals samtools c:start-end, and the region snippet runs — 60 random regions identical
- [PASS] The pysam BED recipe equals samtools -L in content and order on BEDs with track/#/browser/blank/nested/touching/CRLF/6-column/unsorted/unknown-contig rows and on 81 fuzz BEDs (3 real BAMs) — 0 mismatches without zero-width rows; output keeps SO:coordinate
- [FAIL] The text claim "same records as samtools view -L" holds for zero-width (start==end) and space-delimited BED rows — 13/81 fuzz BEDs differ, every one containing a start==end row (samtools keeps the base at s, fetch(c,s,s) returns nothing); space-delimited BED raises IndexError
- [PASS] examples/filter_bam.py equals samtools on bare contig / contig:start / open end / commas / colon contigs / 180 random regions on 3 BAMs, refuses bad regions cleanly, and handles unindexed and name-sorted input — no Traceback on 5 bad regions; -d warns on an unmarked BAM; -q 30 -d -p -P == samtools -f 2 -F 3332 -q 30

**Key output (trimmed; full text in `run/out/`):**

```
PASS pysam rule fetch(c, start-1, end) == samtools c:start-end, 60 random regions mismatches 0
PASS BED recipe (track/#/browser/blank/zero-width/unknown contig/nested rows) == samtools -L, record-for-record in order 2608 vs 2608
PASS BED recipe on crlf BED == samtools -L 2608 vs 2608
PASS BED recipe on 6col_names BED == samtools -L 2608 vs 2608
PASS BED recipe on no_trailing_newline BED == samtools -L 2608 vs 2608
PASS BED recipe on unsorted_reverse BED == samtools -L 2608 vs 2608
PASS BED recipe on touching BED == samtools -L 802 vs 802
PASS BED recipe on contained BED == samtools -L 5550 vs 5550
FAIL BED recipe on space_delimited BED == samtools -L IndexError: list index out of range
PASS BED recipe on whole_contig_huge_end BED == samtools -L 5642 vs 5642
PASS BED recipe fuzz, no zero-width rows: 81 random BEDs on 3 real BAMs (paired, spliced RNA, 1000G) identical to samtools -L in content and order mismatching BEDs 0; non-empty outputs 79/81
   MISMATCH zw rna_spliced #5: pysam 77 vs samtools 92; only-pysam 0, only-samtools 15; BED has zero-width row: True
      BED: track name=fuzz | chr22 2997 3497 | chr22 4697 4697 | chr22 5 35 |
   MISMATCH zw rna_spliced #15: pysam 135 vs samtools 138; only-pysam 0, only-samtools 3; BED has zero-width row: True
      BED: chr22 4361 4511 | chr22 1571 1572 | chr22 2025 2025 | chr22 2044 4850 | chr22 3430 3460 |
   MISMATCH zw rna_spliced #21: pysam 0 vs samtools 28; only-pysam 0, only-samtools 28; BED has zero-width row: True
      BED: chr22 4149 4149 | chrUnknown 1 100 | chr1 100 900 |
   fuzz WITH zero-width rows: 13/81 BEDs differ from samtools -L; 13 of those 13 contain a start==end row
FAIL BED recipe fuzz, zero-width (start==end) rows allowed: identical to samtools -L (text claims "same records as samtools view -L") 13/81 differ
   zero-width BED chr20 1433164 1433164: samtools -L 5 reads; pysam fetch(s,s) 0; fetch(s,s+1) 5; reads covering 0-based pos s 5
PASS pysam fetch(c, s, s) on a zero-width row returns nothing (so the recipe drops what samtools keeps)
PASS filter_bam -r fuzz: 120 random regions (plain/comma/open) record-identical to samtools -F 4 region mismatches 0
```


### Input 4 — Variant B: [regression] Reproducible, pair-consistent subsampling: samtools -s, coverage-matching guard, pysam blake2b recipe (real 1000G BAM)

**Prompt:** "Subsample my BAM to 10% reproducibly, then to exactly ~3000 reads, and match tumor coverage to the normal." (real 1000G BAM 9601 records / 4828 templates; nf-core PE as normal)

**Executed:** true (WSL science env alignment-files). **Scores:** Basic 37/40 | Specialized 57/60 | Total 94/100 ✅

**Result:** Every claim reproduces: -s 42.1 template-consistent and deterministic; bare -s 0.1 == seed 0 (1015); --subsample 0.1 auto seed 1001; guarded coverage matching lands within 8%; pysam recipe honours its seed (Jaccard 0.044-0.069).

**Assertions:**
- [PASS] -s 42.1 keeps or drops every record of a template together, is ~10%, and is deterministic — 512 of 4828 templates, all records kept, identical rerun
- [PASS] The corrected 1.24 seed statements hold (bare -s 0.1 deterministic and equal to seed 0; --subsample without a seed uses a header-derived seed and differs) — 1015 = 1015; auto 1001; NEWS.md 1.24 states the default-seed change (n11)
- [PASS] Sequential cuts with independent seeds give 12.5%; same-seed cuts nest — 1197 of 9601; nested 2256 == direct 2256
- [PASS] The extracted coverage-matching and tumor-normal block is safe when target > total and lands near the target otherwise — target 10M -> unchanged copy 9601; 3000/1000/6000 -> -5.0/-7.8/-0.6%; tumor 5604 vs normal 5640; target == total copies, total-1 keeps all
- [PASS] The pysam blake2b recipe is pair-consistent, honours its seed, reproducible and unbiased — 6 seeds ~10%, all records of a template kept, pairwise Jaccard 0.044-0.069, mean fraction 0.0999, differs from samtools -s (Jaccard 0.062)

**Key output (trimmed; full text in `run/out/`):**

```
PASS -s 42.1: every kept template has ALL its records (mates + secondary) kept 512 templates kept of 4828
PASS -s 42.1: about 10% of templates 0.106
PASS -s 42.1 twice: identical records
PASS bare -s 0.1 twice: byte-identical (text: "deterministic too") 1015 records
PASS bare -s 0.1 == --subsample 0.1 --subsample-seed 0 (text: "it means seed 0")
PASS --subsample 0.1 (no seed) differs from seed 0 on 1.24 (text: header-hash "auto" seed) auto 1001 vs seed0 1015 (text quotes 1001 vs 1015)
PASS --subsample 0.1 twice on the same file: identical (header-derived)
PASS samtools 1.24 --help documents --subsample-seed INT|auto with header hash --subsample-seed INT|auto
PASS sequential -s 1.5 then -s 2.25 (independent seeds): ~12.5% of original 1197 of 9601 = 0.125
PASS same seed: -s 1.5 then -s 1.25 keeps the same reads as direct -s 1.25 (nested 25%, not 12.5%) 2256 vs 2256
   trap: -s 1.084419 keeps 750 of 9601
PASS text: "-s 1.084419" keeps only ~8% of reads 0.078
PASS block with target 10M > total: rc 0, stderr says copied unchanged only 9595 primary reads, fewer than the target; copying unchanged
PASS coverage-matching guard: matched.bam == input.bam (9601 records, not ~8%) 9601
PASS all block outputs exist
PASS tumor-normal: tumor pulled down toward normal (within 10% of 5640) tumor_matched 5604 vs normal 5640
PASS coverage-matching target 3000 (primary count): within 10% of target 2849 primary reads (total 9595) err=-5.0%
PASS coverage-matching target 1000 (primary count): within 10% of target 922 primary reads (total 9595) err=-7.8%
PASS coverage-matching target 6000 (primary count): within 10% of target 5963 primary reads (total 9595) err=-0.6%
   edge target=9595 (total primary 9595): matched.bam 9601 records; rc=0; stderr='only 9595 primary reads, fewer than the target; copying unch'
   edge target=9594 (total primary 9595): matched.bam 9601 records; rc=0; stderr=''
   edge target=1 (total primary 9595): matched.bam 2 records; rc=0; stderr=''
PASS target == total -> unchanged copy
PASS target == total-1: keeps nearly everything (>=90%), not ~0 9601 of 9601
PASS pysam seed 42: all records of a kept template kept; ~10% templates 477 templates (0.099)
PASS pysam seed 1: all records of a kept template kept; ~10% templates 471 templates (0.098)
```


### Input 5 — Stress: [regression] Aligner-aware MAPQ table on five aligners (synthetic repeat genome, known multiplicity) and the real STAR RNA-seq BAM

**Prompt:** "Drop multi-mapped reads from BAMs made by BWA, Bowtie2, HISAT2, minimap2 and STAR." (SYNTHETIC 60 kb genome with exact and diverged repeats; REAL STAR BAM, 7042 primaries)

**Executed:** true (WSL science env alignment-files). **Scores:** Basic 36/40 | Specialized 56/60 | Total 92/100 ✅

**Result:** All thresholds in the fixed table remove 400/400 exact-repeat reads and keep 96-100% of unique reads; every number quoted in the prose (399/400, 374/400, 80/400, 5768) reproduces.

**Assertions:**
- [PASS] Every "drop ambiguous" and "high confidence" threshold read out of the table removes the 400 exact-repeat reads for BWA, Bowtie2, HISAT2, minimap2 and STAR — 0/400 survive in all ten cases
- [PASS] The same thresholds keep the unique reads — 2000/2000 BWA and Bowtie2, 1995/2000 HISAT2 and STAR, minimap2 -q 60 1927/2000
- [PASS] The numbers quoted in the prose reproduce (old -q 1 kept 399 Bowtie2, 374 HISAT2, 80 STAR) — exact match
- [PASS] The STAR facts hold: MAPQ only 0/1/3/255 with NH 5+/3-4/2/1, -q 4..255 equivalent, -e [NH]==1 == -q 255 (synthetic and real 5768) — (255,1) 5768, (3,2) 954, (1,3-4) 292, (0,5-6) 28 on the real BAM
- [PASS] -e [NH]==1 removes 400/400 exact repeats on HISAT2 and returns 0 silently (rc 0) on BWA, Bowtie2 and minimap2 as the text says; Bowtie2 max MAPQ is 42 — n=0 rc=0 stderr empty for the three NH-less aligners

**Key output (trimmed; full text in `run/out/`):**

```
   drop-ambiguous -q 1: exact-repeat kept 0/400; unique kept 2000/2000; diverged-repeat kept 309/320
   old/naive -q 1: exact-repeat kept 0/400
   drop-ambiguous -q 2: exact-repeat kept 0/400; unique kept 2000/2000; diverged-repeat kept 312/320
   old/naive -q 1: exact-repeat kept 399/400
   drop-ambiguous -q 255: exact-repeat kept 0/400; unique kept 1995/2000; diverged-repeat kept 308/320
   old/naive -q 1: exact-repeat kept 80/400
   drop-ambiguous -q 2: exact-repeat kept 0/400; unique kept 1995/2000; diverged-repeat kept 313/320
   old/naive -q 1: exact-repeat kept 374/400
   drop-ambiguous -q 1: exact-repeat kept 0/400; unique kept 1999/2000; diverged-repeat kept 313/320
   old/naive -q 1: exact-repeat kept 0/400
STAR MAPQ values over all primary mapped records: {0: 320, 1: 1, 3: 96, 255: 2303}
STAR (MAPQ, NH) -> n: {(0, 8): 320, (1, 3): 1, (3, 2): 96, (255, 1): 2303}
PASS STAR MAPQ 255 <=> NH==1; 3 <=> NH==2; 1 <=> NH 3-4; 0 <=> NH>4 (prose)
HISAT2 (MAPQ, NH) -> n: {(0, 2): 7, (0, 5): 20, (1, 2): 79, (1, 5): 299, (60, 1): 2308}
Bowtie2 MAPQ values: {0: 2, 1: 406, 6: 41, 7: 3, 11: 8, 12: 18, 15: 7, 16: 4, 17: 22, 18: 23, 23: 5, 25: 16, 26: 1, 30: 28, 31: 51, 32: 50, 33: 1, 35: 33, 37: 4, 40: 155, 42: 1842}
REAL STAR BAM (MAPQ, NH) -> n: {(0, 5): 10, (0, 6): 18, (1, 3): 174, (1, 4): 118, (3, 2): 954, (255, 1): 5768}
FAILS: []
```


### Input 6 — Scope Boundary: [regression] Expression (-e) and read-group filtering, version-introduction claims, composite insert-size request (real BAMs)

**Prompt:** "Keep proper pairs with insert 100-500, <=20% soft clip, NM<=3, and only read group X; and tell me which samtools release each option needs." (real nf-core PE, 1000G with two RG IDs, STAR RNA-seq; synthetic 9-read RG BAM)

**Executed:** true (WSL science env alignment-files). **Scores:** Basic 35/40 | Specialized 51/60 | Total 86/100 ⚠️

**Result:** -e recipes, -r/-R/-l and the new -n all behave as written; the fix added a wrong release number (-n arrived in samtools 1.23, not 1.24) and the composite insert-size request still exposes the signed-tlen trap the text never mentions.

**Assertions:**
- [PASS] The -e recipes equal tag/CIGAR truth (NM, cigar=~, sclen, combined with -F/-q, sclen/qlen, ![NM]) and an -e on an absent tag is silently empty — 229, 16, 28, 4206, 5628, 2 records match truth; [XY] rc 0, 0 rows, no warning
- [PASS] Read-group semantics match the text: -r takes the ID and also emits untagged reads, -e [RG]== is strict, -R file, -l LIBRARY, -n drops untagged, --expr accepted — 6 = 3 tagged + 3 untagged; -e 3; -n 3; -l 9601 of 9601; --expr == -e 5768
- [PASS] Real STAR BAM: -e [NH]==1 equals -q 255 — 5768 = 5768
- [FAIL] The version-introduction claims match the samtools NEWS (-e 1.12, sclen 1.16, --subsample seed 1.24, -n 1.24) — NEWS.md puts --exclude-no-read-group under Release 1.23 (16 Dec 2025), not 1.24; the other three are right (n11)

**Key output (trimmed; full text in `run/out/`):**

```
SYNTHETIC: 3 reads RG=a, 3 RG=b, 3 no RG; `-r a` returns 6 -> ['s0', 's1', 's2', 's6', 's7', 's8']
PASS fixed text: `-r a` also outputs reads that carry no RG tag (3 RG a + 3 untagged = 6) 6
PASS fixed text: -e '[RG]=="ID"' is strictly that read group (3) 3
PASS fixed text: -n -r a drops the untagged reads (3) rc=0 n=3
long option spelled as in SKILL.md (--exclude-no-read-group): rc 0 n 3
PASS fixed text: long option --exclude-no-read-group as written is accepted by 1.24 rc=0 n=3
long option spelled as in the 1.24 --help text (--exclude-no-read_group): rc 1 n 0
naive signed-tlen expression keeps 2109 records; the intended pair-symmetric set is 4225
FAIL SKILL.md warns that tlen is signed (an insert-size -e test needs both signs / abs), the trap that halves this result no mention of tlen in SKILL.md
after composite filter: templates with one mate only = 41 of 2133
PASS long option --expr (text: '-e (or --expr, since 1.12)') is accepted and == -e rc=0 n=5768
FAILS: ['SKILL.md warns that tlen is signed (an insert-size -e test needs both signs / abs), the trap that halves this result']
--subsample default seed now a header hash: NEWS line 27 sits under "Release 1.24 (9th July 2026)"; SKILL.md claims 1.24
-e filtering expressions in samtools view: NEWS line 1401 sits under "Release 1.12 (17th March 2021)"; SKILL.md claims 1.12
sclen keyword documentation: NEWS line 1035 sits under "Release 1.16 (18th August 2022)"; SKILL.md claims 1.16
--exclude-no-read-group / -n: NEWS line 133 sits under "Release 1.23 (16th December 2025)"; SKILL.md claims 1.24
FAIL --exclude-no-read-group / -n: NEWS release == claimed 1.24 Release 1.23 (16th December 2025)
installed samtools --help mentions: ['-n, --exclude-no-read_group']
FAILS: ['--exclude-no-read-group / -n: NEWS release == claimed 1.24']
```


### Input 7 — Adversarial: [regression] "Remove duplicates, keep unique high-confidence proper pairs, then run Manta" on an unmarked-duplicate BAM

**Prompt:** "Clean my BAM: remove duplicates, keep only unique high-confidence properly-paired primary reads, and I will run Manta (SV caller) on it." (planted BAM with UNMARKED duplicates, coordinate-sorted, name-sorted and shuffled; SYNTHETIC all-flags BAM; real 1000G and STAR BAMs)

**Executed:** true (WSL science env alignment-files). **Scores:** Basic 35/40 | Specialized 51/60 | Total 86/100 ✅

**Result:** The dedup trap is closed on all three sort orders and the supplementary/SV warning is correct; the text still says nothing about the discordant-pair signal that -f 2 destroys, or about orphaned mates (53 singletons after -F 3332 -q 30 on the 1000G BAM).

**Assertions:**
- [PASS] The Remove-Duplicates snippet yields 400 records from the unmarked BAM whether it is coordinate-sorted, name-sorted or shuffled, with every remaining template still paired — 400/400/400; 200 templates of size 2
- [PASS] The SV recipe -F 1024 keeps the supplementary reads that -F 2304/2308/3328/3332 remove, and the text warns about it — 1024 supplementary kept vs 0; "NOT -F 2304, 2308, 3328 or 3332" and "Cost of getting this wrong" present
- [PASS] The text warns before the command that -F 1024 is a no-op on an unmarked BAM — "silently removes nothing" within the Remove Duplicates section
- [PASS] "Primary is not unique" holds on real data — real STAR BAM: -F 2304 keeps 7042 primaries of which 1274 have NH>1; -q 255 keeps 5768

**Key output (trimmed; full text in `run/out/`):**

```
== A. the trap the first audit hit: -F 1024 on an unmarked BAM
PASS unmarked planted BAM: 500 records, 0 dup-flagged, plain -F 1024 keeps 500 (silent no-op)
PASS text now warns BEFORE the command that -F 1024 silently removes nothing on an unmarked BAM
PASS snippet on coordinate-sorted unmarked BAM: 400 kept rc=0 n=400
PASS snippet on NAME-sorted unmarked BAM: 400 kept rc=0 n=400 err=no duplicate-flagged reads; marking first
PASS shuffled fixture is a valid 500-record BAM, header @HD not coordinate-sorted after shuffle
PASS snippet on shuffled (unsorted, order random) unmarked BAM: 400 kept rc=0 n=400 err=no duplicate-flagged reads; marking first
PASS after markdup+-F 1024 every remaining template still has both mates 200 templates, sizes [2]
== B. the SV half of the request
PASS synthetic flags: -F 1024 keeps supplementary records (2048 present) 1024
PASS synthetic flags: -F 3332 -q 30 removes supplementary records (2048 present) 0
PASS synthetic flags: -F 2308 removes supplementary records (2048 present) 0
PASS synthetic flags: -F 3328 -q 1 removes supplementary records (2048 present) 0
PASS synthetic flags: -F 2304 removes supplementary records (2048 present) 0
PASS synthetic flags: -F 1280 -q 1 keeps supplementary records (2048 present) 503
PASS text warns SV callers need supplementary reads and gives -F 1024 only
   text on -f 2 / -q for SV callers: ['**Goal:** Choose a filter that matches what the downstream caller expects. Stripping supplementary alignments breaks SV callers; requiring proper-pair drops valid spliced RNA-seq reads.']
FAIL text explains that -f 2 (proper pair) would also discard the discordant-pair SV signal no mention of discordant pairs
   real 1000G BAM: supplementary 0, not-proper-pair mapped 109 of 9601; -F 1024 keeps 9500, -f 2 -F 3332 -q 30 keeps 9344
== C. orphaned mates after read-level filtering (not addressed in the text)
   1000G after -F 3332 -q 30: 53 single-record templates whose mate was mapped (of 4763 templates)
   lines mentioning orphan/singleton/fixmate in SKILL.md: 1 ['samtools collate -O -u input.bam tmp_collate | samtools fixmate -m -u - - | \\']
== D. "Primary is not unique"
PASS STAR real BAM: -F 2304 keeps multi-mapped primaries (text: "Primary is not unique") primary 7042, of which NH>1 1274; -q 255 5768
FAILS: ['text explains that -f 2 (proper pair) would also discard the discordant-pair SV signal']
```


### Input 8 — Variant B: [NEW] MAPQ table on REAL reads: 2821 DNA pairs and 3521 RNA-seq pairs re-aligned with BWA, Bowtie2 (e2e and local), HISAT2, minimap2, STAR

**Prompt:** "I aligned real reads with Bowtie2/HISAT2/BWA/STAR; which -q do I use to drop the ambiguous ones and keep the good ones?" (real nf-core reads re-aligned to the real 40 kb chr22 slice; second method: bowtie2 -k 10, original STAR NH)

**Executed:** true (WSL science env alignment-files). **Scores:** Basic 34/40 | Specialized 52/60 | Total 86/100 ✅

**Result:** The thresholds keep >= 99.9% of real mapped reads for BWA, Bowtie2, HISAT2 and STAR. The slice has no distinct-locus multi-mappers (bowtie2 -k 10 finds none; STAR NH>1 is alternative splicing at one locus), so "drop ambiguous" is not exercised on real data here. minimap2 -ax sr real reads: -q 60 keeps only 58.5%.

**Assertions:**
- [PASS] Table thresholds keep >= 97% of real mapped reads for BWA (-q 1/-q 30), Bowtie2 (-q 2/-q 23), HISAT2 (-q 2/-q 60), STAR (-q 255) on 2821 real DNA pairs — 100% / 99.9% / 100% / 99.9%
- [PASS] The Bowtie2 "MAPQ maxes at 42 end-to-end" statement holds on real reads — e2e max 42; --local max 44 (text restricts the statement to end-to-end)
- [PASS] -q 255 and -e [NH]==1 select the same real STAR records; the re-aligned RNA reads keep STAR MAPQ 255 for all NH==1 records — 5768 in the original BAM; STAR re-alignment: unique kept 5768/5768
- [PASS] The 3521 real RNA pairs re-aligned with each aligner keep the reads STAR calls unique (NH==1) under the table thresholds — BWA 5768/5768, HISAT2 2207/2207, minimap2 5711/5711, STAR 5768/5768; Bowtie2 -q 2 5084/5432 (93.6%, unspliced aligner on spliced reads)

**Key output (trimmed; full text in `run/out/`):**

```
PASS SKILL.md table row Bowtie2 present with the thresholds used here
PASS SKILL.md table row HISAT2 present with the thresholds used here
PASS SKILL.md table row STAR present with the thresholds used here
=== (A) real DNA pairs, 40 kb chr22 slice
  bwa: primary mapped 5640/5642; MAPQ {40: 1, 42: 1, 44: 1, 54: 1, 58: 1, 60: 5635}
     drop-ambiguous -q 1: keeps 5640/5640 (100.0%); high-confidence -q 30: keeps 5640/5640 (100.0%)
PASS bwa real DNA: -q 1 keeps >= 97% of mapped reads (non-repetitive slice) 1.000
PASS bwa real DNA: -q 30 keeps >= 85% of mapped reads 1.000
  bowtie2: primary mapped 5623/5642; MAPQ {3: 2, 8: 1, 23: 10, 24: 20, 40: 22, 42: 5568}
     drop-ambiguous -q 2: keeps 5623/5623 (100.0%); high-confidence -q 23: keeps 5620/5623 (99.9%)
PASS bowtie2 real DNA: -q 2 keeps >= 97% of mapped reads (non-repetitive slice) 1.000
PASS bowtie2 real DNA: -q 23 keeps >= 85% of mapped reads 0.999
  bowtie2_local: primary mapped 5628/5642; MAPQ {36: 2, 41: 4, 42: 28, 44: 5594}
     drop-ambiguous -q 2: keeps 5628/5628 (100.0%); high-confidence -q 23: keeps 5628/5628 (100.0%)
PASS bowtie2_local real DNA: -q 2 keeps >= 97% of mapped reads (non-repetitive slice) 1.000
PASS bowtie2_local real DNA: -q 23 keeps >= 85% of mapped reads 1.000
  hisat2: primary mapped 5586/5642; MAPQ {60: 5586}
     drop-ambiguous -q 2: keeps 5586/5586 (100.0%); high-confidence -q 60: keeps 5586/5586 (100.0%)
PASS hisat2 real DNA: -q 2 keeps >= 97% of mapped reads (non-repetitive slice) 1.000
PASS hisat2 real DNA: -q 60 keeps >= 85% of mapped reads 1.000
  minimap2: primary mapped 5570/5642; MAPQ {1: 1, 2: 20, 4: 1, 5: 1, 9: 1, 13: 1, 14: 1, 16: 1, 17: 4, 18: 3, 19: 3, 20: 3, 21: 4, 23: 5, 24: 2, 25: 2, 26: 1, 27: 1, 29: 1, 30: 2, 32: 3, 33: 1, 34: 1, 35: 4, 36: 2, 37: 3, 38: 4, 39: 1, 40: 8, 41: 3, 
     drop-ambiguous -q 1: keeps 5570/5570 (100.0%); high-confidence -q 60: keeps 3261/5570 (58.5%)
PASS minimap2 real DNA: -q 1 keeps >= 97% of mapped reads (non-repetitive slice) 1.000
  star: primary mapped 5604/5642; MAPQ {3: 4, 255: 5600}
     drop-ambiguous -q 255: keeps 5600/5604 (99.9%); high-confidence -q 255: keeps 5600/5604 (99.9%)
PASS star real DNA: -q 255 keeps >= 97% of mapped reads (non-repetitive slice) 0.999
PASS bowtie2 -k 10 finds no extra alignments on the real DNA slice (no multi-mappers to remove: the table is exercised on unique reads here) 5623 vs 5623
  Bowtie2 max MAPQ end-to-end 42, --local 44
PASS Bowtie2 end-to-end max MAPQ 42 on real reads (prose)
  Bowtie2 --local max MAPQ 44: text "23 is a community uniquely-mapped convention" and "maxes at 42" are stated for end-to-end only
=== (B) real RNA-seq pairs: multiplicity truth = NH of the real STAR alignment
  STAR NH>1 reads 1274; of these with >= 2 NON-OVERLAPPING alignment spans (distinct loci): 0
  bwa: re-mapped 7042; truth-multi reads mapped 0: survive drop-ambiguous -q 1: 0, high-conf -q 30: 0; truth-unique mapped 5768: survive -q 1: 5768 (100.0%)
  bowtie2: re-mapped 6636; truth-multi reads mapped 0: survive drop-ambiguous -q 2: 0, high-conf -q 23: 0; truth-unique mapped 5432: survive -q 2: 5084 (93.6%)
  hisat2: re-mapped 2457; truth-multi reads mapped 0: survive drop-ambiguous -q 2: 0, high-conf -q 60: 0; truth-unique mapped 2207: survive -q 2: 2207 (100.0%)
  minimap2: re-mapped 6917; truth-multi reads mapped 0: survive drop-ambiguous -q 1: 0, high-conf -q 60: 0; truth-unique mapped 5711: survive -q 1: 5711 (100.0%)
  star: re-mapped 7042; truth-multi reads mapped 0: survive drop-ambiguous -q 255: 0, high-conf -q 255: 0; truth-unique mapped 5768: survive -q 255: 5768 (100.0%)
  bowtie2 -k 10: reads with >1 reported alignment: 0; of these truth-multi (STAR NH>1): 0
  Bowtie2 default: reads with >1 alignment (per -k 10) surviving -q 2: 0 of 0
PASS Bowtie2 -q 2 removes every read that bowtie2 -k 10 itself reports at >1 locus 0 multi-locus reads
  hisat2: only 0 distinct-locus reads mapped by this aligner; no assertion (too few)
  star: only 0 distinct-locus reads mapped by this aligner; no assertion (too few)
  bowtie2: only 0 distinct-locus reads mapped by this aligner; no assertion (too few)
  bwa -q 1 leaves 0/0 of the truth-multi reads (BWA gives MAPQ 0 only to exact ties; real multi-mappers with a better hit get MAPQ>0)
```


### Input 9 — Scope Boundary: [NEW] The two rows the fixer left unverified: pbmm2/minimap2 long-read MAPQ rows and the assay-table caller rationale (real GATK runs)

**Prompt:** "Filter my PacBio HiFi and ONT BAMs for variant calling; and I will call germline with HaplotypeCaller and somatic with Mutect2: does the assay table's advice hold?" (SYNTHETIC 300 kb long-read repeat genome, pbmm2 26.2.99 + minimap2; REAL ARTIC nanopore BAM; REAL nf-core BAM with MAPQ set to 10 on 100 reads and 0 on 20, run through GATK 4.6.2.0 Mutect2 and HaplotypeCaller)

**Executed:** true (WSL science env alignment-files). **Scores:** Basic 34/40 | Specialized 50/60 | Total 84/100 ⚠️

**Result:** pbmm2 and minimap2 long-read rows are right (0/80 exact repeats, 300/300 unique kept; pbmm2 CCS MAPQ identical to minimap2 map-hifi for 580/580 reads). The somatic row rationale ("somatic callers handle low MAPQ") is contradicted by a real Mutect2 run: it filters the 120 MAPQ<20 reads itself. Strelka2, DeepVariant, clair3, Sniffles, cuteSV, Manta, GRIDSS, Delly, SvABA are not installed: unverified.

**Assertions:**
- [PASS] pbmm2 row (-q 1 drop ambiguous, -q 60 high confidence) removes the exact-repeat reads and keeps the unique ones for HiFi (CCS) and ONT (SUBREAD) profiles — 0/80 exact repeats, 300/300 unique at both thresholds; the SKILL.md text still says the row was not run, which is now checkable
- [PASS] The minimap2 long-read row (map-hifi, map-ont) behaves the same — 0/80 and 300/300; 8%-diverged copies keep MAPQ 60
- [PASS] The long-read recipe -F 3328 -q 5 and the SV recipe -F 1024 equal bit arithmetic on the real 4916-record ARTIC nanopore BAM — 4916 = 4916; the real BAM has no supplementary reads, so the SV claim is exercised on the synthetic flag BAM only
- [PASS] The germline row (-f 2 -F 3328 -q 20) is consistent with what HaplotypeCaller filters itself — real HaplotypeCaller run: MappingQualityReadFilter 120, NotSecondary 2 of 5642; --help lists MAPQ>=20, not-duplicate, not-secondary defaults
- [FAIL] The somatic row rationale "somatic callers handle low MAPQ" is supported for Mutect2 — real Mutect2 run filtered 120 of 5642 reads by MappingQualityReadFilter (MAPQ<20, default 20); Mutect2 also drops chimeric-original alignments by default

**Key output (trimmed; full text in `run/out/`):**

```
PASS SKILL.md pbmm2 row: `-q 1` drop ambiguous / `-q 60` high confidence
PASS SKILL.md minimap2 row: (DNA, long-read) `-q 1` / `-q 60`
PASS SKILL.md says the pbmm2 row was not run (honest caveat)
reads per class: {'u': 300, 'A2': 80, 'B3': 120, 'C2': 80} (u unique; A2 exact x2; B3 1% x3; C2 8% x2)
-- pbmm2_hifi: 580 primary records; MAPQ summary per class (min/median/max, share of MAPQ 60, share of MAPQ 0)
PASS pbmm2_hifi: samtools -q 1 / -q 60 retention == direct MAPQ count
   -q 1 keeps: unique 300/300, exact repeat 0/80, 1%-diverged 120/120, 8%-diverged 80/80
   -q 60 keeps: unique 300/300, exact repeat 0/80, 1%-diverged 120/120, 8%-diverged 80/80
-- pbmm2_ont: 580 primary records; MAPQ summary per class (min/median/max, share of MAPQ 60, share of MAPQ 0)
PASS pbmm2_ont: samtools -q 1 / -q 60 retention == direct MAPQ count
   -q 1 keeps: unique 300/300, exact repeat 0/80, 1%-diverged 120/120, 8%-diverged 80/80
   -q 60 keeps: unique 300/300, exact repeat 0/80, 1%-diverged 104/120, 8%-diverged 80/80
-- mm2_hifi: 580 primary records; MAPQ summary per class (min/median/max, share of MAPQ 60, share of MAPQ 0)
PASS mm2_hifi: samtools -q 1 / -q 60 retention == direct MAPQ count
   -q 1 keeps: unique 300/300, exact repeat 0/80, 1%-diverged 120/120, 8%-diverged 80/80
   -q 60 keeps: unique 300/300, exact repeat 0/80, 1%-diverged 120/120, 8%-diverged 80/80
-- mm2_ont: 580 primary records; MAPQ summary per class (min/median/max, share of MAPQ 60, share of MAPQ 0)
PASS mm2_ont: samtools -q 1 / -q 60 retention == direct MAPQ count
   -q 1 keeps: unique 300/300, exact repeat 0/80, 1%-diverged 120/120, 8%-diverged 80/80
   -q 60 keeps: unique 300/300, exact repeat 0/80, 1%-diverged 109/120, 8%-diverged 80/80
PASS pbmm2_hifi: table `-q 1` ("drop ambiguous") removes 80/80 exact-repeat reads 0 survive
PASS pbmm2_hifi: table `-q 60` ("high confidence") removes 80/80 exact-repeat reads 0 survive
PASS pbmm2_hifi: `-q 60` keeps >= 90% of unique reads 300/300
PASS pbmm2_hifi: `-q 1` keeps >= 97% of unique reads 300/300
PASS pbmm2_ont: table `-q 1` ("drop ambiguous") removes 80/80 exact-repeat reads 0 survive
PASS pbmm2_ont: table `-q 60` ("high confidence") removes 80/80 exact-repeat reads 0 survive
PASS pbmm2_ont: `-q 60` keeps >= 90% of unique reads 300/300
PASS pbmm2_ont: `-q 1` keeps >= 97% of unique reads 300/300
PASS mm2_hifi: minimap2 row `-q 1` removes 80/80 exact repeats 0
PASS mm2_hifi: minimap2 row `-q 60` removes 80/80 exact repeats and keeps >= 90% unique exact 0, unique 300/300
---- GATK (real runs, n10) ----
set MAPQ 10 on 100 reads and MAPQ 0 on 20 reads
records MAPQ<20 & >0: 5622 minus 5522  => 100; MAPQ 0 mapped: 5642 - 5622
===== Mutect2
03:31:31.777 INFO  Mutect2 - 120 read(s) filtered by: MappingQualityReadFilter
122 total reads filtered out of 5642 reads processed
===== HaplotypeCaller
03:31:35.650 INFO  HaplotypeCaller - 120 read(s) filtered by: MappingQualityReadFilter
122 total reads filtered out of 5642 reads processed
PASS GATK HaplotypeCaller default filters: MAPQ>=20, not duplicate, not secondary (consistent with the germline row -F 3328 -q 20) min MAPQ 20
PASS Mutect2 default filters also enforce MAPQ>=20 (so "somatic callers handle low MAPQ" is not what GATK Mutect2 does) min MAPQ 20
PASS Mutect2 default filters include NonChimericOriginalAlignmentReadFilter (chimeric reads dropped by the caller itself)
SKILL.md somatic row: | Somatic short-variant (Mutect2, Strelka2) | `-F 1280 -q 1` | Drop only MAPQ=0; somatic callers handle low MAPQ; supplementary (chimeric) reads are kept because they may carry real somatic SNVs |
FAIL SKILL.md somatic row claim "somatic callers handle low MAPQ" is supported for Mutect2 CONTRADICTED by GATK: Mutect2 drops MAPQ<20 by default
Rows not verifiable here (callers not installed): Strelka2, DeepVariant, clair3, Sniffles, cuteSV, Manta, GRIDSS, Delly, SvABA -> stated as unverified in the report
FAILS: ['SKILL.md somatic row claim "somatic callers handle low MAPQ" is supported for Mutect2']
```


## Independent checks beyond the inputs

- **Snippet smoke** (`run/r0_snippets_smoke.py`, every fenced block of SKILL.md and usage-guide.md from a copy): 24 blocks, 18 clean, 6 with warning/failure
```
WARN SKILL.md:78   bash   rc=0 stdout_lines=0     no duplicate-flagged reads; marking first
WARN SKILL.md:146  bash   rc=0 stdout_lines=0     [main_samview] region "chr1:1000000-2000000" specifies an invalid region or unknown reference. Continue anyway
WARN SKILL.md:151  bash   rc=0 stdout_lines=0     [main_samview] region "chr1:1000-2000" specifies an invalid region or unknown reference. Continue anyway.
WARN SKILL.md:229  bash   rc=0 stdout_lines=0     only 5642 primary reads, fewer than the target; copying unchanged
FAIL SKILL.md:323  python rc=1 stdout_lines=0     Traceback (most recent call last):
WARN usage-guide.md:8    bash   rc=0 stdout_lines=1     /mnt/openscience/audits/bio-alignment-filtering/run/data/w0/blk_usage_0.sh: line 2: conda: command not found
```
The four WARN/FAIL blocks on `chr1` and `conda` are fixture artifacts (chr22 BAM; no conda in the env); the other two warnings are the snippets' own intended messages.

- **usage-guide.md dedup:** compared the archived pre-fix usage-guide with the fixed one. Every deleted block (FLAG table, `samtools flags 99/147`, `-f/-F` patterns, region/subsample/output commands, three pysam variants, MAPQ error table, troubleshooting, tips) has a counterpart in SKILL.md, except the pysam class variant and `count_with_filter`, which are variants of `passes_filter` and `samtools view -c`. Nothing an agent needs was lost; the contradicting `-F 2308` "standard" and the false "-s 0.1 non-reproducible" advice were dropped correctly.
- **Assay-table caller rationale** (fixer left it unverified): only GATK is installed. Real HaplotypeCaller and Mutect2 runs on a BAM with 100 MAPQ-10 and 20 MAPQ-0 reads: both filter all 120 through MappingQualityReadFilter (min 20). Germline row is consistent; the somatic rationale is contradicted. Strelka2, DeepVariant, clair3, Sniffles, cuteSV, Manta, GRIDSS, Delly, SvABA remain unverified.
- **pbmm2 row** (fixer left it unrun): verified on synthetic 2 kb reads in HiFi and ONT error profiles: same MAPQ semantics as minimap2 (CCS vs map-hifi identical for 580/580 reads).
- **Version claims:** `-e` 1.12, `sclen` 1.16 and the 1.24 default-seed change match samtools NEWS.md; `-n` does not (1.23).
- **Determinism (T3):** all subsampling recipes are seeded; reruns identical (r4). **Security (T4):** no eval/exec; filter_bam.py validates the region string.

## Static evaluation (25 criteria, 8 categories)

| Category | Score | Note |
|---|---|---|
| functional_suitability | 10/12 | Completeness 3: covers flags, MAPQ per aligner, regions, BED, assay recipes, subsampling, -e, read groups, pysam and output; gaps the fixer noticed and left (orphaned mates, signed tlen, discordant pairs). Correctness 3: every recipe runs and matches truth, but a wrong release number (-n), a contradicted caller rationale and an over-claimed BED equivalence remain. Appropriateness 4. |
| reliability | 9/12 | Fault tolerance 3: filter_bam.py validates regions, index and sort order and the snippets guard target>total and unmarked duplicates; the pysam BED recipe still crashes on space-delimited BED and mishandles zero-width rows. Error reporting 3: clean messages from the script, samtools stays silent (rc 0) on an absent contig but the text says so. Recoverability 3: every command writes a new file, none touches the input. |
| performance_context | 7/8 | SKILL.md 426 lines / ~20 KB with tables carrying most content; usage-guide reduced to 64 lines with no duplicated recipes. Token cost 3, execution efficiency 4. |
| agent_usability | 14/16 | Learnability 4; consistency 3 (input.bam / in.bam / mapped.bam naming shifts between blocks); feedback design 3 (count-before-write advice, script prints Kept/Removed and warnings); error prevention 4 (each trap carries a checked number). |
| human_usability | 6/8 | Discoverability 3: the description does not mention subsampling, duplicate removal or read groups, all covered; forgiveness 3 (strict region parsing is correct for this category). |
| security | 11/12 | No credentials, no eval/exec, region strings validated; bash blocks use unquoted variable expansion of user paths (input validation 3). |
| maintainability | 10/12 | One SKILL.md, a slim usage-guide and one runnable example; no references/ directory; flag lists still appear in two forms (table and breakdown list). Modularity 3, modifiability 3, testability 4 (checked numbers in the text, runnable example script). |
| agent_specific | 17/20 | Trigger precision 3; progressive disclosure 3 (no references, but under 500 lines); composability 4 (Related Skills, explicit hand-offs to duplicate-handling, sorting, indexing); idempotency 4; escape hatches 3 (SV warning, "no universal threshold", pbmm2 caveat, but caller rows are not marked unverified). |

**Static subtotal: 84/100** (first audit 74).

## Vetoes

Skill Veto: PASS on all four (stability, contract, determinism, security). Research Veto (Data Analysis): PASS on M1-M4 (see JSON detail). No veto override.

## Recommendations

**[P2] -n (--exclude-no-read-group) arrived in 1.23, not 1.24** (observed in inputs [6])
- Problem: "Samtools 1.24 adds -n (--exclude-no-read-group)" is wrong: samtools NEWS.md lists the option under Release 1.23 (16 Dec 2025). The fix log recorded it as 1.24 without the release heading.
- Root cause: Version claim taken from a NEWS entry without checking which release section it sits under.
- Fix: Write "Samtools 1.23 adds -n (--exclude-no-read-group)". The 1.24 --help spells the long option --exclude-no-read_group; the hyphenated form in the text also works on 1.24 (checked).

**[P2] Somatic-row rationale contradicted by a real Mutect2 run** (observed in inputs [9])
- Problem: "Somatic callers handle low MAPQ" is not what a real Mutect2 run does: 120 of 5642 reads (MAPQ 10 and 0) were removed by its MappingQualityReadFilter (default minimum 20), and by default it also drops chimeric-original alignments. The assay table does not say that no caller row was run.
- Root cause: Caller behaviour written from memory; only aligner/flag behaviour was tested.
- Fix: Reword the somatic row: -F 1280 -q 1 is only a light pre-filter because Mutect2 applies MAPQ>=20, not-secondary, not-duplicate and non-chimeric filters itself. Add one line that the caller-specific rationale comes from caller documentation and was not run for Strelka2, DeepVariant, clair3, Sniffles, cuteSV, Manta, GRIDSS, Delly, SvABA.

**[P2] pysam BED recipe differs from -L on zero-width/space rows** (observed in inputs [3])
- Problem: The text says the recipe gives "the same records as samtools view -L". 13 of 81 fuzz BEDs differ, each with a start==end row (samtools returns the reads covering base s; fetch(c, s, s) returns nothing), and a space-delimited BED raises IndexError at parts[2].
- Root cause: The fix was validated on one zero-width row placed where no reads exist, and on tab-delimited BED only.
- Fix: Say "tab-delimited BED with start < end", or make the recipe match: parts = line.split(); end = max(int(parts[2]), int(parts[1]) + 1).

**[P2] Three known filter pitfalls still missing from the text** (observed in inputs [6, 7])
- Problem: (1) Read-level filters leave orphaned mates (53 single-record templates after -F 3332 -q 30 on the 1000G BAM); (2) -f 2 would also discard the discordant pairs an SV caller needs, but the SV rows only say "-F 1024 only"; (3) tlen is signed, so "-e tlen>=100 && tlen<=500" keeps 2109 of the 4225 intended records.
- Root cause: The fix log lists them as "needs a new section, not a correction".
- Fix: Add a short "Pitfalls" section: samtools fixmate after read-level filtering when pairing matters; do not add -f 2 for SV callers; use abs(tlen)-style symmetric tests in -e.

**[P2] minimap2 row silent about short-read MAPQ ceilings** (observed in inputs [8])
- Problem: The minimap2 row says "(DNA, long-read)" and -q 60. With -ax sr on real Illumina reads -q 60 kept only 58.5% of uniquely mapped reads (unique MAPQ mostly 48-59); on synthetic reads 96%.
- Root cause: The row was checked only for long reads.
- Fix: State that -q 60 is for long-read presets; for -x sr use -q 1 for "drop ambiguous" and a lower high-confidence value (measured MAPQ 48-59 for unique real reads).

## Run record

Scripts in `run/` (all executed): `00_setup.sh`, `make_synthetic_flags.py`, `make_repeat_genome.py`, `lib.py`, `W.sh`, `r0_snippets_smoke.py`, `r1_standard.py`, `r2_flags.py`, `r3_regions.py`, `r4_subsample.py`, `r5_align.sh`, `r5_mapq.py`, `r6_expr.py`, `r7_adversarial.py`, `n8_align_real.sh`, `n8_analyze.py`, `n9_make_longreads.py`, `n9_align_long.sh`, `n9_analyze.py`, `n10_caller_docs.sh`, `n10_caller_assert.py`, `n10_mutect2_run.sh`, `n11_news_check.py`, `build_report.py`. Raw outputs: `run/out/`. `run/skill/` is the copy of the fixed Skill everything ran from. Large intermediate BAMs were deleted after the runs (scripts regenerate them). The pre-fix report is archived under `_pre-fix-20260920/`.
