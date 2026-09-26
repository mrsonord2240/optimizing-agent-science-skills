"""Validate report schema, arithmetic, floors, artifact presence, and source immutability."""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(r"F:\OpenScience\audits\bio-single-cell-cell-annotation\reaudit-optimized-scientific-skills@2dee47f-20260925")
SOURCE = Path(r"F:\OpenScience\audit-sources\optimized-scientific-skills-2dee47f")
REPORT = ROOT / "eval_report_bio-single-cell-cell-annotation_result.json"
data = json.loads(REPORT.read_text(encoding="utf-8"))

assert set(data) == {"meta", "veto_gates", "static_score", "dynamic_score", "final", "key_strengths", "recommendations"}
meta = data["meta"]
assert meta["evaluator_version"] == "skill-auditor@1.0"
assert meta["execution_mode"] in {"A", "B", "C", "D"}
assert meta["n_inputs"] == 7
assert meta["source"] == "mrsonord2240/optimized-scientific-skills@2dee47f80dac6f3ba5c78b53ea9ec132a87cf5db:skills/bio-single-cell-cell-annotation"
assert meta["auditor_independent"] is True

skill_veto = data["veto_gates"]["skill_veto"]
assert set(skill_veto) == {"gate", "stability", "contract", "determinism", "security"}
research_veto = data["veto_gates"]["research_veto"]
assert set(research_veto) == {"applicable", "gate", "scientific_integrity", "practice_boundaries", "methodological_ground", "code_usability"}
assert research_veto["applicable"] is True and research_veto["gate"] == "PASS"
for key in ("scientific_integrity", "practice_boundaries", "methodological_ground", "code_usability"):
    assert set(research_veto[key]) == {"result", "detail"}

expected_categories = {
    "functional_suitability": 12, "reliability": 12, "performance_context": 8,
    "agent_usability": 16, "human_usability": 8, "security": 12,
    "maintainability": 12, "agent_specific": 20,
}
categories = data["static_score"]["categories"]
assert set(categories) == set(expected_categories)
for key, maximum in expected_categories.items():
    item = categories[key]
    assert set(item) == {"score", "max", "note"}
    assert item["max"] == maximum and isinstance(item["score"], int) and 0 <= item["score"] <= maximum
    assert isinstance(item["note"], str) and item["note"]
static = sum(item["score"] for item in categories.values())
assert static == data["static_score"]["subtotal"] == 91

inputs = data["dynamic_score"]["inputs"]
assert len(inputs) == meta["n_inputs"]
passed = 0
total_assertions = 0
for index, item in enumerate(inputs, start=1):
    assert item["index"] == index
    assert item["status"] in {"COMPLETED", "PARTIAL", "ERROR"}
    assert item["basic"] + item["specialized"] == item["total"]
    assert all(isinstance(item[key], int) for key in ("basic", "specialized", "total", "assertions_passed", "assertions_total"))
    assertions = item["assertions"]
    assert 3 <= len(assertions) <= 5
    assert all(set(assertion) == {"text", "result", "note"} for assertion in assertions)
    observed_passes = sum(assertion["result"] == "PASS" for assertion in assertions)
    assert observed_passes == item["assertions_passed"]
    assert len(assertions) == item["assertions_total"]
    assert isinstance(item["executed"], bool) and item["execution_note"]
    if item["status"] == "COMPLETED":
        assert item["status_flag"] == ("✅" if item["total"] >= 75 else "⚠️")
    else:
        assert item["status_flag"] == "❌"
    passed += observed_passes
    total_assertions += len(assertions)

execution_avg = round(sum(item["total"] for item in inputs) / len(inputs), 1)
assert execution_avg == data["dynamic_score"]["execution_avg"] == 90.7
assert data["dynamic_score"]["assertion_pass_rate"] == {"passed": passed, "total": total_assertions}
assert (passed, total_assertions) == (33, 35)
assert sum(item["executed"] for item in inputs) == 5

final = data["final"]
assert final["static_weighted"] == round(static * 0.4, 1) == 36.4
assert final["dynamic_weighted"] == round(execution_avg * 0.6, 1) == 54.4
assert final["score"] == round(final["static_weighted"] + final["dynamic_weighted"]) == 91
assert final["grade"] == "Production Ready" and final["grade_symbol"] == "⭐"
assert final["deployable"] is True and final["veto_override"] is False

layer1_avg = round(sum(item["basic"] for item in inputs) / len(inputs), 1)
layer2_avg = round(sum(item["specialized"] for item in inputs) / len(inputs), 1)
assert static >= 80 and execution_avg >= 85 and layer1_avg >= 32 and layer2_avg >= 48
assert passed / total_assertions >= 0.90
assert 2 <= len(data["key_strengths"]) <= 5
priority_rank = {"P0": 0, "P1": 1, "P2": 2}
priorities = [item["priority"] for item in data["recommendations"]]
assert priorities == sorted(priorities, key=priority_rank.__getitem__)
assert priorities == ["P1", "P2", "P2"]

required_artifacts = [
    ROOT / "eval_viewer_bio-single-cell-cell-annotation.md",
    ROOT / "run" / "input1.log", ROOT / "run" / "input2.log", ROOT / "run" / "input2_clean.log",
    ROOT / "run" / "input3.log", ROOT / "run" / "input4.log", ROOT / "run" / "input5.log",
    ROOT / "run" / "input6.log", ROOT / "run" / "input7.log",
    ROOT / "run" / "validate_required_inputs.log", ROOT / "run" / "verify_seed_repeat.log",
    ROOT / "run" / "input2_wsl_probe.log", ROOT / "run" / "input2_wsl_install_interrupted.log",
    ROOT / "run" / "input2_wsl_partial_environment.yaml",
]
assert all(path.is_file() and path.stat().st_size > 0 for path in required_artifacts)

commit = subprocess.run(["git", "-C", str(SOURCE), "rev-parse", "HEAD"], check=True, text=True, capture_output=True).stdout.strip()
status = subprocess.run(["git", "-C", str(SOURCE), "status", "--porcelain"], check=True, text=True, capture_output=True).stdout
assert commit == "2dee47f80dac6f3ba5c78b53ea9ec132a87cf5db"
assert status == ""

lines = [
    "REPORT_SCHEMA_VALIDATION=PASS",
    f"static={static}", f"execution_avg={execution_avg}", f"layer1_avg={layer1_avg}", f"layer2_avg={layer2_avg}",
    f"assertions={passed}/{total_assertions}", "executed=5/7", "veto=none", "grade=Production Ready",
    f"source_commit={commit}", "source_worktree_clean=true",
]
(ROOT / "run" / "report_validation.log").write_text("\n".join(lines) + "\n", encoding="utf-8")
print("\n".join(lines))
