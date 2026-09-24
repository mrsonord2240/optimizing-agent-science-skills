"""Validate final multipanel report arithmetic and exact-source metadata."""
import json
from pathlib import Path

path = Path(__file__).parents[2] / "eval_report_bio-data-visualization-multipanel-figures_result.json"
report = json.loads(path.read_text(encoding="utf-8"))
inputs = report["dynamic_score"]["inputs"]
assert report["meta"]["source"].startswith("mrsonord2240/bioSkills@3749f31f1c2d406f5e948bb389eaea7379c6e71a:")
assert report["meta"]["auditor_independent"] is False
assert report["meta"]["note"] == "final pass: fixed and audited under one brief, see CHECKPOINT.md"
assert len(inputs) == report["meta"]["n_inputs"] == 5
assert all(row["basic"] + row["specialized"] == row["total"] for row in inputs)
assert report["static_score"]["subtotal"] == sum(row["score"] for row in report["static_score"]["categories"].values()) == 94
assert report["dynamic_score"]["execution_avg"] == round(sum(row["total"] for row in inputs) / len(inputs), 1) == 94.2
assert report["dynamic_score"]["assertion_pass_rate"] == {"passed": 25, "total": 25}
assert sum(row["assertions_passed"] for row in inputs) == 25
assert sum(row["assertions_total"] for row in inputs) == 25
assert report["final"]["score"] == 94.1
assert report["final"]["grade"] == "Production Ready"
assert report["recommendations"] == []
print("Multipanel final report validation PASS")
