"""Validate the final re-audit report's essential arithmetic and schema shape."""
import json
from pathlib import Path

report_path = Path(__file__).parents[2] / "eval_report_bio-data-visualization-heatmaps-clustering_result.json"
report = json.loads(report_path.read_text(encoding="utf-8"))
inputs = report["dynamic_score"]["inputs"]

assert report["meta"]["source"].startswith("mrsonord2240/bioSkills@6454218cec8127aa7880df1b346afd108bc8e3a0:")
assert report["meta"]["auditor_independent"] is False
assert report["meta"]["note"] == "final pass: fixed and audited under one brief, see CHECKPOINT.md"
assert len(inputs) == report["meta"]["n_inputs"] == 8
assert sum(item["total"] for item in inputs) / len(inputs) == 89.375
assert sum(item["assertions_passed"] for item in inputs) == 36
assert sum(item["assertions_total"] for item in inputs) == 37
assert report["static_score"]["subtotal"] == 90
assert report["final"]["score"] == 90
assert report["final"]["grade"] == "Production Ready"
assert report["recommendations"] == []
print("PASS: JSON parses; exact source, final-pass metadata, arithmetic, and cleared recommendations are valid")
