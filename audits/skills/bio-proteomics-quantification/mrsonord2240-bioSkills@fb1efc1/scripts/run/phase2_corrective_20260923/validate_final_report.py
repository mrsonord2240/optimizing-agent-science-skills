"""Schema arithmetic and final-pass metadata checks for the corrective report."""
import json
from pathlib import Path
p=Path(r"F:\OpenScience\audits\bio-proteomics-quantification\eval_report_bio-proteomics-quantification_result.json")
d=json.loads(p.read_text(encoding="utf-8")); xs=d["dynamic_score"]["inputs"]
assert len(xs)==d["meta"]["n_inputs"]==13
assert d["meta"]["auditor_independent"] is False and d["meta"]["note"]=="final pass: fixed and audited under one brief, see CHECKPOINT.md"
assert all("executed" in x and "execution_note" in x for x in xs)
assert all(3<=len(x["assertions"])<=5 and x["basic"]+x["specialized"]==x["total"] for x in xs)
assert all(x["assertions_passed"]==sum(a["result"]=="PASS" for a in x["assertions"]) for x in xs)
assert sum(x["assertions_passed"] for x in xs)==52 and sum(x["assertions_total"] for x in xs)==52
assert round(sum(x["total"] for x in xs)/len(xs),1)==d["dynamic_score"]["execution_avg"]==93.0
assert sum(v["score"] for v in d["static_score"]["categories"].values())==d["static_score"]["subtotal"]==96
assert d["final"]=={"static_weighted":38.4,"dynamic_weighted":55.8,"score":94,"max":100,"grade":"Production Ready","grade_symbol":"⭐","deployable":True,"veto_override":False}
assert d["veto_gates"]["skill_veto"]["gate"]=="PASS" and d["veto_gates"]["research_veto"]["gate"]=="PASS"
print("report=valid inputs=13 executable=12 assertions=52/52 final=Production Ready deployable=true")
