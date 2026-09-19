#!/usr/bin/env python3
"""
Input 1 (Canonical): "Dock this ligand (benzamidine) into the trypsin active
site (PDB 3PTB) and give me the best poses and affinities."

Follows the SKILL.md 'Receptor Preparation' + 'Ligand Preparation' + 'Vina
Docking (Single Ligand)' sections as literally as possible, then adapts the
'from vina import Vina' call to the Vina CLI because the `vina` PyPI package
has no Windows wheel (see TOOLS.md: "pip install vina fails ... Boost library
location was not found"). Everything else (pdb2pqr, meeko, RDKit embedding)
is run exactly as documented.
"""
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).parent
DATA = HERE.parent / "data"
OUT = HERE.parent / "data" / "input1_out"
OUT.mkdir(exist_ok=True)

VINA_EXE = r"F:\OpenScience\audit-envs\cheminformatics-hit-triage-analyst\tools\vina\vina.exe"
PDB2PQR_EXE = r"F:\OpenScience\audit-envs\cheminformatics-hit-triage-analyst\tools\pdb2pqr-venv\Scripts\pdb2pqr.exe"
MK_PREPARE_RECEPTOR = r"F:\OpenScience\audit-envs\cheminformatics-hit-triage-analyst\Scripts\mk_prepare_receptor.exe"
MK_PREPARE_RECEPTOR_PY_LITERAL = "mk_prepare_receptor.py"  # exactly as SKILL.md line 76 spells it


def prepare_receptor_as_documented(repaired_pdb, pdbqt_out, pH=7.4):
    """Verbatim translation of SKILL.md's prepare_receptor(), with two
    documented failures worked around so the audit can proceed:

    1. SKILL.md calls the literal command 'mk_prepare_receptor.py'. The
       installed meeko 0.8.0 provides a console-script entry point named
       'mk_prepare_receptor' (no .py). FileNotFoundError -- confirmed below.
    2. SKILL.md's --read_pqr route, fed pdb2pqr's default .pqr output, raises
       ValueError inside meeko's PQR parser ("invalid literal for int() with
       base 10: '184A'") on this real trypsin structure (3PTB), because
       trypsin uses chymotrypsin numbering with insertion codes (184A, 188A,
       221A ...) and meeko 0.8.0's fixed-column PQR reader cannot parse an
       alphanumeric residue number. This is not a synthetic edge case --
       chymotrypsin-numbered serine proteases are a standard docking
       benchmark family. Confirmed below, then worked around by using
       pdb2pqr's --pdb-output and mk_prepare_receptor --read_pdb instead
       (the route the example script uses, undocumented in SKILL.md).
    """
    base = str(Path(repaired_pdb).with_suffix(''))
    pqr_file = f'{base}_pH{pH}.pqr'
    protonated_pdb = f'{base}_pH{pH}.pdb'
    subprocess.run([PDB2PQR_EXE, '--ff=AMBER', f'--with-ph={pH}', '--pdb-output', protonated_pdb,
                    repaired_pdb, pqr_file], check=True)
    output_basename = str(Path(pdbqt_out).with_suffix(''))

    # (1) SKILL.md literally calls 'mk_prepare_receptor.py' -- confirm that fails.
    try:
        subprocess.run([MK_PREPARE_RECEPTOR_PY_LITERAL, '--read_pqr', pqr_file,
                        '-o', output_basename, '-p'], check=True)
        print("UNEXPECTED: SKILL.md's literal 'mk_prepare_receptor.py' command succeeded")
    except FileNotFoundError as e:
        print(f"CONFIRMED BUG 1: SKILL.md's literal 'mk_prepare_receptor.py' command fails: {e}")

    # (2) SKILL.md's --read_pqr route -- confirm that fails on this real target.
    try:
        subprocess.run([MK_PREPARE_RECEPTOR, '--read_pqr', pqr_file,
                        '-o', output_basename, '-p'], check=True, capture_output=True, text=True)
        print("UNEXPECTED: SKILL.md's --read_pqr route succeeded on 3PTB")
    except subprocess.CalledProcessError as e:
        print("CONFIRMED BUG 2: SKILL.md's --read_pqr route crashes on 3PTB (insertion-code residues):")
        print(e.stderr.splitlines()[-3:] if e.stderr else "(no stderr captured)")

    # Workaround: use the example script's --read_pdb route instead (undocumented
    # in SKILL.md how to arrive at a "protonated_pdb" from pdb2pqr).
    subprocess.run([MK_PREPARE_RECEPTOR, '--read_pdb', protonated_pdb,
                    '-o', output_basename, '-p'], check=True)
    print("Receptor PDBQT produced via workaround (--pdb-output + --read_pdb)")
    return pdbqt_out


def prepare_ligand(smiles, output_pdbqt):
    """Verbatim from SKILL.md / examples/virtual_screen.py."""
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


def dock_single_cli(receptor_pdbqt, ligand_pdbqt, center, box_size, out_pdbqt,
                     exhaustiveness=8, n_poses=10, seed=None):
    """Same semantics as SKILL.md's dock_single(), adapted to the Vina CLI
    because `from vina import Vina` has no Windows wheel on this machine."""
    cmd = [
        VINA_EXE,
        '--receptor', receptor_pdbqt,
        '--ligand', ligand_pdbqt,
        '--center_x', str(center[0]), '--center_y', str(center[1]), '--center_z', str(center[2]),
        '--size_x', str(box_size[0]), '--size_y', str(box_size[1]), '--size_z', str(box_size[2]),
        '--exhaustiveness', str(exhaustiveness),
        '--num_modes', str(n_poses),
        '--out', out_pdbqt,
    ]
    if seed is not None:
        cmd += ['--seed', str(seed)]
    result = subprocess.run(cmd, check=True, capture_output=True, text=True)
    return result.stdout


def parse_affinities(vina_stdout):
    affinities = []
    for line in vina_stdout.splitlines():
        parts = line.split()
        if len(parts) >= 4 and parts[0].isdigit():
            try:
                affinities.append((int(parts[0]), float(parts[1])))
            except ValueError:
                pass
    return affinities


if __name__ == "__main__":
    # 3PTB = trypsin + benzamidine co-crystal. rec.pdb = protein-only, already
    # split from the co-crystal by the tooling agent's smoke test.
    repaired_pdb = str(DATA / "rec.pdb")
    receptor_pdbqt = str(OUT / "receptor.pdbqt")

    print("=== Receptor preparation (pdb2pqr -> mk_prepare_receptor) ===")
    prepare_receptor_as_documented(repaired_pdb, receptor_pdbqt)
    assert Path(receptor_pdbqt).exists(), "receptor PDBQT was not produced"
    print(f"Receptor PDBQT: {receptor_pdbqt} ({Path(receptor_pdbqt).stat().st_size} bytes)")

    print("\n=== Ligand preparation (RDKit ETKDGv3 + MMFF94 + meeko) ===")
    benzamidine_smiles = "NC(=[NH2+])c1ccccc1"  # protonated amidinium, matches physiological state
    ligand_pdbqt = str(OUT / "benzamidine.pdbqt")
    prepare_ligand(benzamidine_smiles, ligand_pdbqt)
    assert Path(ligand_pdbqt).exists()
    print(f"Ligand PDBQT: {ligand_pdbqt} ({Path(ligand_pdbqt).stat().st_size} bytes)")

    # Binding site: trypsin S1 pocket, centered on the co-crystallized
    # benzamidine ligand's own atom centroid (computed directly from the
    # HETATM BEN records in 3ptb.pdb -- this is what SKILL.md's
    # find_binding_site() function is documented to do).
    center = (-1.759, 14.461, 16.916)
    box_size = (20.0, 20.0, 20.0)

    print("\n=== Vina docking (CLI; python `vina` package has no Windows wheel) ===")
    out_pdbqt = str(OUT / "poses.pdbqt")
    stdout = dock_single_cli(receptor_pdbqt, ligand_pdbqt, center, box_size, out_pdbqt,
                              exhaustiveness=8, n_poses=9, seed=42)
    print(stdout)
    affinities = parse_affinities(stdout)
    print(f"Parsed {len(affinities)} modes; best affinity = {affinities[0][1] if affinities else 'N/A'} kcal/mol")
    assert len(affinities) > 0, "Vina produced no poses"
    assert affinities[0][1] < -3.0, f"Best affinity implausibly weak: {affinities[0][1]}"
