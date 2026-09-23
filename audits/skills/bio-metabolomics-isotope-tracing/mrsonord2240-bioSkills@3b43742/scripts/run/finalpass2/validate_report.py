"""Validate final-pass report structure, arithmetic, and required evidence files."""
import json
from pathlib import Path

root = Path(r"F:/OpenScience/audits/bio-metabolomics-isotope-tracing")
report_path = root / "eval_report_bio-metabolomics-isotope-tracing_result.json"
report = json.loads(report_path.read_text(encoding="utf-8"))

assert report["meta"]["source"] == (
    "mrsonord2240/bioSkills@3b437423563329fb137fa6fae8adb9563196fa13:"
    "metabolomics/isotope-tracing"
)
assert report["meta"]["auditor_independent"] is False
assert report["meta"]["note"] == "final pass: fixed and audited under one brief, see CHECKPOINT.md"
assert len(report["dynamic_score"]["inputs"]) == report["meta"]["n_inputs"] == 9
assert set(report["static_score"]["categories"]) == {
    "functional_suitability", "reliability", "performance_context", "agent_usability",
    "human_usability", "security", "maintainability", "agent_specific",
}
assert sum(x["score"] for x in report["static_score"]["categories"].values()) == 98
inputs = report["dynamic_score"]["inputs"]
assert all(len(x["assertions"]) == 4 for x in inputs)
assert all(x["assertions_passed"] == 4 and x["assertions_total"] == 4 for x in inputs)
assert all(x["basic"] + x["specialized"] == x["total"] for x in inputs)
assert sum(x["total"] for x in inputs) / len(inputs) == 93.11111111111111
assert report["dynamic_score"]["assertion_pass_rate"] == {"passed": 36, "total": 36}
assert report["final"] == {
    "static_weighted": 39.2, "dynamic_weighted": 55.9, "score": 95, "max": 100,
    "grade": "Production Ready", "grade_symbol": "⭐", "deployable": True,
    "veto_override": False,
}
for name in [
    "input1_glutamine_correction.py.out.txt", "input2_accucor_correction.R.out.txt",
    "input3_steady_state_and_length_error.py.out.txt", "input5_gcms_derivative_and_error.py.out.txt",
    "input7_plateau_edge_cases.py.out.txt", "input8_15n_correction.py.out.txt",
    "input2_highres_documented_smoke.R.out.txt", "shipped_isotope_correction.py.out.txt",
]:
    assert (root / "run" / "finalpass2" / name).is_file(), name
assert (root / "eval_viewer_bio-metabolomics-isotope-tracing.md").is_file()
print("report_schema_and_arithmetic=PASS")
print("inputs=9; assertions=36/36; executed=6/9")
