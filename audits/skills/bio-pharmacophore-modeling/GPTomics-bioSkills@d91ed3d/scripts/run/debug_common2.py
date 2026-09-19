from rdkit import Chem
from pharmacophore_example import get_feature_factory, molecule_features, shared_feature_types_prefilter
from rdkit.Chem import AllChem

indinavir  = "CC(C)(C)NC(=O)[C@@H]1CN(Cc2cccnc2)CCN1C[C@@H](O)C[C@@H](Cc1ccccc1)C(=O)N[C@H]1c2ccccc2C[C@H]1O"
saquinavir = "CC(C)(C)NC(=O)[C@@H]1C[C@@H]2CCCC[C@@H]2CN1CC(O)[C@H](Cc1ccccc1)NC(=O)[C@@H](CC(N)=O)NC(=O)c1ccc2ccccc2n1"

factory = get_feature_factory()
for name, smi in [("indinavir", indinavir), ("saquinavir", saquinavir)]:
    m = Chem.AddHs(Chem.MolFromSmiles(smi))
    AllChem.EmbedMultipleConfs(m, numConfs=3, params=AllChem.ETKDGv3())
    AllChem.MMFFOptimizeMoleculeConfs(m)
    feats = molecule_features(m, factory)
    types = sorted(set((f[0], f[1]) for f in feats))
    print(name, "n_feature_hits:", len(feats), "n_conformers:", m.GetNumConformers())
    for t in types:
        print("   ", t)

active_mols = [Chem.MolFromSmiles(indinavir), Chem.MolFromSmiles(saquinavir)]
common = shared_feature_types_prefilter(active_mols, factory, n_conf=5)
print("COMMON (skill's own function):", sorted(common))
