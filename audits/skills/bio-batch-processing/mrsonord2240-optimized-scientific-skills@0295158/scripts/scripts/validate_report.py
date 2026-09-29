#!/usr/bin/env python3
"""Validate the strict skill-auditor v4 report contract and arithmetic."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
report = json.loads((ROOT / "report.json").read_text(encoding="utf-8"))

assert set(report) == {
    "meta", "veto_gates", "static_score", "dynamic_score", "final",
    "key_strengths", "recommendations",
}
assert set(report["meta"]) == {
    "skill_name", "description", "evaluated_on", "evaluator_version",
    "category", "execution_mode", "complexity", "n_inputs",
}
assert report["meta"]["n_inputs"] == 5
assert report["meta"]["category"] == "Data Analysis"
assert report["meta"]["execution_mode"] == "D"

skill_veto = report["veto_gates"]["skill_veto"]
assert set(skill_veto) == {"gate", "stability", "contract", "determinism", "security"}
assert all(value == "PASS" for value in skill_veto.values())
research = report["veto_gates"]["research_veto"]
assert set(research) == {
    "applicable", "gate", "scientific_integrity", "practice_boundaries",
    "methodological_ground", "code_usability",
}
assert research["applicable"] is True and research["gate"] == "PASS"
for key in ("scientific_integrity", "practice_boundaries", "methodological_ground", "code_usability"):
    assert set(research[key]) == {"result", "detail"}
    assert research[key]["result"] == "PASS" and research[key]["detail"]

categories = report["static_score"]["categories"]
expected_categories = {
    "functional_suitability": 12,
    "reliability": 12,
    "performance_context": 8,
    "agent_usability": 16,
    "human_usability": 8,
    "security": 12,
    "maintainability": 12,
    "agent_specific": 20,
}
assert set(categories) == set(expected_categories)
for key, maximum in expected_categories.items():
    assert set(categories[key]) == {"score", "max", "note"}
    assert categories[key]["max"] == maximum
    assert 0 <= categories[key]["score"] <= maximum
    assert categories[key]["note"]
static_total = sum(item["score"] for item in categories.values())
assert static_total == report["static_score"]["subtotal"] == 97
assert report["static_score"]["max"] == 100

dynamic = report["dynamic_score"]
assert len(dynamic["inputs"]) == report["meta"]["n_inputs"]
passed = total = 0
totals = []
for position, item in enumerate(dynamic["inputs"], start=1):
    assert item["index"] == position
    assert item["status"] == "COMPLETED" and item["status_flag"] == "✅"
    assert 3 <= len(item["assertions"]) <= 5
    item_passed = sum(assertion["result"] == "PASS" for assertion in item["assertions"])
    assert all(set(assertion) == {"text", "result", "note"} for assertion in item["assertions"])
    assert all(assertion["result"] in {"PASS", "FAIL"} for assertion in item["assertions"])
    assert item_passed == item["assertions_passed"]
    assert len(item["assertions"]) == item["assertions_total"]
    assert item["basic"] + item["specialized"] == item["total"]
    passed += item_passed
    total += len(item["assertions"])
    totals.append(item["total"])
assert dynamic["assertion_pass_rate"] == {"passed": passed, "total": total} == {"passed": 25, "total": 25}
execution_avg = round(sum(totals) / len(totals), 1)
assert dynamic["execution_avg"] == execution_avg == 97.0

final = report["final"]
assert final["static_weighted"] == round(static_total * 0.4, 1) == 38.8
assert final["dynamic_weighted"] == round(execution_avg * 0.6, 1) == 58.2
assert final["score"] == round(final["static_weighted"] + final["dynamic_weighted"]) == 97
assert final["grade"] == "Production Ready" and final["grade_symbol"] == "⭐"
assert final["deployable"] is True and final["veto_override"] is False
assert 2 <= len(report["key_strengths"]) <= 5
assert [item["priority"] for item in report["recommendations"]] == ["P2"]
assert all(set(item) == {"priority", "title", "observed_in", "problem", "root_cause", "fix"} for item in report["recommendations"])

result = {
    "schema": "skill-auditor report_json_schema.md v4.0",
    "valid": True,
    "static_total": static_total,
    "execution_avg": execution_avg,
    "assertions": {"passed": passed, "total": total},
    "final_score": final["score"],
}
(ROOT / "evidence" / "schema-validation.json").write_text(
    json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
)
(ROOT / "evidence" / "assertions.json").write_text(
    json.dumps(
        {
            "candidate_content_sha256": "f5558565b7f1068f76afdfaecee4a560c24917c037658c45b54f554d7ab23afd",
            "passed": passed,
            "total": total,
            "inputs": [
                {"index": item["index"], "assertions": item["assertions"]}
                for item in dynamic["inputs"]
            ],
        },
        indent=2,
        sort_keys=True,
    ) + "\n",
    encoding="utf-8",
)
print(json.dumps(result, sort_keys=True))
