"""Validate report.json against the pinned skill-auditor report_json_schema.md pre-emit checklist."""
import json, sys
p = sys.argv[1]
r = json.load(open(p, encoding='utf-8'))
errs = []
def need(c, m):
    if not c: errs.append(m)
need(list(r) == ["meta", "veto_gates", "static_score", "dynamic_score", "final", "key_strengths", "recommendations"], "top-level keys/order")
m = r["meta"]
need(set(m) == {"skill_name", "description", "evaluated_on", "evaluator_version", "category", "execution_mode", "complexity", "n_inputs"}, "meta keys")
need(m["evaluator_version"] == "skill-auditor@1.0" and m["category"] in ("Evidence Insight", "Protocol Design", "Data Analysis", "Academic Writing", "Other"), "meta values")
sv = r["veto_gates"]["skill_veto"]; rv = r["veto_gates"]["research_veto"]
need(set(sv) == {"gate", "stability", "contract", "determinism", "security"}, "skill_veto keys")
need(set(rv) == {"applicable", "gate", "scientific_integrity", "practice_boundaries", "methodological_ground", "code_usability"}, "research_veto keys")
need(sv["gate"] == ("FAIL" if "FAIL" in [sv[k] for k in ("stability", "contract", "determinism", "security")] else "PASS"), "skill gate logic")
ss = r["static_score"]; mx = dict(functional_suitability=12, reliability=12, performance_context=8, agent_usability=16, human_usability=8, security=12, maintainability=12, agent_specific=20)
need(set(ss["categories"]) == set(mx), "8 categories")
for k, v in ss["categories"].items():
    need(0 <= v["score"] <= mx[k] and v["max"] == mx[k] and v["note"], f"category {k}")
need(ss["subtotal"] == sum(v["score"] for v in ss["categories"].values()), "static subtotal")
d = r["dynamic_score"]; ins = d["inputs"]
need(len(ins) == m["n_inputs"], "n inputs")
for i in ins:
    need(3 <= len(i["assertions"]) <= 5, f"assertion count input {i['index']}")
    need(i["assertions_passed"] == sum(a["result"] == "PASS" for a in i["assertions"]) and i["assertions_total"] == len(i["assertions"]), f"assertion tally {i['index']}")
    need(i["basic"] + i["specialized"] == i["total"] and 0 <= i["basic"] <= 40 and 0 <= i["specialized"] <= 60, f"totals {i['index']}")
    need(all(a["result"] in ("PASS", "FAIL") for a in i["assertions"]), "assertion result enum")
    need(i["type"] in ("Canonical", "Variant A", "Variant B", "Edge", "Stress", "Scope Boundary", "Adversarial"), "input type")
    need(i["status"] in ("COMPLETED", "PARTIAL", "ERROR"), "status enum")
    need(i["status_flag"] == ("✅" if i["status"] == "COMPLETED" and i["total"] >= 75 else "⚠️" if i["status"] == "COMPLETED" else "❌"), f"status_flag {i['index']}")
need(d["execution_avg"] == round(sum(i["total"] for i in ins) / len(ins), 1), "execution_avg")
need(d["assertion_pass_rate"] == {"passed": sum(i["assertions_passed"] for i in ins), "total": sum(i["assertions_total"] for i in ins)}, "assertion rate")
f = r["final"]
need(f["static_weighted"] == round(ss["subtotal"] * 0.4, 1) and f["dynamic_weighted"] == round(d["execution_avg"] * 0.6, 1), "weighted")
need(f["score"] == int(round(f["static_weighted"] + f["dynamic_weighted"])), "final score")
need(f["grade"] == ("Production Ready" if f["score"] >= 85 else "Limited Release" if f["score"] >= 75 else "Beta Only" if f["score"] >= 60 else "Reject"), "grade")
need(f["veto_override"] is False and f["deployable"] == (f["grade"] in ("Production Ready", "Limited Release")), "deployable/veto")
need(2 <= len(r["key_strengths"]) <= 5, "key_strengths count")
pr = [x["priority"] for x in r["recommendations"]]
need(all(p in ("P0", "P1", "P2") for p in pr) and pr == sorted(pr), "recommendation priorities/sort")
for x in r["recommendations"]:
    need(set(x) == {"priority", "title", "observed_in", "problem", "root_cause", "fix"} and len(x["title"]) <= 60, "recommendation shape")
def ascii_only(o):
    return all(ord(c) < 128 for c in json.dumps(o, ensure_ascii=False) if c not in "✅⚠️❌⭐")
need(ascii_only(r), "non-ASCII free text")
print("VALID" if not errs else "INVALID: " + "; ".join(errs))
sys.exit(1 if errs else 0)
