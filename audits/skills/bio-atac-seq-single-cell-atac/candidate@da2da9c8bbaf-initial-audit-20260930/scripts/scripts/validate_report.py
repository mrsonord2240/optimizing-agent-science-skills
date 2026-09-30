"""Validate report.json against the pinned skill-auditor report_json_schema.md pre-emit checklist."""
import json, pathlib, sys
H = pathlib.Path(__file__).resolve().parent.parent
r = json.load(open(H / 'report.json', encoding='utf-8'))
fs = json.load(open(H / 'findings.json', encoding='utf-8'))
err = []
def chk(c, m):
    if not c: err.append(m)
top = ["meta", "veto_gates", "static_score", "dynamic_score", "final", "key_strengths", "recommendations"]
chk(list(r) == top, f"top-level keys {list(r)}")
m = r["meta"]
chk(set(m) == {"skill_name", "description", "evaluated_on", "evaluator_version", "category", "execution_mode", "complexity", "n_inputs"}, "meta keys")
chk(m["evaluator_version"] == "skill-auditor@1.0", "evaluator_version")
chk(m["category"] in ["Evidence Insight", "Protocol Design", "Data Analysis", "Academic Writing", "Other"], "category")
sv = r["veto_gates"]["skill_veto"]
chk(set(sv) == {"gate", "stability", "contract", "determinism", "security"}, "skill_veto keys")
chk(sv["gate"] == ("FAIL" if "FAIL" in [sv[k] for k in sv if k != "gate"] else "PASS"), "skill gate logic")
rv = r["veto_gates"]["research_veto"]
chk(set(rv) == {"applicable", "gate", "scientific_integrity", "practice_boundaries", "methodological_ground", "code_usability"}, "research_veto keys")
chk(rv["gate"] == ("FAIL" if any(rv[k]["result"] == "FAIL" for k in rv if isinstance(rv[k], dict)) else "PASS"), "research gate logic")
sc = r["static_score"]
mx = {"functional_suitability": 12, "reliability": 12, "performance_context": 8, "agent_usability": 16, "human_usability": 8, "security": 12, "maintainability": 12, "agent_specific": 20}
chk(set(sc["categories"]) == set(mx), "static categories")
for k, v in sc["categories"].items():
    chk(0 <= v["score"] <= mx[k] and v["max"] == mx[k] and v["note"], f"static {k}")
chk(sc["subtotal"] == sum(v["score"] for v in sc["categories"].values()), "subtotal")
d = r["dynamic_score"]
chk(len(d["inputs"]) == m["n_inputs"], "n_inputs")
for i in d["inputs"]:
    p = sum(a["result"] == "PASS" for a in i["assertions"])
    chk(3 <= len(i["assertions"]) <= 5, f"assertion count input {i['index']}")
    chk(i["assertions_passed"] == p and i["assertions_total"] == len(i["assertions"]), f"assertion tallies {i['index']}")
    chk(i["basic"] + i["specialized"] == i["total"], f"total {i['index']}")
    chk(i["type"] in ["Canonical", "Variant A", "Variant B", "Edge", "Stress", "Scope Boundary", "Adversarial"], "type")
    exp = "✅" if i["status"] == "COMPLETED" and i["total"] >= 75 else ("⚠️" if i["status"] == "COMPLETED" else "❌")
    chk(i["status_flag"] == exp, f"status_flag {i['index']}")
chk(d["execution_avg"] == round(sum(i["total"] for i in d["inputs"]) / len(d["inputs"]), 1), "execution_avg")
chk(d["assertion_pass_rate"] == {"passed": sum(i["assertions_passed"] for i in d["inputs"]), "total": sum(i["assertions_total"] for i in d["inputs"])}, "pass rate")
f = r["final"]
chk(f["static_weighted"] == round(sc["subtotal"] * 0.4, 1), "static_weighted")
chk(f["dynamic_weighted"] == round(d["execution_avg"] * 0.6, 1), "dynamic_weighted")
chk(f["score"] == round(f["static_weighted"] + f["dynamic_weighted"]), "score")
chk(f["grade"] in ["Production Ready", "Limited Release", "Beta Only", "Reject"], "grade")
chk(f["deployable"] is (f["grade"] in ["Production Ready", "Limited Release"] and not f["veto_override"]), "deployable")
chk(2 <= len(r["key_strengths"]) <= 5, "strengths")
pr = [x["priority"] for x in r["recommendations"]]
chk(all(p in ["P0", "P1", "P2"] for p in pr), "priority enum (no P3)")
chk(pr == sorted(pr), "recommendation sort")
for x in r["recommendations"]:
    chk(set(x) == {"priority", "title", "observed_in", "problem", "root_cause", "fix"} and len(x["title"]) <= 60, f"rec {x['title']}")
ids = [x["id"] for x in fs]
chk(len(set(ids)) == len(ids), "finding ids unique")
for x in r["recommendations"]:
    for fid in __import__("re").findall(r"SCATAC-\d+", x["fix"]):
        chk(fid in ids, f"unknown id {fid}")
print("VALID" if not err else "INVALID: " + "; ".join(err))
sys.exit(1 if err else 0)
