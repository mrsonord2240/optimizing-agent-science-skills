# Input 5 (Stress) -- bio-molecular-standardization
# Multi-part: (a) keep 13C/2H labels for a tracer subset while stripping them
# everywhere else, (b) survive the documented TautomerEnumerator combinatorial
# explosion, (c) throughput on the full 3,966-row hERG library, (d) how many
# distinct structures collide onto one key once stereo is removed.
import time
import pandas as pd
from rdkit import Chem, RDLogger
from rdkit.Chem.MolStandardize import rdMolStandardize
from chembl_structure_pipeline import standardize_mol, get_parent_mol

RDLogger.DisableLog('rdApp.*')
SRC = r"F:\OpenScience\audit-envs\cheminformatics-hit-triage-analyst\public-data\chembl_herg_CHEMBL240_ic50.csv"

# ---- (a) isotope policy ---------------------------------------------------
print("== (a) isotope policy: keep_isotopes flag ==")
TRACERS = [('[13CH3]C(=O)Oc1ccccc1C(=O)O', 'aspirin 13C-methyl (tracer)'),
           ('[2H]c1ccccc1O', 'phenol-d1 (tracer)'),
           ('CC(=O)Oc1ccccc1C(=O)O', 'aspirin, unlabelled')]


def std_iso(smi, keep_isotopes):
    m = Chem.MolFromSmiles(smi)
    Chem.SanitizeMol(m)
    m = rdMolStandardize.LargestFragmentChooser(preferOrganic=True).choose(m)
    m = rdMolStandardize.Normalizer().normalize(m)
    m = rdMolStandardize.Uncharger(canonicalOrder=True).uncharge(m)
    if not keep_isotopes:
        for a in m.GetAtoms():
            a.SetIsotope(0)
    Chem.AssignStereochemistry(m, cleanIt=True, force=True)
    return Chem.MolToSmiles(m), Chem.MolToInchiKey(m)

for smi, label in TRACERS:
    kk, ik_k = std_iso(smi, True)
    ks, ik_s = std_iso(smi, False)
    print(f"  {label:30} keep=True  {kk:32} {ik_k}")
    print(f"  {'':30} keep=False {ks:32} {ik_s}")
print("  -> labelled and unlabelled aspirin share a key only when keep_isotopes=False:",
      std_iso(TRACERS[0][0], False)[1] == std_iso(TRACERS[2][0], False)[1],
      "| with keep_isotopes=True:",
      std_iso(TRACERS[0][0], True)[1] == std_iso(TRACERS[2][0], True)[1])

# ---- (b) tautomer combinatorial explosion --------------------------------
print("\n== (b) TautomerEnumerator on a polyhydroxylated heterocycle ==")
HARD = 'OC1=C(O)C(=O)c2c(O)cc(O)cc2C1=O'   # polyhydroxy anthraquinone-like
for limits in [(None, None), (50, 100)]:
    e = rdMolStandardize.TautomerEnumerator()
    if limits[0]:
        e.SetMaxTransforms(limits[0])
        e.SetMaxTautomers(limits[1])
    t0 = time.time()
    res = e.Enumerate(Chem.MolFromSmiles(HARD))
    print(f"  limits={limits}  tautomers={len(res)}  status={res.status}  "
          f"{time.time()-t0:.2f}s")
t0 = time.time()
canon = Chem.MolToSmiles(rdMolStandardize.TautomerEnumerator().Canonicalize(
    Chem.MolFromSmiles(HARD)))
print(f"  Canonicalize() only: {canon}  {time.time()-t0:.2f}s")

# ---- (c) throughput on the full library ----------------------------------
print("\n== (c) throughput, full 3,966-row hERG library ==")
df = pd.read_csv(SRC).dropna(subset=['canonical_smiles'])
t0 = time.time()
keys, fails = [], 0
for smi in df.canonical_smiles:
    m = Chem.MolFromSmiles(smi)
    if m is None:
        fails += 1
        continue
    p, excl = get_parent_mol(standardize_mol(m))
    keys.append(Chem.MolToInchiKey(p))
t_chembl = time.time() - t0
print(f"  ChEMBL pipeline only : {len(keys)} mols in {t_chembl:.1f}s "
      f"({len(keys)/t_chembl:.0f} mol/s), parse failures={fails}")

t0 = time.time()
sub = df.canonical_smiles.head(500)
e = rdMolStandardize.TautomerEnumerator()
for smi in sub:
    m = Chem.MolFromSmiles(smi)
    p, _ = get_parent_mol(standardize_mol(m))
    e.Canonicalize(p)
t_taut = time.time() - t0
print(f"  + tautomer canonical : 500 mols in {t_taut:.1f}s ({500/t_taut:.0f} mol/s) "
      f"-> {3966*t_taut/500/60:.1f} min projected for the full library")

# ---- (d) stereo-removal key collisions -----------------------------------
print("\n== (d) key collisions caused by removing stereochemistry ==")
with_stereo, without = set(), set()
for smi in df.canonical_smiles.drop_duplicates():
    m = Chem.MolFromSmiles(smi)
    p, _ = get_parent_mol(standardize_mol(m))
    with_stereo.add(Chem.MolToInchiKey(p))
    q = Chem.Mol(p)
    Chem.RemoveStereochemistry(q)
    without.add(Chem.MolToInchiKey(q))
print(f"  distinct keys with stereo={len(with_stereo)}  without stereo={len(without)}  "
      f"-> {len(with_stereo)-len(without)} distinct compounds silently merged")
