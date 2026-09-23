"""Validate the Phase 2 report arithmetic and required final-pass provenance fields."""
import json
from pathlib import Path

ROOT = Path(r"F:\OpenScience\audits\bio-remote-homology")
REPORT = ROOT / "eval_report_bio-remote-homology_result.json"
VIEWER = ROOT / "eval_viewer_bio-remote-homology.md"
EXPECTED_SOURCE = "mrsonord2240/bioSkills@7153e877bfec221df95ba1f5758f4012e788b7aa:database-access/remote-homology"

report = json.loads(REPORT.read_text(encoding="utf-8"))
assert VIEWER.is_file()
assert report["meta"]["source"] == EXPECTED_SOURCE
assert report["meta"]["auditor_independent"] is False
assert report["meta"]["note"] == "final pass: fixed and audited under one brief, see CHECKPOINT.md"
assert len(report["dynamic_score"]["inputs"]) == report["meta"]["n_inputs"] == 11
assert sum(c["score"] for c in report["static_score"]["categories"].values()) == report["static_score"]["subtotal"] == 91
inputs = report["dynamic_score"]["inputs"]
for item in inputs:
    assert item["basic"] + item["specialized"] == item["total"]
    assert len(item["assertions"]) == item["assertions_total"]
    assert sum(a["result"] == "PASS" for a in item["assertions"]) == item["assertions_passed"]
avg = round(sum(i["total"] for i in inputs) / len(inputs), 1)
assert avg == report["dynamic_score"]["execution_avg"] == 93.4
assert round(report["static_score"]["subtotal"] * 0.4, 1) == report["final"]["static_weighted"] == 36.4
assert round(avg * 0.6, 1) == report["final"]["dynamic_weighted"] == 56.0
assert round(report["final"]["static_weighted"] + report["final"]["dynamic_weighted"]) == report["final"]["score"] == 92
assert report["final"]["grade"] == "Production Ready"
assert report["final"]["deployable"] is True
assert report["final"]["veto_override"] is False
assert [r["priority"] for r in report["recommendations"]] == ["P1", "P2"]
print("PASS: Phase 2 report, viewer, arithmetic, source tip, and auditor_independent flag validate.")
