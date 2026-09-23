"""
Re-audit regression test — reproduces the ORIGINAL audit's Input 4 scenario verbatim
(query + lib_A/lib_B/lib_C SMILES, n_conf=20, seed 42) but calls the FIXED
shape_search_ensemble() copied from the fixed SKILL.md (chemoinformatics/shape-similarity,
fix/cg-shape @ cb11853), not the pre-fix version.

Pre-fix result (archived pre-fix audit, Input 4): only 1 of 3 molecules appeared
(lib_B and one of lib_A/lib_C silently vanished with zero message).
Expected post-fix result: all 3 molecules score, with printed WARNING lines for any
molecule that lost some (not all) conformers to non-convergence.
"""
from rdkit import Chem
from rdkit.Chem import AllChem, rdMolAlign, rdShapeHelpers

SEED = 42


def shape_search_ensemble(query_mol, library_mols, n_conf=20):
    hits = []
    dropped = []  # (smiles, reason) for every molecule that produced no usable score
    for target in library_mols:
        smi = Chem.MolToSmiles(target)
        if len(Chem.GetMolFrags(target)) > 1:
            dropped.append((smi, 'disconnected fragments (salt/multi-component); '
                                  'no single shape to compare'))
            continue

        target = Chem.AddHs(target)
        params = AllChem.ETKDGv3()
        params.randomSeed = SEED
        ids = list(AllChem.EmbedMultipleConfs(target, numConfs=n_conf, params=params))
        if not ids:
            dropped.append((smi, 'embedding failed for all requested conformers'))
            continue
        if not AllChem.MMFFHasAllMoleculeParams(target):
            dropped.append((smi, 'MMFF parameters unavailable'))
            continue

        optimization = AllChem.MMFFOptimizeMoleculeConfs(target)
        converged_ids = [cid for cid, (status, _) in zip(ids, optimization) if status == 0]
        n_failed = len(ids) - len(converged_ids)
        if n_failed:
            print(f'WARNING: {smi}: {n_failed}/{len(ids)} conformers failed MMFF '
                  f'convergence; scoring the remaining {len(converged_ids)}')
        if not converged_ids:
            dropped.append((smi, f'all {len(ids)} conformers failed MMFF convergence'))
            continue

        scores = []
        for c in converged_ids:
            O3A = rdMolAlign.GetO3A(target, query_mol, prbCid=c)
            O3A.Align()
            scores.append(1.0 - rdShapeHelpers.ShapeTanimotoDist(
                target, query_mol, confId1=c,
            ))
        hits.append((target, max(scores)))

    if dropped:
        print(f'WARNING: {len(dropped)} library molecule(s) produced no usable '
              f'conformer and were dropped:')
        for smi, reason in dropped:
            print(f'  {smi}: {reason}')
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

print(f"\nn_scored = {len(results)} / {len(LIBRARY_SMI)} library molecules")
assert len(results) == len(LIBRARY_SMI), (
    f"REGRESSION: expected all {len(LIBRARY_SMI)} library molecules to score, "
    f"got {len(results)}"
)
assert all(0.0 <= s <= 1.0 for _, s in results), "shape scores must be in [0,1]"
print("PASS: all 3 molecules scored, all shape scores in [0,1]")
