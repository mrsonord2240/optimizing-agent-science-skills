#!/usr/bin/env python3
"""Strict local checks for the skill-auditor v4 report contract (report_json_schema.md)."""
import json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
d = json.loads((ROOT / "report.json").read_text(encoding="utf-8"))
err = []
def req(c, m):
    if not c: err.append(m)
req(set(d) == {"meta","veto_gates","static_score","dynamic_score","final","key_strengths","recommendations"}, "top-level keys")
req(set(d["meta"]) >= {"skill_name","description","evaluated_on","evaluator_version","category","execution_mode","complexity","n_inputs"}, "meta keys")
req(d["meta"]["evaluator_version"] == "skill-auditor@1.0", "evaluator_version")
sv, rv = d["veto_gates"]["skill_veto"], d["veto_gates"]["research_veto"]
req(set(sv) == {"gate","stability","contract","determinism","security"}, "skill veto keys")
req(set(rv) == {"applicable","gate","scientific_integrity","practice_boundaries","methodological_ground","code_usability"}, "research veto keys")
req(sv["gate"] == ("FAIL" if "FAIL" in [sv[k] for k in ("stability","contract","determinism","security")] else "PASS"), "skill gate logic")
subs = [rv[k]["result"] for k in ("scientific_integrity","practice_boundaries","methodological_ground","code_usability")]
req(rv["gate"] == ("FAIL" if "FAIL" in subs else "PASS"), "research gate logic")
cats = d["static_score"]["categories"]
mx = dict(functional_suitability=12, reliability=12, performance_context=8, agent_usability=16, human_usability=8, security=12, maintainability=12, agent_specific=20)
req(set(cats) == set(mx), "static categories")
for k, v in cats.items():
    req(set(v) == {"score","max","note"} and v["max"] == mx[k] and 0 <= v["score"] <= mx[k] and v["note"], f"category {k}")
req(sum(v["score"] for v in cats.values()) == d["static_score"]["subtotal"], "subtotal")
ins = d["dynamic_score"]["inputs"]
req(len(ins) == d["meta"]["n_inputs"], "n_inputs")
P = T = 0
for i in ins:
    a = i["assertions"]
    req(3 <= len(a) <= 5, f"assertion count {i['index']}")
    req(sum(x["result"] == "PASS" for x in a) == i["assertions_passed"] and len(a) == i["assertions_total"], f"assertion tallies {i['index']}")
    req(i["basic"] + i["specialized"] == i["total"] and 0 <= i["basic"] <= 40 and 0 <= i["specialized"] <= 60, f"scores {i['index']}")
    req(all(set(x) == {"text","result","note"} and x["result"] in ("PASS","FAIL") for x in a), f"assertion shape {i['index']}")
    if i["status"] == "COMPLETED": req(i["status_flag"] == ("✅" if i["total"] >= 75 else "⚠️"), f"flag {i['index']}")
    else: req(i["status_flag"] == "❌", f"flag {i['index']}")
    P += i["assertions_passed"]; T += i["assertions_total"]
req(d["dynamic_score"]["execution_avg"] == round(sum(i["total"] for i in ins) / len(ins), 1), "execution_avg")
req(d["dynamic_score"]["assertion_pass_rate"] == {"passed": P, "total": T}, "assertion aggregate")
f = d["final"]
sw, dw = round(d["static_score"]["subtotal"] * .4, 1), round(d["dynamic_score"]["execution_avg"] * .6, 1)
req(f["static_weighted"] == sw and f["dynamic_weighted"] == dw and f["score"] == round(sw + dw), "final arithmetic")
veto = sv["gate"] == "FAIL" or rv["gate"] == "FAIL"
req(f["veto_override"] == veto, "veto_override")
grade = "Production Ready" if f["score"] >= 85 else "Limited Release" if f["score"] >= 75 else "Beta Only" if f["score"] >= 60 else "Reject"
if veto: grade = "Reject"
req(f["grade"] == grade, f"grade {f['grade']} vs {grade}")
req(f["deployable"] == (grade in ("Production Ready","Limited Release") and not veto), "deployable")
req(2 <= len(d["key_strengths"]) <= 5, "key_strengths")
r = {"P0": 0, "P1": 1, "P2": 2}
pr = [r[x["priority"]] for x in d["recommendations"]]
req(pr == sorted(pr), "recommendation order")
for x in d["recommendations"]:
    req(set(x) == {"priority","title","observed_in","problem","root_cause","fix"} and len(x["title"]) <= 60, f"rec shape {x.get('title')}")
print(json.dumps({"ok": not err, "errors": err}, indent=1))
sys.exit(1 if err else 0)
