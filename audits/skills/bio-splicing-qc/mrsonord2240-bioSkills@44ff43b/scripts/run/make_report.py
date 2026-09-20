#!/usr/bin/env python
"""Assemble eval_report_bio-splicing-qc_result.json and eval_viewer_bio-splicing-qc.md from the audit results (numbers are the ones printed by the input*.py/.sh scripts)."""
import json
OUT = 'F:/OpenScience/audits/bio-splicing-qc'
A = lambda t, r, n: dict(text=t, result=r, note=n)
P, F = 'PASS', 'FAIL'

inputs = [
 dict(index=1, type='Canonical', label='Known vs novel junction classification of a library with planted class fractions (RSeQC junction_annotation + SKILL.md pandas snippet)',
  status='COMPLETED', status_flag='\u26a0\ufe0f', executed=True,
  note='RSeQC output correct vs independent pysam count, but the SKILL.md snippet prints "known: 0.0%, novel: 0.0%" because RSeQC 5.0.5 writes " annotated" with a leading space',
  basic=25, specialized=33,
  assertions=[
   A('RSeQC junction_annotation.py runs from the Skill example and its class counts equal an independent pysam count', P, 'clean: annotated 249 / partial 305 / complete 165 junctions, 11592/553/265 reads; identical to pysam and to planted truth (known 93.4% of reads)'),
   A('The SKILL.md pandas snippet reports the planted known fraction (93.4%)', F, 'printed known 0.0%, novel 0.0% on both libraries; annotation column values are " annotated", " partial_novel", " complete_novel" (leading space)'),
   A('Known-fraction thresholds (>=80 / 60-80 / <60) give the right verdict for clean (93%) vs novel-rich (22%) libraries once parsed', P, 'after .str.strip(): 93.4% Healthy and 22.3% Suspect; directionally right'),
   A('Definition of "known" matches what the Skill implies (annotated junction)', F, 'RSeQC calls a junction annotated when donor AND acceptor are each known, so unannotated exon-skipping junctions count as known (read-level 93.4% vs 86.7% strictly annotated); undocumented'),
   A('Read-weighted and junction-level readings are distinguished', F, 'same BAM: 93% of reads known but only 35% of junctions; RSeQC prints junction-level, the snippet is read-weighted; thresholds do not say which'),
  ]),
 dict(index=2, type='Variant A', label='Junction saturation on planted deep / mid / shallow libraries, real chrX, and contig-name mismatch',
  status='COMPLETED', status_flag='\u2705', executed=True,
  note='junction_saturation.py and the plateau rule work; known-curve growth 80->100%: deep 0.0% (PLATEAU), mid 8.4% and shallow 13.2% (RISING) vs analytic 0.0/5.6/13.6%',
  basic=31, specialized=44,
  assertions=[
   A('Plateau rule (<2% growth 80->100%) classifies the planted libraries correctly', P, 'deep PLATEAU; mid 8.4% and shallow 13.2% STILL RISING; expected 5.6% and 13.6% from Poisson thinning'),
   A('Curve values agree with independent expectation and pysam', P, 'RSeQC all-junction count at 100% equals pysam distinct junctions (919/1022/951); known curve within 3-16 junctions of expectation (unseeded shuffle)'),
   A('Real chrX ERR188383 verdict is produced and plausible', P, 'known 588 -> 2698, growth 6.7% STILL RISING; 100k-read subset, as expected'),
   A('Wrong contig naming is detected or warned about', F, 'BED contig "S" vs BAM "chrS": exit 0, every curve all zeros; the plateau rule then divides 0/0; nothing in the Skill warns'),
   A('SKILL.md "deep BAM -> flat curve is uninformative" claim is correct', F, 'RSeQC samples percentiles of splice events; a curve flat from 10% (sat_deep known 154 -> 180 by 10%) is the saturated case, i.e. informative'),
  ]),
 dict(index=3, type='Edge', label='Strandedness verification (infer_experiment) on planted dUTP / forward / unstranded / leaky PE libraries, real chrX and failure modes',
  status='COMPLETED', status_flag='\u2705', executed=True,
  note='infer_experiment table verified on all planted protocols; the documented failure mode and its fix are wrong',
  basic=30, specialized=47,
  assertions=[
   A('Decision table maps planted protocols to the right rMATS libType', P, 'dUTP 1.00 "1+-,1-+,2++,2--" -> fr-firststrand; forward 1.00 -> fr-secondstrand; unstranded 0.501/0.499; real chrX 0.464/0.453 (+8.3% undetermined)'),
   A('Leaky libraries land in the documented 70-90% band and the Skill says what to do', F, '80% dUTP reads 0.7975, 60% reads 0.59: band exists but no action or libType advice for 70-90%'),
   A('Contig mismatch / wrong BED is diagnosed', F, 'BED contig "S" vs BAM chrS and GTF-as-BED both exit 0 with "Total 0 usable reads were sampled" / "Unknown data type: Mixture"; Skill attributes 0 reads to sample size and says "0 of 200000 reads"'),
   A('Documented fix "use -q 30" restores a MAPQ-1 BAM', F, '-q 30 is already the default and gives "Unknown data type: Mixture"; -q 0 gives 1.00 dUTP'),
   A('Skill points at an existing, runnable tool with correct flags', P, '-i/-r/-s exist in RSeQC 5.0.5; BED6 also accepted by infer_experiment'),
  ]),
 dict(index=4, type='Variant B', label='Per-junction read counts, overhang and ">=10 reads" helpers vs planted CIGARs, multi-mappers, real chrX, regtools',
  status='COMPLETED', status_flag='\u274c', executed=True,
  note='SKILL.md junction_stats gives wrong overhang for multi-junction reads (30 vs true 4); example min_overhang is a no-op; =/X CIGAR shifts coordinates; multi-mappers and both mates counted',
  basic=24, specialized=27,
  assertions=[
   A('junction_stats overhang equals the planted adjacent-exon overhang', F, 'micro-exon reads 30M1000N4M800N66M: Skill 30 and 34 vs true 4 and 4; 20M700N10M900N70M: 20/30 vs 10/10; single-junction reads (6, 50) correct'),
   A('count_junction_reads honours min_overhang', F, 'min_overhang=8 and 99 return identical counts (72 reads, 6 junctions); parameter never used'),
   A('Counts agree with STAR SJ.out.tab / fragment-level counting on real PE data', F, 'chrX pass-2 BAM: read-level count equals STAR unique on 2163/2792 shared junctions, fragment-level on 2792/2792; >=10-read junctions 404 vs 371'),
   A('Junction coordinates correct for =/X CIGAR reads', F, 'example reports (200000,201000) vs true (200050,201050); SKILL.md function handles ops 7/8, example does not'),
   A('Failure on unindexed BAM / BAM without spliced reads is reported clearly', F, 'fetch() ValueError on STAR-sorted BAM without .bai; generate_qc_report on a BAM with no spliced reads raises EmptyDataError'),
  ]),
 dict(index=5, type='Stress', label='Cohort-style STAR 2-pass on 4 real chrX samples (2x75) exactly as in SKILL.md, plus flag and error-string claims',
  status='COMPLETED', status_flag='\u2705', executed=True,
  note='both passes run and improve unique-mapping 97.2->97.6%; several statements about the merge filter, defaults and error messages are wrong',
  basic=31, specialized=45,
  assertions=[
   A('Pass 1 and pass 2 commands run on current STAR (2.7.11b) and produce SJ.out.tab and GeneCounts', P, '4/4 samples; unique mapping 96.5-97.2% -> 97.0-97.6%; ReadsPerGene 2396 rows; --sjdbOverhang 149 with 75-nt reads also runs'),
   A('The awk filter does what SKILL.md says ("strand info AND >=3 unique reads", novel junctions)', F, 'column 5 is the intron motif, column 4 the strand; of 2184 merged junctions 2178 are already in the GTF (only 6 novel); 3533 duplicate lines survive sort -u'),
   A('SKILL.md STAR defaults and error strings are accurate', F, 'alignIntronMax default 0 = ~590 kb, not 1 Mb; "STAR: too many SJs in cohort merge" does not exist (real: Fatal LIMIT error ... re-run with --limitSjdbInsertNsj 10552); alignSJoverhangMin 8 lowers, not raises, microexon sensitivity vs default 5'),
   A('Commands leave an XS-taggable BAM as the strandedness note implies', F, '0 of 20000 spliced reads carry XS because --outSAMstrandField intronMotif is not in the pass commands (mentioned only in a comment)'),
   A('Cited 2-pass benefit is reproduced from the source', F, 'Veeneman 2016 reports >=94% of simulated novel junctions had improved quantification (per-sample two-pass), not 80-86% vs >=94% recovery nor a cohort-vs-per-sample comparison'),
  ]),
 dict(index=6, type='Scope Boundary', label='Splice-site strength: MaxEntScan on 8.5k real annotated chrX donors/acceptors vs decoys, example helper, SpliceAI CLI',
  status='COMPLETED', status_flag='\u26a0\ufe0f', executed=True,
  note='MaxEnt thresholds discriminate real from decoy sites (AUC 0.97/0.96) but the shipped acceptor example scores -7.20 and score_splice_sites misaligns outputs',
  basic=27, specialized=40,
  assertions=[
   A('MaxEnt strong/weak cut-offs (>8 / <5) are directionally supported on real sites', P, '8549 annotated GT donors: 61% >8, 28% 5-8, 12% <5, median 8.6; 88 decoy GT donors 95% <5; AUC donor 0.969, acceptor 0.958; all 399 non-GT annotated donors <5'),
   A('The SKILL.md acceptor example is a valid strong 3\'ss', F, "score3('T'*20+'CAG') = -7.20: the 20-nt intron ends TT, no AG; example script calls it an 'Example 3ss' expecting 8-12 bits"),
   A('Skill\'s documented invalid-input behaviour (ValueError or silently wrong score) matches maxentpy 0.0.2', F, 'wrong length -> SystemExit "Wrong length of fa!" (process ends, exit 0); N/X/U -> KeyError; lower-case accepted'),
   A('score_splice_sites returns scores aligned with its inputs', F, '4 donor inputs -> 3 outputs: the 8-mer is silently dropped and N gives None, so indices shift'),
   A('SpliceAI CLI flags and thresholds are usable', P, 'spliceai -A grch37 -D 50 -M 0 on canonical donor X:193062 G>A -> DS_DG 0.90, DS_DL 1.00; delta cut-offs 0.2/0.1 match Walker 2023'),
  ]),
 dict(index=7, type='Adversarial', label='rRNA contamination (samtools recipe, fastq_screen), 3-prime bias (geneBody_coverage, Picard) and strand-convention block on planted BAMs',
  status='COMPLETED', status_flag='\u26a0\ufe0f', executed=True,
  note='Picard strand mapping and 3-prime-bias direction verified; the samtools rRNA recipe reports 15.6% for a planted 22.2%, flipping the >20% verdict; fastq_screen needs an unlisted aligner',
  basic=27, specialized=37,
  assertions=[
   A('Picard STRAND_SPECIFICITY mapping in SKILL.md is right for dUTP', P, 'SECOND_READ_TRANSCRIPTION_STRAND: PCT_CORRECT_STRAND_READS 1.0; FIRST_READ: 0.0'),
   A('3-prime bias is flagged by the Skill\'s metrics', P, 'planted 3-prime library: MEDIAN_5PRIME_TO_3PRIME_BIAS 0.047 vs 1.009 uniform (<0.5 rule fires); geneBody 5p/3p 0.04 vs 1.02; note >2 is 5-prime bias, not degradation'),
   A('samtools view -c -L recipe reproduces the planted rRNA fraction (22.2%)', F, '8170/52282 = 15.6% (denominator includes 12282 secondary and 3244 unmapped records); Picard PCT_RIBOSOMAL_BASES 0.222 and primary-only recipe 4085/18378 = 22.2% are right; the Skill\'s >20% "failed" verdict is missed'),
   A('fastq_screen command works as written', F, 'literal command exits 255 (no Bowtie/Bowtie2/BWA; aligner not in the prerequisites); with minimap2 and a valid config it reports the planted 25.00% rRNA; a bad index path exits 0 with 100% unmapped'),
   A('rRNA threshold table is internally consistent', F, '<5% poly(A) is Healthy yet 1-3% poly(A) "suggests RNA degradation"; the closing note says >5%'),
  ]),
]

for i in inputs:
    i['total'] = i['basic'] + i['specialized']
    i['assertions_passed'] = sum(1 for a in i['assertions'] if a['result'] == 'PASS')
    i['assertions_total'] = len(i['assertions'])
    assert 3 <= i['assertions_total'] <= 5
avg = round(sum(i['total'] for i in inputs) / len(inputs), 1)
ap = sum(i['assertions_passed'] for i in inputs); at = sum(i['assertions_total'] for i in inputs)

static = {
 'functional_suitability': dict(score=8, max=12, note='Broad coverage of design, STAR 2-pass, saturation, novelty, overhang, MaxEnt, Picard, strandedness, annotation, rRNA. Core RSeQC/Picard/STAR statements verified, but the known-fraction snippet, the MaxEnt acceptor example, the rRNA recipe, the overhang helper and several documented error strings and defaults are wrong.'),
 'reliability': dict(score=5, max=12, note='Silent failures dominate: contig mismatch gives exit-0 zero curves, generate_qc_report crashes on a BAM with no spliced reads, RSeQC plotting needs an unlisted Rscript, and documented error messages are not the ones the tools print.'),
 'performance_context': dict(score=5, max=8, note='One 480-line SKILL.md with no references/ and a large duplicated threshold set; example script is small.'),
 'agent_usability': dict(score=11, max=16, note='Clear decision tables and layer taxonomy; inconsistent thresholds across three tables, BED12 preparation never explained, no format given for reading saturation numbers.'),
 'human_usability': dict(score=5, max=8, note='Natural triggers and a usage guide; little tolerance for naming/format variants (contig names, BED type) and no diagnosis path when tools return zeros.'),
 'security': dict(score=11, max=12, note='No secrets; subprocess called with argument lists, no shell or eval; maxentpy calls sys.exit on bad input and the helper does not validate paths.'),
 'maintainability': dict(score=8, max=12, note='Single example module with functions, but shipped helpers duplicate and diverge from the SKILL.md versions (=/X handling, min_overhang) and there are no tests or fixtures.'),
 'agent_specific': dict(score=15, max=20, note='Good biology-vs-artifact caveats and cross-links (all seven Related Skills exist); overlong description; no seed/idempotency notes for the shuffled saturation subsample; escape hatches are mostly to other Skills.'),
}
sub = sum(v['score'] for v in static.values())
sw = round(sub * 0.4, 1); dw = round(avg * 0.6, 1); final = round(sw + dw)

report = {
 'meta': dict(skill_name='bio-splicing-qc',
   description='Assesses RNA-seq data quality for alternative splicing analysis: design audit, STAR 2-pass, junction saturation, known/novel junction ratio, overhang, splice-site strength (MaxEntScan/SpliceAI), strandedness, 3-prime bias and rRNA screening.',
   evaluated_on='2026-09-20', evaluator_version='skill-auditor@1.0', category='Data Analysis', execution_mode='D', complexity='Complex', n_inputs=7,
   source='mrsonord2240/bioSkills@44ff43bb35e5741c3ddd3c003590e1f1da8a4a4b:alternative-splicing/splicing-qc',
   execution_note='All 7 inputs executed (7/7) in WSL science envs as-core, as-maxent, as-spliceai and af-picard3 (Picard 3.5.0) against synthetic planted BAMs (data/synthetic, labelled synthetic) and real GEUVADIS chrX data. Not executed: featureCounts -s 2 and Qualimap (not installed, not referenced by code), Picard was run from another audit\'s env read-only.'),
 'veto_gates': dict(
   skill_veto=dict(gate='PASS', stability='PASS', contract='PASS', determinism='PASS', security='PASS'),
   research_veto=dict(applicable=True, gate='FAIL',
     scientific_integrity=dict(result='PASS', detail='Citations are real (Veeneman 2016 checked); two mis-stated sources and some invented error strings, but no fabricated DOI/PMID, trial or p-value.'),
     practice_boundaries=dict(result='PASS', detail='Research-only QC; SpliceAI PP3/BP4 mention is a published cut-off, no individual diagnosis or prescription.'),
     methodological_ground=dict(result='PASS', detail='No principled fallacy; the rRNA samtools recipe and read-vs-junction known-fraction ambiguity are quality issues, recorded as P1.'),
     code_usability=dict(result='FAIL', detail='Input 1: the SKILL.md known/novel snippet prints 0.0%/0.0% on real RSeQC 5.0.5 output. RSeQC junction_annotation/saturation exit 1 without Rscript (verified with --rscript /nonexistent) and Rscript is not in the prerequisites, so the example (check=True) raises. Input 4: generate_qc_report raises EmptyDataError on a BAM without spliced reads; junction_stats/count_junction_reads give wrong overhang and coordinates.'))),
 'static_score': dict(subtotal=sub, max=100, categories=static),
 'dynamic_score': dict(execution_avg=avg, max=100, assertion_pass_rate=dict(passed=ap, total=at),
   inputs=[{k: v for k, v in i.items() if k != 'executed'} | {'executed': i['executed'], 'execution_note': i['note']} for i in inputs]),
 'final': dict(static_weighted=sw, dynamic_weighted=dw, score=final, max=100, grade='Reject', grade_symbol='\u274c', deployable=False, veto_override=True),
 'key_strengths': [
   'The RSeQC/Picard core is right: infer_experiment table, junction_saturation plateau rule and Picard strand mapping all reproduced planted truth (dUTP 1.00, plateau vs rising, PCT_CORRECT_STRAND 1.0).',
   'MaxEntScan cut-offs hold on 8.5k real chrX donors and acceptors (AUC 0.97/0.96), and the STAR 2-pass commands run unchanged on current STAR 2.7.11b.',
   'Good biology-vs-artifact framing for high novel-junction rates and layered QC taxonomy; all seven Related Skills exist.',
   'Shipped example file exists and the RSeQC classification it drives matches an independent count exactly.'],
 'recommendations': [
  dict(priority='P0', title='Known/novel snippet returns 0.0%; Rscript undocumented', observed_in=[1, 4],
       problem='RSeQC writes " annotated" with a leading space, so groupby(...).get("annotated") is 0 and the headline known/novel fraction prints 0.0%/0.0% on every library. junction_annotation.py and junction_saturation.py also exit 1 without Rscript (unlisted), and generate_qc_report crashes on a BAM without spliced reads.',
       root_cause='The snippet and example were never run against real RSeQC output; prerequisites omit R and STAR/samtools/picard.',
       fix='Strip the annotation column (junc["annotation"].str.strip()) and assert known+novel==1; pass --skip-plot or list R in prerequisites; guard empty junction output; add a test on a small BAM.'),
  dict(priority='P1', title='Overhang/coverage helpers give wrong numbers', observed_in=[4],
       problem='junction_stats sums all matched bases on each side, so multi-junction reads report overhang 30 where the adjacent exon is 4; count_junction_reads ignores min_overhang, ignores =/X ops, counts multi-mappers and both mates (>=10-read junctions 404 vs STAR 371).',
       root_cause='Hand-written CIGAR loops with no assertion against a known CIGAR or STAR SJ.out.tab.',
       fix='Compute overhang from the adjacent M/=/X block only, filter NH==1 and count per fragment (or read SJ.out.tab/regtools), honour min_overhang, and test on CIGARs such as 30M1000N4M800N66M.'),
  dict(priority='P1', title='rRNA samtools recipe flips the pass/fail verdict', observed_in=[7],
       problem='samtools view -c -L / samtools view -c reported 15.6% for a planted 22.2% because the denominator includes secondary and unmapped records; the >20% failed-depletion rule is then missed. fastq_screen needs an unlisted aligner and exits 255 or 0-with-100%-unmapped on misconfiguration.',
       root_cause='Recipe counts records, not primary mapped fragments; aligner prerequisites not stated.',
       fix='Use -F 0x904 (and -f 0x40 or PCT_RIBOSOMAL_BASES from Picard, which returned 0.222) and state the fastq_screen aligner/index setup and how to read the *_screen.txt.'),
  dict(priority='P1', title='Splice-site example and helper are wrong', observed_in=[6],
       problem="The SKILL.md/example acceptor 'T'*20+'CAG' scores -7.20 (no AG); score_splice_sites drops wrong-length inputs and returns None for N so outputs no longer align with inputs; maxentpy exits the process on a wrong length and raises KeyError for N/U, not ValueError.",
       root_cause='Example never scored; documented failure behaviour guessed.',
       fix="Use a real acceptor (e.g. TTTTTTTTTTTTTTCCTTAGGAG, 11.58), return one score per input (NaN for invalid) and catch SystemExit/KeyError; correct the failure-mode text."),
  dict(priority='P1', title='Documented failure modes and defaults are inaccurate', observed_in=[2, 3, 5],
       problem='infer_experiment "0 of 200000 reads" is really contig-name/BED mismatch ("Total 0 usable reads", exit 0) and -q 30 is already the default; STAR error "too many SJs in cohort merge" does not exist (real: limitSjdbInsertNsj); alignIntronMax default is ~590 kb, not 1 Mb; alignSJoverhangMin 8 lowers microexon sensitivity; a flat deep-BAM saturation curve is saturation, not uninformative; junction_saturation on a contig mismatch returns all zeros with exit 0.',
       root_cause='Failure-mode text written without running the tools.',
       fix='Replace with observed messages, add a chr-naming and BED12 check (junction_* need BED12; infer_experiment accepts BED6), and state RSeQC "annotated" means both sites known (skipping junctions count).'),
  dict(priority='P2', title='Merge filter, thresholds and citations need cleanup', observed_in=[1, 5, 7],
       problem="awk '$5>0' filters on intron motif not strand, the merged 'novel' file is 99.7% annotated with 3533 duplicate lines, pass-2 SJ.out.tab flags inserted junctions as annotated; 30-50M reads, 75-100 nt, rRNA 1-3% vs <5% and 'PE 50nt single-end' are inconsistent; Veeneman 94% is share of junctions improved, per-sample; read-weighted vs junction-level known% both exist; STAR BAMs need samtools index before the pysam helpers; --outSAMstrandField only in a comment.",
       root_cause='Numbers and conventions copied across tables without reconciliation.',
       fix='Filter on $6==0 and cut -f1-4 | sort -u, add --outSAMstrandField intronMotif where XS is needed, unify thresholds in one table with gap ranges, state which known-fraction definition applies, and add samtools index to the STAR steps.'),
  dict(priority='P2', title='Saturation numbers are unseeded and hard to read', observed_in=[2],
       problem='RSeQC shuffles splice events without a seed (known curve moved by up to 16 junctions from expectation) and writes the numbers only inside the .r file; the Skill gives no parsing recipe.',
       root_cause='Plateau rule specified without an input format.',
       fix='Show a 10-line parser for x/y/z/w vectors and say the curve is stochastic; use -l/-u/-s for finer 80-100% steps.'),
 ]}
json.dump(report, open(f'{OUT}/eval_report_bio-splicing-qc_result.json', 'w', encoding='utf-8'), indent=2, ensure_ascii=False)
print('static', sub, 'avg', avg, 'final', final, 'assertions', ap, '/', at)

# ---------------- viewer
md = ['# Eval Viewer \u2014 bio-splicing-qc', 'Generated: 2026-09-20', '',
      'Source: `mrsonord2240/bioSkills@44ff43bb35e5741c3ddd3c003590e1f1da8a4a4b:alternative-splicing/splicing-qc` (first audit). Category: Data Analysis, mode D (SKILL.md + shipped example), Complex -> 7 inputs, 7/7 executed.', '',
      'Synthetic data (auditor-made, planted truth) is in `run/data/synthetic/` (`make_synth.py`); real data is the GEUVADIS chrX set in `audit-envs/alternative-splicing/public-data`.', '',
      '## Summary Table', '', '| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |', '|---|---|---|---|---|---|---|']
for i in inputs:
    md.append(f"| {i['index']} | {i['type']} | {i['basic']} | {i['specialized']} | {i['total']} | {i['assertions_passed']}/{i['assertions_total']} PASS | {i['status_flag']} |")
md += ['', f'**Execution Average: {avg} / 100**  |  **Assertion Pass Rate: {ap}/{at}**  |  Static {sub}/100  |  **Final {final} (Reject: Research Veto M4 FAIL, veto_override)**', '',
       'Without the veto the numeric score would be Beta Only (60-74) and below the Limited Release floors (execution avg < 75, static < 70), so the Skill would still be non-deployable.', '',
       '## Skill Veto: PASS (stability, contract, determinism, security).  Research Veto: M1 PASS, M2 PASS, M3 PASS, M4 FAIL', '',
       '## Detailed Outputs', '']
prompts = {1: 'Classify my junctions as known vs novel and flag samples with a low known-junction fraction (two SE 100-nt libraries; planted 93% and 22% known reads).',
 2: 'Compute junction saturation and tell me whether depth is sufficient (deep / mid / shallow planted libraries, real chrX, BED with mismatched contig names).',
 3: 'Verify library strandedness before I set rMATS --libType (planted dUTP, forward, unstranded, 20% and 40% leakage; real chrX; wrong BED; MAPQ 1 BAM).',
 4: 'Give me per-junction read counts and the overhang distribution; how many junctions have >=10 reads and overhang >=8? (planted CIGARs, multi-mappers, real chrX vs STAR/regtools).',
 5: 'Configure cohort-style STAR 2-pass for my samples (4 real chrX pairs), and check the flags and the merge filter.',
 6: 'Score the donor/acceptor sites with MaxEntScan and SpliceAI and flag weak or cryptic ones (8.5k real annotated chrX sites vs decoys).',
 7: 'Is my library rRNA-contaminated or 3-prime biased, and what do I pass to Picard/rMATS for strand? (planted 22% rRNA, 85% 3-prime library).'}
scripts = {1: 'run/input1_junction_annotation.py', 2: 'run/input2_junction_saturation.py', 3: 'run/input3_strandedness.py', 4: 'run/input4_junction_coverage_overhang.py',
 5: 'run/input5_star_2pass.sh + run/input5_analyze.py', 6: 'run/input6_splice_site_strength.py + run/input6b_spliceai_rscript.sh', 7: 'run/input7_contam_bias.sh, input7b_fastqscreen.sh, input7_parse.py'}
keyout = {
1: '''```
clean:     RSeQC junctions 719 (known 249 / partial 305 / complete 165); reads 12410 (11592 / 553 / 265)
           pysam count identical; planted known-read fraction 0.9341
SKILL.md snippet -> "known: 0.0%, novel: 0.0%"   annotation values: [' annotated', ' complete_novel', ' partial_novel']
after .str.strip(): known 93.4%, novel 6.6%   (strictly annotated junctions only: 86.7%; junction-level known 34.6%)
novelrich: known 22.3% reads (planted 0.2235), junction-level 13.0%
```''',
2: '''```
sat_deep    known 154,180,180,... growth 80->100 = 0.0%    PLATEAU   (expected 0.0%)
sat_mid     known 22,46,73,...,176,180 growth 8.4%          STILL RISING (expected 5.6%)
sat_shallow known 20,36,59,...,175,180 growth 13.2%        STILL RISING (expected 13.6%)
pysam distinct junctions 919/1022/951 == RSeQC all@100%
real chrX ERR188383 known 588 -> 2698 growth 6.7% STILL RISING
contig mismatch: rc=0, known [0,0,0..] all [0,0,0..]; plateau rule -> 0/0
```''',
3: '''```
dutp        {'1++,1--,2+-,2-+': 0.0,    '1+-,1-+,2++,2--': 1.0}     -> fr-firststrand
fwd         {1.0, 0.0}                                                -> fr-secondstrand
unstr       {0.5011, 0.4989}; dutp_leak20 {0.2024, 0.7975}; leak40 {0.4087, 0.5914}
real chrX   {0.4643, 0.4525}, failed to determine 0.0831           -> unstranded
contig mismatch / GTF as BED: rc=0 "Total 0 usable reads were sampled", "Unknown data type: Mixture"
MAPQ-1 BAM: default (-q 30) "Unknown data type: Mixture"; -q 0 -> 1.0
```''',
4: '''```
junction_stats (SKILL.md) on planted CIGARs: 100030-101030 overhang 30 (true 4); 101034-101834 34 (4); 105020-105720 20 (10); 105730-106630 30 (10); 6 -> 6 OK; 50 -> 50 OK
count_junction_reads(min_overhang=8) == (min_overhang=99): identical, 72 reads / 6 junctions
=/X CIGAR read: example (200000,201000) vs SKILL.md function (200050,201050) [true]
NH=4/MAPQ 3 contamination: Skill 12410 reads / 719 junctions vs unique-only 9308 / 648
real chrX ERR188383: read-level 25580 reads vs fragment-level 24091; 665 of 2915 junction counts differ; >=10 reads 420 vs 385; regtools 423
STAR pass-2 BAM: Skill == STAR unique on 2163/2792 junctions; fragment-level == STAR on 2792/2792
generate_qc_report on real BAM: "POOR (<30% junctions have >=10 reads)" 14.4%
```''',
5: '''```
pass1 unique mapping 97.20/96.86/97.17/96.54%  ->  pass2 97.63/97.24/97.53/96.95%; ReadsPerGene 2396 rows
cohort_novel_SJ.tab: 5717 lines, 2184 distinct junctions, 2178 already in GTF (6 novel); 3533 duplicate lines
col5 = intron motif (1-6), col4 = strand (1,2); non-canonical rows 13 (all annotated, strand 0)
XS tags in pass-2 BAM: 0 of 20000 spliced reads
--limitSjdbInsertNsj 10 -> "Fatal LIMIT error ... =10552 ... SOLUTION: re-run with at least --limitSjdbInsertNsj 10552"
sjdbOverhang mismatch -> "present --sjdbOverhang=74 is not equal to the value at the genome generation step =100"
samtools view -c -F 0x100 -F 0x800 == -F 0x100 == -F 0x900 (98732): repeated -F accumulates, Skill row OK
```''',
6: '''```
annotated GT donors n=8549: >8 60.7%, 5-8 27.6%, <5 11.6%, median 8.60;  AG acceptors n=8507: >8 57.9%, <5 13.5%
decoy GT donors n=88: 95.5% <5;  AUC donor 0.969, acceptor 0.958
score5('CAGGTAAGT') = 10.86;  score3('T'*20+'CAG') = -7.20 (SKILL.md example)
wrong length -> SystemExit "Wrong length of fa!"; N/X/U -> KeyError; lower-case ok
score_splice_sites(4 donors incl. 8-mer, lower-case, N) -> [10.86, 10.86, None]
spliceai -A grch37 -D 50 -M 0: SpliceAI=A|PLCXD1|0.00|0.00|0.90|1.00|28|-10|28|-1
```''',
7: '''```
samtools view -c -L rRNA.bed / samtools view -c = 8170 / 52282 = 15.6%   (truth 22.2% of primary mapped fragments)
primary only: 4085 / 18378 = 22.2%   Picard PCT_RIBOSOMAL_BASES 0.222
Picard dUTP: SECOND_READ PCT_CORRECT_STRAND 1.0 ; FIRST_READ 0.0
3-prime library: MEDIAN_5PRIME_TO_3PRIME_BIAS 0.047 (uniform 1.009); geneBody 5p/3p 0.04 vs 1.02
fastq_screen literal: rc=255 (no aligner); --aligner minimap2 + valid config: rRNA 25.00% (truth 25%)
rmats.py --libType {fr-unstranded,fr-firststrand,fr-secondstrand} exists
```'''}
for i in inputs:
    n = i['index']
    md += [f"### Input {n} \u2014 {i['type']}: {i['label']}", f"**Prompt:** {prompts[n]}", f"**Executed:** true. Scripts: `{scripts[n]}`", '**Output (trimmed):**', keyout[n],
           f"**Scores:** Basic: {i['basic']}/40 | Specialized: {i['specialized']}/60 | Total: {i['total']}/100", '**Assertions:**']
    md += [f"- [{a['result']}] {a['text']} \u2014 {a['note']}" for a in i['assertions']] + ['']
md += ['## Static score (25 criteria)', ''] + [f"- {k}: {v['score']}/{v['max']} \u2014 {v['note']}" for k, v in static.items()] + [f'', f'**Static subtotal {sub}/100**', '',
       '## Recommendations', ''] + [f"- **[{r['priority']}] {r['title']}** (inputs {r['observed_in']}): {r['problem']} Fix: {r['fix']}" for r in report['recommendations']]
open(f'{OUT}/eval_viewer_bio-splicing-qc.md', 'w', encoding='utf-8').write('\n'.join(md) + '\n')
