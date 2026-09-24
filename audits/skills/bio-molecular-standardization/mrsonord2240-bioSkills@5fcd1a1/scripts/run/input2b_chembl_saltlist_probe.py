# Input 2 follow-up probe: characterise WHY ChEMBL get_parent_mol keeps sodium acetate,
# and whether the SKILL.md documented mitigation ("pre-filter to >=1 carbon atom") covers it.
from rdkit import Chem, RDLogger
from chembl_structure_pipeline import standardize_mol, get_parent_mol

RDLogger.DisableLog('rdApp.*')

PROBES = [
    ('sodium acetate',        '[Na+].CC(=O)[O-]'),
    ('sodium aspirinate',     '[Na+].CC(=O)Oc1ccccc1C(=O)[O-]'),
    ('sodium benzoate',       '[Na+].O=C([O-])c1ccccc1'),
    ('sodium formate',        '[Na+].[O-]C=O'),
    ('sodium citrate (1:1)',  '[Na+].OC(=O)CC(O)(CC(=O)O)C(=O)[O-]'),
    ('choline chloride',      'OCC[N+](C)(C)C.[Cl-]'),
    ('potassium acetate',     '[K+].CC(=O)[O-]'),
]
for label, smi in PROBES:
    m = Chem.MolFromSmiles(smi)
    p, excl = get_parent_mol(standardize_mol(m))
    out = Chem.MolToSmiles(p)
    nfrag = len(Chem.GetMolFrags(p))
    ncarbon = sum(1 for a in p.GetAtoms() if a.GetAtomicNum() == 6)
    caught = 'NO  <- passes the >=1-carbon filter with the counter-ion still attached' \
        if (nfrag > 1 and ncarbon > 0) else ('yes' if nfrag > 1 else '-')
    print(f"{label:22} -> {out:55} frags={nfrag} C={ncarbon} exclude={excl}  "
          f"caught by SKILL.md mitigation? {caught}")
