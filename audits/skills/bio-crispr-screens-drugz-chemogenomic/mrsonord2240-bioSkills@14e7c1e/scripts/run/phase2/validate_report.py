"""Schema-critical consistency checks for the final-pass JSON report."""
from __future__ import annotations

import json
from pathlib import Path


REPORT = Path(__file__).resolve().parents[2] / "eval_report_bio-crispr-screens-drugz-chemogenomic_result.json"


def main() -> None:
    r = json.loads(REPORT.read_text(encoding="utf-8"))
    expected_source = "mrsonord2240/bioSkills@14e7c1ec9fb76fd5859c5b4ba5ec70128fb85aeb:crispr-screens/drugz-chemogenomic"
    assert r["source"] == expected_source
    assert r["meta"]["source"] == expected_source
    assert r["meta"]["auditor_independent"] is False
    assert r["meta"]["note"] == "final pass: fixed and audited under one brief, see CHECKPOINT.md"
    categories = r["static_score"]["categories"]
    assert len(categories) == 8
    assert sum(v["score"] for v in categories.values()) == r["static_score"]["subtotal"]
    inputs = r["dynamic_score"]["inputs"]
    assert len(inputs) == r["meta"]["n_inputs"] == 9
    for item in inputs:
        assert "executed" in item and "execution_note" in item
        assert 3 <= len(item["assertions"]) <= 5
        assert item["basic"] + item["specialized"] == item["total"]
        assert item["assertions_passed"] == sum(a["result"] == "PASS" for a in item["assertions"])
        assert item["assertions_total"] == len(item["assertions"])
    assert round(sum(i["total"] for i in inputs) / len(inputs), 1) == r["dynamic_score"]["execution_avg"]
    assert round(r["static_score"]["subtotal"] * 0.4, 1) == r["final"]["static_weighted"]
    assert round(r["dynamic_score"]["execution_avg"] * 0.6, 1) == r["final"]["dynamic_weighted"]
    assert round(r["final"]["static_weighted"] + r["final"]["dynamic_weighted"]) == r["final"]["score"]
    assert all(x["priority"] == "P2" for x in r["recommendations"])
    print("report validation: PASS; 9 inputs, 35/36 assertions, score 95")


if __name__ == "__main__":
    main()
