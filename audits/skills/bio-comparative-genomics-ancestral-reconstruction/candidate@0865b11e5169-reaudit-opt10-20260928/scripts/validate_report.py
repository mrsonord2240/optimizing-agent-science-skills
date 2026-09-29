#!/usr/bin/env python3
"""Strict structural and arithmetic validation for the saved auditor v4 report."""
import json
from pathlib import Path

root = Path(__file__).resolve().parent
r = json.loads((root / "report.json").read_text(encoding="utf-8"))
assert set(r) == {"meta", "veto_gates", "static_score", "dynamic_score", "final", "key_strengths", "recommendations"}
assert r["meta"]["n_inputs"] == 7
assert set(r["meta"]) == {"skill_name", "description", "evaluated_on", "evaluator_version", "category", "execution_mode", "complexity", "n_inputs"}
assert set(r["veto_gates"]) == {"skill_veto", "research_veto"}
assert set(r["veto_gates"]["skill_veto"]) == {"gate", "stability", "contract", "determinism", "security"}
assert set(r["veto_gates"]["research_veto"]) == {"applicable", "gate", "scientific_integrity", "practice_boundaries", "methodological_ground", "code_usability"}
assert set(r["static_score"]["categories"]) == {"functional_suitability", "reliability", "performance_context", "agent_usability", "human_usability", "security", "maintainability", "agent_specific"}
assert sum(v["score"] for v in r["static_score"]["categories"].values()) == r["static_score"]["subtotal"]
inputs = r["dynamic_score"]["inputs"]
assert len(inputs) == r["meta"]["n_inputs"] == 7
passed = total_assertions = 0
for i, item in enumerate(inputs, 1):
    assert item["index"] == i
    assert set(item["assertions"][0]) == {"text", "result", "note"}
    assert 3 <= len(item["assertions"]) <= 5
    p = sum(a["result"] == "PASS" for a in item["assertions"])
    assert p == item["assertions_passed"] and len(item["assertions"]) == item["assertions_total"]
    assert item["basic"] + item["specialized"] == item["total"]
    assert 0 <= item["basic"] <= 40 and 0 <= item["specialized"] <= 60
    assert item["status_flag"] in {"✅", "⚠️", "❌"}
    assert (item["status_flag"] == "❌") == (item["status"] in {"PARTIAL", "ERROR"})
    passed += p
    total_assertions += len(item["assertions"])
avg = round(sum(x["total"] for x in inputs) / len(inputs), 1)
assert avg == r["dynamic_score"]["execution_avg"]
assert {"passed": passed, "total": total_assertions} == r["dynamic_score"]["assertion_pass_rate"]
f = r["final"]
assert f["static_weighted"] == round(r["static_score"]["subtotal"] * .4, 1)
assert f["dynamic_weighted"] == round(avg * .6, 1)
assert f["score"] == round(f["static_weighted"] + f["dynamic_weighted"])
veto = r["veto_gates"]["skill_veto"]["gate"] == "FAIL" or r["veto_gates"]["research_veto"]["gate"] == "FAIL"
assert f["veto_override"] == veto and (not f["deployable"] if veto else True)
assert f["grade"] == "Reject" if veto else True
assert 2 <= len(r["key_strengths"]) <= 5
assert all(len(x["title"]) <= 60 for x in r["recommendations"])
assert [x["priority"] for x in r["recommendations"]] == sorted([x["priority"] for x in r["recommendations"]], key={"P0": 0, "P1": 1, "P2": 2}.get)
assert r["veto_gates"]["research_veto"]["applicable"] is True
assert all(x["result"] in {"PASS", "FAIL", "N/A"} for k, x in r["veto_gates"]["research_veto"].items() if isinstance(x, dict))
print(json.dumps({"schema": "skill-auditor-report-v4.0", "valid": True, "input_count": len(inputs), "assertions_passed": passed, "assertions_total": total_assertions, "execution_average": avg, "static_subtotal": r["static_score"]["subtotal"], "diagnostic_score": f["score"], "veto_override": veto, "deployable": f["deployable"]}, indent=2))
