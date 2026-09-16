# bio-admet-prediction -- build the input CSVs for the ADMET-AI runs.
import pandas as pd
from rdkit import Chem, RDLogger
RDLogger.DisableLog('rdApp.*')
D = r"F:\OpenScience\audits\bio-admet-prediction\run"
SRC = r"F:\OpenScience\audit-envs\cheminformatics-hit-triage-analyst\public-data\chembl_herg_CHEMBL240_ic50.csv"

df = pd.read_csv(SRC).dropna(subset=['canonical_smiles', 'pchembl_value'])
df = df.groupby('canonical_smiles', as_index=False).pchembl_value.mean()
# 300 compounds spanning the measured hERG potency range, stratified
df['bin'] = pd.cut(df.pchembl_value, bins=[0, 5, 6, 7, 8, 12], labels=False)
samp = df.groupby('bin', group_keys=False).apply(
    lambda g: g.sample(min(len(g), 60), random_state=42), include_groups=False)
samp = samp.reset_index(drop=True)
samp.rename(columns={'canonical_smiles': 'smiles'})[['smiles']].to_csv(
    D + r"\herg_300.csv", index=False)
samp.to_csv(D + r"\herg_300_truth.csv", index=False)
print(f"herg_300.csv: {len(samp)} compounds, measured pChEMBL "
      f"{samp.pchembl_value.min():.2f}-{samp.pchembl_value.max():.2f}")
print(samp.pchembl_value.describe().round(2).to_string())

# Out-of-distribution probes, drawn from the chemistry the Skill's OOD failure
# mode names: PROTACs, macrocycles, peptides, metal complexes.
OOD = [
    ('drug control: atenolol', 'CC(C)NCC(O)COc1ccc(CC(N)=O)cc1'),
    ('drug control: astemizole (known hERG blocker)',
     'COc1ccc(CCN2CCC(Nc3nc4ccccc4n3Cc3ccc(F)cc3)CC2)cc1'),
    ('macrocycle: erythromycin-like lactone',
     'CC1CC(C)C(=O)C(C)C(O)C(C)CC(C)C(=O)OC(CC)C1O'),
    ('macrocycle: cyclic hexapeptide',
     'O=C1NCC(=O)NCC(=O)NCC(=O)NCC(=O)NCC(=O)NC1'),
    ('peptide: linear tetrapeptide',
     'NC(=O)CNC(=O)[C@H](Cc1ccccc1)NC(=O)[C@@H](N)CC(C)C'),
    ('PROTAC-like: VHL ligand + linker + warhead',
     'CC(C)(C)[C@H](NC(=O)CNC(=O)CCCCCOc1ccc(-c2ccccc2)cc1)C(=O)N1C[C@H](O)C[C@H]1C(=O)NCc1ccc(-c2scnc2C)cc1'),
    ('metal complex: cisplatin', 'N.N.Cl[Pt]Cl'),
    ('inorganic: sodium chloride', '[Na+].[Cl-]'),
    ('very large: paclitaxel',
     'CC(=O)O[C@@H]1C(=O)[C@]2(C)[C@@H](O)C[C@H]3OC[C@]3(OC(C)=O)[C@H]2[C@H](OC(=O)c2ccccc2)[C@]2(O)C[C@H](OC(=O)[C@H](O)[C@@H](NC(=O)c3ccccc3)c3ccccc3)C(C)=C1C2(C)C'),
]
rows = []
for label, smi in OOD:
    m = Chem.MolFromSmiles(smi)
    print(f"  {label:48} parses={m is not None}")
    if m is not None:
        rows.append({'smiles': Chem.MolToSmiles(m), 'label': label})
pd.DataFrame(rows).to_csv(D + r"\ood_probes_truth.csv", index=False)
pd.DataFrame(rows)[['smiles']].to_csv(D + r"\ood_probes.csv", index=False)
print(f"ood_probes.csv: {len(rows)} compounds")
