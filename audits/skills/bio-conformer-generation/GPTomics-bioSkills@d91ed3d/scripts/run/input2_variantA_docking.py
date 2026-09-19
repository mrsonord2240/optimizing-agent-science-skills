# Input 2 (Variant A): "Generate a single low-energy ETKDGv3 + MMFF94 conformer
# for ibuprofen; write to multi-SDF for downstream Vina docking."
# Following SKILL.md "Single initial 3D structure" row of the Decision Tree
# + Force-Field Optimization section.

from rdkit import Chem
from rdkit.Chem import AllChem

ibuprofen = 'CC(C)Cc1ccc(cc1)C(C)C(=O)O'
mol = Chem.MolFromSmiles(ibuprofen)
mol = Chem.AddHs(mol)

params = AllChem.ETKDGv3()
params.randomSeed = 42
params.useRandomCoords = True
embed_status = AllChem.EmbedMolecule(mol, params)
print(f'EmbedMolecule status: {embed_status} (0 = success, -1 = failure)')

if not AllChem.MMFFHasAllMoleculeParams(mol):
    raise ValueError('MMFF parameters unavailable for ibuprofen')
opt_status = AllChem.MMFFOptimizeMolecule(mol, mmffVariant='MMFF94s', maxIters=1000)
print(f'MMFFOptimizeMolecule status: {opt_status} (0 = converged)')

props = AllChem.MMFFGetMoleculeProperties(mol, mmffVariant='MMFF94s')
ff = AllChem.MMFFGetMoleculeForceField(mol, props)
energy = ff.CalcEnergy()
print(f'Final MMFF94s energy: {energy:.4f} kcal/mol')

out_path = 'input2_ibuprofen.sdf'
writer = Chem.SDWriter(out_path)
mol.SetProp('_Name', 'ibuprofen_docking_conf')
mol.SetProp('MMFF94s_energy_kcal_mol', f'{energy:.4f}')
writer.write(mol)
writer.close()
print(f'Wrote {out_path}')

# Verify the SDF round-trips and preserves 3D coords (not a degenerate/flat structure)
check = next(Chem.SDMolSupplier(out_path, removeHs=False))
conf = check.GetConformer()
zs = [conf.GetAtomPosition(i).z for i in range(check.GetNumAtoms())]
print(f'Round-tripped atoms: {check.GetNumAtoms()}, z-coordinate range: {min(zs):.3f} to {max(zs):.3f}')
print(f'Non-planar (real 3D): {(max(zs) - min(zs)) > 0.5}')
