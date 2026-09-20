"""Build eval_report_bio-alignment-msa-statistics_result.json from the scores decided after reading the run outputs
(out_*.txt, results_*.json) and run the schema Pre-Emit Checklist. Run from run/:  python b99_build_report.py"""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(HERE), 'eval_report_bio-alignment-msa-statistics_result.json')

def A(text, ok, note):
    return {'text': text, 'result': 'PASS' if ok else 'FAIL', 'note': note}

inputs = []
def add(index, type_, label, status, flag, note, basic, spec, assertions, executed, exec_note):
    passed = sum(1 for a in assertions if a['result'] == 'PASS')
    inputs.append({'index': index, 'type': type_, 'label': label, 'status': status, 'status_flag': flag, 'note': note,
                   'basic': basic, 'specialized': spec, 'total': basic + spec, 'assertions_passed': passed,
                   'assertions_total': len(assertions), 'assertions': assertions, 'executed': executed, 'execution_note': exec_note})

add(1, 'Canonical', 'Pfam PF00042 globin seed (real, 73 x 141): identity, conservation, entropy/IC, gaps, SP, PSSM, JSD', 'COMPLETED', '✅',
    'All 40 checks equal independent implementations on the dashed and the dotted copy; pre-fix failures (alignment_score, IC with B/Z) fixed',
    35, 55, [
    A('PID1-PID4 (vectorized and per-pair function) equal an independent numpy reference on all 2628 pairs, identical for "-" and "." gap files', True, 'max diff 0.0; mean PID1 19.63% on both (pre-fix dotted file 32.0%)'),
    A('information_content equals scipy rel_entr KL with the published Robinson background and stays under 6.23 bits with B/Z present', True, 'max diff 8.9e-16; max IC 5.507 bits (pre-fix +0.58 bits at B/Z columns)'),
    A('alignment_score equals the textbook sum-of-pairs with gap/gap = 0', True, '-215960 == count-based reference (-330976 if gap/gap were charged)'),
    A('Average conservation equals an independent mean over columns with >= 50% residues and matches the SKILL.md text (34.3%)', True, '34.29% over 118 of 141 columns; all-column mean 37.93%'),
    A('All 12 non-stub SKILL.md python blocks and all 8 shipped examples run on the file with only the intended alphabet warning', True, 'block 0 warns Z 12, B 15; DistanceCalculator block now runs on the normalised seed'),
], True, 'b01_input1_seed.py (both variants, blocks verbatim, examples via argv); out_b01.txt')

add(2, 'Variant A', 'Real tool output: MAFFT, Clustal Omega, hmmalign AFA (lowercase inserts + dots), Pfam seed re-aligned by MAFFT', 'COMPLETED', '✅',
    '82/82 checks; hmmalign IC max 5.507 (pre-fix 29.35); the raw hmmalign A2M file is ragged and AlignIO cannot load it, and SKILL.md names A2M without a loader (recorded in P2 #5)',
    35, 55, [
    A('MAFFT and Clustal Omega output give identical statistics to the reference (identity, conservation, IC, PSSM, JSD, SP)', True, 'SP 8607 and 8403 equal reference; PID1-4 max diff 0'),
    A('hmmalign AFA (284 lowercase letters, 68 dots) gives IC within the physical bound and equal to the KL reference', True, 'IC max 5.507 (pre-fix 29.35 bits); PSSM max diff 0'),
    A('BLOSUM62 sum_of_pairs and alignment_score on hmmalign AFA equal independent references', True, 'SP 6976 (pre-fix 6539), simple SP -1279'),
    A('The DistanceCalculator block runs verbatim on all four real alignments after the normalising import', True, 'pre-fix ValueError Bad letter m / .'),
    A('Pairwise identity on the hmmalign AFA equals the independent reference', True, 'mean PID1 39.3%, PID4 39.4% (pre-fix Skill 40.3% vs reference 38.6%); upper=False (documented A2M path) leaves PID2 unchanged at 40.30%'),
], True, 'b02_input2_real_tool_outputs.py; data made by _first_audit_data_provenance/s01 (MAFFT 7.526, Clustal Omega 1.2.4, HMMER 3.4 in WSL); out_b02.txt')

add(3, 'Edge', 'Terminal overhangs: PID1-4 against pwalign::pid on 169 own real pairwise alignments + 6 hand-computed cases', 'COMPLETED', '✅',
    'PID1/PID2 equal pwalign on all 169 pairs and 88 staggered-flank MSA rows; PID3/PID4 equal pwalign on all; the old denominator would have differed on 22 and 88',
    36, 56, [
    A('PID1 and PID2 equal pwalign::pid within 0.01 pts on 169 protein/DNA alignments (global, local, overlap, global-local, local-global; BLOSUM62, BLOSUM45, DNA 1/-3)', True, 'max diff 0.00000; 22 pairs carry end gaps'),
    A('With unaligned flanks staggered into MSA rows (88 pairs) PID1-PID4 all equal pwalign', True, 'max diff 0.00000; old any-residue denominator differs on 88 of 88 (max 34.1 pts)'),
    A('Six hand-derived cases (terminal overhang only, internal gaps in both rows, no aligned pair, one column, all-gap row, s1/s2 = 80/100/80/66.7) match', True, 'function and vectorized both equal; undefined cases NaN'),
    A('Vectorized matrix equals the per-pair function for every pair and method', True, '169 pairs x 4 methods, max diff 0.0'),
    A('The test discriminates: the pre-fix denominator disagrees with pwalign', True, '22 of 169 pairs (end gaps), 88 of 88 staggered-flank pairs'),
], True, 'b03_pid_pwalign.R (r.sh, pwalign 1.2.0), b03_pid_compare.py, b03b_pid4_probe.py (pwalign PID3/PID4 use the full sequence lengths), b03c_debug.py; out_b03*.txt')

add(4, 'Variant B', 'Real DNA: six HBB CDS, MAFFT default lowercase output: Ti/Tv, DNA IC, conservation, identity', 'COMPLETED', '✅',
    'Ti/Tv 428/355 = 1.21 (pre-fix 0.00), DNA IC max 2.000 (pre-fix 29.90); lower and upper case give identical statistics',
    36, 55, [
    A('Ti/Tv from the shipped script on the lowercase MAFFT file equals the independent count (428 transitions, 355 transversions, 1.21)', True, 'CLI prints Transitions: 428, Transversions: 355, Ti/Tv ratio: 1.21'),
    A('DNA information content is bounded by 2 bits and equals scipy KL', True, 'max 2.000 (pre-fix 29.90)'),
    A('Lower-case and upper-case copies of the alignment give identical Ti/Tv, IC, conservation and identity', True, 'ti/tv, IC max and mean PID1 identical to 1e-15'),
    A('entropy_analysis.py detects DNA and reports max entropy 2.000; PSSM uses the DNA background', True, '"Treating as DNA (uniform background)"; PSSM max diff 0'),
    A('SKILL.md information_content(col, DNA_UNIFORM) on the lowercase alignment stays at or below 2 bits', True, 'max 2.000'),
], True, 'b04_input4_dna_mafft.py; out_b04.txt')

add(5, 'Stress', 'Synthetic 300 x 300 and 2000 x 300 protein alignments: identity matrix, conservation, SP, Kimura', 'COMPLETED', '✅',
    '19/19 checks; 2000 x 300 identity matrix in 30 s (PID1) and 27 s (PID4); PID1 now equals the span definition (pre-fix worst -11.8 pts)',
    35, 55, [
    A('300 x 300 PID1-4 equal the numpy reference on 4000 sampled pairs', True, 'max diff 0.0'),
    A('sum_of_pairs (BLOSUM62, 13M residue pairs) equals a count-based independent SP', True, '18093751 == 18093751; SKILL.md blocks total 142 s'),
    A('alignment_score equals the textbook SP with gap/gap = 0 and Kimura equals the reference on 4000 pairs', True, '-3140959; 0 inf-band mismatches'),
    A('2000 x 300 identity matrix completes for PID1 and PID4 with symmetric finite output equal to the reference on 3000 sampled pairs', True, '30 s and 27 s'),
    A('All four CLI examples run at 300 x 300 through argv in seconds', True, '0.5-3.9 s each, empty stderr'),
], True, 'b08_input5_stress.py (data: first-audit synthetic files, seed 20260920/21); out_b08.txt')

add(6, 'Scope Boundary', 'Publication-grade distances: ModelTest-NG / IQ-TREE / distmat hand-off + DistanceCalculator snippet', 'COMPLETED', '✅',
    'Skill stays in scope and routes to ModelTest-NG; the commands run; stale `.get` claim removed',
    36, 54, [
    A('modeltest-ng commands from SKILL.md run and select a best model (nt K80+I by BIC, aa DAYHOFF+G4 by BIC)', True, 'ModelTest-NG 0.1.7, exit 0, both logs parsed'),
    A('DistanceCalculator(blosum62) equals the hand formula on 28 pairs', True, 'max diff 0.0'),
    A('kimura_protein_distance.py equals EMBOSS distmat -protmethod 2 on 28 of 28 pairs', True, 'max diff 0.00005'),
    A('The .mldist claim holds and the closest pair agrees with IQ-TREE LG distances', True, 'HBB_HUMAN / HBB_PANTR'),
    A('Scope: SKILL.md refuses to pick a model by rule of thumb and marks hand-coded corrections as exploratory', True, 'text asserted in b09_input6_distance_py.py'),
], True, 'b09_wsl_distance_tools.sh (WSL aln-mtng, iqtree3, EMBOSS), b09_input6_distance_py.py; out_b09*.txt')

add(7, 'Adversarial', 'Messy collaborator alignment (case, dots, X/B/Z/U/*, all-gap row) + degenerate alignments + probes of the new behaviours', 'COMPLETED', '✅',
    '15 of 16 checks equal independent references; fix-introduced defect: SKILL.md average_conservation raises ZeroDivisionError when no column reaches min_occupancy; DNA with 12% IUPAC codes is classified as protein without a warning',
    33, 50, [
    A('Case/dot normalisation and identity: row0 vs row1 PID2 = 88.9% and IC per column equals the drop-and-renormalise reference, max 6.23 bits', True, 'pre-fix 40.0% and 21.3 bits'),
    A('An all-gap sequence gives NaN identity (not 0), is excluded from the average and counted (10 undefined pairs)', True, 'average 81.36% over the 20 defined ordered pairs'),
    A('sum_of_pairs skips outside-alphabet pairs and reports the count; alignment_score of an all-gap row is textbook', True, '388 == reference, warning "2 residue pairs"; -45'),
    A('check_alphabet names exactly the letters the statistics will drop (X, B, Z, U, *)', True, 'stderr warning lists all five'),
    A('SKILL.md average_conservation returns for a fragment alignment whose columns are all below min_occupancy', False, 'ZeroDivisionError (the shipped conservation_profile.py prints "nan% over 0 columns" with a numpy RuntimeWarning instead)'),
], True, 'b07_input7_messy_and_edges.py; out_b07.txt')

add(8, 'Variant B', 'NEW: Rfam RF00050 FMN riboswitch seed (real RNA, 146 x 221, U, 38% gaps, Stockholm) + lower/dot FASTA copy', 'COMPLETED', '✅',
    '34/34 checks; RNA U to T through load_alignment; Stockholm and lowercase/dotted FASTA give identical statistics; inline block only warns about U',
    35, 55, [
    A('Ti/Tv on the RNA alignment equals an independent count after U to T (216522 transitions, 189758 transversions, 0 ambiguity pairs)', True, 'ratio 1.141'),
    A('Information content is bounded by 2 bits and equals scipy KL; PID1-4 equal the numpy reference on 3000 sampled pairs', True, 'IC max 2.000; PID1 mean 59.10%'),
    A('The Stockholm file and a lowercase, dot-gapped FASTA copy give identical Ti/Tv, IC, PID1 and conservation', True, 'synthetic transformation of the real alignment'),
    A('82 columns with < 50% residues are NaN and the average conservation is 72.0% over 139 columns; gap_statistics matches the independent gap and >50%-gap column counts', True, '12411 gaps; 82 columns'),
    A('Skipping u_to_t in the inline SKILL.md path is flagged by check_alphabet rather than silently accepted', True, 'WARNING lists U: 4217 of 19855 residues; Ti/Tv without U to T would be 126591/71147 with 208542 unclassified pairs'),
], True, 'b05_new_rna_rfam.py (data downloaded from rfam.org 2026-09-20); out_b05.txt')

add(9, 'Edge', 'NEW: Pfam PF00069 kinase seed (real protein, 37 x 419, 36% dots, staggered fragments): conserved columns, identity, SP', 'COMPLETED', '✅',
    '40/40 numeric checks; gap-heavy family exposes that 157 of 419 columns are NaN and a naive ranking of the NaN-bearing scores is silently wrong',
    35, 54, [
    A('PID1-4 equal the numpy reference on 666 pairs; the dotted FASTA and the Stockholm file give identical statistics; PID2 is the highest mean', True, 'mean PID1 23.43, PID2 28.04, PID3 26.27, PID4 25.49'),
    A('IC, PSSM, JSD, Kimura, SP (186874) and alignment_score (-137507) equal independent references', True, 'IC max 5.507'),
    A('Average conservation with the occupancy rule equals the independent mean over the 262 columns with >= 50% residues', True, '40.9% (45.1% with min_occupancy=0; 36 sparse columns would score 100%)'),
    A('All 12 non-stub SKILL.md blocks run verbatim on the dotted kinase seed', True, 'no errors'),
    A('Following SKILL.md, ranking the most conserved columns (a shipped usage-guide prompt) is correct in the presence of NaN scores', False, 'sorted(key=-score) over the NaN-bearing list returned a top-10 whose 10th value is 0.70 while the NaN-free top-10 are all >= 0.97; SKILL.md says NaN is skipped "by the averages" only'),
], True, 'b06_new_kinase_pfam.py, b11_nan_ranking_probe.py (data downloaded from InterPro 2026-09-20); out_b06.txt, out_b11.txt')

exec_avg = round(sum(i['total'] for i in inputs) / len(inputs), 1)
ap = sum(i['assertions_passed'] for i in inputs); at = sum(i['assertions_total'] for i in inputs)

cats = {
 'functional_suitability': (11, 12, 'Covers every promised use (identity PID1-4, conservation, entropy/IC, JSD, substitutions, gaps, SP, PSSM, distances hand-off); every number checked against an independent implementation; minor: average_conservation crashes on an all-NaN alignment, Kimura returns inf from p=0.85 although the formula is finite to 0.854'),
 'reliability': (10, 12, 'Normalise step plus check_alphabet, NaN for undefined identity/conservation, skipped-pair warnings; gaps: average_conservation ZeroDivisionError, is_nucleotide misclassifies DNA above 10% IUPAC codes with no warning'),
 'performance_context': (6, 8, 'SKILL.md 484 lines with 17 python blocks (5 stubs); usage-guide deduplicated; inline sum_of_pairs is O(N^2 L) Python (28 s at 300 x 300) while the vectorized identity matrix does 2000 x 300 in 30 s'),
 'agent_usability': (14, 16, 'Clear goal/approach per section, normalise-first rule, "Higher means" column, Common Errors keyed to silent symptoms; inline normalize_alignment does not auto-detect RNA (msa_utils does); no guidance on NaN when ranking columns'),
 'human_usability': (6, 8, 'Natural prompts kept in usage-guide; case/gap variants now handled; examples/CLI guess_format() reads only FASTA and Stockholm; ragged A2M cannot be loaded and no route is given'),
 'security': (11, 12, 'Read-only, no eval/exec/network/credentials (grepped); alphabet and method validation present; file paths from argv are not sanitised (local files only)'),
 'maintainability': (10, 12, 'msa_utils.py shared by all examples; Robinson table defined once; selftest.py with hand-derived values caught 16 of 20 mutants but not is_nucleotide, Capra gap penalty/smoothing, gap_statistics, and the inline gap/gap and SP semantics are untested in shipped code; inline SKILL.md functions duplicate example code'),
 'agent_specific': (18, 20, 'Description generic but on target; progressive disclosure (484 lines, examples/, pointers to msa-parsing, multiple-alignment, phylogenetics); idempotent and deterministic; twilight-zone and distance-model escape hatches present'),
}
static = sum(v[0] for v in cats.values())
sw = round(static * 0.4, 1); dw = round(exec_avg * 0.6, 1); score = round(sw + dw)
grade = 'Production Ready' if score >= 85 else 'Limited Release' if score >= 75 else 'Beta Only' if score >= 60 else 'Reject'

rec = [
 {'priority': 'P2', 'title': 'average_conservation raises ZeroDivisionError when no column qualifies', 'observed_in': [7],
  'problem': 'On an alignment whose columns are all below min_occupancy (fragments, sparse supermatrix) the SKILL.md function divides by zero; conservation_profile.py on the same file prints "nan% over 0 of 16 columns" with a numpy RuntimeWarning, so the two disagree.',
  'root_cause': 'The occupancy rule added in the fix returns NaN for every column but the mean does not guard the empty case.',
  'fix': 'Return (float("nan"), 0) when `used` is empty and print an explicit "no column has >= min_occupancy residues" message in the SKILL.md block and the example.'},
 {'priority': 'P2', 'title': 'NaN conservation default with no NaN-aware ranking guidance', 'observed_in': [9, 1],
  'problem': 'Ranking column_conservation() output with sorted(key=-score), the obvious answer to the shipped prompt "Which columns are most conserved?", silently misorders when NaN is present: Pfam globin seed top-10 values 0.37-1.0 vs 0.63-1.0 for the NaN-free ranking; kinase seed 157 NaN columns.',
  'root_cause': 'SKILL.md says NaN columns are "skipped by the averages" but gives no ranking snippet or warning for sort/max.',
  'fix': 'Add a two-line NaN-safe ranking (e.g. `[i for i in np.argsort(-np.nan_to_num(scores, nan=-1)) ...]` or filter NaN first) beside the Per-Column Conservation block and say NaN must be filtered before sort/max.'},
 {'priority': 'P2', 'title': 'is_nucleotide() 0.9 threshold misclassifies IUPAC-rich DNA silently', 'observed_in': [7],
  'problem': 'A DNA alignment with 12% R/Y/S/W/K/M codes is treated as protein (Robinson background, IC max 5.70 bits) and check_alphabet is silent because those letters are also amino acids; at 5% it is detected correctly.',
  'root_cause': 'Auto-detection counts only A/C/G/T/U/N and the protein alphabet contains every IUPAC letter, so the warning cannot fire.',
  'fix': 'Count the full IUPAC nucleotide set in is_nucleotide(), or print the chosen alphabet with the letter composition and let the caller override; document the threshold in SKILL.md.'},
 {'priority': 'P2', 'title': 'selftest.py leaves the gap/gap fix, is_nucleotide and JSD smoothing untested', 'observed_in': [1, 7],
  'problem': 'Mutation testing: 16 of 20 breaks were caught; survivors were is_nucleotide always False, Capra-Singh gap penalty removed, lambda smoothing removed and gap_statistics.py. alignment_score and sum_of_pairs live only in SKILL.md, so the gap/gap = 0 convention has no shipped regression check.',
  'root_cause': 'selftest.py imports only example modules and asserts JSD shape rather than values; inline SKILL.md functions are not importable.',
  'fix': 'Move alignment_score and sum_of_pairs into msa_utils.py (or an examples file), assert the hand values (-12, 78, all-gap column unchanged), assert one JSD column value, and assert is_nucleotide/pick_background on the shipped DNA example.'},
 {'priority': 'P2', 'title': 'Minor: guess_format(), A2M route and the Kimura 0.85 band', 'observed_in': [2, 5],
  'problem': 'examples/CLI treat every non-Stockholm extension as FASTA (Clustal/PHYLIP argv fail); SKILL.md mentions A2M with upper=False but hmmalign A2M is ragged and cannot be loaded by AlignIO; kimura returns inf for 0.85 <= p < 0.854 (92 of 2628 seed pairs) where the formula is finite.',
  'root_cause': 'Format guessing is two-way and the 0.85 cut-off is a rounded pole.',
  'fix': 'Map .aln/.phy/.a2m via a small dict or accept a format argument in load_alignment CLI use, point the A2M sentence to alignment-io for loading, and state that inf means p >= 0.85 by convention.'},
]
key_strengths = [
 'Every pre-fix silent-wrong result is fixed and verified against independent implementations: lowercase/dotted input, DNA Ti/Tv and IC, gap/gap scoring, IC with ambiguity letters, PID1 terminal overhangs.',
 'PID1 equals pwalign::pid on 169 own pairwise alignments and 88 MSA rows with staggered flanks, and the six hand-computed cases (including undefined NaN cases) match.',
 'The normalise-first import, check_alphabet warnings and skipped-pair counts turn formerly silent failures into visible messages; every example now runs with no arguments and selftest.py passes on two numpy versions.',
 'usage-guide deduplication lost nothing: every tip, table row and prerequisite is present once in SKILL.md.',
]
report = {
 'meta': {'skill_name': 'bio-alignment-msa-statistics',
          'description': 'Calculate alignment statistics including sequence identity, conservation scores, substitution matrices, and similarity metrics. Use when comparing alignment quality, measuring sequence divergence, and analyzing evolutionary patterns.',
          'evaluated_on': '2026-09-20', 'evaluator_version': 'skill-auditor@1.0', 'category': 'Data Analysis', 'execution_mode': 'D', 'complexity': 'Complex',
          'n_inputs': len(inputs),
          'source': 'mrsonord2240/bioSkills@7c5cb44b27b2edaabdf5129fdd541523f4b9ef27:alignment/msa-statistics',
          'audit_kind': 're-audit of a fixed Skill (pre-fix: 66, Beta Only, first audit at 354b4992); inputs 1-7 are the first audit inputs re-run as regression, inputs 8-9 are new (real Rfam RNA and Pfam kinase alignments)',
          'executed_summary': f'{len(inputs)}/{len(inputs)} inputs executed; 310 of 311 scripted checks pass (the failure is the average_conservation crash); the NaN-ranking hazard and the IUPAC misdetection are probe findings (b11, b07 section C)'},
 'veto_gates': {
   'skill_veto': {'gate': 'PASS', 'stability': 'PASS', 'contract': 'PASS', 'determinism': 'PASS', 'security': 'PASS'},
   'research_veto': {'applicable': True, 'gate': 'PASS',
     'scientific_integrity': {'result': 'PASS', 'detail': 'No fabricated values; numeric claims re-verified: 34.3% vs 37.9% mean conservation, Ti/Tv 1.21, PID definitions vs pwalign::pid, Capra-Singh Spearman 0.979 and top-10 9/10 vs the authors script, Robinson table equals the published NCBI values and sums to 1.0'},
     'practice_boundaries': {'result': 'PASS', 'detail': 'No clinical or individual-level content in any of 9 inputs'},
     'methodological_ground': {'result': 'PASS', 'detail': 'PID definitions, KL information content with an empirical background, occupancy-aware conservation and the hand-off of publication-grade distances to ModelTest-NG/IQ-TREE are sound; no principled fallacy in any output'},
     'code_usability': {'result': 'PASS', 'detail': 'All 8 examples and 12 non-stub SKILL.md blocks run on real data; selftest.py passes on Windows numpy 2.0.2 and WSL numpy 2.5.3; the only exception found is the average_conservation ZeroDivisionError on an all-NaN edge case (P2)'}}},
 'static_score': {'subtotal': static, 'max': 100, 'categories': {k: {'score': v[0], 'max': v[1], 'note': v[2]} for k, v in cats.items()}},
 'dynamic_score': {'execution_avg': exec_avg, 'max': 100, 'assertion_pass_rate': {'passed': ap, 'total': at}, 'inputs': inputs},
 'final': {'static_weighted': sw, 'dynamic_weighted': dw, 'score': score, 'max': 100, 'grade': grade,
           'grade_symbol': {'Production Ready': '⭐', 'Limited Release': '✅', 'Beta Only': '⚠️', 'Reject': '❌'}[grade],
           'deployable': grade in ('Production Ready', 'Limited Release'), 'veto_override': False},
 'key_strengths': key_strengths,
 'recommendations': rec,
}
# ---- Pre-Emit Checklist ----
assert len(report['static_score']['categories']) == 8
assert static == sum(v['score'] for v in report['static_score']['categories'].values())
assert all(0 <= v['score'] <= v['max'] for v in report['static_score']['categories'].values())
assert len(inputs) == report['meta']['n_inputs']
for i in inputs:
    assert 3 <= len(i['assertions']) <= 5 and i['assertions_passed'] == sum(a['result'] == 'PASS' for a in i['assertions'])
    assert i['basic'] + i['specialized'] == i['total'] and 0 <= i['basic'] <= 40 and 0 <= i['specialized'] <= 60
    assert i['status_flag'] == ('✅' if i['total'] >= 75 and i['status'] == 'COMPLETED' else '⚠️'), i['index']
assert 2 <= len(key_strengths) <= 5
assert [r['priority'] for r in rec] == sorted(r['priority'] for r in rec)
json.dump(report, open(OUT, 'w', encoding='utf-8'), indent=2, ensure_ascii=False)
l1 = sum(i['basic'] for i in inputs) / len(inputs); l2 = sum(i['specialized'] for i in inputs) / len(inputs)
print(f'static {static}  exec_avg {exec_avg}  L1 avg {l1:.1f}/40  L2 avg {l2:.1f}/60  assertions {ap}/{at} ({ap/at*100:.0f}%)  final {sw}+{dw}={score} {grade}')
print('floors (Production Ready): static>=80', static >= 80, 'exec>=85', exec_avg >= 85, 'L1>=32', l1 >= 32, 'L2>=48', l2 >= 48, 'assertions>=90%', ap / at >= 0.9)
