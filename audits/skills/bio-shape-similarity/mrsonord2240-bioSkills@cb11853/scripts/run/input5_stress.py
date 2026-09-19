"""
Input 5 (Stress / multi-part): "Screen this 15-compound library against my query: USRCAT
pre-filter to the top 8, Open3DAlign-rescore those, compute ECFP4 similarity for each, and
classify every rescored hit into the shape/ECFP4 quadrant table from SKILL.md (Shape vs ECFP4
Complementarity) using shape>=0.5 / ecfp>=0.4 as 'High'."

Exercises the full multi-stage pipeline the Skill describes end-to-end on a larger set.
"""
from rdkit import Chem
from rdkit.Chem import AllChem, rdMolDescriptors, rdMolAlign, rdShapeHelpers, rdFingerprintGenerator
from rdkit import DataStructs

SEED = 42
QUERY = 'CC(=O)Nc1ccc(C(=O)c2ccccc2)cc1'

LIBRARY = [
    'CC(=O)Nc1ccc(C(=O)c2ccc(F)cc2)cc1',
    'O=S(=O)(c1ccccc1)Nc2ccc(C(=O)c3ccccc3)cc2',
    'CCC',
    'CC(=O)Nc1ccccc1',
    'CC(C)Cc1ccc(cc1)C(C)C(=O)O',
    'CC(=O)Oc1ccccc1C(=O)O',
    'CC(=O)Nc1ccc(C(=O)c2ccc(Cl)cc2)cc1',
    'O=C(Nc1ccccc1)c1ccccc1',
    'c1ccc2c(c1)ccc3c2cccc3',
    'CC(=O)Nc1ccc(C(=O)c2ccccc2)cc1',
    'Clc1ccc(cc1)C(=O)Nc1ccc(Cl)cc1',
    'CC(=O)Nc1ccc(Oc2ccccc2)cc1',
    'O=C(c1ccccc1)c1ccc(N)cc1',
    'CCOC(=O)c1ccccc1N',
    'CC(=O)Nc1ccc(C(=O)c2ccc(C)cc2)cc1',
]


def embed(smi):
    mol = Chem.MolFromSmiles(smi)
    if mol is None:
        return None
    mol = Chem.AddHs(mol)
    params = AllChem.ETKDGv3()
    params.randomSeed = SEED
    if AllChem.EmbedMolecule(mol, params) != 0:
        return None
    AllChem.MMFFOptimizeMolecule(mol)
    return mol


def ecfp4(smi1, smi2):
    gen = rdFingerprintGenerator.GetMorganGenerator(radius=2, fpSize=2048)
    fp1 = gen.GetFingerprint(Chem.MolFromSmiles(smi1))
    fp2 = gen.GetFingerprint(Chem.MolFromSmiles(smi2))
    return DataStructs.TanimotoSimilarity(fp1, fp2)


query_mol = embed(QUERY)

# Stage 1: USRCAT pre-filter
usr_scores = []
for smi in LIBRARY:
    tm = embed(smi)
    if tm is None:
        print(f"SKIPPED (embed failed): {smi}")
        continue
    d1, d2 = rdMolDescriptors.GetUSRCAT(query_mol), rdMolDescriptors.GetUSRCAT(tm)
    usr_scores.append((smi, rdMolDescriptors.GetUSRScore(d1, d2), tm))

usr_scores.sort(key=lambda x: x[1], reverse=True)
top8 = usr_scores[:8]
print(f"Stage 1 (USRCAT pre-filter): {len(usr_scores)}/{len(LIBRARY)} embedded, top 8 kept")

# Stage 2: Open3DAlign rescore of top 8
print("\nStage 2 (Open3DAlign rescore) + Stage 3 (ECFP4) + Stage 4 (quadrant classification)")
print(f"{'SMILES':55s} {'shape':>6s} {'ecfp4':>6s}  quadrant")
for smi, usr, tm in top8:
    O3A = rdMolAlign.GetO3A(tm, query_mol)
    O3A.Align()
    shape = 1.0 - rdShapeHelpers.ShapeTanimotoDist(tm, query_mol)
    ecfp = ecfp4(QUERY, smi)
    shape_high = shape >= 0.5
    ecfp_high = ecfp >= 0.4
    if shape_high and ecfp_high:
        quadrant = "close analog"
    elif shape_high and not ecfp_high:
        quadrant = "SCAFFOLD-HOP candidate"
    elif not shape_high and ecfp_high:
        quadrant = "different sampled shape"
    else:
        quadrant = "unrelated"
    print(f"{smi:55s} {shape:6.3f} {ecfp:6.3f}  {quadrant}")

print("\nStage complete: full USRCAT -> Open3DAlign -> ECFP4 -> quadrant pipeline ran end to end.")
