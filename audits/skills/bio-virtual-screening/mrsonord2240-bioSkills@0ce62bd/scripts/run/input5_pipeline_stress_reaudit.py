#!/usr/bin/env python3
"""
RE-AUDIT Input 5 (Stress, regression): filter -> dock -> (GNINA not executed)
-> PoseBusters, reusing input2's fixed-code docked results. Also checks
whether the fixed SKILL.md's "Handoff caveat" documentation of the PDBQT->SDF
bond-order loss (added in this fix round) matches what actually happens.
"""
import subprocess
from pathlib import Path
import pandas as pd
from rdkit import Chem
from rdkit.Chem import Descriptors, Lipinski

HERE = Path(__file__).parent
OUT = HERE.parent / "out_input5"
OUT.mkdir(exist_ok=True)
IN2 = HERE.parent / "out_input2"
ENV = Path("F:/OpenScience/audit-envs/cheminformatics-hit-triage-analyst")
OBABEL = ENV / "Scripts/obabel.exe"
BUST = ENV / "Scripts/bust.exe"

LIBRARY = {
    "benzamidine": "NC(=[NH2+])c1ccccc1",
    "4-aminobenzamidine": "NC(=[NH2+])c1ccc(N)cc1",
    "toluene": "Cc1ccccc1",
    "phenol": "Oc1ccccc1",
    "imidazole": "c1c[nH]cn1",
    "way_too_big_decoy": "CCCCCCCCCCCCCCCCCCCC(=O)NCCCCCCCCCCCCCCCCCCCCNC(=O)CCCCCCCCCCCCCCCCCCCC",
}


def drug_like_filter(df):
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
    df_stage1 = drug_like_filter(df)
    print(f"Passed drug-likeness filter: {list(df_stage1['name'])} ({len(df_stage1)}/{len(df)})")
    assert "way_too_big_decoy" not in set(df_stage1['name'])
    assert len(df_stage1) == 5

    results_csv = IN2 / "results.csv"
    assert results_csv.exists(), "run input2_virtual_screen_reaudit.py first"
    docked = pd.read_csv(results_csv)
    docked = docked[docked['name'].isin(df_stage1['name'])]
    print(docked.to_string(index=False))

    print("\nGNINA rescoring: NOT EXECUTED (no Windows binary / no CUDA torch, unchanged since original audit)")

    top = docked.sort_values('affinity_kcal_mol').iloc[0]
    poses_pdbqt = IN2 / f"{top['name']}_poses.pdbqt"
    poses_sdf = OUT / f"{top['name']}_pose1.sdf"
    subprocess.run([str(OBABEL), str(poses_pdbqt), "-O", str(poses_sdf), "-f", "1", "-l", "1"],
                    check=True, capture_output=True, text=True)
    assert poses_sdf.exists() and poses_sdf.stat().st_size > 0

    result = subprocess.run([str(BUST), str(poses_sdf), "--outfmt", "short"],
                             capture_output=True, text=True)
    print("PoseBusters (ligand-only, no receptor context):")
    print(result.stdout)
    print(result.stderr[-2000:] if result.returncode != 0 else "")
    # Documented "Handoff caveat" in the fixed SKILL.md: PDBQT->SDF for a
    # charged ligand loses formal bond order/charge -> RDKit sanitization
    # failure. Confirm that's still what happens (accuracy check on the fix's
    # new documentation, not a re-litigation of the original P2 finding).
