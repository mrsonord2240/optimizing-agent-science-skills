"""Final-pass phase-2 regression and fresh execution evidence.

Runs only against the immutable audit copy of the dispatched source tree. Each
printed INPUT block maps to a report row; every computational claim has an
assertion, rather than trusting an exit status alone.
"""

from __future__ import annotations

import math
import subprocess
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = ROOT / "phase2_skill_copy" / "examples"
sys.path.insert(0, str(EXAMPLES))

from protac_enumerate import build_protac, compute_protac_size, enumerate_linkers
from ternary_geometry_screen import (
    _theoretical_max_reach_alkyl,
    linker_reach,
    screen_linker_library,
)
from cooperativity_dc50 import (
    _hook_curve,
    _hill,
    cooperativity_alpha,
    detect_hook,
    fit_dc50,
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def run_shipped(script: str) -> str:
    completed = subprocess.run(
        [sys.executable, str(EXAMPLES / script)],
        cwd=EXAMPLES,
        text=True,
        capture_output=True,
        check=True,
    )
    require(completed.stderr == "", f"{script} wrote stderr: {completed.stderr}")
    return completed.stdout


def input_1_canonical() -> None:
    output = run_shipped("protac_enumerate.py")
    target = "[*]c1ccc(CN2CCOCC2)cc1"
    e3 = "[*]CC(=O)N1CCC(=O)NC1=O"
    products = enumerate_linkers(target, e3)
    require(len(products) == 11, f"expected 11 linker products, got {len(products)}")
    require(all("*" not in smi for smi in products.values()), "unconsumed dummy atom")
    props = compute_protac_size(products["medium_pegylated"])
    require(props["MolWt"] > 400 and props["TPSA"] > 50 and props["RotBonds"] >= 9,
            f"unexpected medium_peg properties: {props}")
    require("short_alkyl:" in output and "properties:" in output,
            "shipped enumerator demo output incomplete")
    print(f"INPUT1 canonical: 11 connected products; medium_peg={props}; shipped_demo=PASS")


def input_3_attachment_edge() -> None:
    cases = [
        ("double-bond dummy", "[*]=CC", "[*:1]CC[*:2]", "[*]CC", "single bonds"),
        ("two target dummies", "[*]CC[*]", "[*:1]CC[*:2]", "[*]CC", "exactly one"),
        ("invalid smiles", "not-a-smiles", "[*:1]CC[*:2]", "[*]CC", "valid SMILES"),
    ]
    for name, target, linker, e3, expected in cases:
        try:
            build_protac(target, linker, e3)
        except ValueError as exc:
            require(expected in str(exc), f"{name}: unexpected error {exc}")
        else:
            raise AssertionError(f"{name}: expected ValueError")
    control = build_protac("[*]c1ccccc1", "[*:1]CCOCC[*:2]", "[*]C(=O)N")
    require("*" not in control, "valid control retains dummy")
    print(f"INPUT3 attachment edge: 3 invalid inputs rejected; control={control}")


def input_4_vhl_variant() -> None:
    target = "[*]c1ccc(CN2CCOCC2)cc1"
    crbn = "[*]CC(=O)N1CCC(=O)NC1=O"
    vhl = "[*]C(=O)N[C@@H](C(O)=O)C(C)(C)C"
    crbn_products = enumerate_linkers(target, crbn)
    vhl_products = enumerate_linkers(target, vhl)
    require(len(crbn_products) == len(vhl_products) == 11, "ligase switch lost variants")
    crbn_props = compute_protac_size(crbn_products["medium_pegylated"])
    vhl_props = compute_protac_size(vhl_products["medium_pegylated"])
    require(vhl_props["MolWt"] != crbn_props["MolWt"], "ligase switch did not alter product")
    require(all("*" not in smi for smi in vhl_products.values()), "VHL products retain dummy")
    print(f"INPUT4 VHL switch: 11 variants; CRBN_MW={crbn_props['MolWt']:.1f}; VHL_MW={vhl_props['MolWt']:.1f}")


def input_5_well_separated_hook() -> None:
    alpha_cases = [(90.0, 9.0, "positive cooperativity"), (8.0, 32.0, "negative cooperativity"),
                   (15.0, 15.0, "no cooperativity")]
    for binary, ternary, label in alpha_cases:
        result = cooperativity_alpha(binary, ternary)
        require(result["label"] == label, f"alpha label mismatch for {binary}/{ternary}")
    try:
        cooperativity_alpha(-1.0, 2.0)
    except ValueError:
        pass
    else:
        raise AssertionError("negative Kd must be rejected")
    truth = dict(dmax=55.0, dc50=8.0, hill=1.4, hook_k=900.0, hook_hill=2.0)
    rng = np.random.default_rng(777)
    conc = np.logspace(0, 3.7, 16)
    observed = np.clip(_hook_curve(conc, **truth) + rng.normal(0, 1.0, len(conc)), 0, 100)
    hook = detect_hook(conc, observed)
    fit = fit_dc50(conc, observed, peak_idx=hook["peak_idx"])
    dc50_err = abs(fit["dc50_fit"] - truth["dc50"]) / truth["dc50"]
    dmax_err = abs(fit["dmax_fit"] - truth["dmax"])
    require(hook["hook_effect"], "well-separated hook not detected")
    require(dc50_err < 0.30 and dmax_err < 12.0, f"fit mismatch {dc50_err=}, {dmax_err=}")
    require(fit["plateau_reached"] is True and fit["caveat"] is None, "false narrow-hook caveat")
    print(f"INPUT5 well-separated hook: alpha labels PASS; dc50_err={dc50_err:.3f}; dmax_err_pp={dmax_err:.2f}")


def input_8_geometry_stress() -> None:
    output = run_shipped("ternary_geometry_screen.py")
    peg3 = "[*:1]CCOCCOCCOCC[*:2]"
    peg = linker_reach(peg3, n_confs=40, seed=20260923)
    require(peg["n_confs"] >= 20 and peg["min_A"] <= 9.0 <= peg["max_A"] + 2.0,
            f"PEG3 result implausible: {peg}")
    chain_max = []
    for n_carbons in range(1, 8):
        result = linker_reach(f"[*:1]{'C' * n_carbons}[*:2]", n_confs=30, seed=20260923)
        bound = _theoretical_max_reach_alkyl(result["n_bonds"])
        require(result["max_A"] <= bound + 0.5,
                f"C{n_carbons} exceeds all-trans bound")
        chain_max.append(result["max_A"])
    require(chain_max == sorted(chain_max), f"non-monotonic alkyl reach: {chain_max}")
    require("Monotonic-reach and theoretical-bound checks: PASS" in output,
            "shipped geometry demo regression missing")
    print(f"INPUT8 geometry stress: PEG3={peg}; C1..C7_max={[round(x, 2) for x in chain_max]}")


def input_9_narrow_hook_caveat() -> None:
    output = run_shipped("cooperativity_dc50.py")
    truth = dict(dmax=65.0, dc50=120.0, hill=1.8, hook_k=2500.0, hook_hill=1.1)
    conc = np.logspace(0, 4.3, 18)
    observed = _hook_curve(conc, **truth)
    hook = detect_hook(conc, observed)
    fit = fit_dc50(conc, observed, peak_idx=hook["peak_idx"])
    require(hook["hook_effect"], "narrow hook not detected")
    require(fit["plateau_reached"] is False and fit["caveat"], "narrow hook lacks lower-bound caveat")
    require(fit["dmax_fit"] < truth["dmax"], "synthetic narrow hook must demonstrate underestimation")
    require("Narrow-hook caveat check: PASS" in output, "shipped narrow-hook regression missing")
    print(f"INPUT9 narrow hook: dmax_fit={fit['dmax_fit']:.2f}; caveat={fit['caveat']}")


def input_10_fresh_monotonic() -> None:
    truth = dict(dmax=72.0, dc50=35.0, hill=1.5)
    conc = np.logspace(-1, 4, 30)
    observed = _hill(conc, **truth)
    hook = detect_hook(conc, observed)
    fit = fit_dc50(conc, observed)
    require(hook["hook_effect"] is False, "monotonic curve falsely flagged as hook")
    require(fit["plateau_reached"] is None and fit["caveat"] is None, "unneeded hook metadata")
    require(abs(fit["dc50_fit"] - truth["dc50"]) / truth["dc50"] < 0.01, "DC50 recovery failure")
    require(abs(fit["dmax_fit"] - truth["dmax"]) < 0.01, "Dmax recovery failure")
    print(f"INPUT10 NEW monotonic: dc50={fit['dc50_fit']:.3f}; dmax={fit['dmax_fit']:.3f}; no_hook=PASS")


def input_11_fresh_library() -> None:
    library = {
        "rigid_phenyl": "[*:1]c1ccccc1[*:2]",
        "peg2": "[*:1]CCOCCOCC[*:2]",
    }
    results = screen_linker_library(6.0, tolerance_A=0.5, linkers=library)
    require(set(results) == set(library), "library names not preserved")
    for name, result in results.items():
        require(result["n_confs"] > 0 and math.isfinite(result["mean_A"]),
                f"{name} lacks valid sampled conformers")
        expected = (result["min_A"] - 0.5) <= 6.0 <= (result["max_A"] + 0.5)
        require(result["feasible"] == expected, f"{name} feasibility predicate mismatch")
    require(results["peg2"]["max_A"] > results["rigid_phenyl"]["max_A"],
            f"unexpected reach ordering: {results}")
    print(f"INPUT11 NEW library: rigid={results['rigid_phenyl']}; peg2={results['peg2']}")


def main() -> None:
    input_1_canonical()
    input_3_attachment_edge()
    input_4_vhl_variant()
    input_5_well_separated_hook()
    input_8_geometry_stress()
    input_9_narrow_hook_caveat()
    input_10_fresh_monotonic()
    input_11_fresh_library()
    print("ALL EXECUTED PHASE2 ASSERTIONS PASSED")


if __name__ == "__main__":
    main()
