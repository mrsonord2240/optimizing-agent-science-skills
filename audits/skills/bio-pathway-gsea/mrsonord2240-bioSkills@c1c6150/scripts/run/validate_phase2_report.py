import json
from pathlib import Path

report = json.loads(Path(r"F:\OpenScience\audits\bio-pathway-gsea\eval_report_bio-pathway-gsea_result.json").read_text(encoding="utf-8"))
assert report["meta"]["auditor_independent"] is False
assert report["meta"]["source"].startswith("mrsonord2240/bioSkills@c1c6150cba5570abc754866e90d09ee536917b07")
assert len(report["static_score"]["categories"]) == 8
assert report["static_score"]["subtotal"] == sum(x["score"] for x in report["static_score"]["categories"].values())
inputs = report["dynamic_score"]["inputs"]
assert len(inputs) == report["meta"]["n_inputs"] == 7
assert all(x["executed"] is True and x["execution_note"] for x in inputs)
assert all(3 <= len(x["assertions"]) <= 5 for x in inputs)
assert all(x["assertions_passed"] == sum(a["result"] == "PASS" for a in x["assertions"]) for x in inputs)
assert all(x["total"] == x["basic"] + x["specialized"] for x in inputs)
assert report["dynamic_score"]["assertion_pass_rate"] == {"passed": 20, "total": 21}
assert report["dynamic_score"]["execution_avg"] == round(sum(x["total"] for x in inputs) / len(inputs), 1)
assert report["final"]["static_weighted"] == 36.8
assert report["final"]["dynamic_weighted"] == 56.6
assert report["final"]["score"] == 93
assert report["final"]["deployable"] is True and report["final"]["veto_override"] is False
print("report_schema=ok")
