#!/usr/bin/env python3
"""
Input 2 (Variant A): "Screen my small library of 5 compounds against
trypsin's active site and rank them by predicted binding affinity."

Adapts SKILL.md / examples/virtual_screen.py's virtual_screen() to the Vina
CLI (the `vina` PyPI Python binding has no Windows wheel on this machine --
see TOOLS.md). Ligand prep, receptor prep, and the per-ligand dock loop
follow the documented pattern; sorting and CSV output match
examples/virtual_screen.py's virtual_screen().
"""
import subprocess
from pathlib import Path
import pandas as pd

HERE = Path(__file__).parent
OUT = HERE.parent / "data" / "input2_out"
OUT.mkdir(exist_ok=True)

VINA_EXE = r"F:\OpenScience\audit-envs\cheminformatics-hit-triage-analyst\tools\vina\vina.exe"
RECEPTOR_PDBQT = str(HERE.parent / "data" / "input1_out" / "receptor.pdbqt")

# Small library: benzamidine (known trypsin S1 binder), a close analog, and
# three chemically simple decoys expected to bind weakly/nonspecifically.
LIBRARY = {
    "benzamidine": "NC(=[NH2+])c1ccccc1",
    "4-aminobenzamidine": "NC(=[NH2+])c1ccc(N)cc1",
    "toluene": "Cc1ccccc1",
    "phenol": "Oc1ccccc1",
    "imidazole": "c1c[nH]cn1",
}

CENTER = (-1.759, 14.461, 16.916)
BOX = (20.0, 20.0, 20.0)


def prepare_ligand(smiles, output_pdbqt):
    from rdkit import Chem
    from rdkit.Chem import AllChem
    from meeko import MoleculePreparation, PDBQTWriterLegacy

    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        raise ValueError(f'invalid SMILES: {smiles}')
    mol = Chem.AddHs(mol)
    embed_status = AllChem.EmbedMolecule(mol, AllChem.ETKDGv3())
    if embed_status != 0:
        raise RuntimeError('ETKDGv3 failed to generate a ligand conformer')
    if not AllChem.MMFFHasAllMoleculeParams(mol):
        raise ValueError('MMFF94 parameters are unavailable for this ligand')
    optimization_status = AllChem.MMFFOptimizeMolecule(mol)
    if optimization_status != 0:
        raise RuntimeError('MMFF94 ligand optimization did not converge')
    setups = MoleculePreparation().prepare(mol)
    pdbqt_text, is_ok, err = PDBQTWriterLegacy.write_string(setups[0])
    if not is_ok:
        raise RuntimeError(f'Meeko PDBQT export failed: {err}')
    Path(output_pdbqt).write_text(pdbqt_text)
    return output_pdbqt


def dock_cli(receptor_pdbqt, ligand_pdbqt, center, box_size, out_pdbqt, exhaustiveness=8, n_poses=5):
    cmd = [
        VINA_EXE, '--receptor', receptor_pdbqt, '--ligand', ligand_pdbqt,
        '--center_x', str(center[0]), '--center_y', str(center[1]), '--center_z', str(center[2]),
        '--size_x', str(box_size[0]), '--size_y', str(box_size[1]), '--size_z', str(box_size[2]),
        '--exhaustiveness', str(exhaustiveness), '--num_modes', str(n_poses),
        '--out', out_pdbqt, '--seed', '42',
    ]
    result = subprocess.run(cmd, check=True, capture_output=True, text=True)
    return result.stdout


def parse_best_affinity(vina_stdout):
    for line in vina_stdout.splitlines():
        parts = line.split()
        if len(parts) >= 4 and parts[0] == '1':
            try:
                return float(parts[1])
            except ValueError:
                continue
    return None


if __name__ == "__main__":
    assert Path(RECEPTOR_PDBQT).exists(), "run input1_dock_single.py first to produce the receptor"

    results = []
    for name, smiles in LIBRARY.items():
        try:
            ligand_pdbqt = str(OUT / f"{name}.pdbqt")
            prepare_ligand(smiles, ligand_pdbqt)
            out_pdbqt = str(OUT / f"{name}_poses.pdbqt")
            stdout = dock_cli(RECEPTOR_PDBQT, ligand_pdbqt, CENTER, BOX, out_pdbqt)
            best = parse_best_affinity(stdout)
            results.append({"name": name, "smiles": smiles, "affinity_kcal_mol": best})
            print(f"{name}: {best} kcal/mol")
        except Exception as e:
            results.append({"name": name, "smiles": smiles, "affinity_kcal_mol": None, "error": str(e)})
            print(f"{name}: ERROR {e}")

    df = pd.DataFrame(results)
    df = df.sort_values('affinity_kcal_mol')
    csv_path = OUT / "results.csv"
    df.to_csv(csv_path, index=False)
    print(f"\nRanked results written to {csv_path}")
    print(df.to_string(index=False))

    assert df['affinity_kcal_mol'].notna().all(), "one or more ligands failed to dock"
    best_row = df.iloc[0]
    assert best_row['name'] in ('benzamidine', '4-aminobenzamidine'), (
        f"expected a benzamidine analog to rank best; got {best_row['name']}"
    )
