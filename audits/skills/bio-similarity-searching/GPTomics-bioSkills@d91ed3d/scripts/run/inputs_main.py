# bio-similarity-searching -- Inputs 1-6 (input 7 partly here, LSH part in the mhfp venv).
# All code taken from SKILL.md verbatim where a snippet exists.
import time
import numpy as np
import pandas as pd
from rdkit import Chem, DataStructs, RDLogger
from rdkit.Chem import rdFingerprintGenerator, rdFMCS, MACCSkeys
from rdkit.ML.Cluster import Butina
from rdkit.SimDivFilters import rdSimDivPickers

RDLogger.DisableLog('rdApp.*')
SRC = r"F:\OpenScience\audit-envs\cheminformatics-hit-triage-analyst\public-data\chembl_herg_CHEMBL240_ic50.csv"
df = pd.read_csv(SRC).dropna(subset=['canonical_smiles', 'pchembl_value'])
df = df.groupby('canonical_smiles', as_index=False).pchembl_value.mean()
mols = [Chem.MolFromSmiles(s) for s in df.canonical_smiles]
ok = [i for i, m in enumerate(mols) if m is not None]
df, mols = df.iloc[ok].reset_index(drop=True), [mols[i] for i in ok]
gen = rdFingerprintGenerator.GetMorganGenerator(radius=2, fpSize=2048)
fps = [gen.GetFingerprint(m) for m in mols]
print(f"[data] {len(mols)} unique hERG compounds")

# ===== INPUT 1 (Canonical): analog search with the Skill's threshold bands ====
print("\n===== INPUT 1: analog search around astemizole, ECFP4 Tanimoto =====")
Q = 'COc1ccc(CCN2CCC(Nc3nc4ccccc4n3Cc3ccc(F)cc3)CC2)cc1'   # astemizole
qm = Chem.MolFromSmiles(Q)
qfp = gen.GetFingerprint(qm)
t0 = time.time()
sims = np.array(DataStructs.BulkTanimotoSimilarity(qfp, fps))
print(f"  BulkTanimotoSimilarity over {len(fps)} compounds in {time.time()-t0:.3f}s")
print(f"  similarity distribution: mean={sims.mean():.3f} p50={np.median(sims):.3f} "
      f"p95={np.percentile(sims,95):.3f} max={sims.max():.3f}")
BANDS = [(0.85, 1.01, 'same scaffold + close analog'),
         (0.70, 0.85, 'same series, R-group variation'),
         (0.55, 0.70, 'related chemotype'),
         (0.35, 0.55, 'distant analog / possible hop'),
         (0.00, 0.35, 'mostly noise')]
for lo, hi, label in BANDS:
    n = int(((sims >= lo) & (sims < hi)).sum())
    sel = (sims >= lo) & (sims < hi)
    act = df.pchembl_value[sel]
    print(f"  {lo:.2f}-{hi if hi<=1 else 1.0:.2f} {label:32} n={n:5} "
          f"mean pChEMBL={act.mean():.2f}" if n else
          f"  {lo:.2f}-{hi if hi<=1 else 1.0:.2f} {label:32} n=0")
hi = np.argsort(sims)[::-1][:8]
print("  top 8 hits:")
for i in hi:
    print(f"    sim={sims[i]:.3f}  pChEMBL={df.pchembl_value[i]:.2f}  "
          f"{df.canonical_smiles[i][:70]}")
print(f"  query itself present in library: {bool((sims >= 0.999).any())}")

# ===== INPUT 2 (Variant A): Butina, and the Skill's claim about the cutoff ====
print("\n===== INPUT 2: Butina clustering, and what cutoff=0.4 really guarantees =====")
sub_idx = list(range(1200))
sub_fps = [fps[i] for i in sub_idx]
t0 = time.time()
dists = []
for i in range(1, len(sub_fps)):
    s = DataStructs.BulkTanimotoSimilarity(sub_fps[i], sub_fps[:i])
    dists.extend([1 - x for x in s])
clusters = Butina.ClusterData(dists, len(sub_fps), 0.4, isDistData=True)
print(f"  {len(sub_fps)} compounds -> {len(clusters)} clusters in {time.time()-t0:.1f}s; "
      f"largest={max(len(c) for c in clusters)}  singletons="
      f"{sum(1 for c in clusters if len(c)==1)}")
print(f"  distance matrix held {len(dists):,} floats "
      f"({len(dists)*8/1e6:.1f} MB) -- SKILL.md 'Butina materializes O(N^2)'")
viol_centroid = viol_pair = checked = 0
worst = 1.0
for c in clusters:
    if len(c) < 3:
        continue
    cen = c[0]
    for m in c[1:]:
        if DataStructs.TanimotoSimilarity(sub_fps[cen], sub_fps[m]) < 0.6 - 1e-9:
            viol_centroid += 1
    for a in range(1, len(c)):
        for b in range(a + 1, len(c)):
            checked += 1
            s = DataStructs.TanimotoSimilarity(sub_fps[c[a]], sub_fps[c[b]])
            worst = min(worst, s)
            if s < 0.6 - 1e-9:
                viol_pair += 1
print(f"  member-to-CENTROID similarity below 0.6: {viol_centroid} "
      f"(SKILL.md says this should be 0)")
print(f"  non-centroid PAIRS below 0.6: {viol_pair}/{checked} "
      f"(min pair similarity seen = {worst:.3f})")
print("  -> SKILL.md: 'It does NOT guarantee that every pair of non-centroid members "
      "has Tanimoto >= 0.6' -- confirmed by the pair count above.")
rev = list(reversed(sub_idx))
rev_fps = [fps[i] for i in rev]
d2 = []
for i in range(1, len(rev_fps)):
    s = DataStructs.BulkTanimotoSimilarity(rev_fps[i], rev_fps[:i])
    d2.extend([1 - x for x in s])
c2 = Butina.ClusterData(d2, len(rev_fps), 0.4, isDistData=True)
print(f"  same 1200 compounds in reverse order -> {len(c2)} clusters "
      f"(vs {len(clusters)}); SKILL.md Common Errors: 'centroids change when input "
      f"order changes' -> {'CONFIRMED' if len(c2)!=len(clusters) or set(c[0] for c in clusters)!=set(rev[c[0]] for c in c2) else 'not reproduced'}")

# ===== INPUT 3 (Variant B): Tversky asymmetry ================================
print("\n===== INPUT 3: Tversky alpha=1,beta=0 for substructure-like ranking =====")
FRAG = Chem.MolFromSmiles('c1ccc2[nH]c(nc2c1)N')       # 2-aminobenzimidazole
ffp = gen.GetFingerprint(FRAG)
tv = np.array([DataStructs.TverskySimilarity(ffp, f, 1.0, 0.0) for f in fps])
tv_rev = np.array([DataStructs.TverskySimilarity(f, ffp, 1.0, 0.0) for f in fps])
tan = np.array(DataStructs.BulkTanimotoSimilarity(ffp, fps))
print(f"  Tversky(query->lib, a=1,b=0): mean={tv.mean():.3f} max={tv.max():.3f} "
      f"n>=0.9: {(tv>=0.9).sum()}")
print(f"  Tversky(lib->query, a=1,b=0): mean={tv_rev.mean():.3f} max={tv_rev.max():.3f}")
print(f"  asymmetric? mean |difference| = {np.abs(tv-tv_rev).mean():.3f} "
      f"-> {'YES' if np.abs(tv-tv_rev).mean() > 0.01 else 'NO'}")
print(f"  Tanimoto for the same pairs: mean={tan.mean():.3f} max={tan.max():.3f} "
      f"n>=0.9: {(tan>=0.9).sum()}")
patt = Chem.MolFromSmarts('c1ccc2[nH]c(nc2c1)N')
true_sub = np.array([m.HasSubstructMatch(patt) for m in mols])
print(f"  compounds actually CONTAINING the fragment: {true_sub.sum()}")
for thr in [0.7, 0.8, 0.9]:
    sel = tv >= thr
    if sel.sum():
        print(f"    Tversky>={thr}: n={sel.sum():4}  of which truly contain it: "
              f"{int((sel & true_sub).sum()):4} ({100*(sel&true_sub).sum()/sel.sum():.0f}%)")
    sel = tan >= thr
    print(f"    Tanimoto>={thr}: n={sel.sum():4}  of which truly contain it: "
          f"{int((sel & true_sub).sum()):4}")

# ===== INPUT 4 (Edge): activity cliffs =======================================
print("\n===== INPUT 4: activity cliffs at Tanimoto>=0.85 and >=2 log units =====")
t0 = time.time()
cliffs = []
act = df.pchembl_value.to_numpy()
for i in range(len(fps)):
    s = DataStructs.BulkTanimotoSimilarity(fps[i], fps[i + 1:])
    for j_off, sim in enumerate(s):
        if sim >= 0.85:
            j = i + 1 + j_off
            gap = abs(act[i] - act[j])
            if gap >= 2.0:
                cliffs.append((i, j, sim, gap))
print(f"  all-pairs scan of {len(fps)} compounds in {time.time()-t0:.1f}s")
print(f"  activity cliffs found: {len(cliffs)}")
pairs_high = sum(1 for i in range(len(fps))
                 for s in DataStructs.BulkTanimotoSimilarity(fps[i], fps[i+1:]) if s >= 0.85)
print(f"  pairs at Tanimoto>=0.85: {pairs_high}  -> cliff rate "
      f"{100*len(cliffs)/max(pairs_high,1):.2f}%")
for i, j, s, g in sorted(cliffs, key=lambda x: -x[3])[:5]:
    print(f"    sim={s:.3f} gap={g:.2f}  pChEMBL {act[i]:.2f} vs {act[j]:.2f}")
    print(f"      {df.canonical_smiles[i][:72]}")
    print(f"      {df.canonical_smiles[j][:72]}")
print("  -> SKILL.md: 'Tanimoto above 0.7 is not a guarantee of activity preservation'.")

# ===== INPUT 5 (Stress): MaxMin + MCS ========================================
print("\n===== INPUT 5: MaxMin diversity picking and MCS behaviour =====")
picker = rdSimDivPickers.MaxMinPicker()
t0 = time.time()
sel = list(picker.LazyBitVectorPick(fps, len(fps), 100, seed=42))
print(f"  LazyBitVectorPick 100 of {len(fps)} in {time.time()-t0:.2f}s")
sel2 = list(picker.LazyBitVectorPick(fps, len(fps), 100, seed=42))
print(f"  identical on repeat with the same seed: {sel == sel2}")
sel3 = list(picker.LazyBitVectorPick(fps, len(fps), 100, seed=7))
print(f"  different with a different seed: {sel != sel3} "
      f"(overlap {len(set(sel)&set(sel3))}/100)")
print(f"  picker returned the first N inputs? {sel == list(range(100))} "
      f"(SKILL.md Common Errors names this failure)")
pw = []
for a in range(len(sel)):
    for b in range(a + 1, len(sel)):
        pw.append(DataStructs.TanimotoSimilarity(fps[sel[a]], fps[sel[b]]))
rnd = np.random.RandomState(42).choice(len(fps), 100, replace=False)
pw_r = [DataStructs.TanimotoSimilarity(fps[rnd[a]], fps[rnd[b]])
        for a in range(100) for b in range(a + 1, 100)]
print(f"  mean pairwise Tanimoto: MaxMin={np.mean(pw):.3f}  random={np.mean(pw_r):.3f} "
      f"(max pair MaxMin={max(pw):.3f})")

print("  MCS:")
for label, idx, to in [('10 close analogs', list(np.argsort(sims)[::-1][:10]), 60),
                       ('40 diverse compounds', sel[:40], 5),
                       ('40 diverse compounds', sel[:40], 60)]:
    ms = [mols[i] for i in idx]
    params = rdFMCS.MCSParameters()
    params.Timeout = to
    params.BondCompareParameters.MatchFusedRings = True
    params.BondCompareParameters.MatchFusedRingsStrict = True
    params.BondCompareParameters.RingMatchesRingOnly = True
    params.AtomCompareParameters.MatchValences = False
    t0 = time.time()
    r = rdFMCS.FindMCS(ms, params)
    print(f"    {label:22} timeout={to:3}s -> atoms={r.numAtoms:3} bonds={r.numBonds:3} "
          f"canceled={r.canceled} in {time.time()-t0:.1f}s")

# ===== INPUT 6 (Scope boundary): threshold transfer ==========================
print("\n===== INPUT 6: do the per-fingerprint threshold heuristics transfer? =====")
FPS = {
    'ECFP4': rdFingerprintGenerator.GetMorganGenerator(radius=2, fpSize=2048),
    'FCFP4': rdFingerprintGenerator.GetMorganGenerator(
        radius=2, fpSize=2048,
        atomInvariantsGenerator=rdFingerprintGenerator.GetMorganFeatureAtomInvGen()),
    'AtomPair': rdFingerprintGenerator.GetAtomPairGenerator(fpSize=2048),
}
CLAIMED = {'ECFP4': 0.70, 'FCFP4': 0.60, 'AtomPair': 0.55, 'MACCS': 0.85}
sample = list(range(0, len(mols), 4))[:800]
print(f"  {'fp':10} {'claimed thr':12} {'mean sim':9} {'p95':7} {'p99':7} "
      f"{'% pairs above claimed thr':>26}")
for name, g in FPS.items():
    f2 = [g.GetFingerprint(mols[i]) for i in sample]
    allp = []
    for i in range(1, len(f2)):
        allp.extend(DataStructs.BulkTanimotoSimilarity(f2[i], f2[:i]))
    allp = np.array(allp)
    thr = CLAIMED[name]
    print(f"  {name:10} {thr:<12.2f} {allp.mean():<9.3f} {np.percentile(allp,95):<7.3f} "
          f"{np.percentile(allp,99):<7.3f} {100*(allp>=thr).mean():>25.3f}%")
f2 = [MACCSkeys.GenMACCSKeys(mols[i]) for i in sample]
allp = []
for i in range(1, len(f2)):
    allp.extend(DataStructs.BulkTanimotoSimilarity(f2[i], f2[:i]))
allp = np.array(allp)
print(f"  {'MACCS':10} {0.85:<12.2f} {allp.mean():<9.3f} {np.percentile(allp,95):<7.3f} "
      f"{np.percentile(allp,99):<7.3f} {100*(allp>=0.85).mean():>25.3f}%")
print("  -> if the heuristics were calibrated to each other, the % of pairs above")
print("     each threshold would be similar across rows.")

# ===== INPUT 7 part A: Tanimoto 1.0 != same molecule =========================
print("\n===== INPUT 7a: does Tanimoto 1.0 imply identity on this library? =====")
coll = 0
examples = []
for i in range(len(fps)):
    s = DataStructs.BulkTanimotoSimilarity(fps[i], fps[i + 1:])
    for j_off, v in enumerate(s):
        if v >= 0.99999:
            j = i + 1 + j_off
            coll += 1
            if len(examples) < 4:
                examples.append((i, j))
print(f"  pairs with folded-ECFP4 Tanimoto = 1.0 but different canonical SMILES: {coll}")
for i, j in examples:
    same_sparse = (gen.GetSparseCountFingerprint(mols[i]).GetNonzeroElements() ==
                   gen.GetSparseCountFingerprint(mols[j]).GetNonzeroElements())
    print(f"    {df.canonical_smiles[i][:62]}")
    print(f"    {df.canonical_smiles[j][:62]}")
    print(f"      identical unhashed sparse fingerprint too? {same_sparse}  "
          f"identical InChIKey? "
          f"{Chem.MolToInchiKey(mols[i]) == Chem.MolToInchiKey(mols[j])}")
print("  -> SKILL.md fix: 'For exact identity compare canonical SMILES or InChIKey, "
      "not fingerprint. Use unhashed sparse fingerprint to disambiguate.'")
