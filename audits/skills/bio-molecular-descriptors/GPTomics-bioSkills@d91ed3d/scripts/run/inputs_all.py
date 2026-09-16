# bio-molecular-descriptors -- all 7 inputs.
# Every API is taken from SKILL.md or examples/calculate_descriptors.py verbatim.
import sys
import time
import numpy as np
import pandas as pd
from rdkit import Chem, RDLogger, DataStructs
from rdkit.Chem import (AllChem, Descriptors, Descriptors3D, Lipinski, MACCSkeys,
                        QED, rdFingerprintGenerator)

RDLogger.DisableLog('rdApp.*')
SRC = r"F:\OpenScience\audit-envs\cheminformatics-hit-triage-analyst\public-data\chembl_herg_CHEMBL240_ic50.csv"
df = pd.read_csv(SRC).dropna(subset=['canonical_smiles']).drop_duplicates('molecule_chembl_id')
mols = [Chem.MolFromSmiles(s) for s in df.canonical_smiles]
mols = [m for m in mols if m is not None]
print(f"[load] {len(mols)} distinct ChEMBL hERG compounds")

# ===================== INPUT 1 (Canonical): physchem + rule-set panel ======
print("\n===== INPUT 1: physchem panel + rule sets over 1,000 compounds =====")


def physchem(mol):                       # SKILL.md "Physicochemical Descriptors"
    return {
        'MolWt': Descriptors.MolWt(mol), 'MolLogP': Descriptors.MolLogP(mol),
        'HBD': Lipinski.NumHDonors(mol), 'HBA': Lipinski.NumHAcceptors(mol),
        'TPSA': Descriptors.TPSA(mol), 'RotBonds': Lipinski.NumRotatableBonds(mol),
        'AromRings': Lipinski.NumAromaticRings(mol),
        'FractionCSP3': Descriptors.FractionCSP3(mol), 'QED': QED.qed(mol),
    }


sub = mols[:1000]
t0 = time.time()
P = pd.DataFrame([physchem(m) for m in sub])
print(f"  computed 9 descriptors x 1000 mols in {time.time()-t0:.1f}s")
print("  every SKILL.md descriptor call resolved:", list(P.columns))
print(P.describe().loc[['mean', 'min', 'max']].round(2).to_string())
viol = ((P.MolWt > 500).astype(int) + (P.MolLogP > 5).astype(int) +
        (P.HBD > 5).astype(int) + (P.HBA > 10).astype(int))
print(f"  Lipinski Ro5: 0 violations={int((viol == 0).sum())}  1={int((viol == 1).sum())}  "
      f">=2={int((viol >= 2).sum())}")
print(f"  Veber (RotB<=10 and TPSA<=140): {int(((P.RotBonds <= 10) & (P.TPSA <= 140)).sum())}/1000")
print(f"  Egan (LogP<=5.88, TPSA<=131.6): {int(((P.MolLogP <= 5.88) & (P.TPSA <= 131.6)).sum())}/1000")
print(f"  lead-like (MW<=350, LogP<=3):  {int(((P.MolWt <= 350) & (P.MolLogP <= 3)).sum())}/1000")
print(f"  Ro3 fragment (MW<=300,LogP<=3,HBD<=3,HBA<=3,RotB<=3,TPSA<=60): "
      f"{int(((P.MolWt<=300)&(P.MolLogP<=3)&(P.HBD<=3)&(P.HBA<=3)&(P.RotBonds<=3)&(P.TPSA<=60)).sum())}/1000")
print(f"  QED >= 0.5: {int((P.QED >= 0.5).sum())}/1000   QED nan: {int(P.QED.isna().sum())}")
print(f"  BBB TPSA<=90: {int((P.TPSA <= 90).sum())}/1000")

# ===================== INPUT 2 (Variant A): fingerprint taxonomy ==========
print("\n===== INPUT 2: every fingerprint in the taxonomy table =====")
m = Chem.MolFromSmiles('CC(C)NCC(O)COc1ccc(CC(N)=O)cc1')     # atenolol
GENS = {}
try:
    GENS['ECFP4'] = rdFingerprintGenerator.GetMorganGenerator(radius=2, fpSize=2048)
    GENS['ECFP6'] = rdFingerprintGenerator.GetMorganGenerator(radius=3, fpSize=2048)
    inv = rdFingerprintGenerator.GetMorganFeatureAtomInvGen()
    GENS['FCFP4'] = rdFingerprintGenerator.GetMorganGenerator(
        radius=2, fpSize=2048, atomInvariantsGenerator=inv)
    GENS['RDKitFP'] = rdFingerprintGenerator.GetRDKitFPGenerator(fpSize=2048)
    GENS['AtomPair'] = rdFingerprintGenerator.GetAtomPairGenerator(fpSize=2048)
    GENS['TopTorsion'] = rdFingerprintGenerator.GetTopologicalTorsionGenerator(fpSize=2048)
except Exception as e:                                        # noqa: BLE001
    print(f"  GENERATOR CONSTRUCTION FAILED: {type(e).__name__}: {e}")
for name, g in GENS.items():
    fp = g.GetFingerprint(m)
    cnt = g.GetCountFingerprint(m)
    print(f"  {name:10} nBits={fp.GetNumBits():5} on={fp.GetNumOnBits():4} "
          f"count-vector nonzero={cnt.GetNonzeroElements().__len__():4}")
maccs = MACCSkeys.GenMACCSKeys(m)
print(f"  MACCS      nBits={maccs.GetNumBits()} (SKILL.md: 'RDKit MACCS returns 167 bits, "
      f"bit 0 unused') bit0={maccs.GetBit(0)}")
try:
    from rdkit.Avalon import pyAvalonTools
    av = pyAvalonTools.GetAvalonFP(m, nBits=1024)
    print(f"  Avalon     nBits={av.GetNumBits()} on={av.GetNumOnBits()}")
except Exception as e:                                        # noqa: BLE001
    print(f"  Avalon     NOT AVAILABLE: {type(e).__name__}: {e}")
print("  -- FCFP vs ECFP are genuinely different representations:",
      GENS['ECFP4'].GetFingerprint(m) != GENS['FCFP4'].GetFingerprint(m))

# MAP4 and MHFP6, exactly as SKILL.md pins them
print("\n  MAP4 / MHFP6, as pinned in Version Compatibility:")
try:
    import map4                                                # noqa: F401
    print("    map4: importable")
except Exception as e:                                         # noqa: BLE001
    print(f"    map4: NOT INSTALLABLE -- {type(e).__name__}: {e}")
try:
    from mhfp.encoder import MHFPEncoder
    enc = MHFPEncoder(2048)
    print(f"    mhfp: importable in this venv; has encode_mol? "
          f"{hasattr(enc, 'encode_mol')}; has encode? {hasattr(enc, 'encode')}")
except Exception as e:                                         # noqa: BLE001
    print(f"    mhfp: not in the shared venv -- {type(e).__name__}: {e}")

# ===================== INPUT 3 (Edge): radius / bit-collision claims ======
print("\n===== INPUT 3: ECFP radius math and bit collisions =====")
for nb in [512, 1024, 2048, 4096, 8192]:
    g = rdFingerprintGenerator.GetMorganGenerator(radius=2, fpSize=nb)
    folded = np.array([g.GetFingerprint(x).GetNumOnBits() for x in sub[:500]])
    sparse = np.array([len(g.GetSparseCountFingerprint(x).GetNonzeroElements())
                       for x in sub[:500]])
    coll = 100 * (1 - folded.mean() / sparse.mean())
    print(f"  nBits={nb:5} mean on-bits={folded.mean():6.1f}  mean distinct "
          f"environments={sparse.mean():6.1f}  -> {coll:5.2f}% lost to collisions")
print("  radius/diameter table check (ECFP-X: X is the DIAMETER, RDKit radius = X/2):")
for label, r in [('ECFP0', 0), ('ECFP2', 1), ('ECFP4', 2), ('ECFP6', 3)]:
    g = rdFingerprintGenerator.GetMorganGenerator(radius=r, fpSize=2048)
    n = len(g.GetSparseCountFingerprint(m).GetNonzeroElements())
    print(f"    {label} (radius={r}) distinct environments on atenolol = {n}")

# ===================== INPUT 4 (Variant B): 3D over an ensemble ===========
print("\n===== INPUT 4: 3D shape descriptors over a conformer ensemble =====")
FLEX = [('atenolol (8 rot bonds)', 'CC(C)NCC(O)COc1ccc(CC(N)=O)cc1'),
        ('butanol (SKILL.md example)', 'CCCCO'),
        ('verapamil (13 rot bonds)',
         'COc1ccc(CCN(C)CCCC(C#N)(c2ccc(OC)c(OC)c2)C(C)C)cc1OC'),
        ('ferrocene-like (no MMFF params)', '[Fe]')]
for label, smi in FLEX:
    mm = Chem.MolFromSmiles(smi)
    if mm is None:
        print(f"  {label}: SMILES did not parse")
        continue
    mm = Chem.AddHs(mm)
    params = AllChem.ETKDGv3()
    params.randomSeed = 42
    t0 = time.time()
    conf_ids = AllChem.EmbedMultipleConfs(mm, numConfs=20, params=params)
    if not conf_ids:
        print(f"  {label}: ETKDGv3 generated no conformers (SKILL.md raises RuntimeError here)")
        continue
    if not AllChem.MMFFHasAllMoleculeParams(mm):
        print(f"  {label}: MMFF94 params unavailable (SKILL.md raises ValueError here)")
        continue
    res = AllChem.MMFFOptimizeMoleculeConfs(mm)
    nonconv = sum(1 for s, _ in res if s != 0)
    asph = [Descriptors3D.Asphericity(mm, confId=c) for c in conf_ids]
    print(f"  {label:32} confs={len(conf_ids):3} non-converged={nonconv:2} "
          f"asphericity mean={np.mean(asph):.3f} sd={np.std(asph):.3f} "
          f"range=[{min(asph):.3f},{max(asph):.3f}] {time.time()-t0:.1f}s")
    if nonconv:
        print(f"      -> SKILL.md would raise RuntimeError and discard all "
              f"{len(conf_ids)} conformers because {nonconv} did not converge")

# reproducibility of the single-conformer path (the example's function)
print("  single-conformer reproducibility (examples/calculate_descriptors.py path):")
vals = []
for _ in range(3):
    mm = Chem.AddHs(Chem.MolFromSmiles('CC(C)NCC(O)COc1ccc(CC(N)=O)cc1'))
    st = AllChem.EmbedMolecule(mm, AllChem.ETKDGv3())
    AllChem.MMFFOptimizeMolecule(mm)
    vals.append(round(Descriptors3D.Asphericity(mm), 4))
print(f"    3 independent runs of EmbedMolecule+Asphericity: {vals}  identical={len(set(vals))==1}")

# ===================== INPUT 5 (Stress): full-library featurization =======
print("\n===== INPUT 5: full-library featurization for ML =====")
g = rdFingerprintGenerator.GetMorganGenerator(radius=2, fpSize=2048)
t0 = time.time()
X = np.zeros((len(mols), 2048), dtype=np.uint8)
for i, mm in enumerate(mols):
    DataStructs.ConvertToNumpyArray(g.GetFingerprint(mm), X[i])
t_fp = time.time() - t0
print(f"  ECFP4 2048 for {len(mols)} mols: {t_fp:.1f}s ({len(mols)/t_fp:.0f} mol/s), "
      f"matrix {X.shape} {X.nbytes/1e6:.1f} MB")
print(f"  bits never set across the library: {(X.sum(0) == 0).sum()}/2048  "
      f"mean on-bits/mol {X.sum(1).mean():.1f}")
t0 = time.time()
P2 = pd.DataFrame([physchem(mm) for mm in mols])
print(f"  9-descriptor panel for {len(mols)} mols: {time.time()-t0:.1f}s")
print(f"  nan/inf in the descriptor panel: {int(P2.isna().sum().sum())} nan, "
      f"{int(np.isinf(P2.to_numpy(dtype=float)).sum())} inf")

# ===================== INPUT 6 (Scope boundary): QED as a filter ==========
print("\n===== INPUT 6: QED on fragments and natural products =====")
PROBES = [('aspirin (drug)', 'CC(=O)Oc1ccccc1C(=O)O'),
          ('atenolol (drug)', 'CC(C)NCC(O)COc1ccc(CC(N)=O)cc1'),
          ('imatinib (drug)', 'Cc1ccc(NC(=O)c2ccc(CN3CCN(C)CC3)cc2)cc1Nc1nccc(-c2cccnc2)n1'),
          ('benzamidine (fragment)', 'NC(=N)c1ccccc1'),
          ('indole (fragment)', 'c1ccc2[nH]ccc2c1'),
          ('phenol (fragment)', 'Oc1ccccc1'),
          ('paclitaxel (natural product)',
           'CC(=O)O[C@@H]1C(=O)[C@]2(C)[C@@H](O)C[C@H]3OC[C@]3(OC(C)=O)[C@H]2[C@H](OC(=O)c2ccccc2)[C@]2(O)C[C@H](OC(=O)[C@H](O)[C@@H](NC(=O)c3ccccc3)c3ccccc3)C(C)=C1C2(C)C'),
          ('cyclosporine-like peptide', 'CC(C)C[C@H](NC(=O)CN)C(=O)N[C@@H](CC(C)C)C(=O)N[C@@H](Cc1ccccc1)C(=O)O'),
          ('sodium ion (charged)', '[Na+]'),
          ('EDTA tetraanion (charged)', 'O=C([O-])CN(CC(=O)[O-])CCN(CC(=O)[O-])CC(=O)[O-]')]
for label, smi in PROBES:
    mm = Chem.MolFromSmiles(smi)
    if mm is None:
        print(f"  {label:32} SMILES did not parse")
        continue
    try:
        q = QED.qed(mm)
        qs = f"{q:.3f}"
    except Exception as e:                                     # noqa: BLE001
        qs = f"RAISED {type(e).__name__}"
    print(f"  {label:32} MW={Descriptors.MolWt(mm):7.1f} QED={qs:>10}  "
          f"passes a QED>=0.5 gate: {qs not in ('nan',) and qs[0].isdigit() and float(qs) >= 0.5 if qs[0].isdigit() else 'n/a'}")

# ===================== INPUT 7 (Adversarial): charges and LogP ===========
print("\n===== INPUT 7: partial charges and the LogP model question =====")
mm = Chem.MolFromSmiles('CC(=O)Oc1ccccc1C(=O)O')
AllChem.ComputeGasteigerCharges(mm)
ch = [mm.GetAtomWithIdx(i).GetPropsAsDict().get('_GasteigerCharge')
      for i in range(mm.GetNumAtoms())]
print(f"  Gasteiger on aspirin: {len(ch)} charges, sum={sum(ch):+.4f} "
      f"(formal charge {Chem.GetFormalCharge(mm)}), min={min(ch):+.3f} max={max(ch):+.3f}")
bad = Chem.MolFromSmiles('[Fe+2].[Fe+2]')
AllChem.ComputeGasteigerCharges(bad)
ch2 = [bad.GetAtomWithIdx(i).GetPropsAsDict().get('_GasteigerCharge')
       for i in range(bad.GetNumAtoms())]
print(f"  Gasteiger on [Fe+2].[Fe+2]: {ch2}  -> "
      f"{'nan produced silently' if any(x != x for x in ch2) else 'finite values returned'}")
print(f"  Crippen MolLogP(aspirin) = {Descriptors.MolLogP(mm):.2f}  "
      f"(experimental logP of aspirin is 1.19; SKILL.md says Crippen != XLogP3)")
print(f"  MolWt={Descriptors.MolWt(mm):.3f}  ExactMolWt={Descriptors.ExactMolWt(mm):.4f}  "
      f"difference={Descriptors.MolWt(mm)-Descriptors.ExactMolWt(mm):+.3f} "
      f"(SKILL.md Common Errors: average vs monoisotopic)")
print(f"  MACCS literature-166 slice: full={len(np.array(MACCSkeys.GenMACCSKeys(mm)))} "
      f"sliced[1:]={len(np.array(MACCSkeys.GenMACCSKeys(mm))[1:])}")
