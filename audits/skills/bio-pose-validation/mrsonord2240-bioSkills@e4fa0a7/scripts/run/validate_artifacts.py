"""Assert the Phase 2 report contract for bio-pose-validation."""
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
report = json.loads((ROOT / "eval_report_bio-pose-validation_result.json").read_text(encoding="utf-8"))

assert report["meta"]["source"] == "mrsonord2240/bioSkills@e4fa0a78b55a107b91337a3307faebf34a70644d:chemoinformatics/pose-validation"
assert report["meta"]["auditor_independent"] is False
assert report["meta"]["note"] == "final pass: fixed and audited under one brief, see CHECKPOINT.md"
inputs = report["dynamic_score"]["inputs"]
assert len(inputs) == 9
assert all(row["executed"] is True and row["execution_note"] for row in inputs)
assert sum(row["assertions_passed"] for row in inputs) == 30
assert sum(row["assertions_total"] for row in inputs) == 30
assert report["final"] == {"static_weighted": 37.6, "dynamic_weighted": 57.1, "score": 95, "max": 100, "grade": "Production Ready", "grade_symbol": "⭐", "deployable": True, "veto_override": False}
assert "Production Ready" in (ROOT / "eval_viewer_bio-pose-validation.md").read_text(encoding="utf-8")
print("REPORT CONTRACT PASS: 9 executed inputs, 30/30 assertions, final 95 Production Ready")
