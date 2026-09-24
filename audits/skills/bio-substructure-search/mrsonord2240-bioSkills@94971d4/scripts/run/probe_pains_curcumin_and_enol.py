# Follow-up probes for bio-substructure-search, after inputs 3 and 6.
from rdkit import Chem, RDLogger
from rdkit.Chem.FilterCatalog import FilterCatalog, FilterCatalogParams

RDLogger.DisableLog('rdApp.*')

# ---- (1) Does the RDKit PAINS catalog contain a curcumin pattern at all? ---
p = FilterCatalogParams()
p.AddCatalog(FilterCatalogParams.FilterCatalogs.PAINS)
cat = FilterCatalog(p)
descs = [cat.GetEntry(i).GetDescription() for i in range(cat.GetNumEntries())]
print(f"PAINS catalog entries: {len(descs)}")
for kw in ['cur', 'ene_one', 'rhod', 'catech', 'quinone', 'mannich', 'anil']:
    hit = sorted({d for d in descs if kw in d.lower()})
    print(f"  descriptions containing {kw!r:10}: {len(hit)}  {hit[:6]}")

CURC = 'COc1cc(/C=C/C(=O)CC(=O)/C=C/c2ccc(O)c(OC)c2)ccc1O'
m = Chem.MolFromSmiles(CURC)
print(f"\ncurcumin parsed: {m is not None}; heavy atoms={m.GetNumHeavyAtoms()}")
for name in ['PAINS_A', 'PAINS_B', 'PAINS_C', 'PAINS', 'BRENK', 'NIH', 'ZINC', 'ALL']:
    pp = FilterCatalogParams()
    pp.AddCatalog(getattr(FilterCatalogParams.FilterCatalogs, name))
    c = FilterCatalog(pp)
    e = c.GetFirstMatch(m)
    print(f"  curcumin vs {name:8}: {'FLAGGED ' + e.GetDescription() if e else 'clean'}")

# second, independent method: match the two literature curcumin/ene_one SMARTS by hand
print("\n  hand-written ene_one / 1,3-diketone SMARTS against curcumin:")
for lbl, sma in [('enone C=C-C=O', '[CX3]=[CX3][CX3]=[OX1]'),
                 ('1,3-diketone', '[CX3](=[OX1])[CX4H2][CX3](=[OX1])')]:
    print(f"    {lbl:16} -> {m.HasSubstructMatch(Chem.MolFromSmarts(sma))}")

# ---- (2) clean tautomer-miss test (the first attempt did not isolate it) ---
print("\n== clean tautomer-sensitive-miss test ==")
keto_pat = Chem.MolFromSmarts('[CX3]=[OX1]')
or_pat = Chem.MolFromSmarts('[$([CX3]=[OX1]),$([CX3](-[OX2H])=[CX3])]')
for lbl, smi in [('acetone (keto)', 'CC(C)=O'), ('prop-1-en-2-ol (pure enol)', 'CC(O)=C')]:
    mm = Chem.MolFromSmiles(smi)
    print(f"  {lbl:28} [CX3]=[OX1] -> {mm.HasSubstructMatch(keto_pat):<5} "
          f"OR-expanded -> {mm.HasSubstructMatch(or_pat)}")
from rdkit.Chem.MolStandardize import rdMolStandardize
enol = Chem.MolFromSmiles('CC(O)=C')
canon = rdMolStandardize.TautomerEnumerator().Canonicalize(enol)
print(f"  canonicalize-first fix: CC(O)=C -> {Chem.MolToSmiles(canon)}  "
      f"[CX3]=[OX1] -> {canon.HasSubstructMatch(keto_pat)}")

# ---- (3) empty SMARTS is a match-all query, not an error ------------------
print("\n== empty SMARTS ==")
empty = Chem.MolFromSmarts('')
print(f"  MolFromSmarts('') -> {empty}  numAtoms={empty.GetNumAtoms()}")
for smi in ['CCO', 'c1ccccc1', '[Na+]']:
    print(f"    {smi:10} HasSubstructMatch(empty) = "
          f"{Chem.MolFromSmiles(smi).HasSubstructMatch(empty)}")
