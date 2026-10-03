#!/usr/bin/env python3
"""Strict checks for the skill-auditor v4 report contract. Usage: validate_report.py <report.json>"""
import json
import sys
from pathlib import Path

data = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
errors = []


def req(cond, msg):
    if not cond:
        errors.append(msg)


req(set(data) == {"meta", "veto_gates", "static_score", "dynamic_score", "final", "key_strengths", "recommendations"}, "top-level keys")
req(set(data["meta"]) >= {"skill_name", "description", "evaluated_on", "evaluator_version", "category", "execution_mode", "complexity", "n_inputs"}, "meta keys")
sv, rv = data["veto_gates"]["skill_veto"], data["veto_gates"]["research_veto"]
req(set(sv) == {"gate", "stability", "contract", "determinism", "security"}, "skill veto keys")
req(set(rv) == {"applicable", "gate", "scientific_integrity", "practice_boundaries", "methodological_ground", "code_usability"}, "research veto keys")
cats = data["static_score"]["categories"]
mx = {"functional_suitability": 12, "reliability": 12, "performance_context": 8, "agent_usability": 16,
      "human_usability": 8, "security": 12, "maintainability": 12, "agent_specific": 20}
req(set(cats) == set(mx), "category keys")
for k, v in cats.items():
    req(set(v) == {"score", "max", "note"} and v["max"] == mx[k] and 0 <= v["score"] <= mx[k] and v["note"], f"category {k}")
req(sum(v["score"] for v in cats.values()) == data["static_score"]["subtotal"], "subtotal")
ins = data["dynamic_score"]["inputs"]
req(len(ins) == data["meta"]["n_inputs"], "n inputs")
P = T = 0
for i in ins:
    a = i["assertions"]
    req(3 <= len(a) <= 5, f"in{i['index']} assertion count")
    req(sum(x["result"] == "PASS" for x in a) == i["assertions_passed"] and len(a) == i["assertions_total"], f"in{i['index']} counts")
    req(i["basic"] + i["specialized"] == i["total"] and 0 <= i["basic"] <= 40 and 0 <= i["specialized"] <= 60, f"in{i['index']} sums")
    req(all(set(x) == {"text", "result", "note"} for x in a), f"in{i['index']} assertion shape")
    if i["status"] in ("PARTIAL", "ERROR"):
        req(i["status_flag"] == "❌", f"in{i['index']} flag")
    elif i["total"] >= 75:
        req(i["status_flag"] == "✅", f"in{i['index']} flag")
    else:
        req(i["status_flag"] == "⚠️", f"in{i['index']} flag")
    P += i["assertions_passed"]
    T += i["assertions_total"]
avg = round(sum(i["total"] for i in ins) / len(ins), 1)
req(avg == data["dynamic_score"]["execution_avg"], "execution avg")
req(data["dynamic_score"]["assertion_pass_rate"] == {"passed": P, "total": T}, "assertion rate")
f = data["final"]
sw, dw = round(data["static_score"]["subtotal"] * 0.4, 1), round(avg * 0.6, 1)
req(f["static_weighted"] == sw and f["dynamic_weighted"] == dw, "weights")
req(f["score"] == round(sw + dw), "final score")
s = f["score"]
grade, sym = ("Production Ready", "⭐") if s >= 85 else ("Limited Release", "✅") if s >= 75 else ("Beta Only", "⚠️") if s >= 60 else ("Reject", "❌")
gate_fail = sv["gate"] == "FAIL" or rv["gate"] == "FAIL"
if gate_fail:
    grade, sym = "Reject", "❌"
req(f["grade"] == grade and f["grade_symbol"] == sym, f"grade expected {grade}")
req(f["veto_override"] == gate_fail, "veto override")
req(f["deployable"] == (grade in ("Production Ready", "Limited Release") and not gate_fail), "deployable")
req(2 <= len(data["key_strengths"]) <= 5, "strengths")
ranks = [{"P0": 0, "P1": 1, "P2": 2}[r["priority"]] for r in data["recommendations"]]
req(ranks == sorted(ranks), "rec order")
req(all(set(r) == {"priority", "title", "observed_in", "problem", "root_cause", "fix"} for r in data["recommendations"]), "rec shape")
print(json.dumps({"valid": not errors, "errors": errors, "static": data["static_score"]["subtotal"], "exec_avg": avg,
                  "assertions": [P, T], "final": s, "grade": grade}, indent=1))
sys.exit(1 if errors else 0)
