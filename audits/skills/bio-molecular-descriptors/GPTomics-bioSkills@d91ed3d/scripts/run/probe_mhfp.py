# Probe: does the SKILL.md MHFP6 snippet run, and where?
import sys
from rdkit import Chem, RDLogger
RDLogger.DisableLog('rdApp.*')
import numpy
from mhfp.encoder import MHFPEncoder
print("numpy", numpy.__version__)
mol = Chem.MolFromSmiles('CC(C)NCC(O)COc1ccc(CC(N)=O)cc1')
enc = MHFPEncoder(2048)
try:
    fp = enc.encode_mol(mol, radius=3)          # exactly the SKILL.md snippet
    print(f"  encode_mol OK -> len={len(fp)} first5={list(fp[:5])}")
    mol2 = Chem.MolFromSmiles('CC(C)NCC(O)COc1ccc(CC(N)=O)cc1C')
    fp2 = enc.encode_mol(mol2, radius=3)
    print(f"  MHFPEncoder.distance -> {MHFPEncoder.distance(fp, fp2):.4f}")
except Exception as e:
    print(f"  encode_mol FAILED: {type(e).__name__}: {e}")
