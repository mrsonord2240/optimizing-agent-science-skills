> **Audit record for `bio-bam-statistics`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@c8b1af2](https://github.com/mrsonord2240/bioSkills/tree/c8b1af2148fd4b8e6c667f4feb080cee03cd3551/alignment-files/bam-statistics) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-20 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer - bio-bam-statistics (second re-audit)

Generated: 2026-09-20. Source: `mrsonord2240/bioSkills@c8b1af2148fd4b8e6c667f4feb080cee03cd3551:alignment-files/bam-statistics`. Previous score 84 (Limited Release, one P1). All runs are in `run/` (scripts) and `run/out/` (recorded outputs); the Skill was run from `run/skill/` (byte-identical to the worktree HEAD).

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|
| 1 | Canonical | 38 | 56 | 94 | 5/5 PASS | ✅ |
| 2 | Variant A | 37 | 55 | 92 | 5/5 PASS | ✅ |
| 3 | Edge | 37 | 54 | 91 | 4/5 PASS | ✅ |
| 4 | Variant B | 37 | 54 | 91 | 4/5 PASS | ✅ |
| 5 | Stress | 36 | 53 | 89 | 4/4 PASS | ✅ |
| 6 | Scope Boundary | 35 | 50 | 85 | 4/5 PASS | ✅ |
| 7 | Adversarial | 37 | 53 | 90 | 5/5 PASS | ✅ |

**Execution Average: 90.3 / 100**  |  **Assertion Pass Rate: 31/34 (91.2%)**  |  **Static: 85 / 100**  |  **Final: 88 / 100, Production Ready, deployable, no veto, no open P0/P1**

Floors for Production Ready: static >= 80 (85), execution >= 85 (90.3), Layer 1 avg >= 32 (36.7), Layer 2 avg >= 48 (53.6), assertions >= 90% (91.2%): all met.

## Skill Veto and Research Veto

T1 stability PASS (every recipe run; 10 identical reruns), T2 contract PASS (frontmatter name/description present; shipped files present: `examples/qc_report.py`, `usage-guide.md`, all Related Skills exist), T3 determinism PASS (`run/out/t0_stability_determinism.txt`: 1 distinct output for qc_report.py, the -aa recipe, flagstat, region_depth_stats), T4 security PASS (no eval/exec/subprocess/credentials; grep clean). Research veto (Data Analysis): M1 to M4 PASS (details in the JSON).

## Static evaluation (85 / 100)

| Category | Score | Note |
|---|---|---|
| functional_suitability | 11/12 | Completeness 4 (flagstat/idxstats/stats/depth/coverage/mosdepth/pysam, uBAM and CRAM handling, assay table), Correctness 3 (every runnable claim held; two small imprecisions, see P2), Appropriateness 4. |
| reliability | 10/12 | Fault tolerance 4: empty, SE, unindexed, uBAM, CRAM with and without reference, truncated, text and zero-byte inputs all end in a correct result or exit 1 with a message. Error reporting 3: wrong-reference CRAM says only "truncated file"; bare snippets still raise raw pysam errors. Recoverability 3. |
| performance_context | 6/8 | 497-line SKILL.md with everything in one file and no references/ folder; duplication removed in round 2 (Quick Reference, Output to File). Token cost 3, efficiency 3. |
| agent_usability | 14/16 | Learnability 4, Consistency 3, Feedback design 3 (outputs shown, exit-1 messages specified), Error prevention 4 (denominator, cap, overlap, flagstat units, contig-name traps named with the safe command). |
| human_usability | 6/8 | Discoverability 3 (generic description), Forgiveness 3. |
| security | 11/12 | No credentials; paths quoted; no eval/exec/subprocess in shipped code (grep clean). Input validation 3: user paths pass straight to samtools/pysam. |
| maintainability | 9/12 | Modularity 3, Modifiability 3 (recipes now live once), Testability 3: checked-on notes and one runnable example, but no shipped test data or expected outputs. |
| agent_specific | 18/20 | Trigger 3, Progressive disclosure 3 (497 lines, no references/), Composability 4, Idempotency 4, Escape hatches 4 (What Flagstat Does Not Reveal, exit-1 guards, honest "not run end to end"). |

## What Round 2 changed and what I found

| Round-2 target | Verdict from my runs |
|---|---|
| qc_report.py on unaligned BAM | FIXED. uBAM (edge `ubam_no_sq.bam`, 30 records) equals flagstat; text SAM and truncated/text/zero-byte files exit 1 with one line. (`out/t3_edge.txt`, `out/t7_adversarial.txt`, `out/n3_cram_bad_insert.txt`) |
| qc_report.py and snippets on CRAM with / without reference | FIXED. With FASTA: equal to flagstat on own CRAM (5 variants) and the real human CRAM. Without a reachable reference: rc 1 + hint. Trap found while testing: `samtools view -C -T` writes `UR:` into the header, so a CRAM decodes "without a reference" as long as that path exists or the htslib cache holds it (`out/n3_`, `n3b_`, `n3c_`). Wrong-reference message weak (P2). |
| depth -aa -b on read-less contigs | FIXED. 3110 rows (planted-depth), ctgB 800 rows (own_ctg); `-a` drops them (2810 / 0), as stated. (`out/t2_planted.txt`, `out/n2_own_ctg.txt`) |
| mosdepth summary note | CORRECT. 19000 of 22000 bp, 2.95x vs 2.57x; 20100 of 25100 bp, 5.98x vs 4.79x. `--fast-mode` deletion statement correct but incomplete (spliced N also counted): P2. |
| MAX_INSERT | Documented and correct for qc_report (mean 2286 = truth), but stats clamps at the cap rather than dropping (3555.5): P2. |
| Per-tool overlap table | CORRECT on the real BAM to 2 decimals for every row; bcftools INFO/DP 16.77 with and without -x verified independently (also on own_del). The fixer's two counter-claims are right, the earlier re-audit sentences were wrong. |
| Removed Quick Reference table; usage-guide dedup | Nothing lost: each removed row is a command elsewhere (`git diff 377e368 c8b1af2`); usage-guide is overview + prompts + pointer. |
| FREEMIX / somalier labelling | Honest and accurate: VerifyBamID2 on a synthetic 40x chr20 BAM stops with "Insufficient Available markers" (no FREEMIX), somalier extract needs a whole-GRCh38 FASTA. Numbers themselves stay unsourced: P2. |

Defects introduced by Round 2: none that changes a result. Cosmetic: pysam pileup on CRAM prints a "multiple_iterators not implemented for CRAM" UserWarning; htslib prints "[E::cram_index_load]" for an unindexed CRAM although reading succeeds.

## Detailed Outputs

Inputs 1, 3, 4 (partly), 5, 6, 7 re-run the previous auditor inputs (their generators are `g0_generate.sh`, `make_synth.py`, `make_depth.py`, `make_edge.py`, `g1_mt.sh`); the `n*_` scripts are my NEW inputs. Data made here is SYNTHETIC with truth by construction (`data/`, `data/new/`); real data is `audit-envs/alignment-files/public-data/` (read only).

### Input 1 - Canonical: Get alignment statistics and coverage from my BAM: REAL human chr22-slice PE BAM and REAL 1000G chr20 BAM, plus region depth on the real 1000G and RNA BAMs

**Prompt:** Get alignment statistics and coverage from my BAM file (human PE slice, and a 1000 Genomes slice with 101 duplicate-flagged reads). Give me mapping rate, per-contig counts, insert size, mean depth and the fraction at 10x and 20x. Then give me mean depth and >=20x for a region of my 1000G slice and of my spliced RNA-seq BAM.

**Executed:** true. **Scripts (in `run/`):** `t0_stability_determinism.sh`, `t1_canonical.sh`, `t1b_depth_real.sh`, `n5_real_region.sh (+ n5_real_region.py)`, `n9_file_blocks.sh`

**Result:** [t0, t1_canonical.sh, t1b_depth_real.sh, n5_real_region.sh, n9_file_blocks.sh] flagstat, idxstats, stats fields, coverage and the summary-table row equal record-flag truth on both real BAMs (5644/5642/5640/5638; 1000G 9601/9595/9557/9450/101 dup). Block 017 (-aa) prints 16.77x / 2.43% / 2.34% = alignment-block truth (16.7743/2.4299/2.3424); the old 568x average still reproduces only as the documented warning. region_depth_stats equals block-truth and samtools depth -a on 9 real windows of the 1000G slice (dup-flagged reads excluded) and the spliced RNA BAM (N-skips excluded). Determinism: 10 identical reruns of qc_report.py, the -aa recipe, flagstat and region_depth_stats.

Output excerpt `out/t1b_depth_real.txt` (lines matching `block 017|mean 16|TRUTH|raw depth|region \[|OK\]`):

```
TRUTH default (mates twice): mean 16.7743  >=10x 2.4299%  >=20x 2.3424%  covered 1181 (2.952%) max 2532
TRUTH mates once          : mean 8.8603  >=10x 2.3549%  >=20x 2.0024%
TRUTH mean over covered positions only (the OLD wrong denominator): 568.153
=== block 017 (Mean Depth and Breadth, verbatim, -aa)
mean 16.77x  >=10x 2.43%  >=20x 2.34%
=== block 017 with region (as the comment says: -a -r region in the same pipe)
mean 16.77x  >=10x 2.43%  >=20x 2.34%
=== block 014 warning: raw depth average (must reproduce the 568x claim)
raw depth avg over covered positions: 568.153
[OK] region [0,40001) mean 16.7743 (truth 16.7743, samtools depth -a 16.7743) covered 1181/1181 max 2532/2532 >=10x 2.430/2.430 >=20x 2.342/2.342
[OK] region [1950,4700) mean 243.9960 (truth 243.9960, samtools depth -a 243.9960) covered 1181/1181 max 2532/2532 >=10x 35.345/35.345 >=20x 34.073/34.073
[OK] region [2999,3000) mean 1562.0000 (truth 1562.0000, samtools depth -a 1562.0000) covered 1/1 max 1562/1562 >=10x 100.000/100.000 >=20x 100.000/100.000
[OK] region [30000,40001) mean 0.0000 (truth 0.0000, samtools depth -a 0.0000) covered 0/0 max 0/0 >=10x 0.000/0.000 >=20x 0.000/0.000
```

Output excerpt `out/n5_real_region.txt` (lines matching `REAL_REGION|1000G|RNA`):

```
1000G chr20 [1400000,1500000) mean 9.4877 truth 9.4877 samtools_depth_a 9.4877 max 33/33 covered 98442/98442 ge20 4.315/4.315 rows_ok=True mismatches=[]
1000G chr20 [1400000,1400500) mean 7.1360 truth 7.1360 samtools_depth_a 7.1360 max 14/14 covered 500/500 ge20 0.000/0.000 rows_ok=True mismatches=[]
1000G chr20 [1450000,1450001) mean 5.0000 truth 5.0000 samtools_depth_a 5.0000 max 5/5 covered 1/1 ge20 0.000/0.000 rows_ok=True mismatches=[]
1000G chr20 [1499000,1500500) mean 6.8167 truth 6.8167 samtools_depth_a 6.8167 max 17/17 covered 1086/1086 ge20 0.000/0.000 rows_ok=True mismatches=[]
1000G chr20 [1300000,1400000) mean 0.0027 truth 0.0027 samtools_depth_a 0.0027 max 6/6 covered 68/68 ge20 0.000/0.000 rows_ok=True mismatches=[]
RNA chr22 [0,40001) mean 23.6651 truth 23.6651 samtools_depth_a 23.6651 max 2960/2960 covered 7607/7607 ge20 3.325/3.325 rows_ok=True mismatches=[]
RNA chr22 [0,5000) mean 3.3376 truth 3.3376 samtools_depth_a 3.3376 max 55/55 covered 639/639 ge20 8.480/8.480 rows_ok=True mismatches=[]
RNA chr22 [10000,20000) mean 0.8588 truth 0.8588 samtools_depth_a 0.8588 max 19/19 covered 1855/1855 ge20 0.000/0.000 rows_ok=True mismatches=[]
RNA chr22 [39990,40001) mean 0.0000 truth 0.0000 samtools_depth_a 0.0000 max 0/0 covered 0/0 ge20 0.000/0.000 rows_ok=True mismatches=[]
REAL_REGION_MISMATCHES 0
=== recipe block 017 (-aa) vs samtools coverage on the REAL RNA BAM and the 1000G slice region
```

**Scores:** Basic 38/40 | Specialized 56/60 | Total 94/100

**Assertions:**
- [PASS] Block 017 (-aa recipe) prints the block-truth mean and >=10x/>=20x on the real human BAM (16.77x / 2.43% / 2.34%) - Equal to alignment-block truth 16.7743 / 2.4299 / 2.3424.
- [PASS] flagstat, idxstats, stats and the block-005 summary row equal record-flag hand counts on both real BAMs - All 8 fields per BAM equal; 1000G reports 101 duplicates as truth.
- [PASS] region_depth_stats equals alignment-block truth and samtools depth -a on real spliced RNA and real 1000G windows (mean, covered, max, >=10x, >=20x) - 9 windows, 0 mismatches, incl. 1-bp, zero-depth and past-the-data windows; N-skips and duplicate-flagged reads handled.
- [PASS] The 568x raw-average trap is reproduced and the Skill warns about it - raw depth avg 568.153 vs true 16.77.
- [PASS] Identical inputs give identical outputs across 10 runs - md5 of 10 qc_report.py outputs: 1 distinct.

### Input 2 - Variant A: What fraction is covered at 10x/20x when some contigs have no reads: previous auditor planted-depth BAM (regression) + my own_ctg.bam (NEW)

**Prompt:** My reference has a 5 kb contig with no reads and a 100 bp contig with 50x. What is the mean depth and the % of the genome at >=10x and >=20x, what does mosdepth report, and give me the depth for a target list that includes the empty contig.

**Executed:** true. **Scripts (in `run/`):** `t2_planted.sh`, `n2_own_ctg.sh (+ n2_region_truth.py, n1_make_new_data.py)`

**Result:** [t2_planted.sh, n2_own_ctg.sh, n2_region_truth.py] Truth by construction. planted-depth (22000 bp, 4 contigs, chrC read-less): recipe prints 2.57x / 9.32% / 5.68% exactly; -a prints 2.97x as the Skill says. Block 021 (depth -aa -b) now gives 3110 rows (was 2810) and -a still 2810 as the Skill states. own_ctg (25100 bp, ctgB read-less): -aa recipe 4.79x / 42.23% / 2.39% = truth 4.788845 / 42.2311 / 2.3904; -a gives 5.98x; mosdepth summary total covers 20100 of 25100 bp and 5.98x, exactly the note in SKILL.md; -aa -b keeps ctgB (800 rows) and -a drops it; coverage-from-BED loop, mosdepth --by and region_depth_stats (22 windows, BAM and CRAM+reference) equal truth.

Output excerpt `out/t2_planted.txt`:

```
TRUTH all 4 contigs (22000 bp): mean 2.568182 ge10 9.3182% ge20 5.6818% covered 2550 max 100
TRUTH mates once: mean 2.545455; ge10 9.3182% ge20 5.4545%
TRUTH if the denominator is only contigs with reads (19000 bp): mean 2.973684   ge10 10.7895%
=== block 017 verbatim (depth -aa, every @SQ position)
mean 2.57x  >=10x 9.32%  >=20x 5.68%
=== same recipe but with -a (SKILL: -a omits contigs that have no reads)
mean 2.97x  >=10x 10.79%  >=20x 6.58%
row counts: depth (no -a) / -a / -aa  (all @SQ = 22000, without chrC = 19000)
3060
19000
22000
contigs present in -a / -aa output
  10000 chrA
   5000 chrB
```

Output excerpt `out/n2_own_ctg.txt`:

```
TRUTH total_len 25100 (contigs with reads 20100) sum_depth 120200 | mean over ALL 4.788845 | mean over contigs-with-reads 5.980100 | >=10x 42.2311% >=20x 2.3904% | max 50 covered 10600
TRUTH flagstat {'records': 1105, 'secondary': 3, 'supplementary': 4, 'primary': 1098, 'qcfail_primary': 7, 'passed_primary': 1091, 'primary_mapped_passed': 1085, 'primary_dup': 5, 'unmapped': 6}
=== flagstat -O tsv (first rows)
1098	7	total (QC-passed reads + QC-failed reads)
1091	7	primary
3	0	secondary
4	0	supplementary
5	0	duplicates
5	0	primary duplicates
1092	7	mapped
99.45%	100.00%	mapped %
=== block 017 verbatim (depth -aa)
mean 4.79x  >=10x 42.23%  >=20x 2.39%
=== same with -a (Skill: -a omits contigs with no reads) -> expect mean over contigs-with-reads
mean 5.98x  >=10x 52.74%  >=20x 2.99%
=== raw depth mean (Skill warning): 11.3396
rows depth / -a / -aa:
10600
20100
25100
=== samtools coverage (all contigs)
#rname	startpos	endpos	numreads	covbases	coverage	meandepth
ctgA	1	20000	1034	10500	52.5	5.76
ctgC	1	100	50	100	100	50
ctgB	1	5000	0	0	0	0
=== mosdepth default summary (Skill: total covers only contigs that have reads, 20100 of 25100 bp)
chrom	length	bases	mean	min	max
ctgA	20000	115200	5.76	0	30
ctgC	100	5000	50.00	50	50
total	20100	120200	5.98	0	50
mosdepth total: 20100 bp, mean 5.98 ; contigs-with-reads truth 5.98
=== block 021 (depth -aa -b) with a BED touching the read-less contig ctgB, ctgC and ctgA (truth rows: 1000+500+100+50+300 = 1950)
ctgA 1050
ctgB 800
ctgC 100
-a form:
ctgA 1050
ctgC 100
=== block 025 coverage-from-BED loop
ctgA	1	1000	100	1000	100	10
ctgB	101	600	0	0	0	0
ctgC	1	100	50	100	100	50
```

**Scores:** Basic 37/40 | Specialized 55/60 | Total 92/100

**Assertions:**
- [PASS] Block 017 (-aa) prints the truth mean and breadth on both planted BAMs (2.57x/9.32%/5.68%; 4.79x/42.23%/2.39%) - Exact to the printed digits.
- [PASS] Skill claim: depth -a -b drops regions on read-less contigs, -aa keeps them (2810 vs 3110 rows; ctgB 0 vs 800) - Reproduced on both BAMs; block 021 verbatim prints 3110.
- [PASS] Skill claim: mosdepth summary total covers only contigs with reads (19000 of 22000 bp, 2.95x vs 2.57x) - Also 20100 of 25100 bp, 5.98x vs 4.79x on own_ctg.
- [PASS] region_depth_stats equals truth by construction on read-less, 1-bp, contig-end and supplementary windows, on BAM and CRAM with reference= - 35 windows, 0 mismatches; supplementary reads count, dup/QC-fail/secondary do not, like samtools depth.
- [PASS] coverage-from-BED loop and mosdepth --by agree with truth incl. the read-less contig and a track header line - ctgB rows 0.00; header line skipped, no "Failed to parse region".

### Input 3 - Edge: Planted flag categories (secondary, supplementary, QC-fail, duplicate, unmapped, singleton) on 21 BAMs incl. an unaligned BAM + my own planted counts + insert-size boundary

**Prompt:** Run a QC report on this BAM: it has secondary and supplementary alignments, QC-failed reads, duplicates and unmapped reads, and one of my files is an unaligned BAM with no @SQ lines. Are the counts the same as flagstat? Also what insert size does the report give for my mate-pair-like library with templates up to 8500 bp?

**Executed:** true. **Scripts (in `run/`):** `t3_edge.sh`, `n8_own_counts.sh`, `n3_cram_bad_insert.sh (part b)`, `n3b_cram_isolated.sh (part b)`

**Result:** [t3_edge.sh, n8_own_counts.sh, n3_cram_bad_insert.sh (b), n3b_cram_isolated.sh] qc_report.py and the Count Reads snippet equal flagstat -O tsv (QC-passed column and percentages) and record-flag hand counts on 21/21 BAMs including the unaligned BAM (previously a ValueError traceback) and empty/all-QC-fail (message, no ZeroDivisionError); my own_ctg planted counts (1105 records, 3 secondary, 4 supplementary, 7 QC-fail, 5 dup, 1085 mapped passed primary) equal qc_report, flagstat and the plant. The cross-check identity now holds (540-10-10=520=raw total sequences). Insert boundary: qc_report keeps 0<tlen<8000 (mean 2286, matches truth), but samtools stats -i 8000 CLAMPS longer templates to 8000 instead of dropping them (stats mean 3555.5; predicted clamp 3555.5, verified with -i 7000 and -i 400), so the "MAX_INSERT = the samtools stats default" wording hides that the two means differ.

Output excerpt `out/t3_edge.txt` (lines matching `PASS|FAIL|TOTAL|EXPECTED`):

```
PASS flagstat total(pass+fail) == hand total observed= 540 expected= 540
PASS flagstat secondary == hand observed= 10 expected= 10
PASS flagstat supplementary == hand observed= 10 expected= 10
PASS flagstat duplicates == hand observed= 40 expected= 40
PASS flagstat mapped == hand mapped(all records) observed= 525 expected= 525
PASS flagstat primary mapped == hand observed= 505 expected= 505
PASS flagstat properly paired == hand (primary) observed= 480 expected= 480
PASS flagstat singletons == hand observed= 5 expected= 5
PASS flagstat mate diff chr == hand observed= 20 expected= 20
PASS flagstat mate diff chr mq5 == hand observed= 20 expected= 20
PASS stats raw total sequences == hand primary observed= 520 expected= 520
PASS stats reads QC failed == hand observed= 20 expected= 20
PASS stats reads mapped == hand primary_mapped observed= 505 expected= 505
PASS idxstats mapped col sum == hand mapped (all records incl sec/supp) observed= 525 expected= 525
PASS idxstats unmapped col sum == hand unmapped (placed + * lines) observed= 15 expected= 15
PASS Skill cross-check eq holds (pass+fail) observed= 520 expected= 520
```

Output excerpt `out/n8_own_counts.txt`:

```
PASS own_ctg.bam  primary=1091 qcfail=7 sec=3 supp=4 028rc=0 qc_report_rc=0
PASS own_insert.bam  primary=36 qcfail=0 sec=0 supp=0 028rc=0 qc_report_rc=0
PASS own_del.bam  primary=60 qcfail=0 sec=0 supp=0 028rc=0 qc_report_rc=0
TOTAL_MISMATCHES 0
PASS qc_report/flagstat vs planted truth: records observed 1105 planted 1105
PASS qc_report/flagstat vs planted truth: secondary observed 3 planted 3
PASS qc_report/flagstat vs planted truth: supplementary observed 4 planted 4
PASS qc_report/flagstat vs planted truth: qcfail primary observed 7 planted 7
PASS qc_report/flagstat vs planted truth: passed primary observed 1091 planted 1091
PASS qc_report/flagstat vs planted truth: mapped (passed primary) observed 1085 planted 1085
PASS qc_report/flagstat vs planted truth: primary duplicates observed 5 planted 5
PASS qc_report/flagstat vs planted truth: flagstat total pass+fail observed 1105 planted 1105
PLANTED_TRUTH_MISMATCHES 0

```

Output excerpt `out/n3_cram_bad_insert.txt` (lines matching `TRUTH qc_report|qc_report.py\]|Insert size|insert size average|inward|block 030`):

```
TRUTH qc_report rule (0 < tlen < 8000): n=14 mean=2285.6 median(upper)=300 | rule <=8000: n=15 mean=2666.6 | all pairs: n=18 mean=3611.1
[qc_report.py]
Insert size (mean): 2286
Insert size (median): 300
insert size average:	3555.5
inward oriented pairs:	18
insert size average:	3611.1
[block 030 snippet (no cap)]
```

Output excerpt `out/n3b_cram_isolated.txt` (lines matching `predicted|samtools stats -i`):

```
########## samtools stats -i behaviour: clamp or drop? own_insert: 300x10, 7000x3, 7999, 8000, 8001, 8500x2
-i 8000: predicted mean if CLAMPED 3555.5 | if DROPPED (<=i) 2666.6
-i 7000: predicted mean if CLAMPED 3277.8 | if DROPPED (<=i) 1846.2
-i 400: predicted mean if CLAMPED 344.4 | if DROPPED (<=i) 300.0
samtools stats -i 8000: 3555.5
samtools stats -i 7000: 3277.8
samtools stats -i 400: 344.4
```

**Scores:** Basic 37/40 | Specialized 54/60 | Total 91/100

**Assertions:**
- [PASS] qc_report.py and Count Reads equal flagstat and hand counts on all planted-flag BAMs, incl. uBAM, empty and all-QC-fail - 0 mismatches on 21 BAMs.
- [PASS] Counts equal the counts planted by construction (own_ctg: 1105/3/4/7/5/1085; edge expected.json 9 BAMs) - PLANTED_TRUTH_MISMATCHES 0, EXPECTED_JSON_MISMATCHES 0.
- [PASS] Cross-check identity flagstat_total(pass+fail) - secondary - supplementary = stats raw total sequences holds - 540-10-10 = 520 = 520; negative control (pass column only) differs, as the Skill now states.
- [PASS] Unaligned BAM with no @SQ gives correct counts, not a traceback - 30 primary, 0 mapped, rc 0 (round-2 fix confirmed).
- [FAIL] MAX_INSERT wording (samtools stats default) predicts what stats does with templates above the cap - qc_report drops them (mean 2286); samtools stats clamps them to 8000 (mean 3555.5), so the two reports disagree on such libraries.

### Input 4 - Variant B: Depth caps and mate-overlap: 9500x stack, real ARTIC BAM, my own_del.bam (deletions, spliced reads, overlapping mates), disputed claims

**Prompt:** My amplicon and RNA data have deep stacks, spliced reads and overlapping mates. Which tools cap depth, which count overlapping mates twice, does mosdepth count deletions and splice gaps, and does bcftools mpileup INFO/DP change with -x?

**Executed:** true. **Scripts (in `run/`):** `t4_depth_cap.sh`, `n4_disputed_claims.sh (+ n4_overlap_del.py)`

**Result:** [t4_depth_cap.sh, n4_disputed_claims.sh, n4_overlap_del.py, t1b_depth_real.sh] Every default in the cap table reproduced on a 9500x stack (depth uncapped, -d ignored; coverage -d 1000000; mosdepth uncapped; mpileup 8000; bcftools 250; pysam 8000). ARTIC real BAM: recipe, coverage and pysam helper 68.8373x = truth. Overlap table on the real human BAM: depth/coverage/pysam/fast-mode 16.77, depth -s and mosdepth 8.86, mpileup 8.85 / -x 16.75 / -Q 0 16.77, bcftools FORMAT/DP 8.85 default and 16.77 with -x or -Q 0. The two claims the earlier re-audit got wrong were verified independently: (1) mosdepth default does NOT count D (68.84 = depth -aa, own_del sum 4700 = mates once, D/N uncovered) while --fast-mode counts D (69.97 = depth -J; own_del 9600); (2) bcftools INFO/DP is 16.77x with or without -x on the real BAM and 5200 = mates-twice truth in every own_del variant. New: --fast-mode also counts spliced N bases as covered (real RNA BAM mosdepth 17.67x default vs 49.40x fast-mode vs 23.67x depth -aa; own_del D+N truth 9600) and samtools mpileup depth counts D and N too (own_del -Q 0: 9600 vs depth 5200); the Skill names only D.

Output excerpt `out/t4_depth_cap.txt`:

```
=== block 018 table, claim by claim (truth max 9500, mean 1000)
samtools depth default (claimed: uncapped)
  max=9500 mean(sum/1000)=1000.00 rows=1000
samtools depth -d 100 (claimed: silently ignored)
  max=9500 mean(sum/1000)=1000.00 rows=1000
samtools coverage default (claimed -d 1000000)
#rname	startpos	endpos	numreads	covbases	coverage	meandepth
amp	1	1000	10000	200	20	1000
  -d, --depth INT         maximum allowed coverage depth [1000000].
samtools coverage -d 8000 (shows the cap is real)
#rname	startpos	endpos	numreads	covbases	coverage	meandepth
amp	1	1000	10000	200	20	850
mosdepth (claimed uncapped)
total	1000	1000000	1000.00	0	9500
samtools mpileup default (claimed 8000)
8000
samtools mpileup -d 1000000 (claimed fix)
9500
bcftools mpileup default (claimed 250)
250
bcftools mpileup -d 1000000 (claimed fix)
9500
pysam pileup default max_depth (claimed 8000) and max_depth=1_000_000
  default: 8000
```

Output excerpt `out/n4_disputed_claims.txt`:

```
TRUTH sums: default(mates twice, D/N uncovered) 5200 | mates once 4700 | D+N covered 9600
samtools depth -aa                           sum  5200 mean 1.7333  == truth_default True | matesonce False | D+N covered False
samtools depth -aa -s                        sum  4700 mean 1.5667  == truth_default False | matesonce True | D+N covered False
samtools depth -aa -J (include deletions)    sum  5600 mean 1.8667  == truth_default False | matesonce False | D+N covered False
mosdepth default                             sum  4700 mean 1.5667  == truth_default False | matesonce True | D+N covered False
mosdepth --fast-mode                         sum  9600 mean 3.2000  == truth_default False | matesonce False | D+N covered True
samtools mpileup default (-Q13)              sum  9040 mean 3.0133  == truth_default False | matesonce False | D+N covered False
samtools mpileup -x                          sum  9540 mean 3.1800  == truth_default False | matesonce False | D+N covered False
samtools mpileup -Q 0                        sum  9600 mean 3.2000  == truth_default False | matesonce False | D+N covered True
samtools mpileup -Q 0 -x                     sum  9600 mean 3.2000  == truth_default False | matesonce False | D+N covered True
samtools mpileup -B                          sum  9100 mean 3.0333  == truth_default False | matesonce False | D+N covered False
bcftools mpileup default  FORMAT/DP          sum  4680 mean 1.5600  == truth_default False | matesonce False | D+N covered False
bcftools mpileup default  INFO/DP            sum  5200 mean 1.7333  == truth_default True | matesonce False | D+N covered False
bcftools mpileup -x  FORMAT/DP               sum  5180 mean 1.7267  == truth_default False | matesonce False | D+N covered False
bcftools mpileup -x  INFO/DP                 sum  5200 mean 1.7333  == truth_default True | matesonce False | D+N covered False
bcftools mpileup -Q 0  FORMAT/DP             sum  5200 mean 1.7333  == truth_default True | matesonce False | D+N covered False
bcftools mpileup -Q 0  INFO/DP               sum  5200 mean 1.7333  == truth_default True | matesonce False | D+N covered False
bcftools mpileup -B  FORMAT/DP               sum  4700 mean 1.5667  == truth_default False | matesonce True | D+N covered False
bcftools mpileup -B  INFO/DP                 sum  5200 mean 1.7333  == truth_default True | matesonce False | D+N covered False
bcftools mpileup -B -x  FORMAT/DP            sum  5200 mean 1.7333  == truth_default True | matesonce False | D+N covered False
bcftools mpileup -B -x  INFO/DP              sum  5200 mean 1.7333  == truth_default True | matesonce False | D+N covered False
=== REAL human BAM: bcftools mpileup INFO/DP vs FORMAT/DP with / without -x  (sum over printed positions / 40001)
bcftools mpileup -d 1000000  : INFO/DP mean 16.77  FORMAT/DP mean 8.85
bcftools mpileup -d 1000000 -x : INFO/DP mean 16.77  FORMAT/DP mean 16.77
bcftools mpileup -d 1000000 -Q 0 : INFO/DP mean 16.77  FORMAT/DP mean 16.77
bcftools mpileup -d 1000000 -B : INFO/DP mean 16.77  FORMAT/DP mean 8.85
=== REAL ARTIC BAM: mosdepth default vs --fast-mode vs depth -aa vs depth -aa -J (deletions)
total	29903	2058441	68.84
total	29903	2092344	69.97
depth -aa: 68.8373
depth -aa -J: 69.9710
=== REAL RNA BAM (spliced): mosdepth default vs --fast-mode vs depth -aa (does fast-mode also count N?)
total	40001	706625	17.67
total	40001	1975850	49.40
depth -aa: 23.6651 (n=40001)
=== flag names in the overlap paragraph
  -x, --ignore-overlaps-removal, --disable-overlap-removal
  -s           Do not count overlapping reads within a template

```

**Scores:** Basic 37/40 | Specialized 54/60 | Total 91/100

**Assertions:**
- [PASS] Every default in the depth-cap table reproduces on a 9500x stack and the pysam helper returns mean 1000.0 / max 9500 - All 7 tools; helper equals truth.
- [PASS] Overlap table row values reproduce on the real human BAM (16.77 / 8.86 / 8.85 / 16.75 / 16.77, bcftools 8.85 / 16.77) - Each to 2 decimals; -x/--ignore-overlaps-removal flag names exist in --help.
- [PASS] Claim: mosdepth counts deletions as covered only with --fast-mode (default 68.84 = depth -aa) - ARTIC 68.84 vs 69.97; own_del default 4700 vs fast 9600. The earlier re-audit sentence was wrong.
- [PASS] Claim: bcftools INFO/DP is 16.77x with or without -x - Human BAM 16.77 for default, -x, -Q 0, -B; own_del INFO/DP sum 5200 in all variants.
- [FAIL] The --fast-mode caveat is complete for spliced (RNA) data - Fast-mode also counts N skips (RNA 49.40x vs 17.67x default); the Skill mentions only deletions.

### Input 5 - Stress: Summary table for 15 BAMs, plot-bamstats, MultiQC, stats GC-depth, mosdepth command block and quantize, CRAM in mosdepth

**Prompt:** Create a summary table of statistics for all my samples (15 BAMs of every kind, one file name has a space), make the QC plots and a MultiQC report, and run the mosdepth exome, quantize and CRAM commands.

**Executed:** true. **Scripts (in `run/`):** `t5_batch_plots.sh`, `n6_misc_claims.sh`, `n9_file_blocks.sh`

**Result:** [t5_batch_plots.sh, n6_misc_claims.sh, n9_file_blocks.sh] Block 005 verbatim ran on 15 BAMs (real, synthetic, empty, uBAM, QC-fail-heavy, unmapped-only); all 15 rows equal record-flag hand counts, incl. 101 duplicates on 1000G and 220 QC-failed; the space-in-file-name run (t7) also works; own_ctg row 1105/7/1098/1092/0/5. plot-bamstats wrote 11 PNGs; MultiQC 1.35 found the stats, flagstat and idxstats reports and built a 2.2 MB report. Region stats raw total 1760 = samtools view -c -F 2304; depth files 1181 / 40001 / 40001 rows. mosdepth exome thresholds row and --quantize bands equal the block truth (0:1 38820 bp, 1:10 239, 10:100 298, 100:inf 644); mosdepth -f on a CRAM works with .crai and errors "must be indexed" without it. The stats -r GC-depth wording matches --help; GCD row counts are identical with and without -r at the same bin size (not falsified, not confirmed).

Output excerpt `out/t5_batch_plots.txt`:

```
15
=== block 005 verbatim
Sample               Records  QCfail  Primary  PrimaryMapped  ProperPair  PrimaryDup
artic_nanopore       4916     0       4916     4916           0           0
edge_all_qcfail      10       10      10       10             0           0
edge_mixed_pairs     90       0       90       80             25          0
edge_qcfail_heavy    420      220     400      400            340         140
edge_supp_sec_heavy  610      0       110      100            0           0
edge_ubam_no_sq      30       0       30       0              0           0
edge_unmapped_only   120      0       120      0              0           0
empty                0        0       0        0              0           0
g1000                9601     0       9595     9557           9450        101
human_pe             5644     0       5642     5640           5638        0
human_rna            8828     0       7042     7042           7042        0
planted_dups         500      0       500      500            500         0
rf                   200      0       200      200            200         0
sc2_se               100      0       100      100            0           0
synthetic_flags      540      20      520      505            480         40
=== rows vs hand counts (truth.py)
['Sample', 'Records', 'QCfail', 'Primary', 'PrimaryMapped', 'ProperPair', 'PrimaryDup']
PASS ['artic_nanopore', '4916', '0', '4916', '4916', '0', '0'] 
PASS ['edge_all_qcfail', '10', '10', '10', '10', '0', '0'] 
PASS ['edge_mixed_pairs', '90', '0', '90', '80', '25', '0'] 
PASS ['edge_qcfail_heavy', '420', '220', '400', '400', '340', '140'] 
PASS ['edge_supp_sec_heavy', '610', '0', '110', '100', '0', '0'] 
PASS ['edge_ubam_no_sq', '30', '0', '30', '0', '0', '0'] 
```

Output excerpt `out/n6_misc_claims.txt`:

```
=== SKILL mosdepth block (line-by-line, placeholders filled)
mosdepth -t 2 --by exome.bed --thresholds 1,10,20,30,100 --no-per-base sample input.bam   # exome QC
mosdepth -t 2 --quantize 0:1:10:100: sample input.bam                                # CNV-style bands
mosdepth -t 2 -f ref.fa sample c.cram                                            # CRAM: needs the reference and a .crai
total	40001	354421	8.86
chr22	1951	4617	unknown	1181	942	801	776	644
chr22 0 1951 0:1
chr22 1951 1964 1:10
chr22 1964 1977 10:100
chr22 1977 2108 100:inf
chr22 2108 2114 10:100
--- mosdepth -f ref on CRAM with .crai / without
total	20100	120200	5.98
[mosdepth] error alignment file must be indexed
=== truth quantize: chr22 covered positions 1181 of 40001 -> bands: expect 0:1 (zero), 1:10 ... (count rows)
10:100 10 298
1:10 11 239
0:1 6 38820
100:inf 4 644
=== samtools coverage: any overlap option? (Skill: none)
0
  -b, --bam-list FILE     list of input BAM filenames, one per line
  -l, --min-read-len INT  ignore reads shorter than INT bp [0]
  -q, --min-MQ INT        mapping quality threshold [0]
  -Q, --min-BQ INT        base quality threshold [0]
  -d, --depth INT         maximum allowed coverage depth [1000000].
```

Output excerpt `out/n9_file_blocks.txt`:

```
region stats raw total sequences: 1760 ; independent: samtools view -c -F 2304 input.bam chr22:1952-2952 = 1760
depth.txt rows 1181 (covered positions 1181)
depth_with_zeros rows 40001 ; depth_all_contigs rows 40001 (contig 40001 bp)
block 008 first recipe total mapped: 5642 ; stats 'reads mapped' incl secondary: independent samtools view -c -F 4 = 5642
stats.txt lines: 1917

```

**Scores:** Basic 36/40 | Specialized 53/60 | Total 89/100

**Assertions:**
- [PASS] Batch loop rows equal hand counts on 15 BAMs (incl. empty, uBAM, QC-fail, dup) - BATCH_FAILS 0.
- [PASS] plot-bamstats produces the plots and MultiQC builds a report from the text outputs - 11 PNGs; report 2272085 bytes with samtools stats, flagstat and idxstats sections.
- [PASS] mosdepth exome/quantize/CRAM commands run and their output equals truth - Quantized band lengths sum to 40001; CRAM total 20100 bp / 5.98x on own_ctg.
- [PASS] Blocks that only write files produce the right content (stats region, depth, depth -a, depth -aa) - 1760 = 1760; 1181, 40001, 40001 rows.

### Input 6 - Scope Boundary: Mate-pair insert size, adapter read-through soft-clipping, Picard HsMetrics, VerifyBamID2/somalier hand-offs, assay thresholds and unverified-number labelling

**Prompt:** Is my library adapter-contaminated? Give me the soft-clipped fraction, off-target rate for my capture panel, whether the sample is contaminated (FREEMIX) or swapped, and whether my numbers are normal for ATAC/WES/RNA-seq.

**Executed:** true. **Scripts (in `run/`):** `t6_scope.sh`, `t6b_qc_insert_cap.sh`, `t10_vb2.sh (+ t10_make_vb2_data.py)`, `t11_basesmapped.sh`, `t8_misc_claims.sh`

**Result:** [t6_scope.sh, t6b_qc_insert_cap.sh, t10_vb2.sh, t11_basesmapped.sh, t8_misc_claims.sh] The soft-clip awk recipe equals a CIGAR walk with pysam on 11 BAMs under gawk and mawk, and stats bases mapped minus bases mapped (cigar) equals the soft-clipped bases on the two real BAMs (863; 59137); the old grep still returns nothing. RF library: stats reports IS with outward pairs dominating, proper flag set or unset; qc_report.py reports 2000 with the flag set (MAX_INSERT 8000) and prints no insert line when it is unset, as the Skill says. Picard BedToIntervalList and CollectHsMetrics run (PCT_OFF_BAIT 0, MEAN_TARGET_COVERAGE 131.06). VerifyBamID2 end to end on a synthetic chr20 BAM reads the 10k panel, sees 204 markers and stops with "Insufficient Available markers" (no FREEMIX produced); somalier extract fails without a whole-GRCh38 FASTA; the Skill labels both "not run end to end here". The assay table and FREEMIX cut-offs have no source.

Output excerpt `out/t6_scope.txt` (lines matching `PASS|SOFTCLIP|PCT_|MEAN_TARGET|independent|insert size average|outward|Insufficient|No reads found|not found|contamination`):

```
=== A. mate-pair (RF) library, proper flag SET and UNSET: what stats reports (Skill: IS reported, outward counts dominate) and what the pysam tools do
SN	insert size average:	2000.0
SN	outward oriented pairs:	100
SN	insert size average:	2000.0
SN	outward oriented pairs:	100
PASS [awk] clip.bam: recipe='soft-clipped bases: 110 of 510 (21.57%)' rc=0 | truth(cigartuples)=soft-clipped bases: 110 of 510 (21.57%) | stats grep -ci soft = 0
PASS [mawk] clip.bam: recipe='soft-clipped bases: 110 of 510 (21.57%)' rc=0 | truth(cigartuples)=soft-clipped bases: 110 of 510 (21.57%) | stats grep -ci soft = 0
PASS [awk] test.paired_end.sorted.bam: recipe='soft-clipped bases: 863 of 671854 (0.13%)' rc=0 | truth(cigartuples)=soft-clipped bases: 863 of 671854 (0.13%) | stats grep -ci soft = 0
PASS [mawk] test.paired_end.sorted.bam: recipe='soft-clipped bases: 863 of 671854 (0.13%)' rc=0 | truth(cigartuples)=soft-clipped bases: 863 of 671854 (0.13%) | stats grep -ci soft = 0
PASS [awk] test.rna.paired_end.sorted.bam: recipe='soft-clipped bases: 61703 of 1012528 (6.09%)' rc=0 | truth(cigartuples)=soft-clipped bases: 61703 of 1012528 (6.09%) | stats grep -ci soft = 0
PASS [mawk] test.rna.paired_end.sorted.bam: recipe='soft-clipped bases: 61703 of 1012528 (6.09%)' rc=0 | truth(cigartuples)=soft-clipped bases: 61703 of 1012528 (6.09%) | stats grep -ci soft = 0
PASS [awk] HG00349.chr20_1400000-1500000.bam: recipe='soft-clipped bases: 5457 of 965257 (0.57%)' rc=0 | truth(cigartuples)=soft-clipped bases: 5457 of 965257 (0.57%) | stats grep -ci soft = 0
PASS [mawk] HG00349.chr20_1400000-1500000.bam: recipe='soft-clipped bases: 5457 of 965257 (0.57%)' rc=0 | truth(cigartuples)=soft-clipped bases: 5457 of 965257 (0.57%) | stats grep -ci soft = 0
PASS [awk] sars-cov-2_v5.3.2.nanopore.bam: recipe='soft-clipped bases: 59137 of 2141066 (2.76%)' rc=0 | truth(cigartuples)=soft-clipped bases: 59137 of 2141066 (2.76%) | stats grep -ci soft = 0
PASS [mawk] sars-cov-2_v5.3.2.nanopore.bam: recipe='soft-clipped bases: 59137 of 2141066 (2.76%)' rc=0 | truth(cigartuples)=soft-clipped bases: 59137 of 2141066 (2.76%) | stats grep -ci soft = 0
PASS [awk] synth.bam: recipe='soft-clipped bases: 400 of 50500 (0.79%)' rc=0 | truth(cigartuples)=soft-clipped bases: 400 of 50500 (0.79%) | stats grep -ci soft = 0
PASS [mawk] synth.bam: recipe='soft-clipped bases: 400 of 50500 (0.79%)' rc=0 | truth(cigartuples)=soft-clipped bases: 400 of 50500 (0.79%) | stats grep -ci soft = 0
PASS [awk] supp_sec_heavy.bam: recipe='soft-clipped bases: 0 of 10000 (0.00%)' rc=0 | truth(cigartuples)=soft-clipped bases: 0 of 10000 (0.00%) | stats grep -ci soft = 0
PASS [mawk] supp_sec_heavy.bam: recipe='soft-clipped bases: 0 of 10000 (0.00%)' rc=0 | truth(cigartuples)=soft-clipped bases: 0 of 10000 (0.00%) | stats grep -ci soft = 0
PASS [awk] unmapped_only.bam: recipe='no primary mapped reads: nothing to compute' rc=1 | truth(cigartuples)=no primary mapped -> expect rc 1 + message | stats grep -ci soft = 0
PASS [mawk] unmapped_only.bam: recipe='no primary mapped reads: nothing to compute' rc=1 | truth(cigartuples)=no primary mapped -> expect rc 1 + message | stats grep -ci soft = 0
PASS [awk] all_qcfail.bam: recipe='soft-clipped bases: 0 of 1000 (0.00%)' rc=0 | truth(cigartuples)=soft-clipped bases: 0 of 1000 (0.00%) | stats grep -ci soft = 0
PASS [mawk] all_qcfail.bam: recipe='soft-clipped bases: 0 of 1000 (0.00%)' rc=0 | truth(cigartuples)=soft-clipped bases: 0 of 1000 (0.00%) | stats grep -ci soft = 0
PASS [awk] empty.bam: recipe='no primary mapped reads: nothing to compute' rc=1 | truth(cigartuples)=no primary mapped -> expect rc 1 + message | stats grep -ci soft = 0
PASS [mawk] empty.bam: recipe='no primary mapped reads: nothing to compute' rc=1 | truth(cigartuples)=no primary mapped -> expect rc 1 + message | stats grep -ci soft = 0
PASS [awk] ubam_no_sq.bam: recipe='no primary mapped reads: nothing to compute' rc=1 | truth(cigartuples)=no primary mapped -> expect rc 1 + message | stats grep -ci soft = 0
PASS [mawk] ubam_no_sq.bam: recipe='no primary mapped reads: nothing to compute' rc=1 | truth(cigartuples)=no primary mapped -> expect rc 1 + message | stats grep -ci soft = 0
SOFTCLIP_MISMATCHES 0
PCT_OFF_BAIT 0
PCT_SELECTED_BASES 1
```

Output excerpt `out/t10_vb2.txt`:

```
markers 204 reads 8160
NOTICE - Number of marker in Reference Matrix:10000
NOTICE - Number of marker shared with input file:204
NOTICE - Mean Depth:40.000000
NOTICE - SD Depth:0.000000
NOTICE - 204 SNP markers remained after sanity check.

WARNING - 
Insufficient Available markers, check input bam depth distribution in output pileup file after specifying --OutputPileup
ls: cannot access 'sample_vb*': No such file or directory
```

Output excerpt `out/t11_basesmapped.txt`:

```
stats-eligible reads: sum(query_length)= 48500  sum(M/=/X)= 48100  softclip= 400  ins= 0
stats bases mapped: 50500  bases mapped (cigar): 50600
--- same fields on the real human BAM and the ARTIC BAM (stats vs CIGAR walk)
bases mapped:	671854 bases mapped (cigar):	670991 | walk: query bases of mapped primary = 671854, M/=/X bases = 670989
bases mapped:	2141066 bases mapped (cigar):	2081929 | walk: query bases of mapped primary = 2141066, M/=/X bases = 2058441
```

**Scores:** Basic 35/40 | Specialized 50/60 | Total 85/100

**Assertions:**
- [PASS] Soft-clip recipe equals a CIGAR walk on real, synthetic and hand-built CIGARs and exits 1 with a message on empty output - SOFTCLIP_MISMATCHES 0 over 11 BAMs x 2 awks.
- [PASS] Picard CollectHsMetrics/BedToIntervalList commands run and give plausible values - PCT_SELECTED_BASES 1, PCT_OFF_BAIT 0, mean target coverage 131.06 vs depth -s 132.94 / depth 251.68 (mates-once vs twice).
- [PASS] Mate-pair (RF) claims: stats reports IS with outward pairs, pysam tools skip when the proper flag is unset - mean 2000.0, outward 100, flag set and unset; qc_report 0.00% proper, no insert lines.
- [PASS] Contamination hand-offs are labelled as not run end to end and the flags exist - verifybamid2 flags in --help, .dat prefix requirement reproduced, VB2 end-to-end gave no FREEMIX, somalier needs GRCh38: the label is accurate.
- [FAIL] Assay-threshold values and the FREEMIX 1% / 5% cut-offs are backed by a source or by a run - Labelled "literature ranges, not verified" / "commonly cited"; no citation, nothing runnable here.

### Input 7 - Adversarial: Empty, SE, unindexed BAM, Ensembl MT contig, space in name, unaligned BAM, CRAM (reference, embedded, no reference, dead UR, WRONG reference), truncated / text / zero-byte files

**Prompt:** Run the QC report on whatever I have: an empty BAM, a single-end BAM, a BAM without an index, a BAM where the mitochondrion is called MT, an unaligned BAM, several CRAMs (some without their reference, one against the wrong FASTA) and three broken files.

**Executed:** true. **Scripts (in `run/`):** `t7_adversarial.sh`, `n3_cram_bad_insert.sh`, `n3b_cram_isolated.sh`, `n3c_cram_no_ur.sh`, `n7_errmsgs.sh`, `t9_syntax_sweep.sh`, `t8_misc_claims.sh`, `g1_mt.sh`

**Result:** [t7_adversarial.sh, n3_cram_bad_insert.sh, n3b_cram_isolated.sh, n3c_cram_no_ur.sh, n7_errmsgs.sh, t8_misc_claims.sh, t9_syntax_sweep.sh] Empty/SE/MT/unindexed give correct results or an exit-1 message (mito 7.62% on chrM and on MT; "no mapped reads" on a zero-read MT). uBAM: qc_report and Count Reads equal flagstat. CRAM with reference (own and real human): qc_report equals flagstat; CRAM whose @SQ UR is dead and no reference: exit 1 with "CRAM cannot be decoded without its reference: pass the FASTA as 2nd argument"; Count Reads on it raises the OSError the Skill documents and works with reference_filename=; embedded-reference and unindexed CRAM decode with no reference; unindexed CRAM: region_depth_stats -> "no index available for pileup", as documented. Truncated, text-named and zero-byte files: qc_report exits 1 with a one-line message (samtools quickcheck agrees). Wrong-reference CRAM: exit 1 but the message says only "truncated file" (htslib lines above it say MD5 mismatch). Every recipe on a zero-length or unknown-contig region gives a clear ValueError. All 31 executable blocks parse.

Output excerpt `out/t7_adversarial.txt`:

```
=== Skill pysam counters (block 027) + qc_report.py vs flagstat, hand counts: empty / SE / real SE / MT / unindexed
PASS empty.bam  primary=0 qcfail=0 sec=0 supp=0 028rc=1 qc_report_rc=0
PASS se.bam  primary=55 qcfail=0 sec=0 supp=0 028rc=0 qc_report_rc=0
PASS real se sample.bam  primary=100 qcfail=0 sec=0 supp=0 028rc=0 qc_report_rc=0
PASS synth_MT.bam  primary=500 qcfail=20 sec=10 supp=10 028rc=0 qc_report_rc=0
PASS noindex.bam  primary=55 qcfail=0 sec=0 supp=0 028rc=0 qc_report_rc=0
TOTAL_MISMATCHES 0
--- raw outputs on empty.bam
no QC-passed primary reads
block027 rc=1
=== QC Report: empty.bam ===

Total records:     0 (primary 0 + secondary 0 + supplementary 0)
QC-failed primary: 0 (excluded below)
QC-passed primary: 0
No QC-passed primary reads: nothing to report
qc_report rc=0
no properly paired read1 records (single-end data, or proper-pair flag unset: see Insert Size Caveats)
block030 rc=1
--- block 027 on real SE BAM
Primary QC-passed: 100
Mapped: 100 (100.00% of primary)
Single-end data: no paired reads
rc=0
=== depth-based recipes on empty.bam (header has 1 contig, 1000 bp, no reads)
mean 0.00x  >=10x 0.00%  >=20x 0.00%
rc=0
#rname	startpos	endpos	numreads	covbases	coverage	meandepth	meanbaseq
amp	1	1000	0	0	0	0	0
chrom	length	bases	mean	min	max
total	0	0	0.00	0	0
region_depth_stats on empty BAM: {'length': 1000, 'covered': 0, 'mean_depth': 0.0, 'max_depth': 0, 'pct_covered': 0.0, 'pct_ge_10x': 0.0, 'pct_ge_20x': 0.0}
zero-length region -> ValueError empty region [0, 0)
bad contig -> ValueError invalid contig `nosuchcontig`
```

Output excerpt `out/n3c_cram_no_ur.txt`:

```
@SQ	SN:ctgA	LN:20000	M5:4a0e408ed8721632ca3683ae7cf278e5	UR:/mnt/openscience/audits/bio-bam-statistics/run/work/cb3/tmpref/own_ctg.fa
--- samtools flagstat (Skill: needs no reference)
1098	7	total (QC-passed reads + QC-failed reads)
1091	7	primary
--- qc_report.py WITHOUT reference (expect exit 1 + message with the hint)
qc_report.py: cannot read /mnt/openscience/audits/bio-bam-statistics/run/data/new/own_ctg_nourl.cram: truncated file (CRAM cannot be decoded without its reference: pass the FASTA as 2nd argument)
rc=1
--- qc_report.py WITH reference (expect equal to flagstat)

Total records:     1,105 (primary 1,098 + secondary 3 + supplementary 4)
QC-failed primary: 7 (excluded below)
QC-passed primary: 1,091
Mapped:            1,085 (99.45% of QC-passed primary)
Properly paired:   0 (n/a of primary paired reads)
Duplicates:        5 (0.46% of QC-passed primary)
rc=0
--- Count Reads snippet (block 027) without reference (Skill: OSError: truncated file)
OSError: truncated file
--- Count Reads snippet with reference_filename
Primary QC-passed: 1091
Mapped: 1085 (99.45% of primary)
Single-end data: no paired reads
--- samtools stats on it: without --reference, then --reference (Skill: CRAM needs --reference)
0
[E::fai_build3_core] Failed to open the file /mnt/openscience/audits/bio-bam-statistics/run/work/cb3/tmpref/own_ctg.fa : No such file or directory
[E::refs_load_fai] Failed to open reference file '/mnt/openscience/audits/bio-bam-statistics/run/work/cb3/tmpref/own_ctg.fa'
```

Output excerpt `out/n3_cram_bad_insert.txt` (lines matching `truncated|text_named|zero_byte|rc=|quickcheck`):

```
rc=0
rc=0
rc=0
rc=0
rc=0
rc=0
rc=0
rc=0
rc=1
--- truncated.bam (89776 bytes)
[W::bam_hdr_read] EOF marker is absent. The input is probably truncated
rc=1
qc_report.py: cannot read /mnt/openscience/audits/bio-bam-statistics/run/data/new/truncated.bam: no BGZF EOF marker; file may be truncated
rc=1
OSError: no BGZF EOF marker; file may be truncated
rc=1
--- text_named.bam (30 bytes)
Failed to read header for "/mnt/openscience/audits/bio-bam-statistics/run/data/new/text_named.bam"
```

Output excerpt `out/n7_errmsgs.txt`:

```
plain AlignmentFile(uBAM,"rb") -> ValueError: file has no sequences defined (mode='rb') - is it SAM/BAM format? Consider opening with check_sq=False
check_sq=False: records 30
CRAM w/o reference_filename, UR intact, reads: 1105
--- block 028 on ubam_no_sq.bam
  File "pysam/libcalignmentfile.pyx", line 752, in pysam.libcalignmentfile.AlignmentFile.__cinit__
  File "pysam/libcalignmentfile.pyx", line 1001, in pysam.libcalignmentfile.AlignmentFile._open
ValueError: file has no sequences defined (mode='rb') - is it SAM/BAM format? Consider opening with check_sq=False
--- block 028 on own_ctg.bam
ctgA: 1049 mapped, 0 unmapped
ctgB: 0 mapped, 0 unmapped
```

Output excerpt `out/t9_syntax_sweep.txt` (lines matching `FAIL`):

```

```

**Scores:** Basic 37/40 | Specialized 53/60 | Total 90/100

**Assertions:**
- [PASS] Unaligned BAM (no @SQ) through qc_report.py and Count Reads equals flagstat - 30 records, 0 mapped; the ValueError of the earlier audit is gone.
- [PASS] CRAM with reference equals flagstat; CRAM without a reachable reference exits 1 with a message naming the reference - own_ctg_nourl.cram and real human CRAM: rc 1 plus the hint; with the FASTA rc 0 and equal counts.
- [PASS] Truncated, text-named and zero-byte BAMs exit 1 with a one-line message, not a traceback - no BGZF EOF marker / file does not contain alignment data; quickcheck agrees.
- [PASS] Empty, single-end, unindexed and MT-named inputs give the correct result or an exit-1 message - All match flagstat and hand counts; no ZeroDivisionError or silent 0.
- [PASS] A CRAM decoded against the wrong reference never prints partial numbers as a report - rc 1, no report; the message text is weak (see P2).

## Code the Skill directs, as run

Every fenced block of `SKILL.md` was extracted verbatim to `run/blocks/` (`extract_blocks.py`) and run through the scripts above; `examples/qc_report.py` ran from `run/skill/examples/`. `region_depth_stats` (block 029) was exec'd from the extracted block by `depth_truth.py`, `n2_region_truth.py`, `n5_real_region.py`, `t2_region_vs_truth.py`.

## Recommendations

**[P2] mosdepth --fast-mode caveat names deletions only** (input [4])  
Problem: SKILL.md says --fast-mode "also counts deletion (D) bases as covered". It also counts spliced N bases: on the real RNA BAM mosdepth reports 17.67x by default and 49.40x with --fast-mode (depth -aa 23.67x, mates counted twice); on own_del the fast-mode sum 9600 = mates twice + D + N. samtools mpileup depth also includes D and N (own_del -Q 0: 9600 vs depth 5200), which the overlap table does not say.  
Root cause: The round-2 note was written from an amplicon (deletion) BAM only.  
Fix: Say --fast-mode ignores internal CIGAR operations (D and N count as covered) and add one clause to the overlap table that mpileup counts D and N.

**[P2] MAX_INSERT is described as the samtools stats default, but stats clamps** (input [3])  
Problem: qc_report.py and the Insert Size Caveats bullet say longer templates are dropped, attributed to samtools stats -i 8000. samtools stats counts them at the cap: own_insert mean 3555.5 (stats) vs 2286 (qc_report), predicted 3555.5 for clamping and confirmed with -i 7000 and -i 400.  
Root cause: The cap value was matched to stats -i, its behaviour above the cap was not compared.  
Fix: Reword to "drops templates >= 8000 (samtools stats -i 8000 instead counts them at 8000, so the two means differ on long-insert libraries)".

**[P2] Wrong-reference CRAM reports "truncated file"** (input [7])  
Problem: qc_report.py on a CRAM decoded against a FASTA with the right names but other bases exits 1 but prints "cannot read ...: truncated file"; only htslib stderr lines above it say MD5 mismatch. The CRAM hint is shown only when no reference was passed. pileup calls on CRAM also emit a "multiple_iterators not implemented for CRAM" UserWarning.  
Root cause: The handler prints str(e) and adds a hint only for the missing-reference case.  
Fix: When a reference was given and the read fails, append "check that reference.fa is the FASTA the CRAM was written against (see the htslib MD5 message above)".

**[P2] Assay-threshold table and FREEMIX/somalier values unsourced** (input [6])  
Problem: The mapping/duplicate/proper-pair/MAPQ/Mt table and the FREEMIX 1% / 5% cut-offs are hedged as literature ranges but no source is given and no run here could check them; VerifyBamID2 end to end stops at "Insufficient Available markers" on a synthetic slice and somalier needs a whole-GRCh38 FASTA.  
Root cause: No whole-genome data and no citations are available to the fixer or to me.  
Fix: Cite the source of each row (or a single reference per assay) or move the table to a clearly marked "orientation only" note; keep the existing "not run end to end" label until a real WGS BAM run is added.

No P0 and no P1 is open. Other observations (not defects): `samtools stats -r ref.fa` gives identical GCD rows with and without `-r` at the same bin size on the test data (the help text says it is required); the CRAM `UR:` field makes CRAM decoding look reference-free on the machine that wrote it.
