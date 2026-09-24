# bio-similarity-searching -- Input 7b: the MHFP6 LSH-forest route, exactly as SKILL.md writes it.
import time, sys
import numpy as np, pandas as pd
from rdkit import Chem, DataStructs, RDLogger
from rdkit.Chem import rdFingerprintGenerator
RDLogger.DisableLog('rdApp.*')
import numpy; print("numpy", numpy.__version__)
from mhfp.encoder import MHFPEncoder
try:
    from mhfp.lsh_forest import LSHForestHelper
    print("LSHForestHelper import: OK")
except Exception as e:
    print(f"LSHForestHelper import FAILED: {type(e).__name__}: {e}"); sys.exit(0)

SRC = r"F:\OpenScience\audit-envs\cheminformatics-hit-triage-analyst\public-data\chembl_herg_CHEMBL240_ic50.csv"
df = pd.read_csv(SRC).dropna(subset=['canonical_smiles']).drop_duplicates('canonical_smiles').head(1000)
smiles = list(df.canonical_smiles)
encoder = MHFPEncoder(2048)

def build_index(smiles_list):
    forest = LSHForestHelper()
    fingerprints = []
    for i, smi in enumerate(smiles_list):
        fp = encoder.encode(smi, radius=3)
        fingerprints.append(fp)
        forest.add(i, fp)
    forest.index()
    return forest, fingerprints

t0 = time.time()
try:
    forest, fingerprints = build_index(smiles)
    print(f"  built LSH forest over {len(smiles)} compounds in {time.time()-t0:.1f}s")
except Exception as e:
    print(f"  build_index FAILED: {type(e).__name__}: {e}"); sys.exit(0)

qmol = Chem.MolFromSmiles(smiles[0])
def query_index(forest, qmol, fingerprints, k=10):
    qfp = encoder.encode_mol(qmol, radius=3)
    return forest.query(qfp, k=k, data=fingerprints)
try:
    res = query_index(forest, qmol, fingerprints, k=10)
    print(f"  query returned {len(res)} neighbours: {list(res)[:10]}")
except Exception as e:
    print(f"  query_index FAILED: {type(e).__name__}: {e}")
    import inspect
    print("  LSHForestHelper.query signature:", inspect.signature(LSHForestHelper.query))
    res = None

# recall against an exact MHFP search, as the Skill instructs
qfp = encoder.encode_mol(qmol, radius=3)
exact = np.argsort([MHFPEncoder.distance(qfp, f) for f in fingerprints])[:10]
print(f"  exact MHFP top-10 indices: {list(exact)}")
if res is not None:
    print(f"  LSH recall@10 vs exact: {len(set(map(int,res)) & set(map(int,exact)))}/10")
gen = rdFingerprintGenerator.GetMorganGenerator(radius=2, fpSize=2048)
efps = [gen.GetFingerprint(Chem.MolFromSmiles(s)) for s in smiles]
ecfp_top = np.argsort(DataStructs.BulkTanimotoSimilarity(efps[0], efps))[::-1][:10]
print(f"  ECFP4 Tanimoto top-10 indices: {list(ecfp_top)}")
print(f"  overlap between exact-MHFP top-10 and ECFP4 top-10: "
      f"{len(set(map(int,exact)) & set(map(int,ecfp_top)))}/10 "
      f"-- the Skill's 'different distance semantics' point")
