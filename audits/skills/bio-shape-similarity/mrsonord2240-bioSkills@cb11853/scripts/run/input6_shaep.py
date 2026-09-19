"""
Input 6 (Scope boundary): "I don't have RDKit/Open3DAlign results yet -- just run ShaEP
directly on my query and target mol2 files for an ESP-aware shape comparison, the way the
Skill documents."

Tests the Skill's exact documented CLI invocation:
    shaep -q query.mol2 target.mol2 -s aligned_hits.sdf similarity.txt
against the real ShaEP 1.4.2 binary installed in the audit env (TOOLS.md: "the exact version
the Skill names"). Also checks the ESP claim (electrostatic + shape) is real, not just
concept-level.
"""
import subprocess
import sys
from pathlib import Path
from rdkit import Chem
from rdkit.Chem import AllChem

SEED = 42
RUN_DIR = Path(__file__).parent
SHAEP_EXE = r"F:\OpenScience\audit-envs\cheminformatics-hit-triage-analyst\tools\shaep\shaep.exe"


def make_mol2(smi, path):
    mol = Chem.MolFromSmiles(smi)
    mol = Chem.AddHs(mol)
    params = AllChem.ETKDGv3()
    params.randomSeed = SEED
    AllChem.EmbedMolecule(mol, params)
    AllChem.MMFFOptimizeMolecule(mol)
    AllChem.ComputeGasteigerCharges(mol)  # ShaEP needs partial charges for ESP
    Chem.MolToMolFile(str(mol), str(path)) if False else None
    # RDKit has no native Mol2 writer; use MolToPDBFile + obabel, or write minimal Mol2 by hand.
    return mol


def write_mol2_via_obabel(smi, out_path):
    """RDKit alone cannot write Mol2; route through obabel (also referenced across this
    candidate's other Skills / TOOLS.md) since SKILL.md's ShaEP example assumes .mol2 input
    without saying how to produce it from SMILES."""
    obabel = r"F:\OpenScience\audit-envs\cheminformatics-hit-triage-analyst\Scripts\obabel.exe"
    proc = subprocess.run(
        [obabel, f"-:{smi}", "-O", str(out_path), "--gen3D"],
        capture_output=True, text=True,
    )
    return proc


query_mol2 = RUN_DIR / "query.mol2"
target_mol2 = RUN_DIR / "target.mol2"

r1 = write_mol2_via_obabel('CC(=O)Nc1ccc(C(=O)c2ccccc2)cc1', query_mol2)
r2 = write_mol2_via_obabel('CC(=O)Nc1ccc(C(=O)c2ccc(F)cc2)cc1', target_mol2)
print("obabel query stderr:", r1.stderr.strip()[:200])
print("obabel target stderr:", r2.stderr.strip()[:200])
print("query.mol2 exists:", query_mol2.exists(), "size:", query_mol2.stat().st_size if query_mol2.exists() else 0)
print("target.mol2 exists:", target_mol2.exists(), "size:", target_mol2.stat().st_size if target_mol2.exists() else 0)

# Exact SKILL.md-documented invocation:
#   shaep -q query.mol2 target.mol2 -s aligned_hits.sdf similarity.txt
aligned_sdf = RUN_DIR / "aligned_hits.sdf"
similarity_txt = RUN_DIR / "similarity.txt"
cmd = [SHAEP_EXE, "-q", str(query_mol2), str(target_mol2), "-s", str(aligned_sdf), str(similarity_txt)]
print("\nRunning:", " ".join(cmd))
proc = subprocess.run(cmd, capture_output=True, text=True)
print("returncode:", proc.returncode)
print("stdout:\n", proc.stdout[:2000])
print("stderr:\n", proc.stderr[:2000])

if similarity_txt.exists():
    print("\nsimilarity.txt contents:")
    print(similarity_txt.read_text()[:2000])
else:
    print("\nsimilarity.txt NOT produced.")
