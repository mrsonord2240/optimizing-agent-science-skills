# Input 2 (Variant A) -- bio-molecular-standardization
# Registry salt/solvate/co-crystal forms: ChEMBL get_parent_mol vs
# rdMolStandardize LargestFragmentChooser(preferOrganic=True), with the
# quaternary-ammonium charge-preservation requirement checked explicitly.
# Every row of the SKILL.md "Salt Stripping Edge Cases" table is included verbatim.
from rdkit import Chem, RDLogger
from rdkit.Chem.MolStandardize import rdMolStandardize
from chembl_structure_pipeline import standardize_mol, get_parent_mol
from rdkit.Chem import rdMolDescriptors

RDLogger.DisableLog('rdApp.*')

CASES = [
    # (label, input SMILES, SKILL.md claimed result or None)
    ('mono-salt (SKILL.md table)',      '[Na+].CC(=O)[O-]',                        'CC(=O)O'),
    ('di-salt (SKILL.md table)',        '[Na+].[Na+].CC(=O)[O-].CC(=O)[O-]',       'CC(=O)O'),
    ('mixed salt (SKILL.md table)',     'CCO.CC(=O)O',                             'CCO'),
    ('co-crystal (SKILL.md table)',     'CC(=O)O.CCOC(C)=O',                       'largest'),
    ('hydrate (SKILL.md table)',        'CC(=O)O.O',                               'CC(=O)O'),
    ('solvate (SKILL.md table)',        'CC(=O)O.CO',                              'CC(=O)O'),
    ('quaternary N (SKILL.md table)',   'C[N+](C)(C)C',                            'keep +1'),
    # real registry forms
    ('amlodipine besylate',             'CCOC(=O)C1=C(COCCN)NC(C)=C(C(=O)OC)C1c1ccccc1Cl.O=S(=O)(O)c1ccccc1', None),
    ('atenolol HCl',                    'CC(C)NCC(O)COc1ccc(CC(N)=O)cc1.Cl',       None),
    ('bethanechol chloride (quat)',     'C[N+](C)(C)C(C)COC(N)=O.[Cl-]',           None),
    ('verapamil HCl (real hERG cmpd)',  'COc1ccc(CCN(C)CCCC(C#N)(c2ccc(OC)c(OC)c2)C(C)C)cc1OC.Cl', None),
    ('sodium chloride (inorganic)',     '[Na+].[Cl-]',                             None),
]


def chembl_parent(smi):
    mol = Chem.MolFromSmiles(smi)
    if mol is None:
        return 'PARSE_FAIL', None
    std = standardize_mol(mol)
    parent, exclude = get_parent_mol(std)
    return Chem.MolToSmiles(parent), exclude


def rdkit_parent(smi, force=False):
    mol = Chem.MolFromSmiles(smi)
    if mol is None:
        return 'PARSE_FAIL'
    Chem.SanitizeMol(mol)
    mol = rdMolStandardize.LargestFragmentChooser(preferOrganic=True).choose(mol)
    mol = rdMolStandardize.Normalizer().normalize(mol)
    mol = rdMolStandardize.Uncharger(canonicalOrder=True).uncharge(mol)
    return Chem.MolToSmiles(mol)


def netcharge(smi):
    m = Chem.MolFromSmiles(smi)
    return None if m is None else Chem.GetFormalCharge(m)


print(f"{'case':34} {'ChEMBL get_parent_mol':52} {'excl':5} {'rdMolStandardize':40} {'q(C)':5} {'q(R)':5}")
print('-' * 150)
disagree = []
for label, smi, claim in CASES:
    c, excl = chembl_parent(smi)
    r = rdkit_parent(smi)
    print(f"{label:34} {c:52} {str(excl):5} {r:40} {str(netcharge(c)):5} {str(netcharge(r)):5}")
    if c != r:
        disagree.append((label, smi, c, r, claim))

print()
print("DISAGREEMENTS between ChEMBL parent and RDKit LargestFragmentChooser:")
for label, smi, c, r, claim in disagree:
    print(f"  {label}: in={smi}\n      ChEMBL -> {c}\n      RDKit  -> {r}\n      SKILL.md table claims -> {claim}")

print()
print("Quaternary-ammonium charge preservation check:")
for label, smi in [('quat, no counter-ion', 'C[N+](C)(C)C'),
                   ('bethanechol chloride', 'C[N+](C)(C)C(C)COC(N)=O.[Cl-]')]:
    c, _ = chembl_parent(smi)
    r_f = rdkit_parent(smi)
    m = Chem.MolFromSmiles(smi)
    Chem.SanitizeMol(m)
    m = rdMolStandardize.LargestFragmentChooser(preferOrganic=True).choose(m)
    m = rdMolStandardize.Uncharger(canonicalOrder=True, force=True).uncharge(m)
    print(f"  {label}: ChEMBL q={netcharge(c)} ({c}) | Uncharger force=False q={netcharge(r_f)} ({r_f}) "
          f"| force=True q={Chem.GetFormalCharge(m)} ({Chem.MolToSmiles(m)})")
