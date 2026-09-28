#!/usr/bin/env python3
"""Strict local validator for the schema-v4 re-audit report and evidence."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    report = json.loads((ROOT / "report.json").read_text(encoding="utf-8"))
    source = json.loads((ROOT / "source-identity.json").read_text(encoding="utf-8"))
    evidence = json.loads((ROOT / "evidence" / "reaudit-results.json").read_text(encoding="utf-8"))
    suite = json.loads((ROOT / "evidence" / "shipped-suite-summary.json").read_text(encoding="utf-8"))

    assert list(report) == ["meta", "veto_gates", "static_score", "dynamic_score", "final", "key_strengths", "recommendations"]
    assert set(report["veto_gates"]["skill_veto"]) == {"gate", "stability", "contract", "determinism", "security"}
    assert set(report["veto_gates"]["research_veto"]) == {"applicable", "gate", "scientific_integrity", "practice_boundaries", "methodological_ground", "code_usability"}
    category_keys = {"functional_suitability", "reliability", "performance_context", "agent_usability", "human_usability", "security", "maintainability", "agent_specific"}
    categories = report["static_score"]["categories"]
    assert set(categories) == category_keys
    assert report["static_score"]["subtotal"] == sum(item["score"] for item in categories.values())
    assert len(report["dynamic_score"]["inputs"]) == report["meta"]["n_inputs"] == 5
    passed = total = 0
    for index, item in enumerate(report["dynamic_score"]["inputs"], 1):
        assert item["index"] == index
        assert 3 <= len(item["assertions"]) <= 5
        assert item["basic"] + item["specialized"] == item["total"]
        item_passed = sum(assertion["result"] == "PASS" for assertion in item["assertions"])
        assert item_passed == item["assertions_passed"]
        assert len(item["assertions"]) == item["assertions_total"]
        passed += item_passed
        total += len(item["assertions"])
    dynamic = round(sum(item["total"] for item in report["dynamic_score"]["inputs"]) / 5, 1)
    assert dynamic == report["dynamic_score"]["execution_avg"]
    assert report["dynamic_score"]["assertion_pass_rate"] == {"passed": passed, "total": total}
    assert round(report["static_score"]["subtotal"] * 0.4, 1) == report["final"]["static_weighted"]
    assert round(dynamic * 0.6, 1) == report["final"]["dynamic_weighted"]
    assert round(report["final"]["static_weighted"] + report["final"]["dynamic_weighted"]) == report["final"]["score"]
    assert 2 <= len(report["key_strengths"]) <= 5
    assert report["recommendations"] == []
    assert report["final"] == {"static_weighted": 38.4, "dynamic_weighted": 57.7, "score": 96, "max": 100, "grade": "Production Ready", "grade_symbol": "⭐", "deployable": True, "veto_override": False}

    expected = "148b254a310719e781dacc9a782cd45f61e6cc8dd508124e1941d589458b47e1"
    assert evidence["identity_before"]["content_sha256"] == expected
    assert evidence["identity_after"]["content_sha256"] == expected
    assert evidence["identity_stable"] is True
    assert source["candidate"]["content_sha256"] == expected
    assert suite["returncode"] == 0
    assert evidence["ordinary_simplex"]["stages"]["final"]["records"] == 4
    assert evidence["ordinary_duplex"]["stages"]["final"]["records"] == 2
    assert evidence["second_duplex"]["stages"]["final"]["records"] == 2
    assert evidence["metachar_simplex"]["stages"]["final"]["records"] == 4
    for case in ("ordinary_simplex", "ordinary_duplex", "second_duplex", "metachar_simplex"):
        item = evidence[case]
        assert item["stages"]["extracted_umis"]["rx_records"] == 32
        assert item["stages"]["extracted_umis"]["za_records"] == 32
        assert item["stages"]["extracted_umis"]["zb_records"] == 32
        assert item["stages"]["filtered_queryname"]["sort_order"] == "queryname"
        assert item["stages"]["final"]["sort_order"] == "coordinate"
        assert item["index_present"] is True and item["quickcheck_returncode"] == 0
    assert evidence["metachar_shell_side_effect_absent"] is True
    assert evidence["static"]["shell_true_lines"] == [] and evidence["static"]["eval_exec"] == []
    assert evidence["qc"]["public_deterministic"] is True
    assert evidence["qc"]["flag_fixture"]["n"] == 1
    assert all(value["type"] in {"TypeError", "ValueError"} for value in evidence["qc"]["invalid_bounds"].values())
    assert source["audit"]["report_sha256"] == sha256(ROOT / "report.json")
    assert source["audit"]["viewer_sha256"] == sha256(ROOT / "viewer.md")
    assert source["audit"]["reaudit_results_sha256"] == sha256(ROOT / "evidence" / "reaudit-results.json")
    print(json.dumps({"schema": "PASS", "identity": expected, "score": 96, "assertions": f"{passed}/{total}", "suite_returncode": suite["returncode"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
