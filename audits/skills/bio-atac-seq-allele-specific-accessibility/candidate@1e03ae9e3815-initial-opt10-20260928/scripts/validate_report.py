#!/usr/bin/env python3
"""Strict local checks for the skill-auditor v4 report contract."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
REPORT = ROOT / "report.json"


def require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def main() -> int:
    data = json.loads(REPORT.read_text(encoding="utf-8"))
    errors: list[str] = []
    require(
        set(data) == {
            "meta", "veto_gates", "static_score", "dynamic_score",
            "final", "key_strengths", "recommendations",
        },
        "top-level keys differ from schema", errors,
    )
    require(
        set(data["veto_gates"]["skill_veto"])
        == {"gate", "stability", "contract", "determinism", "security"},
        "skill-veto keys differ from schema", errors,
    )
    require(
        set(data["veto_gates"]["research_veto"])
        == {"applicable", "gate", "scientific_integrity", "practice_boundaries", "methodological_ground", "code_usability"},
        "research-veto keys differ from schema", errors,
    )
    category_keys = {
        "functional_suitability", "reliability", "performance_context",
        "agent_usability", "human_usability", "security",
        "maintainability", "agent_specific",
    }
    categories = data["static_score"]["categories"]
    require(set(categories) == category_keys, "static category keys differ from schema", errors)
    require(all(set(v) == {"score", "max", "note"} for v in categories.values()), "static category object shape differs from schema", errors)
    require(sum(v["score"] for v in categories.values()) == data["static_score"]["subtotal"], "static subtotal arithmetic mismatch", errors)
    inputs = data["dynamic_score"]["inputs"]
    require(len(inputs) == data["meta"]["n_inputs"], "dynamic input count mismatch", errors)
    passed = 0
    assertion_total = 0
    for item in inputs:
        assertions = item["assertions"]
        require(3 <= len(assertions) <= 5, f"input {item['index']} assertion count", errors)
        actual_passed = sum(a["result"] == "PASS" for a in assertions)
        require(actual_passed == item["assertions_passed"], f"input {item['index']} pass count", errors)
        require(len(assertions) == item["assertions_total"], f"input {item['index']} assertion total", errors)
        require(item["basic"] + item["specialized"] == item["total"], f"input {item['index']} score addition", errors)
        require(all(set(a) == {"text", "result", "note"} for a in assertions), f"input {item['index']} assertion shape", errors)
        if item["status"] == "COMPLETED" and item["total"] < 75:
            require(item["status_flag"] == "⚠️", f"input {item['index']} status flag", errors)
        if item["status"] in {"PARTIAL", "ERROR"}:
            require(item["status_flag"] == "❌", f"input {item['index']} status flag", errors)
        passed += actual_passed
        assertion_total += len(assertions)
    execution_avg = round(sum(item["total"] for item in inputs) / len(inputs), 1)
    require(execution_avg == data["dynamic_score"]["execution_avg"], "execution average mismatch", errors)
    require(data["dynamic_score"]["assertion_pass_rate"] == {"passed": passed, "total": assertion_total}, "assertion aggregate mismatch", errors)
    static_weighted = round(data["static_score"]["subtotal"] * 0.4, 1)
    dynamic_weighted = round(data["dynamic_score"]["execution_avg"] * 0.6, 1)
    final_score = round(static_weighted + dynamic_weighted)
    require(static_weighted == data["final"]["static_weighted"], "static weight mismatch", errors)
    require(dynamic_weighted == data["final"]["dynamic_weighted"], "dynamic weight mismatch", errors)
    require(final_score == data["final"]["score"], "final score mismatch", errors)
    require(2 <= len(data["key_strengths"]) <= 5, "key-strength cardinality", errors)
    ranks = {"P0": 0, "P1": 1, "P2": 2}
    priorities = [ranks[item["priority"]] for item in data["recommendations"]]
    require(priorities == sorted(priorities), "recommendation order", errors)
    any_gate_failed = any(g["gate"] == "FAIL" for g in (data["veto_gates"]["skill_veto"], data["veto_gates"]["research_veto"]))
    require(data["final"]["veto_override"] == any_gate_failed, "veto override mismatch", errors)
    require(not data["final"]["deployable"], "reject report must not be deployable", errors)
    require(data["final"]["grade"] == "Reject" and data["final"]["grade_symbol"] == "❌", "grade mismatch", errors)
    result = {
        "schema": "skill-auditor report schema v4.0",
        "valid": not errors,
        "errors": errors,
        "static_subtotal": data["static_score"]["subtotal"],
        "dynamic_average": execution_avg,
        "assertions": {"passed": passed, "total": assertion_total},
        "weighted": {"static": static_weighted, "dynamic": dynamic_weighted, "rounded_final": final_score},
    }
    print(json.dumps(result, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
