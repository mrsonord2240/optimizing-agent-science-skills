from rdkit import Chem
from rdkit.Chem import AllChem
from pharmacophore_example import get_feature_factory, molecule_features, shared_feature_types_prefilter, has_feature_types

indinavir  = "CC(C)(C)NC(=O)[C@@H]1CN(Cc2cccnc2)CCN1C[C@@H](O)C[C@@H](Cc1ccccc1)C(=O)N[C@H]1c2ccccc2C[C@H]1O"
saquinavir = "CC(C)(C)NC(=O)[C@@H]1C[C@@H]2CCCC[C@@H]2CN1CC(O)[C@H](Cc1ccccc1)NC(=O)[C@@H](CC(N)=O)NC(=O)c1ccc2ccccc2n1"
ritonavir  = "CC(C)c1nc(CN(C)C(=O)N[C@H](C(=O)N[C@H](CC[C@H](Cc2ccccc2)NC(=O)OCc2cncs2)Cc2ccccc2)C(C)C)cs1"

factory = get_feature_factory()
active_mols = [Chem.MolFromSmiles(indinavir), Chem.MolFromSmiles(saquinavir)]
common = shared_feature_types_prefilter(active_mols, factory)   # default n_conf=20, as the real call used
print("common (n_conf=20 default):", sorted(common))

rmol = Chem.MolFromSmiles(ritonavir)
m = Chem.AddHs(rmol)
AllChem.EmbedMolecule(m, AllChem.ETKDGv3())
AllChem.MMFFOptimizeMolecule(m)
rfeats = molecule_features(m, factory)
rtypes = sorted(set((f[0], f[1]) for f in rfeats))
print("ritonavir single-conf feature types:")
for t in rtypes:
    print("   ", t)
missing = set(common) - set(rtypes)
print("MISSING from ritonavir vs common:", sorted(missing))
result = has_feature_types(list(common), rmol, factory)
print("has_feature_types result:", result)
