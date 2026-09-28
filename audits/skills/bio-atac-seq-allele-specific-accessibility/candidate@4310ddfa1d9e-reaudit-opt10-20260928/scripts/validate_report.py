#!/usr/bin/env python3
"""Validate the strict skill-auditor v4 report and local identity evidence."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def main() -> int:
    data = json.loads((ROOT / "report.json").read_text(encoding="utf-8"))
    identity = json.loads((ROOT / "source-identity.json").read_text(encoding="utf-8"))
    errors: list[str] = []
    require(
        set(data) == {"meta", "veto_gates", "static_score", "dynamic_score", "final", "key_strengths", "recommendations"},
        "top-level report keys", errors,
    )
    require(
        set(data["veto_gates"]["skill_veto"]) == {"gate", "stability", "contract", "determinism", "security"},
        "skill-veto keys", errors,
    )
    require(
        set(data["veto_gates"]["research_veto"]) == {"applicable", "gate", "scientific_integrity", "practice_boundaries", "methodological_ground", "code_usability"},
        "research-veto keys", errors,
    )
    category_keys = {"functional_suitability", "reliability", "performance_context", "agent_usability", "human_usability", "security", "maintainability", "agent_specific"}
    categories = data["static_score"]["categories"]
    require(set(categories) == category_keys, "static category keys", errors)
    require(all(set(item) == {"score", "max", "note"} for item in categories.values()), "static category shapes", errors)
    require(sum(item["score"] for item in categories.values()) == data["static_score"]["subtotal"], "static subtotal", errors)
    inputs = data["dynamic_score"]["inputs"]
    require(len(inputs) == data["meta"]["n_inputs"], "input cardinality", errors)
    passed = total = 0
    for item in inputs:
        assertions = item["assertions"]
        require(3 <= len(assertions) <= 5, f"input {item['index']} assertion cardinality", errors)
        actual = sum(assertion["result"] == "PASS" for assertion in assertions)
        require(actual == item["assertions_passed"], f"input {item['index']} pass count", errors)
        require(len(assertions) == item["assertions_total"], f"input {item['index']} total count", errors)
        require(item["basic"] + item["specialized"] == item["total"], f"input {item['index']} arithmetic", errors)
        require(all(set(assertion) == {"text", "result", "note"} for assertion in assertions), f"input {item['index']} assertion shape", errors)
        expected_flag = "❌" if item["status"] in {"PARTIAL", "ERROR"} else ("✅" if item["total"] >= 75 else "⚠️")
        require(item["status_flag"] == expected_flag, f"input {item['index']} status flag", errors)
        passed += actual
        total += len(assertions)
    execution_avg = round(sum(item["total"] for item in inputs) / len(inputs), 1)
    require(execution_avg == data["dynamic_score"]["execution_avg"], "execution average", errors)
    require(data["dynamic_score"]["assertion_pass_rate"] == {"passed": passed, "total": total}, "assertion aggregate", errors)
    static_weighted = round(data["static_score"]["subtotal"] * 0.4, 1)
    dynamic_weighted = round(execution_avg * 0.6, 1)
    require(data["final"]["static_weighted"] == static_weighted, "static weighted", errors)
    require(data["final"]["dynamic_weighted"] == dynamic_weighted, "dynamic weighted", errors)
    require(data["final"]["score"] == round(static_weighted + dynamic_weighted), "final rounded score", errors)
    require(data["veto_gates"]["research_veto"]["gate"] == "FAIL", "research veto gate", errors)
    require(data["final"]["veto_override"] is True and data["final"]["deployable"] is False, "veto override", errors)
    require(data["final"]["grade"] == "Reject" and data["final"]["grade_symbol"] == "❌", "forced grade", errors)
    require(2 <= len(data["key_strengths"]) <= 5, "key-strength cardinality", errors)
    ranks = {"P0": 0, "P1": 1, "P2": 2}
    priorities = [ranks[item["priority"]] for item in data["recommendations"]]
    require(priorities == sorted(priorities), "recommendation order", errors)
    for relative, expected in identity["durable_evidence"].items():
        path = ROOT / relative
        actual = hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else None
        require(actual == expected, f"durable evidence hash {relative}", errors)
    result = {
        "schema": "skill-auditor report schema v4.0",
        "valid": not errors,
        "errors": errors,
        "static_subtotal": data["static_score"]["subtotal"],
        "dynamic_average": execution_avg,
        "assertions": {"passed": passed, "total": total},
        "weighted": {"static": static_weighted, "dynamic": dynamic_weighted, "rounded_final": data["final"]["score"]},
        "research_veto": data["veto_gates"]["research_veto"]["gate"],
        "open_findings": [item["title"].split(":", 1)[0] for item in data["recommendations"]],
    }
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
