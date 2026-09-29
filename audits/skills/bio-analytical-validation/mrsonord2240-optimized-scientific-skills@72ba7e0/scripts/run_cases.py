#!/usr/bin/env python3
"""Independent exhaustive re-audit for bio-analytical-validation.

The script is deliberately identity-bound and writes no candidate files.
"""

from __future__ import annotations

import csv
import hashlib
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
from scipy.stats import norm, poisson


AUDIT_ROOT = Path("/mnt/openscience/audits/bio-analytical-validation/reaudit-opt10-20260928")
CANDIDATE = Path("/mnt/openscience/wt/opt10-analytical-validation/skills/bio-analytical-validation")
PUBLIC_INPUT = AUDIT_ROOT / "data" / "etamseq_table2_lab1.tsv"
EXPECTED_IDENTITY = "bd66239b9133b70a7522d0d99e3bc4ebbed1b8c1291c74fad26367dfa339b2ab"
MANIFEST_ORDER = (
    "examples/detection_limits.py",
    "scripts/ge_and_poisson.py",
    "scripts/lod95_probit.py",
    "scripts/panel_integrated_lod.py",
    "SKILL.md",
    "usage-guide.md",
)


def candidate_identity() -> tuple[str, list[dict]]:
    manifest = []
    lines = []
    for relative in MANIFEST_ORDER:
        raw = (CANDIDATE / relative).read_bytes()
        sha256 = hashlib.sha256(raw).hexdigest()
        git_blob = hashlib.sha1(f"blob {len(raw)}\0".encode() + raw).hexdigest()
        manifest.append({"path": relative, "sha256": sha256, "git_blob": git_blob, "bytes": len(raw)})
        lines.append(f"{relative}\t{sha256}\t{git_blob}\t{len(raw)}\n")
    identity = hashlib.sha256("".join(lines).encode("utf-8")).hexdigest()
    return identity, manifest


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
    env["PYTHONWARNINGS"] = "error"
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
        "command": f"PYTHONDONTWRITEBYTECODE=1 PYTHONWARNINGS=error {sys.executable} {relative_path}",
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
            midpoint = (float(row["af_low_percent"]) + float(row["af_high_percent"])) / 200.0
            hits = round(float(row["sensitivity_percent"]))
            levels.extend([midpoint] * 100)
            detected.extend([1] * hits + [0] * (100 - hits))
            rows.append({"midpoint_vaf": midpoint, "rounded_hits_of_100": hits})
    return np.asarray(levels), np.asarray(detected), rows


def replicated_series(levels: list[float], positives: list[int], replicates: int) -> tuple[np.ndarray, np.ndarray]:
    x = np.repeat(np.asarray(levels, dtype=float), replicates)
    y = np.concatenate(
        [np.r_[np.ones(count, dtype=int), np.zeros(replicates - count, dtype=int)] for count in positives]
    )
    return x, y


def capture(function, *args, **kwargs) -> dict:
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        try:
            value = function(*args, **kwargs)
            if isinstance(value, np.generic):
                value = value.item()
            return {"raised": None, "value": value, "warnings": [str(item.message) for item in caught]}
        except Exception as exc:  # the public error surface is the evidence
            return {
                "raised": f"{type(exc).__name__}: {exc}",
                "value": None,
                "warnings": [str(item.message) for item in caught],
            }


def case_1(ge) -> dict:
    cli = run_entrypoint("scripts/ge_and_poisson.py")
    observed_ge = ge.genome_equivalents(25.0)
    observed_probability = ge.sampling_probability(25.0, 5e-4)
    expected_probability = float(poisson.sf(0, observed_ge * 5e-4))
    fresh_probability = ge.sampling_probability(12.5, 2e-4, min_mutant_molecules=2)
    fresh_expected = float(poisson.sf(1, 12.5 * (1000 / 3.3) * 2e-4))
    ge95 = ge.ge_for_sampling_probability(1e-4)
    fresh_ge = ge.ge_for_sampling_probability(7.5e-4, target_probability=0.80, min_mutant_molecules=2)
    fresh_lambda = brentq(lambda lam: poisson.sf(1, lam) - 0.80, np.finfo(float).tiny, 20.0)
    output = {
        "canonical": {
            "input_ng": 25.0,
            "vaf": 5e-4,
            "genome_equivalents": observed_ge,
            "expected_mutant_molecules": observed_ge * 5e-4,
            "sampling_probability": observed_probability,
            "ge_for_95_percent_at_1e_4": ge95,
        },
        "fresh_k2": {"observed": fresh_probability, "reference": fresh_expected},
        "fresh_inverse_k2": {"observed_ge": fresh_ge, "reference_ge": fresh_lambda / 7.5e-4},
        "custom_convention_ge": ge.genome_equivalents(1.0, ge_per_ng=330.0),
        "entrypoint": cli,
    }
    assertions = [
        assertion(
            "The default genome-equivalent conversion exactly follows 1,000 pg divided by 3.3 pg and remains explicitly overridable.",
            math.isclose(observed_ge, 25 * 1000 / 3.3, rel_tol=1e-14)
            and math.isclose(output["custom_convention_ge"], 330.0),
            f"25 ng={observed_ge:.12g} GE; alternate 1 ng={output['custom_convention_ge']:.12g} GE.",
        ),
        assertion(
            "Canonical and fresh k=2 sampling probabilities agree with independent SciPy Poisson tails.",
            math.isclose(observed_probability, expected_probability, rel_tol=1e-14)
            and math.isclose(fresh_probability, fresh_expected, rel_tol=1e-14),
            f"canonical={observed_probability:.12g}; fresh={fresh_probability:.12g}.",
        ),
        assertion(
            "The 95% one-template inversion equals -log(0.05)/VAF rather than a rounded lambda=3 shortcut.",
            math.isclose(ge95, -math.log(0.05) / 1e-4, rel_tol=1e-12),
            f"observed={ge95:.12g} GE; reference={-math.log(0.05) / 1e-4:.12g} GE.",
        ),
        assertion(
            "A fresh k=2, 80% inversion agrees with an independent continuous root.",
            math.isclose(fresh_ge, fresh_lambda / 7.5e-4, rel_tol=1e-11),
            f"observed={fresh_ge:.12g} GE; reference={fresh_lambda / 7.5e-4:.12g} GE.",
        ),
        assertion(
            "The command-line surface labels results as sampling-only and excludes recovery, background errors, and false positives.",
            cli["exit_code"] == 0
            and not cli["stderr"]
            and all(term in cli["stdout"].lower() for term in ("sampling only", "recovery", "background errors", "false positives")),
            f"exit={cli['exit_code']}; stderr={cli['stderr']!r}.",
        ),
    ]
    return case_record(1, "Canonical", "Sampling-only molecule-count calculation", output, assertions, [cli["command"]])


def fit_checks(lod, levels: list[float], positives: list[int], replicates: int) -> dict:
    x, y = replicated_series(levels, positives, replicates)
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        result = lod.lod95_probit(x, y)
    lower, upper = result["lod95_confidence_interval"]
    reconstructed = float(norm.cdf(result["intercept"] + result["slope"] * math.log10(result["lod95_vaf"])))
    return {
        "result": result,
        "warnings": [str(item.message) for item in caught],
        "ci_ordered": 0 < lower < result["lod95_vaf"] < upper,
        "reconstructed_probability": reconstructed,
    }


def case_2(lod) -> dict:
    cli = run_entrypoint("scripts/lod95_probit.py")
    blanks = np.asarray([0.00018, 0.00021, 0.00019, 0.00022, 0.00020, 0.00024])
    observed_lob = lod.limit_of_blank(blanks)
    expected_lob = float(blanks.mean() + 1.645 * blanks.std(ddof=1))
    aggregate_x, aggregate_y, rows = public_aggregate_data()
    with warnings.catch_warnings(record=True) as aggregate_warnings:
        warnings.simplefilter("always")
        aggregate = lod.lod95_probit(aggregate_x, aggregate_y)
    fresh_a = fit_checks(lod, [1e-4, 2e-4, 5e-4, 1e-3, 2e-3, 5e-3], [1, 4, 15, 31, 44, 49], 50)
    fresh_b = fit_checks(lod, [2e-4, 6e-4, 1.2e-3, 2.5e-3, 6e-3], [0, 7, 18, 32, 39], 40)
    separated_x, separated_y = replicated_series([1e-4, 1e-3, 1e-2], [0, 0, 20], 20)
    separated = capture(lod.lod95_probit, separated_x, separated_y)
    nonbracket_x, nonbracket_y = replicated_series([1e-4, 1e-3, 1e-2], [0, 5, 18], 20)
    nonbracket = capture(lod.lod95_probit, nonbracket_x, nonbracket_y)
    output = {
        "lob": {"observed": observed_lob, "reference": expected_lob},
        "public_aggregate": {
            "rows": rows,
            "result": aggregate,
            "warnings": [str(item.message) for item in aggregate_warnings],
            "limitation": "Published aggregate percentages rounded to pseudo-replicates for smoke testing only; not raw data or clinical re-analysis.",
        },
        "fresh_fit_a": fresh_a,
        "fresh_fit_b": fresh_b,
        "separated": separated,
        "nonbracketing": nonbracket,
        "entrypoint": cli,
    }
    fit_ok = lambda item: (
        not item["warnings"]
        and item["result"]["converged"]
        and item["result"]["slope"] > 0
        and item["result"]["brackets_0_95"]
        and item["ci_ordered"]
        and math.isclose(item["reconstructed_probability"], 0.95, rel_tol=1e-12)
    )
    assertions = [
        assertion(
            "The Gaussian-shortcut LoB equals mean plus 1.645 sample standard deviations on a fresh blank fixture.",
            math.isclose(observed_lob, expected_lob, rel_tol=1e-14),
            f"observed={observed_lob:.12g}; expected={expected_lob:.12g}.",
        ),
        assertion(
            "The inherited public aggregate smoke case returns an identified result with ordered CI and no warning.",
            not aggregate_warnings
            and aggregate["converged"]
            and aggregate["slope"] > 0
            and 0 < aggregate["lod95_confidence_interval"][0] < aggregate["lod95_vaf"] < aggregate["lod95_confidence_interval"][1],
            f"LoD95={aggregate['lod95_vaf']:.12g}; CI={aggregate['lod95_confidence_interval']}; warnings={len(aggregate_warnings)}.",
        ),
        assertion(
            "Both fresh replicated fits converge with positive slope, ordered inverse-prediction CI, correct 95% inversion, and no warning.",
            fit_ok(fresh_a) and fit_ok(fresh_b),
            f"fresh A={fresh_a['result']['lod95_vaf']:.12g}; fresh B={fresh_b['result']['lod95_vaf']:.12g}.",
        ),
        assertion(
            "Separated and non-bracketing dilution series are refused with stable domain errors.",
            separated["raised"] is not None
            and "separated or unidentified" in separated["raised"]
            and nonbracket["raised"] is not None
            and "must bracket 0.95" in nonbracket["raised"],
            json.dumps({"separated": separated, "nonbracketing": nonbracket}, sort_keys=True),
        ),
        assertion(
            "The command-line probit demo is warning-free and reports a confidence interval, convergence, slope, sample size, levels, and target bracketing.",
            cli["exit_code"] == 0
            and not cli["stderr"]
            and all(term in cli["stdout"].lower() for term in ("95% wald ci", "converged=true", "slope=", "n=", "levels=", "brackets_0.95=true")),
            f"exit={cli['exit_code']}; stderr={cli['stderr']!r}.",
        ),
    ]
    return case_record(2, "Variant A", "Replicated LoB and LoD95 fits", output, assertions, [cli["command"]])


def case_3(ge, lod, panel, example) -> dict:
    series_x, series_y = replicated_series([1e-4, 1e-3, 1e-2], [0, 2, 3], 3)
    probes = {
        "zero_vaf": (capture(ge.sampling_probability, 10.0, 0.0), "vaf must be greater than 0.0"),
        "negative_mass": (capture(ge.genome_equivalents, -1.0), "input_ng must be greater than 0.0"),
        "nonfinite_mass": (capture(ge.genome_equivalents, np.inf), "input_ng must be a finite real number"),
        "boolean_mass": (capture(ge.genome_equivalents, True), "input_ng must be a finite real number"),
        "invalid_k": (capture(ge.sampling_probability, 10.0, 1e-3, 0), "min_mutant_molecules must be an integer of at least 1"),
        "target_one": (capture(ge.ge_for_sampling_probability, 1e-3, 1.0), "target_probability must be less than 1.0"),
        "blank_count": (capture(lod.limit_of_blank, [0.1]), "at least 2 replicates"),
        "blank_shape": (capture(lod.limit_of_blank, [[0.0, 0.1]]), "one-dimensional"),
        "probit_length": (capture(lod.lod95_probit, series_x, series_y[:-1]), "same length"),
        "probit_binary": (capture(lod.lod95_probit, series_x, np.where(np.arange(9) == 8, 0.5, series_y)), "binary outcomes"),
        "probit_replicates": (capture(lod.lod95_probit, [1e-4, 1e-4, 1e-3, 1e-3, 1e-2, 1e-2], [0, 0, 0, 1, 1, 1]), "at least 3 replicate"),
        "confidence_level": (capture(lod.lod95_probit, series_x, series_y, confidence_level=1.0), "strictly between 0 and 1"),
        "k_gt_n": (capture(panel.sampling_only_panel_probability, 30.0, 1e-4, 2, 3), "must not exceed n_loci"),
        "grid_shape": (capture(panel.theoretical_sampling_vaf95_lower_bound, 30.0, 16, grid=[[1e-5, 1e-4]]), "one-dimensional"),
        "grid_order": (capture(panel.theoretical_sampling_vaf95_lower_bound, 30.0, 16, grid=[1e-4, 1e-5]), "strictly increasing"),
        "grid_ceiling": (capture(panel.theoretical_sampling_vaf95_lower_bound, 30.0, 16, grid=[1e-8, 2e-8]), "does not reach target_probability"),
        "simulation_levels": (capture(example.simulate_dilution_series, 1e-3, [1e-4, 1e-3], 10), "at least 3 VAF values"),
        "simulation_replicates": (capture(example.simulate_dilution_series, 1e-3, [1e-4, 1e-3, 1e-2], 2), "integer of at least 3"),
    }
    results = {name: value for name, (value, _) in probes.items()}
    pass_map = {
        name: bool(value["raised"] and value["raised"].startswith("ValueError:") and fragment in value["raised"] and not value["warnings"])
        for name, (value, fragment) in probes.items()
    }
    groups = [
        ("finite/range/type", ["zero_vaf", "negative_mass", "nonfinite_mass", "boolean_mass", "invalid_k", "target_one"]),
        ("blank/shape", ["blank_count", "blank_shape"]),
        ("probit contract", ["probit_length", "probit_binary", "probit_replicates", "confidence_level"]),
        ("panel/grid", ["k_gt_n", "grid_shape", "grid_order", "grid_ceiling"]),
        ("simulation", ["simulation_levels", "simulation_replicates"]),
    ]
    assertions = [
        assertion(
            f"All {label} invalid probes stop with the documented stable ValueError and no warning.",
            all(pass_map[name] for name in names),
            ", ".join(f"{name}={'PASS' if pass_map[name] else 'FAIL'}" for name in names),
        )
        for label, names in groups
    ]
    return case_record(
        3,
        "Edge",
        "Physical, shape, and fit-domain validation",
        {"probes": results, "pass_map": pass_map},
        assertions,
        [f"PYTHONDONTWRITEBYTECODE=1 {sys.executable} run_cases.py (18 invalid probes)"],
    )


def continuous_panel_root(panel, input_ng: float, n_loci: int, k: int, target: float = 0.95) -> float:
    return float(
        brentq(
            lambda vaf: panel.sampling_only_panel_probability(input_ng, vaf, n_loci, k) - target,
            1e-12,
            1.0,
            xtol=1e-15,
            rtol=1e-14,
        )
    )


def case_4(panel) -> dict:
    cli = run_entrypoint("scripts/panel_integrated_lod.py")
    scenarios = [
        {"name": "inherited_n16", "input_ng": 30.0, "n_loci": 16, "k": 2, "grid": None},
        {"name": "inherited_n48", "input_ng": 30.0, "n_loci": 48, "k": 2, "grid": None},
        {"name": "fresh_k1", "input_ng": 15.0, "n_loci": 12, "k": 1, "grid": np.logspace(-7, -2, 2000)},
        {"name": "fresh_k3", "input_ng": 40.0, "n_loci": 30, "k": 3, "grid": np.logspace(-7, -2, 2000)},
    ]
    results = {}
    for scenario in scenarios:
        result = panel.theoretical_sampling_vaf95_lower_bound(
            scenario["input_ng"], scenario["n_loci"], scenario["k"], grid=scenario["grid"]
        )
        root = continuous_panel_root(panel, scenario["input_ng"], scenario["n_loci"], scenario["k"])
        results[scenario["name"]] = {
            "result": result,
            "continuous_root": root,
            "relative_grid_overestimate": result["vaf_lower_bound"] / root - 1,
        }
    p16 = panel.sampling_only_panel_probability(30.0, 1e-4, 16, 2)
    p48 = panel.sampling_only_panel_probability(30.0, 1e-4, 48, 2)
    retired = {
        "panel_integrated_lod95": hasattr(panel, "panel_integrated_lod95"),
        "panel_detection_probability": hasattr(panel, "panel_detection_probability"),
    }
    required_assumptions = {
        "equal VAF at every tracked locus",
        "independent locus sampling",
        "perfect molecular recovery and detection of every present mutant template",
        "no consensus-depth failures, background errors, false positives, or empirical calling effects",
    }
    assertions = [
        assertion(
            "The inherited 48-locus threshold is lower than the 16-locus threshold and its fixed-VAF probability is higher.",
            results["inherited_n48"]["result"]["vaf_lower_bound"] < results["inherited_n16"]["result"]["vaf_lower_bound"]
            and p48 > p16,
            f"bounds={results['inherited_n16']['result']['vaf_lower_bound']:.12g}/{results['inherited_n48']['result']['vaf_lower_bound']:.12g}; probabilities={p16:.12g}/{p48:.12g}.",
        ),
        assertion(
            "Inherited default-grid thresholds agree with independent roots within one log-grid step.",
            all(0 <= results[name]["relative_grid_overestimate"] < 0.024 for name in ("inherited_n16", "inherited_n48")),
            json.dumps({name: results[name]["relative_grid_overestimate"] for name in ("inherited_n16", "inherited_n48")}, sort_keys=True),
        ),
        assertion(
            "Both fresh k-of-N scenarios agree with independent roots within their finer grid step.",
            all(0 <= results[name]["relative_grid_overestimate"] < 0.006 for name in ("fresh_k1", "fresh_k3")),
            json.dumps({name: results[name]["relative_grid_overestimate"] for name in ("fresh_k1", "fresh_k3")}, sort_keys=True),
        ),
        assertion(
            "Every structured result carries all four assumptions and explicitly denies achieved-assay-LoD95 interpretation; misleading legacy APIs are absent.",
            all(set(item["result"]["assumptions"]) == required_assumptions and "not an achieved assay LoD95" in item["result"]["interpretation"] for item in results.values())
            and not any(retired.values()),
            f"retired APIs={retired}.",
        ),
        assertion(
            "The panel command-line surface is warning-free and states sampling-only status plus equal-VAF, independence, recovery, background, and non-assay-LoD boundaries.",
            cli["exit_code"] == 0
            and not cli["stderr"]
            and all(term in cli["stdout"].lower() for term in ("sampling only", "equal vaf", "independent", "recovery", "background errors", "not assay lod95")),
            f"exit={cli['exit_code']}; stderr={cli['stderr']!r}.",
        ),
    ]
    return case_record(
        4,
        "Variant B",
        "Theoretical multi-locus sampling bounds",
        {"scenarios": results, "fixed_vaf_probabilities": {"n16": p16, "n48": p48}, "retired_apis": retired, "entrypoint": cli},
        assertions,
        [cli["command"]],
    )


def case_5(example) -> dict:
    first = run_entrypoint("examples/detection_limits.py")
    second = run_entrypoint("examples/detection_limits.py")
    levels = np.asarray([2e-4, 5e-4, 1e-3, 2e-3, 5e-3, 1e-2])
    vaf_a, det_a = example.simulate_dilution_series(1e-3, levels, 400, seed=991, probit_slope=2.0)
    vaf_a_repeat, det_a_repeat = example.simulate_dilution_series(1e-3, levels, 400, seed=991, probit_slope=2.0)
    vaf_b, det_b = example.simulate_dilution_series(5e-3, levels, 400, seed=991, probit_slope=2.0)
    _, det_slope = example.simulate_dilution_series(1e-3, levels, 400, seed=991, probit_slope=0.8)
    at_true = example.simulate_dilution_series(2e-3, [1e-3, 2e-3, 4e-3], 4000, seed=2027, probit_slope=2.0)[1]
    at_true_rate = float(at_true.reshape(3, 4000)[1].mean())
    output = {
        "entrypoint_first": first,
        "entrypoint_second": second,
        "same_seed_replay": bool(np.array_equal(vaf_a, vaf_a_repeat) and np.array_equal(det_a, det_a_repeat)),
        "true_lod_change_count": int(np.count_nonzero(det_a != det_b)),
        "positives_true_lod_1e_3": int(det_a.sum()),
        "positives_true_lod_5e_3": int(det_b.sum()),
        "slope_change_count": int(np.count_nonzero(det_a != det_slope)),
        "calibration_rate_at_true_lod": at_true_rate,
    }
    assertions = [
        assertion(
            "Two full worked-example runs are byte-for-byte deterministic and warning-free.",
            first["exit_code"] == second["exit_code"] == 0
            and first["stdout"] == second["stdout"]
            and first["stderr"] == second["stderr"] == "",
            f"exit={first['exit_code']}/{second['exit_code']}; stdout_equal={first['stdout'] == second['stdout']}.",
        ),
        assertion(
            "An identical seed and identical inputs reproduce the exact VAF and detection arrays.",
            output["same_seed_replay"],
            f"same_seed_replay={output['same_seed_replay']}.",
        ),
        assertion(
            "Fresh changes to true_lod_vaf and probit_slope materially change outcomes in the documented direction/model.",
            np.array_equal(vaf_a, vaf_b)
            and output["true_lod_change_count"] > 0
            and output["positives_true_lod_1e_3"] > output["positives_true_lod_5e_3"]
            and output["slope_change_count"] > 0,
            f"true-LoD changed={output['true_lod_change_count']}; positives={output['positives_true_lod_1e_3']}/{output['positives_true_lod_5e_3']}; slope changed={output['slope_change_count']}.",
        ),
        assertion(
            "The named true_lod_vaf is empirically calibrated near 95% in a fresh 4,000-replicate sample.",
            abs(at_true_rate - 0.95) < 0.02,
            f"observed rate={at_true_rate:.6f} at true_lod_vaf.",
        ),
        assertion(
            "The full example explicitly labels all sampling and simulation outputs as theoretical or contrived teaching results, not validation evidence.",
            all(term in first["stdout"].lower() for term in ("sampling only", "not an achieved assay lod", "not panel lod95", "contrived probit teaching model", "not validation evidence")),
            f"exit={first['exit_code']}; stderr={first['stderr']!r}.",
        ),
    ]
    return case_record(
        5,
        "Stress",
        "Simulation determinism, calibration, and sensitivity",
        output,
        assertions,
        [first["command"], second["command"]],
    )


def case_record(index: int, kind: str, label: str, output: dict, assertions: list[dict], commands: list[str]) -> dict:
    passed = sum(item["result"] == "PASS" for item in assertions)
    return {
        "index": index,
        "type": kind,
        "label": label,
        "status": "COMPLETED" if passed == len(assertions) else "PARTIAL",
        "commands": commands,
        "output": output,
        "assertions": assertions,
        "assertions_passed": passed,
        "assertions_total": len(assertions),
    }


def main() -> int:
    identity, manifest = candidate_identity()
    if identity != EXPECTED_IDENTITY:
        raise RuntimeError(f"Candidate identity drift: expected {EXPECTED_IDENTITY}, observed {identity}")
    with (AUDIT_ROOT / "inputs.json").open(encoding="utf-8") as handle:
        prompts = {item["index"]: item["prompt"] for item in json.load(handle)}
    ge = load_module("reaudit_ge", "scripts/ge_and_poisson.py")
    lod = load_module("reaudit_lod", "scripts/lod95_probit.py")
    panel = load_module("reaudit_panel", "scripts/panel_integrated_lod.py")
    example = load_module("reaudit_example", "examples/detection_limits.py")
    cases = [case_1(ge), case_2(lod), case_3(ge, lod, panel, example), case_4(panel), case_5(example)]
    for case in cases:
        case["prompt"] = prompts[case["index"]]
    result = {
        "auditor": {
            "phase": "independent-reaudit",
            "performed_initial_audit": False,
            "performed_fix": False,
            "performed_tooling_delta": False,
        },
        "candidate": {
            "path": str(CANDIDATE),
            "head": "0bc0b31fc52742dbec1034f698103434cc9460c3",
            "identity_algorithm": "SHA-256 of UTF-8 lines path<TAB>sha256<TAB>git_blob<TAB>bytes<LF>, in the listed order",
            "identity": identity,
            "manifest": manifest,
        },
        "runtime": {
            "python": sys.version.split()[0],
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
    rendered = json.dumps(result, indent=2, sort_keys=False) + "\n"
    evidence_dir = AUDIT_ROOT / "evidence"
    evidence_dir.mkdir(parents=True, exist_ok=True)
    (evidence_dir / "execution-summary.json").write_text(rendered, encoding="utf-8", newline="\n")
    print(
        json.dumps(
            {
                "candidate_identity": identity,
                "assertion_summary": result["assertion_summary"],
                "evidence": str(evidence_dir / "execution-summary.json"),
            },
            sort_keys=True,
        )
    )
    return 0 if result["assertion_summary"]["passed"] == result["assertion_summary"]["total"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
