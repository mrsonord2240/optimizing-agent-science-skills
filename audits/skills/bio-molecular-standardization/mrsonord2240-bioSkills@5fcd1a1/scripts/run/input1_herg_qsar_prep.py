# Input 1 (Canonical) -- bio-molecular-standardization
# Code written by following SKILL.md "Standardization for ML Training (avoiding data leakage)"
# and examples/standardize_library.py prepare_qsar_data().
# Real data: ChEMBL hERG (CHEMBL240) IC50 export, 3,966 rows.
import sys
import numpy as np
import pandas as pd
from rdkit import Chem, RDLogger
from chembl_structure_pipeline import standardize_mol, get_parent_mol

RDLogger.DisableLog('rdApp.*')

SRC = r"F:\OpenScience\audit-envs\cheminformatics-hit-triage-analyst\public-data\chembl_herg_CHEMBL240_ic50.csv"
OUT = r"F:\OpenScience\audits\bio-molecular-standardization\run\herg_qsar_train.csv"

df = pd.read_csv(SRC)
print(f"[load] rows={len(df)}  unique molecule_chembl_id={df.molecule_chembl_id.nunique()}")
df = df.dropna(subset=['canonical_smiles', 'pchembl_value'])
print(f"[filter] rows with SMILES and pchembl_value = {len(df)}")

counts = {'parse_failure': 0, 'excluded_by_chembl': 0, 'standardize_error': 0,
          'inorganic_no_carbon': 0, 'ok': 0}
rows = []
for _, r in df.iterrows():
    smi = r['canonical_smiles']
    mol = Chem.MolFromSmiles(smi)
    if mol is None:
        counts['parse_failure'] += 1
        continue
    try:
        std = standardize_mol(mol)
        parent, exclude = get_parent_mol(std)
    except Exception as e:                      # noqa: BLE001
        counts['standardize_error'] += 1
        continue
    if exclude:
        counts['excluded_by_chembl'] += 1
        continue
    # SKILL.md "Per-Tool Failure Modes -> ChEMBL pipeline -- inorganic salt fails":
    # pre-filter to compounds with >=1 carbon.
    if sum(1 for a in parent.GetAtoms() if a.GetAtomicNum() == 6) == 0:
        counts['inorganic_no_carbon'] += 1
        continue
    counts['ok'] += 1
    rows.append({
        'smiles': Chem.MolToSmiles(parent),
        'inchikey': Chem.MolToInchiKey(parent),
        'activity': float(r['pchembl_value']),
        'orig_smiles': smi,
        'chembl_id': r['molecule_chembl_id'],
    })

print("[standardize] " + "  ".join(f"{k}={v}" for k, v in counts.items()))
std = pd.DataFrame(rows)

# how many structures actually changed
changed = (std.smiles != std.orig_smiles.map(
    lambda s: Chem.MolToSmiles(Chem.MolFromSmiles(s)))).sum()
print(f"[standardize] canonical SMILES changed by the pipeline: {changed}/{len(std)}")

dedup = std.groupby('inchikey').agg(
    smiles=('smiles', 'first'),
    activity=('activity', 'mean'),
    activity_std=('activity', 'std'),
    activity_range=('activity', lambda x: float(x.max() - x.min())),
    n_replicates=('activity', 'count'),
    n_chembl_ids=('chembl_id', lambda x: x.nunique()),
).reset_index()
print(f"[dedup] unique InChIKeys = {len(dedup)}  (collapsed {len(std) - len(dedup)} records)")

# did standardization merge records that raw SMILES kept apart?
raw_unique = std.orig_smiles.map(
    lambda s: Chem.MolToSmiles(Chem.MolFromSmiles(s))).nunique()
print(f"[dedup] unique canonical SMILES BEFORE standardization = {raw_unique}")
merged_extra = raw_unique - len(dedup)
print(f"[dedup] records merged only because of standardization = {merged_extra}")

multi = dedup[dedup.n_replicates > 1]
disagree = multi[multi.activity_range > 1.0]
print(f"[replicates] compounds with >1 measurement = {len(multi)}")
print(f"[replicates] of those, pChEMBL range > 1 log unit = {len(disagree)} "
      f"({100 * len(disagree) / max(len(multi), 1):.1f}%)")
print(f"[replicates] max range seen = {dedup.activity_range.max():.2f} log units")
print("[replicates] worst 5 disagreements:")
print(disagree.nlargest(5, 'activity_range')[
    ['inchikey', 'n_replicates', 'activity', 'activity_range']].to_string(index=False))

# cross-compound-id check: same structure registered under >1 ChEMBL ID
dupe_ids = dedup[dedup.n_chembl_ids > 1]
print(f"[identity] distinct structures registered under >1 ChEMBL ID = {len(dupe_ids)}")

dedup[['inchikey', 'smiles', 'activity', 'activity_std', 'n_replicates']].to_csv(OUT, index=False)
print(f"[write] {OUT}  rows={len(dedup)}")
