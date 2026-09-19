#!/usr/bin/env python3
"""
RE-AUDIT Input 1 (Canonical, regression): "Dock benzamidine into trypsin's
S1 pocket (PDB 3PTB), full receptor+ligand prep" -- re-run against the FIXED
SKILL.md/examples/virtual_screen.py (branch fix/cg-vscreen, commit 0ce62bd).

Exercises, in order:
  1. prepare_receptor() FIXED route: pdb2pqr --pdb-output -> mk_prepare_receptor
     --read_pdb (was: mk_prepare_receptor.py --read_pqr, both broken pre-fix).
  2. dock_single()-equivalent CLI call with --seed 42 (new parameter).
  3. dock_single()'s positive-energy filter, applied to the real Vina output.

Vina CLI substituted for `from vina import Vina` -- no Windows wheel for the
`vina` PyPI package (TOOLS.md, unchanged pre-existing constraint).
"""
import subprocess
from pathlib import Path

HERE = Path(__file__).parent
OUT = HERE.parent / "out_input1"
OUT.mkdir(exist_ok=True)

ENV = Path("F:/OpenScience/audit-envs/cheminformatics-hit-triage-analyst")
PDB2PQR = ENV / "tools/pdb2pqr-venv/Scripts/pdb2pqr.exe"
MK_PREPARE_RECEPTOR = ENV / "Scripts/mk_prepare_receptor.exe"
VINA_EXE = ENV / "tools/vina/vina.exe"

REC_PDB = HERE.parent / "rec.pdb"
LIGAND_PDBQT = HERE.parent / "lig_benzamidine.pdbqt"
CENTER = (-1.52, 14.47, 17.47)
BOX = (20.0, 20.0, 20.0)


def prepare_receptor(repaired_pdb, pdbqt_out, pH=7.4):
    """Exactly the fixed SKILL.md prepare_receptor()."""
    base = str(Path(repaired_pdb).with_suffix(''))
    protonated_pdb = f'{base}_pH{pH}.pdb'
    pqr_file = f'{base}_pH{pH}.pqr'
    subprocess.run([str(PDB2PQR), '--ff=AMBER', f'--with-ph={pH}',
                    '--pdb-output', protonated_pdb,
                    str(repaired_pdb), pqr_file], check=True)
    output_basename = str(Path(pdbqt_out).with_suffix(''))
    subprocess.run([str(MK_PREPARE_RECEPTOR), '--read_pdb', protonated_pdb,
                    '-o', output_basename, '-p'], check=True)
    return pdbqt_out


def dock_single_filter(energies):
    """Exactly dock_single()'s filter logic from the fixed SKILL.md."""
    valid = [i for i, e in enumerate(energies) if e[0] < 0]
    if len(valid) < len(energies):
        energies = [energies[i] for i in valid]
    return energies


def parse_modes(vina_stdout):
    modes = []
    started = False
    for line in vina_stdout.splitlines():
        if line.strip().startswith('-----'):
            started = True
            continue
        if started:
            parts = line.split()
            if len(parts) >= 4 and parts[0].isdigit():
                modes.append((float(parts[1]), float(parts[2]), float(parts[3])))
    return modes


if __name__ == "__main__":
    receptor_pdbqt = str(OUT / "receptor.pdbqt")
    prepare_receptor(str(REC_PDB), receptor_pdbqt)
    assert Path(receptor_pdbqt).exists() and Path(receptor_pdbqt).stat().st_size > 0
    print(f"Receptor prepared: {receptor_pdbqt} ({Path(receptor_pdbqt).stat().st_size} bytes)")

    out_poses = str(OUT / "poses.pdbqt")
    cmd = [str(VINA_EXE), '--receptor', receptor_pdbqt, '--ligand', str(LIGAND_PDBQT),
           '--center_x', str(CENTER[0]), '--center_y', str(CENTER[1]), '--center_z', str(CENTER[2]),
           '--size_x', str(BOX[0]), '--size_y', str(BOX[1]), '--size_z', str(BOX[2]),
           '--exhaustiveness', '8', '--num_modes', '9', '--seed', '42', '--out', out_poses]
    result = subprocess.run(cmd, check=True, capture_output=True, text=True)
    print(result.stdout)

    modes = parse_modes(result.stdout)
    filtered = dock_single_filter(modes)
    print(f"Parsed {len(modes)} modes; {len(filtered)} after positive-energy filter")
    assert len(filtered) == len(modes), "no positive-energy artifact appeared in this real run (expected -- filter is a no-op safety net here)"
    best = filtered[0][0]
    print(f"Best affinity = {best} kcal/mol")
    assert best < -4.0, f"expected a literature-plausible negative affinity, got {best}"
