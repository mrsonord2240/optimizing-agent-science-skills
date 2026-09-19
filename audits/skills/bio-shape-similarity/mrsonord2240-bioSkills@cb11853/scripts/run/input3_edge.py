"""
Input 3 (Edge): "Run a shape search where the library includes an invalid SMILES and a
molecule that has no MMFF parameters. Show me how the Skill handles these failures."

Exercises the exact failure-handling branches the Skill documents: Chem.MolFromSmiles
returning None, AllChem.EmbedMultipleConfs returning no conformer ids, and
AllChem.MMFFHasAllMoleculeParams returning False (e.g. for an organometallic/hypervalent
species MMFF does not parameterize).
"""
from rdkit import Chem
from rdkit.Chem import AllChem

SEED = 42


def prepare_mol_3d(smiles, n_conf=10, seed=SEED):
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        raise ValueError(f'Invalid SMILES, could not parse: {smiles!r}')
    mol = Chem.AddHs(mol)
    params = AllChem.ETKDGv3()
    params.randomSeed = seed
    ids = list(AllChem.EmbedMultipleConfs(mol, numConfs=n_conf, params=params))
    if not ids:
        raise ValueError(f'Embedding failed for {smiles!r}')
    if not AllChem.MMFFHasAllMoleculeParams(mol):
        raise ValueError(f'MMFF parameters unavailable for {smiles!r}')
    optimization = AllChem.MMFFOptimizeMoleculeConfs(mol, maxIters=1000)
    failed = [ids[i] for i, (status, _) in enumerate(optimization) if status != 0]
    if failed:
        raise RuntimeError(f'MMFF optimization did not converge for conformers {failed}')
    return mol


TEST_CASES = [
    ('valid', 'CC(=O)Nc1ccc(C(=O)c2ccccc2)cc1'),
    ('malformed_smiles', 'C1CC(this is not smiles'),
    ('organometallic_no_mmff', '[Fe+2].[Cl-].[Cl-]'),  # ferrous chloride: MMFF has no metal params
    ('empty_string', ''),
]

print("=== Failure-mode handling per SKILL.md / example pattern ===")
for label, smi in TEST_CASES:
    try:
        mol = prepare_mol_3d(smi)
        print(f"{label:25s} SUCCESS  ({smi!r}) -> {mol.GetNumConformers()} conformers")
    except (ValueError, RuntimeError) as e:
        print(f"{label:25s} HANDLED  ({smi!r}) -> {type(e).__name__}: {e}")
    except Exception as e:
        print(f"{label:25s} UNHANDLED EXCEPTION ({smi!r}) -> {type(e).__name__}: {e}")
