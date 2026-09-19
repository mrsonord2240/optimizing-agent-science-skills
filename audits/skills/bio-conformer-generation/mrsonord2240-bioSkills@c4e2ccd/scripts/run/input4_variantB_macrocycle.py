"""Input 4 (Variant B, regression + extended): macrocycle-aware embedding on a 14-membered ring,
comparing macrocycle-aware vs default settings (same check the original audit used)."""
from rdkit import Chem
from rdkit.Chem import AllChem


def macrocycle_conformers(smiles, n_conf=50, seed=42):
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        raise ValueError(f'Invalid SMILES: {smiles!r}')
    mol = Chem.AddHs(mol)
    params = AllChem.ETKDGv3()
    params.randomSeed = seed
    params.useRandomCoords = True
    params.useMacrocycleTorsions = True
    params.useSmallRingTorsions = True
    params.maxIterations = 5000
    ids = list(AllChem.EmbedMultipleConfs(mol, numConfs=n_conf, params=params))
    if not ids:
        raise RuntimeError(f'No macrocycle conformers embedded for {smiles!r}')
    return mol, ids


# 14-membered simple macrocycle
macrocycle_smiles = 'C1CCCCCCCCCCCCC1'
mol = Chem.MolFromSmiles(macrocycle_smiles)
ring_sizes = [len(r) for r in mol.GetRingInfo().AtomRings()]
print(f'Ring sizes: {ring_sizes}')

mol_macro, ids_macro = macrocycle_conformers(macrocycle_smiles, n_conf=50)
print(f'Macrocycle-aware embedded: {len(ids_macro)}/50')

# default (non-macrocycle) comparison
mol2 = Chem.AddHs(Chem.MolFromSmiles(macrocycle_smiles))
params_default = AllChem.ETKDGv3()
params_default.randomSeed = 42
params_default.useRandomCoords = True
ids_default = list(AllChem.EmbedMultipleConfs(mol2, numConfs=50, params=params_default))
print(f'Default (non-macrocycle) embedded: {len(ids_default)}/50')
print('Note: a plain saturated carbocycle is not a stressing case for useMacrocycleTorsions -- '
      'consistent with the original audit finding (P2, left unfixed by design).')
