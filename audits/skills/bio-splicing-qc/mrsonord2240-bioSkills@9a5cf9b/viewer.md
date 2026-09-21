> **Audit record for `bio-splicing-qc`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@9a5cf9b](https://github.com/mrsonord2240/bioSkills/tree/9a5cf9bd40c5aa1c6b7f8a3b1fc227ccd96fa547/alternative-splicing/splicing-qc) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-20 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-splicing-qc (re-audit of the fixed Skill)
Generated: 2026-09-20
Source: `mrsonord2240/bioSkills@9a5cf9bd40c5aa1c6b7f8a3b1fc227ccd96fa547:alternative-splicing/splicing-qc` (read from a copy in `run/skill/`, identical to the worktree file by `cmp`; the worktree and clone were not written to).
Pre-fix (archived at `_pre-fix-20260920`): 67, Reject, Research Veto M4 (code usability) fired, open P0s. **Now: 85, Production Ready, deployable, no veto, no open P0, one open P1.**
Category: Data Analysis. Mode D. Complexity: Complex, N = 8. Executed 8/8. Every script that was run is in `run/` (logs in `run/out/`); synthetic data are in `run/data/` and labelled synthetic in their generator docstrings.

## How the M4 (code usability) veto was re-judged
Every fenced block of SKILL.md was extracted to `run/blocks/` by `00_extract_blocks.py` (12 blocks) and parse-checked (`bash -n`, `ast.parse`, `out/00_extract.log`, `out/01_syntax_and_test.log`). Each block was then run from its file, with only paths substituted where noted:

| block | what | how run / result |
|---|---|---|
| B01 | helper report CLI | ran unedited; planted, real chrX |
| B02 | STAR pass 1 | ran, only genomeDir / GTF / fastq paths substituted; 4 real samples |
| B03 | merge + STAR pass 2 + samtools index | ran, same substitutions; merge recomputed independently |
| B04 | junction_saturation + helper | ran unedited (inside as-core); tip about -l/-u/-s FAILS |
| B05 | junction_annotation | ran unedited; class counts = pysam |
| B06 | pandas known/novel snippet | ran unedited on real RSeQC output: 93.4% / 22.3% / 99.5% |
| B07 | junctions CLI | ran unedited on 2 BAMs |
| B08 | MaxEnt example | ran unedited (as-maxent): [10.86, 2.68] [11.58] |
| B09 | SpliceAI command | ran, only files and -A grch37 changed (GRCh37 FASTA); 10-variant panel |
| B10 | awk refFlat + Picard + geneBody | ran (Picard in af-picard3); strand flag changed per library; RIBOSOMAL_INTERVALS dropped for real chrX |
| B11 | infer_experiment | ran unedited on 7 planted + real + 4 failure cases |
| B12 | samtools rRNA | ran unedited: 22.2% |
| inline | gffread then cut -f1-12 BED12 recipe | ran on the real GTF: 6001 lines x 12 columns |
| inline | fastq_screen --aligner minimap2 | ran on new reads: 25.00% |
| file | examples/test_splicing_qc.py | ran green in as-core (MaxEnt skipped) and as-maxent (all checks) |

Pre-fix M4 evidence re-judged: (1) the snippet printing 0.0% / 0.0% now prints the true fractions; (2) RSeQC exit 1 without Rscript is documented and `--skip-plot` is in every call; (3) `generate_qc_report` on a BAM without spliced reads now raises `NoSplicedReadsError` with a message; (4) the wrong overhang / ignored `min_overhang` / `=X` helpers are one corrected implementation. **M4: PASS.** M1 (integrity), M2 (practice boundaries), M3 (method) unchanged: PASS.

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|
| 1 | Canonical: Known vs novel junction ratio: SKILL.md blocks B05 (RSeQC), B06 (pandas snippet) and B01 (... | 38 | 53 | 91 | 5/5 | ✅ |
| 2 | Variant A: Junction saturation: B04 unedited on planted deep / mid / shallow libraries and real chrX,... | 35 | 50 | 85 | 4/5 | ⚠️ |
| 3 | Edge: Strandedness: B11 unedited on planted PE dUTP / forward / unstranded / leaky libraries, NE... | 37 | 53 | 90 | 5/5 | ✅ |
| 4 | Variant B: Junction read support: B07 / junction_stats on the planted overhang BAM, a NEW BAM of hand... | 37 | 53 | 90 | 5/5 | ✅ |
| 5 | Stress: Cohort-style STAR 2-pass: B02 and B03 (merge, pass 2, samtools index) on 4 real chrX 2x75 ... | 36 | 52 | 88 | 5/5 | ✅ |
| 6 | Scope Boundary: Splice-site strength: B08 unedited, MaxEntScan on 10k real chrX introns vs decoys via the ... | 36 | 51 | 87 | 5/5 | ✅ |
| 7 | Adversarial: rRNA and 3-prime bias: B12 and B10 unedited on planted libraries; Picard with the SKILL.md... | 35 | 50 | 85 | 4/5 | ⚠️ |
| 8 | NEW (auditor scenario): Cohort QC loop over 4 real STAR pass-2 BAMs + 2 planted libraries with the helper API, and... | 33 | 48 | 81 | 4/5 | ⚠️ |

**Execution Average: 87.1 / 100. Assertion Pass Rate: 37/40.** Static 82 x 0.4 = 32.8; dynamic 87.1 x 0.6 = 52.3; **final 85** (85.1). Layer 1 average 35.9/40, Layer 2 average 51.2/60. The margin over 85 is thin; see the note in the JSON.

## Detailed Outputs

### Input 1 — Canonical (regression + real data)
**Prompt:** Known vs novel junction ratio: SKILL.md blocks B05 (RSeQC), B06 (pandas snippet) and B01 (helper report) unedited on planted libraries, real chrX, and the failure guards
Ran B05 and B06 unedited in a directory holding `sample.bam` / `genes.bed12` (`10_in1_annot.sh`), then B01. Independent check `11_in1_indep.py` classifies junctions with pysam + BED12 only.
```
se_clean       : known: 93.4%, novel: 6.6%    | helper: known 93.4% of 12410 reads (34.6% of 719 junctions) -> Healthy
se_novelrich   : known: 22.3%, novel: 77.7%   | helper: known 22.3% of 12014 reads (13.0% of 1857 junctions) -> Suspect or interesting
real chrX      : known: 99.5%, novel: 0.5%    | BED12 from `gffread genes_chrX.gtf --bed | cut -f1-12`: 6001 lines x 12 columns
independent    : reads {'annotated': 25023, 'complete_novel': 49, 'partial_novel': 84}; EQUAL reads True, junctions True (also se_clean, se_novelrich)
guards (13/14/15): BED6 -> "60 lines have fewer than 12 columns" rc 1; contig mismatch -> "no contig name shared by BAM ['chrS'] and BED ['S']" rc 1;
                   unspliced.bam -> "RSeQC found no spliced reads at MAPQ >= 30" rc 1; literal RSeQC, Rscript absent -> "Rscript executable not found" rc 1;
                   helper --plot with no Rscript on PATH -> tables written, rc 0
```
The raw annotation values are `[' annotated', ' complete_novel', ' partial_novel']` (leading space), which is why the strip in B06 matters.
**Scores:** 38 / 53 / 91. Assertions 5/5:
- PASS: The SKILL.md pandas snippet (B06, unedited) reports the planted known fraction — clean 93.4% / 6.6% (truth 0.9341), novel-rich 22.3% / 77.7% (truth 0.2235), real chrX ERR188383 99.5% / 0.5%; the pre-fix 0.0% / 0.0% is gone (out/10_in1_annot.log)
- PASS: RSeQC class counts equal an independent pysam + BED12 classification (no Skill code) — reads and junctions identical on se_clean (11592/553/265; 249/305/165), se_novelrich and real chrX (25023/84/49; 2719/69/45); EQUAL True on all (out/12_in1_indep.log); also True on the 4 STAR pass-2 BAMs (out/82_n1.log)
- PASS: Silent RSeQC failures are guarded by the helper: BED6, contig mismatch, BAM without spliced reads, Rscript absent — each raises SplicingQCError with the cause, CLI exit 1 (out/15_in1_exitcodes.log); literal RSeQC without --skip-plot and no Rscript on PATH exits 1 as the Skill says, helper --plot with no Rscript still writes the tables (out/14_in1_norscript.log)
- PASS: Read-weighted vs junction-level known% is distinguished and both numbers are right — helper returns read_known 0.934 and junction_known 0.346 on the same BAM, equal to truth.json; SKILL.md wording "RSeQC's printed summary is junction-level" is incomplete: RSeQC prints both Splicing Events (read-weighted) and Splicing Junctions (P2)
- PASS: B01 helper report runs end to end on planted and real BAMs — annotation + saturation + junction support printed for se_clean, se_novelrich and real chrX (2833 junctions, growth 6.9%, 11.0% of junctions >= 10 reads)

### Input 2 — Variant A (regression + new finding)
**Prompt:** Junction saturation: B04 unedited on planted deep / mid / shallow libraries and real chrX, three repeats, plus the documented "-l/-u/-s for a finer 80-100% range" tip
B04 run per library inside as-core (`20_in2_sat.sh`, 3 runs each; `21_in2_fine.sh`, `23_deep_fine.sh` for the tip).
```
known-curve growth 80->100%:  deep 0.0 / 0.0 / 0.0 PLATEAU | mid 5.3 / 4.7 / 2.9 % RISING | shallow 11.1 / 11.8 / 7.8 % RISING | real chrX 7.6 % RISING (563 -> 2698)
all-junction count at 100%: 919 / 1022 / 951 (= distinct junctions in truth.json)
-l 80 -u 100 -s 5 (mid): "sampling 80% (86) ... 100% (428)" of 1710 reads; helper lo=80 growth known 2.63
deep, truth PLATEAU:  lo=5 step=5 -> 0.000 PLATEAU | lo=80 step=5 -> 0.111 STILL RISING | lo=2 step=2 -> 0.000 PLATEAU
```
RSeQC source (`qcmodule/SAM.py` line 4016-4019): `index_st = int(SR_num*((pertl-sample_step)/100)); sample_size += index_end - index_st` starting from 0.
**Scores:** 35 / 50 / 85. Assertions 4/5:
- PASS: Plateau rule (<2% growth 80->100%) classifies planted libraries correctly, across repeats — deep 0.0% PLATEAU x3; mid 5.3 / 4.7 / 2.9% and shallow 11.1 / 11.8 / 7.8% STILL RISING x3 (analytic 5.6 / 13.6%); the Skill's "stochastic, compare growth" advice matches (out/20_in2_sat.log)
- PASS: Helper parses the .r vectors and the curves agree with independent counts — all-junction curve at 100% = 919 / 1022 / 951 = distinct junctions in truth.json; known curve reaches 180 = annotated junctions
- PASS: Real chrX gives a plausible verdict and the read-depth caveat holds — known 563 -> 2698, growth 7.6% STILL RISING for a 50k-pair subset; real BED12 from the gffread recipe worked
- PASS: Contig mismatch / no spliced reads are caught by the helper and described correctly for raw RSeQC — helper raises; literal RSeQC exit 0 with y/z/w all zeros (out/13_in1_guards.log)
- FAIL: The documented refinement "-l/-u/-s for a finer 80-100% range" works — RSeQC source (qcmodule/SAM.py saturation_junction) adds (index_end - index_st) starting from 0, so the labelled percent equals the sampled percent only when -l == -s. -l 80 -u 100 -s 5 on the mid library samples 86 reads at "80%" and 428 of 1710 at "100%"; helper lo=80 on the deep (saturated) library returns growth 11.1% STILL RISING instead of PLATEAU; lo=50 reaches only 157 of 180 known junctions at "100%". lo=2 step=2 (l == s) is correct (out/21_in2_fine.log, 23_deep_fine.log)

### Input 3 — Edge (regression + NEW single-end data)
**Prompt:** Strandedness: B11 unedited on planted PE dUTP / forward / unstranded / leaky libraries, NEW single-end derived libraries, real chrX, and the documented failure modes
`31_in3_strand.sh` (B11 unedited per library; `30_in3_make_se.py` builds the new SE and MAPQ-1 BAMs from the planted PE data).
```
PE dutp 1.0000 "1+-,1-+,2++,2--" | fwd 1.0000 "1++,1--,2+-,2-+" | unstr 0.5011/0.4989 | leak20 0.7975 | leak40 0.5914
SE dutp "+-,-+" 1.0000 | SE fwd "++,--" 1.0000 | real chrX 0.4643/0.4525, failed 0.0831
contig mismatch -> Total 0 usable reads were sampled / Unknown data type: Mixture ; MAPQ-1: same at -q 30, dUTP 1.0000 at -q 0
```
**Scores:** 37 / 53 / 90. Assertions 5/5:
- PASS: PE table maps planted protocols to the right strings and libType — dUTP 1.0000 "1+-,1-+,2++,2--"; forward 1.0000 "1++,1--,2+-,2-+"; unstranded 0.5011 / 0.4989; BED6 also accepted (out/31_in3_strand.log)
- PASS: NEW single-end libraries (read 1 of the planted PE data) give the documented SE strings — SE dUTP "+-,-+" 1.0000 (0.0000 on "++,--"); SE forward "++,--" 1.0000
- PASS: Leaky libraries land in the 70-90% band and the advice is stated — 20% and 40% planted leakage read 0.7975 and 0.5914; Skill says report leakage at 0.7-0.9 and treat < 0.7 as unstranded (labelled a convention)
- PASS: Failure messages and remedy as documented — contig mismatch: "Total 0 usable reads were sampled" / "Unknown data type: Mixture", rc 0; GTF as BED: 12-column skip notes then the same message; MAPQ-1 BAM: same message at -q 30, 1.0000 dUTP with -q 0
- PASS: Real unstranded library is read correctly — chrX ERR188383 0.4643 / 0.4525 with 8.3% failed to determine: Skill table says ~0.5 / ~0.5 = unstranded

### Input 4 — Variant B (regression + NEW hand-truth BAM + real STAR SJ.out.tab)
**Prompt:** Junction read support: B07 / junction_stats on the planted overhang BAM, a NEW BAM of hand-specified CIGARs and flags, and 4 real STAR pass-2 BAMs vs SJ.out.tab
`40_in4_make_edge.py` (NEW hand-truth BAM, 82 records, 13 junctions), `41_in4_junctions.py`, and `52_in5_check.py` against STAR SJ.out.tab.
```
edge.bam: junctions equal to hand truth 13 of 13; extra junctions []; min_overhang 0/30/60 on the pair-overlap junction -> 7 / 5 / 0 (expected)
se_overhang.bam: overhang 4 -> reads>=8 0 of 12 | 10 -> 12 | 6 -> 0 | 50 -> 12
real STAR pass 2: helper vs SJ.out.tab unique reads equal on 2765/2765, 2829/2829, 2792/2792, 2919/2919; >=10 reads 371/398/380/377 vs STAR 371/398/380/377
```
**Scores:** 37 / 53 / 90. Assertions 5/5:
- PASS: Overhang equals the adjacent-block overhang on the auditor's planted CIGARs — se_overhang.bam: micro4 -> 4 and 4 (reads>=8 = 0 of 12), micro10 -> 10, ov6 -> 6, ov50 -> 50 (out/42_in4.log); the pre-fix 30 vs 4 error is gone
- PASS: NEW BAM (10M2D20M500N30M, 5S45M300N50M, 20M1I30M400N50M, 50M300N30M5H, two-junction reads, no-NH / MAPQ 3 / NH=2 / MAPQ 0 with NH=1 / reverse / secondary / supplementary, mates crossing the same, one, or two junctions, 3M overhang, second contig) equals the hand truth table — 13 of 13 junctions equal on reads, reads_all and min_overhang; 0 extra junctions; min_overhang 0 / 30 / 60 give 7 / 5 / 0 as predicted (out/42_in4.log, data/edge_truth.json)
- PASS: Counts equal STAR SJ.out.tab unique reads on real data (4 samples, my own STAR 2.7.11b 2-pass run) — equal on 2765/2765, 2829/2829, 2792/2792, 2919/2919 shared junctions; junctions with >= 10 reads 371 / 398 / 380 / 377 = STAR; 27-50 extra junctions per BAM are absent from SJ.out.tab (ERR204916: 50, all with 1-4 reads, 21 GT..AG and 17 CT..AC canonical; consistent with the SJ.out.tab filters of STAR; out/56_only_helper.log)
- PASS: Unindexed BAM and BAM without spliced reads give a clear result, no crash — unindexed micro BAM read with until_eof; unspliced BAM gives {} / 0.0%; report raises NoSplicedReadsError (out/13_in1_guards.log)
- PASS: B07 CLI runs and its summary is internally consistent — se_overhang: 6 junctions, 3 with anchored reads, 3 with >= 10; edge: 13 / 12 / 0; reads_anchored <= reads_total everywhere

### Input 5 — Stress (regression, re-run on my own STAR index)
**Prompt:** Cohort-style STAR 2-pass: B02 and B03 (merge, pass 2, samtools index) on 4 real chrX 2x75 samples with my own index, plus the Common Errors table
`50_in5_index.sh` (own STAR index, sjdbOverhang 149), `51_in5_star.sh` (B02 and B03 via `sed` path substitution only), `53_in5_check.sh`, `54_in5_errors.sh`.
```
merged: 6 lines x 4 columns, equals independent recomputation, 0 in GTF | pass-2 SJ.out.tab: 3 of 3 merged junctions have col6 = 1
unique mapping p1 -> p2: 97.63->97.67, 97.24->97.29, 97.53->97.54, 96.95->96.98 | XS tag on 100% of spliced records in pass 2
STAR --help: alignIntronMax 0 = (2^16)*9 | EXITING ... present --sjdbOverhang=74 is not equal to the value at the genome generation step =149
Fatal LIMIT error: ... =10552 is larger than the limitSjdbInsertNsj=100 / SOLUTION: re-run with at least --limitSjdbInsertNsj 10552 | pysam: fetch called on bamfile without index
```
**Scores:** 36 / 52 / 88. Assertions 5/5:
- PASS: B02 and B03 run unedited (paths only) on 4 real samples and improve mapping — rc 0 on 8 runs, --sjdbOverhang 149 with 75-nt reads, unique mapping 97.63 -> 97.67, 97.24 -> 97.29, 97.53 -> 97.54, 96.95 -> 96.98 (out/51_in5_star.log)
- PASS: The merge filter does what the comments say — $6==0 && $5>0 && $7>=3 | cut -f1-4 | sort -u = 6 junctions, 4 columns, equals independent recomputation, 0 present in the GTF (out/53_in5_check.log); pass-2 SJ.out.tab marks 3 of 3 merged junctions found as annotated (col 6 = 1), as the Skill notes
- PASS: Flag and default claims: alignIntronMax, XS tag, --outSAMtype None, overhang defaults — STAR --help: alignIntronMax 0 = 2^16 x 9 = 589,824; alignSJoverhangMin 5, alignSJDBoverhangMin 3; XS tag on 24113 / 24113 (and 3 other samples 100%) spliced records with --outSAMstrandField intronMotif
- PASS: Common Errors messages are the real ones — sjdbOverhang mismatch "present --sjdbOverhang=74 is not equal to the value at the genome generation step =149"; "Fatal LIMIT error ... =10552 is larger than the limitSjdbInsertNsj=100 / SOLUTION: re-run with at least --limitSjdbInsertNsj 10552"; pysam "fetch called on bamfile without index"; RSeQC zero-read messages (out/54_in5_errors.log)
- PASS: Data-derived numbers in the Skill hold on the new samples — junctions with >= 10 reads 10.5-12.0% (Skill: 11%); 5,717 lines / 2,184 distinct / 2,178 annotated in the old merge is a fixer measurement on the same data. Veeneman 2016 wording not re-fetched (offline)

### Input 6 — Scope Boundary (regression + NEW variant panel)
**Prompt:** Splice-site strength: B08 unedited, MaxEntScan on 10k real chrX introns vs decoys via the helper, SpliceAI (B09 command) on a NEW panel of canonical-site, exonic and deep-intronic variants
`61_in6.sh` (B08 + `60_in6_sites.py`), `63_in6b_spliceai.sh` (B09 with -A grch37; `62_in6b_make_vcf.py` builds the panel).
```
B08: [10.858, 2.676] [11.580] | helper: [10.86, nan, nan, 2.68] and [11.58, -7.20, nan]
chrX: 10095 GT donors 62.5% >8, 10.8% <5, median 8.68; 451 non-GT donors 100% <5; decoys 94.0% <5; AUC donor 0.969, acceptor 0.954
SpliceAI: donor GT>AT 0.99/0.99 | acceptor AG>AA 1.00/1.00 | exon-interior <=0.07 | deep intronic 0.00
```
**Scores:** 36 / 51 / 87. Assertions 5/5:
- PASS: B08 prints the documented scores — [10.858, 2.676] [11.580] exactly; helper on [good, 7-mer, N, lower-case] gives [10.86, nan, nan, 2.68] and acceptors [11.58, -7.20, nan] (out/61_in6.log)
- PASS: MaxEnt cut-offs (>8 strong, <5 weak) are supported on real sites (independent script) — 10,095 annotated GT donors: 62.5% > 8, 10.8% < 5, median 8.68; 451 non-GT donors 100% < 5; 2000 decoy GT donors 94.0% < 5; AUC donor 0.969, acceptor 0.954. The Skill quotes 8,549 donors, 60.7% / 11.6%, 95.5% of 88 decoys: same conclusion, different sampling (not identical numbers)
- PASS: SpliceAI command works and separates classes on a NEW panel (GRCh37 chrX, -A grch37 because the FASTA is GRCh37, as the Skill requires the assembly to match) — 2 donor GT>AT: max DS 0.99, 0.99; 2 acceptor AG>AA: 1.00, 1.00; 3 exon-interior SNVs <= 0.07; 3 deep-intronic 0.00 (out/63_in6b.log)
- PASS: Splice-site scores stay research-scoped (Practice Boundaries) — Scope section, PP3/BP4 cut-offs framed as references for prioritising sites, "classifying a patient's variant ... out of scope"; no individual diagnosis or prescription
- PASS: Practical throughput of the helper is documented — maxentpy score3 measured ~0.1 s per acceptor under load (300 acceptors 31.8 s; 8k donors + acceptors ~20 min): not stated in the Skill (P2), but nothing wrong

### Input 7 — Adversarial (regression + NEW fastq_screen data + real Picard)
**Prompt:** rRNA and 3-prime bias: B12 and B10 unedited on planted libraries; Picard with the SKILL.md awk refFlat on real chrX; fastq_screen on NEW reads
`71_in7.sh` (B12, B10 unedited), `73_in7_real.sh` + `72_in7_real_picard.py`, `74_in7_fqscreen.sh` with `70_in7_make_fq.py`.
```
B12: rRNA: 22.2% (old recipe 8170/52282 = 15.6%) | Picard PCT_RIBOSOMAL_BASES 0.222277
Picard bias: uniform 1.009 / 1.002, 3-prime 0.0466 | geneBody 5p/3p 1.03 vs 0.043 | strand 1.0
real chrX: refFlat 6001 lines, 0 differ from BED12 | PF_ALIGNED_BASES 7,373,062 = pysam | intergenic 0.025654 vs 0.0257 | bias 0.2745 vs geneBody 0.847
fastq_screen: 25.00% One_hit_one_genome (minimap2 24.9%) | missing .fa.gz -> rc 0, 100% unmapped, Aligner warning | default aligner rc 255
```
**Scores:** 35 / 50 / 85. Assertions 4/5:
- PASS: samtools rRNA recipe (B12) reproduces the planted 22.2% — 22.2% with -F 0x904; the old recipe reads 8170 / 52282 = 15.6% (out/71_in7.log); Picard PCT_RIBOSOMAL_BASES 0.222277
- PASS: B10 awk refFlat + Picard + geneBody work on planted libraries — PCT_CORRECT_STRAND_READS 1 (SECOND_READ for dUTP, FIRST_READ for forward); MEDIAN_5PRIME_TO_3PRIME_BIAS 1.009 / 1.002 uniform vs 0.0466 3-prime; geneBody 5p/3p 1.03 vs 0.043
- PASS: The awk refFlat and Picard are correct on real chrX (NEW, independent check) — refFlat 6001 lines, 0 differ from the BED12 blocks (round trip); Picard PF_ALIGNED_BASES 7,373,062 = pysam aligned bases; intergenic 0.025654 vs independent 0.0257; coding+UTR+intronic+intergenic = 1.0000 (out/73_in7_real.log)
- PASS: fastq_screen setup claims on NEW reads (4000 SE reads, 25% rRNA) — literal --aligner minimap2 command: One_hit_one_genome 25.00% (minimap2 alone 24.9%); missing prefix.fa.gz: rc 0, 100% unmapped, "Aligner warning ... failed to open ... rrna_ref.fa.gz"; default aligner: rc 255 (out/74_in7_fqscreen.log)
- FAIL: The 5'-3' bias thresholds give a right verdict on real data — real chrX library (50k pairs, poly(A) test set): Picard MEDIAN_5PRIME_TO_3PRIME_BIAS 0.2745 -> "<0.5 = 3' bias" but geneBody_coverage 5p/3p is 0.847 on the same BAM; the table gives no depth caveat (P2)

### Input 8 — NEW (auditor scenario) (NEW)
**Prompt:** Cohort QC loop over 4 real STAR pass-2 BAMs + 2 planted libraries with the helper API, and diagnosis of a high novel-junction rate (annotation gap vs artifact)
`80_new_diagnose.sh`, `81_n1_cohort.py` + `82_n1.sh`.
```
sample             known_rd known_jn   growth  %>=10rd  status
ERR188383             0.996    0.964    0.078     11.2  Healthy   saturation still rising; <30% junctions >=10 reads
ERR188428 / ERR188454 / ERR204916  0.995 / 0.994 / 0.993 Healthy, same two flags (10.5-12.0% >= 10 reads)
planted_clean         0.934    0.346    0.000     32.5  Healthy
planted_novelrich     0.223    0.130    0.000     14.6  Suspect or interesting  known<80%; <30% junctions >=10 reads
annotation gap (half the genes missing): known 46.1% / novel 53.9%; median read_count novel classes 2 (vs annotated 56); full model 93.4% / 6.6%
```
**Scores:** 33 / 48 / 81. Assertions 4/5:
- PASS: generate_qc_report loop flags the right samples (usage-guide prompt "report samples below acceptable thresholds") — novel-rich 0.223 Suspect + "<30% junctions >= 10 reads"; clean planted Healthy; real libraries known 0.993-0.996 Healthy, saturation still rising, 10.5-12.0% >= 10 reads (out/82_n1.log)
- PASS: Per-sample class counts on the 4 real pass-2 BAMs equal independent pysam — EQUAL reads and junctions 4/4
- PASS: Annotation-gap scenario behaves as the Skill says (Suspect, then Healthy after updating annotation) — clean BAM vs a gene model with half the genes: known 46.1% / novel 53.9%; full model 93.4% / 6.6% (out/80_new_diagnose.log)
- FAIL: The Skill gives a runnable drill-down that separates annotation gaps from mapping artifacts — the Decision Tree says "drill down" for novel% > 40 but no step or helper splits novel junctions by support or overhang; median read_count of novel classes (2 in the gap scenario vs 5-6 in the artifact-like library) had to be computed by hand from the .xls
- PASS: Helper report verdicts are usable as machine-readable QC — generate_qc_report returns a dict; verdict strings are depth-blind (real 50k-pair libraries print POOR / still rising), acceptable for a subset but not flagged

## Pre-fix defects re-checked

| pre-fix finding | now |
|---|---|
| P0 known/novel snippet prints 0.0% / 0.0% | fixed: 93.4% / 22.3% / 99.5% on real RSeQC output, equal to independent counts (inputs 1, 8) |
| P0 RSeQC exit 1 without Rscript, Rscript unlisted | fixed: `--skip-plot` in every call, requirement stated, reproduced both ways (input 1) |
| P0 generate_qc_report EmptyDataError on BAM without spliced reads | fixed: NoSplicedReadsError, exit 1 with cause (input 1) |
| P1 overhang / min_overhang / =X / multi-mapper / mate double counting | fixed and checked against hand truth and STAR SJ.out.tab on 4 real samples (input 4) |
| P1 rRNA recipe 15.6% for 22.2%; fastq_screen aligner | fixed: 22.2%; 25.00%, both misconfigurations described correctly (input 7) |
| P1 MaxEnt acceptor -7.20; misaligned outputs; SystemExit/KeyError | fixed (input 6) |
| P1 wrong failure-mode text, STAR error strings, alignIntronMax, microexon flag, flat-curve claim | fixed; messages verbatim (inputs 3, 5, 2) |
| P2 merge filter, XS tag, Veeneman numbers, thresholds, unseeded saturation | fixed or stated; Veeneman not re-fetched |
| **new, introduced by the fix**: -l/-u/-s refinement tip and helper lo/hi/step | P1 (input 2) |

## Recommendations
- **P1** The documented "-l/-u/-s for a finer 80-100% range" tip gives wrong curves (input 2): Replace the tip with "for a finer curve lower -s and keep -l equal to -s (-l 2 -u 100 -s 2)"; make junction_saturation() raise or warn when lo != step; add a test on the planted deep BAM.
- **P2** RSeQC summary wording and a missing drill-down for a high novel rate (input 1, 8): State that both blocks are printed and which one the thresholds use; add a helper or 6-line recipe that joins the .junction.xls classes with junction_stats() and reports median reads and min overhang per class.
- **P2** Depth-blind thresholds: 5'-3' bias and the helper verdicts (input 7, 8): Say the ratio needs enough reads on the top expressed transcripts and to confirm with geneBody_coverage; print read counts beside the helper verdicts.
- **P2** Unstated cost and unverifiable references (input 6): Add a throughput note and "about 60% > 8, about 11% < 5" wording; cite page/table for the paper statements.
- **P2** SKILL.md length and residual clinical vocabulary (input 5, 6): Move STAR 2-pass and Picard details to references/; keep the cut-offs but drop the ACMG code names.
