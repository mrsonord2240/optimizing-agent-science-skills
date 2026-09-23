"""
Input 1 (Canonical): "Compute USRCAT descriptors for query.sdf and library.sdf.
Rank library by similarity; return top hits. Then take the top USRCAT hits and
rescore with Open3DAlign for accurate shape alignment."

Follows the SKILL.md USRCAT + Open3DAlign patterns verbatim (rdMolDescriptors.GetUSRCAT /
GetUSRScore, then GetO3A / Align / ShapeTanimotoDist), applied to a small synthetic query +
library (10 SMILES) written for this audit.

Run twice to check determinism (Skill Veto T3): ETKDGv3 is seeded (randomSeed=42 in the
Skill's own prepare_mol_3d pattern), so results must be bit-identical across runs.
"""
from rdkit import Chem
from rdkit.Chem import AllChem, rdMolDescriptors, rdMolAlign, rdShapeHelpers

QUERY_SMI = 'CC(=O)Nc1ccc(C(=O)c2ccccc2)cc1'  # acetaminophen-like benzophenone amide

LIBRARY = [
    ('lib_01', 'CC(=O)Nc1ccc(C(=O)c2ccc(F)cc2)cc1'),   # close analog
    ('lib_02', 'O=S(=O)(c1ccccc1)Nc2ccc(C(=O)c3ccccc3)cc2'),  # scaffold-hop candidate
    ('lib_03', 'CCC'),                                  # tiny unrelated
    ('lib_04', 'CC(=O)Nc1ccccc1'),                       # smaller analog (no biphenyl)
    ('lib_05', 'CC(C)Cc1ccc(cc1)C(C)C(=O)O'),            # ibuprofen (unrelated)
    ('lib_06', 'CC(=O)Oc1ccccc1C(=O)O'),                 # aspirin (unrelated)
    ('lib_07', 'CC(=O)Nc1ccc(C(=O)c2ccc(Cl)cc2)cc1'),    # close analog, Cl
    ('lib_08', 'O=C(Nc1ccccc1)c1ccccc1'),                # benzanilide (partial match)
    ('lib_09', 'c1ccc2c(c1)ccc3c2cccc3'),                 # anthracene (unrelated PAH)
    ('lib_10', 'CC(=O)Nc1ccc(C(=O)c2ccccc2)cc1'),        # identical to query
]

SEED = 42


def embed(smi, n_conf=1):
    mol = Chem.MolFromSmiles(smi)
    if mol is None:
        return None
    mol = Chem.AddHs(mol)
    params = AllChem.ETKDGv3()
    params.randomSeed = SEED
    ids = list(AllChem.EmbedMultipleConfs(mol, numConfs=n_conf, params=params))
    if not ids:
        return None
    AllChem.MMFFOptimizeMoleculeConfs(mol)
    return mol


def usrcat_score(query_mol, target_mol):
    d1 = rdMolDescriptors.GetUSRCAT(query_mol)
    d2 = rdMolDescriptors.GetUSRCAT(target_mol)
    return rdMolDescriptors.GetUSRScore(d1, d2)


def run():
    query_mol = embed(QUERY_SMI)
    assert query_mol is not None, "query embedding failed"

    usr_hits = []
    for name, smi in LIBRARY:
        target_mol = embed(smi)
        if target_mol is None:
            print(f"{name}: SMILES parse/embed FAILED ({smi})")
            continue
        score = usrcat_score(query_mol, target_mol)
        usr_hits.append((name, smi, score, target_mol))

    usr_hits.sort(key=lambda x: x[2], reverse=True)

    print("=== USRCAT ranking (all library members) ===")
    for name, smi, score, _ in usr_hits:
        print(f"{name:8s} USRCAT={score:.4f}  {smi}")

    # Take top 5 USRCAT hits, rescore with Open3DAlign per the Skill's pattern.
    top5 = usr_hits[:5]
    print("\n=== Open3DAlign rescore of top-5 USRCAT hits ===")
    o3a_results = []
    for name, smi, usr_score, target_mol in top5:
        O3A = rdMolAlign.GetO3A(target_mol, query_mol)
        rmsd = O3A.Align()
        o3a_score = O3A.Score()
        shape_tanimoto = 1.0 - rdShapeHelpers.ShapeTanimotoDist(target_mol, query_mol)
        o3a_results.append((name, usr_score, o3a_score, shape_tanimoto, rmsd))
        print(f"{name:8s} USRCAT={usr_score:.4f}  O3A_score={o3a_score:.4f}  "
              f"shape_tanimoto={shape_tanimoto:.4f}  rmsd={rmsd:.4f}")

    # Sanity assertion: shape Tanimoto must be in [0,1] per the Skill's "Common Errors" table.
    for name, _, _, st, _ in o3a_results:
        assert 0.0 <= st <= 1.0, f"shape Tanimoto out of range for {name}: {st}"
    print("\nAssertion PASSED: all shape_tanimoto values in [0,1] (per SKILL.md Common Errors table)")
    return o3a_results


if __name__ == '__main__':
    print("### RUN 1 ###")
    r1 = run()
    print("\n### RUN 2 (determinism check, same seed) ###")
    r2 = run()
    ident = all(a[:2] == b[:2] and abs(a[2] - b[2]) < 1e-9 and abs(a[3] - b[3]) < 1e-9
                for a, b in zip(r1, r2))
    print(f"\nDeterminism check (run1 vs run2 identical): {ident}")
