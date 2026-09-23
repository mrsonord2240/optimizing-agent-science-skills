"""Validate the Phase 2 audit JSON's required final-pass fields and score arithmetic."""
import json
from pathlib import Path

path = Path(r"F:/OpenScience/audits/bio-metabolomics-normalization-qc/eval_report_bio-metabolomics-normalization-qc_result.json")
report = json.loads(path.read_text(encoding="utf-8"))
meta = report["meta"]
assert meta["source"] == "mrsonord2240/bioSkills@980965fb613fd6c6dbbabe8d51c2b54eae3d8f34:metabolomics/normalization-qc"
assert meta["auditor_independent"] is False
assert meta["note"] == "final pass: fixed and audited under one brief, see CHECKPOINT.md"
inputs = report["dynamic_score"]["inputs"]
assert len(inputs) == meta["n_inputs"] == 12
for item in inputs:
    assert item["executed"] is True
    assert item["execution_note"]
    assert item["basic"] + item["specialized"] == item["total"]
    assert item["assertions_passed"] == sum(a["result"] == "PASS" for a in item["assertions"])
    assert item["assertions_total"] == len(item["assertions"])
avg = round(sum(item["total"] for item in inputs) / len(inputs), 1)
assert avg == report["dynamic_score"]["execution_avg"]
assert report["final"]["static_weighted"] == round(report["static_score"]["subtotal"] * 0.4, 1)
assert report["final"]["dynamic_weighted"] == round(avg * 0.6, 1)
assert report["final"]["score"] == 93
assert report["final"]["deployable"] is True
assert report["final"]["veto_override"] is False
assert "nonblocking" in report["final"]["deployment_rationale"]
assert report["recommendations"][0]["priority"] == "P1"
assert "nonblocking" in report["recommendations"][0]["fix"]
print("REPORT_VALID: 12 executed inputs, final-pass metadata, assertions, and scores agree")
