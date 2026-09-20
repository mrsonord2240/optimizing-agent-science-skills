#!/usr/bin/env python3
"""Independent re-check of the emitted JSON against the schema's pre-emit checklist (report_json_schema.md)."""
import json, os
d = json.load(open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "eval_report_bio-long-read-splicing_result.json"), encoding="utf-8"))
assert list(d) == ["meta", "veto_gates", "static_score", "dynamic_score", "final", "key_strengths", "recommendations"]
sv = d["veto_gates"]["skill_veto"]; rv = d["veto_gates"]["research_veto"]
assert set(sv) == {"gate", "stability", "contract", "determinism", "security"}
assert set(rv) == {"applicable", "gate", "scientific_integrity", "practice_boundaries", "methodological_ground", "code_usability"}
cats = d["static_score"]["categories"]
assert set(cats) == {"functional_suitability", "reliability", "performance_context", "agent_usability", "human_usability", "security", "maintainability", "agent_specific"}
assert d["static_score"]["subtotal"] == sum(c["score"] for c in cats.values()) and all(0 <= c["score"] <= c["max"] and c["note"] for c in cats.values())
ins = d["dynamic_score"]["inputs"]; assert len(ins) == d["meta"]["n_inputs"]
for i in ins:
    assert 3 <= len(i["assertions"]) <= 5 and i["assertions_passed"] == sum(a["result"] == "PASS" for a in i["assertions"]) and i["assertions_total"] == len(i["assertions"])
    assert i["basic"] + i["specialized"] == i["total"] and 0 <= i["basic"] <= 40 and 0 <= i["specialized"] <= 60
    assert i["status_flag"] == ("✅" if i["status"] == "COMPLETED" and i["total"] >= 75 else "⚠️" if i["status"] == "COMPLETED" else "❌")
assert d["dynamic_score"]["execution_avg"] == round(sum(i["total"] for i in ins) / len(ins), 1)
assert d["dynamic_score"]["assertion_pass_rate"] == {"passed": sum(i["assertions_passed"] for i in ins), "total": sum(i["assertions_total"] for i in ins)}
f = d["final"]
assert f["static_weighted"] == round(d["static_score"]["subtotal"] * .4, 1) and f["dynamic_weighted"] == round(d["dynamic_score"]["execution_avg"] * .6, 1)
assert f["score"] == round(f["static_weighted"] + f["dynamic_weighted"])
assert (f["grade"], f["grade_symbol"]) == (("Production Ready", "⭐") if f["score"] >= 85 else ("Limited Release", "✅") if f["score"] >= 75 else ("Beta Only", "⚠️") if f["score"] >= 60 else ("Reject", "❌"))
assert f["veto_override"] is False and f["deployable"] is True
assert 2 <= len(d["key_strengths"]) <= 5
pr = [r["priority"] for r in d["recommendations"]]; assert pr == sorted(pr)
print("schema checklist OK: score", f["score"], f["grade"], "| P0", pr.count("P0"), "P1", pr.count("P1"), "P2", pr.count("P2"))
