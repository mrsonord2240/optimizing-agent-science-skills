# bio-molecular-io -- all 7 inputs. Every snippet is taken from SKILL.md verbatim.
import os
import subprocess
import time
import pandas as pd
from rdkit import Chem, RDLogger
from rdkit.Chem import AllChem
from rdkit.Chem.inchi import MolToInchi, MolToInchiKey, InchiToInchiKey

RDLogger.DisableLog('rdApp.*')
D = r"F:\OpenScience\audits\bio-molecular-io\run"
SRC = r"F:\OpenScience\audit-envs\cheminformatics-hit-triage-analyst\public-data\chembl_herg_CHEMBL240_ic50.csv"
df = pd.read_csv(SRC).dropna(subset=['canonical_smiles', 'pchembl_value'])
df = df.groupby('canonical_smiles', as_index=False).pchembl_value.mean()
print(f"[data] {len(df)} unique hERG SMILES")


def parse_smiles_safe(smi):                                 # SKILL.md verbatim
    mol = Chem.MolFromSmiles(smi)
    if mol is None:
        return None, 'parse_failure'
    Chem.AssignStereochemistry(mol, cleanIt=True, force=True)
    canon = Chem.MolToSmiles(mol)
    round_trip = Chem.MolFromSmiles(canon)
    if Chem.MolToSmiles(round_trip) != canon:
        return mol, 'round_trip_unstable'
    return mol, 'ok'


# ===== INPUT 1 (Canonical): load a library, write SDF with props, read back ==
print("\n===== INPUT 1: SMILES -> SDF with properties -> read back =====")
from collections import Counter
t0 = time.time()
status = Counter()
mols = []
for smi, act in zip(df.canonical_smiles, df.pchembl_value):
    m, s = parse_smiles_safe(smi)
    status[s] += 1
    if m is not None:
        m.SetProp('_Name', f'CMP{len(mols):05d}')
        m.SetProp('pChEMBL', f'{act:.3f}')
        mols.append(m)
print(f"  parse_smiles_safe over {len(df)} SMILES in {time.time()-t0:.1f}s: {dict(status)}")
w = Chem.SDWriter(os.path.join(D, 'library.sdf'))
for m in mols:
    w.write(m)
w.close()
size = os.path.getsize(os.path.join(D, 'library.sdf'))
print(f"  wrote library.sdf: {len(mols)} records, {size/1e6:.1f} MB")

supplier = Chem.SDMolSupplier(os.path.join(D, 'library.sdf'), removeHs=False, sanitize=True)
back, fails = [], []
for i, m in enumerate(supplier):
    if m is None:
        fails.append(i)
        continue
    back.append((m, m.GetPropsAsDict()))
print(f"  parsed: {len(back)}; failed: {len(fails)}")
props_ok = sum(1 for _, p in back if 'pChEMBL' in p)
print(f"  records carrying the pChEMBL property: {props_ok}/{len(back)}")
same = sum(1 for (m, _), orig in zip(back, mols)
           if Chem.MolToSmiles(m) == Chem.MolToSmiles(orig))
print(f"  SMILES identical after the SDF round trip: {same}/{len(back)}")
stereo_orig = sum(1 for m in mols if '@' in Chem.MolToSmiles(m))
stereo_back = sum(1 for m, _ in back if '@' in Chem.MolToSmiles(m))
print(f"  compounds carrying tetrahedral stereo: before={stereo_orig} after={stereo_back}")

# ===== INPUT 2 (Variant A): the V2000 999-atom limit ========================
print("\n===== INPUT 2: SDF V2000 999-atom limit and SetForceV3000 =====")
big = Chem.MolFromSmiles('C' * 1200)
print(f"  built a 1200-carbon chain: atoms={big.GetNumAtoms()}")
p2 = os.path.join(D, 'big_v2000.sdf')
w = Chem.SDWriter(p2)
try:
    w.write(big)
    w.close()
    head = open(p2).readlines()[3][:40]
    print(f"  default SDWriter wrote it; counts line = {head!r}")
    rb = next(iter(Chem.SDMolSupplier(p2)))
    print(f"  read back: {'FAILED (None)' if rb is None else f'{rb.GetNumAtoms()} atoms'}")
except Exception as e:                                       # noqa: BLE001
    w.close()
    print(f"  default SDWriter RAISED {type(e).__name__}: {e}")
p3 = os.path.join(D, 'big_v3000.sdf')
w = Chem.SDWriter(p3)
w.SetForceV3000(True)                                        # SKILL.md fix
w.write(big)
w.close()
head = open(p3).readlines()[3][:40]
print(f"  SetForceV3000(True) counts line = {head!r}")
rb = next(iter(Chem.SDMolSupplier(p3)))
print(f"  read back (RDKit auto-detects V3000): "
      f"{'FAILED (None)' if rb is None else f'{rb.GetNumAtoms()} atoms'}")

# ===== INPUT 3 (Variant B): Open Babel route ================================
print("\n===== INPUT 3: the Open Babel pybel route =====")
try:
    from openbabel import pybel                              # SKILL.md fix for OB 3.x
    print("  'from openbabel import pybel' -> OK (the documented OB 3.x import path)")
except Exception as e:                                       # noqa: BLE001
    print(f"  pybel import FAILED: {type(e).__name__}: {e}")
    pybel = None
if pybel is not None:
    mol = pybel.readstring('smi', 'CC(C)NCC(O)COc1ccc(CC(N)=O)cc1')
    print(f"  pybel.readstring -> {mol.write('smi').strip()}")
    for fmt in ['smi', 'inchi', 'inchikey', 'sdf', 'mol2', 'pdbqt']:
        try:
            out = mol.write(fmt).strip()
            print(f"    write({fmt!r:10}) -> OK, {len(out)} chars")
        except Exception as e:                               # noqa: BLE001
            print(f"    write({fmt!r:10}) -> {type(e).__name__}: {str(e)[:80]}")
    OBABEL = os.path.join("F:\\", "OpenScience", "audit-envs", "cheminformatics-hit-triage-analyst", "Scripts", "obabel.exe")
    r = subprocess.run([OBABEL, '-L', 'formats'], capture_output=True, text=True)
    fmts = r.stdout + r.stderr
    for f in ['inchi', 'inchikey', 'mol2', 'pdbqt', 'sdf']:
        present = any(line.strip().startswith(f + ' ') or line.strip().startswith(f + '\t')
                      for line in fmts.splitlines())
        print(f"    obabel -L formats lists {f!r}: {present}")
    print("  the SKILL.md snippet writes inchi from pybel -- see the result above")

# ===== INPUT 4 (Edge): aromaticity models ==================================
print("\n===== INPUT 4: aromaticity models, the 'most common silent error' =====")
print(f"  Chem.AromaticityModel exists: {hasattr(Chem, 'AromaticityModel')}")
print(f"  AROMATICITY_RDKIT exists: "
      f"{hasattr(Chem.AromaticityModel, 'AROMATICITY_RDKIT') if hasattr(Chem,'AromaticityModel') else 'n/a'}")
print(f"  AROMATICITY_MDL exists:   "
      f"{hasattr(Chem.AromaticityModel, 'AROMATICITY_MDL') if hasattr(Chem,'AromaticityModel') else 'n/a'}")
CASES = [('furan', 'c1ccoc1'), ('thiophene', 'c1ccsc1'), ('pyrrole', 'c1cc[nH]c1'),
         ('benzene', 'c1ccccc1'), ('indole', 'c1ccc2[nH]ccc2c1'),
         ('cyclopentadienone', 'O=C1C=CC=C1')]
print(f"  {'molecule':20} {'RDKIT model':14} {'MDL model':14} {'differ?'}")
for lbl, smi in CASES:
    out = []
    for model in ['AROMATICITY_RDKIT', 'AROMATICITY_MDL']:
        m = Chem.MolFromSmiles(smi)
        if m is None:
            out.append('parse_fail')
            continue
        Chem.Kekulize(m, clearAromaticFlags=True)
        Chem.SetAromaticity(m, getattr(Chem.AromaticityModel, model))
        out.append(f"{sum(1 for a in m.GetAtoms() if a.GetIsAromatic())} arom atoms")
    print(f"  {lbl:20} {out[0]:14} {out[1]:14} {out[0] != out[1]}")

# ===== INPUT 5 (Stress): PDB ligand bond orders =============================
print("\n===== INPUT 5: extracting a ligand from a PDB entry =====")
PDB = r"F:\OpenScience\audit-envs\cheminformatics-hit-triage-analyst\smoke\dock\3ptb.pdb"
print(f"  3PTB present: {os.path.exists(PDB)}")
if os.path.exists(PDB):
    lines = [l for l in open(PDB) if l.startswith('HETATM') and l[17:20].strip() == 'BEN']
    open(os.path.join(D, 'ben.pdb'), 'w').write(''.join(lines) + 'END\n')
    lig = Chem.MolFromPDBFile(os.path.join(D, 'ben.pdb'), sanitize=False)
    print(f"  ligand parsed from PDB: atoms={lig.GetNumAtoms()}")
    bt = Counter(str(b.GetBondType()) for b in lig.GetBonds())
    print(f"  bond types straight from PDB: {dict(bt)}  "
          f"(SKILL.md: 'All bonds single; aromatic rings non-aromatic')")
    print(f"  aromatic atoms before template: "
          f"{sum(1 for a in lig.GetAtoms() if a.GetIsAromatic())}")
    template = Chem.MolFromSmiles('NC(=[NH2+])c1ccccc1')
    try:
        fixed = AllChem.AssignBondOrdersFromTemplate(template, lig)
        bt2 = Counter(str(b.GetBondType()) for b in fixed.GetBonds())
        print(f"  after AssignBondOrdersFromTemplate: {dict(bt2)}")
        print(f"  aromatic atoms after: "
              f"{sum(1 for a in fixed.GetAtoms() if a.GetIsAromatic())}  "
              f"SMILES={Chem.MolToSmiles(fixed)}")
    except Exception as e:                                   # noqa: BLE001
        print(f"  AssignBondOrdersFromTemplate RAISED {type(e).__name__}: {e}")
    try:
        neutral = Chem.MolFromSmiles('NC(=N)c1ccccc1')
        fixed2 = AllChem.AssignBondOrdersFromTemplate(neutral, lig)
        print(f"  with a NEUTRAL template: SMILES={Chem.MolToSmiles(fixed2)}")
    except Exception as e:                                   # noqa: BLE001
        print(f"  with a NEUTRAL template RAISED {type(e).__name__}: {str(e)[:90]}")
        print("     -> the template must match the protonation state; SKILL.md does not say so")

# ===== INPUT 6 (Scope boundary): InChI identity and /FixedH ================
print("\n===== INPUT 6: InChI identity, and the /FixedH tautomer caveat =====")
print(f"  rdkit INCHI available: {Chem.inchi.INCHI_AVAILABLE}")
PAIRS = [('2-pyridone / 2-hydroxypyridine', 'O=c1cccc[nH]1', 'Oc1ccccn1'),
         ('acetone keto / enol', 'CC(C)=O', 'CC(O)=C'),
         ('guanine N7H / N9H', 'Nc1nc2[nH]cnc2c(=O)[nH]1', 'Nc1nc2nc[nH]c2c(=O)[nH]1')]
for lbl, a, b in PAIRS:
    ma, mb = Chem.MolFromSmiles(a), Chem.MolFromSmiles(b)
    std_same = MolToInchi(ma) == MolToInchi(mb)
    fa, _ = Chem.MolToInchiAndAuxInfo(ma, options='/FixedH')
    fb, _ = Chem.MolToInchiAndAuxInfo(mb, options='/FixedH')
    print(f"  {lbl:32} std InChI same? {std_same:<5}  /FixedH same? {fa == fb}")
m = Chem.MolFromSmiles('c1ccc2c(c1)cccc2')
print(f"  MolToInchiKey vs InchiToInchiKey(MolToInchi) agree: "
      f"{MolToInchiKey(m) == InchiToInchiKey(MolToInchi(m))}")

# ===== INPUT 7 (Adversarial): broken inputs and the diagnostic path ========
print("\n===== INPUT 7: malformed input and the sanitize=False diagnostic =====")
BAD = [('unclosed ring', 'c1ccccc'), ('bad parens', 'CC(C'), ('nonsense', 'not_a_smiles'),
       ('pentavalent N', 'CN(C)(C)C'), ('valence-bad S', 'FS(F)(F)(F)(F)F'),
       ('aromatic non-ring', 'cccc'), ('empty', '')]
for lbl, smi in BAD:
    m = Chem.MolFromSmiles(smi)
    m2 = Chem.MolFromSmiles(smi, sanitize=False)
    detail = ''
    if m is None and m2 is not None:
        err = Chem.SanitizeMol(m2, catchErrors=True)
        detail = f"  -> sanitize error flag: {err}"
    print(f"  {lbl:18} MolFromSmiles={'None' if m is None else 'ok':5} "
          f"sanitize=False={'None' if m2 is None else 'ok':5}{detail}")
print("  -> the Common Errors fix ('try sanitize=False, inspect') recovers a")
print("     diagnosable object for the valence cases but not for grammar errors.")
