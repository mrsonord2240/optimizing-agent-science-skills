"""Phase-2 Input 4: current SKILL.md MAGeCK MLE invocation on prior HAP1 subset."""
from pathlib import Path
import subprocess
import sys
import pandas as pd

run = Path(__file__).resolve().parent
mageck = r"F:\OpenScience\audit-envs\crispr-screen-analyst\Scripts\mageck"
counts = run / 'mageck' / 'input4_mle_counts.txt'
design = run / 'mageck' / 'input4_design.txt'
prefix = run / 'mageck' / 'phase2_batch_aware_mle'
cmd = [sys.executable, mageck, 'mle', '--count-table', str(counts), '--design-matrix', str(design), '--permutation-round', '10', '--output-prefix', str(prefix)]
print('INPUT 4 Variant B:', ' '.join(cmd))
completed = subprocess.run(cmd, capture_output=True, text=True)
print(completed.stdout[-2500:])
print(completed.stderr[-1500:])
assert completed.returncode == 0, completed.stderr
help_text = subprocess.run([sys.executable, mageck, 'mle', '--help'], capture_output=True, text=True, check=True).stdout
assert '--permutation-round' in help_text
result = pd.read_csv(str(prefix) + '.gene_summary.txt', sep='\t')
beta_cols = [c for c in result if c.endswith('|beta')]
assert beta_cols and result[beta_cols].notna().all().all()
print(f'ASSERT input4: {len(result)} genes, {len(beta_cols)} beta columns, zero NaN betas, documented flag accepted')
print('PHASE2_MAGECK_PASS')
