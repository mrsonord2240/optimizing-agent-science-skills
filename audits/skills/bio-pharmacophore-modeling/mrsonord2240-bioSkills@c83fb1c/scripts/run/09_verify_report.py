"""Validate required audit-report arithmetic and current-source identity."""
import json
import subprocess
from pathlib import Path

audit = Path(__file__).parents[1]
report = json.loads((audit / "eval_report_bio-pharmacophore-modeling_result.json").read_text(encoding="utf-8"))
assert report["meta"]["auditor_independent"] is False
assert report["meta"]["note"] == "final pass: fixed and audited under one brief, see CHECKPOINT.md"
assert report["meta"]["source"] == "mrsonord2240/bioSkills@c83fb1c4c8c3c40079e8cf653c3ed266fa7b1d8c:chemoinformatics/pharmacophore-modeling"
inputs = report["dynamic_score"]["inputs"]
assert len(inputs) == report["meta"]["n_inputs"] == 7
for row in inputs:
    assert row["executed"] is True
    assert isinstance(row["execution_note"], str) and row["execution_note"]
    assert 3 <= len(row["assertions"]) <= 5
    assert row["basic"] + row["specialized"] == row["total"]
    assert row["assertions_passed"] == sum(a["result"] == "PASS" for a in row["assertions"])
assert report["dynamic_score"]["execution_avg"] == round(sum(x["total"] for x in inputs) / len(inputs), 1)
assert report["dynamic_score"]["assertion_pass_rate"] == {"passed": 29, "total": 29}
assert report["static_score"]["subtotal"] == sum(x["score"] for x in report["static_score"]["categories"].values())
assert report["final"]["static_weighted"] == round(report["static_score"]["subtotal"] * 0.4, 1)
assert report["final"]["dynamic_weighted"] == round(report["dynamic_score"]["execution_avg"] * 0.6, 1)
assert report["final"]["score"] == round(report["final"]["static_weighted"] + report["final"]["dynamic_weighted"])
worktree = Path("F:/OpenScience/wt/chemoinformatics-pharmacophore-modeling")
tip = subprocess.check_output(["git", "-C", str(worktree), "rev-parse", "HEAD"], text=True).strip()
assert tip == "c83fb1c4c8c3c40079e8cf653c3ed266fa7b1d8c", tip
print("ASSERT report schema arithmetic, final-pass metadata, and exact source tip: PASS")
