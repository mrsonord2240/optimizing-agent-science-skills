"""Builds eval_report_bio-single-cell-splicing_result.json from the scored inputs below and checks the schema pre-emit checklist."""
import json, sys
OUT = 'F:/OpenScience/audits/bio-single-cell-splicing/eval_report_bio-single-cell-splicing_result.json'
SRC = 'mrsonord2240/bioSkills@44ff43bb35e5741c3ddd3c003590e1f1da8a4a4b:alternative-splicing/single-cell-splicing'

def A(t, r, n): return {'text': t, 'result': r, 'note': n}

inputs = [
 dict(index=1, type='Canonical', label='BRIE2 per-cell PSI on real Smart-seq2 (130 mouse E6.5 cells)', executed=True,
  execution_note='brie-count and brie-quant run with the SKILL flags verbatim on the cached real data; counts cross-checked with pysam; example helpers called from a copy.',
  status='COMPLETED', flag='✅', basic=32, spec=46,
  note='CLI block is correct and the counts track an independent pysam junction count; the example helper pseudobulk_by_celltype crashes and the Skill never says how the GFF3 events are made.',
  assertions=[
   A('brie-count/brie-quant lines from SKILL.md run as written and write brie_count.h5ad / a quant h5ad', 'PASS', 'rc 0; counts (130,50); quant (130,19) with layers Psi, Psi_95CI, Z_std and varm ELBO_gain, pval, fdr, cell_coeff'),
  A('brie-count counts agree with an independent pysam junction count', 'PASS', 'Spearman 0.975 (skip junction, isoform2) and 0.917 (inclusion, isoform1) over 130 cells x 50 events; BRIE unique skip total 5,737 vs pysam 7,381 (0.78)'),
   A('The output keys the Skill points to (ELBO_gain) exist in the installed brie-quant output', 'PASS', 'varm[ELBO_gain], varm[pval], varm[fdr] present; Skill says only "column names depend on version", never names pval/fdr'),
   A('Every helper in examples/sc_splicing_brie2.py runs on real brie output', 'FAIL', 'pseudobulk_by_celltype raises AttributeError (sparse X indexed with a boolean Series); prepare_splicing_events needs briekit-event which is not installed and crashes when installed'),
   A('Skill tells the agent how to obtain the splicing-event GFF3 that brie-count requires', 'FAIL', '"Prepare a GFF3 of splicing events" only; briekit-event (example) fails with ModuleNotFoundError: parseTables; usage-guide never installs briekit')]),
 dict(index=2, type='Variant A', label='BRIE2 two-group differential splicing on planted Smart-seq-like data with dropout', executed=True,
  execution_note='Synthetic 80 cells x 100 SE events (30 planted, 70 null), 15% dropout cells; SKILL brie-quant flags with a group covariate; plus a 100-event all-null run; example differential helper called.',
  status='COMPLETED', flag='✅', basic=33, spec=48,
  note='Recovers all 30 planted events with the right sign; null control shows FDP 9% (3/33 calls) in the mixed set and 0/100 FDR hits in the pure-null set; the Skill threshold delta-ELBO ~3 gives 6/100 false hits on the pure null.',
  assertions=[
   A('LRT recovers planted differential events (dPSI 0.7 and 0.3)', 'PASS', '20/20 big and 10/10 mid at FDR<0.05, median ELBO_gain 58.8 and 23.3'),
   A('Sign of cell_coeff matches the planted direction', 'PASS', '30/30 correct'),
   A('False positives are controlled on the null', 'PASS', 'mixed set: 3/70 null events FDR<0.05 (FDP 0.091); pure null: 0/100 FDR<0.05, raw p<0.05 in 11/100, ELBO_gain>3 in 6/100'),
   A('Per-cell Psi in low-coverage (dropout) cells is shrunk sensibly, not wild', 'PASS', 'mean |Psi - group truth| 0.091 dropout (1.4 unique reads/event) vs 0.077 normal (20.0 reads/event)'),
   A('The Skill states the ELBO_gain cut-off correctly', 'FAIL', '"threshold ~3, analogous to log-Bayes-factor" is not calibrated: 6% of pure-null events pass it while the fdr column BRIE2 already writes gives 0%; the Skill never mentions pval/fdr')]),
 dict(index=3, type='Edge', label='Sparse real plate data: 130 cells, most cell-event pairs with 0 reads, random-label null', executed=True,
  execution_note='Real 130-cell Smart-seq2 run through brie-quant with a random binary label and a log-depth covariate; brie-quant gene filtering and CI width inspected; example helpers on the same object.',
  status='COMPLETED', flag='⚠️', basic=29, spec=42,
  note='No false LRT calls on real null labels, but the Skill does not warn that brie-quant silently drops 31/50 events under its default gene filters, and helpers built for this case crash.',
  assertions=[
   A('No event is called on a random covariate in real data', 'PASS', 'rand_group: 0/19 FDR<0.05, 0 ELBO_gain>3 (max 2.16); log_depth: 0/19'),
   A('Skill quality thresholds are consistent with real Smart-seq2 sparsity', 'PASS', 'median unique reads/cell/event 0; only 18% of cell-event pairs have >=5 reads; mean 95% CI width of per-cell Psi 0.30 - agrees with the ">=5 reads or unreliable" guidance'),
   A('Skill warns that brie-quant silently filters events (minCount 50, minUniq 10, minCell 30)', 'FAIL', '31 of 50 events dropped with only a console line; Skill lists none of these flags or defaults'),
   A('Example find_variable_splicing / differential_splicing_pseudobulk work on sparse real output', 'PASS', 'both run; Mann-Whitney on random labels gives 0/19 FDR<0.05'),
   A('Example pseudobulk_by_celltype works on the same object', 'FAIL', "AttributeError: 'Series' object has no attribute 'nonzero'")]),
 dict(index=4, type='Variant B', label='MARVEL plate workflow: SKILL block on the package demo, then corrected chain on planted PSI truth', executed=True,
  execution_note='SKILL.md MARVEL block run verbatim on the real MARVEL demo (STAR SJ.out.tab rebuilt from it); ComputePSI checked against a hand computation; corrected chain run on a synthetic 200-event x 60-cell matrix and three label permutations.',
  status='PARTIAL', flag='❌', basic=24, spec=33,
  note='CreateMarvelObject and ComputePSI work and match a hand calculation exactly, but AssignModality(EventType=) and CompareValues(n.cells=, no level) raise, and Exp read with row.names=1 loses the gene_id column MARVEL needs.',
  assertions=[
   A('The SKILL MARVEL block (CreateMarvelObject -> ComputePSI -> AssignModality -> CompareValues) runs as written', 'FAIL', "AssignModality: unused argument (EventType = 'SE'); CompareValues: argument 'level' is missing (n.cells and psi.delta also do not apply)"),
   A('ComputePSI output equals a hand PSI from the junction counts', 'PASS', 'max |MARVEL - hand| = 0 over 109 cell-event pairs on the demo; scale is 0-1'),
   A('Corrected call chain recovers planted differential events with the right sign', 'PASS', 'wilcox: 40/40 big and 20/20 mid at adj p<0.05, sign agreement 1.0'),
   A('Null is controlled after correction', 'PASS', '0/140 null events adj p<0.05 (raw 6/140); 3 permutations: 0 adj p<0.05 each'),
   A('Objects the Skill builds pass MARVEL pre-flight checks', 'FAIL', 'Exp via read.table(row.names=1) drops gene_id: CheckAlignment(level="gene") -> undefined columns selected; event tables (rMATS fromGTF) and IntronCounts (RI) not explained')]),
 dict(index=5, type='Stress', label='Pseudobulk between cell types then leafcutter, with dropout and between-cell overdispersion', executed=True,
  execution_note='Skill pseudobulk_junctions() run on the synthetic junction matrix; output fed to leafcutter_ds.R both as n=1 v 1 (what the function returns) and as 5 v 5 replicate pseudobulks; naive Fisher on pooled counts as comparison.',
  status='COMPLETED', flag='⚠️', basic=27, spec=38,
  note='Function conserves counts but silently returns all zeros if the metadata has a default RangeIndex; pooled-per-type pseudobulk gives no replicates, and a pooled Fisher test calls 34/140 null events.',
  assertions=[
   A('pseudobulk_junctions conserves total junction counts', 'PASS', 'group sums 269,534 + 301,486 = 571,020 = matrix total (metadata index = cell ids)'),
   A('pseudobulk_junctions fails loudly on a mismatched metadata index', 'FAIL', 'metadata read without index_col gives A=0, B=0 with no error or warning'),
   A('leafcutter on replicate pseudobulks recovers planted events', 'PASS', '5v5: 40/40 big, 20/20 mid at FDR<0.05; null 7/140 FDR<0.05 (FDP 0.10)'),
   A('Skill warns that pooling all cells of a type yields no replicates (pseudoreplication)', 'FAIL', 'nothing; n=1 v 1 leafcutter runs (-g 1 -i 1) and reports p-values; pooled Fisher: 34/140 null events FDR<0.05, 32% raw p<0.05'),
   A('leafcutter defaults for pseudobulk are stated', 'FAIL', 'leafcutter_ds.R defaults -g 3 -i 5 -c 20 not mentioned; 2-column pseudobulk would test nothing at defaults')]),
 dict(index=6, type='Scope Boundary', label='Psix trajectory-regulated AS, Sierra APA and SpliZ discovery (tools beyond PSI comparison)', executed=True,
  execution_note='Psix run on synthetic 300-cell trajectory data with the real API; Sierra FindPeaks executed literally (argument error) and signatures listed; SpliZ config keys checked in the clone, not run (no nextflow).',
  status='PARTIAL', flag='❌', basic=24, spec=31,
  note='Psix works and recovers planted exons, but the Skill snippet fails twice (constructor, results column); Sierra FindPeaks call fails on bam.file and the required junctions.file; SpliZ not run.',
  assertions=[
   A('Psix snippet runs as written', 'FAIL', "psix.Psix(adata, psi_matrix_path=...) -> TypeError unexpected keyword; .query('psix_score > 1.5 and pvalue < 0.05') -> UndefinedVariableError (columns are psix_score, pvals, qvals)"),
   A('Psix (real API: psi_table + mrna_table + latent file) recovers planted dynamic exons', 'PASS', '30/30 dynamic at q<0.05, 1/120 static false positive; score median 1.85 vs -0.04'),
   A('Sierra snippet runs as written', 'FAIL', 'FindPeaks(bam.file=) -> unused argument (argument is bamfile); junctions.file has no default and is not shown'),
   A('SpliZ launch line and config keys are valid', 'PASS', 'dataname, input_file, SICILIAN, grouping_level_1/2, libraryType, samplesheet, gtf all exist in the repo nextflow.config; pip install line in usage-guide does not work (no setup.py)'),
   A('Skill keeps APA out of the splicing claims', 'PASS', 'Sierra is repeatedly labelled APA, not splicing')]),
 dict(index=7, type='Adversarial', label='"Give me per-cell cassette-exon PSI and cell-type-specific exons from my 10x 3-prime v3 data"', executed=True,
  execution_note='Real 10x v3 neuron subset (1,301 cells) and a synthetic 300-cell 3-prime dataset (near-3-prime vs far-3-prime cassette exons) through the shipped count_splicing_reads (brie-count droplet mode) and brie-quant.',
  status='COMPLETED', flag='✅', basic=35, spec=50,
  note='The Skill answers correctly (no, use APA or pseudobulk) and the measurements back its numbers: 0.035 unique reads per cell per event in real 10x, 0 in far-3-prime planted events.',
  assertions=[
   A('Skill tells the agent that 10x 3-prime cannot support per-cell splicing and gives what to do instead', 'PASS', 'chemistry table, "10X 3 prime problem" and Common Pitfalls all say so; redirects to APA and pseudobulk'),
   A('"<0.1 junction reads per cell per event" is consistent with real 10x data', 'PASS', 'real 10x subset (selected for reads): mean 0.035 unique reads/cell/event, median 0, only 4/50 events with >=100 reads in total, >=5 reads in 0.1% of cell-event pairs'),
   A('Internal exons far from poly(A) get no isoform-discriminating reads', 'PASS', 'synthetic: far-3-prime events 0.000 unique reads/cell/event (ambiguous 3.04), near-3-prime 2.55; brie-quant silently drops the 50 far events'),
   A('Near-3-prime events remain analysable ("maybe near-3-prime events")', 'PASS', '10/10 big and 5/5 mid near-3-prime events recovered at FDR<0.05, 1/35 null'),
   A('The suggested alternative (Sierra APA) runs as written', 'FAIL', 'FindPeaks(bam.file=) is rejected by Sierra 0.99.27 (see input 6)')]),
]

for i in inputs:
    i['total'] = i['basic'] + i['spec']
    assert i['total'] == i['basic'] + i['spec']
    i['assertions_passed'] = sum(a['result'] == 'PASS' for a in i['assertions'])
    i['assertions_total'] = len(i['assertions'])
    assert 3 <= i['assertions_total'] <= 5

dyn_inputs = []
for i in inputs:
    dyn_inputs.append({'index': i['index'], 'type': i['type'], 'label': i['label'], 'status': i['status'], 'status_flag': i['flag'],
                       'note': i['note'], 'basic': i['basic'], 'specialized': i['spec'], 'total': i['total'],
                       'assertions_passed': i['assertions_passed'], 'assertions_total': i['assertions_total'],
                       'assertions': i['assertions'], 'executed': i['executed'], 'execution_note': i['execution_note']})
execution_avg = round(sum(i['total'] for i in inputs) / len(inputs), 1)
ap = sum(i['assertions_passed'] for i in inputs); at = sum(i['assertions_total'] for i in inputs)

cats = {
 'functional_suitability': (8, 12, 'Chemistry-first framing is correct and quantitatively verified; BRIE2 CLI works. But the headline MARVEL, Psix and Sierra blocks call arguments that do not exist, Common Errors cites brie.tl.fit (no such module), and how to make MARVEL/BRIE event tables is missing.'),
 'reliability': (5, 12, 'Per-tool failure modes exist, but several are wrong (Psix connectivities in obsp, min_reads=20, --outSJtype Standard as a fix); brie-quant silently drops events and pseudobulk_junctions returns zeros with no message.'),
 'performance_context': (6, 8, '447-line SKILL.md with no references/; usage-guide is short; some content (tissue biology table, long-read list) repeats material from long-read-splicing.'),
 'agent_usability': (11, 16, 'Decision tables and goal->approach map are easy to follow; output keys and expected results for BRIE2/MARVEL are left vague ("depend on version").'),
 'human_usability': (6, 8, 'Description is long but uses natural trigger phrases (10X, Smart-seq2, splicing per cell); prompts in usage-guide are realistic; input variants are not handled by the code helpers.'),
 'security': (11, 12, 'No credentials; example passes list arguments to subprocess (no shell); no user strings evaluated.'),
 'maintainability': (6, 12, 'Single 447-line SKILL.md, one example script with 5 helpers of which 2 crash, no tests or expected outputs.'),
 'agent_specific': (15, 20, 'Strong escape hatch (chemistry gate, do not impute, APA is not AS); no references/ layout; version line names releases that do not exist (Sierra 1.0+, BRIE2 0.2.4+ vs 2.3.0).'),
}
sub = sum(v[0] for v in cats.values())
static_w = round(sub * 0.4, 1); dyn_w = round(execution_avg * 0.6, 1); score = round(static_w + dyn_w)

report = {
 'meta': {'skill_name': 'bio-single-cell-splicing',
   'description': 'Analyzes alternative splicing at single-cell resolution. First decision is library chemistry (10X 3-prime is fundamentally limited; plate full-length and single-cell long-read chemistries give per-cell isoforms). Covers MARVEL, BRIE2, scQuint, SpliZ, Psix, Sierra (APA), pseudobulk and modality/PSI concepts.',
   'evaluated_on': '2026-09-20', 'evaluator_version': 'skill-auditor@1.0', 'category': 'Data Analysis', 'execution_mode': 'D', 'complexity': 'Complex', 'n_inputs': 7,
   'source': SRC, 'executed_k_of_n': '7/7 (inputs 4 and 6 partly: SpliZ Nextflow, Sierra on data and MARVEL dts were not run)',
   'env': 'WSL as-sc (BRIE2 2.3.0, Psix 0.10.8, scanpy 1.11.5, anndata 0.12.19, pysam 0.24.1), WSL as-rleaf (leafcutter 0.2.9), Windows R 4.4.3 / Bioc 3.20 via r.sh (MARVEL 2.0.5, Sierra 0.99.27, Seurat)',
   'data': 'real: BRIE2 tutorial Smart-seq2 mouse E6.5 (130 cells) and 10x v3 neuron subset (1,301 cells), MARVEL package demo (30 Smart-seq2 cells); synthetic (labelled): run/data/synth_ss2, synth_ss2_null, synth_10x, marvel_planted_*, psix_planted'},
 'source': SRC,
 'veto_gates': {
  'skill_veto': {'gate': 'PASS', 'stability': 'PASS', 'contract': 'PASS', 'determinism': 'PASS', 'security': 'PASS'},
  'research_veto': {'applicable': True, 'gate': 'FAIL',
   'scientific_integrity': {'result': 'PASS', 'detail': 'No fabricated DOIs, PMIDs or data. The quantitative anchor (<0.1 junction reads per cell per event on 10x 3-prime) reproduced at 0.035 on the real 10x subset; the reference list was not independently verified but no invented identifiers were noticed. brie.tl.fit and a few Common Errors rows are invented but are code-accuracy errors, not fabricated results.'},
   'practice_boundaries': {'result': 'PASS', 'detail': 'Research tooling; nothing diagnostic or prescriptive.'},
   'methodological_ground': {'result': 'PASS', 'detail': 'Chemistry gate, no imputation of PSI and separating APA from AS are sound. Weak point (P1, not a fallacy): pseudobulk advice omits replicates, so pooled per-type counts give n=1 per group.'},
   'code_usability': {'result': 'FAIL', 'detail': 'The MARVEL workflow (primary_tool) fails at AssignModality(EventType=) and CompareValues(n.cells=, no level) and drops gene_id from Exp; the Psix snippet fails at the constructor and at the results query; the Sierra FindPeaks call is rejected (bam.file); the example prepare_splicing_events and pseudobulk_by_celltype do not run. Only the BRIE2 CLI blocks and the pseudobulk_junctions function ran as written.'}}},
 'static_score': {'subtotal': sub, 'max': 100, 'categories': {k: {'score': v[0], 'max': v[1], 'note': v[2]} for k, v in cats.items()}},
 'dynamic_score': {'execution_avg': execution_avg, 'max': 100, 'assertion_pass_rate': {'passed': ap, 'total': at}, 'inputs': dyn_inputs},
 'final': {'static_weighted': static_w, 'dynamic_weighted': dyn_w, 'score': score, 'max': 100, 'grade': 'Reject', 'grade_symbol': '❌', 'deployable': False, 'veto_override': True,
           'note': f'Numeric score {score} would be Beta Only; grade forced to Reject by the Research Veto M4 (code usability), consistent with the sibling audits. Layer 1 average {sum(i["basic"] for i in inputs)/7:.1f}/40, Layer 2 average {sum(i["spec"] for i in inputs)/7:.1f}/60.'},
 'key_strengths': [
  'The chemistry-first thesis is right and measured: real 10x v3 data give 0.035 isoform-discriminating reads per cell per event, and synthetic cassette exons far from poly(A) get exactly 0 reads while near-3-prime exons stay analysable.',
  'The BRIE2 CLI blocks (brie-count -S/-s/-b, brie-quant --interceptMode/--LRTindex/--testBase/--MCsize/--batchSize) run verbatim, the counts track an independent pysam count (rho 0.975), and the ELBO_gain LRT recovered 30/30 planted events with the right sign and controlled the null.',
  'MARVEL SpliceJunction/CreateMarvelObject/ComputePSI usage is right (PSI equals a hand calculation exactly), and once the correct signature is used MARVEL detects 60/60 planted events and 0/140 nulls.',
  'Explicit escape hatches: do not impute PSI, APA is not splicing, snRNA-seq IR caution, doublet filtering, microexon aligner settings.']
 ,
 'recommendations': [
  {'priority': 'P0', 'title': 'MARVEL block calls arguments that do not exist and breaks Exp',
   'observed_in': [4], 'problem': "AssignModality(marvel, EventType='SE') and CompareValues(..., n.cells=25, psi.delta=0.1) raise (unused argument / argument 'level' missing); Exp = read.table(..., row.names=1) removes the gene_id column so CheckAlignment(level='gene') fails; the event tables and IntronCounts are never sourced.",
   'root_cause': 'Signatures were written from memory, not from ?AssignModality / ?CompareValues in MARVEL 2.0.5.',
   'fix': "Replace with AssignModality(marvel, sample.ids = <cell ids>, min.cells = 5, seed = 1) and CompareValues(marvel, cell.group.g1 = , cell.group.g2 = , min.cells = 5, method = 'wilcox', level = 'splicing', event.type = 'SE'); read Exp keeping gene_id (row.names=NULL); say that SpliceFeature tables come from rMATS fromGTF.*.txt (MARVEL vignette) and that RI needs IntronCounts; PSI is on a 0-1 scale; note MARVEL 2.0.5 ComputePSI(SE) errors when the SE table has no minus-strand event and 'dts' needs the twosamples package."},
  {'priority': 'P0', 'title': 'Psix and Sierra snippets do not run',
   'observed_in': [6, 7], 'problem': "psix.Psix(adata, psi_matrix_path=...) raises TypeError; .query('psix_score > 1.5 and pvalue < 0.05') raises UndefinedVariableError; Sierra FindPeaks(bam.file=...) is rejected and the required junctions.file is absent; the Psix failure row (connectivities in adata.obsp) describes a mechanism Psix does not use.",
   'root_cause': 'API written from the papers rather than the installed packages (Psix 0.10.8, Sierra 0.99.27).',
   'fix': "Psix: p = psix.Psix(psi_table='psi.tsv', mrna_table='mrna.tsv'); p.run_psix(latent='latent.tsv', n_jobs=4); p.psix_results.query('qvals < 0.05') (columns psix_score, pvals, qvals; PSI and mRNA tables are events x cells, latent is a cells x dims TSV). Sierra: FindPeaks(output.file=, gtf.file=, bamfile=, junctions.file=<from regtools/STAR>, ...). Correct the Psix Common Errors row."},
  {'priority': 'P1', 'title': 'Example script: 2 of 5 helpers cannot run and prerequisites are wrong',
   'observed_in': [1, 3], 'problem': "prepare_splicing_events shells out to briekit-event, which the prerequisites never install and whose entry point crashes on install (ModuleNotFoundError: parseTables); pseudobulk_by_celltype raises on sparse X; differential_splicing_pseudobulk is a per-cell Mann-Whitney on shrunken Psi, not pseudobulk; 'pip install brie' fails (sdist lacks requirements.txt); the SpliZ pip line has no installable package.",
   'root_cause': 'The example was never executed end to end.',
   'fix': "Drop briekit-event and point to BRIE's shipped GFF3 annotations, fix pseudobulk_by_celltype (use a numpy mask and X.toarray()), rename the differential helper, install BRIE2 from the GitHub clone, and remove the SpliZ pip line (Nextflow only)."},
  {'priority': 'P1', 'title': 'Pseudobulk guidance omits replicates and has a silent-zero helper',
   'observed_in': [5], 'problem': 'pseudobulk_junctions pools all cells of a type into one column (n=1 per group) and returns zeros without error when the metadata index is not the cell ids; a pooled Fisher test called 34/140 null events; leafcutter defaults (-g 3 -i 5) are not stated.',
   'root_cause': 'The section describes aggregation but not the replicate structure the downstream tools need.',
   'fix': 'Aggregate per sample (donor/batch) x cell type, require >=3 replicates per group, assert that the summed matrix equals the total, and set leafcutter_ds.R -g/-i/-c explicitly.'},
  {'priority': 'P1', 'title': 'BRIE2 output and filtering are under-specified; Common Errors invented',
   'observed_in': [1, 2, 3], 'problem': 'The Skill uses ELBO_gain>~3 as the test (6/100 pure-null events pass) and never names the pval/fdr columns brie-quant writes; brie-quant silently drops 31/50 real events under minCount/minUniq/minCell defaults; brie.tl.fit and min_reads=20 do not exist; brie-quant has no --seed.',
   'root_cause': 'Output keys and error strings were not checked against BRIE2 2.3.0.',
   'fix': 'Document varm[ELBO_gain/pval/fdr/cell_coeff], layers Psi/Psi_95CI/Z_std, threshold on fdr, the gene-filter flags, and replace the invented rows with observed errors (e.g. "Could not retrieve index file" when BAMs lack .bai).'},
  {'priority': 'P2', 'title': 'Metadata and version line',
   'observed_in': [], 'problem': 'tool_type python with primary_tool MARVEL (R); Sierra "1.0+" (only 0.99.27 exists); BRIE2 "0.2.4+" vs installed 2.3.0; SKILL.md is a 447-line monolith with no references/; MARVEL dts needs twosamples which is not installed with it.',
   'root_cause': 'Version line and metadata not refreshed.', 'fix': 'Correct the version line, set tool_type to mixed, split tool recipes into references/.'}
 ]
}
assert sum(1 for k in report['static_score']['categories'] if True) == 8
assert report['static_score']['subtotal'] == sum(v['score'] for v in report['static_score']['categories'].values())
assert 2 <= len(report['key_strengths']) <= 5
assert [r['priority'] for r in report['recommendations']] == sorted(r['priority'] for r in report['recommendations'])
print('static', sub, 'exec_avg', execution_avg, 'static_w', static_w, 'dyn_w', dyn_w, 'score', score, 'assertions', ap, '/', at)
with open(OUT, 'w', encoding='utf-8', newline='\n') as f:
    json.dump(report, f, ensure_ascii=False, indent=2)
json.dump(inputs, open('F:/OpenScience/audits/bio-single-cell-splicing/run/out/inputs_scored.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
