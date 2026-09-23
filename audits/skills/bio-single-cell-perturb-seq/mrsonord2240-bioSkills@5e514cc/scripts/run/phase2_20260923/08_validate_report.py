"""Validate Phase 2 JSON schema invariants required by the audit brief."""
import json
from pathlib import Path
p = Path(r"F:/OpenScience/audits/bio-single-cell-perturb-seq/eval_report_bio-single-cell-perturb-seq_result.json")
r = json.loads(p.read_text(encoding="utf-8"))
assert r["meta"]["source"].endswith("876237de72453b0651d8fe631c1201046d99c668:single-cell/perturb-seq")
assert r["meta"]["auditor_independent"] is False
assert r["meta"]["note"] == "final pass: fixed and audited under one brief, see CHECKPOINT.md"
assert len(r["static_score"]["categories"]) == 8
assert sum(v["score"] for v in r["static_score"]["categories"].values()) == r["static_score"]["subtotal"]
inputs = r["dynamic_score"]["inputs"]
assert len(inputs) == r["meta"]["n_inputs"] == 7
assert all(i["executed"] is True and i["execution_note"] and 3 <= len(i["assertions"]) <= 5 for i in inputs)
assert all(i["basic"] + i["specialized"] == i["total"] for i in inputs)
assert round(sum(i["total"] for i in inputs) / len(inputs), 1) == r["dynamic_score"]["execution_avg"]
assert r["final"]["veto_override"] and not r["final"]["deployable"]
print("PASS report JSON invariants")
