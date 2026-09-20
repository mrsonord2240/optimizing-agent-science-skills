"""Report post-processing: move `source` into meta (as the previous report did), add per-input executed/execution_note, fix two counts. Reads and rewrites the JSON as UTF-8."""
import json
p = r'F:\OpenScience\audits\bio-alignment-io\eval_report_bio-alignment-io_result.json'
j = json.load(open(p, encoding='utf-8'))
src = j.pop('source')
meta = j['meta']; meta = {**{k: v for k, v in meta.items() if k != 're_audit'}}
meta['source'] = src
meta['audit_type'] = 're-audit (second) of the fixed Skill fix/al-io2; regression of the archived first re-audit inputs plus two new inputs (5 and 8)'
meta['executed'] = True
meta['execution_note'] = 'Executed 8/8 inputs. Windows venv (Biopython 1.88, pyhmmer 0.12.3) plus WSL tools: MAFFT 7.526, HMMER 3.4, Infernal 1.1.5, HH-suite reformat.pl/hhfilter, RAxML-NG 1.2.2 and 2.0.3, PhyML 3.3.20220408 and 3.3.20260528, IQ-TREE 3.1.3, MrBayes 3.2.7, PAML 4.10.10, Foldmason. Shipped examples ran from copies; no __pycache__ in the worktree or the external clone. Previous (first re-audit) result: 85 Limited Release, 32/39 assertions.'
j['meta'] = meta
notes = {
 1: 'Executed: run/i1_examples.py (examples copied to run/scratch, removed afterwards).',
 2: 'Executed: run/i2_stockholm.py, run/i2b_rfam_real.py, run/i2b_infernal.sh (WSL cmbuild/hmmbuild). Real Pfam PF00042 and Rfam RF00005; SYNTHETIC data/synthetic_rna.sto.',
 3: 'Executed: run/i3_phylip.py, run/i3b_blocks.py, run/i3c_streaming.py. Real Pfam ids and NCBI ids; SYNTHETIC name-collision alignments.',
 4: 'Executed: run/i4_maf.py (real UCSC MAF, UCSC REST API ground truth), run/i4b_a2m.sh (WSL hmmbuild/hmmalign/reformat.pl/hhfilter), run/i4b_a2m.py.',
 5: 'Executed: run/i5_mafft.sh, run/i5_e2e_prep.py, run/i5_tools.sh (MrBayes, IQ-TREE, RAxML-NG, codeml in WSL), run/i5_check.py. Real RefSeq HBB CDS and UniProt globins.',
 6: 'Executed: run/i6_format_table.py (75 probes with i6c), run/i6c_foldmason.sh, run/i6c_foldmason_read.py. Real Pfam, Biopython test MSF/Mauve files, PDB structures; SYNTHETIC PSL/chain one-liners.',
 7: 'Executed: run/i7_prep.py, run/i7b_prep.py, run/i7_recipe.py, run/i7_tools.sh (RAxML-NG x2, PhyML x2, IQ-TREE, MrBayes in WSL), run/i7_check.py. Real Pfam rows; SYNTHETIC injected characters labelled in the scripts.',
 8: 'Executed: run/i8_infer.py (15 cases through the shipped script), run/i8_mb_prep.py, run/i8_mb.sh, run/i8_mb_check.py (MrBayes on datatype=rna). Real HBB/Rfam/Pfam/UniProt; SYNTHETIC substitutions and tiny cases labelled.',
}
for i in j['dynamic_score']['inputs']:
    i['executed'] = True; i['execution_note'] = notes[i['index']]
i7 = j['dynamic_score']['inputs'][6]; i7['note'] = i7['note'].replace('26/26 probes', '30 probes, all pass')
j['key_strengths'] = [s.replace('the 75-cell format table', 'the 75 format-table probes') for s in j['key_strengths']]
json.dump(j, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print('ok', list(j.keys()))
