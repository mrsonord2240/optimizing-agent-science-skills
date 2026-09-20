"""Pre-emit checklist of skill-auditor/references/report_json_schema.md, run on the written report."""
import json, sys
from pathlib import Path
d = json.load(open(Path(__file__).resolve().parents[2] / "eval_report_bio-alignment-validation_result.json", encoding="utf-8"))
top = ["meta", "veto_gates", "static_score", "dynamic_score", "final", "key_strengths", "recommendations"]
assert list(d) == top, list(d)
sv = d["veto_gates"]["skill_veto"]; assert set(sv) == {"gate", "stability", "contract", "determinism", "security"}
rv = d["veto_gates"]["research_veto"]; assert set(rv) == {"applicable", "gate", "scientific_integrity", "practice_boundaries", "methodological_ground", "code_usability"}
cats = d["static_score"]["categories"]; assert len(cats) == 8
assert d["static_score"]["subtotal"] == sum(c["score"] for c in cats.values())
ins = d["dynamic_score"]["inputs"]; assert len(ins) == d["meta"]["n_inputs"]
tp = tt = 0
for i in ins:
    assert 3 <= len(i["assertions"]) <= 5
    assert i["assertions_passed"] == sum(a["result"] == "PASS" for a in i["assertions"]) and i["assertions_total"] == len(i["assertions"])
    assert i["basic"] + i["specialized"] == i["total"] and 0 <= i["basic"] <= 40 and 0 <= i["specialized"] <= 60
    assert i["executed"] in (True, False) and i["execution_note"]
    tp += i["assertions_passed"]; tt += i["assertions_total"]
assert d["dynamic_score"]["assertion_pass_rate"] == {"passed": tp, "total": tt}
assert d["dynamic_score"]["execution_avg"] == round(sum(i["total"] for i in ins) / len(ins), 1)
f = d["final"]
assert f["static_weighted"] == round(d["static_score"]["subtotal"] * 0.4, 1) and f["dynamic_weighted"] == round(d["dynamic_score"]["execution_avg"] * 0.6, 1)
assert f["score"] == round(f["static_weighted"] + f["dynamic_weighted"])
assert 2 <= len(d["key_strengths"]) <= 5
pr = [r["priority"] for r in d["recommendations"]]; assert pr == sorted(pr)
assert d["meta"]["source"].startswith("mrsonord2240/bioSkills@f9307f4029f87c79892a5d2832dee4b903038056:") and d["meta"]["evaluated_on"] == "2026-09-20"
print("OK", f, "| assertions", tp, "/", tt, "| recs", pr.count("P0"), pr.count("P1"), pr.count("P2"))
