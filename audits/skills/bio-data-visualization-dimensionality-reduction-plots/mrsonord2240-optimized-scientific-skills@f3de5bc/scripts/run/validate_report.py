"""Independent pre-emit validation of the generated report contract and totals."""
from __future__ import annotations

from pathlib import Path
import json

ROOT = Path(r"F:\OpenScience\audits\bio-data-visualization-dimensionality-reduction-plots")
path = ROOT / "eval_report_bio-data-visualization-dimensionality-reduction-plots_result.json"
report = json.loads(path.read_text(encoding="utf-8"))

assert list(report) == ["meta", "veto_gates", "static_score", "dynamic_score", "final", "key_strengths", "recommendations"]
assert report["meta"]["source"] == "mrsonord2240/optimized-scientific-skills@f3de5bc6421ca81d37ca532c1771e533a9af5cdf:skills/bio-data-visualization-dimensionality-reduction-plots"
assert report["meta"]["auditor_independent"] is True
assert report["meta"]["n_inputs"] == len(report["dynamic_score"]["inputs"]) == 9
categories = report["static_score"]["categories"]
assert len(categories) == 8
assert report["static_score"]["subtotal"] == sum(v["score"] for v in categories.values()) == 93
inputs = report["dynamic_score"]["inputs"]
assert all(item["executed"] is True for item in inputs)
assert all(3 <= len(item["assertions"]) <= 5 for item in inputs)
assert all(item["basic"] + item["specialized"] == item["total"] for item in inputs)
assert all(item["assertions_passed"] == sum(a["result"] == "PASS" for a in item["assertions"]) for item in inputs)
passed = sum(item["assertions_passed"] for item in inputs)
total = sum(item["assertions_total"] for item in inputs)
assert (passed, total) == (44, 45)
assert round(sum(item["total"] for item in inputs) / len(inputs), 1) == report["dynamic_score"]["execution_avg"] == 92.3
final = report["final"]
assert final["static_weighted"] == 37.2
assert final["dynamic_weighted"] == 55.4
assert final["score"] == 93 and final["grade"] == "Production Ready" and final["deployable"] is True
assert report["veto_gates"]["skill_veto"]["gate"] == "PASS"
assert report["veto_gates"]["research_veto"]["gate"] == "PASS"
assert [rec["priority"] for rec in report["recommendations"]] == ["P2", "P2", "P2"]
viewer = ROOT / "eval_viewer_bio-data-visualization-dimensionality-reduction-plots.md"
assert viewer.is_file() and viewer.stat().st_size > 10_000
print(f"VALID report bytes={path.stat().st_size} viewer bytes={viewer.stat().st_size} inputs=9 assertions={passed}/{total} final=93")
