'''Input 1 (Canonical, regression of pre-fix Input 1): "Run MAGeCK and BAGEL2 on my
essentiality screen. Build a 2-method consensus hit list using the thresholds this
Skill's own Quantitative Thresholds table recommends."

Uses examples/consensus_hits.py (Mode B script) verbatim, real HAP1 TKOv3 data,
validated against CEGv2/NEGv1 ground truth. Regression check: does the script's
own hardcoded default (now FDR<0.05/BF>6) match the table without any override,
where pre-fix it silently used FDR<0.1/BF>5?
'''
import subprocess, sys, os
import pandas as pd

RUN = os.path.dirname(os.path.abspath(__file__))
os.chdir(RUN)

# Run the example script exactly as shipped -- it reads mageck.gene_summary.txt /
# bagel_bf.txt by hardcoded filename, so stage the real HAP1 files under those names.
import shutil
shutil.copy('mageck_hap1.gene_summary.txt', 'mageck.gene_summary.txt')
shutil.copy('bayes_factor.txt', 'bagel_bf.txt')

result = subprocess.run([sys.executable, 'examples_consensus_hits.py'],
                         capture_output=True, text=True)
print('--- STDOUT ---')
print(result.stdout)
print('--- STDERR ---')
print(result.stderr)
print('--- EXIT CODE ---', result.returncode)

assert result.returncode == 0, 'examples_consensus_hits.py did not exit cleanly'
assert os.path.exists('consensus_hits.csv'), 'expected output file missing'

out = pd.read_csv('consensus_hits.csv')
n_consensus = len(out)
print(f'\nConsensus (both methods) rows written: {n_consensus}')
assert 'WARNING' not in result.stdout, 'unexpected comparability warning on a genuinely matched MAGeCK+BAGEL2 pair'

# Validate against CEGv2 (core essential) / NEGv1 (non-essential) ground truth
# (both are tab-separated with GENE as the first column, not one bare gene per line)
ceg = set(pd.read_csv('CEGv2.txt', sep='\t')['GENE'])
neg = set(pd.read_csv('NEGv1.txt', sep='\t')['GENE'])
hit_genes = set(out['gene'])
tp = len(hit_genes & ceg)
fp_neg = len(hit_genes & neg)
precision_proxy = tp / max(1, tp + fp_neg)
print(f'CEGv2 (core essential) overlap: {tp}/{len(ceg)}')
print(f'NEGv1 (non-essential) overlap (false positives): {fp_neg}')
print(f'Precision proxy (CEGv2 hits / (CEGv2 hits + NEGv1 hits)): {precision_proxy:.4f}')
