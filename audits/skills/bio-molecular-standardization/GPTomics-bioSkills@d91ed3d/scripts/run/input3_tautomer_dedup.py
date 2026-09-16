# Input 3 (Edge) -- bio-molecular-standardization
# Do the SKILL.md "Tautomer Canonicalization (debated)" pairs collapse to one
# representation, and does plain InChIKey already collapse them without a tautomer step?
from rdkit import Chem, RDLogger
from rdkit.Chem.MolStandardize import rdMolStandardize
from chembl_structure_pipeline import standardize_mol, get_parent_mol

RDLogger.DisableLog('rdApp.*')
enum = rdMolStandardize.TautomerEnumerator()

PAIRS = [
    ('keto / enol (acetone)',            'CC(C)=O',                'CC(O)=C'),
    ('keto / enol (acetylacetone)',      'CC(=O)CC(C)=O',          'CC(O)=CC(C)=O'),
    ('lactam / lactim (2-pyridone)',     'O=c1cccc[nH]1',          'Oc1ccccn1'),
    ('amidine / iminol (acetamide)',     'CC(N)=O',                'CC(=N)O'),
    ('phenol / keto (2-naphthol)',       'Oc1ccc2ccccc2c1',        'O=C1C=Cc2ccccc2C1'),
    ('1H / 2H-pyrazole (3-Me)',          'Cc1cc[nH]n1',            'Cc1n[nH]cc1'),
    ('guanine N7H / N9H',                'Nc1nc2[nH]cnc2c(=O)[nH]1', 'Nc1nc2nc[nH]c2c(=O)[nH]1'),
    ('nitro / aci-nitro',                'CC[N+](=O)[O-]',         'CC=[N+]([O-])O'),
]


def chembl_only(smi):
    m = Chem.MolFromSmiles(smi)
    if m is None:
        return None
    p, _ = get_parent_mol(standardize_mol(m))
    return p


print(f"{'pair':34} {'ChEMBL same?':13} {'ChEMBL InChIKey same?':22} {'+tautomer canon same?':22}")
print('-' * 95)
rows = []
for label, a, b in PAIRS:
    pa, pb = chembl_only(a), chembl_only(b)
    if pa is None or pb is None:
        print(f"{label:34} PARSE_FAIL")
        continue
    smi_same = Chem.MolToSmiles(pa) == Chem.MolToSmiles(pb)
    ik_same = Chem.MolToInchiKey(pa) == Chem.MolToInchiKey(pb)
    ta = Chem.MolToSmiles(enum.Canonicalize(pa))
    tb = Chem.MolToSmiles(enum.Canonicalize(pb))
    t_same = ta == tb
    rows.append((label, smi_same, ik_same, t_same, ta, tb,
                 Chem.MolToInchiKey(pa)[:14], Chem.MolToInchiKey(pb)[:14]))
    print(f"{label:34} {str(smi_same):13} {str(ik_same):22} {str(t_same):22}")

print()
print("Cases where the ChEMBL-only route would register the same compound twice:")
for label, smi_same, ik_same, t_same, ta, tb, ska, skb in rows:
    if not ik_same:
        fix = 'FIXED by TautomerEnumerator.Canonicalize' if t_same else 'STILL SPLIT after tautomer canonicalization'
        print(f"  {label}: InChIKey skeletons {ska} vs {skb} -> {fix}")
        if not t_same:
            print(f"      canonical tautomers: {ta}  |  {tb}")

print()
print("InChIKey first-block (skeleton) agreement -- tests the SKILL.md claim that standard")
print("InChIKey 'may collapse some mobile-hydrogen tautomer representations':")
for label, smi_same, ik_same, t_same, ta, tb, ska, skb in rows:
    print(f"  {label:34} skeleton_same={ska == skb}  full_key_same={ik_same}")
