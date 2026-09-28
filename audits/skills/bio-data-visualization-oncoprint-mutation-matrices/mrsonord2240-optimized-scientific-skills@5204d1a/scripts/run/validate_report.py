"""Pre-emit checklist and dispatch-specific validation for the re-audit report."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess
import sys


if len(sys.argv) != 3:
    raise SystemExit("usage: validate_report.py <report.json> <provider-worktree>")
report_path = Path(sys.argv[1])
worktree = Path(sys.argv[2])
report = json.loads(report_path.read_text(encoding="utf-8"))

assert set(report) == {"meta", "veto_gates", "static_score", "dynamic_score", "final", "key_strengths", "recommendations"}
meta = report["meta"]
assert meta["source"] == "mrsonord2240/optimized-scientific-skills@5204d1a4bc6069eac905b4422d6591ccc400ff3f:skills/bio-data-visualization-oncoprint-mutation-matrices"
assert meta["auditor_independent"] is True
assert meta["n_inputs"] == 9

skill_veto = report["veto_gates"]["skill_veto"]
assert set(skill_veto) == {"gate", "stability", "contract", "determinism", "security"}
assert all(value == "PASS" for value in skill_veto.values())
research = report["veto_gates"]["research_veto"]
assert set(research) == {"applicable", "gate", "scientific_integrity", "practice_boundaries", "methodological_ground", "code_usability"}
assert research["applicable"] is True and research["gate"] == "PASS"
assert all(research[key]["result"] == "PASS" for key in ("scientific_integrity", "practice_boundaries", "methodological_ground", "code_usability"))

expected_categories = {"functional_suitability", "reliability", "performance_context", "agent_usability", "human_usability", "security", "maintainability", "agent_specific"}
categories = report["static_score"]["categories"]
assert set(categories) == expected_categories
assert report["static_score"]["subtotal"] == sum(item["score"] for item in categories.values())
assert all(0 <= item["score"] <= item["max"] and item["note"] for item in categories.values())

inputs = report["dynamic_score"]["inputs"]
assert len(inputs) == meta["n_inputs"] == 9
all_passed = 0
all_assertions = 0
for expected_index, item in enumerate(inputs, start=1):
    assert item["index"] == expected_index
    assert 3 <= len(item["assertions"]) <= 5
    assert item["basic"] + item["specialized"] == item["total"]
    passed = sum(a["result"] == "PASS" for a in item["assertions"])
    assert passed == item["assertions_passed"]
    assert len(item["assertions"]) == item["assertions_total"]
    assert item["executed"] is True and item["execution_note"]
    all_passed += passed
    all_assertions += len(item["assertions"])

dynamic = report["dynamic_score"]
assert dynamic["execution_avg"] == round(sum(item["total"] for item in inputs) / len(inputs), 1)
assert dynamic["assertion_pass_rate"] == {"passed": all_passed, "total": all_assertions}
final = report["final"]
assert final["static_weighted"] == round(report["static_score"]["subtotal"] * 0.4, 1)
assert final["dynamic_weighted"] == round(dynamic["execution_avg"] * 0.6, 1)
assert final["score"] == round(final["static_weighted"] + final["dynamic_weighted"])
assert final["grade"] == "Production Ready" and final["grade_symbol"] == "⭐"
assert final["deployable"] is True and final["veto_override"] is False
assert 2 <= len(report["key_strengths"]) <= 5
priority_order = {"P0": 0, "P1": 1, "P2": 2}
assert [priority_order[x["priority"]] for x in report["recommendations"]] == sorted(priority_order[x["priority"]] for x in report["recommendations"])

head = subprocess.check_output(["git", "-C", str(worktree), "rev-parse", "HEAD"], text=True).strip()
status = subprocess.check_output(["git", "-C", str(worktree), "status", "--short"], text=True).strip()
assert head == "5204d1a4bc6069eac905b4422d6591ccc400ff3f" and status == ""
provider_skill = worktree / "skills" / "bio-data-visualization-oncoprint-mutation-matrices" / "SKILL.md"
audit_skill = report_path.parent / "run" / "skill" / "SKILL.md"
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(provider_skill) == sha(audit_skill)

print("REPORT VALIDATION PASS")
print("score", final["score"], "static", report["static_score"]["subtotal"], "dynamic", dynamic["execution_avg"])
print("inputs", len(inputs), "assertions", all_passed, "/", all_assertions)
print("source", meta["source"])
print("provider head", head, "clean", status == "", "source sha256", sha(provider_skill))
