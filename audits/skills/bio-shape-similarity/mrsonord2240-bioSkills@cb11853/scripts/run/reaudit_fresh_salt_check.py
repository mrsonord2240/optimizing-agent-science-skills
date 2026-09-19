"""
Re-audit fresh case (not used by the fixer or the original audit): a different
disconnected-fragment / salt SMILES than the original audit's organometallic
[Fe+2].[Cl-].[Cl-] test case -- diphenhydramine hydrochloride, an ordinary small-molecule
drug salt with an organic cation and a chloride counter-ion. Confirms the fixed
disconnected-fragment guard rejects it with a clear reason, and that a normal
single-fragment molecule is unaffected.
"""
from rdkit import Chem
from rdkit.Chem import AllChem, rdMolAlign, rdShapeHelpers

SEED = 42


def shape_search_ensemble(query_mol, library_mols, n_conf=20):
    hits = []
    dropped = []
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
            scores.append(1.0 - rdShapeHelpers.ShapeTanimotoDist(target, query_mol, confId1=c))
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
query_mol = embed_query(QUERY_SMI)

# Fresh, never-used-before test set: diphenhydramine HCl (salt) + a clean control molecule.
DIPHENHYDRAMINE_HCL = 'CN(C)CCOC(c1ccccc1)c1ccccc1.Cl'
CONTROL = 'CC(=O)Nc1ccc(C(=O)c2ccc(F)cc2)cc1'  # ordinary single-fragment molecule

library_mols = [Chem.MolFromSmiles(DIPHENHYDRAMINE_HCL), Chem.MolFromSmiles(CONTROL)]

print("n_frags(diphenhydramine.HCl) =", len(Chem.GetMolFrags(library_mols[0])))
print("MMFFHasAllMoleculeParams(diphenhydramine.HCl) =",
      AllChem.MMFFHasAllMoleculeParams(library_mols[0]))

results = shape_search_ensemble(query_mol, library_mols, n_conf=20)

print("\n=== Results ===")
for target, score in results:
    smi = Chem.MolToSmiles(Chem.RemoveHs(target))
    print(f"best_shape={score:.4f}  smiles={smi}")

assert len(results) == 1, f"expected exactly 1 scored molecule (salt rejected), got {len(results)}"
scored_smi = Chem.MolToSmiles(Chem.RemoveHs(results[0][0]))
assert scored_smi == Chem.CanonSmiles(CONTROL), "wrong molecule survived"
print("\nPASS: salt correctly rejected with a clear reason; control molecule scored normally")
