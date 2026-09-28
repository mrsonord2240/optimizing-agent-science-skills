#!/usr/bin/env python3
"""Strict checks for the skill-auditor v4 report contract and arithmetic."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def main() -> int:
    report = json.loads((ROOT / "report.json").read_text(encoding="utf-8"))
    errors: list[str] = []

    def require(condition: bool, message: str) -> None:
        if not condition:
            errors.append(message)

    require(set(report) == {"meta", "veto_gates", "static_score", "dynamic_score", "final", "key_strengths", "recommendations"}, "top-level keys")
    require(set(report["veto_gates"]["skill_veto"]) == {"gate", "stability", "contract", "determinism", "security"}, "skill veto keys")
    require(set(report["veto_gates"]["research_veto"]) == {"applicable", "gate", "scientific_integrity", "practice_boundaries", "methodological_ground", "code_usability"}, "research veto keys")
    category_keys = {"functional_suitability", "reliability", "performance_context", "agent_usability", "human_usability", "security", "maintainability", "agent_specific"}
    categories = report["static_score"]["categories"]
    require(set(categories) == category_keys, "static category keys")
    require(all(set(value) == {"score", "max", "note"} for value in categories.values()), "static category shape")
    require(sum(value["score"] for value in categories.values()) == report["static_score"]["subtotal"], "static subtotal")
    inputs = report["dynamic_score"]["inputs"]
    require(len(inputs) == report["meta"]["n_inputs"], "dynamic input count")
    passed = total = 0
    for item in inputs:
        assertions = item["assertions"]
        require(3 <= len(assertions) <= 5, f"input {item['index']} assertion cardinality")
        item_passed = sum(assertion["result"] == "PASS" for assertion in assertions)
        require(item_passed == item["assertions_passed"], f"input {item['index']} pass count")
        require(len(assertions) == item["assertions_total"], f"input {item['index']} assertion total")
        require(item["basic"] + item["specialized"] == item["total"], f"input {item['index']} score")
        passed += item_passed
        total += len(assertions)
    dynamic = round(sum(item["total"] for item in inputs) / len(inputs), 1)
    require(dynamic == report["dynamic_score"]["execution_avg"], "dynamic average")
    require(report["dynamic_score"]["assertion_pass_rate"] == {"passed": passed, "total": total}, "assertion aggregate")
    static_weighted = round(report["static_score"]["subtotal"] * 0.4, 1)
    dynamic_weighted = round(dynamic * 0.6, 1)
    require(report["final"]["static_weighted"] == static_weighted, "static weighting")
    require(report["final"]["dynamic_weighted"] == dynamic_weighted, "dynamic weighting")
    require(report["final"]["score"] == round(static_weighted + dynamic_weighted), "final score")
    require(2 <= len(report["key_strengths"]) <= 5, "key strength cardinality")
    ranks = {"P0": 0, "P1": 1, "P2": 2}
    priorities = [ranks[item["priority"]] for item in report["recommendations"]]
    require(priorities == sorted(priorities), "recommendation order")
    require(report["final"]["veto_override"] is True and report["final"]["deployable"] is False, "veto override")
    result = {
        "schema": "skill-auditor report schema v4.0",
        "valid": not errors,
        "errors": errors,
        "static_subtotal": report["static_score"]["subtotal"],
        "dynamic_average": dynamic,
        "assertions": {"passed": passed, "total": total},
        "weighted": {"static": static_weighted, "dynamic": dynamic_weighted, "rounded_final": round(static_weighted + dynamic_weighted)}
    }
    (ROOT / "evidence" / "schema-validation.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
