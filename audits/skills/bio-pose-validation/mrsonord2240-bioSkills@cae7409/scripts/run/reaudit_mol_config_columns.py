"""
New independent check: SKILL.md's config table says
  `mol` | Intra-ligand only (sanity, bonds, angles, rings, stereo, energy)
implying 'mol' config includes stereo checks. But the earlier paragraph says
"Double-bond stereo, chirality ... are reference checks: they only run when
mol_true is supplied (config='redock')." These two statements conflict.
Check which is true against the installed library.
"""
from posebusters import PoseBusters

bust_mol = PoseBusters(config='mol')
r = bust_mol.bust(mol_pred='../data/mode1_fixed.sdf')
cols = list(r.columns)
print("mol config columns:", cols)
print()
print("has double_bond_stereochemistry:", 'double_bond_stereochemistry' in cols)
print("has tetrahedral_chirality:", 'tetrahedral_chirality' in cols)
