"""Executable re-audit against source commit 87bcd4677e0402e821a95f06f06d8400733606ae."""
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

import numpy as np
import pandas as pd
from rdkit import Chem, DataStructs
from rdkit.Chem import rdFMCS, rdFingerprintGenerator
from rdkit.ML.Cluster import Butina


COMMIT = "87bcd4677e0402e821a95f06f06d8400733606ae"
ROOT = Path(r"F:\OpenScience\worktrees\bio-similarity-searching-fixpass")
SKILL = ROOT / "chemoinformatics" / "similarity-searching"
DATA = Path(r"F:\OpenScience\audit-envs\cheminformatics-hit-triage-analyst\public-data\chembl_herg_CHEMBL240_ic50.csv")


def load_example():
    source = SKILL / "examples" / "similarity_search.py"
    spec = spec_from_file_location("similarity_search", source)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def hERG_mols(n=500):
    df = pd.read_csv(DATA).dropna(subset=["canonical_smiles", "pchembl_value"])
    df = df.drop_duplicates("canonical_smiles").iloc[:n].copy()
    df["mol"] = df.canonical_smiles.map(Chem.MolFromSmiles)
    return df[df.mol.notna()].reset_index(drop=True)


def main():
    example = load_example()
    text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    df = hERG_mols()
    mols = list(df.mol)
    achiral = rdFingerprintGenerator.GetMorganGenerator(radius=2, fpSize=2048)
    chiral = rdFingerprintGenerator.GetMorganGenerator(
        radius=2, fpSize=2048, includeChirality=True)
    fps = [achiral.GetFingerprint(mol) for mol in mols]
    print(f"source_commit={COMMIT}")
    print(f"data={len(mols)} ChEMBL hERG molecules")

    # Regression 1: analog search is still ranked and query-first.
    hits = example.find_similar(df.canonical_smiles.iloc[0], list(df.canonical_smiles), 0.4)
    print(f"input1_search_hits={len(hits)} top={hits[0][1]:.3f}")
    assert hits and hits[0][1] == 1.0

    # Regression 2: the documented Butina centroid relationship still holds.
    subset = fps[:200]
    distances = []
    for i in range(1, len(subset)):
        distances.extend(1 - score for score in DataStructs.BulkTanimotoSimilarity(subset[i], subset[:i]))
    clusters = Butina.ClusterData(distances, len(subset), 0.4, isDistData=True)
    centroid_violations = sum(
        DataStructs.TanimotoSimilarity(subset[cluster[0]], subset[index]) < 0.6 - 1e-9
        for cluster in clusters for index in cluster[1:]
    )
    print(f"input2_clusters={len(clusters)} centroid_violations={centroid_violations}")
    assert centroid_violations == 0

    # Regression 3: Tversky remains asymmetric; new guard confirms containment.
    query = Chem.MolFromSmiles("Nc1[nH]c2ccccc2n1")
    query_fp = achiral.GetFingerprint(query)
    scores_q_to_lib = [DataStructs.TverskySimilarity(query_fp, fp, 1.0, 0.0) for fp in fps]
    scores_lib_to_q = [DataStructs.TverskySimilarity(fp, query_fp, 1.0, 0.0) for fp in fps]
    delta = float(np.mean(np.abs(np.array(scores_q_to_lib) - np.array(scores_lib_to_q))))
    candidate_smiles = [df.canonical_smiles.iloc[i] for i in np.argsort(scores_q_to_lib)[-20:]]
    confirmed = example.confirm_substructure_hits("Nc1[nH]c2ccccc2n1", candidate_smiles)
    print(f"input3_tversky_asymmetry={delta:.3f} candidates=20 smart_confirmed={len(confirmed)}")
    assert delta > 0 and all(Chem.MolFromSmiles(s).HasSubstructMatch(query) for s in confirmed)

    # Regression 4: default chiral cliffs prevent achiral stereoisomer conflation.
    left = Chem.MolFromSmiles("N[C@@H](C)C(=O)O")
    right = Chem.MolFromSmiles("N[C@H](C)C(=O)O")
    achiral_score = DataStructs.TanimotoSimilarity(achiral.GetFingerprint(left), achiral.GetFingerprint(right))
    chiral_score = DataStructs.TanimotoSimilarity(chiral.GetFingerprint(left), chiral.GetFingerprint(right))
    print(f"input4_stereo_achiral={achiral_score:.3f} chiral={chiral_score:.3f}")
    assert achiral_score == 1.0 and chiral_score < 1.0
    assert "strip salts" in text and "includeChirality=True" in text

    # Regression 5: a small MCS with canceled=False is distinguished from timeout.
    divergent = [Chem.MolFromSmiles(s) for s in ["CCO", "c1ccccc1", "CC(=O)O", "C1CCCCC1", "CCN"]]
    result = rdFMCS.FindMCS(divergent, timeout=5)
    print(f"input5_mcs_atoms={result.numAtoms} canceled={result.canceled}")
    assert result.canceled is False and result.numAtoms <= 2
    assert "result.canceled=False" in text

    # Regression 6: percentile calibration retains its requested fraction.
    sampled_scores = []
    for i in range(len(fps)):
        sampled_scores.extend(DataStructs.BulkTanimotoSimilarity(fps[i], fps[:i]))
    threshold = float(np.quantile(sampled_scores, 0.995))
    retained = float(np.mean(np.array(sampled_scores) >= threshold))
    print(f"input6_p995={threshold:.3f} retained={retained:.4f}")
    assert 0.004 <= retained <= 0.007 and "99.5th percentile" in text

    # Regression 7: documented invalid-SMILES behavior remains explicit.
    try:
        example.find_similar("not a SMILES", ["CCO"])
    except ValueError as exc:
        print(f"input7_invalid_smiles={exc}")
    else:
        raise AssertionError("invalid query did not raise ValueError")

    # New input 8: exact identity is explicitly separated from fingerprint similarity.
    key_left = Chem.MolToInchiKey(left)
    key_right = Chem.MolToInchiKey(right)
    print(f"input8_inchikey_equal={key_left == key_right}")
    assert key_left != key_right and "For exact identity" in text

    # New input 9: each original audit correction is present in the exact source.
    required = [
        "SMARTS confirmation",
        "result.canceled=True",
        "includeChirality=True",
        "retained-pair percentile",
    ]
    missing = [phrase for phrase in required if phrase not in text]
    print(f"input9_required_guidance_missing={missing}")
    assert not missing


if __name__ == "__main__":
    main()
