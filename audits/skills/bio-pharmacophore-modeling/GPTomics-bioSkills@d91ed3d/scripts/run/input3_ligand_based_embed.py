# Input 3 (Edge / single active compound) -- run SKILL.md's own
# "Ligand-Based Pharmacophore (RDKit Pharm3D)" code block verbatim, then test whether the
# 2-feature (Aromatic + Donor, bounds 3.5-5.0 A) toy pharmacophore it defines actually
# discriminates a real matching scaffold from a real non-matching one.
from rdkit import Chem, Geometry
from rdkit.Chem import ChemicalFeatures
from rdkit.Chem.Pharm3D import EmbedLib, Pharmacophore
from rdkit.RDPaths import RDDataDir
import os

fdef_file = os.path.join(RDDataDir, 'BaseFeatures.fdef')
factory = ChemicalFeatures.BuildFeatureFactory(fdef_file)

query_features = [
    ChemicalFeatures.FreeChemicalFeature(
        'Aromatic', Geometry.Point3D(0.0, 0.0, 0.0)),
    ChemicalFeatures.FreeChemicalFeature(
        'Donor', Geometry.Point3D(4.0, 0.0, 0.0)),
]
pharmacophore = Pharmacophore.Pharmacophore(query_features)
pharmacophore.setLowerBound(0, 1, 3.5)
pharmacophore.setUpperBound(0, 1, 5.0)


def try_match(name, smiles):
    target = Chem.AddHs(Chem.MolFromSmiles(smiles))
    can_match, feature_matches = EmbedLib.MatchPharmacophoreToMol(
        target, factory, pharmacophore)
    print(f"\n--- {name} ({smiles}) ---")
    print("can_match (feature-type level):", can_match)
    if not can_match:
        return
    atom_match = tuple(tuple(matches[0].GetAtomIds())
                        for matches in feature_matches)
    print("atom_match:", atom_match)
    try:
        bounds_ok, embeddings, n_failed = EmbedLib.EmbedPharmacophore(
            target, atom_match, pharmacophore, randomSeed=23, count=20, silent=True)
        print("EmbedPharmacophore: n_embeddings:", len(embeddings), "| n_failed:", n_failed)
    except ValueError as e:
        # This is the documented Common Errors row: "Pharm3D.EmbedPharmacophore fails |
        # Bounds matrix infeasible" -- i.e. the feature TYPES are present but their real
        # geometry cannot satisfy the query's distance bounds. Real, expected failure mode.
        print("EmbedPharmacophore raised (documented bounds-infeasible failure):", e)


# 1) The molecule from SKILL.md's own snippet: phenethylamine (aromatic ring + terminal NH2 donor)
try_match("SKILL.md example -- phenethylamine", "c1ccc(cc1)CCN")

# 2) Real drug that should plausibly match: tyramine, an aromatic ring + para-phenol OH donor,
#    a real endogenous trace amine / dietary compound -- distance aromatic-centroid to OH donor
#    is in a comparable range to the toy 3.5-5.0 A window.
try_match("tyramine (real compound, expected plausible match)", "Oc1ccc(CCN)cc1")

# 3) Real distractor with NO aromatic ring at all -- the aromatic feature cannot exist,
#    so this must fail at the feature-type level regardless of donor geometry.
try_match("cyclohexylamine (no aromatic ring, expected can_match=False)", "NC1CCCCC1")

# 4) Real distractor with an aromatic ring but the donor too close (ortho-aminophenol,
#    donor directly fused to the ring) -- tests whether geometry, not just feature presence,
#    is actually enforced by EmbedPharmacophore.
try_match("phenol (aromatic + donor fused on the ring, expected can_match True but embedding tests the bound)", "Oc1ccccc1")
