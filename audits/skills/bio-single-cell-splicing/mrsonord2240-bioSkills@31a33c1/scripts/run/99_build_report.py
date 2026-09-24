"""Builds eval_report_bio-single-cell-splicing_result.json (schema: skill-auditor/references/report_json_schema.md) and asserts the Pre-Emit Checklist.
Scores are the auditor's judgements from the runs logged in run/out/*.log; nothing here is computed from data."""
import json, os
D = os.path.dirname(os.path.abspath(__file__)) + '/..'
A = lambda t, r, n: {'text': t, 'result': 'PASS' if r else 'FAIL', 'note': n}

def inp(i, typ, label, status, note, b, s, asr, exe=True, exnote=''):
    return {'index': i, 'type': typ, 'label': label, 'status': status, 'status_flag': '✅' if (status == 'COMPLETED' and b + s >= 75) else ('⚠️' if status == 'COMPLETED' else '❌'),
            'note': note, 'basic': b, 'specialized': s, 'total': b + s, 'assertions_passed': sum(a['result'] == 'PASS' for a in asr), 'assertions_total': len(asr), 'assertions': asr,
            'executed': exe, 'execution_note': exnote}

inputs = [
 inp(1, 'Canonical', 'BRIE2 CLI + readout (S05, S06) and every example helper, on real Smart-seq2 (130 mouse E6.5 cells)', 'COMPLETED',
     'Blocks run literally. Silent gene filter (31 of 50 events dropped) is exactly as the Skill says; varm/layers keys as documented; brie-count tracks a pysam junction count (Spearman 0.975 skip, 0.917 inclusion); all 5 example helpers run from a clean copy and match hand values.',
     37, 54, [A('SKILL.md block S05 (brie-count + brie-quant) runs unedited on real BAMs and writes brie_quant.h5ad', True, '130 x 19 output; loss printed; no traceback'),
              A('varm[ELBO_gain|pval|fdr|cell_coeff] are events x tested features and layers Psi/Psi_95CI/Z_std exist, as SKILL.md states', True, 'shapes (19,2) for a 2-covariate table; Psi 0-0.999; fdr equals an independent BH of pval (max diff 0.0)'),
              A('The silent gene-filter warning matches observed behaviour', True, 'log: Filtered out 31 genes ... = 31 of 50, same figure the Skill quotes'),
              A('brie-count output agrees with an independent junction count', True, 'pysam per-cell counts: Spearman 0.975 (skip) and 0.917 (inclusion) over 130 x 50'),
              A('Every helper in examples/sc_splicing_brie2.py runs from a clean copy and returns checked values', True, 'fetch (5,227 genes), count on real 10x (0.0348), inference (130,19), find_variable vs hand mean (diff <1e-6), per-cell MWU, pseudobulk conservation 5737==5737, 3 failure modes raise')],
     True, 'run/10_in1_real_brie.sh, 11_in1_pysam_check.py, 12_in1_readout.py, 13_in1_example_helpers.py'),
 inp(2, 'Variant A', 'BRIE2 differential splicing on auditor-generated planted data (60 events, half minus-strand, 100 cells, 28% low-coverage) plus a pure-null set; pre-fix planted/null sets re-run', 'COMPLETED',
     'Planted v2: 12/12 large (dPSI 0.5) and 8/8 small (dPSI 0.2) events at fdr < 0.05, all planted signs correct, 0/40 null events; pure-null 60 events: 0 fdr hits (2 raw p < 0.05). Pre-fix sets: 20/20, 10/10, 2/70 null (FDP 6%); pure null 0/100.',
     38, 55, [A('Large planted effects recovered at fdr < 0.05', True, '12/12 (dPSI 0.5); pre-fix design 20/20'),
              A('Small effects (dPSI 0.2) recovered with the planted sign', True, '8/8 fdr < 0.05; sign(cell_coeff)==sign(psiB-psiA) for all 20 planted hits'),
              A('Null events are not called at fdr < 0.05', True, '0/40 in the mixed set, 0/60 pure null (raw p<0.05: 1 and 2); pre-fix pure null 0/100 (13 raw)'),
              A('Low-coverage cells are shrunk, not blown up', True, 'mean |Psi - truth| 0.079 in low-coverage cells vs 0.083 in normal cells; low cells have 0.62 vs 10.85 reads/event'),
              A('Result is reproducible run to run', True, 'two brie-quant reruns: identical significant set (20 = 20); per-cell Psi differs up to 0.0334, as the Skill states; fdr differs up to 0.52 on non-significant events')],
     True, 'run/20_gen_planted_v2.py, 21_in2_brie_planted.sh, 22_in2_eval.py, 72_determinism.sh; regress/run_regress.sh, regress/13_null_ss2.sh'),
 inp(3, 'Edge', 'Sparse real plate data with random labels; droplet mode on planted 3-prime-like reads (cassette exon near vs far from the poly-A end)', 'COMPLETED',
     'Real random-label null: 0/19 fdr hits. Droplet mode works with the helper: near-3-prime events 15/15 detected, 0/35 null; far-3-prime events (exon >1.5 kb from poly-A) yield 0 discriminating reads. Failure-mode prose beyond the runs (TensorFlow GPU memory, Sierra annotation gaps) was not exercised.',
     35, 51, [A('Random labels on real sparse data give no fdr calls', True, '0 of 19 events at fdr < 0.05 (2 raw p < 0.05)'),
              A('Sparsity caveats are stated and match the measurements', True, 'median 0 unique reads per cell-event; 18% of cell-events >= 5 reads; Skill: >=5-10 needed and <=1 unreliable'),
              A('Planted droplet data: near-3-prime events called, far-3-prime events give no signal', True, 'near3 big 10/10, mid 5/5, null 0/35 at fdr < 0.05; far3 discriminating reads = 0 of 50 events x 300 cells'),
              A('--batchSize default quoted in the OOM failure mode is correct', True, 'brie-quant -h: default 500000'),
              A('Every Per-Tool Failure Mode is backed by an observed run', False, 'BRIE2 TensorFlow memory (CPU-only run), Sierra annotation gaps and the scQuint 3-prime sparsity row were not reproduced')],
     True, 'regress/14_brie_10x.py, regress/13_null_ss2.sh, 12_in1_readout.py'),
 inp(4, 'Variant B', 'MARVEL: rMATS event-table loop (S03) and the full plate workflow (S04) on the real package demo and on planted truth; other event types and dts', 'COMPLETED',
     'S03 and S04 run unedited. Demo: hand PSI == MARVEL PSI (249 pairs, max diff 0), top-event p within Wilcoxon continuity of an independent wilcox.test. Planted v2 (120 events, 20 minus-strand): big 30/30, mid 17/20, null 0/69 at adj p < 0.05, sign 1.0, hand PSI max diff 0 over 2,313 pairs; permuted-label null 0/108. Pre-fix set: 40/40, 20/20, 0/140. RI needs thread >= 2, not in the Skill.',
     36, 52, [A('S03 Preprocess_rMATS loop runs on real rMATS output and the GTF caveat is true', True, 'chrX 2v2: 978/52/162/165/205 events -> same row counts; gene_type NA for all rows without gene rows, 0 NA once gene rows were added; hand-built plus-strand tran_id found in the table'),
              A('S04 runs unedited on the real demo; MARVEL PSI equals a hand computation', True, '10 events, 249 cell-event pairs, max |diff| 0; CompareValues x100 scaling and mean.diff = g2 - g1 confirmed'),
              A('Planted truth recovered, correct sign, null clean', True, 'big 30/30, mid 17/20, null 0/69; sign 1.0 (n 47); permuted null 0/108 (9 raw); regression set 40/40, 20/20, 0/140'),
              A('MXE/A5SS/A3SS/dts statements are accurate', True, 'ComputePSI MXE, A5SS, A3SS run and equal the package-shipped PSI (max diff 0); dts fails with no package called twosamples, as stated'),
              A('Every event class the Skill names can be computed with the text given', False, 'ComputePSI(EventType=RI) errors (argument is of length zero) unless thread >= 2 is passed; the Skill only says RI needs IntronCounts')],
     True, 'run/30-31_marvel_demo_*.R, 32_marvel_S03_rmats.sh, 33_marvel_S03.R, 34_make_gencode_style_gtf.py, 35-37_marvel_*.R, 38-39c_marvel_*.R, regress/28_marvel_planted.R'),
 inp(5, 'Stress', 'Pseudobulk then leafcutter on a replicate-structured design (2 cell types x 7 donors x 6 cells, donor random effect, 20% low coverage) with mismatched-index and n=1 controls', 'COMPLETED',
     'S12/S13/S14 run unedited. 14 pseudobulks, reads conserved (113,015), column hand-check exact, join is by cell id (shuffled metadata gives the identical table). Loud ValueError for RangeIndex, missing cells, NaN, 1 donor, case-changed ids. leafcutter: big 20/20, mid 12/20 fdr < 0.05, null 0/110 (5 raw). Pooled n=1 Fisher: null 9/110 fdr, 17 raw.',
     37, 55, [A('S12/S13/S14 run unedited and conserve every read', True, 'pb (450,14); sum 113,015 == input; T2__d3 column equals a numpy mask sum'),
              A('The join is keyed by cell id, not position', True, 'shuffled metadata rows and reversed matrix columns give identical pseudobulk and groups'),
              A('A mismatched index fails loudly', True, 'RangeIndex, 10 cells missing, NaN sample, 1 donor per type and lower-cased ids all raise ValueError with the cell ids or counts named'),
              A('leafcutter -i 5 -g 3 -c 20 on replicate pseudobulks recovers planted events without null calls', True, 'big 20/20, mid 12/20 (17 raw), null 0/110 at FDR < 0.05; direction 1.0 on 32 planted hits'),
              A('The Skill warning that pooled n=1 pseudobulk is anti-conservative is right', True, 'Fisher on the same counts pooled per type: 9/110 null at FDR < 0.05, 17/110 raw')],
     True, 'run/40_pb_gen.py, 41_pb_S12_S13.py, 42_pb_leafcutter.sh, 43_pb_score.py'),
 inp(6, 'Scope Boundary', 'Psix along a trajectory, Sierra APA on a real 10x BAM, scQuint on real STARsolo output and planted data, SpliZ config', 'PARTIAL',
     'Psix S09 (defaults) runs: 25/25 dynamic (15 sigmoid, 10 bump), 6/75 static at q < 0.05, 903 s. Sierra S10/S11 run on the bundled real BAM: 34 peaks, top-5 UMI totals within 1% of an Rsamtools count, planted 7/8. scQuint S07 fails on real self-consistent STARsolo output (0 introns matched; cryptic ValueError) and only works with chr-prefixed junctions plus a non-chr GTF; then planted 30/30, 20/20, 1/70 null. SpliZ not run (config keys verified).',
     31, 44, [A('Psix block runs unedited and recovers planted regulated exons', True, '25/25 dynamic, 6/75 static at qvals < 0.05 (Skill quotes 1-4 of 120); median psix_score 1.21 vs -0.01'),
              A('Sierra blocks run unedited on a real BAM and agree with an independent count', True, 'FindPeaks 34 peaks; CountPeaks 22,439 UMIs; peak UMIs 6253/6284, 2776/2777, 1600/1609, 1250/1261, 899/899; null split 0 peaks; planted 7/8'),
              A('scQuint block works on real STARsolo SJ output with the GTF the run used', False, 'real SmartSeq STARsolo (contigs X): add_gene_annotation matches 0 introns, adata (4,0), group_introns raises ValueError; works only if junctions carry chr and the GTF does not'),
              A('scQuint failure-mode text (all groups filtered -> both tables empty) is accurate', False, 'default 30/30 on 40 planted cells raised ValueError not enough values to unpack; tables were not returned empty'),
              A('Unrun tools are hedged and their commands are real', True, 'SpliZ marked not run, nextflow.config keys dataname/input_file/SICILIAN/grouping_level_1/2/libraryType present, no setup.py; junctions2psi marked not run; pip lines: brie/psix/scquint resolve on dry run, Psix needs --no-build-isolation (fails without)')],
     True, 'run/50_psix_gen_and_S09.py, 51_sierra_stage_S10.sh, 52_sierra_S11.R, 60_starsolo_real.sh, 61-64_scquint_*.py, 70_install_claims.sh; SpliZ, junctions2psi and pip installs not executed (Nextflow absent; dry run only)'),
 inp(7, 'Adversarial', '"Give me per-cell cassette-exon PSI and cell-type-specific exons from my 10x 3-prime v3 data"', 'COMPLETED',
     'The Skill answers no and redirects (Sierra for APA, pseudobulk, plate or long-read). Measured: 0.0348 unique discriminating reads per cell per event on the real 10x subset (Skill: < 0.1); 0 for events far from poly-A; R2 length 91 nt confirmed. Not measured: > 70% of unique reads in the 3-prime UTR, median fragment < 1 kb.',
     36, 52, [A('Refuses transcriptome-wide per-cell PSI from 10x 3-prime and says why', True, 'chemistry table, 10X 3-prime section and decision tree all say No; consistent'),
              A('The < 0.1 reads per cell per event figure holds on real 10x data', True, '0.0348 mean (1301 cells x 50 events); 0.11% of cell-events reach 5 reads; 4 of 50 events reach 100 reads over all cells'),
              A('Events far from the poly-A end give no signal', True, 'planted 10x: far3 events 0 discriminating reads'),
              A('Redirects to workable alternatives with runnable code', True, 'Sierra block S10/S11 and pseudobulk S12-S14 both ran'),
              A('Every numeric claim in the 10X section is backed', False, '> 70% of reads in 3-prime UTR and median fragment < 1 kb are not measured or cited to a specific figure; R2 91 nt confirmed from the BAM')],
     True, 'regress/15_real_10x.py, regress/14_brie_10x.py, 13_in1_example_helpers.py'),
]

static = {
 'functional_suitability': (10, 12, 'Every block the fix touched now runs; 4 event classes, dts and RI are only partly covered (RI needs thread >= 2) and the scQuint claim about contig naming is wrong for self-consistent STAR runs.'),
 'reliability': (9, 12, 'Failure modes quote real error text and the pseudobulk helper fails loudly; two scQuint statements (empty tables, chr handling) do not match behaviour; BRIE2 has no seed but sets are stable.'),
 'performance_context': (5, 8, 'SKILL.md is 561 lines / 38 KB with no references/ split; usage-guide.md was cut to a short pointer file (no content lost).'),
 'agent_usability': (13, 16, 'Version block, install lines, output keys and thresholds are explicit and were run; occasional undefined placeholders (cell_types, cell_identities, junction_counts) are the user own inputs.'),
 'human_usability': (7, 8, 'Description names the chemistry decision first and the tools; strict failures with clear messages.'),
 'security': (11, 12, 'No secrets; subprocess argument lists; one network download (SourceForge GFF3) without checksum.'),
 'maintainability': (8, 12, 'Monolithic SKILL.md; helpers separated in examples/ and versions pinned; blocks are copy-run testable.'),
 'agent_specific': (15, 20, 'Precise trigger; escape hatches (chemistry gate, do not impute, APA is not AS) are strong; progressive disclosure weak (no references/).'),
}
sub = sum(v[0] for v in static.values())
avg = round(sum(i['total'] for i in inputs) / len(inputs), 1)
sw, dw = round(sub * 0.4, 1), round(avg * 0.6, 1); score = round(sw + dw)
assert (sub, avg, score) == (78, 87.6, 84), (sub, avg, score)
recs = [
 {'priority': 'P1', 'title': 'scQuint block fails on real self-consistent STARsolo output', 'observed_in': [6],
  'problem': 'add_gene_annotation prepends chr to the GTF contigs, so a STAR run with contigs X/1 (or chr1 plus a chr GTF) matches 0 introns: adata is (n,0) and group_introns raises "Cannot set a DataFrame with multiple columns". With every group filtered, run_differential_splicing raises "not enough values to unpack" instead of returning empty tables. The block only works with chr-prefixed junctions and a non-chr GTF.',
  'root_cause': 'The section was validated only on a synthetic SJ directory whose junction contigs carried chr while the GTF did not, and the empty-table statement was not reproduced.',
  'fix': 'State the naming rule explicitly (junction chromosome names must be chr-prefixed and the GTF contigs not), add a one-line check that adata.n_vars > 0 after add_gene_annotation, and replace the "both tables are empty" sentence with the observed ValueError and the advice to lower the two thresholds.'},
 {'priority': 'P2', 'title': 'MARVEL RI cannot be computed with the text given', 'observed_in': [4],
  'problem': 'ComputePSI(EventType="RI") errors with "argument is of length zero" unless thread >= 2 is passed; the Skill says only that RI needs IntronCounts. CoverageThreshold=10 is not a plain sum of the three junction counts (NA pattern matches no simple rule).',
  'root_cause': 'RI ComputePSI was hedged as not run.',
  'fix': 'Add thread=2 (and read.length) to a one-line RI example run on the demo, or say RI was not run and needs thread >= 2.'},
 {'priority': 'P2', 'title': 'SKILL.md is 561 lines with no references/ split', 'observed_in': [],
  'problem': 'Everything is loaded on every trigger; static progressive-disclosure and token-cost scores suffer.',
  'root_cause': 'Run-verified blocks were added to one file.',
  'fix': 'Move the per-tool sections (MARVEL, BRIE2, scQuint, Psix, Sierra, pseudobulk) into references/<tool>.md and keep the decision tables and failure-mode index in SKILL.md.'},
 {'priority': 'P2', 'title': 'Unsupported 10X numbers and unmarked install hedges', 'observed_in': [7],
  'problem': '"> 70% of unique reads within 3-prime UTR" and "median fragment < 1 kb" carry no measurement or specific citation; pip/remotes install lines are not marked as unrun; Psix runtime (about 4 min) was 15 min for 240 cells x 100 exons at defaults, with 6/75 static exons at q < 0.05.',
  'root_cause': 'Numeric context copied from the original text; timing taken from one machine and dataset.',
  'fix': 'Cite or drop the two figures, add "install lines not re-run" to the version paragraph, and give the Psix runtime as a range with the n_random_exons / n_neighbors trade-off.'},
]
report = {
 'meta': {'skill_name': 'bio-single-cell-splicing',
          'description': 'Analyzes alternative splicing at single-cell resolution. The first decision is library chemistry: 10X 3-prime cannot support transcriptome-wide splicing; plate full-length and single-cell long-read chemistries can. Covers MARVEL, BRIE2, scQuint, SpliZ, Psix, Sierra (APA) and pseudobulk leafcutter.',
          'evaluated_on': '2026-09-20', 'evaluator_version': 'skill-auditor@1.0', 'category': 'Data Analysis', 'execution_mode': 'D', 'complexity': 'Complex', 'n_inputs': 7,
          'source': 'mrsonord2240/bioSkills@86ae9ee222b5c1ce1e0a9c835c655e2f33b48ccd:alternative-splicing/single-cell-splicing',
          'audit_kind': 're-audit of a fixed Skill (pre-fix 69, Reject, Research Veto M4); auditor different from first auditor and fixer',
          'executed_k_of_n': '7/7 (input 6 partial: SpliZ, Psix junctions2psi, MARVEL RI/dts and pip/remotes installs not executed or only dry-run)',
          'env': 'WSL as-sc (BRIE2 2.3.0, Psix 0.10.8, scQuint, scanpy 1.11.5), as-core (STAR 2.7.11b, rMATS-turbo 4.4.0, regtools 1.0.0, pysam), as-rleaf (leafcutter 0.2.9); Windows R 4.4.3 via r.sh (MARVEL 2.0.5, Sierra 0.99.27, Seurat, Rsamtools)',
          'data': 'real: BRIE tutorial Smart-seq2 130 cells and 10x subset, MARVEL demo (30 cells), Sierra bundled TIP BAM, chrX RNA-seq (rMATS + STARsolo SmartSeq); synthetic and labelled: run/data (v2 BRIE/pseudobulk sets, pre-fix generators re-run), run/out/in4_planted, in4_null, in6_psix',
          'pre_fix': {'score': 69, 'grade': 'Reject', 'veto': 'Research Veto M4 code usability'}},
 'veto_gates': {
   'skill_veto': {'gate': 'PASS', 'stability': 'PASS', 'contract': 'PASS', 'determinism': 'PASS', 'security': 'PASS'},
   'research_veto': {'applicable': True, 'gate': 'PASS',
     'scientific_integrity': {'result': 'PASS', 'detail': 'No fabricated results. Three spot-checked references match Crossref (Psix Genome Res 32:1385, MARVEL NAR 51:e29, Joglekar Nat Neurosci 27:1051-1063). The quantitative anchor (<0.1 reads per cell per event on 10x) measured 0.0348 on real data. Two 10X numbers (>70% in 3-prime UTR, fragment <1 kb) are unmeasured but not fabricated results.'},
     'practice_boundaries': {'result': 'PASS', 'detail': 'Research tooling; nothing diagnostic or prescriptive.'},
     'methodological_ground': {'result': 'PASS', 'detail': 'Chemistry gate, no PSI imputation, APA kept apart from splicing, pseudobulk now requires >= 3 replicate samples per group and the n=1 warning was confirmed (9/110 null at FDR<0.05). No principled fallacy found.'},
     'code_usability': {'result': 'PASS', 'detail': 'Blocks S03, S04, S05, S06, S09, S10, S11, S12, S13 and S14 ran unedited (placeholders defined) with checked output; S07 (scQuint) runs and recovers planted truth but only with chr-prefixed junctions and a non-chr GTF (P1). S01/S02 install lines dry-run only; S08 SpliZ hedged as not run. Pre-fix failures (MARVEL AssignModality/CompareValues arguments, Exp read, Psix constructor and query, Sierra FindPeaks) all fixed.'}}},
 'static_score': {'subtotal': sub, 'max': 100, 'categories': {k: {'score': v[0], 'max': v[1], 'note': v[2]} for k, v in static.items()}},
 'dynamic_score': {'execution_avg': avg, 'max': 100,
   'assertion_pass_rate': {'passed': sum(i['assertions_passed'] for i in inputs), 'total': sum(i['assertions_total'] for i in inputs)}, 'inputs': inputs},
 'final': {'static_weighted': sw, 'dynamic_weighted': dw, 'score': score, 'max': 100, 'grade': 'Limited Release', 'grade_symbol': '✅', 'deployable': True, 'veto_override': False,
           'note': 'Pre-fix 69 (Reject, M4 fired) -> 84. Layer 1 average 35.7/40, Layer 2 average 51.9/60, assertion pass 30/35. No open P0; one open P1 (scQuint). Floors for Limited Release met; below Production Ready.'},
 'key_strengths': [
   'Every MARVEL, BRIE2, pseudobulk/leafcutter, Psix and Sierra block that was broken before the fix now runs unedited and matches hand computation or planted truth (MARVEL PSI exact; 30/30 and 40/40 large events, 0 null calls).',
   'Pseudobulk helper joins by cell id and fails loudly on RangeIndex, missing, NaN and single-donor input; the n=1 warning is empirically right.',
   'Chemistry-first gate is measured, not asserted: 0.0348 reads per cell per event on real 10x, 0 for far-3-prime events.',
   'Silent behaviours are documented from real runs (BRIE2 gene filter, no --seed, MARVEL x100 scale, GTF gene_type NA, twosamples for dts).',
   'usage-guide.md was deduplicated without losing anything a task needs (install block, chemistry tips and prompts are in SKILL.md).'],
 'recommendations': recs}

# ---- Pre-Emit Checklist
cs = report['static_score']['categories']; assert len(cs) == 8 and all(0 <= v['score'] <= v['max'] for v in cs.values()) and report['static_score']['subtotal'] == sum(v['score'] for v in cs.values())
assert len(inputs) == 7 == report['meta']['n_inputs']
for i in inputs:
    assert 3 <= len(i['assertions']) <= 5 and i['assertions_passed'] == sum(a['result'] == 'PASS' for a in i['assertions']) and i['basic'] + i['specialized'] == i['total'] and i['assertions_total'] == len(i['assertions'])
assert 2 <= len(report['key_strengths']) <= 5 and [r['priority'] for r in recs] == sorted(r['priority'] for r in recs)
json.dump(report, open(D + '/eval_report_bio-single-cell-splicing_result.json', 'w', encoding='utf-8', newline='\n'), indent=2, ensure_ascii=False)
print('static', sub, 'exec avg', avg, 'final', score, 'assertions', report['dynamic_score']['assertion_pass_rate'])
