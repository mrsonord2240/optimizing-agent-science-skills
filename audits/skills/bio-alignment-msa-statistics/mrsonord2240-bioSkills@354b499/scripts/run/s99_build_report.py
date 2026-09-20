"""Build eval_report_bio-alignment-msa-statistics_result.json (schema: skill-auditor/references/report_json_schema.md) and run the
Pre-Emit Checklist as asserts. All numbers come from the run/ outputs (out_s*.txt, results_*.json)."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.dirname(HERE)
P, F = 'PASS', 'FAIL'
A = lambda t, r, n: dict(text=t, result=r, note=n)

static = {
 'functional_suitability': (8, 12, 'Covers identity (PID1-4), conservation, entropy/IC, gaps, SP, PSSM, Capra-Singh JSD, Kimura and substitution counts; every number is correct on clean uppercase input (verified vs independent implementations). Gaps: "substitution matrices" in the description are only raw pair counts (usage-guide promises "Build a substitution matrix"); PID1 code contradicts its stated definition; alignment_score charges gap/gap pairs; IC blows up on unknown letters; Ti/Tv printed for protein.'),
 'reliability': (5, 12, 'No handling of lowercase, "." gaps or IUPAC/ambiguity letters: MAFFT nucleotide default output (lowercase) gives Ti/Tv 0.00 instead of 1.21 and IC 29.9 bits; all-gap sequence reports 0% identity; failures are silent. Common Errors table is stale (ZeroDivisionError never raised; "Negative IC / wrong alphabet size" does not apply to the KL formula). Stateless and re-runnable.'),
 'performance_context': (6, 8, 'SKILL.md is 450 lines with stubs pointing to examples/ (good); large prose on PID definitions. Vectorised identity matrix takes 66 s for 2000 x 300; SP over 300 seqs 28 s: acceptable.'),
 'agent_usability': (10, 16, 'Goal/Approach headers and pick-a-method tables are clear. Inconsistent semantics: gap/gap pairs are penalised in alignment_score but skipped in sum_of_pairs; text recommends PID4 but identity_matrix.py implements PID1; frontmatter primary_tool Bio.Align while all code uses Bio.AlignIO and MultipleSeqAlignment-only methods. No warnings for the most common real-world traps (case, dots, ambiguity, DNA vs protein).'),
 'human_usability': (4, 8, 'Description and usage-guide prompts are natural. Off-spec input (lowercase, dots, ambiguity codes) is neither rejected nor handled: it silently yields wrong numbers.'),
 'security': (10, 12, 'No credentials, no eval/exec, read-only file access. No input validation of alphabet or alignment shape beyond what Biopython raises.'),
 'maintainability': (8, 12, 'One SKILL.md plus 8 focused example scripts, all present. ROBINSON_BACKGROUND is copy-pasted in 3 example files and SKILL.md (values differ from published Robinson table by up to 5% relative; sum 1.0036); two divergent pairwise_identity definitions. No shipped expected outputs or tests.'),
 'agent_specific': (16, 20, 'Trigger is reasonable though it overlaps msa-parsing (conservation, gaps). Progressive disclosure good (450 lines, stubs to examples/). Cross-references to msa-parsing (henikoff_weights.py, neff.py, mi_apc.py), multiple-alignment, phylogenetics/* all exist. Read-only and deterministic. Twilight-zone table and ModelTest-NG hand-off are good escape hatches; no stop condition for wrong alphabet.'),
}
subtotal = sum(v[0] for v in static.values())

inputs = [
 dict(index=1, type='Canonical', label='Pfam PF00042 seed (real, 73x141): identity matrix, conservation, entropy/IC, gaps, SP, PSSM, JSD', status='COMPLETED',
      note='All 8 examples and 12 SKILL.md python blocks ran; 14/16 numeric checks vs independent implementations pass. Failures: alignment_score gap/gap penalty (-330,976 vs textbook -215,960) and IC inflated up to +0.58 bits by the seed\'s 27 B/Z residues.',
      basic=32, specialized=46, executed=True,
      execution_note='Executed on real data (Windows venv, Biopython 1.88). References: numpy/scipy re-implementations, hand formulas, authors\' Capra-Singh script (Spearman 1.0 raw, 0.987 with BLOSUM62 background), EMBOSS-free.',
      assertions=[
        A('Percent identity PID2/PID3/PID4 equals the definitional value for all 2,628 sequence pairs', P, 'Asserted in loop against independent pid_ref; matched-residue counts equal a numpy elementwise count.'),
        A('Per-column conservation, Shannon entropy, JSD, PSSM, Kimura and substitution totals equal independent implementations', P, 'scipy entropy diff 1e-15; PSSM 0.0; JSD raw diff 0.0016 vs authors\' formula; Kimura 2,023 finite pairs equal; substitution total 227,180 = brute force.'),
        A('alignment_score (simple SP) equals the textbook sum-of-pairs', F, 'Skill -330,976; textbook with gap/gap = 0 is -215,960 (gap/gap pairs are charged -2).'),
        A('information_content is correct when the alignment contains ambiguity letters (B/Z present in the seed)', F, 'Unknown letters fall back to background 1e-9: 25 columns inflated, max +0.58 bits.'),
        A('All shipped examples/*.py exit 0 and print checked, non-empty output', P, '8/8 rc=0; stdout 6-238 lines each; gap totals (1,943) and gap-free column count match.')]),
 dict(index=2, type='Variant A', label='Real tool output: MAFFT/Clustal Omega (upper), hmmalign AFA (lowercase inserts + dots), Pfam seed with "." gaps', status='COMPLETED',
      note='Uppercase MAFFT/Clustal Omega alignments are exact. hmmalign AFA (284 lowercase, 68 dots): 14/161 conservation columns wrong, IC 29.35 vs 5.48 bits, SP 6,539 vs 6,976. Pfam seed with "." gaps: mean identity 32.0% vs 19.6%, avg conservation 44.7% vs 37.9%. No warning anywhere.',
      basic=22, specialized=29, executed=True,
      execution_note='Executed. hmmalign/MAFFT/Clustal Omega/HMMER run in WSL; A2M output is ragged and cannot be read as fixed-width (not the Skill\'s fault, recorded).',
      assertions=[
        A('MAFFT and Clustal Omega protein alignments (uppercase, "-") give conservation, entropy, IC, PSSM, SP and identity equal to the reference', P, '0 differing columns; SP 8,607 and 8,403 identical to reference.'),
        A('Conservation is correct on an hmmalign alignment with lowercase insert columns', F, '14 of 161 columns differ (max error 0.375): "a" and "A" counted as different residues.'),
        A('Information content stays within the physical maximum (about 6.2 bits for a KL over 20 amino acids)', F, 'Skill max IC 29.35 bits (lowercase letters get background 1e-9); reference 5.48.'),
        A('Percent identity is correct on the Pfam seed written with "." gaps', F, 'Mean pair identity 32.0% vs 19.6% (max pair error 18 points): "." == "." counted as a match.'),
        A('The SKILL.md DistanceCalculator(blosum62) snippet runs on these alignments', F, 'ValueError "Bad letter" on lowercase and on "." inputs.')]),
 dict(index=3, type='Edge', label='Hand-computed 3x8 protein alignment with terminal gaps, an internal gap, ambiguity and a gap-only column (synthetic)', status='COMPLETED',
      note='PID2 100%, PID3 80%, PID4 66.7%, conservation, entropy, gap profile, BLOSUM62 SP 78, simple SP -12, Kimura 0.4393 and substitution counts all equal hand values. PID1 is 50% (hand/paper definition 80%); an all-gap column dilutes average conservation (0.796 vs 0.896) and changes alignment_score (-18 vs -12). Against pwalign::pid on 4 real globin pairs PID2-4 match and PID1 fails on 3 (24.5 vs 25.5, 25.0 vs 40.7, 24.5 vs 42.0).',
      basic=28, specialized=44, executed=True,
      execution_note='Executed. Hand values derived before running (one hand slip in the gap-profile expectation was corrected and is logged in the script).',
      assertions=[
        A('PID2, PID3, PID4 for the tiny pair equal 100%, 80%, 66.7% (hand-computed)', P, 'Exact.'),
        A('PID1 equals 80% (aligned + internal-gap positions, as SKILL.md states and Raghava-Barton/pwalign define)', F, 'Skill counts the 3 terminal-overhang columns: 50%. Same defect vs pwalign::pid on real overlap/local pairs.'),
        A('Per-column conservation, entropy and gap fractions equal the hand values', P, 'cons [1,1,1,.667,1,1,1,.5]; H [0,0,0,.918,0,0,0,1.0]; gaps 1/3 in cols 1,3,5,7,8.'),
        A('BLOSUM62 sum_of_pairs = 78, simple SP = -12, Kimura(s2,s3) = 0.4393, substitution counts = {D-N:2, K-R:1}', P, 'All equal the hand computation.'),
        A('An all-gap column leaves average conservation and the SP score unchanged', F, 'Average conservation 0.796 vs 0.896; alignment_score -18 vs -12 (gap/gap pairs charged).')]),
 dict(index=4, type='Variant B', label='Six real mammalian HBB CDS aligned with MAFFT --auto (nucleotide output is lowercase): Ti/Tv, DNA IC, PSSM, identity', status='COMPLETED',
      note='On the MAFFT default (lowercase) alignment substitution_counts.py prints Transitions 0, Ti/Tv 0.00 (true 428/355 = 1.21) and DNA IC is 29.9 bits (max possible 2.00); DNA PSSM is wrong. Upper-cased copy is exactly right (Ti/Tv 1.21, IC 2.00). Conservation and identity are unaffected (case is consistent within the file).',
      basic=21, specialized=28, executed=True,
      execution_note='Executed on real RefSeq CDS; MAFFT 7.526 in WSL.',
      assertions=[
        A('Ti/Tv from substitution_counts.py equals the independent count on the uppercase alignment', P, '428 transitions, 355 transversions, ratio 1.21.'),
        A('Ti/Tv is correct on the MAFFT default (lowercase) nucleotide alignment', F, 'Prints Transitions 0 / Ti/Tv 0.00: the {"A","G"},{"C","T"} test never matches lowercase.'),
        A('DNA information content stays within 0-2 bits', F, 'Lowercase gives 29.9 bits per column.'),
        A('DNA PSSM with an explicit DNA background equals the reference', F, 'Max error 4.64 log2 units on lowercase; exact on uppercase.'),
        A('Conservation and identity are unaffected by consistent lowercase', P, 'Conservation avg 0.926, identity 87.8% identical for both cases.')]),
 dict(index=5, type='Stress', label='Synthetic 300x300 (clades, terminal and internal gaps) and 2000x300 protein alignments: identity matrix, profile, SP, Kimura', status='COMPLETED',
      note='All computations correct and finish: identity 300x300 in 1.6 s, 2000x300 in 66 s, conservation_profile 1.5 s, BLOSUM62 SP (13M pairs) 28 s, Kimura all pairs 4 s. PID1 under-estimates the internal-gap definition by up to 11.8 points (mean -1.4) when 20% of sequences carry terminal gaps.',
      basic=32, specialized=48, executed=True,
      execution_note='Executed on SYNTHETIC data (numpy seed 20260920/21, files labelled synthetic in data/).',
      assertions=[
        A('identity_matrix_vectorized equals a numpy 3-D broadcast reference', P, 'max diff < 1e-12 on 300x300.'),
        A('sum_of_pairs (BLOSUM62) equals a count-based reference', P, '18,093,751.0 both.'),
        A('Kimura all-pairs (sampled) and conservation_profile equal independent values', P, '435 pairs equal; profile equals mean over columns [i-5, i+4].'),
        A('The 2000x300 identity matrix completes and spot-checks', P, '66.2 s; pair (17,1503) exact.'),
        A('PID1 in identity_matrix.py equals the internal-gap definition it is described by', F, 'Terminal-gap columns counted: -11.8 points worst case.')]),
 dict(index=6, type='Scope Boundary', label='Publication-grade distances: ModelTest-NG / IQ-TREE / distmat hand-off and DistanceCalculator snippet', status='COMPLETED',
      note='ModelTest-NG (installed in a side env) ran both SKILL.md commands (nt: BIC K80+I; aa: BIC DAYHOFF+G4); IQ-TREE writes .mldist as claimed; DistanceCalculator(blosum62) equals the hand formula on 28 pairs; the Skill\'s Kimura equals EMBOSS distmat to 1e-4. The Skill correctly declines to hand-code publication-grade distances. One stale API claim found (.get on a BLOSUM Array).',
      basic=34, specialized=52, executed=True,
      execution_note='Executed: modeltest-ng 0.1.7 (WSL env aln-mtng), iqtree3 (env bio), EMBOSS distmat, Windows Python.',
      assertions=[
        A('The two modeltest-ng commands in SKILL.md run and report a best model', P, 'nt: K80+I (BIC); aa: DAYHOFF+G4 (BIC), exit 0 and output files written.'),
        A('DistanceCalculator(blosum62) snippet matches the documented formula', P, 'Equal to the hand implementation on all 28 pairs.'),
        A('kimura_protein_distance.py agrees with EMBOSS distmat -protmethod 2 (independent tool)', P, '28/28 finite pairs, worst diff 0.0001.'),
        A('IQ-TREE writes .mldist and its closest pair agrees with the Skill\'s distances', P, 'HBB_HUMAN / HBB_PANTR in both.'),
        A('SKILL.md statements about the Biopython 1.88 substitution-matrix API are accurate', F, 'Claim ".get((c1,c2),0) silently always returns 0" is false in 1.88: Array.get returns the correct score (4.0 for A,A).')]),
 dict(index=7, type='Adversarial', label='Messy collaborator alignment (mixed case, ".", X/B/Z/U/*, all-gap sequence) and degenerate inputs (synthetic)', status='COMPLETED',
      note='Silent wrong answers: case-different identical rows score 40% vs 88.9%; all-gap sequence gives 0% identity (no NaN/warning); IC up to 21.3 bits (max 6.2); sum_of_pairs 288 vs 388 (lowercase/U/./* pairs dropped); avg identity NaN for one sequence; a protein alignment whose first row lacks E/F/I/L/P/Q/Y/W is treated as DNA. Unequal lengths give a clear Biopython ValueError.',
      basic=19, specialized=26, executed=True,
      execution_note='Executed on SYNTHETIC small alignments written by the auditor (run/work_in7).',
      assertions=[
        A('Identical sequences differing only in case give 100% identity after normalisation', F, 'Skill 40.0% vs reference 88.9%.'),
        A('An all-gap sequence is flagged (NaN or warning) rather than reported as 0% identity', F, 'pid1..pid4 return 0 silently; identity matrix diagonal 0.'),
        A('Information content is bounded when X/B/Z/U/*/lowercase letters occur', F, 'Max 21.3 bits vs reference 6.2.'),
        A('Degenerate input (unequal lengths, one sequence, two identical sequences) fails clearly or returns a sane value', P, 'Unequal lengths: ValueError "Sequences must all be the same length"; 1 and 2 sequences run (average identity for N=1 is NaN with a numpy warning).'),
        A('entropy_analysis.py picks the protein background for a valid protein alignment', F, 'The E/F/I/L/P/Q/Y/W test picks DNA_UNIFORM when row 0 lacks those letters.')]),
]
for i in inputs:
    i['total'] = i['basic'] + i['specialized']
    i['assertions_passed'] = sum(a['result'] == P for a in i['assertions']); i['assertions_total'] = len(i['assertions'])
    i['status_flag'] = '\u2705' if i['total'] >= 75 else '\u26a0\ufe0f'
    assert 3 <= len(i['assertions']) <= 5
exec_avg = round(sum(i['total'] for i in inputs) / len(inputs), 1)
sw, dw = round(subtotal * 0.4, 1), round(exec_avg * 0.6, 1)
score = int(round(sw + dw))
grade = 'Production Ready' if score >= 85 else 'Limited Release' if score >= 75 else 'Beta Only' if score >= 60 else 'Reject'
sym = {'Production Ready': '\u2b50', 'Limited Release': '\u2705', 'Beta Only': '\u26a0\ufe0f', 'Reject': '\u274c'}[grade]
tp = sum(i['assertions_passed'] for i in inputs); tt = sum(i['assertions_total'] for i in inputs)

rec = lambda pr, title, obs, prob, root, fix: dict(priority=pr, title=title, observed_in=obs, problem=prob, root_cause=root, fix=fix)
recs = [
 rec('P1', 'No case / gap-glyph / ambiguity normalisation (silent wrong output)', [2, 4, 7],
     'Lowercase input (MAFFT nucleotide default, hmmalign inserts), "." gaps and B/Z/X/U letters are treated as distinct residues: Ti/Tv 0.00 vs 1.21, DNA IC 29.9 vs 2.0 bits, Pfam-dot identity 32.0% vs 19.6%, SP drops pairs, DistanceCalculator raises. Nothing warns.',
     'Every function assumes uppercase A-Z plus "-" and never validates the alphabet.',
     'Add a normalise step to Required Import (upper-case, map ".", "~" to "-") and a validation call that reports letters outside the alphabet; apply it at the top of every example; warn that MAFFT nucleotide output is lowercase.'),
 rec('P1', 'PID1 code does not implement its stated definition', [3, 5],
     'PID1 is documented as aligned positions plus internal gaps, but the code counts every column with at least one residue, including terminal overhangs: 50% vs 80% on the hand example, 25.0% vs 40.7% (pwalign::pid) on a fragment pair. identity_matrix.py uses this PID1 while the text recommends PID4.',
     'Denominator written as (a != "-" or b != "-") without excluding terminal gaps.',
     'Exclude gap columns outside each sequence\'s residue span (or rename the metric), add a method argument to identity_matrix.py and default the example to PID4 to match the text.'),
 rec('P1', 'alignment_score charges gap/gap pairs', [1, 3],
     'alignment_score returns -330,976 on the Pfam seed where standard sum-of-pairs gives -215,960, and an all-gap column changes the score. It also contradicts sum_of_pairs, which skips gaps.',
     'The gap branch tests c1 == "-" or c2 == "-" without excluding the both-gap case.',
     'Skip pairs where both characters are gaps (score 0) and state the convention.'),
 rec('P1', 'information_content fallback of 1e-9 inflates IC by ~26 bits per unknown letter', [1, 2, 4, 7],
     'Letters missing from the background dictionary (B, Z, X, U, lowercase, DNA N) add ~26 bits x frequency; IC exceeded 29 bits on real alignments and +0.58 bits on the Pfam seed (27 B/Z residues).',
     'background.get(r, 1e-9) is used instead of dropping and renormalising.',
     'Drop letters outside the background (report the count) and renormalise the column before the KL sum.'),
 rec('P2', 'substitution_counts.py prints Ti/Tv for protein and misses lowercase/RNA', [1, 4],
     'On the protein Pfam seed it prints "Ti/Tv ratio: 0.02" (Ala/Gly and Cys/Thr counted as transitions); on lowercase DNA it prints 0.00; U is not handled.',
     'No alphabet detection; transition set is hard-coded to upper-case A/G/C/T.',
     'Detect nucleotide alignments, upper-case, map U to T, and print Ti/Tv only for DNA/RNA.'),
 rec('P2', 'average_conservation/conservation columns ignore occupancy', [1, 3],
     'Columns with 2-33 residues of 73 score up to 100% conserved (5 such columns >50% gapped) and all-gap columns score 0, so the mean is inflated (37.9% vs 34.3%) or diluted depending on the alignment.',
     'ignore_gaps=True divides by residue count only; no minimum occupancy.',
     'Add a min_occupancy argument (or return NaN for empty columns) and report it with the mean.'),
 rec('P2', 'Stale or inaccurate statements', [6, 1],
     'The claim that Array.get((c1,c2),0) silently returns 0 is false in Biopython 1.88; primary_tool says Bio.Align but code needs MultipleSeqAlignment (Alignment.get_alignment_length raises AttributeError); ROBINSON_BACKGROUND deviates from the published table by up to 5% relative and sums to 1.0036; "Laplace add-one" is a total pseudocount of 1; Common Errors lists ZeroDivisionError and Negative IC causes that do not occur.',
     'Text written against older Biopython and not re-verified.',
     'Correct or delete these statements; use the published Robinson values or label the table approximate; state that AlignIO (MultipleSeqAlignment) is required.'),
 rec('P2', 'Minor gaps', [1, 3, 7],
     '"Build a substitution matrix" (usage-guide) yields only counts; the "Built-in Pairwise Substitutions" snippet reuses gapped MSA rows so "-" appears in the matrix; conservation_profile window is [i-5, i+4]; all-gap sequence returns 0% identity and average identity is NaN for one sequence; no shipped expected outputs.',
     'Snippets are illustrations, not tested.',
     'Add a log-odds matrix helper or reword, strip gaps before PairwiseAligner, centre or document the window, return NaN for undefined identities and ship a small alignment.fasta with expected numbers.'),
]

report = dict(
 source='mrsonord2240/bioSkills@354b4992cd8d2f1bee039510af618da0333821f1:alignment/msa-statistics',
 meta=dict(skill_name='bio-alignment-msa-statistics',
   description='Calculate alignment statistics including sequence identity, conservation scores, substitution matrices, and similarity metrics. Use when comparing alignment quality, measuring sequence divergence, and analyzing evolutionary patterns.',
   evaluated_on='2026-09-20', evaluator_version='skill-auditor@1.0', category='Data Analysis', execution_mode='D', complexity='Complex', n_inputs=7,
   source='mrsonord2240/bioSkills@354b4992cd8d2f1bee039510af618da0333821f1:alignment/msa-statistics',
   audit_kind='first audit', env='F:/OpenScience/audit-envs/alignment (Windows venv Biopython 1.88, numpy 2.0.2, scipy 1.18.1; WSL alignment env; R 4.4.3 pwalign 1.2.0; modeltest-ng 0.1.7 in side env aln-mtng)',
   executed_summary='7/7 inputs executed (Input 6 partly in WSL); 8/8 shipped examples run from a copy; 12 non-stub SKILL.md python blocks run verbatim; shipped-means-present: PASS (all files and cross-referenced sibling examples exist)'),
 veto_gates=dict(
   skill_veto=dict(gate='PASS', stability='PASS', contract='PASS', determinism='PASS', security='PASS'),
   research_veto=dict(applicable=True, gate='PASS',
     scientific_integrity=dict(result='PASS', detail='No fabricated identifiers or results. Verified against sources: Raghava & Barton 2006 (11.5%, 22%, PID4 best at r=0.86; PID definitions equal pwalign::pid) and the authors\' Capra-Singh script (BLOSUM62 background; Robinson-background ranking Spearman 0.987, top-10 9/10). Minor mis-attribution: the "Robinson" table deviates from the published values (P2).'),
     practice_boundaries=dict(result='PASS', detail='Sequence-statistics Skill with no diagnostic or prescriptive content across all 7 outputs.'),
     methodological_ground=dict(result='PASS', detail='Recommended practice is sound (report the PID definition; ModelTest-NG for publication distances; SP weighting caveat). Implementation defects (PID1 terminal gaps, gap/gap SP, lowercase handling) are logged as P1 rather than a principled fallacy.'),
     code_usability=dict(result='PASS', detail='8/8 examples and 12/12 non-stub SKILL.md blocks parse and run on clean input; imports exist in Biopython 1.88; modeltest-ng, iqtree3 and distmat commands run. The DistanceCalculator snippet raises ValueError on lowercase or dot-gapped alignments (loud, logged in P1).'))),
 static_score=dict(subtotal=subtotal, max=100, categories={k: dict(score=v[0], max=v[1], note=v[2]) for k, v in static.items()}),
 dynamic_score=dict(execution_avg=exec_avg, max=100, assertion_pass_rate=dict(passed=tp, total=tt), inputs=[
   dict(index=i['index'], type=i['type'], label=i['label'], status=i['status'], status_flag=i['status_flag'], note=i['note'], basic=i['basic'],
        specialized=i['specialized'], total=i['total'], assertions_passed=i['assertions_passed'], assertions_total=i['assertions_total'],
        executed=i['executed'], execution_note=i['execution_note'], assertions=i['assertions']) for i in inputs]),
 final=dict(static_weighted=sw, dynamic_weighted=dw, score=score, max=100, grade=grade, grade_symbol=sym, deployable=(grade in ('Production Ready', 'Limited Release')), veto_override=False),
 key_strengths=[
   'Core statistics are exact on clean uppercase input: PID2-4, conservation, entropy, PSSM, BLOSUM62 sum-of-pairs, Kimura and substitution counts equal independent implementations; Kimura equals EMBOSS distmat to 1e-4 and Capra-Singh JSD reproduces the authors\' formula.',
   'Unusually careful prose on percent-identity definitions, IC background choice, SP bias and when to hand off to ModelTest-NG/IQ-TREE; the hand-off commands were run and work.',
   'Small, deterministic, read-only and complete: 8 examples present, run from a copy, cross-references to sibling Skills all resolve.'],
 recommendations=recs)

# ---- Pre-Emit Checklist ----
assert len(report['static_score']['categories']) == 8 and subtotal == sum(v['score'] for v in report['static_score']['categories'].values())
assert all(0 <= v['score'] <= v['max'] for v in report['static_score']['categories'].values())
assert len(inputs) == report['meta']['n_inputs'] == 7
for i in report['dynamic_score']['inputs']:
    assert i['basic'] + i['specialized'] == i['total'] and 0 <= i['basic'] <= 40 and 0 <= i['specialized'] <= 60
    assert i['assertions_passed'] == sum(a['result'] == 'PASS' for a in i['assertions']) and 3 <= len(i['assertions']) <= 5
assert exec_avg == round(sum(i['total'] for i in inputs) / 7, 1) and 2 <= len(report['key_strengths']) <= 5
assert [r['priority'] for r in recs] == sorted(r['priority'] for r in recs)
assert report['final']['grade'] == grade and report['final']['veto_override'] is False
json.dump(report, open(os.path.join(OUT, 'eval_report_bio-alignment-msa-statistics_result.json'), 'w', encoding='utf-8'), indent=2, ensure_ascii=False)
print('static', subtotal, 'exec_avg', exec_avg, 'final', sw, '+', dw, '=', score, grade, 'assertions', tp, '/', tt)
print('L1 avg', round(sum(i['basic'] for i in inputs) / 7, 1), 'L2 avg', round(sum(i['specialized'] for i in inputs) / 7, 1))
