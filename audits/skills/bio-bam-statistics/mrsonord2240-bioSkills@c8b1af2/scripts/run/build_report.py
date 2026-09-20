#!/usr/bin/env python3
"""Builds eval_report_bio-bam-statistics_result.json and eval_viewer_bio-bam-statistics.md from the scores below and excerpts of out/*.txt (the recorded outputs).
Run from anywhere: python build_report.py"""
import json, os, re
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
def ex(name, pat=None, n=14, width=200, start=0):
    lines = open(os.path.join(HERE, 'out', name), encoding='utf-8', errors='replace').read().split('\n')
    if pat: lines = [l for l in lines if re.search(pat, l)]
    return '\n'.join(l[:width] for l in lines[start:start + n])

SRC = 'mrsonord2240/bioSkills@c8b1af2148fd4b8e6c667f4feb080cee03cd3551:alignment-files/bam-statistics'
meta = {
    'skill_name': 'bio-bam-statistics',
    'description': 'Generate alignment statistics using samtools flagstat, stats, depth, coverage, and mosdepth. Use when assessing alignment quality, calculating coverage, or generating QC reports.',
    'source': SRC, 'evaluated_on': '2026-09-20', 'evaluator_version': 'skill-auditor@1.0',
    'category': 'Data Analysis', 'execution_mode': 'D', 'complexity': 'Complex', 'n_inputs': 7,
    'audit_type': 'second re-audit of a fixed Skill (fix/af-bamstat round 2, commit c8b1af2 on top of 377e368); previous report: 84 Limited Release, deployable, one P1, five P2 (archived at audits/_pre-fix-20260920b/bio-bam-statistics/)',
    'pre_fix_score': 84,
    'regression_inputs': 'Inputs 1-7 re-run every pre-fix input (the previous auditor generators, truth helpers and check scripts, updated for the new block numbers and signatures).',
    'new_inputs': 'NEW, different from the previous auditors: own_ctg.bam/.cram (3 contigs incl. a read-less 5 kb contig and a 100 bp contig, 7 QC-fail, 5 dup, 3 secondary, 4 supplementary, 6 unmapped, truth by construction) as BAM, CRAM+reference, CRAM embedded reference, unindexed CRAM, CRAM with dead @SQ UR, CRAM vs WRONG reference; own_insert.bam (template lengths across the 8000 boundary); own_del.bam (D, N and overlapping mates planted); truncated / text-named / zero-byte BAM; region_depth_stats on the REAL 1000G chr20 slice and REAL spliced RNA BAM; bcftools INFO/DP vs FORMAT/DP; mosdepth --fast-mode on real ARTIC and RNA BAMs.',
    'executed': '7/7 inputs executed (input 6 partly: VerifyBamID2 was run end to end on a synthetic BAM and stops with "Insufficient Available markers", so no FREEMIX exists; somalier needs a whole-GRCh38 FASTA that is not on this machine; the assay-threshold table is not executable)',
    'tools': 'samtools 1.24, pysam 0.24.1, mosdepth 0.3.14, bcftools 1.24, Picard 3.5.0, MultiQC 1.35, plot-bamstats, VerifyBamID2 2.0.3, somalier 0.3.5 (WSL science, env alignment-files); run from a copy of the Skill in run/skill (byte-identical to the worktree HEAD, checked with git show), worktree untouched',
}
veto = {
    'skill_veto': {'gate': 'PASS', 'stability': 'PASS', 'contract': 'PASS', 'determinism': 'PASS', 'security': 'PASS'},
    'research_veto': {
        'applicable': True, 'gate': 'PASS',
        'scientific_integrity': {'result': 'PASS', 'detail': 'No fabricated identifiers, results or sample sizes. Every numeric claim I could run reproduced (depth caps, overlap table, 16.77x / 8.86x, 2810 vs 3110 rows, mosdepth 19000 of 22000 bp, INFO/DP 16.77x). The assay-threshold table and the FREEMIX 1% / 5% cut-offs remain unsourced but are labelled "literature ranges, not verified" and "commonly cited".'},
        'practice_boundaries': {'result': 'PASS', 'detail': 'QC statistics only; no diagnosis or prescription.'},
        'methodological_ground': {'result': 'PASS', 'detail': 'Denominators, mate-overlap double counting, depth caps, secondary/supplementary/QC-fail handling are stated and were confirmed against truth by construction and against alignment blocks; no principled fallacy found.'},
        'code_usability': {'result': 'PASS', 'detail': 'All 31 executable fenced blocks parse (27 bash -n, 4 py_compile) and every one that matters ran on real or planted data with asserted output; examples/qc_report.py equals samtools flagstat on 30+ BAMs/CRAMs, exits 1 with a message on missing, truncated, text, zero-byte and reference-less CRAM input.'}}}
static = {
    'functional_suitability': (11, 12, 'Completeness 4 (flagstat/idxstats/stats/depth/coverage/mosdepth/pysam, uBAM and CRAM handling, assay table), Correctness 3 (every runnable claim held; two small imprecisions, see P2), Appropriateness 4.'),
    'reliability': (10, 12, 'Fault tolerance 4: empty, SE, unindexed, uBAM, CRAM with and without reference, truncated, text and zero-byte inputs all end in a correct result or exit 1 with a message. Error reporting 3: wrong-reference CRAM says only "truncated file"; bare snippets still raise raw pysam errors. Recoverability 3.'),
    'performance_context': (6, 8, '497-line SKILL.md with everything in one file and no references/ folder; duplication removed in round 2 (Quick Reference, Output to File). Token cost 3, efficiency 3.'),
    'agent_usability': (14, 16, 'Learnability 4, Consistency 3, Feedback design 3 (outputs shown, exit-1 messages specified), Error prevention 4 (denominator, cap, overlap, flagstat units, contig-name traps named with the safe command).'),
    'human_usability': (6, 8, 'Discoverability 3 (generic description), Forgiveness 3.'),
    'security': (11, 12, 'No credentials; paths quoted; no eval/exec/subprocess in shipped code (grep clean). Input validation 3: user paths pass straight to samtools/pysam.'),
    'maintainability': (9, 12, 'Modularity 3, Modifiability 3 (recipes now live once), Testability 3: checked-on notes and one runnable example, but no shipped test data or expected outputs.'),
    'agent_specific': (18, 20, 'Trigger 3, Progressive disclosure 3 (497 lines, no references/), Composability 4, Idempotency 4, Escape hatches 4 (What Flagstat Does Not Reveal, exit-1 guards, honest "not run end to end").')}
A = lambda t, r, n: {'text': t, 'result': r, 'note': n}
inputs = [
 dict(index=1, type='Canonical', label='Get alignment statistics and coverage from my BAM: REAL human chr22-slice PE BAM and REAL 1000G chr20 BAM, plus region depth on the real 1000G and RNA BAMs',
      prompt='Get alignment statistics and coverage from my BAM file (human PE slice, and a 1000 Genomes slice with 101 duplicate-flagged reads). Give me mapping rate, per-contig counts, insert size, mean depth and the fraction at 10x and 20x. Then give me mean depth and >=20x for a region of my 1000G slice and of my spliced RNA-seq BAM.',
      status='COMPLETED', basic=38, specialized=56,
      note='[t0, t1_canonical.sh, t1b_depth_real.sh, n5_real_region.sh, n9_file_blocks.sh] flagstat, idxstats, stats fields, coverage and the summary-table row equal record-flag truth on both real BAMs (5644/5642/5640/5638; 1000G 9601/9595/9557/9450/101 dup). Block 017 (-aa) prints 16.77x / 2.43% / 2.34% = alignment-block truth (16.7743/2.4299/2.3424); the old 568x average still reproduces only as the documented warning. region_depth_stats equals block-truth and samtools depth -a on 9 real windows of the 1000G slice (dup-flagged reads excluded) and the spliced RNA BAM (N-skips excluded). Determinism: 10 identical reruns of qc_report.py, the -aa recipe, flagstat and region_depth_stats.',
      assertions=[A('Block 017 (-aa recipe) prints the block-truth mean and >=10x/>=20x on the real human BAM (16.77x / 2.43% / 2.34%)', 'PASS', 'Equal to alignment-block truth 16.7743 / 2.4299 / 2.3424.'),
                  A('flagstat, idxstats, stats and the block-005 summary row equal record-flag hand counts on both real BAMs', 'PASS', 'All 8 fields per BAM equal; 1000G reports 101 duplicates as truth.'),
                  A('region_depth_stats equals alignment-block truth and samtools depth -a on real spliced RNA and real 1000G windows (mean, covered, max, >=10x, >=20x)', 'PASS', '9 windows, 0 mismatches, incl. 1-bp, zero-depth and past-the-data windows; N-skips and duplicate-flagged reads handled.'),
                  A('The 568x raw-average trap is reproduced and the Skill warns about it', 'PASS', 'raw depth avg 568.153 vs true 16.77.'),
                  A('Identical inputs give identical outputs across 10 runs', 'PASS', 'md5 of 10 qc_report.py outputs: 1 distinct.')]),
 dict(index=2, type='Variant A', label='What fraction is covered at 10x/20x when some contigs have no reads: previous auditor planted-depth BAM (regression) + my own_ctg.bam (NEW)',
      prompt='My reference has a 5 kb contig with no reads and a 100 bp contig with 50x. What is the mean depth and the % of the genome at >=10x and >=20x, what does mosdepth report, and give me the depth for a target list that includes the empty contig.',
      status='COMPLETED', basic=37, specialized=55,
      note='[t2_planted.sh, n2_own_ctg.sh, n2_region_truth.py] Truth by construction. planted-depth (22000 bp, 4 contigs, chrC read-less): recipe prints 2.57x / 9.32% / 5.68% exactly; -a prints 2.97x as the Skill says. Block 021 (depth -aa -b) now gives 3110 rows (was 2810) and -a still 2810 as the Skill states. own_ctg (25100 bp, ctgB read-less): -aa recipe 4.79x / 42.23% / 2.39% = truth 4.788845 / 42.2311 / 2.3904; -a gives 5.98x; mosdepth summary total covers 20100 of 25100 bp and 5.98x, exactly the note in SKILL.md; -aa -b keeps ctgB (800 rows) and -a drops it; coverage-from-BED loop, mosdepth --by and region_depth_stats (22 windows, BAM and CRAM+reference) equal truth.',
      assertions=[A('Block 017 (-aa) prints the truth mean and breadth on both planted BAMs (2.57x/9.32%/5.68%; 4.79x/42.23%/2.39%)', 'PASS', 'Exact to the printed digits.'),
                  A('Skill claim: depth -a -b drops regions on read-less contigs, -aa keeps them (2810 vs 3110 rows; ctgB 0 vs 800)', 'PASS', 'Reproduced on both BAMs; block 021 verbatim prints 3110.'),
                  A('Skill claim: mosdepth summary total covers only contigs with reads (19000 of 22000 bp, 2.95x vs 2.57x)', 'PASS', 'Also 20100 of 25100 bp, 5.98x vs 4.79x on own_ctg.'),
                  A('region_depth_stats equals truth by construction on read-less, 1-bp, contig-end and supplementary windows, on BAM and CRAM with reference=', 'PASS', '35 windows, 0 mismatches; supplementary reads count, dup/QC-fail/secondary do not, like samtools depth.'),
                  A('coverage-from-BED loop and mosdepth --by agree with truth incl. the read-less contig and a track header line', 'PASS', 'ctgB rows 0.00; header line skipped, no "Failed to parse region".')]),
 dict(index=3, type='Edge', label='Planted flag categories (secondary, supplementary, QC-fail, duplicate, unmapped, singleton) on 21 BAMs incl. an unaligned BAM + my own planted counts + insert-size boundary',
      prompt='Run a QC report on this BAM: it has secondary and supplementary alignments, QC-failed reads, duplicates and unmapped reads, and one of my files is an unaligned BAM with no @SQ lines. Are the counts the same as flagstat? Also what insert size does the report give for my mate-pair-like library with templates up to 8500 bp?',
      status='COMPLETED', basic=37, specialized=54,
      note='[t3_edge.sh, n8_own_counts.sh, n3_cram_bad_insert.sh (b), n3b_cram_isolated.sh] qc_report.py and the Count Reads snippet equal flagstat -O tsv (QC-passed column and percentages) and record-flag hand counts on 21/21 BAMs including the unaligned BAM (previously a ValueError traceback) and empty/all-QC-fail (message, no ZeroDivisionError); my own_ctg planted counts (1105 records, 3 secondary, 4 supplementary, 7 QC-fail, 5 dup, 1085 mapped passed primary) equal qc_report, flagstat and the plant. The cross-check identity now holds (540-10-10=520=raw total sequences). Insert boundary: qc_report keeps 0<tlen<8000 (mean 2286, matches truth), but samtools stats -i 8000 CLAMPS longer templates to 8000 instead of dropping them (stats mean 3555.5; predicted clamp 3555.5, verified with -i 7000 and -i 400), so the "MAX_INSERT = the samtools stats default" wording hides that the two means differ.',
      assertions=[A('qc_report.py and Count Reads equal flagstat and hand counts on all planted-flag BAMs, incl. uBAM, empty and all-QC-fail', 'PASS', '0 mismatches on 21 BAMs.'),
                  A('Counts equal the counts planted by construction (own_ctg: 1105/3/4/7/5/1085; edge expected.json 9 BAMs)', 'PASS', 'PLANTED_TRUTH_MISMATCHES 0, EXPECTED_JSON_MISMATCHES 0.'),
                  A('Cross-check identity flagstat_total(pass+fail) - secondary - supplementary = stats raw total sequences holds', 'PASS', '540-10-10 = 520 = 520; negative control (pass column only) differs, as the Skill now states.'),
                  A('Unaligned BAM with no @SQ gives correct counts, not a traceback', 'PASS', '30 primary, 0 mapped, rc 0 (round-2 fix confirmed).'),
                  A('MAX_INSERT wording (samtools stats default) predicts what stats does with templates above the cap', 'FAIL', 'qc_report drops them (mean 2286); samtools stats clamps them to 8000 (mean 3555.5), so the two reports disagree on such libraries.')]),
 dict(index=4, type='Variant B', label='Depth caps and mate-overlap: 9500x stack, real ARTIC BAM, my own_del.bam (deletions, spliced reads, overlapping mates), disputed claims',
      prompt='My amplicon and RNA data have deep stacks, spliced reads and overlapping mates. Which tools cap depth, which count overlapping mates twice, does mosdepth count deletions and splice gaps, and does bcftools mpileup INFO/DP change with -x?',
      status='COMPLETED', basic=37, specialized=54,
      note='[t4_depth_cap.sh, n4_disputed_claims.sh, n4_overlap_del.py, t1b_depth_real.sh] Every default in the cap table reproduced on a 9500x stack (depth uncapped, -d ignored; coverage -d 1000000; mosdepth uncapped; mpileup 8000; bcftools 250; pysam 8000). ARTIC real BAM: recipe, coverage and pysam helper 68.8373x = truth. Overlap table on the real human BAM: depth/coverage/pysam/fast-mode 16.77, depth -s and mosdepth 8.86, mpileup 8.85 / -x 16.75 / -Q 0 16.77, bcftools FORMAT/DP 8.85 default and 16.77 with -x or -Q 0. The two claims the earlier re-audit got wrong were verified independently: (1) mosdepth default does NOT count D (68.84 = depth -aa, own_del sum 4700 = mates once, D/N uncovered) while --fast-mode counts D (69.97 = depth -J; own_del 9600); (2) bcftools INFO/DP is 16.77x with or without -x on the real BAM and 5200 = mates-twice truth in every own_del variant. New: --fast-mode also counts spliced N bases as covered (real RNA BAM mosdepth 17.67x default vs 49.40x fast-mode vs 23.67x depth -aa; own_del D+N truth 9600) and samtools mpileup depth counts D and N too (own_del -Q 0: 9600 vs depth 5200); the Skill names only D.',
      assertions=[A('Every default in the depth-cap table reproduces on a 9500x stack and the pysam helper returns mean 1000.0 / max 9500', 'PASS', 'All 7 tools; helper equals truth.'),
                  A('Overlap table row values reproduce on the real human BAM (16.77 / 8.86 / 8.85 / 16.75 / 16.77, bcftools 8.85 / 16.77)', 'PASS', 'Each to 2 decimals; -x/--ignore-overlaps-removal flag names exist in --help.'),
                  A('Claim: mosdepth counts deletions as covered only with --fast-mode (default 68.84 = depth -aa)', 'PASS', 'ARTIC 68.84 vs 69.97; own_del default 4700 vs fast 9600. The earlier re-audit sentence was wrong.'),
                  A('Claim: bcftools INFO/DP is 16.77x with or without -x', 'PASS', 'Human BAM 16.77 for default, -x, -Q 0, -B; own_del INFO/DP sum 5200 in all variants.'),
                  A('The --fast-mode caveat is complete for spliced (RNA) data', 'FAIL', 'Fast-mode also counts N skips (RNA 49.40x vs 17.67x default); the Skill mentions only deletions.')]),
 dict(index=5, type='Stress', label='Summary table for 15 BAMs, plot-bamstats, MultiQC, stats GC-depth, mosdepth command block and quantize, CRAM in mosdepth',
      prompt='Create a summary table of statistics for all my samples (15 BAMs of every kind, one file name has a space), make the QC plots and a MultiQC report, and run the mosdepth exome, quantize and CRAM commands.',
      status='COMPLETED', basic=36, specialized=53,
      note='[t5_batch_plots.sh, n6_misc_claims.sh, n9_file_blocks.sh] Block 005 verbatim ran on 15 BAMs (real, synthetic, empty, uBAM, QC-fail-heavy, unmapped-only); all 15 rows equal record-flag hand counts, incl. 101 duplicates on 1000G and 220 QC-failed; the space-in-file-name run (t7) also works; own_ctg row 1105/7/1098/1092/0/5. plot-bamstats wrote 11 PNGs; MultiQC 1.35 found the stats, flagstat and idxstats reports and built a 2.2 MB report. Region stats raw total 1760 = samtools view -c -F 2304; depth files 1181 / 40001 / 40001 rows. mosdepth exome thresholds row and --quantize bands equal the block truth (0:1 38820 bp, 1:10 239, 10:100 298, 100:inf 644); mosdepth -f on a CRAM works with .crai and errors "must be indexed" without it. The stats -r GC-depth wording matches --help; GCD row counts are identical with and without -r at the same bin size (not falsified, not confirmed).',
      assertions=[A('Batch loop rows equal hand counts on 15 BAMs (incl. empty, uBAM, QC-fail, dup)', 'PASS', 'BATCH_FAILS 0.'),
                  A('plot-bamstats produces the plots and MultiQC builds a report from the text outputs', 'PASS', '11 PNGs; report 2272085 bytes with samtools stats, flagstat and idxstats sections.'),
                  A('mosdepth exome/quantize/CRAM commands run and their output equals truth', 'PASS', 'Quantized band lengths sum to 40001; CRAM total 20100 bp / 5.98x on own_ctg.'),
                  A('Blocks that only write files produce the right content (stats region, depth, depth -a, depth -aa)', 'PASS', '1760 = 1760; 1181, 40001, 40001 rows.')]),
 dict(index=6, type='Scope Boundary', label='Mate-pair insert size, adapter read-through soft-clipping, Picard HsMetrics, VerifyBamID2/somalier hand-offs, assay thresholds and unverified-number labelling',
      prompt='Is my library adapter-contaminated? Give me the soft-clipped fraction, off-target rate for my capture panel, whether the sample is contaminated (FREEMIX) or swapped, and whether my numbers are normal for ATAC/WES/RNA-seq.',
      status='COMPLETED', basic=35, specialized=50,
      note='[t6_scope.sh, t6b_qc_insert_cap.sh, t10_vb2.sh, t11_basesmapped.sh, t8_misc_claims.sh] The soft-clip awk recipe equals a CIGAR walk with pysam on 11 BAMs under gawk and mawk, and stats bases mapped minus bases mapped (cigar) equals the soft-clipped bases on the two real BAMs (863; 59137); the old grep still returns nothing. RF library: stats reports IS with outward pairs dominating, proper flag set or unset; qc_report.py reports 2000 with the flag set (MAX_INSERT 8000) and prints no insert line when it is unset, as the Skill says. Picard BedToIntervalList and CollectHsMetrics run (PCT_OFF_BAIT 0, MEAN_TARGET_COVERAGE 131.06). VerifyBamID2 end to end on a synthetic chr20 BAM reads the 10k panel, sees 204 markers and stops with "Insufficient Available markers" (no FREEMIX produced); somalier extract fails without a whole-GRCh38 FASTA; the Skill labels both "not run end to end here". The assay table and FREEMIX cut-offs have no source.',
      assertions=[A('Soft-clip recipe equals a CIGAR walk on real, synthetic and hand-built CIGARs and exits 1 with a message on empty output', 'PASS', 'SOFTCLIP_MISMATCHES 0 over 11 BAMs x 2 awks.'),
                  A('Picard CollectHsMetrics/BedToIntervalList commands run and give plausible values', 'PASS', 'PCT_SELECTED_BASES 1, PCT_OFF_BAIT 0, mean target coverage 131.06 vs depth -s 132.94 / depth 251.68 (mates-once vs twice).'),
                  A('Mate-pair (RF) claims: stats reports IS with outward pairs, pysam tools skip when the proper flag is unset', 'PASS', 'mean 2000.0, outward 100, flag set and unset; qc_report 0.00% proper, no insert lines.'),
                  A('Contamination hand-offs are labelled as not run end to end and the flags exist', 'PASS', 'verifybamid2 flags in --help, .dat prefix requirement reproduced, VB2 end-to-end gave no FREEMIX, somalier needs GRCh38: the label is accurate.'),
                  A('Assay-threshold values and the FREEMIX 1% / 5% cut-offs are backed by a source or by a run', 'FAIL', 'Labelled "literature ranges, not verified" / "commonly cited"; no citation, nothing runnable here.')]),
 dict(index=7, type='Adversarial', label='Empty, SE, unindexed BAM, Ensembl MT contig, space in name, unaligned BAM, CRAM (reference, embedded, no reference, dead UR, WRONG reference), truncated / text / zero-byte files',
      prompt='Run the QC report on whatever I have: an empty BAM, a single-end BAM, a BAM without an index, a BAM where the mitochondrion is called MT, an unaligned BAM, several CRAMs (some without their reference, one against the wrong FASTA) and three broken files.',
      status='COMPLETED', basic=37, specialized=53,
      note='[t7_adversarial.sh, n3_cram_bad_insert.sh, n3b_cram_isolated.sh, n3c_cram_no_ur.sh, n7_errmsgs.sh, t8_misc_claims.sh, t9_syntax_sweep.sh] Empty/SE/MT/unindexed give correct results or an exit-1 message (mito 7.62% on chrM and on MT; "no mapped reads" on a zero-read MT). uBAM: qc_report and Count Reads equal flagstat. CRAM with reference (own and real human): qc_report equals flagstat; CRAM whose @SQ UR is dead and no reference: exit 1 with "CRAM cannot be decoded without its reference: pass the FASTA as 2nd argument"; Count Reads on it raises the OSError the Skill documents and works with reference_filename=; embedded-reference and unindexed CRAM decode with no reference; unindexed CRAM: region_depth_stats -> "no index available for pileup", as documented. Truncated, text-named and zero-byte files: qc_report exits 1 with a one-line message (samtools quickcheck agrees). Wrong-reference CRAM: exit 1 but the message says only "truncated file" (htslib lines above it say MD5 mismatch). Every recipe on a zero-length or unknown-contig region gives a clear ValueError. All 31 executable blocks parse.',
      assertions=[A('Unaligned BAM (no @SQ) through qc_report.py and Count Reads equals flagstat', 'PASS', '30 records, 0 mapped; the ValueError of the earlier audit is gone.'),
                  A('CRAM with reference equals flagstat; CRAM without a reachable reference exits 1 with a message naming the reference', 'PASS', 'own_ctg_nourl.cram and real human CRAM: rc 1 plus the hint; with the FASTA rc 0 and equal counts.'),
                  A('Truncated, text-named and zero-byte BAMs exit 1 with a one-line message, not a traceback', 'PASS', 'no BGZF EOF marker / file does not contain alignment data; quickcheck agrees.'),
                  A('Empty, single-end, unindexed and MT-named inputs give the correct result or an exit-1 message', 'PASS', 'All match flagstat and hand counts; no ZeroDivisionError or silent 0.'),
                  A('A CRAM decoded against the wrong reference never prints partial numbers as a report', 'PASS', 'rc 1, no report; the message text is weak (see P2).')]),
]
for i in inputs:
    i['total'] = i['basic'] + i['specialized']
    i['assertions_passed'] = sum(a['result'] == 'PASS' for a in i['assertions']); i['assertions_total'] = len(i['assertions'])
    i['status_flag'] = '✅' if i['status'] == 'COMPLETED' and i['total'] >= 75 else '⚠️'
avg = round(sum(i['total'] for i in inputs) / len(inputs), 1)
sub = sum(v[0] for v in static.values())
sw, dw = round(sub * 0.4, 1), round(avg * 0.6, 1); score = round(sw + dw)
grade = 'Production Ready' if score >= 85 else 'Limited Release' if score >= 75 else 'Beta Only' if score >= 60 else 'Reject'
passed = sum(i['assertions_passed'] for i in inputs); total = sum(i['assertions_total'] for i in inputs)
l1 = sum(i['basic'] for i in inputs) / 7; l2 = sum(i['specialized'] for i in inputs) / 7
print('static', sub, 'exec avg', avg, 'score', score, grade, 'assertions', passed, total, f'{100*passed/total:.1f}%', 'L1', round(l1, 1), 'L2', round(l2, 1))
recs = [
 dict(priority='P2', title='mosdepth --fast-mode caveat names deletions only', observed_in=[4],
      problem='SKILL.md says --fast-mode "also counts deletion (D) bases as covered". It also counts spliced N bases: on the real RNA BAM mosdepth reports 17.67x by default and 49.40x with --fast-mode (depth -aa 23.67x, mates counted twice); on own_del the fast-mode sum 9600 = mates twice + D + N. samtools mpileup depth also includes D and N (own_del -Q 0: 9600 vs depth 5200), which the overlap table does not say.',
      root_cause='The round-2 note was written from an amplicon (deletion) BAM only.',
      fix='Say --fast-mode ignores internal CIGAR operations (D and N count as covered) and add one clause to the overlap table that mpileup counts D and N.'),
 dict(priority='P2', title='MAX_INSERT is described as the samtools stats default, but stats clamps', observed_in=[3],
      problem='qc_report.py and the Insert Size Caveats bullet say longer templates are dropped, attributed to samtools stats -i 8000. samtools stats counts them at the cap: own_insert mean 3555.5 (stats) vs 2286 (qc_report), predicted 3555.5 for clamping and confirmed with -i 7000 and -i 400.',
      root_cause='The cap value was matched to stats -i, its behaviour above the cap was not compared.',
      fix='Reword to "drops templates >= 8000 (samtools stats -i 8000 instead counts them at 8000, so the two means differ on long-insert libraries)".'),
 dict(priority='P2', title='Wrong-reference CRAM reports "truncated file"', observed_in=[7],
      problem='qc_report.py on a CRAM decoded against a FASTA with the right names but other bases exits 1 but prints "cannot read ...: truncated file"; only htslib stderr lines above it say MD5 mismatch. The CRAM hint is shown only when no reference was passed. pileup calls on CRAM also emit a "multiple_iterators not implemented for CRAM" UserWarning.',
      root_cause='The handler prints str(e) and adds a hint only for the missing-reference case.',
      fix='When a reference was given and the read fails, append "check that reference.fa is the FASTA the CRAM was written against (see the htslib MD5 message above)".'),
 dict(priority='P2', title='Assay-threshold table and FREEMIX/somalier values unsourced', observed_in=[6],
      problem='The mapping/duplicate/proper-pair/MAPQ/Mt table and the FREEMIX 1% / 5% cut-offs are hedged as literature ranges but no source is given and no run here could check them; VerifyBamID2 end to end stops at "Insufficient Available markers" on a synthetic slice and somalier needs a whole-GRCh38 FASTA.',
      root_cause='No whole-genome data and no citations are available to the fixer or to me.',
      fix='Cite the source of each row (or a single reference per assay) or move the table to a clearly marked "orientation only" note; keep the existing "not run end to end" label until a real WGS BAM run is added.'),
]
report = {
 'meta': meta, 'veto_gates': veto,
 'static_score': {'subtotal': sub, 'max': 100, 'categories': {k: {'score': v[0], 'max': v[1], 'note': v[2]} for k, v in static.items()}},
 'dynamic_score': {'execution_avg': avg, 'max': 100, 'assertion_pass_rate': {'passed': passed, 'total': total},
   'inputs': [{'index': i['index'], 'type': i['type'], 'label': i['label'], 'status': i['status'], 'status_flag': i['status_flag'], 'note': i['note'],
               'executed': True,
               'execution_note': 'Executed for real in WSL (samtools 1.24, pysam 0.24.1, mosdepth 0.3.14, bcftools 1.24, Picard 3.5.0); asserted on content against truth by construction and a second method. ' + ('Part of the input is not executable: VerifyBamID2 gave no FREEMIX and somalier could not run (no whole-genome data); labelled by the Skill.' if i['index'] == 6 else 'No part skipped.'),
               'basic': i['basic'], 'specialized': i['specialized'], 'total': i['total'],
               'assertions_passed': i['assertions_passed'], 'assertions_total': i['assertions_total'], 'assertions': i['assertions']} for i in inputs]},
 'final': {'static_weighted': sw, 'dynamic_weighted': dw, 'score': score, 'max': 100, 'grade': grade, 'grade_symbol': '⭐' if grade == 'Production Ready' else '✅', 'deployable': True, 'veto_override': False},
 'key_strengths': [
   'The round-2 target P1 is fixed and verified: qc_report.py and the pysam snippets handle unaligned BAM (equal to flagstat), CRAM with reference (equal to flagstat, own and real), CRAM without reference (exit 1 with a reference hint) and broken files (exit 1, one line).',
   'Every depth denominator, cap and overlap statement I could run reproduced against truth by construction and a second method; the two claims the earlier re-audit got wrong (mosdepth deletions, bcftools INFO/DP) are now stated correctly.',
   'Round 2 removed the duplicated Quick Reference table and the usage-guide overlap with nothing lost (every removed row exists as a command elsewhere), and SKILL.md is under 500 lines.',
   'Unrun claims are honestly labelled (literature ranges, "commonly cited", "not run end to end"); the labelling matched what I saw: VerifyBamID2 gave no FREEMIX and somalier could not run.'],
 'recommendations': recs}
json.dump(report, open(os.path.join(ROOT, 'eval_report_bio-bam-statistics_result.json'), 'w', encoding='utf-8'), indent=2, ensure_ascii=False)

# ---------------------------------------------------------------- viewer
V = []
W = V.append
W('# Eval Viewer - bio-bam-statistics (second re-audit)\n\nGenerated: 2026-09-20. Source: `%s`. Previous score 84 (Limited Release, one P1). All runs are in `run/` (scripts) and `run/out/` (recorded outputs); the Skill was run from `run/skill/` (byte-identical to the worktree HEAD).\n' % SRC)
W('## Summary Table\n\n| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |\n|---|---|---|---|---|---|---|')
for i in inputs: W(f'| {i["index"]} | {i["type"]} | {i["basic"]} | {i["specialized"]} | {i["total"]} | {i["assertions_passed"]}/{i["assertions_total"]} PASS | {i["status_flag"]} |')
W(f'\n**Execution Average: {avg} / 100**  |  **Assertion Pass Rate: {passed}/{total} ({100*passed/total:.1f}%)**  |  **Static: {sub} / 100**  |  **Final: {score} / 100, {grade}, deployable, no veto, no open P0/P1**\n')
W('Floors for Production Ready: static >= 80 (%d), execution >= 85 (%.1f), Layer 1 avg >= 32 (%.1f), Layer 2 avg >= 48 (%.1f), assertions >= 90%% (%.1f%%): all met.\n' % (sub, avg, l1, l2, 100 * passed / total))
W('## Skill Veto and Research Veto\n\nT1 stability PASS (every recipe run; 10 identical reruns), T2 contract PASS (frontmatter name/description present; shipped files present: `examples/qc_report.py`, `usage-guide.md`, all Related Skills exist), T3 determinism PASS (`run/out/t0_stability_determinism.txt`: 1 distinct output for qc_report.py, the -aa recipe, flagstat, region_depth_stats), T4 security PASS (no eval/exec/subprocess/credentials; grep clean). Research veto (Data Analysis): M1 to M4 PASS (details in the JSON).\n')
W('## Static evaluation (%d / 100)\n\n| Category | Score | Note |\n|---|---|---|' % sub)
for k, v in static.items(): W(f'| {k} | {v[0]}/{v[1]} | {v[2]} |')
W('\n## What Round 2 changed and what I found\n')
W('| Round-2 target | Verdict from my runs |\n|---|---|')
for a, b in [
 ('qc_report.py on unaligned BAM', 'FIXED. uBAM (edge `ubam_no_sq.bam`, 30 records) equals flagstat; text SAM and truncated/text/zero-byte files exit 1 with one line. (`out/t3_edge.txt`, `out/t7_adversarial.txt`, `out/n3_cram_bad_insert.txt`)'),
 ('qc_report.py and snippets on CRAM with / without reference', 'FIXED. With FASTA: equal to flagstat on own CRAM (5 variants) and the real human CRAM. Without a reachable reference: rc 1 + hint. Trap found while testing: `samtools view -C -T` writes `UR:` into the header, so a CRAM decodes "without a reference" as long as that path exists or the htslib cache holds it (`out/n3_`, `n3b_`, `n3c_`). Wrong-reference message weak (P2).'),
 ('depth -aa -b on read-less contigs', 'FIXED. 3110 rows (planted-depth), ctgB 800 rows (own_ctg); `-a` drops them (2810 / 0), as stated. (`out/t2_planted.txt`, `out/n2_own_ctg.txt`)'),
 ('mosdepth summary note', 'CORRECT. 19000 of 22000 bp, 2.95x vs 2.57x; 20100 of 25100 bp, 5.98x vs 4.79x. `--fast-mode` deletion statement correct but incomplete (spliced N also counted): P2.'),
 ('MAX_INSERT', 'Documented and correct for qc_report (mean 2286 = truth), but stats clamps at the cap rather than dropping (3555.5): P2.'),
 ('Per-tool overlap table', 'CORRECT on the real BAM to 2 decimals for every row; bcftools INFO/DP 16.77 with and without -x verified independently (also on own_del). The fixer\'s two counter-claims are right, the earlier re-audit sentences were wrong.'),
 ('Removed Quick Reference table; usage-guide dedup', 'Nothing lost: each removed row is a command elsewhere (`git diff 377e368 c8b1af2`); usage-guide is overview + prompts + pointer.'),
 ('FREEMIX / somalier labelling', 'Honest and accurate: VerifyBamID2 on a synthetic 40x chr20 BAM stops with "Insufficient Available markers" (no FREEMIX), somalier extract needs a whole-GRCh38 FASTA. Numbers themselves stay unsourced: P2.')]:
    W(f'| {a} | {b} |')
W('\nDefects introduced by Round 2: none that changes a result. Cosmetic: pysam pileup on CRAM prints a "multiple_iterators not implemented for CRAM" UserWarning; htslib prints "[E::cram_index_load]" for an unindexed CRAM although reading succeeds.\n')
DET = {
 1: (['t0_stability_determinism.sh', 't1_canonical.sh', 't1b_depth_real.sh', 'n5_real_region.sh (+ n5_real_region.py)', 'n9_file_blocks.sh'],
     [('t1b_depth_real.txt', 'block 017|mean 16|TRUTH|raw depth|region \\[|OK\\]', 16), ('n5_real_region.txt', 'REAL_REGION|1000G|RNA', 12)]),
 2: (['t2_planted.sh', 'n2_own_ctg.sh (+ n2_region_truth.py, n1_make_new_data.py)'], [('t2_planted.txt', None, 14), ('n2_own_ctg.txt', None, 42)]),
 3: (['t3_edge.sh', 'n8_own_counts.sh', 'n3_cram_bad_insert.sh (part b)', 'n3b_cram_isolated.sh (part b)'], [('t3_edge.txt', 'PASS|FAIL|TOTAL|EXPECTED', 16), ('n8_own_counts.txt', None, 14), ('n3_cram_bad_insert.txt', 'TRUTH qc_report|qc_report.py\\]|Insert size|insert size average|inward|block 030', 10), ('n3b_cram_isolated.txt', 'predicted|samtools stats -i', 8)]),
 4: (['t4_depth_cap.sh', 'n4_disputed_claims.sh (+ n4_overlap_del.py)'], [('t4_depth_cap.txt', None, 24), ('n4_disputed_claims.txt', None, 42)]),
 5: (['t5_batch_plots.sh', 'n6_misc_claims.sh', 'n9_file_blocks.sh'], [('t5_batch_plots.txt', None, 26), ('n6_misc_claims.txt', None, 26), ('n9_file_blocks.txt', None, 6)]),
 6: (['t6_scope.sh', 't6b_qc_insert_cap.sh', 't10_vb2.sh (+ t10_make_vb2_data.py)', 't11_basesmapped.sh', 't8_misc_claims.sh'], [('t6_scope.txt', 'PASS|SOFTCLIP|PCT_|MEAN_TARGET|independent|insert size average|outward|Insufficient|No reads found|not found|contamination', 30), ('t10_vb2.txt', None, 10), ('t11_basesmapped.txt', None, 5)]),
 7: (['t7_adversarial.sh', 'n3_cram_bad_insert.sh', 'n3b_cram_isolated.sh', 'n3c_cram_no_ur.sh', 'n7_errmsgs.sh', 't9_syntax_sweep.sh', 't8_misc_claims.sh', 'g1_mt.sh'], [('t7_adversarial.txt', None, 34), ('n3c_cram_no_ur.txt', None, 26), ('n3_cram_bad_insert.txt', 'truncated|text_named|zero_byte|rc=|quickcheck', 18), ('n7_errmsgs.txt', None, 10), ('t9_syntax_sweep.txt', 'FAIL', 2)]),
}
W('## Detailed Outputs\n\nInputs 1, 3, 4 (partly), 5, 6, 7 re-run the previous auditor inputs (their generators are `g0_generate.sh`, `make_synth.py`, `make_depth.py`, `make_edge.py`, `g1_mt.sh`); the `n*_` scripts are my NEW inputs. Data made here is SYNTHETIC with truth by construction (`data/`, `data/new/`); real data is `audit-envs/alignment-files/public-data/` (read only).\n')
for i in inputs:
    scripts, excerpts = DET[i['index']]
    W(f'### Input {i["index"]} - {i["type"]}: {i["label"]}\n')
    W(f'**Prompt:** {i["prompt"]}\n')
    W('**Executed:** true. **Scripts (in `run/`):** ' + ', '.join('`%s`' % x for x in scripts) + '\n')
    W(f'**Result:** {i["note"]}\n')
    for name, pat, n in excerpts:
        W(f'Output excerpt `out/{name}`' + (f' (lines matching `{pat}`)' if pat else '') + ':\n\n```\n' + ex(name, pat, n, 210) + '\n```\n')
    W(f'**Scores:** Basic {i["basic"]}/40 | Specialized {i["specialized"]}/60 | Total {i["total"]}/100\n\n**Assertions:**')
    for a in i['assertions']: W(f'- [{a["result"]}] {a["text"]} - {a["note"]}')
    W('')
W('## Code the Skill directs, as run\n\nEvery fenced block of `SKILL.md` was extracted verbatim to `run/blocks/` (`extract_blocks.py`) and run through the scripts above; `examples/qc_report.py` ran from `run/skill/examples/`. `region_depth_stats` (block 029) was exec\'d from the extracted block by `depth_truth.py`, `n2_region_truth.py`, `n5_real_region.py`, `t2_region_vs_truth.py`.\n')
W('## Recommendations\n')
for r in recs: W(f'**[{r["priority"]}] {r["title"]}** (input {r["observed_in"]})  \nProblem: {r["problem"]}  \nRoot cause: {r["root_cause"]}  \nFix: {r["fix"]}\n')
W('No P0 and no P1 is open. Other observations (not defects): `samtools stats -r ref.fa` gives identical GCD rows with and without `-r` at the same bin size on the test data (the help text says it is required); the CRAM `UR:` field makes CRAM decoding look reference-free on the machine that wrote it.\n')
open(os.path.join(ROOT, 'eval_viewer_bio-bam-statistics.md'), 'w', encoding='utf-8').write('\n'.join(V))
print('viewer written', sum(len(x) for x in V), 'chars')
