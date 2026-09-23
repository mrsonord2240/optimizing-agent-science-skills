"""Validate report arithmetic, required final-pass metadata, and audit artifacts."""
import json
from pathlib import Path

AUDIT = Path(r"F:\OpenScience\audits\bio-crispr-screens-jacks-analysis")
report = json.loads((AUDIT / "eval_report_bio-crispr-screens-jacks-analysis_result.json").read_text(encoding="utf-8"))
assert report["meta"]["source"] == "mrsonord2240/bioSkills@d1b1b166dcd771e115e8564fb7969260e791c39f:crispr-screens/jacks-analysis"
assert report["meta"]["auditor_independent"] is False
assert report["meta"]["note"] == "final pass: fixed and audited under one brief, see CHECKPOINT.md"
inputs = report["dynamic_score"]["inputs"]
assert len(inputs) == report["meta"]["n_inputs"] == 9
assert all(i["executed"] is True and i["execution_note"] for i in inputs)
assert all(3 <= len(i["assertions"]) <= 5 for i in inputs)
assert all(i["basic"] + i["specialized"] == i["total"] for i in inputs)
assert sum(c["score"] for c in report["static_score"]["categories"].values()) == report["static_score"]["subtotal"] == 97
avg = round(sum(i["total"] for i in inputs) / len(inputs), 1)
assert avg == report["dynamic_score"]["execution_avg"] == 93.7
assert report["final"]["score"] == round(report["final"]["static_weighted"] + report["final"]["dynamic_weighted"]) == 95
assert report["final"]["deployable"] is True and report["final"]["veto_override"] is False
assert (AUDIT / "eval_viewer_bio-crispr-screens-jacks-analysis.md").exists()
assert all((AUDIT / "run" / f"input{n}_{suffix}.py").exists() for n, suffix in [(1,"canonical_joint"),(2,"single_screen_hap1"),(3,"wrong_library_prior"),(4,"shipped_example_script"),(5,"crispri_hyperparam_override"),(6,"mismatched_naming"),(7,"determinism_itercap_pval"),(8,"reffile_output_contract"),(9,"relative_wrapper_and_summary")])
print("PASS: schema arithmetic, final-pass metadata, viewer, and 9 saved input scripts validated")
