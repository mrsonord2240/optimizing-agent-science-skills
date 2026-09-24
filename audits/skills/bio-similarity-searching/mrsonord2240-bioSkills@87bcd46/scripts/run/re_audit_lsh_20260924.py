"""Focused exact-commit execution of the documented MHFP6 LSH route."""
from pathlib import Path

import numpy as np
import pandas as pd
from rdkit import Chem
from mhfp.encoder import MHFPEncoder
from mhfp.lsh_forest import LSHForestHelper


source = Path(r"F:\OpenScience\worktrees\bio-similarity-searching-fixpass\chemoinformatics\similarity-searching\SKILL.md").read_text(encoding="utf-8")
assert "LSHForestHelper" in source
data = pd.read_csv(r"F:\OpenScience\audit-envs\cheminformatics-hit-triage-analyst\public-data\chembl_herg_CHEMBL240_ic50.csv")
smiles = list(data.dropna(subset=["canonical_smiles"]).drop_duplicates("canonical_smiles").canonical_smiles.head(100))
encoder = MHFPEncoder(2048)
forest = LSHForestHelper()
fingerprints = []
for index, smiles_value in enumerate(smiles):
    fingerprint = encoder.encode(smiles_value, radius=3)
    fingerprints.append(fingerprint)
    forest.add(index, fingerprint)
forest.index()
query = encoder.encode_mol(Chem.MolFromSmiles(smiles[0]), radius=3)
approximate = list(forest.query(query, k=10, data=fingerprints))
exact = list(np.argsort([MHFPEncoder.distance(query, fp) for fp in fingerprints])[:10])
recall = len(set(map(int, approximate)) & set(map(int, exact)))
print(f"lsh_n={len(smiles)} returned={len(approximate)} recall_at_10={recall}/10")
assert len(approximate) == 10 and recall >= 8
