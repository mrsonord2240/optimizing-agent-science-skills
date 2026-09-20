> **Audit record for `bio-splicing-qc`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@44ff43b](https://github.com/mrsonord2240/bioSkills/tree/44ff43bb35e5741c3ddd3c003590e1f1da8a4a4b/alternative-splicing/splicing-qc) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-20 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-splicing-qc
Generated: 2026-09-20

Source: `mrsonord2240/bioSkills@44ff43bb35e5741c3ddd3c003590e1f1da8a4a4b:alternative-splicing/splicing-qc` (first audit). Category: Data Analysis, mode D (SKILL.md + shipped example), Complex -> 7 inputs, 7/7 executed.

Synthetic data (auditor-made, planted truth) is in `run/data/synthetic/` (`make_synth.py`); real data is the GEUVADIS chrX set in `audit-envs/alternative-splicing/public-data`.

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|
| 1 | Canonical | 25 | 33 | 58 | 2/5 PASS | ⚠️ |
| 2 | Variant A | 31 | 44 | 75 | 3/5 PASS | ✅ |
| 3 | Edge | 30 | 47 | 77 | 2/5 PASS | ✅ |
| 4 | Variant B | 24 | 27 | 51 | 0/5 PASS | ❌ |
| 5 | Stress | 31 | 45 | 76 | 1/5 PASS | ✅ |
| 6 | Scope Boundary | 27 | 40 | 67 | 2/5 PASS | ⚠️ |
| 7 | Adversarial | 27 | 37 | 64 | 2/5 PASS | ⚠️ |

**Execution Average: 66.9 / 100**  |  **Assertion Pass Rate: 12/35**  |  Static 68/100  |  **Final 67 (Reject: Research Veto M4 FAIL, veto_override)**

Without the veto the numeric score would be Beta Only (60-74) and below the Limited Release floors (execution avg < 75, static < 70), so the Skill would still be non-deployable.

## Skill Veto: PASS (stability, contract, determinism, security).  Research Veto: M1 PASS, M2 PASS, M3 PASS, M4 FAIL

## Detailed Outputs

### Input 1 — Canonical: Known vs novel junction classification of a library with planted class fractions (RSeQC junction_annotation + SKILL.md pandas snippet)
**Prompt:** Classify my junctions as known vs novel and flag samples with a low known-junction fraction (two SE 100-nt libraries; planted 93% and 22% known reads).
**Executed:** true. Scripts: `run/input1_junction_annotation.py`
**Output (trimmed):**
```
clean:     RSeQC junctions 719 (known 249 / partial 305 / complete 165); reads 12410 (11592 / 553 / 265)
           pysam count identical; planted known-read fraction 0.9341
SKILL.md snippet -> "known: 0.0%, novel: 0.0%"   annotation values: [' annotated', ' complete_novel', ' partial_novel']
after .str.strip(): known 93.4%, novel 6.6%   (strictly annotated junctions only: 86.7%; junction-level known 34.6%)
novelrich: known 22.3% reads (planted 0.2235), junction-level 13.0%
```
**Scores:** Basic: 25/40 | Specialized: 33/60 | Total: 58/100
**Assertions:**
- [PASS] RSeQC junction_annotation.py runs from the Skill example and its class counts equal an independent pysam count — clean: annotated 249 / partial 305 / complete 165 junctions, 11592/553/265 reads; identical to pysam and to planted truth (known 93.4% of reads)
- [FAIL] The SKILL.md pandas snippet reports the planted known fraction (93.4%) — printed known 0.0%, novel 0.0% on both libraries; annotation column values are " annotated", " partial_novel", " complete_novel" (leading space)
- [PASS] Known-fraction thresholds (>=80 / 60-80 / <60) give the right verdict for clean (93%) vs novel-rich (22%) libraries once parsed — after .str.strip(): 93.4% Healthy and 22.3% Suspect; directionally right
- [FAIL] Definition of "known" matches what the Skill implies (annotated junction) — RSeQC calls a junction annotated when donor AND acceptor are each known, so unannotated exon-skipping junctions count as known (read-level 93.4% vs 86.7% strictly annotated); undocumented
- [FAIL] Read-weighted and junction-level readings are distinguished — same BAM: 93% of reads known but only 35% of junctions; RSeQC prints junction-level, the snippet is read-weighted; thresholds do not say which

### Input 2 — Variant A: Junction saturation on planted deep / mid / shallow libraries, real chrX, and contig-name mismatch
**Prompt:** Compute junction saturation and tell me whether depth is sufficient (deep / mid / shallow planted libraries, real chrX, BED with mismatched contig names).
**Executed:** true. Scripts: `run/input2_junction_saturation.py`
**Output (trimmed):**
```
sat_deep    known 154,180,180,... growth 80->100 = 0.0%    PLATEAU   (expected 0.0%)
sat_mid     known 22,46,73,...,176,180 growth 8.4%          STILL RISING (expected 5.6%)
sat_shallow known 20,36,59,...,175,180 growth 13.2%        STILL RISING (expected 13.6%)
pysam distinct junctions 919/1022/951 == RSeQC all@100%
real chrX ERR188383 known 588 -> 2698 growth 6.7% STILL RISING
contig mismatch: rc=0, known [0,0,0..] all [0,0,0..]; plateau rule -> 0/0
```
**Scores:** Basic: 31/40 | Specialized: 44/60 | Total: 75/100
**Assertions:**
- [PASS] Plateau rule (<2% growth 80->100%) classifies the planted libraries correctly — deep PLATEAU; mid 8.4% and shallow 13.2% STILL RISING; expected 5.6% and 13.6% from Poisson thinning
- [PASS] Curve values agree with independent expectation and pysam — RSeQC all-junction count at 100% equals pysam distinct junctions (919/1022/951); known curve within 3-16 junctions of expectation (unseeded shuffle)
- [PASS] Real chrX ERR188383 verdict is produced and plausible — known 588 -> 2698, growth 6.7% STILL RISING; 100k-read subset, as expected
- [FAIL] Wrong contig naming is detected or warned about — BED contig "S" vs BAM "chrS": exit 0, every curve all zeros; the plateau rule then divides 0/0; nothing in the Skill warns
- [FAIL] SKILL.md "deep BAM -> flat curve is uninformative" claim is correct — RSeQC samples percentiles of splice events; a curve flat from 10% (sat_deep known 154 -> 180 by 10%) is the saturated case, i.e. informative

### Input 3 — Edge: Strandedness verification (infer_experiment) on planted dUTP / forward / unstranded / leaky PE libraries, real chrX and failure modes
**Prompt:** Verify library strandedness before I set rMATS --libType (planted dUTP, forward, unstranded, 20% and 40% leakage; real chrX; wrong BED; MAPQ 1 BAM).
**Executed:** true. Scripts: `run/input3_strandedness.py`
**Output (trimmed):**
```
dutp        {'1++,1--,2+-,2-+': 0.0,    '1+-,1-+,2++,2--': 1.0}     -> fr-firststrand
fwd         {1.0, 0.0}                                                -> fr-secondstrand
unstr       {0.5011, 0.4989}; dutp_leak20 {0.2024, 0.7975}; leak40 {0.4087, 0.5914}
real chrX   {0.4643, 0.4525}, failed to determine 0.0831           -> unstranded
contig mismatch / GTF as BED: rc=0 "Total 0 usable reads were sampled", "Unknown data type: Mixture"
MAPQ-1 BAM: default (-q 30) "Unknown data type: Mixture"; -q 0 -> 1.0
```
**Scores:** Basic: 30/40 | Specialized: 47/60 | Total: 77/100
**Assertions:**
- [PASS] Decision table maps planted protocols to the right rMATS libType — dUTP 1.00 "1+-,1-+,2++,2--" -> fr-firststrand; forward 1.00 -> fr-secondstrand; unstranded 0.501/0.499; real chrX 0.464/0.453 (+8.3% undetermined)
- [FAIL] Leaky libraries land in the documented 70-90% band and the Skill says what to do — 80% dUTP reads 0.7975, 60% reads 0.59: band exists but no action or libType advice for 70-90%
- [FAIL] Contig mismatch / wrong BED is diagnosed — BED contig "S" vs BAM chrS and GTF-as-BED both exit 0 with "Total 0 usable reads were sampled" / "Unknown data type: Mixture"; Skill attributes 0 reads to sample size and says "0 of 200000 reads"
- [FAIL] Documented fix "use -q 30" restores a MAPQ-1 BAM — -q 30 is already the default and gives "Unknown data type: Mixture"; -q 0 gives 1.00 dUTP
- [PASS] Skill points at an existing, runnable tool with correct flags — -i/-r/-s exist in RSeQC 5.0.5; BED6 also accepted by infer_experiment

### Input 4 — Variant B: Per-junction read counts, overhang and ">=10 reads" helpers vs planted CIGARs, multi-mappers, real chrX, regtools
**Prompt:** Give me per-junction read counts and the overhang distribution; how many junctions have >=10 reads and overhang >=8? (planted CIGARs, multi-mappers, real chrX vs STAR/regtools).
**Executed:** true. Scripts: `run/input4_junction_coverage_overhang.py`
**Output (trimmed):**
```
junction_stats (SKILL.md) on planted CIGARs: 100030-101030 overhang 30 (true 4); 101034-101834 34 (4); 105020-105720 20 (10); 105730-106630 30 (10); 6 -> 6 OK; 50 -> 50 OK
count_junction_reads(min_overhang=8) == (min_overhang=99): identical, 72 reads / 6 junctions
=/X CIGAR read: example (200000,201000) vs SKILL.md function (200050,201050) [true]
NH=4/MAPQ 3 contamination: Skill 12410 reads / 719 junctions vs unique-only 9308 / 648
real chrX ERR188383: read-level 25580 reads vs fragment-level 24091; 665 of 2915 junction counts differ; >=10 reads 420 vs 385; regtools 423
STAR pass-2 BAM: Skill == STAR unique on 2163/2792 junctions; fragment-level == STAR on 2792/2792
generate_qc_report on real BAM: "POOR (<30% junctions have >=10 reads)" 14.4%
```
**Scores:** Basic: 24/40 | Specialized: 27/60 | Total: 51/100
**Assertions:**
- [FAIL] junction_stats overhang equals the planted adjacent-exon overhang — micro-exon reads 30M1000N4M800N66M: Skill 30 and 34 vs true 4 and 4; 20M700N10M900N70M: 20/30 vs 10/10; single-junction reads (6, 50) correct
- [FAIL] count_junction_reads honours min_overhang — min_overhang=8 and 99 return identical counts (72 reads, 6 junctions); parameter never used
- [FAIL] Counts agree with STAR SJ.out.tab / fragment-level counting on real PE data — chrX pass-2 BAM: read-level count equals STAR unique on 2163/2792 shared junctions, fragment-level on 2792/2792; >=10-read junctions 404 vs 371
- [FAIL] Junction coordinates correct for =/X CIGAR reads — example reports (200000,201000) vs true (200050,201050); SKILL.md function handles ops 7/8, example does not
- [FAIL] Failure on unindexed BAM / BAM without spliced reads is reported clearly — fetch() ValueError on STAR-sorted BAM without .bai; generate_qc_report on a BAM with no spliced reads raises EmptyDataError

### Input 5 — Stress: Cohort-style STAR 2-pass on 4 real chrX samples (2x75) exactly as in SKILL.md, plus flag and error-string claims
**Prompt:** Configure cohort-style STAR 2-pass for my samples (4 real chrX pairs), and check the flags and the merge filter.
**Executed:** true. Scripts: `run/input5_star_2pass.sh + run/input5_analyze.py`
**Output (trimmed):**
```
pass1 unique mapping 97.20/96.86/97.17/96.54%  ->  pass2 97.63/97.24/97.53/96.95%; ReadsPerGene 2396 rows
cohort_novel_SJ.tab: 5717 lines, 2184 distinct junctions, 2178 already in GTF (6 novel); 3533 duplicate lines
col5 = intron motif (1-6), col4 = strand (1,2); non-canonical rows 13 (all annotated, strand 0)
XS tags in pass-2 BAM: 0 of 20000 spliced reads
--limitSjdbInsertNsj 10 -> "Fatal LIMIT error ... =10552 ... SOLUTION: re-run with at least --limitSjdbInsertNsj 10552"
sjdbOverhang mismatch -> "present --sjdbOverhang=74 is not equal to the value at the genome generation step =100"
samtools view -c -F 0x100 -F 0x800 == -F 0x100 == -F 0x900 (98732): repeated -F accumulates, Skill row OK
```
**Scores:** Basic: 31/40 | Specialized: 45/60 | Total: 76/100
**Assertions:**
- [PASS] Pass 1 and pass 2 commands run on current STAR (2.7.11b) and produce SJ.out.tab and GeneCounts — 4/4 samples; unique mapping 96.5-97.2% -> 97.0-97.6%; ReadsPerGene 2396 rows; --sjdbOverhang 149 with 75-nt reads also runs
- [FAIL] The awk filter does what SKILL.md says ("strand info AND >=3 unique reads", novel junctions) — column 5 is the intron motif, column 4 the strand; of 2184 merged junctions 2178 are already in the GTF (only 6 novel); 3533 duplicate lines survive sort -u
- [FAIL] SKILL.md STAR defaults and error strings are accurate — alignIntronMax default 0 = ~590 kb, not 1 Mb; "STAR: too many SJs in cohort merge" does not exist (real: Fatal LIMIT error ... re-run with --limitSjdbInsertNsj 10552); alignSJoverhangMin 8 lowers, not raises, microexon sensitivity vs default 5
- [FAIL] Commands leave an XS-taggable BAM as the strandedness note implies — 0 of 20000 spliced reads carry XS because --outSAMstrandField intronMotif is not in the pass commands (mentioned only in a comment)
- [FAIL] Cited 2-pass benefit is reproduced from the source — Veeneman 2016 reports >=94% of simulated novel junctions had improved quantification (per-sample two-pass), not 80-86% vs >=94% recovery nor a cohort-vs-per-sample comparison

### Input 6 — Scope Boundary: Splice-site strength: MaxEntScan on 8.5k real annotated chrX donors/acceptors vs decoys, example helper, SpliceAI CLI
**Prompt:** Score the donor/acceptor sites with MaxEntScan and SpliceAI and flag weak or cryptic ones (8.5k real annotated chrX sites vs decoys).
**Executed:** true. Scripts: `run/input6_splice_site_strength.py + run/input6b_spliceai_rscript.sh`
**Output (trimmed):**
```
annotated GT donors n=8549: >8 60.7%, 5-8 27.6%, <5 11.6%, median 8.60;  AG acceptors n=8507: >8 57.9%, <5 13.5%
decoy GT donors n=88: 95.5% <5;  AUC donor 0.969, acceptor 0.958
score5('CAGGTAAGT') = 10.86;  score3('T'*20+'CAG') = -7.20 (SKILL.md example)
wrong length -> SystemExit "Wrong length of fa!"; N/X/U -> KeyError; lower-case ok
score_splice_sites(4 donors incl. 8-mer, lower-case, N) -> [10.86, 10.86, None]
spliceai -A grch37 -D 50 -M 0: SpliceAI=A|PLCXD1|0.00|0.00|0.90|1.00|28|-10|28|-1
```
**Scores:** Basic: 27/40 | Specialized: 40/60 | Total: 67/100
**Assertions:**
- [PASS] MaxEnt strong/weak cut-offs (>8 / <5) are directionally supported on real sites — 8549 annotated GT donors: 61% >8, 28% 5-8, 12% <5, median 8.6; 88 decoy GT donors 95% <5; AUC donor 0.969, acceptor 0.958; all 399 non-GT annotated donors <5
- [FAIL] The SKILL.md acceptor example is a valid strong 3'ss — score3('T'*20+'CAG') = -7.20: the 20-nt intron ends TT, no AG; example script calls it an 'Example 3ss' expecting 8-12 bits
- [FAIL] Skill's documented invalid-input behaviour (ValueError or silently wrong score) matches maxentpy 0.0.2 — wrong length -> SystemExit "Wrong length of fa!" (process ends, exit 0); N/X/U -> KeyError; lower-case accepted
- [FAIL] score_splice_sites returns scores aligned with its inputs — 4 donor inputs -> 3 outputs: the 8-mer is silently dropped and N gives None, so indices shift
- [PASS] SpliceAI CLI flags and thresholds are usable — spliceai -A grch37 -D 50 -M 0 on canonical donor X:193062 G>A -> DS_DG 0.90, DS_DL 1.00; delta cut-offs 0.2/0.1 match Walker 2023

### Input 7 — Adversarial: rRNA contamination (samtools recipe, fastq_screen), 3-prime bias (geneBody_coverage, Picard) and strand-convention block on planted BAMs
**Prompt:** Is my library rRNA-contaminated or 3-prime biased, and what do I pass to Picard/rMATS for strand? (planted 22% rRNA, 85% 3-prime library).
**Executed:** true. Scripts: `run/input7_contam_bias.sh, input7b_fastqscreen.sh, input7_parse.py`
**Output (trimmed):**
```
samtools view -c -L rRNA.bed / samtools view -c = 8170 / 52282 = 15.6%   (truth 22.2% of primary mapped fragments)
primary only: 4085 / 18378 = 22.2%   Picard PCT_RIBOSOMAL_BASES 0.222
Picard dUTP: SECOND_READ PCT_CORRECT_STRAND 1.0 ; FIRST_READ 0.0
3-prime library: MEDIAN_5PRIME_TO_3PRIME_BIAS 0.047 (uniform 1.009); geneBody 5p/3p 0.04 vs 1.02
fastq_screen literal: rc=255 (no aligner); --aligner minimap2 + valid config: rRNA 25.00% (truth 25%)
rmats.py --libType {fr-unstranded,fr-firststrand,fr-secondstrand} exists
```
**Scores:** Basic: 27/40 | Specialized: 37/60 | Total: 64/100
**Assertions:**
- [PASS] Picard STRAND_SPECIFICITY mapping in SKILL.md is right for dUTP — SECOND_READ_TRANSCRIPTION_STRAND: PCT_CORRECT_STRAND_READS 1.0; FIRST_READ: 0.0
- [PASS] 3-prime bias is flagged by the Skill's metrics — planted 3-prime library: MEDIAN_5PRIME_TO_3PRIME_BIAS 0.047 vs 1.009 uniform (<0.5 rule fires); geneBody 5p/3p 0.04 vs 1.02; note >2 is 5-prime bias, not degradation
- [FAIL] samtools view -c -L recipe reproduces the planted rRNA fraction (22.2%) — 8170/52282 = 15.6% (denominator includes 12282 secondary and 3244 unmapped records); Picard PCT_RIBOSOMAL_BASES 0.222 and primary-only recipe 4085/18378 = 22.2% are right; the Skill's >20% "failed" verdict is missed
- [FAIL] fastq_screen command works as written — literal command exits 255 (no Bowtie/Bowtie2/BWA; aligner not in the prerequisites); with minimap2 and a valid config it reports the planted 25.00% rRNA; a bad index path exits 0 with 100% unmapped
- [FAIL] rRNA threshold table is internally consistent — <5% poly(A) is Healthy yet 1-3% poly(A) "suggests RNA degradation"; the closing note says >5%

## Static score (25 criteria)

- functional_suitability: 8/12 — Broad coverage of design, STAR 2-pass, saturation, novelty, overhang, MaxEnt, Picard, strandedness, annotation, rRNA. Core RSeQC/Picard/STAR statements verified, but the known-fraction snippet, the MaxEnt acceptor example, the rRNA recipe, the overhang helper and several documented error strings and defaults are wrong.
- reliability: 5/12 — Silent failures dominate: contig mismatch gives exit-0 zero curves, generate_qc_report crashes on a BAM with no spliced reads, RSeQC plotting needs an unlisted Rscript, and documented error messages are not the ones the tools print.
- performance_context: 5/8 — One 480-line SKILL.md with no references/ and a large duplicated threshold set; example script is small.
- agent_usability: 11/16 — Clear decision tables and layer taxonomy; inconsistent thresholds across three tables, BED12 preparation never explained, no format given for reading saturation numbers.
- human_usability: 5/8 — Natural triggers and a usage guide; little tolerance for naming/format variants (contig names, BED type) and no diagnosis path when tools return zeros.
- security: 11/12 — No secrets; subprocess called with argument lists, no shell or eval; maxentpy calls sys.exit on bad input and the helper does not validate paths.
- maintainability: 8/12 — Single example module with functions, but shipped helpers duplicate and diverge from the SKILL.md versions (=/X handling, min_overhang) and there are no tests or fixtures.
- agent_specific: 15/20 — Good biology-vs-artifact caveats and cross-links (all seven Related Skills exist); overlong description; no seed/idempotency notes for the shuffled saturation subsample; escape hatches are mostly to other Skills.

**Static subtotal 68/100**

## Recommendations

- **[P0] Known/novel snippet returns 0.0%; Rscript undocumented** (inputs [1, 4]): RSeQC writes " annotated" with a leading space, so groupby(...).get("annotated") is 0 and the headline known/novel fraction prints 0.0%/0.0% on every library. junction_annotation.py and junction_saturation.py also exit 1 without Rscript (unlisted), and generate_qc_report crashes on a BAM without spliced reads. Fix: Strip the annotation column (junc["annotation"].str.strip()) and assert known+novel==1; pass --skip-plot or list R in prerequisites; guard empty junction output; add a test on a small BAM.
- **[P1] Overhang/coverage helpers give wrong numbers** (inputs [4]): junction_stats sums all matched bases on each side, so multi-junction reads report overhang 30 where the adjacent exon is 4; count_junction_reads ignores min_overhang, ignores =/X ops, counts multi-mappers and both mates (>=10-read junctions 404 vs STAR 371). Fix: Compute overhang from the adjacent M/=/X block only, filter NH==1 and count per fragment (or read SJ.out.tab/regtools), honour min_overhang, and test on CIGARs such as 30M1000N4M800N66M.
- **[P1] rRNA samtools recipe flips the pass/fail verdict** (inputs [7]): samtools view -c -L / samtools view -c reported 15.6% for a planted 22.2% because the denominator includes secondary and unmapped records; the >20% failed-depletion rule is then missed. fastq_screen needs an unlisted aligner and exits 255 or 0-with-100%-unmapped on misconfiguration. Fix: Use -F 0x904 (and -f 0x40 or PCT_RIBOSOMAL_BASES from Picard, which returned 0.222) and state the fastq_screen aligner/index setup and how to read the *_screen.txt.
- **[P1] Splice-site example and helper are wrong** (inputs [6]): The SKILL.md/example acceptor 'T'*20+'CAG' scores -7.20 (no AG); score_splice_sites drops wrong-length inputs and returns None for N so outputs no longer align with inputs; maxentpy exits the process on a wrong length and raises KeyError for N/U, not ValueError. Fix: Use a real acceptor (e.g. TTTTTTTTTTTTTTCCTTAGGAG, 11.58), return one score per input (NaN for invalid) and catch SystemExit/KeyError; correct the failure-mode text.
- **[P1] Documented failure modes and defaults are inaccurate** (inputs [2, 3, 5]): infer_experiment "0 of 200000 reads" is really contig-name/BED mismatch ("Total 0 usable reads", exit 0) and -q 30 is already the default; STAR error "too many SJs in cohort merge" does not exist (real: limitSjdbInsertNsj); alignIntronMax default is ~590 kb, not 1 Mb; alignSJoverhangMin 8 lowers microexon sensitivity; a flat deep-BAM saturation curve is saturation, not uninformative; junction_saturation on a contig mismatch returns all zeros with exit 0. Fix: Replace with observed messages, add a chr-naming and BED12 check (junction_* need BED12; infer_experiment accepts BED6), and state RSeQC "annotated" means both sites known (skipping junctions count).
- **[P2] Merge filter, thresholds and citations need cleanup** (inputs [1, 5, 7]): awk '$5>0' filters on intron motif not strand, the merged 'novel' file is 99.7% annotated with 3533 duplicate lines, pass-2 SJ.out.tab flags inserted junctions as annotated; 30-50M reads, 75-100 nt, rRNA 1-3% vs <5% and 'PE 50nt single-end' are inconsistent; Veeneman 94% is share of junctions improved, per-sample; read-weighted vs junction-level known% both exist; STAR BAMs need samtools index before the pysam helpers; --outSAMstrandField only in a comment. Fix: Filter on $6==0 and cut -f1-4 | sort -u, add --outSAMstrandField intronMotif where XS is needed, unify thresholds in one table with gap ranges, state which known-fraction definition applies, and add samtools index to the STAR steps.
- **[P2] Saturation numbers are unseeded and hard to read** (inputs [2]): RSeQC shuffles splice events without a seed (known curve moved by up to 16 junctions from expectation) and writes the numbers only inside the .r file; the Skill gives no parsing recipe. Fix: Show a 10-line parser for x/y/z/w vectors and say the curve is stochastic; use -l/-u/-s for finer 80-100% steps.
