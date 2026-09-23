import json
from pathlib import Path

root = Path(r"F:\OpenScience\audits\bio-crispr-screens-crispresso-editing")
report = json.loads((root / "eval_report_bio-crispr-screens-crispresso-editing_result.json").read_text(encoding="utf-8"))
assert set(report) == {"meta", "veto_gates", "static_score", "dynamic_score", "final", "key_strengths", "recommendations"}
assert report["meta"]["source"] == "mrsonord2240/bioSkills@205c8574b66f30fb04cb2fdbd0464f6d37a70920:crispr-screens/crispresso-editing"
assert report["meta"]["auditor_independent"] is False
assert report["meta"]["note"] == "final pass: fixed and audited under one brief, see CHECKPOINT.md"
assert len(report["dynamic_score"]["inputs"]) == 11
assert all(x["executed"] is True and x["execution_note"] for x in report["dynamic_score"]["inputs"])
assert all(len(x["assertions"]) in range(3, 6) for x in report["dynamic_score"]["inputs"])
assert all(x["basic"] + x["specialized"] == x["total"] for x in report["dynamic_score"]["inputs"])
assert round(sum(x["total"] for x in report["dynamic_score"]["inputs"]) / 11, 1) == report["dynamic_score"]["execution_avg"]
assert sum(v["score"] for v in report["static_score"]["categories"].values()) == report["static_score"]["subtotal"]
assert report["final"]["deployable"] is True and report["final"]["veto_override"] is False
print("report schema, scoring, and execution coverage OK")
