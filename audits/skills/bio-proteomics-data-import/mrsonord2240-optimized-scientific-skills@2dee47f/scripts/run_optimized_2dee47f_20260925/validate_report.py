"""Validate report schema arithmetic, evidence completeness, and immutable-source identity."""
from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path


AUDIT = Path(__file__).resolve().parents[1]
RUN = AUDIT / "run"
SOURCE_REPO = Path(r"F:\OpenScience\audit-sources\optimized-scientific-skills-2dee47f")
SOURCE_SKILL = SOURCE_REPO / "skills" / "bio-proteomics-data-import"
EXPECTED_COMMIT = "2dee47f80dac6f3ba5c78b53ea9ec132a87cf5db"
REPORT_PATH = AUDIT / "eval_report_bio-proteomics-data-import_result.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


report = json.loads(REPORT_PATH.read_text(encoding="utf-8"))
assert set(report) == {
    "meta",
    "veto_gates",
    "static_score",
    "dynamic_score",
    "final",
    "key_strengths",
    "recommendations",
}
meta = report["meta"]
assert meta["evaluator_version"] == "skill-auditor@1.0"
assert meta["evaluated_on"] == "2026-09-25"
assert meta["n_inputs"] == 7
assert meta["auditor_independent"] is True
assert meta["source"] == f"mrsonord2240/optimized-scientific-skills@{EXPECTED_COMMIT}:skills/bio-proteomics-data-import"

skill_veto = report["veto_gates"]["skill_veto"]
assert set(skill_veto) == {"gate", "stability", "contract", "determinism", "security"}
assert skill_veto["gate"] == "PASS"
assert all(skill_veto[key] == "PASS" for key in ("stability", "contract", "determinism", "security"))
research_veto = report["veto_gates"]["research_veto"]
assert set(research_veto) == {
    "applicable",
    "gate",
    "scientific_integrity",
    "practice_boundaries",
    "methodological_ground",
    "code_usability",
}
assert research_veto["applicable"] is True and research_veto["gate"] == "PASS"
for key in ("scientific_integrity", "practice_boundaries", "methodological_ground", "code_usability"):
    assert set(research_veto[key]) == {"result", "detail"}
    assert research_veto[key]["result"] == "PASS"
    assert research_veto[key]["detail"]

category_maxima = {
    "functional_suitability": 12,
    "reliability": 12,
    "performance_context": 8,
    "agent_usability": 16,
    "human_usability": 8,
    "security": 12,
    "maintainability": 12,
    "agent_specific": 20,
}
categories = report["static_score"]["categories"]
assert set(categories) == set(category_maxima)
for key, maximum in category_maxima.items():
    value = categories[key]
    assert set(value) == {"score", "max", "note"}
    assert value["max"] == maximum and 0 <= value["score"] <= maximum and value["note"]
assert report["static_score"]["subtotal"] == sum(v["score"] for v in categories.values()) == 94
assert report["static_score"]["max"] == 100

inputs = report["dynamic_score"]["inputs"]
assert len(inputs) == meta["n_inputs"] == 7
assert [item["index"] for item in inputs] == list(range(1, 8))
passed = 0
total = 0
totals = []
allowed_types = {"Canonical", "Variant A", "Variant B", "Edge", "Stress", "Scope Boundary", "Adversarial"}
for item in inputs:
    assert item["type"] in allowed_types
    assert item["status"] in {"COMPLETED", "PARTIAL", "ERROR"}
    assert item["status_flag"] in {"✅", "⚠️", "❌"}
    assert item["executed"] is True and item["execution_note"]
    assertions = item["assertions"]
    assert 3 <= len(assertions) <= 5
    for assertion in assertions:
        assert set(assertion) == {"text", "result", "note"}
        assert assertion["result"] in {"PASS", "FAIL"}
        assert assertion["text"] and assertion["note"]
    observed_passed = sum(a["result"] == "PASS" for a in assertions)
    assert item["assertions_passed"] == observed_passed
    assert item["assertions_total"] == len(assertions)
    assert item["basic"] + item["specialized"] == item["total"]
    if item["status"] == "COMPLETED" and item["total"] >= 75:
        assert item["status_flag"] == "✅"
    passed += observed_passed
    total += len(assertions)
    totals.append(item["total"])
assert report["dynamic_score"]["assertion_pass_rate"] == {"passed": passed, "total": total}
assert (passed, total) == (34, 35)
execution_avg = round(sum(totals) / len(totals), 1)
assert report["dynamic_score"]["execution_avg"] == execution_avg == 95.1
assert report["dynamic_score"]["max"] == 100

final = report["final"]
assert final["static_weighted"] == round(report["static_score"]["subtotal"] * 0.4, 1) == 37.6
assert final["dynamic_weighted"] == round(execution_avg * 0.6, 1) == 57.1
assert final["score"] == round(final["static_weighted"] + final["dynamic_weighted"]) == 95
assert final["grade"] == "Production Ready" and final["grade_symbol"] == "⭐"
assert final["deployable"] is True and final["veto_override"] is False
assert 2 <= len(report["key_strengths"]) <= 5 and all(isinstance(x, str) and x for x in report["key_strengths"])
priority_order = {"P0": 0, "P1": 1, "P2": 2}
priorities = [priority_order[item["priority"]] for item in report["recommendations"]]
assert priorities == sorted(priorities)
for recommendation in report["recommendations"]:
    assert set(recommendation) == {"priority", "title", "observed_in", "problem", "root_cause", "fix"}
    assert recommendation["priority"] in priority_order

head = subprocess.run(
    ["git", "rev-parse", "HEAD"], cwd=SOURCE_REPO, check=True, capture_output=True, text=True
).stdout.strip()
status = subprocess.run(
    ["git", "status", "--short"], cwd=SOURCE_REPO, check=True, capture_output=True, text=True
).stdout.strip()
assert head == EXPECTED_COMMIT
assert status == ""
for name in ("inspect_mzml.py", "load_diann.py", "load_maxquant.py", "load_maxquant_qfeatures.R"):
    assert sha256(SOURCE_SKILL / "examples" / name) == sha256(RUN / "source_examples" / name)

execution = json.loads((RUN / "execution-summary.json").read_text(encoding="utf-8"))
by_name = {item["name"]: item for item in execution}
for name in (
    "input1_maxquant_lfq",
    "input2_diann",
    "input3_mzml",
    "input4_column_choice",
    "input5_combined_missingness",
    "input6_tmt",
    "input7_wrong_table",
    "input4_qfeatures_wsl",
):
    assert by_name[name]["exit_code"] == 0 and by_name[name]["timed_out"] is False
assert by_name["input4_qfeatures_windows"]["exit_code"] == 139
assert by_name["input4_qfeatures_windows"]["expected_success"] is False
assert "Segmentation fault" in (RUN / "input4_qfeatures_windows.stderr.log").read_text(encoding="utf-8", errors="replace")
skill_text = (SOURCE_SKILL / "SKILL.md").read_text(encoding="utf-8")
assert "0xC0000005" in skill_text and "WSL/Linux" in skill_text and "Treat the nonzero exit as failure" in skill_text
for item in execution:
    assert (RUN / item["stdout"]).is_file()
    assert (RUN / item["stderr"]).is_file()
assert (AUDIT / "eval_viewer_bio-proteomics-data-import.md").is_file()

print(
    json.dumps(
        {
            "schema_arithmetic": "PASS",
            "source_commit": head,
            "source_clean": True,
            "exact_example_copies": 4,
            "inputs_executed": len(inputs),
            "assertions": f"{passed}/{total}",
            "execution_avg": execution_avg,
            "final_score": final["score"],
            "grade": final["grade"],
            "wsl_qfeatures_exit": by_name["input4_qfeatures_wsl"]["exit_code"],
            "windows_qfeatures_exit": by_name["input4_qfeatures_windows"]["exit_code"],
        },
        indent=2,
    )
)
