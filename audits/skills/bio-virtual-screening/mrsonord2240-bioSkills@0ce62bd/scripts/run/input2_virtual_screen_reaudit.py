#!/usr/bin/env python3
"""
RE-AUDIT Input 2 (Variant A, regression): "Screen a 5-compound library
against the same active site, rank by affinity" -- re-run against the FIXED
examples/virtual_screen.py, exercising the new seed=42 parameter and the new
positive-energy pose filter (`energies = [e for e in energies if e[0] < 0] or
energies`).
"""
import subprocess
from pathlib import Path
import pandas as pd
from rdkit import Chem
from rdkit.Chem import AllChem
from meeko import MoleculePreparation, PDBQTWriterLegacy

HERE = Path(__file__).parent
OUT = HERE.parent / "out_input2"
OUT.mkdir(exist_ok=True)

ENV = Path("F:/OpenScience/audit-envs/cheminformatics-hit-triage-analyst")
VINA_EXE = ENV / "tools/vina/vina.exe"
RECEPTOR_PDBQT = HERE.parent / "out_input1" / "receptor.pdbqt"

LIBRARY = {
    "benzamidine": "NC(=[NH2+])c1ccccc1",
    "4-aminobenzamidine": "NC(=[NH2+])c1ccc(N)cc1",
    "toluene": "Cc1ccccc1",
    "phenol": "Oc1ccccc1",
    "imidazole": "c1c[nH]cn1",
}
CENTER = (-1.52, 14.47, 17.47)
BOX = (20.0, 20.0, 20.0)


def prepare_ligand(smiles, output_pdbqt):
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        raise ValueError(f'invalid SMILES: {smiles}')
    mol = Chem.AddHs(mol)
    if AllChem.EmbedMolecule(mol, AllChem.ETKDGv3()) != 0:
        raise RuntimeError('ETKDGv3 failed to generate a ligand conformer')
    if not AllChem.MMFFHasAllMoleculeParams(mol):
        raise ValueError('MMFF94 parameters are unavailable for this ligand')
    if AllChem.MMFFOptimizeMolecule(mol) != 0:
        raise RuntimeError('MMFF94 ligand optimization did not converge')
    setups = MoleculePreparation().prepare(mol)
    pdbqt_text, is_ok, err = PDBQTWriterLegacy.write_string(setups[0])
    if not is_ok:
        raise RuntimeError(f'meeko PDBQT export failed: {err}')
    Path(output_pdbqt).write_text(pdbqt_text)
    return output_pdbqt


def dock_cli(receptor_pdbqt, ligand_pdbqt, center, box_size, out_pdbqt, seed=42, exhaustiveness=8, n_poses=5):
    cmd = [str(VINA_EXE), '--receptor', receptor_pdbqt, '--ligand', ligand_pdbqt,
           '--center_x', str(center[0]), '--center_y', str(center[1]), '--center_z', str(center[2]),
           '--size_x', str(box_size[0]), '--size_y', str(box_size[1]), '--size_z', str(box_size[2]),
           '--exhaustiveness', str(exhaustiveness), '--num_modes', str(n_poses),
           '--out', out_pdbqt, '--seed', str(seed)]
    return subprocess.run(cmd, check=True, capture_output=True, text=True).stdout


def parse_energies(vina_stdout):
    modes = []
    started = False
    for line in vina_stdout.splitlines():
        if line.strip().startswith('-----'):
            started = True
            continue
        if started:
            parts = line.split()
            if len(parts) >= 4 and parts[0].isdigit():
                modes.append((float(parts[1]),))
    return modes


if __name__ == "__main__":
    assert RECEPTOR_PDBQT.exists(), "run input1_dock_single_reaudit.py first"
    results = []
    for name, smiles in LIBRARY.items():
        try:
            ligand_pdbqt = str(OUT / f"{name}.pdbqt")
            prepare_ligand(smiles, ligand_pdbqt)
            out_pdbqt = str(OUT / f"{name}_poses.pdbqt")
            stdout = dock_cli(str(RECEPTOR_PDBQT), ligand_pdbqt, CENTER, BOX, out_pdbqt)
            energies = parse_energies(stdout)
            # examples/virtual_screen.py's exact filter line:
            energies = [e for e in energies if e[0] < 0] or energies
            best = energies[0][0] if energies else None
            results.append({"name": name, "smiles": smiles, "affinity_kcal_mol": best})
            print(f"{name}: {best} kcal/mol")
        except Exception as e:
            results.append({"name": name, "smiles": smiles, "affinity_kcal_mol": None, "error": str(e)})
            print(f"{name}: ERROR {e}")

    df = pd.DataFrame(results).sort_values('affinity_kcal_mol')
    csv_path = OUT / "results.csv"
    df.to_csv(csv_path, index=False)
    print(df.to_string(index=False))

    assert df['affinity_kcal_mol'].notna().all(), "one or more ligands failed to dock"
    best_row = df.iloc[0]
    assert best_row['name'] in ('benzamidine', '4-aminobenzamidine'), \
        f"expected a benzamidine analog to rank best; got {best_row['name']}"
