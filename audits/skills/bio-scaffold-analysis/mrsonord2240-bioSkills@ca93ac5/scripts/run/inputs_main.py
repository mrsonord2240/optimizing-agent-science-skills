# bio-scaffold-analysis -- Inputs 1,2,3,4,6,7 (input 5 = mmpdb, separate script).
# Every function below is copied verbatim from SKILL.md.
import random
from collections import defaultdict
import numpy as np
import pandas as pd
from rdkit import Chem, RDLogger
from rdkit.Chem.Scaffolds import MurckoScaffold
from rdkit.Chem import rdRGroupDecomposition as rgd
from rdkit.Chem.MolStandardize import rdMolStandardize

RDLogger.DisableLog('rdApp.*')
SRC = r"F:\OpenScience\audit-envs\cheminformatics-hit-triage-analyst\public-data\chembl_herg_CHEMBL240_ic50.csv"
df = pd.read_csv(SRC).dropna(subset=['canonical_smiles', 'pchembl_value'])
df = df.groupby('canonical_smiles', as_index=False).pchembl_value.mean()
df = df[df.canonical_smiles.map(lambda s: Chem.MolFromSmiles(s) is not None)].reset_index(drop=True)
print(f"[data] {len(df)} unique hERG compounds")


def scaffold_clusters(smiles_list):                    # SKILL.md verbatim
    clusters = defaultdict(list)
    for smi in smiles_list:
        mol = Chem.MolFromSmiles(smi)
        if mol is None:
            continue
        scaffold = MurckoScaffold.GetScaffoldForMol(mol)
        clusters[Chem.MolToSmiles(scaffold)].append(smi)
    return clusters


def scaffold_split(df, smiles_col='smiles', train_frac=0.8, seed=42):   # SKILL.md verbatim
    rng = random.Random(seed)
    scaffolds = defaultdict(list)
    invalid_positions = []
    for pos, smi in enumerate(df[smiles_col].tolist()):
        mol = Chem.MolFromSmiles(smi)
        if mol is None:
            invalid_positions.append(pos)
            continue
        scaff = Chem.MolToSmiles(MurckoScaffold.GetScaffoldForMol(mol))
        scaffolds[scaff].append(pos)
    if invalid_positions:
        raise ValueError(f'Invalid SMILES at row positions: {invalid_positions}')
    scaffold_sets = list(scaffolds.values())
    rng.shuffle(scaffold_sets)
    scaffold_sets.sort(key=lambda x: len(x), reverse=True)
    n_total = sum(len(s) for s in scaffold_sets)
    n_train = int(n_total * train_frac)
    if len(scaffold_sets) < 2:
        raise ValueError('A scaffold split requires at least two scaffolds')
    train_idx = list(scaffold_sets[0])
    test_idx = []
    for i, scaff_set in enumerate(scaffold_sets[1:], start=1):
        if not test_idx and i == len(scaffold_sets) - 1:
            test_idx.extend(scaff_set)
        elif abs(len(train_idx) + len(scaff_set) - n_train) < abs(len(train_idx) - n_train):
            train_idx.extend(scaff_set)
        else:
            test_idx.extend(scaff_set)
    return df.iloc[train_idx], df.iloc[test_idx]


# ===== INPUT 1 (Canonical): chemotype clustering ===========================
print("\n===== INPUT 1: Bemis-Murcko chemotype clusters over the whole library =====")
cl = scaffold_clusters(list(df.canonical_smiles))
sizes = sorted((len(v) for v in cl.values()), reverse=True)
print(f"  distinct Bemis-Murcko scaffolds: {len(cl)}  for {len(df)} compounds "
      f"({len(df)/len(cl):.2f} compounds per scaffold)")
print(f"  singletons: {sum(1 for s in sizes if s == 1)} "
      f"({100*sum(1 for s in sizes if s==1)/len(cl):.1f}% of scaffolds, "
      f"{100*sum(1 for s in sizes if s==1)/len(df):.1f}% of compounds)")
print(f"  largest clusters: {sizes[:10]}")
print(f"  empty-scaffold ('' = no rings) compounds: {len(cl.get('', []))}")
series = {s: c for s, c in cl.items() if len(c) >= 3}
print(f"  series with >=3 members (detect_series, min_size=3): {len(series)} "
      f"covering {sum(len(c) for c in series.values())} compounds")
print("  top 5 scaffolds:")
for s, c in sorted(cl.items(), key=lambda kv: -len(kv[1]))[:5]:
    print(f"    n={len(c):4}  {s[:76] if s else '<empty: acyclic>'}")

# ===== INPUT 2 (Variant A): the shipped scaffold_split =====================
print("\n===== INPUT 2: the SKILL.md scaffold_split, run verbatim =====")
d = df.rename(columns={'canonical_smiles': 'smiles'})
for frac in [0.8, 0.7, 0.9]:
    tr, te = scaffold_split(d, 'smiles', train_frac=frac, seed=42)
    achieved = len(tr) / (len(tr) + len(te))
    s_tr = {Chem.MolToSmiles(MurckoScaffold.GetScaffoldForMol(Chem.MolFromSmiles(s)))
            for s in tr.smiles}
    s_te = {Chem.MolToSmiles(MurckoScaffold.GetScaffoldForMol(Chem.MolFromSmiles(s)))
            for s in te.smiles}
    print(f"  train_frac requested={frac}  achieved={achieved:.3f}  "
          f"train={len(tr)} test={len(te)}  scaffold overlap={len(s_tr & s_te)}  "
          f"train scaffolds={len(s_tr)} test scaffolds={len(s_te)}")
tr, te = scaffold_split(d, 'smiles', train_frac=0.8, seed=42)
te_sizes = [len(cl[Chem.MolToSmiles(MurckoScaffold.GetScaffoldForMol(Chem.MolFromSmiles(s)))])
            for s in te.smiles]
tr_sizes = [len(cl[Chem.MolToSmiles(MurckoScaffold.GetScaffoldForMol(Chem.MolFromSmiles(s)))])
            for s in tr.smiles]
print(f"  SKILL.md failure mode 'Test set is mostly singleton scaffolds':")
print(f"    test compounds whose scaffold is a singleton: "
      f"{sum(1 for s in te_sizes if s == 1)}/{len(te)} "
      f"({100*sum(1 for s in te_sizes if s==1)/max(len(te),1):.1f}%)")
print(f"    train compounds whose scaffold is a singleton: "
      f"{sum(1 for s in tr_sizes if s == 1)}/{len(tr)} "
      f"({100*sum(1 for s in tr_sizes if s==1)/len(tr):.1f}%)")
print(f"  activity balance: train mean pChEMBL={tr.pchembl_value.mean():.3f} "
      f"sd={tr.pchembl_value.std():.3f} | test mean={te.pchembl_value.mean():.3f} "
      f"sd={te.pchembl_value.std():.3f}")
tr2, te2 = scaffold_split(d, 'smiles', train_frac=0.8, seed=7)
print(f"  different seed -> train={len(tr2)} test={len(te2)}  "
      f"same split? {set(tr.index) == set(tr2.index)}")

# ===== INPUT 3 (Variant B): R-group decomposition ==========================
print("\n===== INPUT 3: R-group decomposition on a real analog series =====")


def decompose_series(compounds, scaffold_smiles_with_R):      # SKILL.md verbatim
    scaffold = Chem.MolFromSmiles(scaffold_smiles_with_R)
    if scaffold is None:
        raise ValueError('Invalid scaffold SMARTS/SMILES')
    parsed = [(i, Chem.MolFromSmiles(s)) for i, s in enumerate(compounds)]
    invalid = [i for i, mol in parsed if mol is None]
    if invalid:
        raise ValueError(f'Invalid compound SMILES at positions: {invalid}')
    mols = [mol for _, mol in parsed]
    decomp, unmatched = rgd.RGroupDecompose([scaffold], mols, asSmiles=True)
    unmatched_set = set(unmatched)
    matched_positions = [i for i in range(len(mols)) if i not in unmatched_set]
    return decomp, matched_positions, list(unmatched)


print("  (a) the SKILL.md worked example, verbatim:")
try:
    t = decompose_series(['c1ccc(C(=O)NCC)cc1F', 'c1ccc(C(=O)NCCC)cc1Cl'],
                         'c1ccc(C(=O)N[*:1])cc1-[*:2]')
    print(f"      decomp={t[0]}")
    print(f"      matched={t[1]} unmatched={t[2]}")
except Exception as e:                                        # noqa: BLE001
    print(f"      RAISED {type(e).__name__}: {e}")

print("  (b) a real 20-compound series from the library:")
big_scaff, members = max(cl.items(), key=lambda kv: len(kv[1]))
print(f"      scaffold with the most members (n={len(members)}): {big_scaff[:70]}")
core = big_scaff
try:
    decomp, matched, unmatched = decompose_series(members[:20], core)
    print(f"      decomposed against the bare scaffold: matched={len(matched)} "
          f"unmatched={len(unmatched)}")
    if decomp:
        keys = sorted({k for row in decomp for k in row})
        print(f"      R-group columns found: {keys}")
        for row in decomp[:3]:
            print(f"        {{{', '.join(f'{k}: {row[k][:34]}' for k in keys)}}}")
except Exception as e:                                        # noqa: BLE001
    print(f"      RAISED {type(e).__name__}: {e}")

# ===== INPUT 4 (Edge): the documented scaffold failure modes ===============
print("\n===== INPUT 4: the documented scaffold failure modes =====")
print("  (a) the SKILL.md worked example's exact claim:")
m = Chem.MolFromSmiles('Cc1ccc(C(=O)NCC2CCCC2)cc1')
bm = MurckoScaffold.GetScaffoldForMol(m)
gen = MurckoScaffold.MakeScaffoldGeneric(bm)
print(f"      bemis_murcko  = {Chem.MolToSmiles(bm)}")
print(f"      SKILL.md says   c1ccc(C(=O)NCC2CCCC2)cc1  -> "
      f"{Chem.MolToSmiles(bm) == 'c1ccc(C(=O)NCC2CCCC2)cc1'}")
print(f"      generic       = {Chem.MolToSmiles(gen)}")
print(f"      SKILL.md says   C1CCC(C(C)CCC2CCCC2)CC1   -> "
      f"{Chem.MolToSmiles(gen) == 'C1CCC(C(C)CCC2CCCC2)CC1'}")

print("  (b) linear molecule -> empty scaffold:")
for lbl, smi in [('palmitic acid', 'CCCCCCCCCCCCCCCC(=O)O'), ('ethylamine', 'CCN'),
                 ('glucose', 'OC[C@H]1OC(O)[C@H](O)[C@@H](O)[C@@H]1O')]:
    s = Chem.MolToSmiles(MurckoScaffold.GetScaffoldForMol(Chem.MolFromSmiles(smi)))
    print(f"      {lbl:16} -> {s!r}  empty={s == ''}")

print("  (c) generic framework loses heteroatoms:")
pairs = [('benzene', 'c1ccccc1'), ('pyridine', 'c1ccncc1'), ('pyrimidine', 'c1cncnc1'),
         ('thiophene', 'c1ccsc1'), ('furan', 'c1ccoc1')]
gens = {}
for lbl, smi in pairs:
    mm = Chem.MolFromSmiles(smi)
    b = MurckoScaffold.GetScaffoldForMol(mm)
    g = Chem.MolToSmiles(MurckoScaffold.MakeScaffoldGeneric(b))
    gens.setdefault(g, []).append(lbl)
    print(f"      {lbl:11} BM={Chem.MolToSmiles(b):12} generic={g}")
for g, labs in gens.items():
    if len(labs) > 1:
        print(f"      -> collapsed to one generic framework {g}: {labs}")

print("  (d) spiro / bridged rings:")
for lbl, smi in [('spiro[4.5]decane', 'C1CCC2(CC1)CCCC2'),
                 ('a spiro drug-like', 'O=C1NC2(CCN(Cc3ccccc3)CC2)C(=O)N1'),
                 ('bridged tropane', 'CN1C2CCC1CC(O)C2')]:
    mm = Chem.MolFromSmiles(smi)
    print(f"      {lbl:20} BM={Chem.MolToSmiles(MurckoScaffold.GetScaffoldForMol(mm))}")

# ===== INPUT 6 (Scope boundary): generic framework for series detection ====
print("\n===== INPUT 6: what happens if generic frameworks are used to define series =====")
gmap = defaultdict(list)
for smi in list(df.canonical_smiles)[:1500]:
    mm = Chem.MolFromSmiles(smi)
    b = MurckoScaffold.GetScaffoldForMol(mm)
    try:
        g = Chem.MolToSmiles(MurckoScaffold.MakeScaffoldGeneric(b))
    except Exception:                                          # noqa: BLE001
        g = 'ERROR'
    gmap[g].append(smi)
bmap = scaffold_clusters(list(df.canonical_smiles)[:1500])
print(f"  1500 compounds -> {len(bmap)} Bemis-Murcko scaffolds vs "
      f"{len(gmap)} generic frameworks ({len(bmap)/max(len(gmap),1):.2f}x collapse)")
worst = max(gmap.items(), key=lambda kv: len(kv[1]))
distinct_bm = {Chem.MolToSmiles(MurckoScaffold.GetScaffoldForMol(Chem.MolFromSmiles(s)))
               for s in worst[1]}
print(f"  largest generic framework has {len(worst[1])} compounds spanning "
      f"{len(distinct_bm)} distinct Bemis-Murcko scaffolds")
print(f"  MakeScaffoldGeneric errors: {len(gmap.get('ERROR', []))}")

# ===== INPUT 7 (Adversarial): tautomer-induced scaffold variation ==========
print("\n===== INPUT 7: 'singleton scaffolds dominate -- check for tautomers' =====")
enum = rdMolStandardize.TautomerEnumerator()
CASES = [('2-pyridone / 2-hydroxypyridine', 'O=c1cccc[nH]1', 'Oc1ccccn1'),
         ('4-pyrimidinone pair', 'O=c1cc[nH]cn1', 'Oc1ccncn1'),
         ('2-thiouracil pair', 'O=c1cc[nH]c(=S)[nH]1', 'Oc1ccnc(S)n1'),
         ('barbiturate keto/enol', 'O=C1CC(=O)NC(=O)N1', 'OC1=CC(=O)NC(=O)N1')]
for lbl, a, b in CASES:
    sa = Chem.MolToSmiles(MurckoScaffold.GetScaffoldForMol(Chem.MolFromSmiles(a)))
    sb = Chem.MolToSmiles(MurckoScaffold.GetScaffoldForMol(Chem.MolFromSmiles(b)))
    ca = Chem.MolToSmiles(MurckoScaffold.GetScaffoldForMol(
        enum.Canonicalize(Chem.MolFromSmiles(a))))
    cb = Chem.MolToSmiles(MurckoScaffold.GetScaffoldForMol(
        enum.Canonicalize(Chem.MolFromSmiles(b))))
    print(f"  {lbl:30} same scaffold raw? {sa == sb:<5}  "
          f"after tautomer canonicalization? {ca == cb}")
print("  -> the Common Errors fix ('canonicalize first') is testable and works above.")
tiny = pd.DataFrame({'smiles': ['c1ccccc1C', 'c1ccccc1CC', 'c1ccccc1CCC']})
try:
    scaffold_split(tiny, 'smiles')
    print("  scaffold_split on a 1-scaffold frame: NO ERROR (defect)")
except ValueError as e:
    print(f"  scaffold_split on a 1-scaffold frame -> ValueError: {e}")
bad = pd.DataFrame({'smiles': ['c1ccccc1C', 'not_a_smiles', 'c1ccncc1CC']})
try:
    scaffold_split(bad, 'smiles')
    print("  scaffold_split with an invalid SMILES: NO ERROR (defect)")
except ValueError as e:
    print(f"  scaffold_split with an invalid SMILES -> ValueError: {e}")
