"""Parse and assert on the completed Phase-2 MAGeCK output (Input 4)."""
from pathlib import Path
import subprocess
import sys
import pandas as pd

run = Path(__file__).resolve().parent
prefix = run / 'mageck' / 'phase2_batch_aware_mle'
table = Path(str(prefix) + '.gene_summary.txt')
assert table.exists() and table.stat().st_size > 1000
df = pd.read_csv(table, sep='\t')
beta_columns = [c for c in df.columns if c.endswith('|beta')]
assert beta_columns, df.columns.tolist()
assert df[beta_columns].notna().all().all(), 'NaN beta found'
mageck = r'F:\OpenScience\audit-envs\crispr-screen-analyst\Scripts\mageck'
help_text = subprocess.run([sys.executable, mageck, 'mle', '--help'], capture_output=True, text=True, check=True).stdout
assert '--permutation-round' in help_text
print(f'ASSERT input4: completed documented MAGeCK MLE output: {len(df)} genes, {len(beta_columns)} beta columns, zero NaN beta values; --permutation-round advertised by --help')
print('PHASE2_MAGECK_POSTRUN_ASSERT_PASS')
