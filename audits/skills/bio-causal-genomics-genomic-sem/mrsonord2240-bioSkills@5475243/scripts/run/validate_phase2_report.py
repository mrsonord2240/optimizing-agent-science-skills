"""Schema-critical arithmetic and per-input execution-field validation."""
import json
from pathlib import Path

report = Path(r"F:/OpenScience/audits/bio-causal-genomics-genomic-sem/eval_report_bio-causal-genomics-genomic-sem_result.json")
d = json.loads(report.read_text(encoding="utf-8"))
assert d["meta"]["auditor_independent"] is False
assert d["meta"]["note"] == "final pass: fixed and audited under one brief, see CHECKPOINT.md"
inputs = d["dynamic_score"]["inputs"]
assert len(inputs) == d["meta"]["n_inputs"] == 11
assert all("executed" in x and "execution_note" in x for x in inputs)
assert all(x["basic"] + x["specialized"] == x["total"] for x in inputs)
assert all(3 <= len(x["assertions"]) <= 5 and x["assertions_passed"] == sum(a["result"] == "PASS" for a in x["assertions"]) for x in inputs)
assert round(sum(x["total"] for x in inputs) / len(inputs), 1) == d["dynamic_score"]["execution_avg"]
assert sum(c["score"] for c in d["static_score"]["categories"].values()) == d["static_score"]["subtotal"]
assert d["final"]["score"] == round(d["final"]["static_weighted"] + d["final"]["dynamic_weighted"])
assert d["veto_gates"]["skill_veto"]["gate"] == d["veto_gates"]["research_veto"]["gate"] == "PASS"
print("PHASE2_REPORT_VALID inputs=11 assertions=33/33 final=94 deployable=true")
