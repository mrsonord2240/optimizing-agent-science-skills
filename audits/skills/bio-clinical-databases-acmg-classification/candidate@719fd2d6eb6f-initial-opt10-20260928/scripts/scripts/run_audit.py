#!/usr/bin/env python3
"""Independent bounded execution for the ACMG classification skill audit."""

from __future__ import annotations

import contextlib
import hashlib
import importlib.util
import io
import json
import os
import pathlib
import subprocess
import sys
from typing import Any

import requests


ROOT = pathlib.Path(os.environ["ACMG_AUDIT_ROOT"])
CANDIDATE = pathlib.Path(os.environ["ACMG_CANDIDATE"])
OUTPUT = ROOT / "evidence" / "execution.json"


def load_module():
    path = CANDIDATE / "scripts" / "acmg_classify.py"
    spec = importlib.util.spec_from_file_location("candidate_acmg_classify", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def manifest_identity() -> dict[str, Any]:
    rows = []
    for path in sorted(
        (p for p in CANDIDATE.rglob("*") if p.is_file()),
        key=lambda p: p.relative_to(CANDIDATE).as_posix(),
    ):
        rel = path.relative_to(CANDIDATE).as_posix()
        data = path.read_bytes()
        rows.append(f"{rel}\t{len(data)}\t{hashlib.sha256(data).hexdigest()}")
    manifest = "\n".join(rows).encode("utf-8")
    return {
        "algorithm": "sha256-manifest-v1",
        "file_count": len(rows),
        "manifest_bytes": len(manifest),
        "digest": hashlib.sha256(manifest).hexdigest(),
        "rows": rows,
    }


def response_probe(url: str, **kwargs: Any) -> dict[str, Any]:
    try:
        response = requests.get(url, timeout=30, **kwargs)
        return {
            "url": response.url,
            "status": response.status_code,
            "content_type": response.headers.get("content-type"),
            "body_excerpt": response.text[:500],
        }
    except Exception as exc:  # evidence must retain the access failure
        return {"url": url, "error": f"{type(exc).__name__}: {exc}"}


def candidate_genebe(module) -> dict[str, Any]:
    try:
        value = module.genebe_api("NM_000546.6:c.215C>G")
        return {"status": "success", "value_type": type(value).__name__}
    except Exception as exc:
        response = getattr(exc, "response", None)
        return {
            "status": "error",
            "error": f"{type(exc).__name__}: {exc}",
            "http_status": getattr(response, "status_code", None),
            "body_excerpt": getattr(response, "text", "")[:500] if response is not None else "",
            "url": getattr(response, "url", None),
        }


def main() -> None:
    module = load_module()
    demo = subprocess.run(
        [sys.executable, "-B", str(CANDIDATE / "scripts" / "acmg_classify.py")],
        text=True,
        capture_output=True,
        timeout=30,
        check=False,
    )

    expected_oddspath = {
        "350.000001": "PS3_VeryStrong",
        "350.0": "PS3",
        "18.700001": "PS3",
        "18.7": "PS3_Moderate",
        "4.300001": "PS3_Moderate",
        "4.3": "PS3_Supporting",
        "2.100001": "PS3_Supporting",
        "2.1": None,
        "0.48": None,
        "0.479999": "BS3_Supporting",
        "0.23": "BS3_Supporting",
        "0.229999": "BS3_Moderate",
        "0.053": "BS3_Moderate",
        "0.052999": "BS3",
    }
    oddspath = []
    for text_value, expected in expected_oddspath.items():
        value = float(text_value)
        actual = module.ps3_oddspath(value)
        oddspath.append(
            {"value": value, "expected": expected, "actual": actual, "match": actual == expected}
        )

    pvs1_cases = [
        {
            "label": "nonsense_nmd_relevant_transcript",
            "args": ["nonsense", True, 0.01, False, True],
            "expected": "PVS1_VeryStrong",
        },
        {
            "label": "nonsense_nmd_irrelevant_transcript",
            "args": ["nonsense", True, 0.01, False, False],
            "expected": None,
        },
        {
            "label": "nonsense_escape_exactly_ten_percent",
            "args": ["nonsense", False, 0.10, False, True],
            "expected": "PVS1_Moderate",
        },
        {
            "label": "nonsense_escape_over_ten_percent",
            "args": ["nonsense", False, 0.100001, False, True],
            "expected": "PVS1_Strong",
        },
        {
            "label": "splice_escape_without_consequence_context",
            "args": ["splice_donor", False, 0.0, False, True],
            "expected": "requires_transcript_consequence_review",
        },
    ]
    for case in pvs1_cases:
        case["actual"] = module.pvs1_decision_tree(*case["args"])
        case["match"] = case["actual"] == case["expected"]

    alpha_expected = {
        "0.070": "BP4_Strong",
        "0.100": "BP4_Supporting",
        "0.169": "BP4_Supporting",
        "0.170": None,
        "0.200": None,
        "0.700": None,
        "0.791": None,
        "0.792": "PP3_Supporting",
        "0.906": "PP3_Moderate",
        "0.972": "PP3_Strong_3pt",
        "0.990": "PP3_Strong",
    }
    alpha = []
    for text_value, expected in alpha_expected.items():
        value = float(text_value)
        actual = module.alphamissense_supporting_only(value)
        alpha.append(
            {"value": value, "expected": expected, "actual": actual, "match": actual == expected}
        )

    score_boundaries = []
    criteria_for_score = {
        10: ["PVS1_VeryStrong", "PM2_Supporting", "PP3_Supporting"],
        9: ["PVS1_VeryStrong", "PM2_Supporting"],
        6: ["PS3", "PM2_Supporting", "PP3_Supporting"],
        5: ["PS3", "PP3_Supporting"],
        0: [],
        -1: ["BP1"],
        -6: ["BS1", "BP1", "BP2"],
        -7: ["BS1", "BP1", "BP2", "BP3"],
    }
    for points, criteria in criteria_for_score.items():
        result = module.tavtigian_classify(criteria)
        score_boundaries.append({"target_points": points, "criteria": criteria, "result": result})

    validation_probes = []
    for label, fn, args in [
        ("unknown_criterion", module.tavtigian_classify, [["NOT_A_CRITERION"]]),
        ("duplicate_criterion", module.tavtigian_classify, [["PS3", "PS3"]]),
        ("negative_alpha", module.alphamissense_supporting_only, [-0.1]),
        ("alpha_over_one", module.alphamissense_supporting_only, [1.1]),
        ("negative_oddspath", module.ps3_oddspath, [-1.0]),
        ("zero_penetrance", module.whiffin_max_credible_af, [0.001, 1.0, 1.0, 0.0]),
        ("negative_prevalence", module.whiffin_max_credible_af, [-0.1]),
        ("nonnumeric_score", module.revel_pp3_bp4, ["0.9"]),
    ]:
        try:
            value = fn(*args)
            validation_probes.append({"label": label, "accepted": True, "result": value})
        except Exception as exc:
            validation_probes.append(
                {"label": label, "accepted": False, "error": f"{type(exc).__name__}: {exc}"}
            )

    germline = module.classify_with_subsumption(
        ["PVS1_VeryStrong", "PM2_Supporting", "PP3_Strong"]
    )
    somatic = {
        "tier_i_a": module.cancer_amp_tier(1, False, True, "clinical"),
        "tier_i_b": module.cancer_amp_tier(4, True, True, "clinical"),
        "tier_ii_c": module.cancer_amp_tier(2, False, False, "clinical"),
        "tier_ii_d": module.cancer_amp_tier(4, False, False, "preclinical"),
        "tier_iii_iv": module.cancer_amp_tier(4, False, True, "clinical"),
        "invalid_negative_level": module.cancer_amp_tier(-1, False, False, "clinical"),
    }

    result = {
        "runtime": {
            "python": sys.version,
            "requests": requests.__version__,
            "pandas": module.pd.__version__,
        },
        "candidate_identity": manifest_identity(),
        "input_1_canonical_demo": {
            "returncode": demo.returncode,
            "stdout": demo.stdout,
            "stderr": demo.stderr,
        },
        "input_2_pvs1": pvs1_cases,
        "input_3_oddspath": oddspath,
        "input_4_tavtigian": {
            "boundaries": score_boundaries,
            "subsumption": germline,
            "unknown": module.tavtigian_classify(["NOT_A_CRITERION"]),
            "duplicate": module.tavtigian_classify(["PS3", "PS3"]),
        },
        "input_5_alphamissense": alpha,
        "input_6_framework_separation_and_validation": {
            "germline": germline,
            "somatic": somatic,
            "validation_probes": validation_probes,
        },
        "input_7_current_interfaces": {
            "candidate_genebe": candidate_genebe(module),
            "current_genebe_control": response_probe(
                "https://api.genebe.net/cloud/api-public/v1/variant",
                params={"chr": "17", "pos": 28364411, "ref": "C", "alt": "A", "genome": "hg38"},
            ),
            "candidate_cspec_route": response_probe(
                "https://cspec.genome.network/cspec/ui/svi/all"
            ),
            "current_cspec_service": response_probe(
                "https://cspec.genome.network/cspec/srvc"
            ),
            "current_cspec_gene_versions": response_probe(
                "https://cspec.genome.network/cspec/Gene/id/GATM/SequenceVariantInterpretation/version"
            ),
        },
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(OUTPUT),
        "identity": result["candidate_identity"]["digest"],
        "oddspath_matches": sum(row["match"] for row in oddspath),
        "oddspath_total": len(oddspath),
        "pvs1_matches": sum(row["match"] for row in pvs1_cases),
        "pvs1_total": len(pvs1_cases),
        "alpha_matches": sum(row["match"] for row in alpha),
        "alpha_total": len(alpha),
    }, sort_keys=True))


if __name__ == "__main__":
    main()
