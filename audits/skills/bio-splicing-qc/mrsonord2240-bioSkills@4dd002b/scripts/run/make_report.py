"""Builds eval_report_bio-splicing-qc_result.json and eval_viewer_bio-splicing-qc.md (re-audit of the fixed Skill).
Every number below was printed by a script in this run/ folder (logs in run/out/). Run: python make_report.py"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = 'mrsonord2240/bioSkills@9a5cf9bd40c5aa1c6b7f8a3b1fc227ccd96fa547:alternative-splicing/splicing-qc'


def A(text, result, note):
    return {'text': text, 'result': result, 'note': note}


inputs = [
    dict(index=1, type='Canonical', new='regression + real data',
         label='Known vs novel junction ratio: SKILL.md blocks B05 (RSeQC), B06 (pandas snippet) and B01 (helper report) unedited on planted libraries, real chrX, and the failure guards',
         note='B06 now prints known 93.4% / novel 6.6% (planted clean), 22.3% / 77.7% (novel-rich), 99.5% / 0.5% (real chrX); class counts equal an independent pysam classification exactly; every guarded failure (BED6, contig mismatch, no spliced reads, no Rscript) raises a clear error with exit 1.',
         basic=38, specialized=53,
         assertions=[
             A('The SKILL.md pandas snippet (B06, unedited) reports the planted known fraction', 'PASS', 'clean 93.4% / 6.6% (truth 0.9341), novel-rich 22.3% / 77.7% (truth 0.2235), real chrX ERR188383 99.5% / 0.5%; the pre-fix 0.0% / 0.0% is gone (out/10_in1_annot.log)'),
             A('RSeQC class counts equal an independent pysam + BED12 classification (no Skill code)', 'PASS', 'reads and junctions identical on se_clean (11592/553/265; 249/305/165), se_novelrich and real chrX (25023/84/49; 2719/69/45); EQUAL True on all (out/12_in1_indep.log); also True on the 4 STAR pass-2 BAMs (out/82_n1.log)'),
             A('Silent RSeQC failures are guarded by the helper: BED6, contig mismatch, BAM without spliced reads, Rscript absent', 'PASS', 'each raises SplicingQCError with the cause, CLI exit 1 (out/15_in1_exitcodes.log); literal RSeQC without --skip-plot and no Rscript on PATH exits 1 as the Skill says, helper --plot with no Rscript still writes the tables (out/14_in1_norscript.log)'),
             A('Read-weighted vs junction-level known% is distinguished and both numbers are right', 'PASS', 'helper returns read_known 0.934 and junction_known 0.346 on the same BAM, equal to truth.json; SKILL.md wording "RSeQC\'s printed summary is junction-level" is incomplete: RSeQC prints both Splicing Events (read-weighted) and Splicing Junctions (P2)'),
             A('B01 helper report runs end to end on planted and real BAMs', 'PASS', 'annotation + saturation + junction support printed for se_clean, se_novelrich and real chrX (2833 junctions, growth 6.9%, 11.0% of junctions >= 10 reads)'),
         ]),
    dict(index=2, type='Variant A', new='regression + new finding',
         label='Junction saturation: B04 unedited on planted deep / mid / shallow libraries and real chrX, three repeats, plus the documented "-l/-u/-s for a finer 80-100% range" tip',
         note='Plateau rule and curve parsing are right (deep 0.0% PLATEAU; mid 2.9-5.3% and shallow 7.8-11.8% STILL RISING; all-junction count at 100% equals pysam 919/1022/951), but the documented -l/-u/-s refinement is wrong: RSeQC accumulates sample size from zero, so with -l 80 the "80%" point is 5% of the reads and a saturated library reads STILL RISING.',
         basic=35, specialized=50,
         assertions=[
             A('Plateau rule (<2% growth 80->100%) classifies planted libraries correctly, across repeats', 'PASS', 'deep 0.0% PLATEAU x3; mid 5.3 / 4.7 / 2.9% and shallow 11.1 / 11.8 / 7.8% STILL RISING x3 (analytic 5.6 / 13.6%); the Skill\'s "stochastic, compare growth" advice matches (out/20_in2_sat.log)'),
             A('Helper parses the .r vectors and the curves agree with independent counts', 'PASS', 'all-junction curve at 100% = 919 / 1022 / 951 = distinct junctions in truth.json; known curve reaches 180 = annotated junctions'),
             A('Real chrX gives a plausible verdict and the read-depth caveat holds', 'PASS', 'known 563 -> 2698, growth 7.6% STILL RISING for a 50k-pair subset; real BED12 from the gffread recipe worked'),
             A('Contig mismatch / no spliced reads are caught by the helper and described correctly for raw RSeQC', 'PASS', 'helper raises; literal RSeQC exit 0 with y/z/w all zeros (out/13_in1_guards.log)'),
             A('The documented refinement "-l/-u/-s for a finer 80-100% range" works', 'FAIL', 'RSeQC source (qcmodule/SAM.py saturation_junction) adds (index_end - index_st) starting from 0, so the labelled percent equals the sampled percent only when -l == -s. -l 80 -u 100 -s 5 on the mid library samples 86 reads at "80%" and 428 of 1710 at "100%"; helper lo=80 on the deep (saturated) library returns growth 11.1% STILL RISING instead of PLATEAU; lo=50 reaches only 157 of 180 known junctions at "100%". lo=2 step=2 (l == s) is correct (out/21_in2_fine.log, 23_deep_fine.log)'),
         ]),
    dict(index=3, type='Edge', new='regression + NEW single-end data',
         label='Strandedness: B11 unedited on planted PE dUTP / forward / unstranded / leaky libraries, NEW single-end derived libraries, real chrX, and the documented failure modes',
         note='Every string and fraction in the decision table reproduced, including the single-end strings on new data; contig mismatch, GTF-as-BED and MAPQ-1 messages and the "-q 0" remedy behave as documented.',
         basic=37, specialized=53,
         assertions=[
             A('PE table maps planted protocols to the right strings and libType', 'PASS', 'dUTP 1.0000 "1+-,1-+,2++,2--"; forward 1.0000 "1++,1--,2+-,2-+"; unstranded 0.5011 / 0.4989; BED6 also accepted (out/31_in3_strand.log)'),
             A('NEW single-end libraries (read 1 of the planted PE data) give the documented SE strings', 'PASS', 'SE dUTP "+-,-+" 1.0000 (0.0000 on "++,--"); SE forward "++,--" 1.0000'),
             A('Leaky libraries land in the 70-90% band and the advice is stated', 'PASS', '20% and 40% planted leakage read 0.7975 and 0.5914; Skill says report leakage at 0.7-0.9 and treat < 0.7 as unstranded (labelled a convention)'),
             A('Failure messages and remedy as documented', 'PASS', 'contig mismatch: "Total 0 usable reads were sampled" / "Unknown data type: Mixture", rc 0; GTF as BED: 12-column skip notes then the same message; MAPQ-1 BAM: same message at -q 30, 1.0000 dUTP with -q 0'),
             A('Real unstranded library is read correctly', 'PASS', 'chrX ERR188383 0.4643 / 0.4525 with 8.3% failed to determine: Skill table says ~0.5 / ~0.5 = unstranded'),
         ]),
    dict(index=4, type='Variant B', new='regression + NEW hand-truth BAM + real STAR SJ.out.tab',
         label='Junction read support: B07 / junction_stats on the planted overhang BAM, a NEW BAM of hand-specified CIGARs and flags, and 4 real STAR pass-2 BAMs vs SJ.out.tab',
         note='Overhang, min_overhang, D/I/S/H/=/X handling, NH and MAPQ rules, mate de-duplication and unindexed input all match hand truth (13/13 junctions), and unique-read counts equal STAR SJ.out.tab on every shared junction of 4 real samples.',
         basic=37, specialized=53,
         assertions=[
             A('Overhang equals the adjacent-block overhang on the auditor\'s planted CIGARs', 'PASS', 'se_overhang.bam: micro4 -> 4 and 4 (reads>=8 = 0 of 12), micro10 -> 10, ov6 -> 6, ov50 -> 50 (out/42_in4.log); the pre-fix 30 vs 4 error is gone'),
             A('NEW BAM (10M2D20M500N30M, 5S45M300N50M, 20M1I30M400N50M, 50M300N30M5H, two-junction reads, no-NH / MAPQ 3 / NH=2 / MAPQ 0 with NH=1 / reverse / secondary / supplementary, mates crossing the same, one, or two junctions, 3M overhang, second contig) equals the hand truth table', 'PASS', '13 of 13 junctions equal on reads, reads_all and min_overhang; 0 extra junctions; min_overhang 0 / 30 / 60 give 7 / 5 / 0 as predicted (out/42_in4.log, data/edge_truth.json)'),
             A('Counts equal STAR SJ.out.tab unique reads on real data (4 samples, my own STAR 2.7.11b 2-pass run)', 'PASS', 'equal on 2765/2765, 2829/2829, 2792/2792, 2919/2919 shared junctions; junctions with >= 10 reads 371 / 398 / 380 / 377 = STAR; 27-50 extra junctions per BAM are absent from SJ.out.tab (ERR204916: 50, all with 1-4 reads, 21 GT..AG and 17 CT..AC canonical; consistent with the SJ.out.tab filters of STAR; out/56_only_helper.log)'),
             A('Unindexed BAM and BAM without spliced reads give a clear result, no crash', 'PASS', 'unindexed micro BAM read with until_eof; unspliced BAM gives {} / 0.0%; report raises NoSplicedReadsError (out/13_in1_guards.log)'),
             A('B07 CLI runs and its summary is internally consistent', 'PASS', 'se_overhang: 6 junctions, 3 with anchored reads, 3 with >= 10; edge: 13 / 12 / 0; reads_anchored <= reads_total everywhere'),
         ]),
    dict(index=5, type='Stress', new='regression, re-run on my own STAR index',
         label='Cohort-style STAR 2-pass: B02 and B03 (merge, pass 2, samtools index) on 4 real chrX 2x75 samples with my own index, plus the Common Errors table',
         note='B02/B03 ran with only path substitutions on all 4 samples; the merged file equals an independent recomputation (6 novel junctions, none annotated); STAR defaults, XS tag and every Common Errors message reproduce verbatim.',
         basic=36, specialized=52,
         assertions=[
             A('B02 and B03 run unedited (paths only) on 4 real samples and improve mapping', 'PASS', 'rc 0 on 8 runs, --sjdbOverhang 149 with 75-nt reads, unique mapping 97.63 -> 97.67, 97.24 -> 97.29, 97.53 -> 97.54, 96.95 -> 96.98 (out/51_in5_star.log)'),
             A('The merge filter does what the comments say', 'PASS', '$6==0 && $5>0 && $7>=3 | cut -f1-4 | sort -u = 6 junctions, 4 columns, equals independent recomputation, 0 present in the GTF (out/53_in5_check.log); pass-2 SJ.out.tab marks 3 of 3 merged junctions found as annotated (col 6 = 1), as the Skill notes'),
             A('Flag and default claims: alignIntronMax, XS tag, --outSAMtype None, overhang defaults', 'PASS', 'STAR --help: alignIntronMax 0 = 2^16 x 9 = 589,824; alignSJoverhangMin 5, alignSJDBoverhangMin 3; XS tag on 24113 / 24113 (and 3 other samples 100%) spliced records with --outSAMstrandField intronMotif'),
             A('Common Errors messages are the real ones', 'PASS', 'sjdbOverhang mismatch "present --sjdbOverhang=74 is not equal to the value at the genome generation step =149"; "Fatal LIMIT error ... =10552 is larger than the limitSjdbInsertNsj=100 / SOLUTION: re-run with at least --limitSjdbInsertNsj 10552"; pysam "fetch called on bamfile without index"; RSeQC zero-read messages (out/54_in5_errors.log)'),
             A('Data-derived numbers in the Skill hold on the new samples', 'PASS', 'junctions with >= 10 reads 10.5-12.0% (Skill: 11%); 5,717 lines / 2,184 distinct / 2,178 annotated in the old merge is a fixer measurement on the same data. Veeneman 2016 wording not re-fetched (offline)'),
         ]),
    dict(index=6, type='Scope Boundary', new='regression + NEW variant panel',
         label='Splice-site strength: B08 unedited, MaxEntScan on 10k real chrX introns vs decoys via the helper, SpliceAI (B09 command) on a NEW panel of canonical-site, exonic and deep-intronic variants',
         note='B08 prints the documented [10.86, 2.68] [11.58]; helper keeps one output per input; MaxEnt cut-offs hold on real data (AUC 0.969 / 0.954); SpliceAI separates canonical-site variants (max DS 0.99-1.00) from exonic (<= 0.07) and deep-intronic (0.00) ones.',
         basic=36, specialized=51,
         assertions=[
             A('B08 prints the documented scores', 'PASS', '[10.858, 2.676] [11.580] exactly; helper on [good, 7-mer, N, lower-case] gives [10.86, nan, nan, 2.68] and acceptors [11.58, -7.20, nan] (out/61_in6.log)'),
             A('MaxEnt cut-offs (>8 strong, <5 weak) are supported on real sites (independent script)', 'PASS', '10,095 annotated GT donors: 62.5% > 8, 10.8% < 5, median 8.68; 451 non-GT donors 100% < 5; 2000 decoy GT donors 94.0% < 5; AUC donor 0.969, acceptor 0.954. The Skill quotes 8,549 donors, 60.7% / 11.6%, 95.5% of 88 decoys: same conclusion, different sampling (not identical numbers)'),
             A('SpliceAI command works and separates classes on a NEW panel (GRCh37 chrX, -A grch37 because the FASTA is GRCh37, as the Skill requires the assembly to match)', 'PASS', '2 donor GT>AT: max DS 0.99, 0.99; 2 acceptor AG>AA: 1.00, 1.00; 3 exon-interior SNVs <= 0.07; 3 deep-intronic 0.00 (out/63_in6b.log)'),
             A('Splice-site scores stay research-scoped (Practice Boundaries)', 'PASS', 'Scope section, PP3/BP4 cut-offs framed as references for prioritising sites, "classifying a patient\'s variant ... out of scope"; no individual diagnosis or prescription'),
             A('Practical throughput of the helper is documented', 'PASS', 'maxentpy score3 measured ~0.1 s per acceptor under load (300 acceptors 31.8 s; 8k donors + acceptors ~20 min): not stated in the Skill (P2), but nothing wrong'),
         ]),
    dict(index=7, type='Adversarial', new='regression + NEW fastq_screen data + real Picard',
         label='rRNA and 3-prime bias: B12 and B10 unedited on planted libraries; Picard with the SKILL.md awk refFlat on real chrX; fastq_screen on NEW reads',
         note='rRNA recipe now gives 22.2% for a planted 22.2%; the awk refFlat is valid and Picard matches an independent aggregate on real data; fastq_screen reproduces 25.00% on new reads and both documented misconfigurations. The 5\'-3\' bias threshold contradicts geneBody on a low-depth real sample.',
         basic=35, specialized=50,
         assertions=[
             A('samtools rRNA recipe (B12) reproduces the planted 22.2%', 'PASS', '22.2% with -F 0x904; the old recipe reads 8170 / 52282 = 15.6% (out/71_in7.log); Picard PCT_RIBOSOMAL_BASES 0.222277'),
             A('B10 awk refFlat + Picard + geneBody work on planted libraries', 'PASS', 'PCT_CORRECT_STRAND_READS 1 (SECOND_READ for dUTP, FIRST_READ for forward); MEDIAN_5PRIME_TO_3PRIME_BIAS 1.009 / 1.002 uniform vs 0.0466 3-prime; geneBody 5p/3p 1.03 vs 0.043'),
             A('The awk refFlat and Picard are correct on real chrX (NEW, independent check)', 'PASS', 'refFlat 6001 lines, 0 differ from the BED12 blocks (round trip); Picard PF_ALIGNED_BASES 7,373,062 = pysam aligned bases; intergenic 0.025654 vs independent 0.0257; coding+UTR+intronic+intergenic = 1.0000 (out/73_in7_real.log)'),
             A('fastq_screen setup claims on NEW reads (4000 SE reads, 25% rRNA)', 'PASS', 'literal --aligner minimap2 command: One_hit_one_genome 25.00% (minimap2 alone 24.9%); missing prefix.fa.gz: rc 0, 100% unmapped, "Aligner warning ... failed to open ... rrna_ref.fa.gz"; default aligner: rc 255 (out/74_in7_fqscreen.log)'),
             A('The 5\'-3\' bias thresholds give a right verdict on real data', 'FAIL', 'real chrX library (50k pairs, poly(A) test set): Picard MEDIAN_5PRIME_TO_3PRIME_BIAS 0.2745 -> "<0.5 = 3\' bias" but geneBody_coverage 5p/3p is 0.847 on the same BAM; the table gives no depth caveat (P2)'),
         ]),
    dict(index=8, type='NEW (auditor scenario)', new='NEW',
         label='Cohort QC loop over 4 real STAR pass-2 BAMs + 2 planted libraries with the helper API, and diagnosis of a high novel-junction rate (annotation gap vs artifact)',
         note='The loop flags the novel-rich sample and the real libraries as designed, per-sample classes equal independent pysam; an annotation-gap scenario reads 46.1% known and returns to 93.4% with the full gene model, but the Skill gives no runnable recipe to tell annotation gaps from artifacts.',
         basic=33, specialized=48,
         assertions=[
             A('generate_qc_report loop flags the right samples (usage-guide prompt "report samples below acceptable thresholds")', 'PASS', 'novel-rich 0.223 Suspect + "<30% junctions >= 10 reads"; clean planted Healthy; real libraries known 0.993-0.996 Healthy, saturation still rising, 10.5-12.0% >= 10 reads (out/82_n1.log)'),
             A('Per-sample class counts on the 4 real pass-2 BAMs equal independent pysam', 'PASS', 'EQUAL reads and junctions 4/4'),
             A('Annotation-gap scenario behaves as the Skill says (Suspect, then Healthy after updating annotation)', 'PASS', 'clean BAM vs a gene model with half the genes: known 46.1% / novel 53.9%; full model 93.4% / 6.6% (out/80_new_diagnose.log)'),
             A('The Skill gives a runnable drill-down that separates annotation gaps from mapping artifacts', 'FAIL', 'the Decision Tree says "drill down" for novel% > 40 but no step or helper splits novel junctions by support or overhang; median read_count of novel classes (2 in the gap scenario vs 5-6 in the artifact-like library) had to be computed by hand from the .xls'),
             A('Helper report verdicts are usable as machine-readable QC', 'PASS', 'generate_qc_report returns a dict; verdict strings are depth-blind (real 50k-pair libraries print POOR / still rising), acceptable for a subset but not flagged'),
         ]),
]

for i in inputs:
    i['total'] = i['basic'] + i['specialized']
    i['assertions_passed'] = sum(a['result'] == 'PASS' for a in i['assertions'])
    i['assertions_total'] = len(i['assertions'])
    i['status'] = 'COMPLETED'
    i['status_flag'] = '\u2705' if i['assertions_passed'] == i['assertions_total'] else '\u26a0\ufe0f'
    i['executed'] = True
    i['execution_note'] = i['note']

n = len(inputs)
avg = round(sum(i['total'] for i in inputs) / n, 1)
l1 = round(sum(i['basic'] for i in inputs) / n, 1)
l2 = round(sum(i['specialized'] for i in inputs) / n, 1)
ap = sum(i['assertions_passed'] for i in inputs)
at = sum(i['assertions_total'] for i in inputs)
static = 82
final = round(static * 0.4 + avg * 0.6, 1)
score = int(final + 0.5)
print('avg', avg, 'L1', l1, 'L2', l2, 'assert', ap, at, 'final', final, score)

static_cats = {
    'functional_suitability': (10, 12, 'Every block the fix touched now runs and matches an independent method (known/novel snippet, overhang, STAR merge, rRNA, MaxEnt example, Picard refFlat, SpliceAI, fastq_screen). Remaining errors: the -l/-u/-s refinement tip, the "printed summary is junction-level" wording, depth-blind bias threshold.'),
    'reliability': (9, 12, 'Helper turns the silent RSeQC failures into clear errors (BED6, contig mismatch, no spliced reads, no Rscript); documented error strings are the real ones. Raw RSeQC is still silent by design, and the helper lo/hi/step arguments silently produce a wrong curve when lo != step.'),
    'performance_context': (6, 8, 'SKILL.md is 401 lines with no references/ split; usage-guide is now a short pointer. maxentpy throughput (~0.1 s per acceptor) is undocumented.'),
    'agent_usability': (14, 16, 'One threshold table, design targets separate, BED12 preparation and contig checks explained up front, exact output strings for both strandedness modes; no drill-down recipe for a high novel rate.'),
    'human_usability': (6, 8, 'Clear triggers and prompts, tolerant helper errors; verdicts are depth-blind and a user must read conventions labels to know what is measured.'),
    'security': (11, 12, 'No secrets; subprocess with argument lists and no shell; paths passed through unvalidated to RSeQC.'),
    'maintainability': (11, 12, 'One implementation of junction counting, a self-contained test that ran green in two envs; the test does not cover lo != step or the CLI exit codes.'),
    'agent_specific': (15, 20, 'Good biology-vs-artifact framing and honest "convention" labelling; unseeded RSeQC subsampling is stated; several literature statements (Veeneman, Brown 2022 gene list, Walker 2023 cut-offs) cannot be checked offline.'),
}
assert sum(v[0] for v in static_cats.values()) == static, sum(v[0] for v in static_cats.values())

blocks = [
    ('B01', 'helper report CLI', 'ran unedited; planted, real chrX'),
    ('B02', 'STAR pass 1', 'ran, only genomeDir / GTF / fastq paths substituted; 4 real samples'),
    ('B03', 'merge + STAR pass 2 + samtools index', 'ran, same substitutions; merge recomputed independently'),
    ('B04', 'junction_saturation + helper', 'ran unedited (inside as-core); tip about -l/-u/-s FAILS'),
    ('B05', 'junction_annotation', 'ran unedited; class counts = pysam'),
    ('B06', 'pandas known/novel snippet', 'ran unedited on real RSeQC output: 93.4% / 22.3% / 99.5%'),
    ('B07', 'junctions CLI', 'ran unedited on 2 BAMs'),
    ('B08', 'MaxEnt example', 'ran unedited (as-maxent): [10.86, 2.68] [11.58]'),
    ('B09', 'SpliceAI command', 'ran, only files and -A grch37 changed (GRCh37 FASTA); 10-variant panel'),
    ('B10', 'awk refFlat + Picard + geneBody', 'ran (Picard in af-picard3); strand flag changed per library; RIBOSOMAL_INTERVALS dropped for real chrX'),
    ('B11', 'infer_experiment', 'ran unedited on 7 planted + real + 4 failure cases'),
    ('B12', 'samtools rRNA', 'ran unedited: 22.2%'),
    ('inline', 'gffread then cut -f1-12 BED12 recipe', 'ran on the real GTF: 6001 lines x 12 columns'),
    ('inline', 'fastq_screen --aligner minimap2', 'ran on new reads: 25.00%'),
    ('file', 'examples/test_splicing_qc.py', 'ran green in as-core (MaxEnt skipped) and as-maxent (all checks)'),
]

report = {
    'meta': {
        'skill_name': 'bio-splicing-qc',
        'description': 'Assesses RNA-seq data quality for alternative splicing analysis: design audit, STAR cohort-style 2-pass, junction saturation, known-vs-novel junction ratio, overhang, splice-site strength (MaxEntScan, SpliceAI), strandedness, 3-prime bias and rRNA screening.',
        'evaluated_on': '2026-09-20',
        'evaluator_version': 'skill-auditor@1.0',
        'category': 'Data Analysis',
        'execution_mode': 'D',
        'complexity': 'Complex',
        'n_inputs': n,
        'source': SRC,
        'audit_kind': 're-audit of a fixed Skill (pre-fix 67, Reject, Research Veto M4); auditor different from first auditor and fixer',
        'executed_k_of_n': '8/8 (not executed: featureCounts -s 2, Qualimap, fastq_screen with bowtie2/bwa/bowtie, Picard from a GTF via gtfToGenePred; citation texts not re-fetched offline)',
        'execution_note': 'All 8 inputs executed in WSL envs as-core (RSeQC 5.0.5, STAR 2.7.11b, samtools 1.24, pysam 0.24.1, minimap2, fastq_screen 0.16.0), as-maxent (maxentpy 0.0.2), as-spliceai (SpliceAI 1.3.1) and af-picard3 (Picard 3.5.0). Inputs 1-7 re-run the pre-fix audit inputs (its planted BAMs copied to run/data/synthetic, labelled synthetic); inputs 3, 4, 6, 7 add new data (SE libraries, hand-truth CIGAR BAM, variant panel, fastq_screen reads, real Picard) and input 8 is a new scenario. STAR index and 2-pass runs are my own (scratch F:\\OpenScience\\as-qc-reaudit-scratch).',
        'env': 'WSL science: as-core, as-maxent, as-spliceai, af-picard3; Windows Python only for block extraction. No package installed or changed.',
        'data': 'real: nf-core chrX GRCh37 RNA-seq (4 samples, BAM + FASTQ + GTF), real X.fa; synthetic and labelled: run/data/synthetic (pre-fix auditor planted BAMs), run/data/edge.bam + edge_truth.json, run/work/in3 SE BAMs, run/work/in7/fq reads',
        'pre_fix': {'score': 67, 'grade': 'Reject', 'veto': 'Research Veto M4 code usability'},
    },
    'veto_gates': {
        'skill_veto': {'gate': 'PASS', 'stability': 'PASS', 'contract': 'PASS', 'determinism': 'PASS', 'security': 'PASS'},
        'research_veto': {
            'applicable': True, 'gate': 'PASS',
            'scientific_integrity': {'result': 'PASS', 'detail': 'No fabricated result, DOI or trial. The chrX MaxEnt figures quoted in the Skill (8,549 donors, 60.7% / 11.6%, 95.5% of 88 decoys) are not the numbers my independent script got (10,095 donors, 62.5% / 10.8%, 94.0% of 2000 decoys, AUC 0.969 / 0.954) but support the same cut-offs; the junction-support and 2-pass numbers reproduced. Literature statements (Veeneman 94%, Brown 2022 / Klim 2019 gene list, Walker 2023 thresholds) could not be re-fetched offline.'},
            'practice_boundaries': {'result': 'PASS', 'detail': 'A Scope section states research QC only; SpliceAI PP3/BP4 cut-offs are cited as published references for prioritising sites, and classifying a patient\'s variant is declared out of scope.'},
            'methodological_ground': {'result': 'PASS', 'detail': 'Known fraction is read-weighted with the junction-level number reported beside it; the rRNA recipe is on primary mapped records; no principled fallacy. The plateau rule uses only the known curve (a library with a large low-count novel tail reads PLATEAU), stated as such.'},
            'code_usability': {'result': 'PASS', 'detail': 'All 12 fenced blocks plus the inline gffread, fastq_screen and awk recipes were run from the copied files with checked output; the pre-fix failures (0.0% snippet, Rscript exit 1, EmptyDataError, wrong overhang, 15.6% rRNA, MaxEnt -7.20 acceptor, exit-255 fastq_screen) are all fixed. The one documented refinement that does not work (-l/-u/-s for 80-100%) is an optional tip beside a correct default path, recorded as P1.'},
        },
    },
    'static_score': {'subtotal': static, 'max': 100, 'categories': {k: {'score': v[0], 'max': v[1], 'note': v[2]} for k, v in static_cats.items()}},
    'dynamic_score': {
        'execution_avg': avg, 'max': 100,
        'assertion_pass_rate': {'passed': ap, 'total': at},
        'inputs': [{k: i[k] for k in ('index', 'type', 'label', 'status', 'status_flag', 'note', 'basic', 'specialized', 'assertions', 'total', 'assertions_passed', 'assertions_total', 'executed', 'execution_note')} for i in inputs],
    },
    'final': {
        'static_weighted': round(static * 0.4, 1), 'dynamic_weighted': round(avg * 0.6, 1),
        'score': score, 'max': 100, 'grade': 'Production Ready', 'grade_symbol': '\u2b50',
        'deployable': True, 'veto_override': False,
        'note': f'Pre-fix 67 (Reject, M4 fired) -> {score}. Layer 1 average {l1}/40, Layer 2 average {l2}/60, assertion pass {ap}/{at}. No open P0; one open P1 (the -l/-u/-s refinement tip). Every Production Ready floor is met (static {static} >= 80, execution {avg} >= 85, L1 >= 32, L2 >= 48, assertions {ap/at:.0%} >= 90%), but only just: static and execution each carry 2-5 points of judgment, so treat {score} as the low end of Production Ready.',
    },
    'key_strengths': [
        'All three pre-fix P0s are fixed and verified on real output: the known/novel snippet prints 93.4% / 22.3% / 99.5% and equals an independent pysam classification; RSeQC without Rscript, and BAMs without spliced reads, now fail with a stated cause.',
        'junction_stats equals STAR SJ.out.tab unique-read counts on every shared junction of four real samples (2765/2765, 2829/2829, 2792/2792, 2919/2919) and matches a hand-truth BAM of 13 junctions with D/I/S/H/=/X, NH/MAPQ, flag and mate cases.',
        'Documented error strings, defaults and recipes are now the observed ones (STAR sjdbOverhang / limitSjdbInsertNsj, pysam, RSeQC zero-read messages, alignIntronMax 589,824, rRNA 22.2%, fastq_screen 25.00%, Picard refFlat matches an independent aggregate).',
        'A self-contained test ships with the Skill and passes in two envs; usage-guide redundancy is gone and thresholds sit in one table.',
    ],
    'recommendations': [
        {'priority': 'P1', 'title': 'The documented "-l/-u/-s for a finer 80-100% range" tip gives wrong curves', 'observed_in': [2],
         'problem': 'RSeQC adds (index_end - index_st) from zero, so with -l 80 -u 100 -s 5 the "80%" point is 5% of the reads and "100%" is 25%. The mid library gives growth 263% and the saturated deep library flips from PLATEAU to STILL RISING (11.1%) with helper lo=80; lo=50 reaches only 157 of 180 known junctions at "100%". The default and l == s (e.g. -l 2 -u 100 -s 2) are correct.',
         'root_cause': 'The refinement was written from the option names, never run, and the helper exposes lo/hi/step without a guard.',
         'fix': 'Replace the tip with "for a finer curve lower -s and keep -l equal to -s (-l 2 -u 100 -s 2)"; make junction_saturation() raise or warn when lo != step; add a test on the planted deep BAM.'},
        {'priority': 'P2', 'title': 'RSeQC summary wording and a missing drill-down for a high novel rate', 'observed_in': [1, 8],
         'problem': 'The Skill says the printed summary is junction-level; RSeQC prints both Splicing Events (read-weighted) and Splicing Junctions. The Decision Tree says "drill down" for novel% > 40 but gives no step to tell annotation gaps from mapping artifacts (novel-junction support, overhang).',
         'root_cause': 'Definitions were inferred from one output; the drill-down is prose only.',
         'fix': 'State that both blocks are printed and which one the thresholds use; add a helper or 6-line recipe that joins the .junction.xls classes with junction_stats() and reports median reads and min overhang per class.'},
        {'priority': 'P2', 'title': 'Depth-blind thresholds: 5\'-3\' bias and the helper verdicts', 'observed_in': [7, 8],
         'problem': 'On a real 50k-pair library Picard MEDIAN_5PRIME_TO_3PRIME_BIAS is 0.2745 (rule: < 0.5 = 3\' bias) while geneBody_coverage 5p/3p is 0.847; the helper prints POOR / still rising for four real libraries of that depth.',
         'root_cause': 'Conventions labelled as such but without a depth condition.',
         'fix': 'Say the ratio needs enough reads on the top expressed transcripts and to confirm with geneBody_coverage; print read counts beside the helper verdicts.'},
        {'priority': 'P2', 'title': 'Unstated cost and unverifiable references', 'observed_in': [6],
         'problem': 'maxentpy score3 costs ~0.1 s per acceptor (about 20 min for 10k introns), not mentioned; the quoted chrX MaxEnt numbers differ from an independent re-count; Veeneman 2016, the Brown 2022 gene list and Walker 2023 cut-offs could not be re-checked offline.',
         'root_cause': 'Numbers from one sampling of the test data, prose citations.',
         'fix': 'Add a throughput note and "about 60% > 8, about 11% < 5" wording; cite page/table for the paper statements.'},
        {'priority': 'P2', 'title': 'SKILL.md length and residual clinical vocabulary', 'observed_in': [5, 6],
         'problem': '401-line SKILL.md with no references/ split; PP3/BP4 codes remain in the SpliceAI paragraph though scoped as research use.',
         'root_cause': 'Single-file layout.',
         'fix': 'Move STAR 2-pass and Picard details to references/; keep the cut-offs but drop the ACMG code names.'},
    ],
}

(ROOT / 'eval_report_bio-splicing-qc_result.json').write_text(json.dumps(report, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')

# ---------------------------------------------------------------- viewer
L = []
w = L.append
w('# Eval Viewer \u2014 bio-splicing-qc (re-audit of the fixed Skill)')
w('Generated: 2026-09-20')
w(f'Source: `{SRC}` (read from a copy in `run/skill/`, identical to the worktree file by `cmp`; the worktree and clone were not written to).')
w(f'Pre-fix (archived at `_pre-fix-20260920`): 67, Reject, Research Veto M4 (code usability) fired, open P0s. **Now: {score}, Production Ready, deployable, no veto, no open P0, one open P1.**')
w(f'Category: Data Analysis. Mode D. Complexity: Complex, N = {n}. Executed 8/8. Every script that was run is in `run/` (logs in `run/out/`); synthetic data are in `run/data/` and labelled synthetic in their generator docstrings.')
w('')
w('## How the M4 (code usability) veto was re-judged')
w('Every fenced block of SKILL.md was extracted to `run/blocks/` by `00_extract_blocks.py` (12 blocks) and parse-checked (`bash -n`, `ast.parse`, `out/00_extract.log`, `out/01_syntax_and_test.log`). Each block was then run from its file, with only paths substituted where noted:')
w('')
w('| block | what | how run / result |')
w('|---|---|---|')
for b in blocks:
    w(f'| {b[0]} | {b[1]} | {b[2]} |')
w('')
w('Pre-fix M4 evidence re-judged: (1) the snippet printing 0.0% / 0.0% now prints the true fractions; (2) RSeQC exit 1 without Rscript is documented and `--skip-plot` is in every call; (3) `generate_qc_report` on a BAM without spliced reads now raises `NoSplicedReadsError` with a message; (4) the wrong overhang / ignored `min_overhang` / `=X` helpers are one corrected implementation. **M4: PASS.** M1 (integrity), M2 (practice boundaries), M3 (method) unchanged: PASS.')
w('')
w('## Summary Table')
w('')
w('| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |')
w('|---|---|---|---|---|---|---|')
for i in inputs:
    w(f"| {i['index']} | {i['type']}: {i['label'][:90]}{'...' if len(i['label']) > 90 else ''} | {i['basic']} | {i['specialized']} | {i['total']} | {i['assertions_passed']}/{i['assertions_total']} | {i['status_flag']} |")
w('')
w(f'**Execution Average: {avg} / 100. Assertion Pass Rate: {ap}/{at}.** Static {static} x 0.4 = {static*0.4:.1f}; dynamic {avg} x 0.6 = {avg*0.6:.1f}; **final {score}** ({final}). Layer 1 average {l1}/40, Layer 2 average {l2}/60. The margin over 85 is thin; see the note in the JSON.')
w('')
w('## Detailed Outputs')
detail = {
    1: '''Ran B05 and B06 unedited in a directory holding `sample.bam` / `genes.bed12` (`10_in1_annot.sh`), then B01. Independent check `11_in1_indep.py` classifies junctions with pysam + BED12 only.
```
se_clean       : known: 93.4%, novel: 6.6%    | helper: known 93.4% of 12410 reads (34.6% of 719 junctions) -> Healthy
se_novelrich   : known: 22.3%, novel: 77.7%   | helper: known 22.3% of 12014 reads (13.0% of 1857 junctions) -> Suspect or interesting
real chrX      : known: 99.5%, novel: 0.5%    | BED12 from `gffread genes_chrX.gtf --bed | cut -f1-12`: 6001 lines x 12 columns
independent    : reads {'annotated': 25023, 'complete_novel': 49, 'partial_novel': 84}; EQUAL reads True, junctions True (also se_clean, se_novelrich)
guards (13/14/15): BED6 -> "60 lines have fewer than 12 columns" rc 1; contig mismatch -> "no contig name shared by BAM ['chrS'] and BED ['S']" rc 1;
                   unspliced.bam -> "RSeQC found no spliced reads at MAPQ >= 30" rc 1; literal RSeQC, Rscript absent -> "Rscript executable not found" rc 1;
                   helper --plot with no Rscript on PATH -> tables written, rc 0
```
The raw annotation values are `[' annotated', ' complete_novel', ' partial_novel']` (leading space), which is why the strip in B06 matters.''',
    2: '''B04 run per library inside as-core (`20_in2_sat.sh`, 3 runs each; `21_in2_fine.sh`, `23_deep_fine.sh` for the tip).
```
known-curve growth 80->100%:  deep 0.0 / 0.0 / 0.0 PLATEAU | mid 5.3 / 4.7 / 2.9 % RISING | shallow 11.1 / 11.8 / 7.8 % RISING | real chrX 7.6 % RISING (563 -> 2698)
all-junction count at 100%: 919 / 1022 / 951 (= distinct junctions in truth.json)
-l 80 -u 100 -s 5 (mid): "sampling 80% (86) ... 100% (428)" of 1710 reads; helper lo=80 growth known 2.63
deep, truth PLATEAU:  lo=5 step=5 -> 0.000 PLATEAU | lo=80 step=5 -> 0.111 STILL RISING | lo=2 step=2 -> 0.000 PLATEAU
```
RSeQC source (`qcmodule/SAM.py` line 4016-4019): `index_st = int(SR_num*((pertl-sample_step)/100)); sample_size += index_end - index_st` starting from 0.''',
    3: '''`31_in3_strand.sh` (B11 unedited per library; `30_in3_make_se.py` builds the new SE and MAPQ-1 BAMs from the planted PE data).
```
PE dutp 1.0000 "1+-,1-+,2++,2--" | fwd 1.0000 "1++,1--,2+-,2-+" | unstr 0.5011/0.4989 | leak20 0.7975 | leak40 0.5914
SE dutp "+-,-+" 1.0000 | SE fwd "++,--" 1.0000 | real chrX 0.4643/0.4525, failed 0.0831
contig mismatch -> Total 0 usable reads were sampled / Unknown data type: Mixture ; MAPQ-1: same at -q 30, dUTP 1.0000 at -q 0
```''',
    4: '''`40_in4_make_edge.py` (NEW hand-truth BAM, 82 records, 13 junctions), `41_in4_junctions.py`, and `52_in5_check.py` against STAR SJ.out.tab.
```
edge.bam: junctions equal to hand truth 13 of 13; extra junctions []; min_overhang 0/30/60 on the pair-overlap junction -> 7 / 5 / 0 (expected)
se_overhang.bam: overhang 4 -> reads>=8 0 of 12 | 10 -> 12 | 6 -> 0 | 50 -> 12
real STAR pass 2: helper vs SJ.out.tab unique reads equal on 2765/2765, 2829/2829, 2792/2792, 2919/2919; >=10 reads 371/398/380/377 vs STAR 371/398/380/377
```''',
    5: '''`50_in5_index.sh` (own STAR index, sjdbOverhang 149), `51_in5_star.sh` (B02 and B03 via `sed` path substitution only), `53_in5_check.sh`, `54_in5_errors.sh`.
```
merged: 6 lines x 4 columns, equals independent recomputation, 0 in GTF | pass-2 SJ.out.tab: 3 of 3 merged junctions have col6 = 1
unique mapping p1 -> p2: 97.63->97.67, 97.24->97.29, 97.53->97.54, 96.95->96.98 | XS tag on 100% of spliced records in pass 2
STAR --help: alignIntronMax 0 = (2^16)*9 | EXITING ... present --sjdbOverhang=74 is not equal to the value at the genome generation step =149
Fatal LIMIT error: ... =10552 is larger than the limitSjdbInsertNsj=100 / SOLUTION: re-run with at least --limitSjdbInsertNsj 10552 | pysam: fetch called on bamfile without index
```''',
    6: '''`61_in6.sh` (B08 + `60_in6_sites.py`), `63_in6b_spliceai.sh` (B09 with -A grch37; `62_in6b_make_vcf.py` builds the panel).
```
B08: [10.858, 2.676] [11.580] | helper: [10.86, nan, nan, 2.68] and [11.58, -7.20, nan]
chrX: 10095 GT donors 62.5% >8, 10.8% <5, median 8.68; 451 non-GT donors 100% <5; decoys 94.0% <5; AUC donor 0.969, acceptor 0.954
SpliceAI: donor GT>AT 0.99/0.99 | acceptor AG>AA 1.00/1.00 | exon-interior <=0.07 | deep intronic 0.00
```''',
    7: '''`71_in7.sh` (B12, B10 unedited), `73_in7_real.sh` + `72_in7_real_picard.py`, `74_in7_fqscreen.sh` with `70_in7_make_fq.py`.
```
B12: rRNA: 22.2% (old recipe 8170/52282 = 15.6%) | Picard PCT_RIBOSOMAL_BASES 0.222277
Picard bias: uniform 1.009 / 1.002, 3-prime 0.0466 | geneBody 5p/3p 1.03 vs 0.043 | strand 1.0
real chrX: refFlat 6001 lines, 0 differ from BED12 | PF_ALIGNED_BASES 7,373,062 = pysam | intergenic 0.025654 vs 0.0257 | bias 0.2745 vs geneBody 0.847
fastq_screen: 25.00% One_hit_one_genome (minimap2 24.9%) | missing .fa.gz -> rc 0, 100% unmapped, Aligner warning | default aligner rc 255
```''',
    8: '''`80_new_diagnose.sh`, `81_n1_cohort.py` + `82_n1.sh`.
```
sample             known_rd known_jn   growth  %>=10rd  status
ERR188383             0.996    0.964    0.078     11.2  Healthy   saturation still rising; <30% junctions >=10 reads
ERR188428 / ERR188454 / ERR204916  0.995 / 0.994 / 0.993 Healthy, same two flags (10.5-12.0% >= 10 reads)
planted_clean         0.934    0.346    0.000     32.5  Healthy
planted_novelrich     0.223    0.130    0.000     14.6  Suspect or interesting  known<80%; <30% junctions >=10 reads
annotation gap (half the genes missing): known 46.1% / novel 53.9%; median read_count novel classes 2 (vs annotated 56); full model 93.4% / 6.6%
```''',
}
for i in inputs:
    w('')
    w(f"### Input {i['index']} \u2014 {i['type']} ({i['new']})")
    w(f"**Prompt:** {i['label']}")
    w(detail[i['index']])
    w(f"**Scores:** {i['basic']} / {i['specialized']} / {i['total']}. Assertions {i['assertions_passed']}/{i['assertions_total']}:")
    for a in i['assertions']:
        w(f"- {a['result']}: {a['text']} \u2014 {a['note']}")
w('')
w('## Pre-fix defects re-checked')
w('')
w('| pre-fix finding | now |')
w('|---|---|')
for a, b in [
    ('P0 known/novel snippet prints 0.0% / 0.0%', 'fixed: 93.4% / 22.3% / 99.5% on real RSeQC output, equal to independent counts (inputs 1, 8)'),
    ('P0 RSeQC exit 1 without Rscript, Rscript unlisted', 'fixed: `--skip-plot` in every call, requirement stated, reproduced both ways (input 1)'),
    ('P0 generate_qc_report EmptyDataError on BAM without spliced reads', 'fixed: NoSplicedReadsError, exit 1 with cause (input 1)'),
    ('P1 overhang / min_overhang / =X / multi-mapper / mate double counting', 'fixed and checked against hand truth and STAR SJ.out.tab on 4 real samples (input 4)'),
    ('P1 rRNA recipe 15.6% for 22.2%; fastq_screen aligner', 'fixed: 22.2%; 25.00%, both misconfigurations described correctly (input 7)'),
    ('P1 MaxEnt acceptor -7.20; misaligned outputs; SystemExit/KeyError', 'fixed (input 6)'),
    ('P1 wrong failure-mode text, STAR error strings, alignIntronMax, microexon flag, flat-curve claim', 'fixed; messages verbatim (inputs 3, 5, 2)'),
    ('P2 merge filter, XS tag, Veeneman numbers, thresholds, unseeded saturation', 'fixed or stated; Veeneman not re-fetched'),
    ('**new, introduced by the fix**: -l/-u/-s refinement tip and helper lo/hi/step', 'P1 (input 2)'),
]:
    w(f'| {a} | {b} |')
w('')
w('## Recommendations')
for r in report['recommendations']:
    w(f"- **{r['priority']}** {r['title']} (input {', '.join(map(str, r['observed_in']))}): {r['fix']}")
(ROOT / 'eval_viewer_bio-splicing-qc.md').write_text('\n'.join(L) + '\n', encoding='utf-8')
print('written')
