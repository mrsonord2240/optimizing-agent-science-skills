"""
Re-auditor Input 6 (new, not part of the original 5 or the fixer's checks):
"I docked a chiral fragment blind (no reference structure) and used the
Skill's 'dock' config to QC it. Does PoseBusters actually catch a
chirality-inverted pose in that mode, or only under redock?"

Uses a molecule not present anywhere else in this audit: (R)-1-phenylethanol,
a simple chiral drug-fragment-like molecule with one stereocenter, unrelated
to the benzamidine/3PTB system used throughout. Builds a genuine
stereo-inverted "docked" pose (same heavy-atom framework, opposite
configuration at the stereocenter) and checks whether 'dock' and 'mol'
configs actually flag it, versus 'redock' with the correct enantiomer as
mol_true.
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from posebusters import PoseBusters

R_smiles = "C[C@H](O)c1ccccc1"   # (R)-1-phenylethanol
S_smiles = "C[C@@H](O)c1ccccc1"  # (S)-1-phenylethanol -- inverted stereocenter

def embed(smi, seed):
    m = Chem.MolFromSmiles(smi)
    m = Chem.AddHs(m)
    params = AllChem.ETKDGv3()
    params.randomSeed = seed
    AllChem.EmbedMolecule(m, params)
    AllChem.MMFFOptimizeMolecule(m)
    return m

true_mol = embed(R_smiles, seed=42)     # the "reference"/correct enantiomer
pred_mol = embed(S_smiles, seed=42)     # the "docked pose" -- wrong stereocenter

for name, m in [('true_R.sdf', true_mol), ('pred_S_inverted.sdf', pred_mol)]:
    w = Chem.SDWriter(f'../data/{name}')
    w.write(m)
    w.close()

print("=== redock config, mol_true = correct (R) enantiomer, mol_pred = inverted (S) ===")
bust_redock = PoseBusters(config='redock')
r1 = bust_redock.bust(mol_pred='../data/pred_S_inverted.sdf', mol_true='../data/true_R.sdf', mol_cond='../data/receptor.pdb')
print("columns:", list(r1.columns))
print("tetrahedral_chirality:", bool(r1['tetrahedral_chirality'].iloc[0]) if 'tetrahedral_chirality' in r1.columns else 'N/A (no column)')

print()
print("=== dock config, mol_pred = inverted (S) pose alone, no reference ===")
bust_dock = PoseBusters(config='dock')
r2 = bust_dock.bust(mol_pred='../data/pred_S_inverted.sdf', mol_cond='../data/receptor.pdb')
print("columns:", list(r2.columns))
print("has tetrahedral_chirality column:", 'tetrahedral_chirality' in r2.columns)
bool_cols2 = [c for c in r2.select_dtypes(include='bool').columns]
pb_valid2 = bool(r2[bool_cols2].all(axis=1).iloc[0])
print("pb_valid under dock config (chirality inversion NOT checkable here):", pb_valid2)

print()
print("=== mol config, mol_pred = inverted (S) pose alone ===")
bust_mol = PoseBusters(config='mol')
r3 = bust_mol.bust(mol_pred='../data/pred_S_inverted.sdf')
print("columns:", list(r3.columns))
print("has tetrahedral_chirality column:", 'tetrahedral_chirality' in r3.columns)
