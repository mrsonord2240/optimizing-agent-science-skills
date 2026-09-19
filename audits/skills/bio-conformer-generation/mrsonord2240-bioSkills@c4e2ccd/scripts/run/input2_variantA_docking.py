"""Input 2 (Variant A, regression): single low-energy ibuprofen conformer for docking, SDF output."""
from rdkit import Chem
from rdkit.Chem import AllChem

ibuprofen = 'CC(C)CC1=CC=C(C=C1)C(C)C(=O)O'
mol = Chem.MolFromSmiles(ibuprofen)
if mol is None:
    raise ValueError(f'Invalid SMILES: {ibuprofen!r}')
mol = Chem.AddHs(mol)
params = AllChem.ETKDGv3()
params.randomSeed = 42
params.useRandomCoords = True
embed_status = AllChem.EmbedMolecule(mol, params)
print(f'Embed status: {embed_status}')
if not AllChem.MMFFHasAllMoleculeParams(mol):
    raise ValueError('MMFF parameters unavailable')
opt_status = AllChem.MMFFOptimizeMolecule(mol, mmffVariant='MMFF94s', maxIters=1000)
print(f'Optimize status: {opt_status}')
mmff_props = AllChem.MMFFGetMoleculeProperties(mol, mmffVariant='MMFF94s')
ff = AllChem.MMFFGetMoleculeForceField(mol, mmff_props)
energy = ff.CalcEnergy()
print(f'Energy: {energy:.4f} kcal/mol')

conf = mol.GetConformer()
zs = [conf.GetAtomPosition(i).z for i in range(mol.GetNumAtoms())]
print(f'Z range: {min(zs):.2f} to {max(zs):.2f} (non-planar check)')

sdf_path = 'ibuprofen_docking_input.sdf'
w = Chem.SDWriter(sdf_path)
w.write(mol)
w.close()

# round-trip
mol2 = next(Chem.SDMolSupplier(sdf_path, removeHs=False))
conf2 = mol2.GetConformer()
zs2 = [conf2.GetAtomPosition(i).z for i in range(mol2.GetNumAtoms())]
print(f'Round-trip Z range: {min(zs2):.2f} to {max(zs2):.2f}')
print(f'Round-trip atom count matches: {mol2.GetNumAtoms() == mol.GetNumAtoms()}')
