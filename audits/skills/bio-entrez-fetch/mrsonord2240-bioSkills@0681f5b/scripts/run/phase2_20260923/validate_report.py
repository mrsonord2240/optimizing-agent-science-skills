import json
from pathlib import Path

report_path = Path(r"F:\OpenScience\audits\bio-entrez-fetch\eval_report_bio-entrez-fetch_result.json")
report = json.loads(report_path.read_text(encoding="utf-8"))
assert report["source"] == "mrsonord2240/bioSkills@0681f5b171b43eade5c4d81f0285dd9a5dbadb20:database-access/entrez-fetch"
meta = report["meta"]
assert meta["auditor_independent"] is False
assert meta["note"] == "final pass: fixed and audited under one brief, see CHECKPOINT.md"
assert meta["n_inputs"] == len(report["dynamic_score"]["inputs"]) == 7
categories = report["static_score"]["categories"]
assert len(categories) == 8
assert report["static_score"]["subtotal"] == sum(item["score"] for item in categories.values())
inputs = report["dynamic_score"]["inputs"]
assert all(item["executed"] is True and item["execution_note"] for item in inputs)
assert all(item["basic"] + item["specialized"] == item["total"] for item in inputs)
assert all(3 <= len(item["assertions"]) <= 5 for item in inputs)
assert all(item["assertions_passed"] == sum(a["result"] == "PASS" for a in item["assertions"]) for item in inputs)
assert report["dynamic_score"]["assertion_pass_rate"] == {"passed": 28, "total": 28}
average = round(sum(item["total"] for item in inputs) / len(inputs), 1)
assert report["dynamic_score"]["execution_avg"] == average == 95.7
final = report["final"]
assert final["static_weighted"] == round(report["static_score"]["subtotal"] * 0.4, 1)
assert final["dynamic_weighted"] == round(average * 0.6, 1)
assert final["score"] == round(final["static_weighted"] + final["dynamic_weighted"])
assert final["veto_override"] is False and final["deployable"] is True
assert report["veto_gates"]["research_veto"]["applicable"] is True
assert report["veto_gates"]["research_veto"]["gate"] == "PASS"
assert all(item["priority"] in {"P0", "P1", "P2"} for item in report["recommendations"])
print("REPORT_SCHEMA_AND_METADATA_OK")
