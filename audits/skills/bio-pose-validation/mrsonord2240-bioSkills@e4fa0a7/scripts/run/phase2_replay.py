"""Phase 2 independent replay for bio-pose-validation.

Runs the seven Phase-1 input classes against the exact-tip source snapshot and
two additional boundary cases.  All paths are audit-owned; the assigned source
worktree is never imported or written during this execution.
"""
from __future__ import annotations

import importlib.util
import subprocess
import sys
from pathlib import Path

import numpy as np
from posebusters import PoseBusters
from rdkit import Chem
from rdkit.Chem import AllChem


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
SNAPSHOT = ROOT / "run" / "source_snapshot"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


VALIDATE = load_module("audit_validate_poses", SNAPSHOT / "validate_poses.py")
BATCH = load_module("audit_pose_qc_batch", SNAPSHOT / "pose_qc_batch.py")


def boolean_columns(frame):
    return [c for c in frame.select_dtypes(include="bool").columns if not c.lower().startswith("rmsd")]


def pb_valid(frame):
    columns = boolean_columns(frame)
    assert columns, "PoseBusters returned no boolean check columns"
    return bool(frame[columns].all(axis=1).iloc[0])


def input_1_canonical():
    r = PoseBusters(config="dock").bust(mol_pred=DATA / "mode1_fixed.sdf", mol_cond=DATA / "receptor.pdb")
    ok = pb_valid(r)
    assert ok and len(boolean_columns(r)) == 22
    print(f"INPUT 1 PASS: dock bool_checks={len(boolean_columns(r))} pb_valid={ok}")


def input_2_strain():
    smoke = subprocess.run([sys.executable, str(SNAPSHOT / "validate_poses.py")], check=True, capture_output=True, text=True)
    assert "OK: fixture pose is PB-valid, strain computed successfully." in smoke.stdout
    r = VALIDATE.ligand_strain_mmff(DATA / "mode1_fixed.sdf", n_ref_conf=20)
    value = float(r.loc[0, "strain_kcal"])
    assert r.loc[0, "note"] == "ok" and abs(value - 4.162648) < 0.001
    print(f"INPUT 2 PASS: fixture __main__ and strain_kcal={value:.6f} note={r.loc[0, 'note']}")


def input_3_edge_poses():
    dock = PoseBusters(config="dock")
    clash = dock.bust(mol_pred=DATA / "clash_pose.sdf", mol_cond=DATA / "receptor.pdb")
    clash_failures = [c for c in boolean_columns(clash) if not bool(clash[c].iloc[0])]
    mol = PoseBusters(config="mol")
    stretched = mol.bust(mol_pred=DATA / "stretched_bond.sdf")
    stretched_failures = [c for c in boolean_columns(stretched) if not bool(stretched[c].iloc[0])]
    puckered = mol.bust(mol_pred=DATA / "puckered_ring.sdf")
    control = mol.bust(mol_pred=DATA / "mode1_fixed.sdf")
    assert not pb_valid(clash) and {"minimum_distance_to_protein", "volume_overlap_with_protein"}.issubset(clash_failures)
    assert not pb_valid(stretched) and {"bond_lengths", "bond_angles"}.issubset(stretched_failures)
    assert pb_valid(puckered) and pb_valid(control)
    print(f"INPUT 3 PASS: clash={clash_failures}; stretched={stretched_failures}; puckered=True; control=True")


def input_4_redock():
    r = PoseBusters(config="redock").bust(
        mol_pred=DATA / "mode1_fixed.sdf", mol_true=DATA / "ben_ref.sdf", mol_cond=DATA / "receptor.pdb"
    )
    rmsd = next(c for c in r.columns if c.lower().startswith("rmsd"))
    assert pb_valid(r) and bool(r[rmsd].iloc[0])
    assert bool(r["double_bond_stereochemistry"].iloc[0]) and bool(r["tetrahedral_chirality"].iloc[0])
    rmsd_label = rmsd.encode("ascii", "replace").decode("ascii")
    print(f"INPUT 4 PASS: {rmsd_label}={bool(r[rmsd].iloc[0])} pb_valid=True")


def input_5_stress_batch():
    paths = [DATA / f"mode{i}_fixed.sdf" for i in range(1, 9)] + [DATA / "clash_pose.sdf"]
    cli = subprocess.run(
        [sys.executable, str(SNAPSHOT / "pose_qc_batch.py"), str(DATA / "receptor.pdb"), *[str(p) for p in paths]],
        check=True, capture_output=True, text=True,
    )
    assert "8 / 9 files have a PB-valid pose" in cli.stdout
    shortlisted = BATCH.pose_qc_pipeline([str(p) for p in paths], str(DATA / "receptor.pdb"))
    valid_sources = set(shortlisted["source"])
    assert len(shortlisted) == 8
    assert all(str(DATA / f"mode{i}_fixed.sdf") in valid_sources for i in range(1, 9))
    assert str(DATA / "clash_pose.sdf") not in valid_sources
    print("INPUT 5 PASS: 8 valid Vina modes retained; clash excluded")


def input_6_chirality():
    redock = PoseBusters(config="redock").bust(
        mol_pred=DATA / "pred_S_inverted.sdf", mol_true=DATA / "true_R.sdf", mol_cond=DATA / "receptor.pdb"
    )
    dock = PoseBusters(config="dock").bust(mol_pred=DATA / "pred_S_inverted.sdf", mol_cond=DATA / "receptor.pdb")
    mol = PoseBusters(config="mol").bust(mol_pred=DATA / "pred_S_inverted.sdf")
    assert not bool(redock["tetrahedral_chirality"].iloc[0])
    assert "tetrahedral_chirality" not in dock.columns and "tetrahedral_chirality" not in mol.columns
    assert "double_bond_stereochemistry" not in mol.columns
    print("INPUT 6 PASS: redock catches R/S inversion; dock/mol correctly omit reference stereo checks")


def input_7_planarity():
    outputs = []
    for name in ("puck_0.6.sdf", "puck_1.0.sdf", "puck_1.5.sdf", "puck_2.0.sdf"):
        completed = subprocess.run(
            [sys.executable, str(SNAPSHOT / "aromatic_planarity.py"), str(DATA / name)],
            check=True, capture_output=True, text=True,
        )
        value = float(completed.stdout.strip().split("deviation ")[-1].split()[0])
        flat = bool(PoseBusters(config="mol").bust(mol_pred=DATA / name)["aromatic_ring_flatness"].iloc[0])
        outputs.append((name, round(value, 4), flat))
    assert outputs[0][1:] == (0.2888, True)
    assert outputs[1][1:] == (0.4524, False)
    assert outputs[2][2] is False and outputs[3][2] is False
    print(f"INPUT 7 PASS: planarity series={outputs}")


def input_8_fresh_multimode_file():
    multi = DATA / "fresh_invalid_then_valid.sdf"
    writer = Chem.SDWriter(str(multi))
    for source in (DATA / "clash_pose.sdf", DATA / "mode1_fixed.sdf", DATA / "mode2_fixed.sdf"):
        supplier = Chem.SDMolSupplier(str(source), removeHs=False)
        molecule = next(m for m in supplier if m is not None)
        writer.write(molecule)
    writer.close()
    raw = PoseBusters(config="dock").bust(mol_pred=multi, mol_cond=DATA / "receptor.pdb")
    raw_valid = raw[boolean_columns(raw)].all(axis=1).tolist()
    shortlisted = BATCH.pose_qc_pipeline([str(multi)], str(DATA / "receptor.pdb"))
    assert raw_valid == [False, True, True]
    assert len(shortlisted) == 1 and int(shortlisted.index[0][-1]) == 1
    print("INPUT 8 PASS: fresh three-pose SDF retains the first PB-valid pose after an invalid first record")


def input_9_fresh_unsupported_mmff():
    path = DATA / "fresh_malformed.sdf"
    path.write_text("not an SDF record\n", encoding="utf-8")
    r = VALIDATE.ligand_strain_mmff(path, n_ref_conf=5)
    note = str(r.loc[0, "note"])
    assert note == "parse_fail", note
    assert r.loc[0, "strain_kcal"] is None
    print(f"INPUT 9 PASS: fresh malformed SDF returns structured note={note}, not a crash")


def main():
    for run in (
        input_1_canonical, input_2_strain, input_3_edge_poses, input_4_redock,
        input_5_stress_batch, input_6_chirality, input_7_planarity,
        input_8_fresh_multimode_file, input_9_fresh_unsupported_mmff,
    ):
        run()
    print("ALL ASSERTIONS PASS: 9/9 inputs completed")


if __name__ == "__main__":
    main()
