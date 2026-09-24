# Builds the SYNTHETIC "in-house registry" file used by Input 4 of the
# bio-molecular-standardization audit. See README.md in this folder.
# Takes 300 real ChEMBL hERG compounds and re-expresses them the way a
# second registry plausibly would: HCl/Na salt forms, solvates, stereo dropped,
# a deuterium label, and an alternate (non-canonical) tautomer where one exists.
import random
import pandas as pd
from rdkit import Chem, RDLogger
from rdkit.Chem.MolStandardize import rdMolStandardize

RDLogger.DisableLog('rdApp.*')
random.seed(20260916)

SRC = r"F:\OpenScience\audit-envs\cheminformatics-hit-triage-analyst\public-data\chembl_herg_CHEMBL240_ic50.csv"
OUT = r"F:\OpenScience\audits\bio-molecular-standardization\data\inhouse_registry_synthetic.csv"

df = pd.read_csv(SRC).dropna(subset=['canonical_smiles'])
df = df.drop_duplicates('molecule_chembl_id').head(300).reset_index(drop=True)

enum = rdMolStandardize.TautomerEnumerator()
enum.SetMaxTransforms(50)
enum.SetMaxTautomers(20)

rows = []
transforms = []
for i, r in df.iterrows():
    smi = r['canonical_smiles']
    mol = Chem.MolFromSmiles(smi)
    kind = i % 6
    if kind == 0:
        out, tag = smi, 'as_is'
    elif kind == 1:
        out, tag = smi + '.Cl', 'hcl_salt'
    elif kind == 2:
        out, tag = smi + '.O', 'hydrate'
    elif kind == 3:
        m2 = Chem.MolFromSmiles(smi)
        Chem.RemoveStereochemistry(m2)
        out, tag = Chem.MolToSmiles(m2), 'stereo_dropped'
    elif kind == 4:
        m2 = Chem.MolFromSmiles(smi)
        for a in m2.GetAtoms():
            if a.GetAtomicNum() == 6 and a.GetTotalNumHs() == 3:
                a.SetIsotope(13)
                break
        out, tag = Chem.MolToSmiles(m2), 'c13_label'
    else:
        taut = [Chem.MolToSmiles(t) for t in enum.Enumerate(mol)]
        canon = Chem.MolToSmiles(mol)
        alt = next((t for t in taut if t != canon), canon)
        out, tag = alt, 'alt_tautomer' if alt != canon else 'as_is'
    rows.append({'inhouse_id': f'INH{i:04d}', 'smiles': out,
                 'source_chembl_id': r['molecule_chembl_id'], 'perturbation': tag})
    transforms.append(tag)

pd.DataFrame(rows).to_csv(OUT, index=False)
print(pd.Series(transforms).value_counts().to_string())
print(f"wrote {OUT}  rows={len(rows)}")
