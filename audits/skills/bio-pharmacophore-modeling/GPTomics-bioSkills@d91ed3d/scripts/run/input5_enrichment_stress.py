# Input 5 (Stress / multi-part) -- run the Skill's own `pharmacophore_enrichment` function
# (from SKILL.md's "Pharmacophore Quality Validation" section) end to end on a real
# active/inactive set: 5 real HIV-1 protease inhibitors (actives) vs 5 real, unrelated
# marketed drugs (inactives), using the aromatic+donor 3D pharmacophore geometrically
# validated in input3 (feature-type match AND EmbedPharmacophore bounds-satisfaction).
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


def matches_pharmacophore(mol, query_pharmacophore):
    """Real geometric match: feature types present AND EmbedPharmacophore satisfies bounds."""
    target = Chem.AddHs(mol)
    can_match, feature_matches = EmbedLib.MatchPharmacophoreToMol(
        target, factory, query_pharmacophore)
    if not can_match:
        return False
    atom_match = tuple(tuple(m[0].GetAtomIds()) for m in feature_matches)
    try:
        bounds_ok, embeddings, n_failed = EmbedLib.EmbedPharmacophore(
            target, atom_match, query_pharmacophore, randomSeed=23, count=10, silent=True)
        return len(embeddings) > 0
    except ValueError:
        return False


# --- SKILL.md's own function, copied verbatim from the "Pharmacophore Quality Validation" section ---
def pharmacophore_enrichment(query_pharmacophore, actives, inactives, matches_pharmacophore):
    """Return active/inactive match-rate enrichment for a supplied matcher."""
    if not actives or not inactives:
        raise ValueError('actives and inactives must both be non-empty')
    n_active_match = sum(
        bool(matches_pharmacophore(mol, query_pharmacophore))
        for mol in actives)
    n_inactive_match = sum(
        bool(matches_pharmacophore(mol, query_pharmacophore))
        for mol in inactives)
    active_rate = n_active_match / len(actives)
    inactive_rate = n_inactive_match / len(inactives)
    return float('inf') if inactive_rate == 0 else active_rate / inactive_rate
# --- end verbatim ---


active_smiles = {
    "indinavir":  "CC(C)(C)NC(=O)[C@@H]1CN(Cc2cccnc2)CCN1C[C@@H](O)C[C@@H](Cc1ccccc1)C(=O)N[C@H]1c2ccccc2C[C@H]1O",
    "saquinavir": "CC(C)(C)NC(=O)[C@@H]1C[C@@H]2CCCC[C@@H]2CN1CC(O)[C@H](Cc1ccccc1)NC(=O)[C@@H](CC(N)=O)NC(=O)c1ccc2ccccc2n1",
    "ritonavir":  "CC(C)c1nc(CN(C)C(=O)N[C@H](C(=O)N[C@H](CC[C@H](Cc2ccccc2)NC(=O)OCc2cncs2)Cc2ccccc2)C(C)C)cs1",
    "nelfinavir": "Cc1c(O)cccc1C(=O)NC(CSc1ccccc1)C(O)CN1CC2CCCCC2CC1C(=O)NC(C)(C)C",
    "amprenavir": "CC(C)CN(C[C@@H](O)[C@H](Cc1ccccc1)NC(=O)O[C@H]1CCOC1)S(=O)(=O)c1ccc(N)cc1",
}
inactive_smiles = {
    "caffeine":      "Cn1c(=O)c2c(ncn2C)n(C)c1=O",
    "aspirin":       "CC(=O)Oc1ccccc1C(=O)O",
    "ibuprofen":     "CC(C)Cc1ccc(C(C)C(=O)O)cc1",
    "metformin":     "CN(C)C(=N)NC(=N)N",
    "acetaminophen": "CC(=O)Nc1ccc(O)cc1",
}

actives = {k: Chem.MolFromSmiles(v) for k, v in active_smiles.items()}
inactives = {k: Chem.MolFromSmiles(v) for k, v in inactive_smiles.items()}

print("Per-compound match results (aromatic-donor 3.5-5.0 A pharmacophore, geometric):")
for name, mol in list(actives.items()) + list(inactives.items()):
    role = "ACTIVE" if name in actives else "inactive"
    m = matches_pharmacophore(mol, pharmacophore)
    print(f"  [{role:8s}] {name:15s} match={m}")

enrichment = pharmacophore_enrichment(
    pharmacophore, list(actives.values()), list(inactives.values()), matches_pharmacophore)
print(f"\nEnrichment (active match rate / inactive match rate) = {enrichment}")
