"""Local structural and arithmetic checks for the emitted audit JSON."""
import json
from pathlib import Path

report = Path(__file__).resolve().parents[1] / "eval_report_bio-causal-genomics-colocalization-analysis_result.json"
d = json.loads(report.read_text(encoding="utf-8"))
assert list(d) == ["meta", "veto_gates", "static_score", "dynamic_score", "final", "key_strengths", "recommendations"]
assert d["meta"]["auditor_independent"] is False and d["meta"]["note"] == "final pass: fixed and audited under one brief, see CHECKPOINT.md"
assert len(d["static_score"]["categories"]) == 8
assert sum(x["score"] for x in d["static_score"]["categories"].values()) == d["static_score"]["subtotal"]
inputs = d["dynamic_score"]["inputs"]
assert len(inputs) == d["meta"]["n_inputs"] == 12
assert all(3 <= len(x["assertions"]) <= 5 for x in inputs)
assert all(x["basic"] + x["specialized"] == x["total"] for x in inputs)
assert all(x["assertions_passed"] == sum(a["result"] == "PASS" for a in x["assertions"]) for x in inputs)
assert round(sum(x["total"] for x in inputs) / len(inputs), 1) == d["dynamic_score"]["execution_avg"]
assert d["dynamic_score"]["assertion_pass_rate"] == {"passed": 59, "total": 60}
assert d["final"]["static_weighted"] == round(d["static_score"]["subtotal"] * .4, 1)
assert d["final"]["dynamic_weighted"] == round(d["dynamic_score"]["execution_avg"] * .6, 1)
assert not d["final"]["veto_override"] and d["final"]["deployable"] and d["final"]["grade"] == "Production Ready"
assert d["veto_gates"]["research_veto"]["gate"] == "PASS"
assert all(a["priority"] in {"P0", "P1", "P2"} for a in d["recommendations"])
print("REPORT_SCHEMA_AND_ARITHMETIC_PASS")
