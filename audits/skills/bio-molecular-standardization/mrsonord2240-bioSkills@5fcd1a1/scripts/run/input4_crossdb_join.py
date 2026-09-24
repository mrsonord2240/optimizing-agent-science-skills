# Input 4 (Variant B) -- bio-molecular-standardization
# Join a ChEMBL export against a synthetic in-house registry. Measure InChIKey
# overlap (a) raw, (b) after the ChEMBL pipeline, (c) after ChEMBL + tautomer
# canonicalization + stereo removal, against known ground truth.
import pandas as pd
from rdkit import Chem, RDLogger
from rdkit.Chem.MolStandardize import rdMolStandardize
from chembl_structure_pipeline import standardize_mol, get_parent_mol

RDLogger.DisableLog('rdApp.*')
enum = rdMolStandardize.TautomerEnumerator()

CHEMBL = r"F:\OpenScience\audit-envs\cheminformatics-hit-triage-analyst\public-data\chembl_herg_CHEMBL240_ic50.csv"
INHOUSE = r"F:\OpenScience\audits\bio-molecular-standardization\data\inhouse_registry_synthetic.csv"

a = pd.read_csv(CHEMBL).dropna(subset=['canonical_smiles']).drop_duplicates(
    'molecule_chembl_id').head(300).reset_index(drop=True)
b = pd.read_csv(INHOUSE)
print(f"[load] chembl side={len(a)}  in-house side={len(b)}  ground-truth pairs=300")


def key_raw(smi):
    m = Chem.MolFromSmiles(smi)
    return None if m is None else Chem.MolToInchiKey(m)


def key_chembl(smi):
    m = Chem.MolFromSmiles(smi)
    if m is None:
        return None
    p, excl = get_parent_mol(standardize_mol(m))
    return None if excl else Chem.MolToInchiKey(p)


def key_full(smi):
    m = Chem.MolFromSmiles(smi)
    if m is None:
        return None
    p, excl = get_parent_mol(standardize_mol(m))
    if excl:
        return None
    for at in p.GetAtoms():
        at.SetIsotope(0)
    p = enum.Canonicalize(p)
    Chem.RemoveStereochemistry(p)
    return Chem.MolToInchiKey(p)


for name, fn in [('raw InChIKey', key_raw),
                 ('ChEMBL pipeline', key_chembl),
                 ('ChEMBL + isotope strip + tautomer canon + stereo strip', key_full)]:
    ka = a.canonical_smiles.map(fn)
    kb = b.smiles.map(fn)
    lut = dict(zip(ka, a.molecule_chembl_id))
    hit = [lut.get(k) == src for k, src in zip(kb, b.source_chembl_id)]
    n = sum(1 for h in hit if h)
    per = b.assign(hit=hit).groupby('perturbation').hit.mean().mul(100).round(0).astype(int)
    print(f"\n[{name}] recovered {n}/300 correct joins ({100*n/300:.1f}%)")
    print("   by perturbation (% recovered): " +
          "  ".join(f"{k}={v}" for k, v in per.items()))
