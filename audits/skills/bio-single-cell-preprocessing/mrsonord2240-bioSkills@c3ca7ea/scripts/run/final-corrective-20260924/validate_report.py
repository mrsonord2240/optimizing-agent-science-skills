"""Validate the c3ca7ea final-pass report and rendered viewer."""

import json
from pathlib import Path


AUDIT = Path("F:/OpenScience/audits/bio-single-cell-preprocessing")
report = json.loads(
    (AUDIT / "eval_report_bio-single-cell-preprocessing_result.json").read_text(
        encoding="utf-8"
    )
)
viewer = (AUDIT / "eval_viewer_bio-single-cell-preprocessing.md").read_text(
    encoding="utf-8"
)

source = (
    "mrsonord2240/bioSkills@"
    "c3ca7ea1aa3aacf4efebc322b9b01dee31fe3917:single-cell/preprocessing"
)
assert report["meta"]["source"] == source
assert report["meta"]["n_inputs"] == 9
assert report["meta"]["regression_inputs"] == [1, 2, 3, 4, 5, 6, 7]
assert report["meta"]["new_inputs"] == [8, 9]
assert report["meta"]["executed_inputs"] == "8/9"
assert report["meta"]["auditor_independent"] is False

inputs = report["dynamic_score"]["inputs"]
assert len(inputs) == 9
assert [row["index"] for row in inputs] == list(range(1, 10))
assert sum(row["executed"] for row in inputs) == 8
assert all(3 <= len(row["assertions"]) <= 5 for row in inputs)
assert all(
    row["assertions_passed"]
    == sum(assertion["result"] == "PASS" for assertion in row["assertions"])
    == row["assertions_total"]
    for row in inputs
)
assert report["dynamic_score"]["execution_avg"] == 92.9
assert report["dynamic_score"]["assertion_pass_rate"] == {
    "passed": 36,
    "total": 36,
}
assert report["static_score"]["subtotal"] == 92
assert report["final"]["score"] == 93
assert report["final"]["grade"] == "Production Ready"
assert report["final"]["deployable"] is True
assert report["recommendations"] == []

assert source in viewer
assert "**93/100**" in viewer
assert "**Assertion Pass Rate: 36/36**" in viewer
print("PASS: c3ca7ea report and viewer invariants")
