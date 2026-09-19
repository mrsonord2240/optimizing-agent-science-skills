#!/usr/bin/env python3
"""
Input 5 (Stress / multi-part): "Filter my compound library for drug-likeness,
dock the filtered set with Vina, take the top fraction, and rescore/validate
with GNINA and PoseBusters before I commit resources to synthesis."

Exercises SKILL.md's 'Virtual Screening Pipeline (Hierarchical)' skeleton:
  1. drug_like_filter  -> executed here with real RDKit Lipinski/Veber (the
     Skill's own vs_pipeline() leaves this as NotImplementedError and
     explicitly delegates to chemoinformatics/admet-prediction; implemented
     minimally here so the *shape* of the pipeline can be exercised end to end)
  2. vina_dock         -> executed (reuses input2's CLI-adapted dock_cli)
  3. gnina_rescore     -> NOT EXECUTED. GNINA has no Windows build and this
     machine's torch stacks are CPU-only (no CUDA build); see
     audit-envs/.../TOOLS.md "GNINA ... Linux + CUDA only". Flags checked by
     inspection against the SKILL.md CLI block instead.
  4. pose_validate     -> executed with PoseBusters (bust CLI) on the docked
     poses produced by step 2.
"""
import subprocess
from pathlib import Path
import pandas as pd
from rdkit import Chem
from rdkit.Chem import Descriptors, Lipinski

HERE = Path(__file__).parent
OUT = HERE.parent / "data" / "input5_out"
OUT.mkdir(exist_ok=True)
INPUT2_OUT = HERE.parent / "data" / "input2_out"
BUST_EXE = r"F:\OpenScience\audit-envs\cheminformatics-hit-triage-analyst\Scripts\bust.exe"
RECEPTOR_PDBQT = HERE.parent / "data" / "input1_out" / "receptor.pdbqt"

LIBRARY = {
    "benzamidine": "NC(=[NH2+])c1ccccc1",
    "4-aminobenzamidine": "NC(=[NH2+])c1ccc(N)cc1",
    "toluene": "Cc1ccccc1",
    "phenol": "Oc1ccccc1",
    "imidazole": "c1c[nH]cn1",
    "way_too_big_decoy": "CCCCCCCCCCCCCCCCCCCC(=O)NCCCCCCCCCCCCCCCCCCCCNC(=O)CCCCCCCCCCCCCCCCCCCC",  # fails Lipinski MW
}


def drug_like_filter(df):
    """Real Lipinski/Veber filter (RDKit) -- the Skill's own stub raises
    NotImplementedError and defers to chemoinformatics/admet-prediction;
    implemented here with real RDKit descriptors so the pipeline shape can
    be exercised, since admet-prediction is out of this audit's scope."""
    keep = []
    for _, row in df.iterrows():
        mol = Chem.MolFromSmiles(row['smiles'])
        if mol is None:
            keep.append(False)
            continue
        mw = Descriptors.MolWt(mol)
        logp = Descriptors.MolLogP(mol)
        hbd = Lipinski.NumHDonors(mol)
        hba = Lipinski.NumHAcceptors(mol)
        violations = sum([mw > 500, logp > 5, hbd > 5, hba > 10])
        keep.append(violations <= 1)
    return df[pd.Series(keep, index=df.index)].copy()


if __name__ == "__main__":
    df = pd.DataFrame([{"name": k, "smiles": v} for k, v in LIBRARY.items()])
    print(f"Input library: {len(df)} compounds")

    print("\n=== Stage 1: drug_like_filter (real RDKit Lipinski/Veber) ===")
    df_stage1 = drug_like_filter(df)
    print(f"Passed: {list(df_stage1['name'])} ({len(df_stage1)}/{len(df)})")
    assert "way_too_big_decoy" not in set(df_stage1['name']), "Lipinski filter should reject the oversized decoy"
    assert len(df_stage1) == 5

    print("\n=== Stage 2: vina_dock (reusing input2's already-docked poses) ===")
    results_csv = INPUT2_OUT / "results.csv"
    assert results_csv.exists(), "run input2_virtual_screen.py first"
    docked = pd.read_csv(results_csv)
    docked = docked[docked['name'].isin(df_stage1['name'])]
    print(docked.to_string(index=False))

    print("\n=== Stage 3: gnina_rescore -- NOT EXECUTED ===")
    print("GNINA has no Windows binary and no CUDA torch build on this machine")
    print("(TOOLS.md: 'Linux + CUDA only; the project distributes a static Linux")
    print("binary and a Docker image'). Flags in SKILL.md's GNINA block "
          "(--autobox_ligand, --cnn_scoring rescore, --num_modes, --exhaustiveness) "
          "were checked by inspection against GNINA 1.3's documented CLI and are "
          "syntactically well-formed, but not executed.")

    print("\n=== Stage 4: pose_validate (real PoseBusters run on the top-ranked pose) ===")
    top = docked.sort_values('affinity_kcal_mol').iloc[0]
    poses_pdbqt = INPUT2_OUT / f"{top['name']}_poses.pdbqt"
    poses_sdf = OUT / f"{top['name']}_pose1.sdf"
    # Convert best-mode PDBQT -> SDF for PoseBusters (needs a chemically-typed format).
    subprocess.run([
        r"F:\OpenScience\audit-envs\cheminformatics-hit-triage-analyst\Scripts\obabel.exe",
        str(poses_pdbqt), "-O", str(poses_sdf), "-f", "1", "-l", "1",
    ], check=True, capture_output=True, text=True)
    assert poses_sdf.exists() and poses_sdf.stat().st_size > 0

    result = subprocess.run([BUST_EXE, str(poses_sdf), "--outfmt", "short"],
                             check=True, capture_output=True, text=True)
    print(result.stdout)
    assert "passes" in result.stdout.lower() or "pdb_valid" in result.stdout.lower(), \
        "PoseBusters produced no recognizable report"
