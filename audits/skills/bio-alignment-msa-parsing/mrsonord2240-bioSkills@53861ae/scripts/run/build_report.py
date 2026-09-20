"""Builds eval_report_bio-alignment-msa-parsing_result.json and eval_viewer_bio-alignment-msa-parsing.md from the scores below and the
captured outputs in run/in*_output.txt. Every number in the tables was produced by the scripts in this folder (see run_all.sh)."""
import json, os, re, statistics
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.dirname(HERE)
def out_lines(n):
    return open(os.path.join(HERE, f'in{n}_output.txt'), encoding='utf-8').read().splitlines()

SRC = 'mrsonord2240/bioSkills@53861ae5dcb3ba770ab1dc6d8cf1582925b49004:alignment/msa-parsing'
DESC = ('Parse and analyze multiple sequence alignments using Biopython. Extract sequences, identify conserved regions, analyze gaps, '
        'work with annotations, and manipulate alignment data for downstream analysis. Use when parsing or manipulating multiple sequence alignments.')

A = lambda t, r, n: {'text': t, 'result': r, 'note': n}
INPUTS = [
 dict(index=1, type='Canonical', label='Pfam globin seed PF00042 (real, 73 x 141): IDs, conserved, gaps, consensus  [regression of first-audit input 1]',
  status='COMPLETED', basic=37, specialized=55, executed=True, script='in1_canonical.py, skillns.py',
  prompt='Here is the Pfam globin seed alignment (PF00042, 73 sequences, Stockholm). List the sequence IDs, show me the GLB2_LUMTE record, find the fully conserved columns and the ones conserved in at least 80% of sequences, count gaps per sequence and per column, and give me a 70% consensus.',
  note='Real data. All 25 python blocks of SKILL.md exec from the file without examples/ on the path; every value equals an independent parse of the raw Stockholm text. Protein consensus now uses X (0 spurious N; was 124).',
  assertions=[
   A('All 25 python blocks of SKILL.md execute from the file (no examples/ on the path)', 'PASS', '25/25 blocks ran, no NameError/ImportError (skillns.py)'),
   A('find_conserved_positions(1.0) and (0.8) equal an independent count from the raw Stockholm text', 'PASS', '(17,F),(77,H) fully conserved; 3 columns at >= 0.8 incl. (11,P); fractions equal'),
   A('Gaps per sequence and per column equal an independent raw-file count of the same 1943 cells', 'PASS', '1943 = 1943 = 1943; per-column list identical'),
   A('Protein consensus uses a non-residue placeholder and equals an independent consensus at 0.7 and 0.5', 'PASS', '124 X, 0 N, 0 true Asn-majority columns; identical to independent (was 124 N of which 2 real Asn)'),
   A('Shipped analyze_alignment / find_conserved / gap_analysis / consensus_sequence run from a copy on the real .sto and print the verified values', 'PASS', 'rc 0, empty stderr; Col 0 composition dict, 1943 gap sums and 50% consensus equal independent values')]),
 dict(index=2, type='Variant A', label='Clean: gappy columns, gappy/duplicate rows, ID filter, keep annotations, save  [regression of first-audit input 2]',
  status='COMPLETED', basic=36, specialized=54, executed=True, script='in2_cleaning.py, probes/probe_sto_roundtrip.py',
  prompt='Clean this alignment: drop columns that are 50% gaps or more, drop sequences with more than 20% gaps, remove exact duplicates, keep only IDs starting with GLB, and save the cleaned alignment. Keep the Stockholm annotations.',
  note='Real Pfam seed + hand-computed synthetic 5 x 12. Annotations now survive and are sliced correctly; over-strict filters raise. Biopython 1.88 own Stockholm writer drops unrecognised tags (GC seq_cons, GR pAS) even for the UNCLEANED alignment - not a Skill defect.',
  assertions=[
   A('remove_gappy_columns(0.5) keeps exactly the columns an independent mask keeps, content identical', 'PASS', '118 of 141 columns, all 73 rows equal raw-file columns; boundary (gap fraction == threshold) removed'),
   A('Record annotations, GC seq_cons and GR letter annotations survive cleaning and are sliced to the kept columns', 'PASS', 'accession/start/end on 73 records; seq_cons equals the original string at the kept columns; was {} before the fix'),
   A('Over-strict filters raise ValueError naming the threshold and the lowest gap fraction instead of returning an empty alignment', 'PASS', "filter_by_gap_content(0.0): 'max_gap_fraction=0.0 (lowest fraction 0.11) removes all 73 sequences'; filter_by_id('^zzz') same"),
   A('Cleaned alignment written as Stockholm loses nothing that Biopython writes for the original', 'PASS', '#=GS 146/146, #=GR 1/1 (active_site sliced); GC seq_cons absent in BOTH (Biopython writer limit, probe)'),
   A('Shipped clean_alignment.py from a copy on the real .sto equals the independent column-then-row pipeline', 'PASS', '73 x 118, IDs/sequences identical, FASTA written with "-" gaps only')]),
 dict(index=3, type='Edge', label='Messy files: all-gap column, single sequence, ragged, "." gaps, A2M/A3M, degenerate weights  [regression of first-audit input 3]',
  status='COMPLETED', basic=34, specialized=49, executed=True, script='in3_edge.py',
  prompt='Some of my alignment files are messy: an HMMER/hhsearch A2M with lowercase inserts and "." gaps, an alignment with an all-gap column, a single-sequence file, a ragged file and a ColabFold A3M. Give me match-only columns and a consensus without it blowing up.',
  note='Synthetic, hand-known answers. All first-audit failures (".", lowercase) fixed. New defect found: all-zero weights give an all-placeholder consensus silently.',
  assertions=[
   A('"."-gapped input: gaps_per_column, coordinate_map, consensus and filters treat "." as a gap', 'PASS', 'gaps [0,0,3,3,0,0] (was all 0); coordinate_map 4 residues (was 6); consensus ACXXGT without "."'),
   A('All-gap column, single sequence and ragged file behave as documented', 'PASS', 'consensus ACD-EG keeps "-"; single sequence reproduced; ragged raises ValueError "same length"'),
   A('A2M example gives the hand-known result on the shipped example.a2m and a hhsearch-style A2M; unpadded A3M fails loudly and the pyhmmer hand-off pads it', 'PASS', '9 match columns, inserts 0/2/1; A3M ValueError; MSAFile(format="a2m") gives the same match-only columns'),
   A('normalize_alignment semantics and modern Bio.Align.Alignment handling', 'PASS', 'upper=False keeps case ("Ac-dE"); input not mutated; Alignment object raises AttributeError (loud), matching the SKILL API note'),
   A('Degenerate weights fail loudly (all-zero weights)', 'FAIL', "consensus_sequence(weights=[0,0,0,0]) returns 'XXXXXX' with only a RuntimeWarning (0/0); wrong length raises ValueError correctly")]),
 dict(index=4, type='Variant B', label='Proximal His of myoglobin (PDB 1MBN) to an alignment column  [regression of first-audit input 4]',
  status='COMPLETED', basic=37, specialized=56, executed=True, script='in4_position_map.py, wsl_tools.sh mafft_globins',
  prompt='In my 8-globin alignment, which column is the proximal histidine of sperm whale myoglobin (PDB 1MBN His93), what residue does every other globin have there, and how do I convert between column numbers and residue numbers?',
  note='Real data: 8 UniProt globins aligned with MAFFT 7.526 L-INS-i, ground truth from real 1MBN coordinates. The SKILL sentence about PDB numbering (His93 = UniProt residue 94) verified.',
  assertions=[
   A('coordinate_map round-trips for all 8 records and equals the loop-based walk', 'PASS', 'ungapped == UniProt sequence, seq->aln->seq exact, gap columns -1, 8/8'),
   A('PDB ground truth and the SKILL sentence about numbering hold', 'PASS', '1MBN starts at Val 1 = UniProt residue 2; index 93 is H, index 92 is S; residue 93 HIS, 64 HIS'),
   A('The column reached from PDB residue 93 holds His in all 8 globins; distal His column too', 'PASS', 'column 94 {H} x 8; distal His column 65 H in both myoglobins'),
   A('find_conserved_positions(1.0) lists the proximal His column (alignment and structure agree)', 'PASS', '(94,H) in the fully conserved list'),
   A('aln_to_seq is -1 exactly at gap columns; doc variable renamed with a 0-based comment', 'PASS', 'gap column [2]; column_of_residue_index_42 with "0-based index 42 is the 43rd residue"')]),
 dict(index=5, type='Stress', label='Henikoff weights, Neff/L, MI-APC on the Pfam seed (real)  [regression of first-audit input 5]',
  status='COMPLETED', basic=36, specialized=54, executed=True, script='in5_weights_neff_mi.py, wsl_tools.sh hmmbuild_pf, probes/probe_pb_easel*.py',
  prompt='Compute Henikoff sequence weights for the Pfam globin seed, report Neff and Neff/L at 62% and 80% identity, and find the top coevolving column pairs with MI-APC (tell me if the alignment is deep enough).',
  note='Real seed. Guard, null, ValueError, Neff table and prose all verified against independent code, pyhmmer, hmmbuild 3.4 and real 1MBN contacts. Easel pb reproduced exactly by a 12-line independent function (the fixer could not), confirming the SKILL prose.',
  assertions=[
   A('henikoff_weights equals an independent Henikoff, matches the hand-computed 4 x 5 answer, and raises on an all-gap alignment', 'PASS', 'max diff 0.0; [7/30,7/30,3/10,7/30]; ValueError names pyhmmer/trimming (was NaN)'),
   A('SKILL prose on Easel pb is correct (gap-ignoring, consensus columns >= 50% residues, / residue count, rescaled to N), Spearman 0.909, max diff 0.0091', 'PASS', 'independent reimplementation matches pyhmmer to 7e-16; pb and blosum weights sum to 73.0'),
   A('Neff table rows reproduced by own runs; Neff/L threshold stated one way', 'PASS', 'Neff 66.08/73.00 == independent; pb sum 73.0; hmmbuild eff_nseq 6.35; no stale "> 0.5" anywhere'),
   A('mi_apc.py enforces the SKILL guard on the seed: warns, ranks raw MI, prints a null, calls no pair', 'PASS', 'WARNING L=141, Neff/L=0.47; raw MI == scipy MI to 4e-15; force=True MI-APC == independent APC; 0 of top 20 above null 2.671'),
   A('SKILL figures reproduced: best MI-APC 0.603 < shuffled 0.616; none of top-30 pairs are 1MBN contacts', 'PASS', '0.6031 vs 0.6161 (seed 0, best of 5); contact precision 0.00 vs baseline 0.09')]),
 dict(index=6, type='Scope Boundary', label='Trim for trees and HMMs, keep column numbers, mask unreliable columns (MUSCLE5 route), stream with pyhmmer  [regression of first-audit input 6]',
  status='COMPLETED', basic=36, specialized=53, executed=True, script='in6_scope_trimming.py, wsl_tools.sh trim/muscle_help/muscle_ens8/muscle_ens73',
  prompt='Trim this Pfam globin alignment for tree building and separately for HMM building, keep the original column numbers, mask unreliable columns, then stream the file with pyhmmer weights.',
  note='The first audit could not run GUIDANCE2. The replacement, a MUSCLE 5.3 ensemble route, was run exactly as SKILL.md writes it on 8 UniProt globins and 73 Pfam sequences; CC decoded independently and compared with a replicate-agreement count computed from the raw .efa.',
  assertions=[
   A('trimAl -colnumbering map reproduces the trimmed alignment; ClipKIT kpic-smart-gap valid', 'PASS', '103 map entries, every trimmed row == original columns at mapped indices; ClipKIT 121 of 141'),
   A('MUSCLE5 route runs as written and the example script decodes CC correctly', 'PASS', 'ens8 best acb.2, 155 columns; 73 Pfam best bca.2, 156 columns; script survivor counts == my own digit decode; masked.fa == best replicate at CC >= 0.9 columns'),
   A('CC reflects replicate agreement and the SKILL sentence about 8 globins holds', 'PASS', 'all 6 columns present in < 90% of the 16 replicates have CC < 0.9; 11 of 155 columns CC < 0.9; mean CC 0.990 vs 0.727 (agree vs disagree)'),
   A('GUIDANCE2 / TCS / the 0.93 cut-off are no longer recommended', 'PASS', '2 mentions, both negative ("not offered", "0.93 does not transfer"); no TCS'),
   A('pyhmmer streaming pattern works and the version block lists pyhmmer >= 0.11.3', 'PASS', '2-alignment Stockholm: [(73,73.0),(73,73.0)]; block states >= 0.11.3, checked 0.12.3, install line')]),
 dict(index=7, type='Adversarial', label='Annotations kept through cleaning, soft-masked DNA, weights, malformed regex  [regression of first-audit input 7]',
  status='COMPLETED', basic=34, specialized=50, executed=True, script='in7_adversarial.py',
  prompt='Pull the secondary structure and RF annotation out of my Stockholm alignment and keep it after cleaning; also give me the consensus of my soft-masked (mixed-case) DNA alignment, weight the sequences before computing conservation, and filter sequences with this regex I typed: "["',
  note='Synthetic, hand-known answers. Every first-audit failure fixed (annotations kept, case-insensitive, weights= accepted, SummaryInfo statement). New: remove_duplicates is the one helper that does not normalise, contradicting "every helper normalises internally".',
  assertions=[
   A('The SKILL.md annotation block, run verbatim on a synthetic Stockholm, returns SS per record and SS_cons', 'PASS', 'seqA HHHEEEC, seqB HHH-EEC, ss_cons HHHEEEC'),
   A('Cleaning keeps SS/RF/GS annotations, sliced by the hand rule, and the written Stockholm carries them', 'PASS', 'SS -> HHHEEC, RF -> xxxxxx; #=GR SS, #=GC SS_cons, #=GC RF, #=GS OS present; re-read equal'),
   A('Soft-masked DNA consensus is case-insensitive; DNA/RNA get N, protein gets X', 'PASS', 'ACGTACGT and 8/8 conserved (was ACGTNNNN, 0); RNA (U) detected'),
   A('weights= is actionable and consistent: hand-computed weighted consensus; malformed regex raises', 'PASS', 'col 3 A -> C as hand computed; weighted vs unweighted helpers agree on 400 random cases (0 mismatches); re.error "unterminated character set"'),
   A('SKILL.md claim "every helper normalises its input internally" holds (remove_duplicates)', 'FAIL', "remove_duplicates keeps AC-GT, AC.GT and ac-gt as 3 distinct rows (expected 1); it compares raw strings")]),
 dict(index=8, type='Variant B', label='NEW: real hmmalign Stockholm/A2M, real HBB CDS DNA (soft-masked), real Pfam Ras seed (EBI download)',
  status='COMPLETED', basic=34, specialized=50, executed=True, script='in8_real_new.py, wsl_tools.sh hmmalign_globins/hmmalign_a2m/mafft_hbb',
  prompt='I have hmmalign output for 8 globins against the Pfam globin profile (Stockholm with "." gaps, lowercase inserts, PP lines) and its A2M version, a MAFFT alignment of six mammalian HBB coding sequences, softmasked in places, and the Pfam Ras seed. Give me match-only columns, conserved columns, a consensus per file, gap counts, weights, and keep the PP/RF annotation through cleaning.',
  note='New input built from files the fixer never saw (HMMER 3.4 hmmalign output, MAFFT 7.526 DNA alignment, PF00071 from the EBI public API). 28 raw assertions pass; the one failure is real: HMMER own A2M output is not padded, so the shipped a2m example (AlignIO) raises.',
  assertions=[
   A('hmmalign Stockholm (mixed case, "." and "-"): gaps, consensus, fully conserved columns equal an independent case-folded parse; proximal His column is H in all 8', 'PASS', '8 x 161; 115 gap cells both ways; 14 conserved columns; coordinate_map(MYG idx 93) -> column 97, HHHHHHHH'),
   A('PP letter annotations and RF/PP_cons survive remove_gappy_columns and equal the raw lines sliced to the kept columns', 'PASS', '147 of 161 columns kept; 8 #=GR PP lines and #=GC RF/PP_cons written'),
   A('Real HBB CDS alignment: nucleotide detected, N placeholder, ATG start; 25% soft-masking changes nothing; Neff by hand', 'PASS', '6 x 444; consensus[:3] ATG; identical consensus/conserved/Henikoff on the lowercased copy; all six >= 0.845 identical -> Neff 1.000'),
   A('Real Ras seed (new family): gaps, consensus, conserved, Henikoff equal independent; P-loop GxxxxGK recovered; guard fires with correct L and Neff/L', 'PASS', '60 x 229; GDXGVGKS; 19 columns >= 0.9; WARNING L=229, Neff/L=0.14 equals my own 32.57/229'),
   A('The shipped examples/a2m_a3m_io.py handles real `hmmalign --outformat a2m` output', 'FAIL', 'rc 1: ValueError "Sequences must all be the same length": HMMER 3.4 writes its A2M unpadded (rows 149-161, no "." chars). match_only_columns itself is right (117 per row = profile LENG = RF x count) when fed records; pyhmmer padding also works')]),
 dict(index=9, type='Stress', label='NEW: redundant clade weighting and deep-alignment MI-APC with planted coupling (synthetic, seeded)',
  status='COMPLETED', basic=37, specialized=55, executed=True, script='in9_weighting_coevolution.py',
  prompt='My 35-sequence alignment is 30 near-identical clones plus 5 divergent sequences: weight it, tell me the effective number of sequences, and give me a consensus and conserved columns that do not just follow the over-represented clade. Separately, I have a deep alignment (400 sequences, 120 columns): find coevolving pairs with MI-APC and tell me when the tool refuses.',
  note='New synthetic input with closed-form answers: the parts of the Skill the real seed cannot reach (weights= in practice, the guard passing, planted coupling recovered, guard boundaries).',
  assertions=[
   A('Henikoff clone-group weight and Neff equal the closed-form hand values', 'PASS', 'clone group 0.3619 = (6/2 + 10/3 + 18/6 + 6*30/35)/40 (unweighted 0.857); Neff(0.62) = 6.000'),
   A('Weighted consensus / conserved columns do not follow the clade', 'PASS', 'unweighted A x34; weighted X in columns 6-33 and only the 6 identical columns conserved (40 unweighted)'),
   A('Deep alignment passes the guard silently and recovers the planted pairs; MI-APC equals independent scipy MI - APC', 'PASS', 'Neff/L 3.33, no warning; (10,60) 2.563 and (25,90) 2.136 rank 1-2 of 7140; max diff 5e-15; MI by hand 1 / 0 / 0.8113 bits'),
   A('mi_apc.py CLI on the deep alignment: no WARNING, planted pairs > 5x the shuffled null, null at the right scale', 'PASS', 'null 0.155 vs independent shuffle 0.131; 2 of top 20 above null'),
   A('Guard boundaries: L = 100 refuses, 101 passes; 400 rows / 60 distinct refuses (Neff/L 0.5)', 'PASS', 'L=100 warns and returns raw MI (== independent MI); force=True differs; redundant set Neff 60')]),
]
for i in INPUTS:
    i['total'] = i['basic'] + i['specialized']
    i['assertions_passed'] = sum(a['result'] == 'PASS' for a in i['assertions']); i['assertions_total'] = len(i['assertions'])
    i['status_flag'] = '✅' if i['status'] == 'COMPLETED' and i['total'] >= 75 else ('⚠️' if i['status'] == 'COMPLETED' else '❌')
    assert 3 <= len(i['assertions']) <= 5

STATIC = {
 'functional_suitability': (10, 12, 'Completeness 4, Correctness 3, Appropriateness 3. Every promised use case (parse, conserved, gaps, annotations, manipulate) plus weights, Neff, MI-APC, position mapping and a MUSCLE5 reliability route works and equals independent ground truth. Small inaccuracies remain: remove_duplicates does not normalise, hmmalign A2M example fails, a pointer to _pdbx_poly_seq_scheme that is not in structure-navigation. Pure-Python MI-APC/Neff are slow.'),
 'reliability': (10, 12, 'Fault tolerance 3, Error reporting 3, Recoverability 4. Empty filters, all-gap Henikoff, wrong-length weights and the APC guard raise or warn with a named threshold and a next step; modern Bio.Align objects fail loudly. Still silent: all-zero weights. Helpers are pure and never mutate the input.'),
 'performance_context': (4, 8, 'Token cost 2, Execution efficiency 2. SKILL.md grew to 504 lines / 28.7 KB with full code duplicated in examples/. select_columns rebuilds str(record.seq) for every kept column, so every helper is quadratic in alignment length (10 x 100,000 columns: 7.2 s per normalisation, 9.0 s per gaps_per_column vs 1.95 s pre-fix); MI-APC and Neff are pure-Python pair loops (400 x 120: about a minute).'),
 'agent_usability': (14, 16, 'Learnability 3, Consistency 3, Feedback design 4, Error prevention 4. One Neff/L rule everywhere, alphabet-aware placeholder, printed null and survivor counts, ValueErrors that name the threshold, estimator-dependence table, PDB-numbering trap. Henikoff/Easel/Neff paragraph is dense; "every helper normalises" has one exception.'),
 'human_usability': (7, 8, 'Discoverability 3, Forgiveness 4. Natural prompts in usage-guide.md now cover weighting, coevolution and reliability; the frontmatter description still omits weights/Neff/MI-APC/MUSCLE5. Input variants ("." gaps, lowercase, mixed case) are handled, and strict rejection (ValueError) is used where continuing would give wrong numbers.'),
 'security': (11, 12, 'Credential safety 4, Input validation 3, Data safety 4. No secrets, network, eval/exec or subprocess in any shipped file (grep); user regex is compiled unvalidated (raises re.error); paths come from argv.'),
 'maintainability': (10, 12, 'Modularity 3, Modifiability 3, Testability 4. examples/ share msa_utils.py; SKILL.md still repeats the function bodies, but I checked SKILL.md and examples produce identical output on the seed. Every example runs with no arguments on shipped data and on a path argument; answers are hand-checkable.'),
 'agent_specific': (18, 20, 'Trigger 3, Progressive disclosure 3, Composability 4, Idempotency 4, Escape hatches 4. Related-skill paths all exist (8/8); hand-offs to trimming, structure-navigation, plmDCA/EVcouplings and pyhmmer are explicit; guard refuses instead of guessing. Description unchanged and undersells the Skill; SKILL.md is over 500 lines.'),
}
static_sub = sum(v[0] for v in STATIC.values())
exec_avg = round(statistics.mean(i['total'] for i in INPUTS), 1)
sw, dw = round(static_sub * 0.4, 1), round(exec_avg * 0.6, 1)
score = int(round(sw + dw))
tot_p = sum(i['assertions_passed'] for i in INPUTS); tot_t = sum(i['assertions_total'] for i in INPUTS)
l1 = statistics.mean(i['basic'] for i in INPUTS); l2 = statistics.mean(i['specialized'] for i in INPUTS)
floors = dict(static=static_sub >= 80, execution=exec_avg >= 85, l1=l1 >= 32, l2=l2 >= 48, assertions=tot_p / tot_t >= 0.9)
assert all(floors.values()), floors
grade, sym = ('Production Ready', '⭐') if score >= 85 else (('Limited Release', '✅') if score >= 75 else ('Beta Only', '⚠️'))

REC = [
 dict(priority='P2', title='select_columns / normalize_alignment is quadratic in length', observed_in=[],
      problem='select_columns does "".join(str(record.seq)[i] for i in keep), materialising the whole string for every kept column, and every helper calls it: 10 x 100,000 columns takes 7.2 s per normalisation (9.0 s for gaps_per_column) against 1.95 s for the pre-fix count; 1 M columns would take about 12 min per call.',
      root_cause='The fix normalises by rebuilding the alignment column by column instead of once per record.',
      fix='Take text = str(record.seq) once per record and slice/translate it (for the full-width case use text.upper().replace(".", "-")); keep select_columns for real column subsets.'),
 dict(priority='P2', title='remove_duplicates does not normalise (doc says every helper does)', observed_in=[7],
      problem='remove_duplicates compares raw strings: AC-GT, AC.GT and ac-gt are kept as three distinct rows, contradicting the "Every helper below normalises its input internally" sentence.',
      root_cause='The fix added normalisation to the column helpers but not to the row-comparison helper.',
      fix='Compare str(r.seq) of normalize_alignment(alignment) rows in remove_duplicates (keep the original records), or narrow the sentence.'),
 dict(priority='P2', title='a2m_a3m_io.py fails on real HMMER A2M output', observed_in=[8],
      problem='`hmmalign --outformat a2m` (HMMER 3.4) writes unpadded rows (149-161 characters, no "." characters), so AlignIO.read(..., "fasta") raises "Sequences must all be the same length"; the docstring and SKILL.md/alignment-io describe A2M as padded.',
      root_cause='The example was written for padded (HH-suite style) A2M and only tested on the hand-made example.a2m.',
      fix='Read with SeqIO.parse (match_only_columns already accepts a list of records: 117 columns per row = profile LENG) or pad through pyhmmer MSAFile(format="a2m"), and say that HMMER writes A2M unpadded.'),
 dict(priority='P2', title='All-zero weights return an all-placeholder consensus silently', observed_in=[3],
      problem='consensus_sequence(weights=[0,0,0,0]) returns XXXXXX with only a RuntimeWarning (0/0); find_conserved_positions would return nothing.',
      root_cause='No check on weights.sum().',
      fix='Raise ValueError("weights must sum to a positive value") next to the length check in both weighted helpers.'),
 dict(priority='P2', title='SKILL.md over 500 lines; description omits weights, Neff, MI-APC, MUSCLE5', observed_in=[],
      problem='SKILL.md is 504 lines / 28.7 KB with the function bodies repeated in examples/, and the frontmatter description (unchanged) does not mention weighting, Neff, MI-APC or the MUSCLE5 column-confidence route that the body now covers.',
      root_cause='Fix added content without moving code out of SKILL.md or refreshing the trigger text.',
      fix='Point to examples/ for the longer functions (keep a signature and a one-line use), and add "sequence weights, Neff, MI-APC coevolution, MUSCLE5 column confidence" to the description.'),
 dict(priority='P2', title='Small documentation inaccuracies', observed_in=[2, 5, 6],
      problem='(a) SKILL.md sends the reader to structure-navigation for the "authoritative _pdbx_poly_seq_scheme mapping": that string is not in the Skill (it covers SEQRES/PPBuilder/auth vs label numbering). (b) "stderr ends best <name>": the line is second to last, a URL follows; muscle5_column_confidence.py with no argument dies with a bare IndexError and no usage line. (c) Biopython 1.88 writes only recognised Stockholm tags: Pfam GC seq_cons and GR pAS are dropped even from an uncleaned alignment, which the "GC ... survive read/write" sentence does not say. (d) The Cocco 2018 attribution for "APC underperforms raw MI below 100 columns" was not verified by me; on the seed both raw MI (top-30 contact precision 0.13) and MI-APC (0.00) sit near the 0.09 baseline.',
      root_cause='Prose written from memory of related Skills and one tool run.',
      fix='Name the section that exists in structure-navigation, reword (b), add the recognised-tags caveat to the annotation paragraph, and cite or soften (d).'),
]
KEY = [
 'Every defect the first audit listed is fixed and I re-verified each against independent ground truth: "." and lowercase handled, X placeholder, guard + shuffled null in mi_apc.py, Henikoff ValueError, annotations kept, weights= on both helpers.',
 'The MUSCLE5 ensemble route that replaced GUIDANCE2 runs exactly as written (MUSCLE 5.3, 8 UniProt globins and 73 Pfam sequences); the example script decodes CC digit rows to the same values as my own decode and its masked output is exact.',
 'Numbers in the prose are measured and reproducible: Neff 66.08, pb sum 73.0, hmmbuild eff_nseq 6.35, Spearman 0.909, MI-APC 0.603 vs shuffled 0.616, 0 of top-30 1MBN contacts; the Easel pb description is correct (an independent 12-line function matches pyhmmer to 7e-16).',
 'The Skill behaves on files it was not tuned to: real hmmalign Stockholm with PP/RF, real HBB CDS DNA with soft-masking, a new real family (Pfam Ras) and a planted-coupling deep alignment all equal independent answers.',
]

meta = dict(skill_name='bio-alignment-msa-parsing', description=DESC, evaluated_on='2026-09-20', evaluator_version='skill-auditor@1.0',
            category='Data Analysis', execution_mode='A', complexity='Complex', n_inputs=len(INPUTS), source=SRC,
            audit_type='re-audit of a fixed Skill (third agent, different from first auditor and fixer)', pre_fix_score=78, pre_fix_grade='Beta Only',
            regression_inputs=[1, 2, 3, 4, 5, 6, 7], new_inputs=[8, 9],
            n_inputs_note='Complex = 7 inputs by the complexity rule; 7 first-audit inputs re-run as regression plus 2 new inputs of my own = 9.',
            raw_script_assertions='196/199 passed (run/in*_output.txt + examples_noargs_output.txt); the 45 per-input assertions below are the selection scored')
JSON = dict(meta=meta,
  veto_gates=dict(skill_veto=dict(gate='PASS', stability='PASS', contract='PASS', determinism='PASS', security='PASS'),
    research_veto=dict(applicable=True, gate='PASS',
      scientific_integrity=dict(result='PASS', detail='No fabricated values in 9 inputs; every SKILL-stated number (Neff 66.08, eff_nseq 6.35, 0.603/0.616, 11 of 155 CC<0.9) reproduced. The cited references are real; the Cocco 2018 attribution for the <100-column APC statement is unverified (P2), not fabricated.'),
      practice_boundaries=dict(result='PASS', detail='No clinical or diagnostic content; sequence-analysis Skill.'),
      methodological_ground=dict(result='PASS', detail='Guard (L > 100, Neff/L > 1) now enforced in code with a shuffled null; weights and Neff labelled by estimator; raw-vs-APC caveats stated; no correlation/causation or model misuse.'),
      code_usability=dict(result='PASS', detail='25/25 SKILL.md python blocks exec without examples/; the 10 runnable shipped examples run from a copy with no arguments (all rc 0, printed content checked) and on real files (a2m example fails only on unpadded HMMER A2M, P2); every checked output equals independent ground truth.'))),
  static_score=dict(subtotal=static_sub, max=100, categories={k: dict(score=v[0], max=v[1], note=v[2]) for k, v in STATIC.items()}),
  dynamic_score=dict(execution_avg=exec_avg, max=100, assertion_pass_rate=dict(passed=tot_p, total=tot_t),
    inputs=[dict(index=i['index'], type=i['type'], label=i['label'], status=i['status'], status_flag=i['status_flag'], note=i['note'], basic=i['basic'], specialized=i['specialized'],
                 total=i['total'], assertions_passed=i['assertions_passed'], assertions_total=i['assertions_total'], assertions=i['assertions'], executed=i['executed'],
                 execution_note=f"executed: true. Script: {i['script']}. " + ('Real data; ' if i['index'] in (1, 4, 5, 6, 8) else 'Synthetic data; ') + 'outputs in run/in%d_output.txt.' % i['index'])
            for i in INPUTS]),
  final=dict(static_weighted=sw, dynamic_weighted=dw, score=score, max=100, grade=grade, grade_symbol=sym, deployable=True, veto_override=False),
  key_strengths=KEY, recommendations=REC)
json.dump(JSON, open(os.path.join(OUT, 'eval_report_bio-alignment-msa-parsing_result.json'), 'w', encoding='utf-8'), indent=2, ensure_ascii=False)

# ---------------------------------------------------------------- viewer
def excerpt(n, maxprint=22):
    ls = [l[:230] for l in out_lines(n) if l.strip()]
    prints = [l for l in ls if not l.startswith('[PASS]') and not l.startswith('[FAIL]') and not l.startswith('  FAILED') and not l.startswith('ASSERTIONS')][:maxprint]
    fails = [l for l in ls if l.startswith('[FAIL]')]
    tail = [l for l in ls if l.startswith('ASSERTIONS')]
    npass = sum(l.startswith('[PASS]') for l in ls)
    return '\n'.join(prints + fails + tail + [f'... ({npass} [PASS] lines omitted; full text in run/in{n}_output.txt)'])
M = []
w = M.append
w('# Eval Viewer - bio-alignment-msa-parsing (RE-AUDIT of the fixed Skill)')
w(f'Generated: 2026-09-20  |  Source: `{SRC}`  |  Auditor: fresh Sonnet (third agent; not the first auditor, not the fixer)\n')
w(f'**Pre-fix 78 (Beta Only, not deployable) -> {score}/100 {sym} {grade}; deployable: true.** Static {static_sub} x 0.4 = {sw}; execution {exec_avg} x 0.6 = {dw}. Skill veto PASS, research veto PASS, no open P0, no open P1, 6 P2. 9/9 inputs executed; assertions {tot_p}/{tot_t} ({tot_p / tot_t * 100:.1f}%); raw script assertions 196/199.\n')
w(f'Floors (Production Ready): static {static_sub}>=80 ok, execution {exec_avg}>=85 ok, Layer 1 avg {l1:.1f}>=32 ok, Layer 2 avg {l2:.1f}>=48 ok, assertion pass rate {tot_p / tot_t * 100:.1f}%>=90 ok. No downgrade.\n')
w('## Classification and inputs\nCategory 3 Data Analysis; Mode A (agent applies the Skill code patterns; examples/ are runnable demos); Complex -> 7 inputs. I re-ran the 7 first-audit inputs as regression (fresh scripts, the SKILL.md code exec\'d from the file, no transcription) and added 2 new inputs (8, 9) on data and structure the fixer never used. The schema lists n_inputs 1-8; 9 is used because 7 regression + 2 new is what the brief requires.\n')
w('Environment: `F:\\OpenScience\\audit-envs\\alignment\\` (Windows venv Biopython 1.88, numpy 2.0.2, pyhmmer 0.12.3; WSL `alignment` env: MAFFT 7.526, HMMER 3.4, MUSCLE 5.3, trimAl 1.5.1, ClipKIT 2.14). The Skill was copied from the worktree to `run/skill/` (byte-identical, `cmp` checked for SKILL.md, usage-guide.md and all 11 example modules) and run from there; the worktree and `external/` were never written (no `__pycache__`).\n')
w('## Step 1 - Skill Veto\nT1 stability PASS (9 inputs, 199 scripted assertions, no crash or hang; errors only where intended). T2 contract PASS (name, description, tool_type, primary_tool, license). T3 determinism PASS (no randomness except the seeded shuffled null; `mi_apc.py` printed identical output twice on the shipped example and on the Ras seed). T4 security PASS (grep of all shipped files: no eval/exec/subprocess/os.system/network; the user regex is compiled and raises `re.error` on bad input; paths come from argv).\n')
w('**Shipped-means-present:** every file the SKILL.md/usage-guide.md name exists (`examples/{a2m_a3m_io,henikoff_weights,neff,mi_apc,muscle5_column_confidence}.py`, `examples/data/`); the 8 Related Skills folders exist; alignment-io has "A2M / A3M Conventions" and "Streaming Large Stockholm Databases" and the `reformat.pl` pitfall. Not present: the string `_pdbx_poly_seq_scheme` that SKILL.md says lives in structure-navigation (P2, wording). The first-audit examples needed unshipped input files: now all 9 path-taking examples run with no arguments on `examples/data/` (`run/examples_noargs_output.txt`, 11/11).\n')
w('## Step 2 - Static (25 criteria)\n| Category | Score | Note |\n|---|---|---|')
for k, v in STATIC.items():
    w(f'| {k} | {v[0]}/{v[1]} | {v[2]} |')
w(f'| **Subtotal** | **{static_sub}/100** (first audit 76) | |\n')
w('## Summary table\n| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Executed | Status |\n|---|---|---|---|---|---|---|---|')
for i in INPUTS:
    w(f"| {i['index']}{' (NEW)' if i['index'] > 7 else ''} | {i['type']} | {i['basic']} | {i['specialized']} | {i['total']} | {i['assertions_passed']}/{i['assertions_total']} PASS | yes | {i['status_flag']} |")
w(f'\n**Execution Average: {exec_avg} / 100**  |  **Assertion pass rate: {tot_p}/{tot_t}**  |  Layer 1 avg {l1:.1f}/40, Layer 2 avg {l2:.1f}/60. Layer 2 uses the Data Analysis rubric (methodological validity /20, code executability /15, data QC /10, reproducibility /10, security /5).\n')

w('## Verification of the fix log (my runs, not the log)\n| fix-log claim | my result |\n|---|---|')
for a, b in [
 ('"." gaps and lowercase handled by every helper', 'Confirmed for 11 helpers (in3, in7, in8); FAILED for remove_duplicates (P2). Note Biopython 1.88 already converts "." to "-" when reading Stockholm, so the trap bites FASTA/A2M input, not .sto via AlignIO.'),
 ('normalize_alignment / select_columns keep annotations', 'Confirmed on real Pfam (accession/start/end, GC seq_cons, GR pAS, sliced correctly) and real hmmalign PP/RF. But quadratic in alignment length (probes/probe_scaling_output.txt): new P2.'),
 ('mi_apc.py guard + shuffled null; single Neff/L > 1 rule', 'Confirmed: warning text, raw-MI fallback, null, `force=True`; MI and APC equal independent scipy code to 5e-15 on the seed and a 400 x 120 alignment; planted pairs ranked 1-2; L=100/101 and Neff/L=0.5 boundaries; no stale "0.5" anywhere.'),
 ('protein consensus X, gap-row denominator stated', 'Confirmed (124 X / 0 N on the seed; DNA and RNA keep N; a peptide over A/C/G/T is misdetected as nucleotide but `ambiguous=` overrides).'),
 ('Henikoff/Neff prose rewritten; henikoff_weights raises', 'Confirmed: ValueError on all-gap; hand-computed weights; Spearman 0.909 / 0.0091; Neff table three rows reproduced (66.08, 73.0, 6.35). Easel pb: I could reproduce it exactly (see below).'),
 ('annotation-preserving cleaning; filters raise on empty result', 'Confirmed (in2, in7, in8).'),
 ('GUIDANCE2 replaced by a MUSCLE5 ensemble route', 'Confirmed by running MUSCLE 5.3 (in6): commands as written, CC decode independent, masked output exact. Cosmetic: the best-replicate name is second to last in stderr, not last.'),
 ('usage-guide.md dedup', 'Nothing lost: pip line -> SKILL Version block; Key Concepts -> intro conventions; annotations block and paragraph moved whole to SKILL.md (I ran it verbatim, in7); every Tips bullet is covered in SKILL.md (unreliable regions, trimming, gap handling, 0-based). usage-guide.md gained prompts for weighting/coevolution/reliability.'),
]:
    w(f'| {a} | {b} |')
w('\n**The two things the fixer left undone.** (1) *Easel-exact `pb` function*: does not matter for correctness, and I can say why. My independent 12-line function (probes/probe_pb_easel2.py: consensus columns with >= 50% residues, canonical residues only, per-sequence weight divided by its canonical-residue count in those columns, rescaled to sum N) matches pyhmmer to 7e-16, so the SKILL.md prose is exactly right and the fix log\'s "did not match" was an implementation slip, not an Easel property. The Skill correctly routes gappy alignments to pyhmmer; shipping the function would only remove that dependency (optional). (2) *Description unchanged*: a real but small trigger-precision cost (static 3/4), P2; it does not block deployment.\n')

w('## Detailed outputs\nCode: the Skill code is the SKILL.md blocks themselves, exec\'d from the file by `run/skillns.py` (25/25 ran with no examples/ on the path, `run/skillns_output.txt`), plus the shipped examples run as subprocesses from `run/skill/examples/`. Every script is in `run/`; `run/run_all.sh` re-runs all of it.\n')
for i in INPUTS:
    w(f"### Input {i['index']} - {i['type']}: {i['label']}")
    w(f"**Prompt:** {i['prompt']}\n")
    w(f"**Executed:** true. **Script:** `{i['script']}`.  **Scores:** Basic {i['basic']}/40 | Specialized {i['specialized']}/60 | Total {i['total']}/100\n")
    w(f"**Result:** {i['note']}\n")
    w('**Assertions:**')
    for a in i['assertions']:
        w(f"- [{a['result']}] {a['text']} - {a['note']}")
    w(f"\n**Output (trimmed, from `run/in{i['index']}_output.txt`):**\n```\n{excerpt(i['index'])}\n```\n")
    if i['index'] == 6:
        w('**MUSCLE 5.3 commands as run (`run/wsl_tools.sh muscle_ens8`, `muscle_ens73`; output `run/wsl_tools_output.txt`):**\n```\nmuscle -align seqs.fa -stratified -output ens.efa\nmuscle -maxcc ens.efa -output maxcc.afa        -> "CC min 148, avg 150, max 152, best acb.2" (8 globins); "best bca.2" (73 Pfam)\nmuscle -addconfseq ens.efa -output ens_cc.efa\npython examples/muscle5_column_confidence.py ens_cc.efa acb.2 0.9 masked.fa\n```\nOn the 73 Pfam sequences only 60 of 156 columns reach CC >= 0.9 (mean CC 0.617), so the example\'s 0.9 cut-off would discard 62% of a divergent family: SKILL.md says there is no calibrated cut-off and tells the user to look at the survivor table first.\n')
    if i['index'] == 8:
        w('Real HMMER 3.4 A2M: `hmmalign --outformat a2m` row lengths 161/150/151/160/149/149/149/151, zero "." characters (`run/wsl_tools_output.txt`).\n')

w('## Defects the fix introduced or left (own probes)\n- **Quadratic `select_columns`** (`run/probes/probe_scaling_output.txt`): `normalize_alignment` 0.04 s / 0.38 s / 2.0 s / 7.2 s for 10 sequences x 5k / 20k / 50k / 100k columns; pre-fix `gaps_per_column` 1.95 s at 100k. Results correct, only slow on long alignments.\n- `remove_duplicates` not normalised; all-zero weights silent; hmmalign A2M example; wording items (see Recommendations).\n- Not defects (checked): the "GC seq_cons dropped on Stockholm write" is Biopython 1.88 (uncleaned alignment loses it too, `run/probes/probe_sto_roundtrip_output.txt`); Biopython converts "." to "-" on Stockholm read.\n')
w('## Research Veto (Data Analysis)\nM1 PASS (every SKILL-stated number reproduced; references are real, one attribution unverified), M2 PASS (no clinical content), M3 PASS (guard and null in code, estimators labelled), M4 PASS (code runs; details in the JSON).\n')
w('## Recommendations\nNo P0, no P1.\n')
for r in REC:
    w(f"**[{r['priority']}] {r['title']}**  \nObserved in: {r['observed_in'] or 'static / probe'}  \nProblem: {r['problem']}  \nRoot cause: {r['root_cause']}  \nFix: {r['fix']}\n")
w('## Files\n`run/`: `common.py`, `skillns.py` (exec the SKILL.md blocks), `mkdata.py`, `in1..in9_*.py` with `in*_output.txt`, `wsl_tools.sh` (+ `wsl_tools_output.txt`: MAFFT, hmmbuild/hmmalign, trimAl/ClipKIT, MUSCLE5 ensembles), `probes/` (Easel pb, Stockholm round trip, scaling), `build_report.py`, `run_all.sh`, `skill/` (byte-identical copy of the audited Skill), `data/` (REAL: public-data inputs, EBI PF00071 seed, tool outputs; SYNTHETIC: every `syn_*` file; see `data/SOURCES.txt`).')
open(os.path.join(OUT, 'eval_viewer_bio-alignment-msa-parsing.md'), 'w', encoding='utf-8').write('\n'.join(M) + '\n')
print('score', score, grade, 'static', static_sub, 'exec', exec_avg, 'assertions', tot_p, tot_t, 'L1', round(l1, 1), 'L2', round(l2, 1))
