"""
Audit Input 3 (Edge) — bio-pose-validation
Prompt: "I have three docked poses I'm not sure about — one may clash with the
receptor, one has a stretched bond, one has a puckered ring. Run PoseBusters
and tell me exactly which checks fail for each, and confirm the good pose
still passes."
"""
from posebusters import PoseBusters
import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 250)

print("=== clash_pose.sdf (dock config, vs receptor) ===")
bust = PoseBusters(config='dock')
r = bust.bust(mol_pred='../data/clash_pose.sdf', mol_cond='../data/receptor.pdb')
check_cols = [c for c in r.select_dtypes(include='bool').columns if not c.lower().startswith('rmsd')]
r['pb_valid'] = r[check_cols].all(axis=1)
failed = [c for c in check_cols if not bool(r[c].iloc[0])]
print("pb_valid:", bool(r['pb_valid'].iloc[0]), "| failed checks:", failed)

print()
print("=== stretched_bond.sdf (mol config, ligand-only) ===")
bust_mol = PoseBusters(config='mol')
r2 = bust_mol.bust(mol_pred='../data/stretched_bond.sdf')
check_cols2 = [c for c in r2.select_dtypes(include='bool').columns]
r2['pb_valid'] = r2[check_cols2].all(axis=1)
failed2 = [c for c in check_cols2 if not bool(r2[c].iloc[0])]
print("pb_valid:", bool(r2['pb_valid'].iloc[0]), "| failed checks:", failed2)

print()
print("=== puckered_ring.sdf (mol config, ligand-only) ===")
r3 = bust_mol.bust(mol_pred='../data/puckered_ring.sdf')
check_cols3 = [c for c in r3.select_dtypes(include='bool').columns]
r3['pb_valid'] = r3[check_cols3].all(axis=1)
failed3 = [c for c in check_cols3 if not bool(r3[c].iloc[0])]
print("pb_valid:", bool(r3['pb_valid'].iloc[0]), "| failed checks:", failed3)

print()
print("=== control: good pose (mode1_fixed.sdf) under mol config, should pass everything ===")
r4 = bust_mol.bust(mol_pred='../data/mode1_fixed.sdf')
check_cols4 = [c for c in r4.select_dtypes(include='bool').columns]
r4['pb_valid'] = r4[check_cols4].all(axis=1)
print("pb_valid:", bool(r4['pb_valid'].iloc[0]))
