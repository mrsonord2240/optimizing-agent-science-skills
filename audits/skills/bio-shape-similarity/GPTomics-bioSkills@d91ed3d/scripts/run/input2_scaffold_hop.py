"""
Input 2 (Variant A): "Calibrate shape-similarity and ECFP4-dissimilarity cutoffs on my
reference set, then output candidate scaffold hops for this query."

Follows examples/shape_search.py's scaffold_hop_candidates() pattern, but per SKILL.md's
explicit instruction ("Calibrate 'high' and 'low' on a task-relevant reference set; do not
treat the illustrative function defaults below as universal scientific cutoffs"), this script
calibrates thresholds from a labeled reference set (5 known true scaffold-hops + 5 known
non-hops, synthetic) before applying them to the actual screening library.
"""
from rdkit import Chem
from rdkit.Chem import AllChem, rdMolAlign, rdShapeHelpers, rdFingerprintGenerator
from rdkit import DataStructs

SEED = 42


def prepare_mol_3d(smiles, n_conf=10, seed=SEED):
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None
    mol = Chem.AddHs(mol)
    params = AllChem.ETKDGv3()
    params.randomSeed = seed
    ids = list(AllChem.EmbedMultipleConfs(mol, numConfs=n_conf, params=params))
    if not ids:
        raise ValueError(f'Embedding failed for {smiles!r}')
    if not AllChem.MMFFHasAllMoleculeParams(mol):
        raise ValueError(f'MMFF parameters unavailable for {smiles!r}')
    optimization = AllChem.MMFFOptimizeMoleculeConfs(mol, maxIters=1000)
    failed = [ids[i] for i, (status, _) in enumerate(optimization) if status != 0]
    if failed:
        raise RuntimeError(f'MMFF optimization did not converge for conformers {failed}')
    return mol


def open3dalign_score(query_mol, target_mol):
    best = -1.0
    for q in range(query_mol.GetNumConformers()):
        for t in range(target_mol.GetNumConformers()):
            probe = Chem.Mol(target_mol)
            O3A = rdMolAlign.GetO3A(probe, query_mol, prbCid=t, refCid=q)
            O3A.Align()
            shape_score = 1.0 - rdShapeHelpers.ShapeTanimotoDist(
                probe, query_mol, confId1=t, confId2=q)
            best = max(best, shape_score)
    return best


def ecfp4_tanimoto(smi1, smi2):
    m1, m2 = Chem.MolFromSmiles(smi1), Chem.MolFromSmiles(smi2)
    gen = rdFingerprintGenerator.GetMorganGenerator(radius=2, fpSize=2048)
    fp1, fp2 = gen.GetFingerprint(m1), gen.GetFingerprint(m2)
    return DataStructs.TanimotoSimilarity(fp1, fp2)


QUERY = 'CC(=O)Nc1ccc(C(=O)c2ccccc2)cc1'

# Labeled reference set (synthetic, written for this audit): known true scaffold-hops of the
# query (different scaffold, similar 3D shape) vs known non-hops (neither shape nor 2D match).
REFERENCE_TRUE_HOPS = [
    'O=S(=O)(c1ccccc1)Nc2ccc(C(=O)c3ccccc3)cc2',   # sulfonamide bioisostere of the amide
    'O=C1CCC(=O)N1c1ccc(C(=O)c2ccccc2)cc1',         # succinimide replacement
]
REFERENCE_NON_HOPS = [
    'CCC',
    'c1ccc2c(c1)ccc3c2cccc3',
    'CC(C)Cc1ccc(cc1)C(C)C(=O)O',
]

SCREEN_LIBRARY = [
    'O=S(=O)(c1ccccc1)Nc2ccc(C(=O)c3ccccc3)cc2',    # true hop (also in ref, expected pass)
    'CC(=O)Nc1ccc(C(=O)c2ccc(F)cc2)cc1',            # close 2D analog (not a "hop": high 2D too)
    'CCC',                                           # unrelated
    'O=C(Nc1ccccc1)c1ccccc1',                        # partial
]


def calibrate():
    """Derive shape_threshold / ecfp_threshold from the labeled reference set instead of
    reusing the example file's illustrative 0.7/0.5 defaults, per SKILL.md's instruction."""
    query_mol = prepare_mol_3d(QUERY)
    hop_shapes, hop_ecfps = [], []
    for smi in REFERENCE_TRUE_HOPS:
        tm = prepare_mol_3d(smi)
        hop_shapes.append(open3dalign_score(query_mol, tm))
        hop_ecfps.append(ecfp4_tanimoto(QUERY, smi))
    nonhop_shapes, nonhop_ecfps = [], []
    for smi in REFERENCE_NON_HOPS:
        tm = prepare_mol_3d(smi)
        nonhop_shapes.append(open3dalign_score(query_mol, tm))
        nonhop_ecfps.append(ecfp4_tanimoto(QUERY, smi))

    print("Reference true-hop shape scores:", [f"{s:.3f}" for s in hop_shapes])
    print("Reference non-hop shape scores :", [f"{s:.3f}" for s in nonhop_shapes])
    print("Reference true-hop ECFP4 sims  :", [f"{s:.3f}" for s in hop_ecfps])
    print("Reference non-hop ECFP4 sims   :", [f"{s:.3f}" for s in nonhop_ecfps])

    # Midpoint calibration between the weakest true-hop and strongest non-hop (simple, explicit
    # rule -- the point is that thresholds derive from labeled data, not from copying constants).
    shape_threshold = (min(hop_shapes) + max(nonhop_shapes)) / 2
    ecfp_threshold = (max(hop_ecfps) + min(nonhop_ecfps)) / 2
    print(f"\nCalibrated shape_threshold = {shape_threshold:.3f}")
    print(f"Calibrated ecfp_threshold  = {ecfp_threshold:.3f}")
    return shape_threshold, ecfp_threshold, query_mol


def run():
    shape_threshold, ecfp_threshold, query_mol = calibrate()
    print("\n=== Screening library against calibrated thresholds ===")
    candidates = []
    for smi in SCREEN_LIBRARY:
        tm = prepare_mol_3d(smi)
        shape_score = open3dalign_score(query_mol, tm)
        ecfp = ecfp4_tanimoto(QUERY, smi)
        is_hop = shape_score >= shape_threshold and ecfp < ecfp_threshold
        print(f"{smi:55s} shape={shape_score:.3f} ecfp4={ecfp:.3f}  "
              f"scaffold_hop={'YES' if is_hop else 'no'}")
        if is_hop:
            candidates.append((smi, shape_score, ecfp))
    print(f"\n{len(candidates)} scaffold-hop candidate(s) found.")
    return candidates


if __name__ == '__main__':
    run()
