"""Final-pass execution evidence for bio-conformer-generation.

Runs the nine archived logical inputs against code extracted from the current
SKILL.md plus two fresh packaged-example/edge inputs. Usage:
  python final_regression_audit.py --skill-dir <conformer-generation-dir> --out audit-result.json
"""

import argparse
import importlib.util
import json
import os
import re
import subprocess
import sys
from pathlib import Path

import numpy as np
from rdkit import Chem
from rdkit.Chem import AllChem, Descriptors3D, Lipinski


def load_inline_functions(skill_dir: Path) -> dict:
    """Execute every Python fence from SKILL.md in the documented order."""
    text = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
    blocks = re.findall(r"```python\n(.*?)```", text, flags=re.DOTALL)
    scope = {"Chem": Chem, "AllChem": AllChem, "np": np, "subprocess": subprocess, "Path": Path}
    for index, block in enumerate(blocks, start=1):
        compile(block, f"SKILL.md python block {index}", "exec")
        exec(block, scope)
    expected = {"gen_conformers", "optimize_conformers", "prune_conformers_rmsd",
                "filter_by_energy", "macrocycle_conformers", "crest_workflow",
                "boltzmann_weights", "boltzmann_average"}
    missing = expected.difference(scope)
    if missing:
        raise RuntimeError(f"SKILL.md code fences did not define: {sorted(missing)}")
    return scope


def record(results: list, label: str, callback) -> None:
    try:
        details = callback()
        results.append({"label": label, "pass": True, "details": details})
    except Exception as exc:  # retain all failures as audit evidence
        results.append({"label": label, "pass": False,
                        "details": {"exception": type(exc).__name__, "message": str(exc)}})


def energies_for(mol, ids):
    props = AllChem.MMFFGetMoleculeProperties(mol, mmffVariant="MMFF94s")
    if props is None:
        raise AssertionError("MMFF94s unexpectedly unavailable")
    values = []
    for cid in ids:
        force_field = AllChem.MMFFGetMoleculeForceField(mol, props, confId=cid)
        assert force_field is not None
        status = force_field.Minimize(maxIts=1000)
        assert status == 0
        values.append(float(force_field.CalcEnergy()))
    return values


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skill-dir", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    skill_dir = args.skill_dir.resolve()
    args.out.parent.mkdir(parents=True, exist_ok=True)
    scope = load_inline_functions(skill_dir)
    gen = scope["gen_conformers"]
    optimize = scope["optimize_conformers"]
    prune = scope["prune_conformers_rmsd"]
    energy_filter = scope["filter_by_energy"]
    macrocycle = scope["macrocycle_conformers"]
    crest = scope["crest_workflow"]
    bweights = scope["boltzmann_weights"]
    baverage = scope["boltzmann_average"]
    results = []

    def input1():
        mol, ids = gen("CC(=O)OC1=CC=CC=C1C(=O)O", n_conf=20, seed=42)
        output = optimize(mol, ids)
        assert len(ids) == 20 and len(output) == 20
        assert all(item.get("converged") for item in output)
        return {"embedded": len(ids), "converged": len(output),
                "energy_range": [min(x["energy"] for x in output), max(x["energy"] for x in output)]}
    record(results, "1 canonical aspirin ETKDGv3/MMFF94s regression", input1)

    def input2():
        mol, ids = gen("CC(C)Cc1ccc(cc1)[C@@H](C)C(=O)O", n_conf=1, seed=42)
        values = optimize(mol, ids)
        sdf_path = args.out.parent / "input2_ibuprofen.sdf"
        writer = Chem.SDWriter(str(sdf_path))
        writer.write(mol, confId=ids[0])
        writer.close()
        roundtrip = Chem.SDMolSupplier(str(sdf_path), removeHs=False)[0]
        z_values = [roundtrip.GetConformer().GetAtomPosition(i).z for i in range(roundtrip.GetNumAtoms())]
        assert max(z_values) - min(z_values) > 0.1
        return {"embedded": len(ids), "energy": values[0]["energy"], "sdf": str(sdf_path)}
    record(results, "2 variant ibuprofen one-conformer SDF regression", input2)

    def input3():
        mol, ids = gen("OB(O)c1ccccc1", n_conf=10, seed=42)
        output = optimize(mol, ids)
        assert len(output) == 10 and {x["force_field"] for x in output} == {"UFF"}
        return {"embedded": len(ids), "force_field": "UFF",
                "energy_range": [min(x["energy"] for x in output), max(x["energy"] for x in output)]}
    record(results, "3 edge phenylboronic-acid UFF fallback regression", input3)

    def input4():
        smiles = "C1CCCCCCCCCCCCC1"
        ring_sizes = [len(ring) for ring in Chem.GetSymmSSSR(Chem.MolFromSmiles(smiles))]
        assert ring_sizes == [14]
        # Same archived macrocycle scenario, bounded to 10 conformers because RDKit
        # 2026.03 takes minutes for 50 with the deliberately expensive settings.
        mol, ids = macrocycle(smiles, n_conf=10, seed=42)
        energies = energies_for(mol, ids)
        default = AllChem.ETKDGv3()
        assert default.useMacrocycleTorsions is True
        return {"ring_size": 14, "embedded": len(ids), "default_macrocycle_torsions": True,
                "energy_range": [min(energies), max(energies)]}
    record(results, "4 variant macrocycle ETKDGv3 regression", input4)

    def input5():
        smiles = "Cc1ccc(NC(=O)c2ccc(CN3CCN(C)CC3)cc2)cc1Nc1nccc(-c2cccnc2)n1"
        n_conf = max(10, 5 * Lipinski.NumRotatableBonds(Chem.MolFromSmiles(smiles)) + 10)
        mol, ids = gen(smiles, n_conf=n_conf, seed=42)
        output = optimize(mol, ids)
        conf_ids = [item["conf_id"] for item in output if "energy" in item]
        values = [item["energy"] for item in output if "energy" in item]
        kept = prune(mol, conf_ids, rmsd_cutoff=0.5)
        kept_energy = [values[conf_ids.index(cid)] for cid in kept]
        windowed = energy_filter(mol, kept, kept_energy, window_kcal=10.0)
        property_values = [Descriptors3D.Asphericity(mol, confId=cid) for cid in kept]
        average = baverage(property_values, kept_energy)
        assert len(ids) == n_conf and windowed and np.isfinite(average)
        return {"rotatable_bonds": Lipinski.NumRotatableBonds(Chem.MolFromSmiles(smiles)),
                "requested": n_conf, "embedded": len(ids), "rmsd_kept": len(kept),
                "energy_window_kept": len(windowed), "boltzmann_asphericity": average}
    record(results, "5 stress flexible drug pipeline regression", input5)

    def input6():
        crest_dir = args.out.parent / "crest_expected_missing"
        try:
            crest("CCO", out_dir=crest_dir)
        except FileNotFoundError as exc:
            crest_error = str(exc)
        else:
            raise AssertionError("crest_workflow unexpectedly succeeded without CREST")
        xtb = Path(r"F:\OpenScience\audit-envs\cheminformatics-hit-triage-analyst\tools\xtb\xtb-6.7.1\bin\xtb.exe")
        xtb_share = str(xtb.parents[1] / "share" / "xtb")
        mol, ids = gen("CCO", n_conf=1, seed=42)
        xyz = args.out.parent / "ethanol.xyz"
        xyz.write_text(Chem.MolToXYZBlock(mol, confId=ids[0]), encoding="utf-8")
        environment = os.environ.copy()
        environment["XTBPATH"] = xtb_share
        completed = subprocess.run([str(xtb), xyz.name, "--opt"], cwd=xyz.parent, env=environment,
                                   capture_output=True, text=True, check=True, timeout=120)
        optimized = xyz.parent / "xtbopt.xyz"
        assert optimized.exists() and completed.returncode == 0
        return {"crest_exception": crest_error, "xtbopt": str(optimized), "xtb_returncode": completed.returncode}
    record(results, "6 scope Windows CREST caveat and xtb fallback regression", input6)

    def input7():
        messages = []
        for bad in ("Xyz[[[invalid", "c1ccccc1(((", ""):
            try:
                gen(bad)
            except ValueError as exc:
                messages.append(str(exc))
            else:
                raise AssertionError(f"invalid SMILES accepted: {bad!r}")
        def seeded(seed):
            mol, ids = gen("Cn1cnc2c1c(=O)n(C)c(=O)n2C", n_conf=15, seed=seed)
            return sorted(round(value, 6) for value in energies_for(mol, ids))
        run_one, run_two, different_seed = seeded(7), seeded(7), seeded(99)
        assert run_one == run_two and run_one != different_seed
        assert all("Invalid SMILES" in message for message in messages)
        return {"invalid_messages": messages, "same_seed_identical": True, "different_seed_changes": True}
    record(results, "7 adversarial malformed-SMILES and determinism regression", input7)

    def input8():
        smiles = "[Fe+2].C1=CC=CC=C1.C1=CC=CC=C1"
        mol, ids = gen(smiles, n_conf=5, seed=42)
        try:
            output = optimize(mol, ids)
            outcome = {"result": "optimized", "force_fields": sorted({x.get("force_field") for x in output})}
        except ValueError as exc:
            outcome = {"result": "clear_error", "message": str(exc)}
        assert ids and outcome["result"] in {"optimized", "clear_error"}
        return {"embedded": len(ids), **outcome}
    record(results, "8 adversarial metal/disconnected input regression", input8)

    def input9():
        assert prune(Chem.MolFromSmiles("c1ccccc1"), []) == []
        assert energy_filter(None, [], []) == []
        try:
            energy_filter(None, [1], [])
        except ValueError as exc:
            mismatch = str(exc)
        else:
            raise AssertionError("mismatched energy arrays did not fail")
        for values in ([], [1.0, float("nan")]):
            try:
                bweights(values)
            except ValueError:
                pass
            else:
                raise AssertionError("invalid Boltzmann energy input did not fail")
        uniform = bweights([10.0, 10.0, 10.0])
        assert np.allclose(uniform, uniform[0]) and np.isclose(uniform.sum(), 1.0)
        return {"empty_energy_filter": [], "mismatch_message": mismatch, "uniform_weights": uniform.tolist()}
    record(results, "9 edge empty helpers and Boltzmann validation regression", input9)

    def input10():
        sys.dont_write_bytecode = True
        path = skill_dir / "examples" / "gen_conformers.py"
        module_spec = importlib.util.spec_from_file_location("packaged_gen_conformers", path)
        module = importlib.util.module_from_spec(module_spec)
        assert module_spec.loader is not None
        module_spec.loader.exec_module(module)
        mol, data = module.gen_conformer_ensemble("CCO", n_conf=3, seed=42)
        macro_mol, macro_ids = module.macrocycle_conformers("C1CCCCCCCCCCCCC1", n_conf=3, seed=42)
        try:
            module.gen_conformer_ensemble("")
        except ValueError as exc:
            empty_message = str(exc)
        else:
            raise AssertionError("packaged example accepted empty SMILES")
        assert len(data) == 3 and len(macro_ids) == 3 and macro_mol.GetNumConformers() == 3
        return {"ensemble_rows": len(data), "macrocycle_ids": len(macro_ids), "empty_message": empty_message}
    record(results, "10 fresh packaged gen_conformers contract input", input10)

    def input11():
        script = skill_dir / "examples" / "compare_macrocycle_embedding.py"
        command = [sys.executable, str(script), "--smiles", "O=C1CCCCCCCCCCCNC1", "--n-conf", "5", "--seed", "42"]
        completed = subprocess.run(command, capture_output=True, text=True, check=True)
        summary = json.loads(completed.stdout)
        assert summary["etkdgv3_default"]["embedded"] > 0
        assert summary["macrocycle_torsions_opt_out"]["embedded"] > 0
        invalid = subprocess.run([sys.executable, str(script), "--smiles", "CCO", "--n-conf", "0"],
                                 capture_output=True, text=True)
        assert invalid.returncode != 0 and "at least 1" in invalid.stderr
        return summary
    record(results, "11 fresh packaged macrocycle comparison input", input11)

    report = {"source_skill_dir": str(skill_dir), "rdkit": __import__("rdkit").__version__, "results": results}
    report["passed"] = sum(item["pass"] for item in results)
    report["total"] = len(results)
    args.out.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    if report["passed"] != report["total"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
