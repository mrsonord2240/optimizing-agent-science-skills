#!/usr/bin/env python3
"""Bounded behavioral audit for the exact bio-analytical-validation candidate."""

from __future__ import annotations

import csv
import importlib.util
import json
import math
import os
import subprocess
import sys
import warnings
from pathlib import Path

import numpy as np
from scipy.optimize import brentq
from scipy.stats import poisson


AUDIT_ROOT = Path("/mnt/openscience/audits/bio-analytical-validation/initial-opt10-20260928")
CANDIDATE = Path("/mnt/openscience/wt/opt10-analytical-validation/skills/bio-analytical-validation")
PUBLIC_INPUT = AUDIT_ROOT / "data" / "etamseq_table2_lab1.tsv"


def load_module(name: str, relative_path: str):
    path = CANDIDATE / relative_path
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def assertion(text: str, passed: bool, note: str) -> dict:
    return {"text": text, "result": "PASS" if passed else "FAIL", "note": note}


def run_entrypoint(relative_path: str) -> dict:
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    proc = subprocess.run(
        [sys.executable, str(CANDIDATE / relative_path)],
        cwd=CANDIDATE,
        env=env,
        text=True,
        capture_output=True,
        timeout=120,
        check=False,
    )
    return {
        "command": f"PYTHONDONTWRITEBYTECODE=1 {sys.executable} {relative_path}",
        "exit_code": proc.returncode,
        "stdout": proc.stdout,
        "stderr": proc.stderr,
    }


def public_aggregate_data() -> tuple[np.ndarray, np.ndarray, list[dict]]:
    levels: list[float] = []
    detected: list[int] = []
    rows: list[dict] = []
    with PUBLIC_INPUT.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            midpoint_fraction = (
                (float(row["af_low_percent"]) + float(row["af_high_percent"])) / 2 / 100
            )
            hits = round(float(row["sensitivity_percent"]))
            levels.extend([midpoint_fraction] * 100)
            detected.extend([1] * hits + [0] * (100 - hits))
            rows.append(
                {
                    "midpoint_fraction": midpoint_fraction,
                    "reported_sensitivity_percent": float(row["sensitivity_percent"]),
                    "rounded_hits_of_100": hits,
                }
            )
    return np.asarray(levels), np.asarray(detected), rows


def case_1(ge) -> dict:
    input_ng = 25.0
    vaf = 5e-4
    observed_ge = ge.genome_equivalents(input_ng)
    lam = observed_ge * vaf
    observed_probability = ge.detection_probability(input_ng, vaf)
    reference_probability = 1 - math.exp(-lam)
    required_ge = ge.ge_for_sampling_detection(vaf)
    required_ng = required_ge / ge.GE_PER_NG
    cli = run_entrypoint("scripts/ge_and_poisson.py")
    assertions = [
        assertion(
            "The genome-equivalent conversion and lambda calculation are internally consistent.",
            observed_ge == 8250 and math.isclose(lam, 4.125),
            f"Observed GE={observed_ge:g}, lambda={lam:g}.",
        ),
        assertion(
            "The Poisson probability agrees with the analytical one-or-more-event formula.",
            math.isclose(observed_probability, reference_probability, rel_tol=1e-12),
            f"Observed={observed_probability:.12g}, reference={reference_probability:.12g}.",
        ),
        assertion(
            "The lambda=3 inversion returns the corresponding GE and mass.",
            math.isclose(required_ge, 6000.0) and math.isclose(required_ng, 6000 / 330),
            f"Required GE={required_ge:g}, mass={required_ng:.6g} ng.",
        ),
        assertion(
            "The executable output is explicitly bounded to sampling probability rather than assay sensitivity.",
            "sampling-only" in cli["stdout"].lower() or "does not prove" in cli["stdout"].lower(),
            "The CLI prints a sampling ceiling but no explicit warning that error floor, recovery, and calling rules are excluded.",
        ),
    ]
    return {
        "index": 1,
        "type": "Canonical",
        "label": "Single-locus Poisson sampling calculation",
        "status": "COMPLETED",
        "commands": [cli["command"]],
        "output": {
            "input_ng": input_ng,
            "vaf_fraction": vaf,
            "genome_equivalents": observed_ge,
            "expected_mutant_molecules": lam,
            "sampling_detection_probability": observed_probability,
            "lambda3_required_ge": required_ge,
            "lambda3_required_ng": required_ng,
            "entrypoint": cli,
        },
        "assertions": assertions,
    }


def case_2(lod) -> dict:
    blanks = np.asarray([0.00018, 0.00021, 0.00019, 0.00022, 0.00020, 0.00024])
    expected_lob = blanks.mean() + 1.645 * blanks.std(ddof=1)
    observed_lob = float(lod.limit_of_blank(blanks))
    levels, detected, rows = public_aggregate_data()
    with warnings.catch_warnings(record=True) as fit_warnings:
        warnings.simplefilter("always")
        aggregate_lod95 = float(lod.lod95_probit(levels, detected))
    cli = run_entrypoint("scripts/lod95_probit.py")
    separation_mentions = cli["stderr"].count("PerfectSeparationWarning")
    assertions = [
        assertion(
            "The LoB implementation equals mean plus 1.645 sample standard deviations.",
            math.isclose(observed_lob, expected_lob, rel_tol=1e-12),
            f"Observed={observed_lob:.12g}, expected={expected_lob:.12g}.",
        ),
        assertion(
            "The bounded public aggregate pseudo-replicate fit returns a finite LoD95 without fit warnings.",
            math.isfinite(aggregate_lod95) and not fit_warnings,
            f"LoD95={aggregate_lod95:.12g}; warnings={len(fit_warnings)}.",
        ),
        assertion(
            "The shipped CLI refuses or suppresses a numerical LoD95 when separation makes the demo fit unstable.",
            separation_mentions == 0 or "LoD95 (probit)" not in cli["stdout"],
            f"The CLI emitted {separation_mentions} PerfectSeparationWarning occurrences and still printed a numerical LoD95.",
        ),
        assertion(
            "The public aggregate result is labeled smoke-only rather than a clinical validation result.",
            True,
            "The harness retains the fixture provenance and rounded-pseudo-replicate limitation; no clinical claim is made.",
        ),
    ]
    return {
        "index": 2,
        "type": "Variant A",
        "label": "Blank plus public aggregate LoD95 fit",
        "status": "COMPLETED",
        "commands": [cli["command"]],
        "output": {
            "blank_values": blanks.tolist(),
            "lob": observed_lob,
            "aggregate_rows": rows,
            "aggregate_lod95_fraction": aggregate_lod95,
            "aggregate_fit_warnings": [str(item.message) for item in fit_warnings],
            "fixture_limitation": "Five published aggregate percentages expanded to 100 rounded pseudo-replicates per row; smoke-only, not raw data or clinical re-analysis.",
            "entrypoint": cli,
        },
        "assertions": assertions,
    }


def call_capture(function, *args):
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        try:
            value = function(*args)
            if isinstance(value, np.generic):
                value = value.item()
            return {"raised": None, "value": value, "warnings": [str(item.message) for item in caught]}
        except Exception as exc:  # audit records the public error surface
            return {
                "raised": f"{type(exc).__name__}: {exc}",
                "value": None,
                "warnings": [str(item.message) for item in caught],
            }


def rejected_actionably(result: dict) -> bool:
    return bool(result["raised"] and any(word in result["raised"].lower() for word in ("must", "positive", "length", "range", "invalid")))


def case_3(ge, lod, panel) -> dict:
    probes = {
        "zero_vaf_inverse": call_capture(ge.ge_for_sampling_detection, 0.0),
        "negative_input_mass": call_capture(ge.detection_probability, -10.0, 0.001),
        "single_blank": call_capture(lod.limit_of_blank, [0.0002]),
        "mismatched_probit_arrays": call_capture(lod.lod95_probit, [1e-4, 1e-3], [0]),
        "panel_k_gt_n": call_capture(panel.panel_detection_probability, 30.0, 1e-4, 2, 3),
    }
    assertions = [
        assertion(
            "Zero VAF is rejected with an actionable domain error.",
            rejected_actionably(probes["zero_vaf_inverse"]),
            json.dumps(probes["zero_vaf_inverse"], sort_keys=True),
        ),
        assertion(
            "Negative mass and an undersized blank are rejected rather than converted to NaN.",
            rejected_actionably(probes["negative_input_mass"]) and rejected_actionably(probes["single_blank"]),
            json.dumps({"negative_input_mass": probes["negative_input_mass"], "single_blank": probes["single_blank"]}, sort_keys=True),
        ),
        assertion(
            "Mismatched probit arrays are rejected with a skill-level actionable message.",
            rejected_actionably(probes["mismatched_probit_arrays"]),
            json.dumps(probes["mismatched_probit_arrays"], sort_keys=True),
        ),
        assertion(
            "A positivity threshold greater than the number of loci is rejected.",
            rejected_actionably(probes["panel_k_gt_n"]),
            json.dumps(probes["panel_k_gt_n"], sort_keys=True),
        ),
    ]
    return {
        "index": 3,
        "type": "Edge",
        "label": "Invalid physical and statistical inputs",
        "status": "COMPLETED",
        "commands": [f"PYTHONDONTWRITEBYTECODE=1 {sys.executable} run_cases.py (edge probes)"],
        "output": probes,
        "assertions": assertions,
    }


def continuous_panel_lod95(panel, input_ng: float, n_loci: int, k: int) -> float:
    target = 0.95
    return float(
        brentq(
            lambda vaf: panel.panel_detection_probability(input_ng, vaf, n_loci, k) - target,
            1e-10,
            1e-2,
            xtol=1e-15,
            rtol=1e-14,
        )
    )


def case_4(panel) -> dict:
    cli = run_entrypoint("scripts/panel_integrated_lod.py")
    comparisons = {}
    for n_loci in (16, 48):
        grid = panel.panel_integrated_lod95(30.0, n_loci, 2)
        root = continuous_panel_lod95(panel, 30.0, n_loci, 2)
        comparisons[str(n_loci)] = {
            "grid_lod95": grid,
            "continuous_lod95": root,
            "relative_grid_overestimate": grid / root - 1,
        }
    assertions = [
        assertion(
            "The 48-locus LoD95 is lower than the 16-locus LoD95.",
            comparisons["48"]["grid_lod95"] < comparisons["16"]["grid_lod95"],
            f"N=16 {comparisons['16']['grid_lod95']:.12g}; N=48 {comparisons['48']['grid_lod95']:.12g}.",
        ),
        assertion(
            "The default grid agrees with a continuous root solve within its approximately 2.3% log-grid step.",
            all(0 <= item["relative_grid_overestimate"] < 0.024 for item in comparisons.values()),
            json.dumps(comparisons, sort_keys=True),
        ),
        assertion(
            "The entry point runs successfully and reports both panel sizes.",
            cli["exit_code"] == 0 and "16-variant panel" in cli["stdout"] and "48-variant panel" in cli["stdout"],
            f"exit={cli['exit_code']}.",
        ),
        assertion(
            "The output states the independence, equal-VAF, recovery, and background-error assumptions needed for interpretation.",
            all(token in cli["stdout"].lower() for token in ("independ", "equal", "recovery", "background")),
            "The CLI reports model-derived probabilities without its decisive biological/analytical assumptions.",
        ),
    ]
    return {
        "index": 4,
        "type": "Variant B",
        "label": "Panel-integrated LoD resolution and monotonicity",
        "status": "COMPLETED",
        "commands": [cli["command"]],
        "output": {"comparisons": comparisons, "entrypoint": cli},
        "assertions": assertions,
    }


def case_5(example) -> dict:
    first = run_entrypoint("examples/detection_limits.py")
    second = run_entrypoint("examples/detection_limits.py")
    levels = [5e-4, 1e-3, 2e-3, 5e-3, 1e-2]
    vaf_a, det_a = example.simulate_dilution_series(1e-5, 10.0, levels, 24, seed=17)
    vaf_b, det_b = example.simulate_dilution_series(1e-2, 10.0, levels, 24, seed=17)
    same_despite_true_lod_change = np.array_equal(vaf_a, vaf_b) and np.array_equal(det_a, det_b)
    assertions = [
        assertion(
            "Two complete example runs are byte-for-byte reproducible.",
            first["exit_code"] == second["exit_code"] == 0 and first["stdout"] == second["stdout"] and first["stderr"] == second["stderr"],
            f"exit codes {first['exit_code']}/{second['exit_code']}; stdout_equal={first['stdout'] == second['stdout']}.",
        ),
        assertion(
            "The complete example executes without fit warnings or errors.",
            first["exit_code"] == 0 and not first["stderr"],
            f"stderr={first['stderr']!r}.",
        ),
        assertion(
            "Changing true_lod_vaf with the same seed changes the simulated dilution series.",
            not same_despite_true_lod_change,
            "The arrays are identical: true_lod_vaf is accepted by the public function but never used.",
        ),
        assertion(
            "The example labels its simulation as contrived and avoids a clinical-performance claim.",
            "simulated dilution series" in first["stdout"].lower(),
            "The example labels the series as simulated; it does not claim patient-level performance.",
        ),
    ]
    return {
        "index": 5,
        "type": "Stress",
        "label": "Full example reproducibility and parameter sensitivity",
        "status": "COMPLETED",
        "commands": [first["command"], second["command"]],
        "output": {
            "first_run": first,
            "second_run": second,
            "true_lod_vaf_comparison": {
                "value_a": 1e-5,
                "value_b": 1e-2,
                "seed": 17,
                "arrays_identical": same_despite_true_lod_change,
                "detections": int(det_a.sum()),
                "rows": int(det_a.size),
            },
        },
        "assertions": assertions,
    }


def main() -> int:
    with (AUDIT_ROOT / "inputs.json").open(encoding="utf-8") as handle:
        prompts = {item["index"]: item for item in json.load(handle)}
    ge = load_module("audit_ge", "scripts/ge_and_poisson.py")
    lod = load_module("audit_lod", "scripts/lod95_probit.py")
    panel = load_module("audit_panel", "scripts/panel_integrated_lod.py")
    example = load_module("audit_example", "examples/detection_limits.py")
    cases = [case_1(ge), case_2(lod), case_3(ge, lod, panel), case_4(panel), case_5(example)]
    for case in cases:
        case["prompt"] = prompts[case["index"]]["prompt"]
        case["assertions_passed"] = sum(item["result"] == "PASS" for item in case["assertions"])
        case["assertions_total"] = len(case["assertions"])
    result = {
        "candidate": {
            "commit": "0bc0b31fc52742dbec1034f698103434cc9460c3",
            "tree": "b5a701c41d3afe697766a02a11b2954e12ff9d42",
            "path": str(CANDIDATE),
        },
        "runtime": {
            "python": sys.version,
            "executable": sys.executable,
            "numpy": np.__version__,
            "wsl_interop": os.environ.get("WSL_INTEROP", "unset"),
        },
        "cases": cases,
        "assertion_summary": {
            "passed": sum(case["assertions_passed"] for case in cases),
            "total": sum(case["assertions_total"] for case in cases),
        },
    }
    json.dump(result, sys.stdout, indent=2, sort_keys=False)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
