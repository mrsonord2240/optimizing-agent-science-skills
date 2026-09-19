"""
Audit Input 1 (Canonical) — bio-pose-validation
Prompt: "Run PoseBusters dock config on my docked benzamidine pose (from AutoDock
Vina against 3PTB trypsin) and receptor.pdb. Output a table per pose with each
check pass/fail. Filter to PB-valid; rank by Vina score."
Follows the Skill's "Python Library API" section verbatim (PoseBusters(config='dock')
+ AND-aggregate boolean check columns into pb_valid).
"""
from posebusters import PoseBusters
import pandas as pd

bust = PoseBusters(config='dock')

results = bust.bust(
    mol_pred='../data/mode1_fixed.sdf',
    mol_cond='../data/receptor.pdb',
)

check_cols = [
    col for col in results.select_dtypes(include='bool').columns
    if not col.lower().startswith('rmsd')
]
results['pb_valid'] = results[check_cols].all(axis=1)

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 200)
print("Columns returned:", list(results.columns))
print()
print(results[check_cols + ['pb_valid']].T)
print()
valid = results[results['pb_valid']]
print(f'{len(valid)} / {len(results)} poses are PB-valid')
