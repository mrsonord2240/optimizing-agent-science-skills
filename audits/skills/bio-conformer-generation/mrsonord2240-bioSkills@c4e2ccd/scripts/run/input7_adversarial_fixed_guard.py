"""Input 7 (Adversarial, regression, CRITICAL): verify the P1 fix -- gen_conformers() on malformed
SMILES now raises ValueError, using a DIFFERENT malformed string than the fix log used
(fixer used 'C1CC(not_a_smiles'). Also re-checks determinism."""
from rdkit import Chem
from rdkit.Chem import AllChem


def gen_conformers(smiles, n_conf=20, seed=42):
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        raise ValueError(f'Invalid SMILES: {smiles!r}')
    mol = Chem.AddHs(mol)
    params = AllChem.ETKDGv3()
    params.randomSeed = seed
    params.useRandomCoords = True
    params.maxIterations = 1000
    ids = AllChem.EmbedMultipleConfs(mol, numConfs=n_conf, params=params)
    return mol, list(ids)


bad_smiles_list = [
    'Xyz[[[invalid',      # nonsense token soup, different from fixer's example
    'c1ccccc1(((',        # unbalanced parens on a real ring
    '',                   # empty string
]

for bad in bad_smiles_list:
    print(f'--- Testing malformed SMILES: {bad!r} ---')
    try:
        gen_conformers(bad)
        print('UNEXPECTED: no exception raised')
    except ValueError as e:
        print(f'Got expected ValueError: {e}')
    except Exception as e:
        print(f'FAIL -- got a DIFFERENT exception type: {type(e).__name__}: {e}')

print('\n--- Determinism check: two independent seeded runs, sorted energies ---')


def run_and_get_energies(smiles, seed):
    mol, ids = gen_conformers(smiles, n_conf=15, seed=seed)
    mmff_props = AllChem.MMFFGetMoleculeProperties(mol, mmffVariant='MMFF94s')
    energies = []
    for cid in ids:
        ff = AllChem.MMFFGetMoleculeForceField(mol, mmff_props, confId=cid)
        ff.Minimize(maxIts=1000)
        energies.append(round(ff.CalcEnergy(), 6))
    return sorted(energies)


caffeine = 'Cn1cnc2c1c(=O)n(C)c(=O)n2C'
run1 = run_and_get_energies(caffeine, seed=7)
run2 = run_and_get_energies(caffeine, seed=7)
print(f'Run 1 == Run 2 (seed=7, bit-identical sorted energies): {run1 == run2}')

run3 = run_and_get_energies(caffeine, seed=99)
print(f'Different seed (99) gives different result: {run1 != run3}')
