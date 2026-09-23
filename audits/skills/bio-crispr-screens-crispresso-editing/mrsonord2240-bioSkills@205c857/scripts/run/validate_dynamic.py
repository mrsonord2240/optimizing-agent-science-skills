import json
import sys
from pathlib import Path
import pandas as pd

root = Path(sys.argv[1])
checks = {}

def quant(path):
    return pd.read_csv(path, sep='\t')

q1 = quant(root / 'input1_cas9/out1/CRISPResso_on_canonical/CRISPResso_quantification_of_editing_frequency.txt')
checks['cas9_modified_pct'] = float(q1.loc[q1.Amplicon == 'Reference', 'Modified%'].iloc[0])
assert abs(checks['cas9_modified_pct'] - 26.38297872) < 1e-6
q2path = root / 'input2_cbe/out2/CRISPResso_on_cbe/Quantification_window_nucleotide_percentage_table.txt'
assert q2path.exists() and q2path.stat().st_size > 100
checks['cbe_window_table_bytes'] = q2path.stat().st_size
wrong_log = (root / 'input3_wrong_locus/container.log').read_text(encoding='utf-16')
assert int((root / 'input3_wrong_locus/exit_code.txt').read_text(encoding='utf-8-sig').strip()) == 0
assert 'ERROR: No alignments were found' in wrong_log
assert not (root / 'input3_wrong_locus/out3/CRISPResso_on_wrong_locus/CRISPResso_quantification_of_editing_frequency.txt').exists()
checks['wrong_locus_error_reported'] = True
pool = pd.read_csv(root / 'input4_pooled/out4/CRISPRessoPooled_on_Both.Cas9/SAMPLES_QUANTIFICATION_SUMMARY.txt', sep='\t')
checks['pooled_rows'] = int(pool.shape[0])
assert pool.shape[0] == 2 and not pool.isna().all(axis=1).any()
batch = pd.read_csv(root / 'input5_batch/out5/CRISPRessoBatch_on_FANC.local/CRISPRessoBatch_quantification_of_editing_frequency.txt', sep='\t')
checks['batch_rows'] = int(batch.shape[0])
assert set(batch['Batch']) == {'Untreated', 'Cas9'}
assert (root / 'input5_compare/out5/compare/CRISPRessoCompare_on_Untreated_VS_Cas9/CRISPRessoCompare_RUNNING_LOG.txt').exists()
parser = json.loads((root / 'input6_parser_real.json').read_text(encoding='utf-16'))
assert parser['reads_in_input'] == 250 and parser['reads_aligned'] == 235 and abs(parser['mapping_pct'] - 94.0) < 1e-8
checks['parser_mapping_pct'] = parser['mapping_pct']
wgss = pd.read_csv(root / 'input6_wgs/out6wgs/CRISPRessoWGS_on_Both.Cas9.fastq.smallGenome/SAMPLES_QUANTIFICATION_SUMMARY.txt', sep='\t')
assert set(wgss['Name']) == {'FANCF', 'HEK3'} and not wgss.isna().all(axis=1).any()
checks['wgs_rows'] = int(wgss.shape[0])
q7 = quant(root / 'input7_be_default/out7/CRISPResso_on_be_default/CRISPResso_quantification_of_editing_frequency.txt')
assert q7.shape[0] >= 1
checks['be_default_rows'] = int(q7.shape[0])
assert (root / 'input8_shipped_script_syntax.txt').exists()
q9path = root / 'input9_abe/out9/CRISPResso_on_abe/Quantification_window_nucleotide_percentage_table.txt'
assert q9path.exists() and q9path.stat().st_size > 100
checks['abe_window_table_bytes'] = q9path.stat().st_size
q10 = quant(root / 'input10_prime/out10/CRISPResso_on_prime/CRISPResso_quantification_of_editing_frequency.txt')
assert {'Reference', 'Prime-edited', 'Scaffold-incorporated'}.issubset(set(q10['Amplicon']))
checks['prime_amplicons'] = q10['Amplicon'].tolist()
(root / 'validation.json').write_text(json.dumps(checks, indent=2) + '\n')
print(json.dumps(checks, indent=2))
