import json, pathlib, sys
R = pathlib.Path(__file__).resolve().parent.parent
r = json.loads((R / "report.json").read_text(encoding="utf-8"))
e = []
def chk(c, m):
    if not c: e.append(m)
chk(set(r) == {"meta", "veto_gates", "static_score", "dynamic_score", "final", "key_strengths", "recommendations"}, "top keys")
sv = r["veto_gates"]["skill_veto"]; chk(set(sv) == {"gate", "stability", "contract", "determinism", "security"}, "skill_veto keys")
rv = r["veto_gates"]["research_veto"]; chk(set(rv) == {"applicable", "gate", "scientific_integrity", "practice_boundaries", "methodological_ground", "code_usability"}, "research_veto keys")
c = r["static_score"]["categories"]
mx = dict(functional_suitability=12, reliability=12, performance_context=8, agent_usability=16, human_usability=8, security=12, maintainability=12, agent_specific=20)
chk(set(c) == set(mx), "8 categories")
for k, v in mx.items():
    chk(0 <= c[k]["score"] <= v and c[k]["max"] == v and c[k]["note"], "cat " + k)
chk(r["static_score"]["subtotal"] == sum(x["score"] for x in c.values()), "subtotal")
d = r["dynamic_score"]; ins = d["inputs"]
chk(len(ins) == r["meta"]["n_inputs"], "n_inputs")
for i in ins:
    chk(i["basic"] + i["specialized"] == i["total"], "sum %d" % i["index"])
    chk(3 <= len(i["assertions"]) <= 5, "assert card %d" % i["index"])
    chk(i["assertions_passed"] == sum(a["result"] == "PASS" for a in i["assertions"]), "passed %d" % i["index"])
    chk(i["assertions_total"] == len(i["assertions"]), "total %d" % i["index"])
    chk(i["basic"] <= 40 and i["specialized"] <= 60, "ranges")
chk(d["execution_avg"] == round(sum(i["total"] for i in ins) / len(ins), 1), "avg")
chk(d["assertion_pass_rate"]["passed"] == sum(i["assertions_passed"] for i in ins), "apr passed")
chk(d["assertion_pass_rate"]["total"] == sum(i["assertions_total"] for i in ins), "apr total")
f = r["final"]
chk(f["static_weighted"] == round(r["static_score"]["subtotal"] * .4, 1), "sw")
chk(f["dynamic_weighted"] == round(d["execution_avg"] * .6, 1), "dw")
chk(f["score"] == int(round(f["static_weighted"] + f["dynamic_weighted"])), "score")
chk(2 <= len(r["key_strengths"]) <= 5, "strengths")
pr = [x["priority"] for x in r["recommendations"]]
chk(all(p in ("P0", "P1", "P2") for p in pr) and pr == sorted(pr), "recs P0-P2 sorted")
for x in r["recommendations"]:
    chk(set(x) == {"priority", "title", "observed_in", "problem", "root_cause", "fix"} and len(x["title"]) <= 60, "rec " + x["title"])
chk(f["veto_override"] == (sv["gate"] == "FAIL" or rv["gate"] == "FAIL"), "veto_override")
print("VALID" if not e else "INVALID: %s" % e)
sys.exit(1 if e else 0)
