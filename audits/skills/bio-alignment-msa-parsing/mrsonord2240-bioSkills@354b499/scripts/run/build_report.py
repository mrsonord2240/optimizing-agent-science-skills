"""Builds eval_report_bio-alignment-msa-parsing_result.json and the eval viewer from the scores decided during the audit.
Scores are judgements recorded here; every number in `note` / assertion text comes from the in*_output.txt files in this folder."""
import json, os, re
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.dirname(HERE)
SK = 'bio-alignment-msa-parsing'
SRC = 'mrsonord2240/bioSkills@354b4992cd8d2f1bee039510af618da0333821f1:alignment/msa-parsing'

def A(t, r, n): return {'text': t, 'result': r, 'note': n}
P, Fl = 'PASS', 'FAIL'

inputs = [
 dict(index=1, type='Canonical', label='Pfam globin seed: IDs, conserved columns, gaps, consensus (real data)', status='COMPLETED', executed=True,
  prompt="Here is the Pfam globin seed alignment (PF00042, 73 sequences, Stockholm). List the sequence IDs, show me the GLB2_LUMTE record, find the fully conserved columns and the ones conserved in at least 80% of sequences, count gaps per sequence and per column, and give me a 70% consensus.",
  script='in1_canonical.py (+ shipped analyze_alignment.py, find_conserved.py, gap_analysis.py, consensus_sequence.py from a copy)', out='in1_output.txt',
  note='All SKILL.md snippets and 4 shipped examples ran on the real 73x141 Pfam seed; results equal an independent numpy/pandas implementation (2 fully conserved columns F17/H77, 3 at >=80%, 1943 gap chars counted 2 ways). Protein consensus emits 124 "N" placeholders, only 2 of which are real Asn.',
  basic=35, spec=51, executed_note='executed: true. Assertions on printed values vs independent implementation.',
  asserts=[A('Loaded shape is 73x141 and IDs/lookup (get_sequence_by_id) return the right records', P, 'shape (73,141); GLB2_LUMTE/31-141 found; missing id returns None'),
           A('find_conserved_positions equals an independent numpy/pandas count at 1.0 and 0.8', P, '[(17,F),(77,H)] and 3 columns at >=0.8 identical to independent code'),
           A('Gap counts per sequence and per column agree and equal an independent count', P, '1943 = 1943 = 1943; gap_analysis.py per-column lines sum to 1943'),
           A('Shipped examples analyze_alignment/find_conserved/gap_analysis/consensus_sequence run from a copy and print the verified values', P, 'rc=0, stderr empty; consensus in output equals independent consensus'),
           A('Protein consensus uses a placeholder that cannot be confused with a residue', Fl, "default ambiguous='N' is asparagine: 124 'N' in the 0.5 consensus, only 2 columns have Asn as the plurality residue")]),
 dict(index=2, type='Variant A', label='Clean: gappy columns, gappy/duplicate sequences, ID filter, save', status='COMPLETED', executed=True,
  prompt="Clean this alignment: drop columns that are 50% gaps or more, drop sequences with more than 20% gaps, remove exact duplicates, keep only IDs starting with GLB, and save the cleaned alignment.",
  script='in2_cleaning.py (+ shipped clean_alignment.py from a copy)', out='in2_output.txt',
  note='Real Pfam seed: 141 -> 118 columns identical to an independent mask; synthetic 5x12 alignment with hand-computed gap counts matches. Cleaning silently drops all per-record and column annotations; a 0.1 gap filter keeps 0 of 73 sequences and returns an empty alignment with no message.',
  basic=34, spec=49, executed_note='executed: true.',
  asserts=[A('remove_gappy_columns(0.5) keeps exactly the columns an independent numpy mask keeps, with identical content', P, '118 columns, all 73 rows equal arr[:, keep]'),
           A('Sequence filters (gap fraction, duplicates, regex ID) return the same IDs as independent code and hand-known synthetic answers', P, 'species_E dropped as duplicate of A; 44 of 73 kept at 0.2; ^GLB -> 32'),
           A('Shipped clean_alignment.py output equals the independent pipeline (column trim then sequence filter)', P, '73 x 118, same IDs'),
           A('Cleaning preserves record/column annotations (accession, start, end, GC seq_cons)', Fl, 'after: annotations {} and column_annotations {} (before: 3 keys and GC:seq_cons)'),
           A('An over-strict filter that empties the alignment is reported to the user', Fl, 'filter_by_gap_content(0.1) on the real seed keeps 0 of 73; returns an empty alignment silently')]),
 dict(index=3, type='Edge', label="Messy files: all-gap column, single sequence, ragged, A2M '.' gaps, A3M", status='COMPLETED', executed=True,
  prompt="Some of my alignment files are messy: an HMMER/hhsearch A2M with lowercase inserts and '.' gaps, an alignment with an all-gap column, a single-sequence file, a ragged file and a ColabFold A3M. Give me match-only columns and a consensus without it blowing up.",
  script='in3_edge.py (+ shipped a2m_a3m_io.py from a copy)', out='in3_output.txt',
  note="Synthetic data. All-gap column, single sequence, ragged error, A2M match-only extraction (hand-known 9 match columns, inserts 0/2/1) and A3M-must-be-reformatted all behave as documented. Every function recognises only '-' as a gap: on '.'-gapped input gaps_per_column returns all zeros, coordinate_map counts '.' as residues and consensus emits '.'.",
  basic=33, spec=43, executed_note='executed: true. Data synthetic (syn_*.fasta/.a2m/.a3m).',
  asserts=[A('All-gap column: consensus keeps "-" (AC-G), is not reported conserved, and is removed by remove_gappy_columns', P, 'consensus AC-G; 3 columns after removal'),
           A('Single-sequence alignment loads and consensus reproduces it', P, '1x6, consensus ACDE-G'),
           A('Shipped a2m_a3m_io.py gives the hand-known result (3 seq x 11 cols -> 9 match columns; inserts 0, 2, 1)', P, "match_only_columns == ['ACDEFGHIK','AC-EFGHIK','ACDEFG-IK']"),
           A('Ragged and unpadded A3M inputs fail loudly (Common Errors / A2M-A3M section)', P, 'ValueError: Sequences must all be the same length; pyhmmer MSAFile(format=a2m) pads the A3M so the hand-off works'),
           A("'.' gap characters (HMMER/A2M convention) are treated as gaps by the snippets", Fl, "gaps_per_column=[0]*6 instead of [0,0,2,2,0,0]; coordinate_map len 6 not 4; consensus 'AC..GT'")]),
 dict(index=4, type='Variant B', label='Map proximal His of myoglobin (PDB 1MBN) to an alignment column', status='COMPLETED', executed=True,
  prompt="In my 8-globin alignment, which column is the proximal histidine of sperm whale myoglobin (PDB 1MBN His93), what residue does every other globin have there, and how do I convert between column numbers and residue numbers?",
  script='in4_mafft.sh (MAFFT L-INS-i in WSL) + in4_position_map.py', out='in4_output.txt',
  note='Real UniProt globins aligned with MAFFT, ground truth from real PDB 1MBN coordinates (Bio.PDB). coordinate_map round-trips for all 8 sequences and equals a loop-based walk; PDB residue 93 = UniProt index 93 (initiator Met offset) maps to column 94 where all 8 globins have His (also fully conserved per find_conserved_positions).',
  basic=36, spec=54, executed_note='executed: true. MAFFT 7.526 in WSL; Windows Python for analysis.',
  asserts=[A('coordinate_map: ungapped == original UniProt sequence, seq->aln->seq round-trips, gap columns are -1, for all 8 records', P, '8/8 records'),
           A('Vectorised map equals the loop-based walk the SKILL describes for single lookups', P, 'identical for MYG_PHYMC'),
           A('Ground truth: PDB 1MBN residue 93 is HIS and maps to the column where all 8 globins have His', P, 'column 94, {H} in 8/8; distal His64 -> column 65 also His'),
           A('PDB-numbering offset is real and the correct route lands on His while the naive 1-based route does not', P, '1MBN starts at UniProt residue 2; index 92 is Ser, index 93 is His'),
           A('Skill function find_conserved_positions agrees with the structure (proximal His column is fully conserved)', P, "(94,'H') in the fully conserved list")]),
 dict(index=5, type='Stress', label='Henikoff weights, Neff/L, MI-APC on the Pfam seed', status='COMPLETED', executed=True,
  prompt="Compute Henikoff sequence weights for the Pfam globin seed, report Neff and Neff/L at 62% and 80% identity, and find the top coevolving column pairs with MI-APC.",
  script='in5_weights_neff_mi.py, in5b_examples_main.py, in5_hmmbuild.sh (+ shipped henikoff_weights.py, neff.py, mi_apc.py)', out='in5_output.txt',
  note='Numerics exact vs independent code (weights diff 0.0, Neff 66.08/73.00, MI-APC diff 5e-15), all 3 examples exit 0. But mi_apc.py prints "top coevolving pairs" with no caveat when Neff/L=0.47 (the Skill says skip APC below 1): top score 0.603 vs 0.616 for a column-shuffled null, 0/30 top pairs are 1MBN contacts (baseline 0.11). Henikoff returns NaN when every column has a gap. Neff table conflates weights (sum to N=73) with Neff; hmmbuild eff_nseq is 6.35 vs skill Neff 66.08.',
  basic=30, spec=42, executed_note='executed: true. Ground truth: pyhmmer/Easel weights, scipy entropy, hmmbuild 3.4 (WSL), real PDB 1MBN contacts.',
  asserts=[A('Henikoff weights equal an independent textbook implementation (sum to 1, no zero weights)', P, 'max abs diff 0.0; Spearman 0.909 vs Easel PB weights'),
           A('neff() and mi_matrix_apc() equal independent implementations, and the three shipped __main__ blocks run with correct printed values', P, 'Neff 66.08 / 73.00 vs 66.0833 / 73.0; MI-APC max diff 5.3e-15; 73 weight lines sum 1.0000'),
           A("Skill's own guard (APC only when L>100 and Neff/L>1) is enforced or warned in mi_apc.py output", Fl, 'Neff/L=0.469 yet prints 20 "coevolving" pairs; top 0.603 < shuffled-null max 0.616; contact precision 0.00 vs baseline 0.11'),
           A('Henikoff weights return finite values or a clear error when every column contains a gap', Fl, 'weights [nan nan nan nan] with only a RuntimeWarning'),
           A('Skill claims about HMMER pb equivalence and estimator spread hold', Fl, 'Easel PB max diff 0.0091 vs skill weights (docstring says it matches); hmmbuild eff_nseq 6.35 vs Neff 66.08 = 10.4x, not "2-3x"')]),
 dict(index=6, type='Scope Boundary', label='Trimming/reliability routing claims and pyhmmer streaming', status='COMPLETED', executed=True,
  prompt="Trim this alignment for tree building and separately for HMM building, keep the original column numbers, mask unreliable columns with GUIDANCE2, then stream the file with pyhmmer weights.",
  script='in6_wsl.sh (trimAl, ClipKIT, muscle help in WSL) + in6_scope_trimming.py', out='in6_output.txt',
  note='Skill only routes to alignment-trimming; the routed claims were run on the real seed. trimAl -gappyout -colnumbering mapping is exact (103 of 141 columns); ClipKIT kpic-smart-gap valid (121 of 141); MUSCLE5 ensemble flags exist; pyhmmer MSAFile streaming + compute_weights(method="pb") works. GUIDANCE2 (recommended twice, threshold 0.93) is not obtainable so that part was NOT executed; version block omits pyhmmer.',
  basic=34, spec=46, executed_note='executed: true for everything except GUIDANCE2 (not executed: package unobtainable, TOOLS.md Blocked).',
  asserts=[A('trimAl -colnumbering map reproduces the trimmed alignment from original columns (0-based, correct)', P, '103 map entries; every trimmed row == original columns at mapped indices'),
           A('ClipKIT kpic-smart-gap (decision-matrix first-line tool for trees) is a valid mode with sane output', P, '121 of 141 kept, 14.2% trimmed, 73 sequences'),
           A("pyhmmer streaming pattern (iterate MSAFile, compute_weights(method='pb')) works", P, '[(73,73.0),(73,73.0)] on a 2-alignment Stockholm file'),
           A('GUIDANCE2 column masking, recommended twice with a 0.93 threshold, can actually be run', Fl, 'NOT executed: distribution URL now serves an HTML page; the Skill gives no install path or alternative command'),
           A('Version block lists every library needing a minimum version (pyhmmer compute_weights needs >= 0.11.3)', Fl, 'Version Compatibility mentions only BioPython 1.83+ and numpy 1.26+')]),
 dict(index=7, type='Adversarial', label='Annotations, soft-masked DNA consensus, user regex', status='COMPLETED', executed=True,
  prompt="Pull the secondary structure and RF annotation out of my Stockholm alignment and keep it after cleaning; also give me the consensus of my soft-masked (mixed-case) DNA alignment, and filter sequences with this regex I typed: '['.",
  script='in7_adversarial.py', out='in7_output.txt',
  note="Synthetic data. The usage-guide annotation snippet is correct on Biopython 1.88 (keys 'secondary_structure', column 'secondary_structure'); Stockholm round-trip keeps GC/GR/GS; a malformed regex raises re.error. Failures: cleaning then writing Stockholm drops all GC/GR lines; consensus/conservation are case-sensitive (mixed-case DNA gives ACGTNNNN and 0/8 conserved columns); SummaryInfo is said to be 'deprecated' but its methods are gone in 1.88; 'weight before any column-wise statistic' is not actionable because no function accepts weights.",
  basic=31, spec=41, executed_note='executed: true. Data synthetic (syn_annot.sto, syn_dna_mixedcase.fasta).',
  asserts=[A("usage-guide 'Working with Annotations' snippet, run verbatim, returns SS per record and SS_cons", P, "printed [('seqA','HHHEEEC'),('seqB','HHH-EEC')]; column SS_cons 'HHHEEEC'"),
           A('Stockholm write/read round trip keeps GC (SS_cons, RF), GR SS and GS organism; FASTA write drops them (documented behaviour)', P, 'round trip identical; FASTA text has no annotation'),
           A('Malformed user regex given to filter_by_id fails with a clear error rather than an empty alignment', P, 're.error: unterminated character set at position 0'),
           A('Consensus and conservation are case-insensitive for soft-masked DNA', Fl, "consensus@0.7 'ACGTNNNN'; find_conserved_positions(1.0) reports 0 of 8 unanimous columns"),
           A("SKILL guidance 'compute sequence weights before any column-wise statistic' is actionable with the shipped functions", Fl, 'no function among find_conserved_positions/consensus_sequence/gaps_per_column accepts weights')]),
]

for i in inputs:
    i['total'] = i['basic'] + i['spec']
    i['passed'] = sum(1 for a in i['asserts'] if a['result'] == P)
    assert 3 <= len(i['asserts']) <= 5

static_cats = {
 'functional_suitability': (9, 12, "Completeness 3, Correctness 3, Appropriateness 3. Core primitives match independent implementations; gaps recognised only as '-', no case handling, no weighted statistics; prose errors on HMMER pb gap handling and the Neff estimator table; protein consensus placeholder 'N' is Asn."),
 'reliability': (7, 12, "Fault tolerance 2, Error reporting 2, Recoverability 3. Relies on Biopython errors; silent wrong answers on '.' gaps, NaN from Henikoff, empty alignments after filtering; functions are pure and never mutate input."),
 'performance_context': (6, 8, "Token cost 3, Efficiency 3. SKILL.md is 454 lines with full code duplicated in examples/; MI-APC and Neff use python pair loops (1.5 s and 0.1 s at 73x141)."),
 'agent_usability': (11, 16, "Learnability 3, Consistency 2, Feedback 3, Error prevention 3. Goal/Approach blocks are clear; SKILL.md and examples disagree (find_conserved variants, HMMER-weight statements, Neff/L 0.5 vs 1, fifth-state advice); good pitfall callouts (APC over-correction, PDB numbering, Neff estimator)."),
 'human_usability': (5, 8, "Discoverability 3, Forgiveness 2. Natural trigger phrasing and example prompts; strict '-' only handling with no normalisation or warning."),
 'security': (11, 12, "Credential safety 4, Input validation 3, Data safety 4. No secrets or network; user regex is compiled unvalidated (raises re.error); no eval/exec."),
 'maintainability': (9, 12, "Modularity 3, Modifiability 3, Testability 3. Independent functions and per-task examples; every function is duplicated in SKILL.md and examples and has already drifted; examples read alignment.fasta / hhsearch_output.a2m that are not shipped."),
 'agent_specific': (18, 20, "Trigger 3, Progressive disclosure 3, Composability 4, Idempotency 4, Escape hatches 4. Description omits weights/Neff/MI-APC; all 7 Related Skills paths resolve; clear hand-offs (trimming, PDB mapping, plmDCA, pyhmmer)."),
}
static_total = sum(v[0] for v in static_cats.values())
assert static_total == 76, static_total
ex_avg = round(sum(i['total'] for i in inputs) / len(inputs), 1)
sw = round(static_total * 0.4, 1); dw = round(ex_avg * 0.6, 1); score = int(round(sw + dw))
apass = sum(i['passed'] for i in inputs); atot = sum(len(i['asserts']) for i in inputs)
l1 = sum(i['basic'] for i in inputs) / 7; l2 = sum(i['spec'] for i in inputs) / 7
print('static', static_total, 'exec avg', ex_avg, 'sw', sw, 'dw', dw, 'score', score, 'assert', apass, atot, round(apass / atot, 3), 'L1', round(l1, 1), 'L2', round(l2, 1))
grade_by_score = 'Production Ready' if score >= 85 else 'Limited Release' if score >= 75 else 'Beta Only' if score >= 60 else 'Reject'
floors = {'static>=70 (LR)': static_total >= 70, 'exec>=75 (LR)': ex_avg >= 75, 'L1>=28 (LR)': l1 >= 28, 'L2>=42 (LR)': l2 >= 42, 'assert>=80% (LR)': apass / atot >= 0.80}
print('floors', floors, 'grade by score', grade_by_score)
order = ['Production Ready', 'Limited Release', 'Beta Only', 'Reject']
grade = grade_by_score
if not all(floors.values()):
    grade = order[min(order.index(grade_by_score) + 1, 3)]
sym = {'Production Ready': '\u2b50', 'Limited Release': '\u2705', 'Beta Only': '\u26a0\ufe0f', 'Reject': '\u274c'}[grade]
deployable = grade in ('Production Ready', 'Limited Release')
print('final grade', grade, 'deployable', deployable)

recs = [
 dict(priority='P1', title="Gap symbol hard-coded to '-'; '.' and lowercase break every helper silently", observed_in=[3, 7],
      problem="On '.'-gapped input (hmmalign/A2M) gaps_per_column returns zeros, coordinate_map treats '.' as residues (len 6 instead of 4) and consensus emits '.'; on soft-masked DNA consensus gives ACGTNNNN and find_conserved_positions reports 0 of 8 unanimous columns.",
      root_cause="All snippets compare against the literal '-' and use case-sensitive Counter without a normalisation step.",
      fix="Add a documented normalize_alignment() step (replace '.' with '-', optionally upper-case) that every snippet and example calls, or accept gap_chars and case_sensitive arguments; assert on a '.'-gapped synthetic file."),
 dict(priority='P1', title='mi_apc.py ignores the Skill\'s own APC guard; output is noise on the shipped test case', observed_in=[5],
      problem="On the real Pfam seed (L=141, Neff/L=0.47) mi_apc.py prints 20 'coevolving column pairs' with no caveat; the top score (0.603) is below a column-shuffled null (0.616) and 0/30 top pairs are contacts in 1MBN (baseline 0.11). Thresholds also disagree: SKILL.md Neff section and neff.py say Neff/L > 0.5, the APC section says Neff/L > 1.",
      root_cause='Guard exists only in prose; the example applies APC unconditionally and the DCA threshold is stated two ways.',
      fix='Compute Neff inside mi_apc.py main, print a warning and return raw MI (or refuse) when L<=100 or Neff/L<=1, unify the Neff/L threshold across SKILL.md and neff.py, and add a shuffled-column null to the example.'),
 dict(priority='P1', title="Protein consensus default 'N' is asparagine", observed_in=[1],
      problem="consensus_sequence(ambiguous='N') on the real 73-globin seed returns 124 'N' at 0.5, of which only 2 are true Asn-plurality columns, so the consensus cannot be read as a protein sequence. The shipped consensus_sequence.py uses the same default.",
      root_cause="Default placeholder was chosen for nucleotides and the function is not alphabet-aware.",
      fix="Default to 'X' for protein (detect alphabet or add an alphabet argument), keep 'N' for DNA, and state that the threshold denominator includes gap rows."),
 dict(priority='P1', title='Henikoff/Neff prose contradicts itself and Easel; NaN on all-gappy alignments', observed_in=[5],
      problem="SKILL.md says HMMER pb 'includes gaps as a residue type'; the example docstring says it 'restricts to ungapped columns'; pyhmmer docs say pb ignores gaps, uses consensus columns and double-normalises by length (skill vs Easel max diff 0.0091, Spearman 0.909). Easel pb/blosum weights sum to N (73) so they are not an Neff, yet the Neff table uses pb as 'baseline'; hmmbuild eff_nseq is 6.35 vs 66.08 (10x, not '2-3x'). henikoff_weights returns NaN when every column has a gap.",
      root_cause='Estimator descriptions were written from memory and never checked against pyhmmer output.',
      fix="Rewrite the Henikoff edge-case and Neff-estimator paragraphs from pyhmmer's documented behaviour, state that compute_weights() outputs sum to N, add a guard raising ValueError when no gap-free column exists, and give one runnable pyhmmer comparison snippet."),
 dict(priority='P2', title='Cleaning helpers silently drop annotations and can return empty alignments', observed_in=[2, 7],
      problem="remove_gappy_columns rebuilds SeqRecords without annotations/letter_annotations/column_annotations, so writing Stockholm afterwards loses GC/GR lines; filter_by_gap_content(0.1) on the real seed returns 0 of 73 without any message.",
      root_cause='New SeqRecord objects carry only id and description; no post-filter size check.',
      fix='Slice records (record[i:j] style or copy annotations) or note the loss next to the code; raise/print when a filter removes every sequence.'),
 dict(priority='P2', title='GUIDANCE2 recommended twice but no longer installable; pyhmmer minimum version missing', observed_in=[6],
      problem='GUIDANCE2 (0.93 threshold) is named in unreliable-region step 3 and the trimming matrix; its download URL now returns an HTML page. compute_weights needs pyhmmer >= 0.11.3 but the version block lists only BioPython and numpy. SummaryInfo is called deprecated while its methods are removed in 1.88.',
      root_cause='External-tool advice and version block not re-verified.',
      fix='Give the MUSCLE5 route as the runnable command (muscle -align in.fa -stratified -output ens.efa; muscle -letterconf ens.efa -ref aln.afa -output conf.afa, both verified to exist in 5.3), add pyhmmer>=0.11.3 to the version block, say SummaryInfo methods are removed.'),
 dict(priority='P2', title='Duplicated code has drifted; weighting guidance not actionable; unverified estimator claims', observed_in=[1, 7],
      problem="Every function is duplicated in SKILL.md and examples/ (dedup per doctrine); find_conserved differs between the two; 'compute weights before any column-wise statistic' but no statistic accepts weights; gap-handling advice says prefer SIC 'or fifth-state' right after calling fifth-state biologically problematic; AlphaFold2 'unweighted cluster count at 62%' ratio table is unsourced.",
      root_cause='Prose and example scripts maintained separately.',
      fix='Keep one copy (import from examples/ or trim SKILL.md to signatures), add a weights= argument to the conservation/consensus helpers, fix the contradictory sentence, and source or remove the unsupported table rows.'),
 dict(priority='P2', title='Examples need input files that are not shipped; position-numbering ambiguity', observed_in=[3, 4],
      problem="Examples read alignment.fasta and hhsearch_output.a2m that the Skill does not ship (all 9 ran only after supplying data); the docs name seq_to_aln[42] 'column_for_residue_42' although it is the 43rd residue (0-based); the PDB numbering offset (1MBN is UniProt index n = residue n) is real but only referenced.",
      root_cause='Examples are illustrative fragments without fixtures.',
      fix='Ship a tiny FASTA and A2M under examples/data, take the path as argv, and add a one-line note that PDB numbers are offset from UniProt (checked: 1MBN His93 = UniProt 94).'),
]

meta = dict(skill_name=SK, description='Parse and analyze multiple sequence alignments using Biopython. Extract sequences, identify conserved regions, analyze gaps, work with annotations, and manipulate alignment data for downstream analysis.',
            evaluated_on='2026-09-19', evaluator_version='skill-auditor@1.0', category='Data Analysis', execution_mode='A', complexity='Complex', n_inputs=7,
            source=SRC, executed_inputs='7/7 (input 6 executed except the GUIDANCE2 step)',
            environment='Windows venv Biopython 1.88 / pyhmmer 0.12.3 / clipkit 2.14.0; WSL env alignment: MAFFT 7.526, HMMER 3.4, trimAl 1.5.1, MUSCLE 5.3. Real data: Pfam PF00042 seed, 8 UniProt globins, PDB 1MBN. See F:/OpenScience/audit-envs/alignment/TOOLS.md')
report = {
 'source': SRC,
 'meta': meta,
 'veto_gates': {
  'skill_veto': {'gate': 'PASS', 'stability': 'PASS', 'contract': 'PASS', 'determinism': 'PASS', 'security': 'PASS'},
  'research_veto': {'applicable': True, 'gate': 'PASS',
   'scientific_integrity': {'result': 'PASS', 'detail': 'No fabricated identifiers or results across 7 inputs; cited references (Henikoff 1994, Dunn 2008, Ekeberg 2013, Hopf 2017, etc.) are real. Two estimator claims are unsupported or wrong (AlphaFold2 62% gating table, HMMER pb gap handling) and are P1/P2 defects, not fabrication.'},
   'practice_boundaries': {'result': 'PASS', 'detail': 'Sequence-analysis skill; no diagnostic, prescriptive or individual-level content in any output.'},
   'methodological_ground': {'result': 'PASS', 'detail': 'Skill text itself warns about APC on short/shallow alignments, Neff estimator dependence and gap treatment. The shipped mi_apc.py does not enforce that guard (P1) but no output asserted a wrong scientific conclusion.'},
   'code_usability': {'result': 'PASS', 'detail': 'All SKILL.md functions and all 9 shipped examples ran from a copy with correct printed values checked against independent implementations; only GUIDANCE2 (an external tool, no code shown) could not be run.'}}},
 'static_score': {'subtotal': static_total, 'max': 100, 'categories': {k: {'score': v[0], 'max': v[1], 'note': v[2]} for k, v in static_cats.items()}},
 'dynamic_score': {'execution_avg': ex_avg, 'max': 100, 'assertion_pass_rate': {'passed': apass, 'total': atot},
  'inputs': [dict(index=i['index'], type=i['type'], label=i['label'], status=i['status'], status_flag=('\u2705' if i['total'] >= 75 else '\u26a0\ufe0f'),
                  note=i['note'], executed=i['executed'], execution_note=i['executed_note'] + ' Script: ' + i['script'] + '.', prompt=i['prompt'],
                  basic=i['basic'], specialized=i['spec'], total=i['total'], assertions_passed=i['passed'], assertions_total=len(i['asserts']), assertions=i['asserts']) for i in inputs]},
 'final': {'static_weighted': sw, 'dynamic_weighted': dw, 'score': score, 'max': 100, 'grade': grade, 'grade_symbol': sym, 'deployable': deployable, 'veto_override': False,
           'grade_note': f'Numeric score {score} maps to {grade_by_score}; assertion pass rate {apass}/{atot} = {apass / atot:.1%} is below the 80% Limited Release floor, so the grade drops one tier per scoring_rubric section 5. Static 76 (>=70), execution average {ex_avg} (>=75), Layer 1 avg {l1:.1f} (>=28) and Layer 2 avg {l2:.1f} (>=42) all meet the Limited Release floors. No P0 and no veto.'},
 'key_strengths': [
  'Every core primitive (conserved columns, gaps, consensus, coordinate_map, Henikoff, Neff, MI-APC) matched an independent implementation exactly on the real Pfam PF00042 seed; coordinate_map also checked against real PDB 1MBN residue numbering.',
  'Honest, useful cautions in prose: APC over-correction on short alignments, Neff estimator dependence, PDB SEQRES/ATOM offset, gap-treatment tradeoffs; routing claims to alignment-trimming (trimAl -colnumbering, ClipKIT kpic-smart-gap, MUSCLE5 ensemble flags) all verified by running the tools.',
  'All 9 shipped examples run from a copy; all 7 Related Skills paths and the alignment-io cross-references exist; pyhmmer streaming pattern and Stockholm annotation snippet are correct on Biopython 1.88 / pyhmmer 0.12.',
 ],
 'recommendations': recs,
}
json.dump(report, open(os.path.join(OUT, f'eval_report_{SK}_result.json'), 'w', encoding='utf-8', newline='\n'), ensure_ascii=False, indent=2)

# ---- checklist ----
r = report
assert len(r['static_score']['categories']) == 8 and r['static_score']['subtotal'] == sum(c['score'] for c in r['static_score']['categories'].values())
assert all(0 <= c['score'] <= c['max'] for c in r['static_score']['categories'].values())
assert len(r['dynamic_score']['inputs']) == r['meta']['n_inputs'] == 7
for i in r['dynamic_score']['inputs']:
    assert 3 <= len(i['assertions']) <= 5 and i['assertions_passed'] == sum(a['result'] == 'PASS' for a in i['assertions']) and i['basic'] + i['specialized'] == i['total']
assert r['dynamic_score']['execution_avg'] == round(sum(i['total'] for i in r['dynamic_score']['inputs']) / 7, 1)
assert 2 <= len(r['key_strengths']) <= 5
assert [x['priority'] for x in recs] == sorted(x['priority'] for x in recs)
print('checklist OK')

# ---- viewer ----
def excerpt(fn, n=40):
    t = open(os.path.join(HERE, fn), encoding='utf-8').read().splitlines()
    t = [l[:230] for l in t]
    return '\n'.join(t[:n]) + (f'\n... ({len(t) - n} more lines in run/{fn})' if len(t) > n else '')
L = []
L.append(f'# Eval Viewer - {SK}\nGenerated: 2026-09-19  |  Source: `{SRC}`  |  Auditor: fresh Sonnet (audit stage, first audit)\n')
L.append(f"**Final score {score}/100 (static {static_total} x 0.4 = {sw}; execution {ex_avg} x 0.6 = {dw}); numeric band {grade_by_score}; grade after floors: {sym} {grade}; deployable: {str(deployable).lower()}; skill veto PASS, research veto PASS, no P0.**\n")
L.append(f"Floors (Limited Release): static {static_total}>=70 ok, execution {ex_avg}>=75 ok, Layer 1 avg {l1:.1f}>=28 ok, Layer 2 avg {l2:.1f}>=42 ok, **assertion pass rate {apass}/{atot} = {apass / atot:.1%} < 80% FAILS** -> one tier down. The only thing keeping this from Limited Release is the assertion floor.\n")
L.append('## Classification\nCategory 3 Data Analysis; execution mode A (agent applies the Skill code patterns; examples are demo scripts, not a CLI); complexity Complex (many task types, 9 examples, hand-offs to 6 other Skills) -> 7 inputs. Environment: `F:\\OpenScience\\audit-envs\\alignment\\TOOLS.md` (Biopython 1.88, pyhmmer 0.12.3, WSL MAFFT/HMMER/trimAl/MUSCLE).\n')
L.append('## Step 1 - Skill Veto\nT1 stability PASS (no crash across 122 scripted assertions, 9 examples). T2 contract PASS (name, description, tool_type, primary_tool, license). T3 determinism PASS (no randomness; MI/Neff/weights reproduce exactly). T4 security PASS (no eval/exec, no network; user regex compiled but raises re.error on bad input).\n')
L.append('**Shipped-means-present:** `usage-guide.md`, `examples/henikoff_weights.py`, `neff.py`, `mi_apc.py` exist; Related Skills `alignment/{multiple-alignment,alignment-io,pairwise-alignment,msa-statistics,alignment-trimming,structural-alignment}`, `phylogenetics/modern-tree-inference`, `structural-biology/structure-navigation` exist; alignment-io has the "A2M / A3M Conventions" and "Streaming Large Stockholm Databases" sections. No missing primary file. Not shipped: the example input files (alignment.fasta, hhsearch_output.a2m) - P2. `__pycache__` check of the clone: none.\n')
L.append('## Step 2 - Static (25 criteria)\n| Category | Score | Note |\n|---|---|---|')
for k, v in static_cats.items(): L.append(f'| {k} | {v[0]}/{v[1]} | {v[2]} |')
L.append(f'| **Subtotal** | **{static_total}/100** | |\n')
L.append('## Summary table\n| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Executed | Status |\n|---|---|---|---|---|---|---|---|')
for i in inputs:
    flag = '\u2705' if i['total'] >= 75 else '\u26a0\ufe0f'
    L.append(f"| {i['index']} | {i['type']} | {i['basic']} | {i['spec']} | {i['total']} | {i['passed']}/{len(i['asserts'])} | yes | {flag} |")
L.append(f'\n**Execution Average: {ex_avg} / 100**  |  **Assertion pass rate: {apass}/{atot}**  |  Layer 1 avg {l1:.1f}/40, Layer 2 avg {l2:.1f}/60\n')
L.append('Layer 2 uses the Data Analysis rubric (methodological validity /20, code executability /15, data QC /10, reproducibility /10, security /5). Raw script assertions (all `[PASS]`/`[FAIL]` lines in `run/in*_output.txt`): 102 pass, 20 fail; the 35 assertions in the JSON are the per-input selection (3 core-function checks + 2 edge/claim checks).\n')
L.append('## Detailed outputs\n')
for i in inputs:
    L.append(f"### Input {i['index']} - {i['type']}: {i['label']}\n**Prompt:** {i['prompt']}\n\n**Executed:** {i['executed_note']}  **Script:** `{i['script']}`\n\n**Scores:** Basic {i['basic']}/40 | Specialized {i['spec']}/60 | Total {i['total']}/100\n\n**Result:** {i['note']}\n")
    L.append('**Assertions:**')
    for a in i['asserts']: L.append(f"- [{a['result']}] {a['text']} - {a['note']}")
    L.append(f"\n**Output (trimmed, from `run/{i['out']}`):**\n```\n{excerpt(i['out'], 34)}\n```\n")
    if i['index'] == 5:
        L.append(f"**Shipped `__main__` blocks (`run/in5b_output.txt`):**\n```\n{excerpt('in5b_output.txt', 30)}\n```\n")
    if i['index'] == 6:
        L.append(f"**WSL tool output (`run/in6_wsl_output.txt`):**\n```\n{excerpt('in6_wsl_output.txt', 30)}\n```\n")
L.append('## Research Veto (Data Analysis)\nM1 PASS, M2 PASS, M3 PASS, M4 PASS (details in the JSON). Not-run item: GUIDANCE2.\n')
L.append('## Recommendations')
for x in recs:
    L.append(f"**[{x['priority']}] {x['title']}**  \nObserved in: {x['observed_in']}  \nProblem: {x['problem']}  \nRoot cause: {x['root_cause']}  \nFix: {x['fix']}\n")
L.append('## Files\n`run/` holds every script (common.py, skill_md_funcs.py = verbatim SKILL.md functions checked against SKILL.md by in1, mkdata.py, probe1.py, in1..in7, in5b, build_report.py, .sh files) and `run/data/` (real: pfam_PF00042_seed_from_real.fasta, globins8_mafft_linsi.fasta, trimAl/ClipKIT outputs, hmmbuild_out.txt, pf.hmm; SYNTHETIC: every `syn_*` file and hhsearch_output.a2m). Real inputs live in `F:\\OpenScience\\audit-envs\\alignment\\public-data\\msa` and `...\\structures\\1MBN.pdb`.\n')
open(os.path.join(OUT, f'eval_viewer_{SK}.md'), 'w', encoding='utf-8', newline='\n').write('\n'.join(L))
print('written')
