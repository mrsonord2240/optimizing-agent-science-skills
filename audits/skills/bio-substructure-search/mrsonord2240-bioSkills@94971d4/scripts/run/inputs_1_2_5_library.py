# bio-substructure-search -- Inputs 1 (Canonical), 2 (Variant A), 5 (Stress)
# Code follows SKILL.md "PAINS Filter", "When to Apply Each Filter" and
# "Recursive SMARTS performance". Real data: ChEMBL hERG CHEMBL240 export.
import time
from collections import Counter
import pandas as pd
from rdkit import Chem, RDLogger
from rdkit.Chem.FilterCatalog import FilterCatalog, FilterCatalogParams

RDLogger.DisableLog('rdApp.*')
SRC = r"F:\OpenScience\audit-envs\cheminformatics-hit-triage-analyst\public-data\chembl_herg_CHEMBL240_ic50.csv"

df = pd.read_csv(SRC).dropna(subset=['canonical_smiles']).drop_duplicates('molecule_chembl_id')
all_mols = [(cid, Chem.MolFromSmiles(s)) for cid, s in
            zip(df.molecule_chembl_id, df.canonical_smiles)]
all_mols = [(c, m) for c, m in all_mols if m is not None]
print(f"[load] {len(all_mols)} distinct ChEMBL hERG compounds parsed")
hits = all_mols[:800]


def build(catalogs):
    p = FilterCatalogParams()
    for c in catalogs:
        p.AddCatalog(getattr(FilterCatalogParams.FilterCatalogs, c))
    return FilterCatalog(p)


# ---- verify the catalog sizes the SKILL.md table claims --------------------
print("\n== catalog entry counts vs the SKILL.md table ==")
CLAIMED = {'PAINS_A': 16, 'PAINS_B': 55, 'PAINS_C': 409, 'BRENK': 105,
           'NIH': 180, 'ZINC': 50, 'PAINS': 480}
for name, claim in CLAIMED.items():
    n = build([name]).GetNumEntries()
    mark = 'OK' if n == claim else f'MISMATCH (SKILL.md says {claim})'
    print(f"  {name:8} installed={n:4}  {mark}")

# ---- INPUT 1: PAINS_A flag-not-delete on 800 screening hits ---------------
print("\n== INPUT 1: PAINS_A triage of 800 hits (flag, do not delete) ==")
cat_a = build(['PAINS_A'])
flagged, clean, patterns = [], [], Counter()
for cid, m in hits:
    e = cat_a.GetFirstMatch(m)
    if e is None:
        clean.append(cid)
    else:
        flagged.append((cid, e.GetDescription()))
        patterns[e.GetDescription()] += 1
print(f"  PAINS_A flagged {len(flagged)}/800 ({100*len(flagged)/800:.1f}%), clean {len(clean)}")
print("  patterns that fired:")
for pat, n in patterns.most_common():
    print(f"    {pat:24} {n}")
print(f"  distinct PAINS_A patterns firing: {len(patterns)}/16")
print("  retained in output? flagged compounds kept with a reason string:",
      all(isinstance(d, str) and d for _, d in flagged))

# ---- INPUT 2: HTS library prep, PAINS_A + BRENK + ZINC --------------------
print("\n== INPUT 2: library prep, PAINS_A + BRENK + ZINC ==")
cats = {}
for name in ['PAINS_A', 'BRENK', 'ZINC']:
    c = build([name])
    s = {cid for cid, m in hits if c.HasMatch(m)}
    cats[name] = s
    print(f"  {name:8} flags {len(s):4}/800 ({100*len(s)/800:.1f}%)")
union = set().union(*cats.values())
print(f"  union flagged = {len(union)}/800 ({100*len(union)/800:.1f}%) -> "
      f"{800-len(union)} compounds survive the combined filter")
print("  pairwise overlap:")
names = list(cats)
for i in range(len(names)):
    for j in range(i + 1, len(names)):
        a, b = names[i], names[j]
        print(f"    {a} & {b}: {len(cats[a] & cats[b])}")
print(f"  flagged by all three: {len(cats['PAINS_A'] & cats['BRENK'] & cats['ZINC'])}")
print("  -> ZINC and BRENK do most of the attrition; PAINS_A alone would keep "
      f"{800 - len(cats['PAINS_A'])} compounds")

# ---- INPUT 5: full library, all catalogs, and recursive SMARTS cost -------
print("\n== INPUT 5: full library throughput and recursive-SMARTS cost ==")
cat_all = build(['ALL'])
t0 = time.time()
n_flag = sum(1 for _, m in all_mols if cat_all.HasMatch(m))
t_all = time.time() - t0
print(f"  catalog ALL ({cat_all.GetNumEntries()} entries) over {len(all_mols)} mols: "
      f"{t_all:.1f}s ({len(all_mols)/t_all:.0f} mol/s), flagged {n_flag} "
      f"({100*n_flag/len(all_mols):.1f}%)")

# rebuild cost per call vs once (SKILL.md Common Errors: "Build catalog once")
t0 = time.time()
for _, m in all_mols[:200]:
    build(['PAINS_A']).HasMatch(m)
t_rebuild = time.time() - t0
c1 = build(['PAINS_A'])
t0 = time.time()
for _, m in all_mols[:200]:
    c1.HasMatch(m)
t_reuse = time.time() - t0
print(f"  catalog rebuilt per molecule: {t_rebuild:.2f}s vs reused: {t_reuse:.3f}s "
      f"-> {t_rebuild/max(t_reuse,1e-9):.0f}x penalty (SKILL.md 'build catalog once')")

FLAT = '[NX3;H2]'
REC = '[NX3;H2;$(N-[#6]);!$(N-[C,S,P]=[O,S,N])]'
for label, sma in [('flat [NX3;H2]', FLAT), ('recursive primary amine', REC)]:
    p = Chem.MolFromSmarts(sma)
    t0 = time.time()
    n = sum(1 for _, m in all_mols if m.HasSubstructMatch(p))
    dt = time.time() - t0
    print(f"  {label:26} {dt:.3f}s  matches={n}")
p_f, p_r = Chem.MolFromSmarts(FLAT), Chem.MolFromSmarts(REC)
t0 = time.time()
pre = [m for _, m in all_mols if m.HasSubstructMatch(p_f)]
n2 = sum(1 for m in pre if m.HasSubstructMatch(p_r))
dt = time.time() - t0
print(f"  pre-filter then re-test (SKILL.md fix): {dt:.3f}s  matches={n2}  "
      f"(prefilter pool {len(pre)})")
