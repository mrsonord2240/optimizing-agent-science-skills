"""
Input 4 (Variant B): "For each library compound, generate 20 conformers; find best-shape
conformer match to query. Use Open3DAlign."

Runs SKILL.md's shape_search_ensemble() function verbatim (Conformer-Ensemble Shape
Searching section) against a small synthetic library.
"""
from rdkit import Chem
from rdkit.Chem import AllChem, rdMolAlign, rdShapeHelpers

SEED = 42


def shape_search_ensemble(query_mol, library_mols, n_conf=20):
    hits = []
    for target in library_mols:
        target = Chem.AddHs(target)
        params = AllChem.ETKDGv3()
        params.randomSeed = SEED
        ids = list(AllChem.EmbedMultipleConfs(target, numConfs=n_conf, params=params))
        if not ids:
            continue
        if not AllChem.MMFFHasAllMoleculeParams(target):
            continue
        optimization = AllChem.MMFFOptimizeMoleculeConfs(target)
        if any(status != 0 for status, _ in optimization):
            continue

        scores = []
        for c in range(target.GetNumConformers()):
            O3A = rdMolAlign.GetO3A(target, query_mol, prbCid=c)
            O3A.Align()
            scores.append(1.0 - rdShapeHelpers.ShapeTanimotoDist(
                target, query_mol, confId1=c,
            ))
        if scores:
            hits.append((target, max(scores)))
    return sorted(hits, key=lambda x: x[1], reverse=True)


def embed_query(smi):
    mol = Chem.MolFromSmiles(smi)
    mol = Chem.AddHs(mol)
    params = AllChem.ETKDGv3()
    params.randomSeed = SEED
    AllChem.EmbedMolecule(mol, params)
    AllChem.MMFFOptimizeMolecule(mol)
    return mol


QUERY_SMI = 'CC(=O)Nc1ccc(C(=O)c2ccccc2)cc1'
LIBRARY_SMI = {
    'lib_A': 'CC(=O)Nc1ccc(C(=O)c2ccc(F)cc2)cc1',
    'lib_B': 'O=S(=O)(c1ccccc1)Nc2ccc(C(=O)c3ccccc3)cc2',
    'lib_C': 'CCCCCCCC',  # flexible, unrelated
}

query_mol = embed_query(QUERY_SMI)
library_mols = [Chem.MolFromSmiles(smi) for smi in LIBRARY_SMI.values()]
names = list(LIBRARY_SMI.keys())

results = shape_search_ensemble(query_mol, library_mols, n_conf=20)

print("=== Conformer-ensemble shape search (n_conf=20, best conformer per molecule) ===")
for target, score in results:
    smi = Chem.MolToSmiles(Chem.RemoveHs(target))
    print(f"best_shape={score:.4f}  n_conformers_used={target.GetNumConformers()}  smiles={smi}")

assert len(results) == len(LIBRARY_SMI), "expected all 3 library molecules to embed successfully"
assert all(0.0 <= s <= 1.0 for _, s in results), "shape scores must be in [0,1]"
print("\nAssertion PASSED: all 3 molecules processed, all shape scores in [0,1]")
