#!/usr/bin/env python3
"""Validate the skill-auditor v4 report contract and arithmetic."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
report = json.loads((ROOT / "report.json").read_text(encoding="utf-8"))
errors: list[str] = []


def check(condition: bool, message: str) -> None:
    if not condition:
        errors.append(message)


check(
    set(report) == {
        "meta",
        "veto_gates",
        "static_score",
        "dynamic_score",
        "final",
        "key_strengths",
        "recommendations",
    },
    "top-level keys differ from schema",
)
meta = report["meta"]
inputs = report["dynamic_score"]["inputs"]
check(len(inputs) == meta["n_inputs"] == 5, "input count mismatch")
category_keys = {
    "functional_suitability",
    "reliability",
    "performance_context",
    "agent_usability",
    "human_usability",
    "security",
    "maintainability",
    "agent_specific",
}
categories = report["static_score"]["categories"]
check(set(categories) == category_keys, "static category keys mismatch")
static_sum = sum(value["score"] for value in categories.values())
check(static_sum == report["static_score"]["subtotal"], "static subtotal mismatch")

assertion_passed = 0
assertion_total = 0
totals = []
allowed_types = {
    "Canonical",
    "Variant A",
    "Variant B",
    "Edge",
    "Stress",
    "Scope Boundary",
    "Adversarial",
}
for expected_index, item in enumerate(inputs, start=1):
    check(item["index"] == expected_index, f"input {expected_index} index mismatch")
    check(item["type"] in allowed_types, f"input {expected_index} type invalid")
    check(3 <= len(item["assertions"]) <= 5, f"input {expected_index} assertion cardinality")
    passed = sum(assertion["result"] == "PASS" for assertion in item["assertions"])
    check(passed == item["assertions_passed"], f"input {expected_index} passed mismatch")
    check(len(item["assertions"]) == item["assertions_total"], f"input {expected_index} total mismatch")
    check(item["basic"] + item["specialized"] == item["total"], f"input {expected_index} score mismatch")
    assertion_passed += passed
    assertion_total += len(item["assertions"])
    totals.append(item["total"])

dynamic = round(sum(totals) / len(totals), 1)
check(dynamic == report["dynamic_score"]["execution_avg"], "dynamic average mismatch")
check(
    {"passed": assertion_passed, "total": assertion_total}
    == report["dynamic_score"]["assertion_pass_rate"],
    "assertion aggregate mismatch",
)
static_weighted = round(report["static_score"]["subtotal"] * 0.4, 1)
dynamic_weighted = round(dynamic * 0.6, 1)
check(static_weighted == report["final"]["static_weighted"], "static weighted mismatch")
check(dynamic_weighted == report["final"]["dynamic_weighted"], "dynamic weighted mismatch")
check(round(static_weighted + dynamic_weighted) == report["final"]["score"], "final score mismatch")
check(report["veto_gates"]["research_veto"]["gate"] == "FAIL", "research veto gate mismatch")
check(report["final"]["veto_override"] is True, "veto override mismatch")
check(report["final"]["deployable"] is False, "deployability mismatch")
check(2 <= len(report["key_strengths"]) <= 5, "key strengths cardinality")
priority_order = {"P0": 0, "P1": 1, "P2": 2}
priorities = [priority_order[item["priority"]] for item in report["recommendations"]]
check(priorities == sorted(priorities), "recommendations not priority-sorted")

result = {
    "schema_reference": "skill-auditor/references/report_json_schema.md version 4.0",
    "valid": not errors,
    "errors": errors,
    "verified": {
        "static_subtotal": static_sum,
        "dynamic_average": dynamic,
        "assertions": {"passed": assertion_passed, "total": assertion_total},
        "weighted_static": static_weighted,
        "weighted_dynamic": dynamic_weighted,
        "rounded_final": round(static_weighted + dynamic_weighted),
    },
}
(ROOT / "evidence" / "schema-validation.json").write_text(
    json.dumps(result, indent=2) + "\n", encoding="utf-8"
)
(ROOT / "evidence" / "final-assertions.json").write_text(
    json.dumps(
        {str(item["index"]): item["assertions"] for item in inputs},
        indent=2,
    )
    + "\n",
    encoding="utf-8",
)
print(json.dumps(result))
raise SystemExit(0 if not errors else 1)
