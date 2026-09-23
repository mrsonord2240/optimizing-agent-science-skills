"""Verbatim SKILL.md ligand-based block, with only result assertions appended."""
from rdkit import Chem, Geometry
from rdkit.Chem import ChemicalFeatures
from rdkit.Chem.Pharm3D import EmbedLib, Pharmacophore
from rdkit.RDPaths import RDDataDir
import os

fdef_file = os.path.join(RDDataDir, 'BaseFeatures.fdef')
factory = ChemicalFeatures.BuildFeatureFactory(fdef_file)
query_features = [
    ChemicalFeatures.FreeChemicalFeature('Aromatic', Geometry.Point3D(0.0, 0.0, 0.0)),
    ChemicalFeatures.FreeChemicalFeature('Donor', Geometry.Point3D(4.0, 0.0, 0.0)),
]
pharmacophore = Pharmacophore.Pharmacophore(query_features)
pharmacophore.setLowerBound(0, 1, 3.5)
pharmacophore.setUpperBound(0, 1, 5.0)
target = Chem.AddHs(Chem.MolFromSmiles('c1ccc(cc1)CCN'))
can_match, feature_matches = EmbedLib.MatchPharmacophoreToMol(target, factory, pharmacophore)
if can_match:
    atom_match = tuple(tuple(matches[0].GetAtomIds()) for matches in feature_matches)
    _, embeddings, n_failed = EmbedLib.EmbedPharmacophore(target, atom_match, pharmacophore, randomSeed=23, silent=True)
else:
    embeddings, n_failed = [], -1
print("CAN_MATCH", can_match, "EMBEDDINGS", len(embeddings), "N_FAILED", n_failed)
assert can_match and len(embeddings) > 0 and n_failed == 0
print("ASSERT verbatim ligand-based application code produces valid embeddings: PASS")
