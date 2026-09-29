#!/usr/bin/env python3
"""Strict local schema, arithmetic, and current readiness-floor check."""
import json
from pathlib import Path

root = Path(__file__).resolve().parent
r = json.loads((root / "report.json").read_text(encoding="utf-8"))
assert set(r) == {"meta", "veto_gates", "static_score", "dynamic_score", "final", "key_strengths", "recommendations"}
assert set(r["meta"]) == {"skill_name", "description", "evaluated_on", "evaluator_version", "category", "execution_mode", "complexity", "n_inputs"}
assert r["meta"]["n_inputs"] == len(r["dynamic_score"]["inputs"])
assert set(r["veto_gates"]) == {"skill_veto", "research_veto"}
assert set(r["veto_gates"]["skill_veto"]) == {"gate", "stability", "contract", "determinism", "security"}
assert set(r["veto_gates"]["research_veto"]) == {"applicable", "gate", "scientific_integrity", "practice_boundaries", "methodological_ground", "code_usability"}
assert set(r["static_score"]["categories"]) == {"functional_suitability", "reliability", "performance_context", "agent_usability", "human_usability", "security", "maintainability", "agent_specific"}
assert sum(v["score"] for v in r["static_score"]["categories"].values()) == r["static_score"]["subtotal"]
passed = total_assertions = 0
for index, item in enumerate(r["dynamic_score"]["inputs"], 1):
    assert item["index"] == index
    assert 3 <= len(item["assertions"]) <= 5
    assert item["basic"] + item["specialized"] == item["total"]
    assert len(item["assertions"]) == item["assertions_total"]
    count = sum(assertion["result"] == "PASS" for assertion in item["assertions"])
    assert count == item["assertions_passed"]
    assert item["status"] == "COMPLETED" and item["status_flag"] == "✅" and item["total"] >= 75
    passed += count
    total_assertions += len(item["assertions"])
avg = round(sum(x["total"] for x in r["dynamic_score"]["inputs"]) / len(r["dynamic_score"]["inputs"]), 1)
assert avg == r["dynamic_score"]["execution_avg"]
assert {"passed": passed, "total": total_assertions} == r["dynamic_score"]["assertion_pass_rate"]
f = r["final"]
assert f["static_weighted"] == round(r["static_score"]["subtotal"] * 0.4, 1)
assert f["dynamic_weighted"] == round(avg * 0.6, 1)
assert f["score"] == round(f["static_weighted"] + f["dynamic_weighted"])
assert r["veto_gates"]["skill_veto"]["gate"] == "PASS"
assert r["veto_gates"]["research_veto"]["gate"] == "PASS"
assert f["veto_override"] is False and f["deployable"] is True
l1 = sum(item["basic"] for item in r["dynamic_score"]["inputs"]) / len(r["dynamic_score"]["inputs"])
l2 = sum(item["specialized"] for item in r["dynamic_score"]["inputs"]) / len(r["dynamic_score"]["inputs"])
assert f["score"] >= 85 and r["static_score"]["subtotal"] >= 80 and avg >= 85
assert l1 >= 32 and l2 >= 48 and passed / total_assertions >= 0.90
assert not r["recommendations"]
print(json.dumps({
    "schema": "skill-auditor-report-v4.0",
    "valid": True,
    "inputs": len(r["dynamic_score"]["inputs"]),
    "assertions": f"{passed}/{total_assertions}",
    "static": r["static_score"]["subtotal"],
    "execution": avg,
    "layer1_average": l1,
    "layer2_average": l2,
    "final_score": f["score"],
    "readiness_floors_pass": True,
    "veto_override": False
}, indent=2))
