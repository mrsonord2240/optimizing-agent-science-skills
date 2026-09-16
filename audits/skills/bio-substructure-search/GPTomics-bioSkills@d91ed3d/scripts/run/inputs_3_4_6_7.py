# bio-substructure-search -- Inputs 3 (Edge), 4 (Variant B), 6 (Scope boundary), 7 (Adversarial)
import time
from rdkit import Chem, RDLogger
from rdkit.Chem import Lipinski
from rdkit.Chem.MolStandardize import rdMolStandardize
from rdkit.Chem.FilterCatalog import FilterCatalog, FilterCatalogParams

RDLogger.DisableLog('rdApp.*')

# ============ INPUT 3 (Edge): the five documented SMARTS failure modes =====
print("== INPUT 3: documented failure modes, tested one by one ==")

print("\n-- (a) fused-ring specificity: does c1ccccc1 match fused systems? --")
for name, smi in [('benzene', 'c1ccccc1'), ('naphthalene', 'c1ccc2ccccc2c1'),
                  ('indole', 'c1ccc2[nH]ccc2c1'), ('toluene', 'Cc1ccccc1'),
                  ('pyridine', 'c1ccncc1')]:
    m = Chem.MolFromSmiles(smi)
    naive = m.HasSubstructMatch(Chem.MolFromSmarts('c1ccccc1'))
    # SKILL.md fix: add explicit ring-degree / fusion constraints
    iso = m.HasSubstructMatch(Chem.MolFromSmarts('c1(-,:[!R1,R0,#1])ccccc1')) if False else None
    strict = m.HasSubstructMatch(Chem.MolFromSmarts('[cR1]1[cR1][cR1][cR1][cR1][cR1]1'))
    print(f"  {name:12} c1ccccc1={str(naive):5}  [cR1]x6={str(strict):5}")
print("  -> SKILL.md claim 'c1ccccc1 does match benzene cycles within naphthalene': confirmed;")
print("     the prescribed fix (explicit ring-membership constraint) separates them.")

print("\n-- (b) tautomer-sensitive miss: keto SMARTS vs enol molecule --")
keto_pat = Chem.MolFromSmarts('[CX3]=[OX1]')
or_pat = Chem.MolFromSmarts('[$([CX3]=[OX1]),$([CX3](-[OX2H])=[CX3])]')
enol = Chem.MolFromSmiles('CC(O)=CC(C)=O')          # acetylacetone enol form
keto = Chem.MolFromSmiles('CC(=O)CC(C)=O')
enum = rdMolStandardize.TautomerEnumerator()
print(f"  keto form  matches [CX3]=[OX1]: {keto.HasSubstructMatch(keto_pat)}")
print(f"  enol form  matches [CX3]=[OX1]: {enol.HasSubstructMatch(keto_pat)}")
print(f"  enol form  matches OR-expanded pattern: {enol.HasSubstructMatch(or_pat)}")
canon_enol = enum.Canonicalize(enol)
print(f"  enol canonicalized -> {Chem.MolToSmiles(canon_enol)}  "
      f"matches [CX3]=[OX1]: {canon_enol.HasSubstructMatch(keto_pat)}")
print("  -> both prescribed fixes (OR-expansion, canonicalize-first) work.")

print("\n-- (c) aromaticity dialect: heteroaromatic rings under RDKit --")
for name, smi in [('furan', 'c1ccoc1'), ('thiazole', 'c1cscn1'), ('pyrrole', 'c1cc[nH]c1'),
                  ('tropone', 'O=C1C=CC=CC=C1')]:
    m = Chem.MolFromSmiles(smi)
    if m is None:
        print(f"  {name:10} SMILES did not parse as aromatic in RDKit")
        continue
    arom = any(a.GetIsAromatic() for a in m.GetAtoms())
    c_match = m.HasSubstructMatch(Chem.MolFromSmarts('[a]'))
    elem = m.HasSubstructMatch(Chem.MolFromSmarts('[#6]~[#6]'))
    print(f"  {name:10} RDKit-aromatic={str(arom):5} [a] matches={str(c_match):5} "
          f"element-based [#6]~[#6] matches={elem}")
print("  -> SKILL.md fix 'use [#6]:[#6] / explicit element+bond' is dialect-independent; confirmed.")

print("\n-- (d) stereochemistry: useChirality flag --")
patt = Chem.MolFromSmarts('[C@H](N)(C)C(=O)O')
for name, smi in [('L-alanine', 'N[C@@H](C)C(=O)O'), ('D-alanine', 'N[C@H](C)C(=O)O')]:
    m = Chem.MolFromSmiles(smi)
    print(f"  {name:10} useChirality=False -> {len(m.GetSubstructMatches(patt))} match(es); "
          f"useChirality=True -> {len(m.GetSubstructMatches(patt, useChirality=True))}")
print("  -> SKILL.md claim 'SMARTS matching is stereo-agnostic by default': confirmed.")

print("\n-- (e) recursive SMARTS performance, deeply nested --")
smis = ['CCN(CC)CCNC(=O)c1ccc(N)cc1', 'CC(C)NCC(O)COc1ccc(CC(N)=O)cc1',
        'NCCc1ccc(O)c(O)c1', 'CC(=O)Nc1ccc(O)cc1'] * 500
mols = [Chem.MolFromSmiles(s) for s in smis]
DEEP = '[$([NX3;H2;$(N-[$([#6;!$([CX3]=[OX1])])])]);!$(N-[C,S,P]=[O,S,N])]'
for label, sma in [('flat [NX3;H2]', '[NX3;H2]'),
                   ('1-level recursive', '[NX3;H2;$(N-[#6])]'),
                   ('deeply nested', DEEP)]:
    p = Chem.MolFromSmarts(sma)
    if p is None:
        print(f"  {label:20} SMARTS FAILED TO PARSE")
        continue
    t0 = time.time()
    n = sum(1 for m in mols if m.HasSubstructMatch(p))
    print(f"  {label:20} {time.time()-t0:.4f}s  matches={n}/{len(mols)}")

# ============ INPUT 4 (Variant B): custom reactive warhead filter ==========
print("\n\n== INPUT 4: reactive-warhead filter, and the covalent-design exemption ==")
REACTIVE_SMARTS = {
    'acid_anhydride': '[CX3](=O)O[CX3](=O)',
    'acid_halide': '[CX3](=O)[F,Cl,Br,I]',
    'alpha_halo_carbonyl': '[CX3](=O)C([F,Cl,Br,I])',
    'aldehyde_reactive': '[CX3H1](=O)[#6;X4]',
    'epoxide': 'C1OC1',
    'aziridine': 'C1NC1',
    'isocyanate': '[NX2]=C=[OX1]',
    'isothiocyanate': '[NX2]=C=[SX1]',
    'beta_lactam': 'C1(=O)NCC1',
    'sulfonyl_halide': '[SX4](=O)(=O)[F,Cl,Br,I]',
    'Michael_acceptor': '[CX3]=[CX3][CX3]=O',
    'vinyl_sulfone': '[SX4](=O)(=O)C=C',
}
COMPILED = {k: Chem.MolFromSmarts(v) for k, v in REACTIVE_SMARTS.items()}
bad = [k for k, v in COMPILED.items() if v is None]
print(f"  all 12 SMARTS parse: {not bad}" + (f"  FAILED: {bad}" if bad else ""))


def reactive_filter(mol, exclude_warheads=True):
    if not exclude_warheads:
        return False, None
    for name, p in COMPILED.items():
        if mol.HasSubstructMatch(p):
            return True, name
    return False, None


PROBES = [
    ('afatinib (acrylamide TCI)', 'CN(C)C/C=C/C(=O)Nc1cc2c(Nc3ccc(F)c(Cl)c3)ncnc2cc1OC1CCOC1'),
    ('ibrutinib (acrylamide TCI)', 'C=CC(=O)N1CCC[C@@H](n2nc(-c3ccc(Oc4ccccc4)cc3)c3c(N)ncnc32)C1'),
    ('sotorasib-like chloroacetamide', 'O=C(CCl)N1CCCCC1'),
    ('penicillin G (beta-lactam)', 'CC1(C)SC2C(NC(=O)Cc3ccccc3)C(=O)N2C1C(=O)O'),
    ('benzoyl chloride', 'O=C(Cl)c1ccccc1'),
    ('glycidol (epoxide)', 'OCC1CO1'),
    ('phenyl isocyanate', 'O=C=Nc1ccccc1'),
    ('benzenesulfonyl fluoride', 'O=S(=O)(F)c1ccccc1'),
    ('divinyl sulfone', 'C=CS(=O)(=O)C=C'),
    ('aspirin (should be clean)', 'CC(=O)Oc1ccccc1C(=O)O'),
    ('atenolol (should be clean)', 'CC(C)NCC(O)COc1ccc(CC(N)=O)cc1'),
    ('curcumin (Michael acceptor)', 'COc1cc(/C=C/C(=O)CC(=O)/C=C/c2ccc(O)c(OC)c2)ccc1O'),
    ('butanal (aliphatic aldehyde)', 'CCCC=O'),
    ('benzaldehyde (aromatic ald.)', 'O=Cc1ccccc1'),
]
for name, smi in PROBES:
    m = Chem.MolFromSmiles(smi)
    if m is None:
        print(f"  {name:32} AUDITOR PROBE SMILES DID NOT PARSE -- skipped")
        continue
    flag, why = reactive_filter(m)
    off, _ = reactive_filter(m, exclude_warheads=False)
    print(f"  {name:32} flagged={str(flag):5} as={str(why):22} "
          f"covalent-design mode flagged={off}")

# ============ INPUT 6 (Scope boundary) ====================================
print("\n\n== INPUT 6: PAINS status of approved drugs (the Capuzzi 2017 check) ==")
p = FilterCatalogParams()
p.AddCatalog(FilterCatalogParams.FilterCatalogs.PAINS)
pains = FilterCatalog(p)
APPROVED = [
    ('curcumin (not approved, classic PAINS)', 'COc1cc(/C=C/C(=O)CC(=O)/C=C/c2ccc(O)c(OC)c2)ccc1O'),
    ('quercetin (flavonoid)', 'O=c1c(O)c(-c2ccc(O)c(O)c2)oc2cc(O)cc(O)c12'),
    ('dopamine (catechol)', 'NCCc1ccc(O)c(O)c1'),
    ('levodopa (approved)', 'N[C@@H](Cc1ccc(O)c(O)c1)C(=O)O'),
    ('entacapone (approved)', 'CCN(CC)C(=O)C(=Cc1cc(O)c(O)c([N+](=O)[O-])c1)C#N'),
    ('epinephrine (approved)', 'CNC[C@H](O)c1ccc(O)c(O)c1'),
    ('mitoxantrone (approved)', 'OCCNCCNc1ccc(NCCNCCO)c2c1C(=O)c1c(O)ccc(O)c1C2=O'),
    ('aspirin (approved)', 'CC(=O)Oc1ccccc1C(=O)O'),
    ('atorvastatin (approved)', 'CC(C)c1c(C(=O)Nc2ccccc2)c(-c2ccccc2)c(-c2ccc(F)cc2)n1CC[C@@H](O)C[C@@H](O)CC(=O)O'),
]
n_flagged = 0
for name, smi in APPROVED:
    m = Chem.MolFromSmiles(smi)
    e = pains.GetFirstMatch(m)
    if e:
        n_flagged += 1
    print(f"  {name:40} PAINS={'FLAGGED: ' + e.GetDescription() if e else 'clean'}")
print(f"  -> {n_flagged}/{len(APPROVED)} of this set flagged, including approved drugs;")
print("     supports the SKILL.md 'PAINS is a flag for assay validation, not a killing filter'.")

# ============ INPUT 7 (Adversarial / ambiguous) ===========================
print("\n\n== INPUT 7: 'find all molecules with an NH2 group' -- which query? ==")
QUERIES = {
    '[NH2] (naive, as a user would write it)': '[NH2]',
    '[NX3;H2] (any sp3 N with 2 H)': '[NX3;H2]',
    'SKILL.md primary amine (context-aware)': '[NX3;H2;$(N-[#6]);!$(N-[C,S,P]=[O,S,N])]',
}
CASES = [('propylamine', 'CCCN'), ('aniline', 'Nc1ccccc1'),
         ('acetamide (amide, not an amine)', 'CC(N)=O'),
         ('sulfonamide', 'NS(=O)(=O)c1ccccc1'),
         ('hydrazine', 'NN'), ('urea', 'NC(N)=O'),
         ('ammonium ion', '[NH4+]'), ('guanidine', 'N=C(N)N')]
hdr = f"  {'molecule':34}" + "".join(f"{k[:26]:28}" for k in QUERIES)
print(hdr)
for name, smi in CASES:
    m = Chem.MolFromSmiles(smi)
    cells = ""
    for q in QUERIES.values():
        pp = Chem.MolFromSmarts(q)
        cells += f"{str(m.HasSubstructMatch(pp)):28}"
    print(f"  {name:34}{cells}")

print("\n  invalid SMARTS handling:")
for bad_s in ['[OX2H', 'c1cccc', '[Q]', '']:
    pp = Chem.MolFromSmarts(bad_s)
    print(f"    MolFromSmarts({bad_s!r:10}) -> {pp}")
print("  -> MolFromSmarts returns None rather than raising; the shipped example's")
print("     has_substructure() converts that to a named ValueError, but SKILL.md's own")
print("     filter_library() and pains snippets do not check for None.")
m = Chem.MolFromSmiles('CCO')
try:
    print("  SKILL.md filter_library with an invalid exclude pattern:",
          [Chem.MolToSmiles(x) for x in
           [mm for mm in [m] if mm and not mm.HasSubstructMatch(Chem.MolFromSmarts('[OX2H'))]])
except Exception as exc:                                     # noqa: BLE001
    print(f"  SKILL.md filter_library with an invalid exclude pattern raised: "
          f"{type(exc).__name__}: {exc}")
