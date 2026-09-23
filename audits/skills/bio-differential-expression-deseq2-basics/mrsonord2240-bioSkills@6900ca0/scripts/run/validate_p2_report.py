"""Validate Phase 2 report invariants required by report_json_schema.md."""
import json
from pathlib import Path

report = Path(r"F:/OpenScience/audits/bio-differential-expression-deseq2-basics/eval_report_bio-differential-expression-deseq2-basics_result.json")
data = json.loads(report.read_text(encoding="utf-8"))
assert set(data) == {"meta", "veto_gates", "static_score", "dynamic_score", "final", "key_strengths", "recommendations"}
assert data["meta"]["auditor_independent"] is False
assert data["meta"]["note"] == "final pass: fixed and audited under one brief, see CHECKPOINT.md"
categories = data["static_score"]["categories"]
assert len(categories) == 8
assert sum(row["score"] for row in categories.values()) == data["static_score"]["subtotal"]
inputs = data["dynamic_score"]["inputs"]
assert len(inputs) == data["meta"]["n_inputs"] == 7
assert all(len(row["assertions"]) in range(3, 6) for row in inputs)
assert all(row["basic"] + row["specialized"] == row["total"] for row in inputs)
assert all(row["assertions_passed"] == sum(a["result"] == "PASS" for a in row["assertions"]) for row in inputs)
assert round(sum(row["total"] for row in inputs) / len(inputs), 1) == data["dynamic_score"]["execution_avg"]
assert all(row["executed"] is True and row["execution_note"] for row in inputs)
assert data["veto_gates"]["research_veto"]["gate"] == "PASS"
assert data["final"]["veto_override"] is False and data["final"]["deployable"] is True
assert [r["priority"] for r in data["recommendations"]] == ["P2"]
print("report schema invariants: PASS")
