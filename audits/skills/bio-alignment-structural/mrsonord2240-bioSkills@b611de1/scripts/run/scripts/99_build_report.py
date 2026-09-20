"""Assemble eval_report_bio-alignment-structural_result.json from the scores decided after reading the logs in run/logs/.
Windows python:  PYTHONIOENCODING=utf-8 python run/scripts/99_build_report.py   (any cwd; paths are absolute).
Checks the schema's pre-emit checklist arithmetic before writing."""
import json, os, statistics

OUT = r'F:\OpenScience\audits\bio-alignment-structural\eval_report_bio-alignment-structural_result.json'
A = lambda t, r, n: {'text': t, 'result': r, 'note': n}

inputs = [
 dict(index=1, type='Canonical', label='[regression] Myoglobin 1MBN vs hemoglobin alpha 1A3N-A (25% id): example, US-align, numpy, DaliLite, PyMOL, flag claims',
  status='COMPLETED', note='TM 0.900/0.836, RMSD 1.56, Lali 141 identical in TM-align, US-align and my numpy Kabsch (1.556); -o prefix fix confirmed (sup2.pdb -> sup2.pdb.pdb); DaliLite block gives Z 20.3 as documented; PyMOL super 1.80 / cealign 1.61.',
  basic=36, specialized=55, executed=True,
  execution_note='examples/tm_align_pairwise.py run from the copy (function and __main__), all asserts in scripts/10_input1_pairwise.py passed; superposed.pdb written with 4370 ATOM records.',
  assertions=[
   A('Example returns TM 0.900/0.836, RMSD 1.56 over 141 residues and equals US-align and an independent numpy Kabsch/TM from TM-align\'s own pairing', 'PASS', 'numpy RMSD 1.5561, TM lower bound 0.8999/0.8356'),
   A('The documented -o prefix behaviour is true and the example writes the file it reports', 'PASS', 'superposed.pdb exists (4370 ATOM); -o sup2.pdb wrote sup2.pdb.pdb'),
   A('Fold call uses min(TM1,TM2) and a readable interpretation with the short-chain guard', 'PASS', "interpret_tmscore(0.836,141) = 'very similar topology'; (0.9, 40) -> chain < 60 guard"),
   A('DaliLite block copied from SKILL.md reproduces the documented result line', 'PASS', '1a3n-A Z 20.3 rmsd 1.6 lali 141 26% id'),
   A('Flag claims (-a T adds average-length TM; -outfmt 2 rejects -a/-u/-L/-d) are accurate', 'PASS', "message '-outfmt 2 cannot be used with -a, -u, -L, -d'; -a T third TM 0.86661"),
  ]),
 dict(index=2, type='Variant A', label='[regression] Foldseek search of 1MBN: custom 15-file folder, real CATH50, real AFDB Swiss-Prot; type 1 vs type 2; cap',
  status='COMPLETED', note='Top hits correct (AFDB AF-P02185 alnTM 0.992 100% id, TM-align 0.974/0.980; CATH sperm-whale myoglobin domains; custom folder 1MBO/1A6M/1EMY then hemoglobins). Type 1: old filter keeps 0, new alnTM filter keeps 14 (custom) / 200 of 200 (AFDB). Cap warning fires (200 rows).',
  basic=35, specialized=52, executed=True,
  execution_note='examples/foldseek_search.py functions imported from the copy and run against 3 databases; __main__ run separately (21_example_mains.py) after replacing only the placeholders; Foldseek prints its full parameter dump to stdout on every call.',
  assertions=[
   A('Top hit of a myoglobin query is myoglobin with alnTM > 0.98 and matches TM-align on the same pair', 'PASS', 'AFDB alnTM 0.9917 vs TM-align 0.9742/0.9804; custom 1MBO 0.997'),
   A('SKILL claim: under --alignment-type 1 E-values are 0.88-0.99 and an evalue<1e-3 filter returns 0 hits; the fixed confident_hits keeps them', 'PASS', 'old filter 0, new 14 (custom); AFDB type 1 old 0, new 200; E 0.83-0.99'),
   A('The --max-seqs cap is disclosed when rows equal the cap', 'PASS', 'AFDB/CATH 200 rows -> warning printed by __main__; cap 1000 confirmed in help; 999 rows with cap 1000'),
   A('Kinase negative control returns only kinases as confident hits', 'PASS', '1ATP query: confident 1ATP_E, 1HCK, 2ITZ only; easy-cluster gave no mixed globin/kinase cluster'),
   A('Other Foldseek commands in SKILL.md (easy-cluster --tmscore-threshold, createdb --mask-bfactor-threshold, custom --format-output, foldseek version) run as documented', 'PASS', '14 db files; 8-field custom row; --version rc 1 as stated'),
  ]),
 dict(index=3, type='Edge', label='[regression] Bio.PDB Superimposer: myoglobin 1MBN/1A6M and apo/holo calmodulin 1CFD/1CLL (Ca2+ ions named CA); refusals; inline SKILL block',
  status='COMPLETED', note='Fixed example: 0.483 A/151 pairs (numpy 0.483, TM-align 0.48) and 10.829 A/144 pairs for calmodulin (numpy 10.829; the pre-fix pairing gives 13.378). Refuses 1MBN vs 1A3N/1ATP/2LHB with an actionable message. The inline SKILL.md block has no name check: 1MBN vs 1A3N prints 7.539 A over 141 pairs with no warning.',
  basic=34, specialized=51, executed=True,
  execution_note='examples/biopython_superimposer.py run (functions and __main__) and the SKILL.md python block extracted and executed verbatim from the copy; RMSD recomputed from the written mobile_superposed.pdb (10.829).',
  assertions=[
   A('Calmodulin apo/holo RMSD is 10.829 A over 144 CA pairs, confirmed by an independent ATOM-only Kabsch', 'PASS', 'example 10.829/144, numpy 10.829/144, naive name-only pairing reproduces the 13.378 trap'),
   A('Myoglobin 1MBN/1A6M: 0.483 A over 151 pairs, equal to independent Kabsch and TM-align', 'PASS', 'numpy 0.483/151; TM-align 0.48 Lali 151'),
   A('The example refuses structures that are not co-numbered instead of returning a number', 'PASS', "ValueError for 1MBN/1A3N (116 of 141 names differ), 1MBN/1ATP (no shared key), 1MBN/2LHB"),
   A('The inline block printed in SKILL.md is equally safe on non-co-numbered input', 'FAIL', 'inline block: 1MBN vs 1A3N -> RMSD 7.539 A over 141 CA pairs, rc 0, no warning (only the example script has the name check)'),
  ]),
 dict(index=4, type='Variant B', label='[regression] Foldmason structural MSA of 8 globin + 3 kinase structures (19 chains): seed, rows, scores key, tree, HTML',
  status='COMPLETED', note='19 chain rows x 378 columns; every row ungaps to the true chain sequence (SEP/TPO shown as S/T); --refine-seed 42 twice and --refine-iters 0 twice byte-identical, unseeded x3 all different; report[scores] length 378 = columns, 30 columns -1; tree has 19 tips; HTML 5.3 MB; 90% of TM-align 1MBN/1A3N-A pairs land in the same column. The quoted 74%/88% unseeded overlap did not reproduce (99.4% on these 11; 56%/87% on the original 5).',
  basic=36, specialized=54, executed=True,
  execution_note='foldmason_msa/summarize/per_column_lddt run through the example (function and __main__ in 21_example_mains.py), SKILL.md JSON snippet executed verbatim, single-structure error reproduced (structuremsa died, Segmentation fault).',
  assertions=[
   A('Same --refine-seed gives identical MSAs across runs; --refine-iters 0 is deterministic; unseeded refinement varies', 'PASS', 'seed 42 x2 md5 9f432a6b48; iters 0 x2 identical; unseeded 3 different md5'),
   A('Rows are chains named <file>_<chain> and ungap to the real chain sequences (independent PDB parse)', 'PASS', '19 rows, 0 mismatches'),
   A("report['scores'] exists, per_column_lddt does not, and len(scores) equals the MSA columns; the SKILL.md snippet runs", 'PASS', '378 = 378; get(per_column_lddt) is None; snippet printed SNIPPET OK 378'),
   A('MSA columns recover the TM-align residue pairing of a known homolog pair', 'PASS', '127 of 141 (90%) same column'),
   A('The quoted unseeded-variance figure (74% of aligned pairs shared, homologous 88%) is reproducible', 'FAIL', '11-structure set 99.4% (same-family 0.993); original 5-structure set 56.3% (same-family 0.870): set-dependent, not a general figure'),
  ]),
 dict(index=5, type='Stress', label='[regression + new] Multimer: 1IRD in 1A3N, tetramer vs tetramer (1HBA and NEW 2HHB), easy-multimersearch/cluster, -mm 4, speed on 62 oligomers',
  status='COMPLETED', note='US-align -mm 1 -ter 0 0.977/0.494 RMSD 0.94 Lali 286 (numpy chain-mapping 0.9768/0.4943, 0.943); 2HHB/1HBA vs 1A3N 0.995/0.992; easy-multimersearch report has 9 columns, 1IRD in 1A3N qTM 0.981/tTM 0.492; --multimer-tm-threshold rejected on search; directory clusters 9 rows, 9-file list and 3-file list collapse to 1 row. Speed: 62 pairs US-align 34.7 s vs Foldseek 19.9 s (directory) / 6.0 s (prebuilt DB) = 1.7x / 5.8x.',
  basic=35, specialized=53, executed=True,
  execution_note='example tm_align(multimer=True) run; Foldseek-Multimer commands run as documented from the copy; 60 real RCSB oligomers + 2 hemoglobin tetramers as the speed set; -mm 4 segfaults (rc -11) as documented.',
  assertions=[
   A('US-align -mm 1 -ter 0 dimer-in-tetramer scores 0.977/0.494 (RMSD 0.94) as SKILL.md states, confirmed by numpy chain-mapping Kabsch and by Foldseek-Multimer', 'PASS', 'numpy 0.9768/0.4943; Foldseek qTM 0.981 tTM 0.492'),
   A('Foldseek-Multimer _report has the nine documented columns and ranks the hemoglobin tetramers >0.95 and non-globins <0.2', 'PASS', '9 columns; 2HHB/1HBA 0.983; 1ATP/1HCK/2ITZ/1DIW <0.2'),
   A('Corrected traps hold: --multimer-tm-threshold rejected on search but valid on cluster; file list/glob collapses to one row (exit 0); directory input clusters all', 'PASS', 'rc 1 with parameter suggestion; rows 9 vs 1 vs 1'),
   A('-mm 4 is not offered as the remedy; SKILL warns it is MSTA and segfaulted on two complexes', 'PASS', 'USalign -h: 4: MSTA; rc -11 reproduced; no byresi text left'),
   A('Foldseek-Multimer speed (10-100x pairwise) and database names (AFDB-Multimer, PDB100-Multimer) are supported by anything runnable here', 'FAIL', 'measured 1.7x (directory incl. createdb) and 5.8x (prebuilt DB) on 62 small oligomers; foldseek databases lists no multimer or PDB100 database'),
  ]),
 dict(index=6, type='Scope Boundary', label='[regression] AlphaFold model AF-P02185 vs crystal 1MBN: TM, RMSD, lDDT, GDT-TS (TMscore -seq), pLDDT masking of AF p53',
  status='COMPLETED', note='TM 0.974/0.980, RMSD 0.71 over 153 (TM-align = US-align = numpy); Foldseek lddt > 0.9; TMscore default GDT-TS 0.508 vs -seq 0.985 (documented trap reproduced), independent GDT-TS lower bound 0.9755; --mask-bfactor-threshold 70 changed exactly the 158 positions with pLDDT < 70 (soft-masked lowercase).',
  basic=36, specialized=55, executed=True,
  execution_note='documented TMscore command run with and without -seq; GDT-TS independently bounded from the TM-align superposition; masked 3Di database dumped and compared position by position.',
  assertions=[
   A('TM-score, RMSD and Foldseek lddt for model vs native agree across TM-align, US-align, numpy and Foldseek', 'PASS', 'TM 0.9742/0.9804; RMSD 0.71 (numpy 0.7054); lddt > 0.6 cutoff'),
   A('GDT-TS command in SKILL.md reproduces the documented values (0.985 with -seq; 0.508 without)', 'PASS', 'TMscore -seq GDT 0.9853 TM 0.9804 RMSD 0.705; default 0.5082/0.593'),
   A('GDT-TS is independently plausible', 'PASS', 'numpy GDT-TS from TM-align superposition 0.9755 <= 0.9853'),
   A('The pLDDT masking claim is true: only residues below the threshold change', 'PASS', '158 positions changed = 158 B-factor < 70 residues; self-search still hits E 6.5e-76'),
  ]),
 dict(index=7, type='Adversarial', label='[regression] "Ubiquitin and protein G B1 have TM > 0.5, so they are homologs; give me the p-value"; max vs min rule over 136 real pairs',
  status='COMPLETED', note='TM 0.4215/0.4978 RMSD 3.14; the example guards chains < 60 residues, SKILL says fold is not homology and no tool prints a p-value; DALI Z 2.8 (candidate band). max rule: 3 false same-fold calls (1PGA vs 1ATP/1HCK/2ITZ 0.505-0.544), min rule 0; min misses 1CFD/1CLL and 1UBQ/1PGA (disclosed). 10-residue helix scores 0.846 and the guard fires.',
  basic=37, specialized=56, executed=True,
  execution_note='136 TM-align pairs of 17 real entries (95 known-different-fold); DaliLite, US-align and Foldseek on the ubiquitin/GB1 pair; no p-value string in TMalign/USalign output.',
  assertions=[
   A('The Skill does not equate TM > 0.5 with homology and does not fabricate a p-value', 'PASS', "'not proof of homology'; 'no tool here prints a p-value'; 'p-value' absent from TMalign+USalign output"),
   A('Short chains (< 60 residues) are guarded in the shipped code', 'PASS', 'interpret_tmscore returns the guard for 56-residue GB1 and the 10-residue helix'),
   A("The numeric claim 'max rule gives false same-fold calls, min rule none' reproduces on real entries", 'PASS', 'max: 3 (1PGA vs three kinases); min: 0 of 95 different-fold pairs'),
   A('DALI Z for the pair falls in the SKILL band that does not support homology', 'PASS', 'Z 2.8 -> candidate (2-8)'),
  ]),
 dict(index=8, type='Variant B', label='[NEW] Kinase remote homology: PKA 1ATP-E vs CDK2 1HCK/AF models; AFDB Swiss-Prot + CATH50 search, Foldmason, MUSTANG, DALI, GDT-TS',
  status='COMPLETED', note='TM 0.680/0.766 RMSD 2.85 Lali 254 (US-align, numpy agree), idali 27.6%, DALI Z 24.1; PKA vs AFDB Swiss-Prot top hits AF-P25321/P05132 alnTM 0.997 and CATH 1.10.510.10 in the top 3 (TM-align on 5 downloaded hit models 0.99); Foldmason 6 chain rows x 391 columns reproducible with seed 42; MUSTANG row writes out.afasta (3 rows) + out.pdb, PKA/CDK2 identity 28%; CDK2 AF model vs 1HCK GDT-TS 0.9175 (numpy bound 0.908). Foldmason agrees with only 54% of TM-align pairs for this twilight pair (90% for globins).',
  basic=35, specialized=54, executed=True,
  execution_note='real AFDB v6 models P17612 and P24941 downloaded; every SKILL.md command for the workflow run: tm_align example, DaliLite block, foldseek_search/confident_hits, foldmason_msa/per_column_lddt, MUSTANG row, TMscore -seq.',
  assertions=[
   A('PKA vs CDK2 fold call and metrics are consistent across TM-align, US-align, numpy and DALI, and the identity is in the twilight range', 'PASS', 'TM 0.680/0.766, RMSD 2.85; Z 24.1; 27.6% identity; interpret -> same fold'),
   A('Foldseek hits for PKA in AFDB Swiss-Prot and CATH50 are kinase-fold homologs, confirmed by TM-align on downloaded models', 'PASS', '5 of 5 hits TM 0.99 by 1ATP; CATH 1.10.510.10 in top 3'),
   A('Foldmason (seed) is reproducible and the MUSTANG row in SKILL.md runs', 'PASS', 'md5 c3c767d61a twice; out.afasta 3 rows, out.pdb present'),
   A('GDT-TS of the CDK2 model via the documented TMscore -seq command is consistent with an independent bound', 'PASS', 'TMscore 0.9175 vs numpy 0.9082; TM 0.9606 vs TM-align 0.9616'),
  ]),
 dict(index=9, type='Edge', label='[NEW] Superimposer on T4 lysozyme WT/L99A, six SeMet (MSE) entries, AF model vs crystal; degenerate inputs and Common Errors rows',
  status='COMPLETED', note='2LZM/181L: 0.200 A over 162 pairs (numpy 0.200, TM-align 0.20); AF CDK2 vs 1HCK 1.873 A/294 (numpy equal); PKA crystal chain E vs AF chain A refused with an actionable message. HETATM MSE residues (1-4% of residues in six real entries) are dropped from the pairing without mention. one_residue/ligand_only raise RuntimeError with the tool message; Foldseek wrong path rc 1; Bio.PDB unequal lists reproduced; US-align segfaults on a one-residue structure_1.',
  basic=33, specialized=49, executed=True,
  execution_note='rotated copies written at file level (Bio.PDB atom.coord does not reach altloc children); every claim in the Common Errors table that involves the examples was executed.',
  assertions=[
   A('A real point-mutant pair (T4L 2LZM/181L) superposes with RMSD equal to independent Kabsch and TM-align', 'PASS', '0.200 / 0.200 / 0.20 over 162 pairs'),
   A('Modified residues that the code excludes (HETATM MSE) are disclosed in the docs or in the printed output', 'FAIL', '6 SeMet entries: 1-4% of residues excluded (7KOM 5 of 134); SKILL.md has no MSE/modified-residue note; the printed pair count is the only trace'),
   A('AF model vs crystal with different chain ids is refused with an actionable message, not silently mispaired', 'PASS', "ValueError 'No residues share (chain, number, insertion code) ... Use TMalign / USalign'"),
   A('Degenerate inputs raise with the tool message instead of returning None', 'PASS', "'Sequence is too short <3!' and 'Cannot parse file ... Chain number 0'"),
   A('Common Errors rows reproduce (wrong DB path rc 1, unequal atom lists, one-residue crash)', 'PASS', "'Input /nonexistent/db does not exist' rc 1; 'Fixed and moving atom lists differ in size'; USalign rc 139 on one_residue"),
  ]),
]

for i in inputs:
    i['total'] = i['basic'] + i['specialized']
    i['assertions_passed'] = sum(a['result'] == 'PASS' for a in i['assertions'])
    i['assertions_total'] = len(i['assertions'])
    assert 3 <= i['assertions_total'] <= 5
    i['status_flag'] = '\u2705' if i['status'] == 'COMPLETED' and i['total'] >= 75 else ('\u26a0\ufe0f' if i['status'] == 'COMPLETED' else '\u274c')
    assert i['basic'] <= 40 and i['specialized'] <= 60
avg = round(statistics.mean(i['total'] for i in inputs), 1)
cat = {
 'functional_suitability': (10, 12, 'Completeness 3 (every workflow the description promises now has a runnable path; no Xu-Zhang p-value, no Foldseek-Multimer database named), Correctness 3 (every command and number I re-ran reproduces; speed/literature figures and the 74%/88% variance quote are unverified or set-specific), Appropriateness 4.'),
 'reliability': (10, 12, 'Fault tolerance 3 (tm_align raises with the tool message, Superimposer example refuses offset numbering, cap warning; the inline block and MSE exclusion fail silently), Error reporting 4 (Common Errors rows reproduced), Recoverability 3 (seeded, rerunnable).'),
 'performance_context': (5, 8, 'Token cost 2 (one 330-line SKILL.md, no references/ split, though usage-guide.md fell from 106 to 41 lines), Execution efficiency 3 (foldseek_search prints Foldseek\'s full parameter dump on every call).'),
 'agent_usability': (14, 16, 'Learnability 3 (example __main__ blocks keep placeholder names query.pdb, /path/to/afdb, structures/), Consistency 3, Feedback design 4 (examples print pair counts, cap warning, scored-column counts), Error prevention 4 (numbering, file-list, -o prefix, short-chain, seed traps all named).'),
 'human_usability': (6, 8, 'Discoverability 3 (natural prompts; description says "Predict" but no prediction path exists), Forgiveness 3 (refusals name the alternative tool).'),
 'security': (11, 12, 'argv-list subprocess only, no eval, no credentials, no data retention (4 and 4); no path validation on user filenames (3).'),
 'maintainability': (8, 12, 'Modularity 3, Modifiability 3, Testability 2 (asserts exist in per_column_lddt and the refusals, but no sample data or test inputs ship).'),
 'agent_specific': (17, 20, 'Trigger precision 3, Progressive disclosure 3, Composability 3 (all 10 Related Skills paths exist), Idempotency 4 (seeded Foldmason, deterministic tools), Escape hatches 4 (identity table, <60-residue guard, Not-covered sentence, refusal messages).'),
}
subtotal = sum(v[0] for v in cat.values()); assert subtotal == 81
sw = round(subtotal * 0.4, 1); dw = round(avg * 0.6, 1); score = round(sw + dw)
passed = sum(i['assertions_passed'] for i in inputs); total = sum(i['assertions_total'] for i in inputs)
print('static', subtotal, 'exec avg', avg, 'score', sw + dw, '->', score, '| assertions', passed, '/', total, '=%.1f%%' % (100 * passed / total),
      '| L1 avg %.1f L2 avg %.1f' % (statistics.mean(i['basic'] for i in inputs), statistics.mean(i['specialized'] for i in inputs)))
assert score >= 85 and subtotal >= 80 and avg >= 85 and statistics.mean(i['basic'] for i in inputs) >= 32 and statistics.mean(i['specialized'] for i in inputs) >= 48 and passed / total >= 0.90

rep = lambda p, t, o, pr, rc, fx: dict(priority=p, title=t, observed_in=o, problem=pr, root_cause=rc, fix=fx)
report = {
 'meta': {
  'skill_name': 'bio-alignment-structural',
  'description': 'Align protein structures using Foldseek 3Di, TM-align, US-align, DALI, or Foldmason for structural MSA. Predict, score, and superpose backbone coordinates when sequence identity is below the twilight zone or remote-homology detection is required. Use when sequence MSA fails (<25% identity), when the dark proteome is the target, when AlphaFoldDB / ESM Atlas search is needed, or when structural superposition is the goal.',
  'evaluated_on': '2026-09-20', 'evaluator_version': 'skill-auditor@1.0', 'category': 'Data Analysis', 'execution_mode': 'D', 'complexity': 'Complex', 'n_inputs': 9,
  'source': 'mrsonord2240/bioSkills@b611de1c303cb454f76e2e10ae39cba0db3e3c06:alignment/structural-alignment',
  'audit_type': 're-audit (third agent, after fix/al-struct)', 'pre_fix_score': 73, 'pre_fix_grade': 'Beta Only', 'regression_inputs': [1, 2, 3, 4, 5, 6, 7], 'new_inputs': [8, 9],
  'n_inputs_note': 'Complex rule = 7; the 7 pre-fix inputs were re-run as regression tests (input 5 also gained NEW complexes 2HHB and a 62-entry speed set) and 2 NEW inputs (8 kinases, 9 edge cases) added.',
  'executed_inputs': '9/9', 'fix_log': 'F:/optimizing-agent-science-skills/fixes/bio-alignment-structural.md (not used as evidence)',
  'env': 'F:/OpenScience/audit-envs/alignment (WSL science env alignment: TM-align 20240303 compiled, US-align 20241108, TMscore, Foldseek 10.941cd33, Foldmason 4.dd3c235, DaliLite v5, MUSTANG 3.2.3, PyMOL 3.1.0, Biopython 1.88, Python 3.12.14); public RCSB/AFDB downloads for new data',
  'execution_note': 'Skill copied from the fix commit into run/skill (byte-identical to the worktree); nothing written in the worktree or external/. Every number was cross-checked by a second method (US-align, numpy Kabsch/TM/GDT written for the audit, DaliLite, PyMOL, Foldseek, independent PDB parse).'},
 'veto_gates': {
  'skill_veto': {'gate': 'PASS', 'stability': 'PASS', 'contract': 'PASS', 'determinism': 'PASS', 'security': 'PASS'},
  'research_veto': {'applicable': True, 'gate': 'PASS',
   'scientific_integrity': {'result': 'PASS', 'detail': 'No fabricated identifiers or numbers: every TM-score, RMSD, Z, GDT-TS and lDDT quoted in the 9 outputs was reproduced by a second tool; the Skill states that no p-value can be printed rather than inventing one. Literature figures (Foldseek-Multimer speed, Gilchrist 2026 pages) are unverified, not fabricated evidence.'},
   'practice_boundaries': {'result': 'PASS', 'detail': 'Structural bioinformatics only; nothing diagnostic or prescriptive.'},
   'methodological_ground': {'result': 'PASS', 'detail': 'The pre-fix max(TM) fold call is replaced by min(TM) with a < 60-residue guard and an explicit fold-is-not-homology statement; residual limits (min rule misses shifted homologs) are disclosed in the Skill.'},
   'code_usability': {'result': 'PASS', 'detail': 'All four examples run from a clean copy (functions and __main__, placeholders replaced only for foldseek_search); the inline SKILL.md Superimposer and JSON blocks run verbatim; outputs asserted on content in every script.'}}},
 'static_score': {'subtotal': subtotal, 'max': 100, 'categories': {k: {'score': v[0], 'max': v[1], 'note': v[2]} for k, v in cat.items()}},
 'dynamic_score': {'execution_avg': avg, 'max': 100, 'assertion_pass_rate': {'passed': passed, 'total': total},
   'inputs': [{k: i[k] for k in ('index', 'type', 'label', 'status', 'status_flag', 'note', 'basic', 'specialized', 'total', 'assertions_passed', 'assertions_total', 'assertions', 'executed', 'execution_note')} for i in inputs]},
 'final': {'static_weighted': sw, 'dynamic_weighted': dw, 'score': score, 'max': 100, 'grade': 'Production Ready', 'grade_symbol': '\u2b50', 'deployable': True, 'veto_override': False},
 'key_strengths': [
  'Every pre-fix P1 is genuinely fixed: corrected Foldseek-Multimer commands, -mm 1 -ter 0, Foldmason scores key and --refine-seed reproducibility, the 10.83 A calmodulin Superimposer result, the alnTM filter under --alignment-type 1 all reproduced by my own runs.',
  'Numbers in the Skill are checkable: DaliLite Z 20.3, TMscore -seq GDT-TS 0.985, US-align 0.977/0.494 and the 3-vs-0 false fold calls all matched, and independent numpy Kabsch/TM/GDT agreed.',
  'Deleted claims are gone (Expresso, 3D-Coffee, PROMALS3D, mTM-align, FATCAT, ChimeraX, pLM aligners appear only in one Not-covered sentence) and the usage-guide dedup (106 to 41 lines) lost nothing an agent needs.',
  'Failure modes are named and refused in code: numbering offset, short chains, file-list clustering, one-residue input, wrong database path, single-structure Foldmason.'],
 'recommendations': [
  rep('P2', 'Inline Superimposer block and MSE handling are less safe than the example', [3, 9],
      'The SKILL.md inline block pairs by residue number with no name check (1MBN vs 1A3N prints 7.539 A over 141 pairs, exit 0), and both it and the example drop HETATM MSE/modified residues (1-4% of residues in six real entries) without mention.',
      'The refusals were added to examples/biopython_superimposer.py but not to the shorter block in SKILL.md; id[0]==\' \' was chosen to exclude ions.',
      "Add the residue-name check to the inline block (or say 'use examples/biopython_superimposer.py') and one sentence that modified residues such as MSE are excluded; optionally accept id[0]=='H_MSE'."),
  rep('P2', 'Foldseek-Multimer speed and database-name claims are unverified', [5],
      'The 10-100x pairwise and >99% chain-pairing figures were left unchecked; on 62 small oligomers Foldseek-Multimer was 1.7x (directory, incl. createdb) to 5.8x (prebuilt DB) faster than US-align, and foldseek databases lists no AFDB-Multimer or PDB100 database that the text and a usage-guide prompt name.',
      'Literature numbers copied without a source location; the bioRxiv abstract supports only 3-4 orders of magnitude at database scale.',
      'Cite the figure to the paper as a scale claim (thousands of complexes and up), drop the pairwise 10-100x and PDB100-Multimer, and name a target that exists (PDB or a folder of complexes).'),
  rep('P2', 'The unseeded Foldmason variance figures are set-specific', [4],
      "'74% of aligned pairs shared; homologous pairs 88%' came from a 5-structure set; re-measured 56%/87% there but 99.4% on the 11-structure globin/kinase set.",
      'One measurement quoted as a general fact.',
      "Say 'unseeded refinement changes the MSA (as little as 0.6% to as much as 44% of aligned pairs in our runs)' or drop the numbers; the seed advice stays."),
  rep('P2', 'Housekeeping left from the fix', [2, 8],
      "Description still says 'Predict' (no prediction path); the Hamamsy 2024 (TM-Vec) reference outlives the deleted pLM section; example __main__ blocks keep placeholder names; foldseek_search dumps Foldseek's parameter table on every call; SKILL.md is one 330-line file with no references/ split.",
      'Deletions and rewrites did not sweep the description, reference list and examples.',
      "Reword the description ('Score and superpose...'), drop the Hamamsy reference, add -v 1 to the Foldseek calls and read paths from argv in the examples."),
 ]}
json.dump(report, open(OUT, 'w', encoding='utf-8'), indent=2, ensure_ascii=False)
print('wrote', OUT)
