"""
Independent re-auditor check: list dock vs redock config columns directly,
not reusing any fixer or auditor helper code, and cross-check against the
Skill's corrected SKILL.md claim (5-column gap: molecular_formula,
molecular_bonds, double_bond_stereochemistry, tetrahedral_chirality, RMSD).
"""
from posebusters import PoseBusters

dock = PoseBusters(config='dock')
r_dock = dock.bust(mol_pred='../data/mode1_fixed.sdf', mol_cond='../data/receptor.pdb')

redock = PoseBusters(config='redock')
r_redock = redock.bust(mol_pred='../data/mode1_fixed.sdf', mol_true='../data/ben_ref.sdf', mol_cond='../data/receptor.pdb')

dock_cols = set(r_dock.columns)
redock_cols = set(r_redock.columns)

print("dock n_cols:", len(dock_cols))
print("redock n_cols:", len(redock_cols))
diff = sorted(redock_cols - dock_cols)
print("redock-only columns:", diff)
print("dock-only columns (should be empty):", sorted(dock_cols - redock_cols))
