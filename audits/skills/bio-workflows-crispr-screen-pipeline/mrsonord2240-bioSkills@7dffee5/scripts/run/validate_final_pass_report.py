"""Validate the required final-pass JSON report invariants.

Usage: python validate_final_pass_report.py
"""
from __future__ import annotations

import json
from pathlib import Path


REPORT = Path(__file__).parents[1] / "eval_report_bio-workflows-crispr-screen-pipeline_result.json"


def main() -> None:
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    assert set(report) == {"meta", "veto_gates", "static_score", "dynamic_score", "final", "key_strengths", "recommendations"}
    meta = report["meta"]
    assert meta["auditor_independent"] is False
    assert meta["note"] == "final pass: fixed and audited under one brief, see CHECKPOINT.md"
    assert meta["n_inputs"] == len(report["dynamic_score"]["inputs"]) == 7
    static = report["static_score"]
    categories = static["categories"]
    required_categories = {"functional_suitability", "reliability", "performance_context", "agent_usability", "human_usability", "security", "maintainability", "agent_specific"}
    assert set(categories) == required_categories
    assert static["subtotal"] == sum(item["score"] for item in categories.values())
    inputs = report["dynamic_score"]["inputs"]
    for index, item in enumerate(inputs, start=1):
        assert item["index"] == index
        assert 3 <= len(item["assertions"]) <= 5
        assert item["assertions_total"] == len(item["assertions"])
        assert item["assertions_passed"] == sum(a["result"] == "PASS" for a in item["assertions"])
        assert item["basic"] + item["specialized"] == item["total"]
    dynamic = sum(item["total"] for item in inputs) / len(inputs)
    assert report["dynamic_score"]["execution_avg"] == round(dynamic, 1)
    final = report["final"]
    assert final["static_weighted"] == round(static["subtotal"] * 0.4, 1)
    assert final["dynamic_weighted"] == round(dynamic * 0.6, 1)
    assert final["score"] == round(final["static_weighted"] + final["dynamic_weighted"])
    assert final["grade"] == "Production Ready" and final["grade_symbol"] == "⭐"
    assert final["deployable"] is True and final["veto_override"] is False
    assert 2 <= len(report["key_strengths"]) <= 5
    assert report["recommendations"] == []
    print("final-pass report schema and arithmetic: PASS")


if __name__ == "__main__":
    main()
