"""Schema-focused validation for the final-pass JSON report."""
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
report = json.loads((ROOT / "eval_report_bio-pathway-enrichment-visualization_result.json").read_text(encoding="utf-8"))
assert report["meta"]["auditor_independent"] is False
assert report["meta"]["note"] == "final pass: fixed and audited under one brief, see CHECKPOINT.md"
assert report["meta"]["source"].startswith("mrsonord2240/bioSkills@9500048793a19cae65ca89930733581eddcc1375")
categories = report["static_score"]["categories"]
assert len(categories) == 8
assert sum(item["score"] for item in categories.values()) == report["static_score"]["subtotal"]
inputs = report["dynamic_score"]["inputs"]
assert len(inputs) == report["meta"]["n_inputs"] == 7
for item in inputs:
    assert item["executed"] is True and item["execution_note"]
    assert 3 <= len(item["assertions"]) <= 5
    assert item["assertions_passed"] == sum(a["result"] == "PASS" for a in item["assertions"])
    assert item["assertions_total"] == len(item["assertions"])
    assert item["basic"] + item["specialized"] == item["total"]
assert report["dynamic_score"]["assertion_pass_rate"] == {"passed": 28, "total": 28}
assert round(sum(item["total"] for item in inputs) / len(inputs), 1) == report["dynamic_score"]["execution_avg"]
final = report["final"]
assert final["static_weighted"] == round(report["static_score"]["subtotal"] * 0.4, 1)
assert final["dynamic_weighted"] == round(report["dynamic_score"]["execution_avg"] * 0.6, 1)
assert final["score"] == round(final["static_weighted"] + final["dynamic_weighted"])
assert final["grade"] == "Production Ready" and final["grade_symbol"] == "⭐"
assert final["deployable"] is True and final["veto_override"] is False
assert 2 <= len(report["key_strengths"]) <= 5
assert [x["priority"] for x in report["recommendations"]] == ["P2"]
print("PHASE2_REPORT_SCHEMA_VALIDATION_PASS")
