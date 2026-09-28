#!/usr/bin/env python3
"""Strict local validator for the modular ACMG re-audit record."""

from __future__ import annotations

import hashlib
import json
import pathlib
import re


ROOT = pathlib.Path(__file__).resolve().parents[1]
CANDIDATE = pathlib.Path(
    r"F:\OpenScience\wt\opt10-acmg-classification\skills\bio-clinical-databases-acmg-classification"
)
EXPECTED_IDENTITY = "926ce0436d0d9fd1fb73a5f2b83728adfb622cf6f8ec41c8c00ad8d8300e8c07"


def candidate_identity() -> tuple[str, list[dict]]:
    rows = []
    files = []
    for path in sorted(
        (p for p in CANDIDATE.rglob("*") if p.is_file()),
        key=lambda p: p.relative_to(CANDIDATE).as_posix(),
    ):
        relative = path.relative_to(CANDIDATE).as_posix()
        data = path.read_bytes()
        digest = hashlib.sha256(data).hexdigest()
        rows.append(f"{relative}\t{len(data)}\t{digest}")
        files.append({"path": relative, "bytes": len(data), "sha256": digest})
    return hashlib.sha256("\n".join(rows).encode("utf-8")).hexdigest(), files


report = json.loads((ROOT / "report.json").read_text(encoding="utf-8"))
identity = json.loads((ROOT / "source-identity.json").read_text(encoding="utf-8"))
execution = json.loads((ROOT / "evidence" / "execution.json").read_text(encoding="utf-8"))
inputs = json.loads((ROOT / "inputs.json").read_text(encoding="utf-8"))

assert list(report) == [
    "meta", "veto_gates", "static_score", "dynamic_score", "final", "key_strengths", "recommendations"
]
assert report["meta"]["evaluator_version"] == "skill-auditor@1.0"
assert report["meta"]["category"] == "Data Analysis"
assert report["meta"]["execution_mode"] == "D"
assert report["meta"]["n_inputs"] == len(inputs) == len(report["dynamic_score"]["inputs"]) == 7

skill_veto = report["veto_gates"]["skill_veto"]
assert set(skill_veto) == {"gate", "stability", "contract", "determinism", "security"}
assert skill_veto["gate"] == "PASS" and all(skill_veto[key] == "PASS" for key in skill_veto if key != "gate")
research = report["veto_gates"]["research_veto"]
assert set(research) == {
    "applicable", "gate", "scientific_integrity", "practice_boundaries", "methodological_ground", "code_usability"
}
assert research["applicable"] is True and research["gate"] == "FAIL"
assert research["methodological_ground"]["result"] == "FAIL"
assert research["scientific_integrity"]["result"] == "PASS"
assert research["practice_boundaries"]["result"] == "PASS"
assert research["code_usability"]["result"] == "PASS"

category_max = {
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
assert set(categories) == set(category_max)
assert all(set(value) == {"score", "max", "note"} for value in categories.values())
assert all(value["max"] == category_max[key] for key, value in categories.items())
assert all(isinstance(value["score"], int) and 0 <= value["score"] <= value["max"] for value in categories.values())
assert report["static_score"]["subtotal"] == sum(value["score"] for value in categories.values()) == 76

rows = report["dynamic_score"]["inputs"]
assert [row["index"] for row in rows] == list(range(1, 8))
assert [item["index"] for item in inputs] == list(range(1, 8))
for row in rows:
    assert row["status"] in {"COMPLETED", "PARTIAL", "ERROR"}
    assert row["status_flag"] in {"✅", "⚠️", "❌"}
    assert isinstance(row["basic"], int) and 0 <= row["basic"] <= 40
    assert isinstance(row["specialized"], int) and 0 <= row["specialized"] <= 60
    assert row["basic"] + row["specialized"] == row["total"]
    assert 3 <= len(row["assertions"]) <= 5
    assert row["assertions_total"] == len(row["assertions"])
    assert row["assertions_passed"] == sum(item["result"] == "PASS" for item in row["assertions"])
    assert all(set(item) == {"text", "result", "note"} for item in row["assertions"])
    assert all(item["result"] in {"PASS", "FAIL"} for item in row["assertions"])

passed = sum(row["assertions_passed"] for row in rows)
total = sum(row["assertions_total"] for row in rows)
assert report["dynamic_score"]["assertion_pass_rate"] == {"passed": passed, "total": total} == {"passed": 26, "total": 35}
execution_avg = round(sum(row["total"] for row in rows) / len(rows), 1)
assert report["dynamic_score"]["execution_avg"] == execution_avg == 75.9

final = report["final"]
assert final["static_weighted"] == round(76 * 0.4, 1) == 30.4
assert final["dynamic_weighted"] == round(execution_avg * 0.6, 1) == 45.5
assert final["score"] == round(final["static_weighted"] + final["dynamic_weighted"]) == 76
assert final["grade"] == "Reject" and final["grade_symbol"] == "❌"
assert final["deployable"] is False and final["veto_override"] is True
assert 2 <= len(report["key_strengths"]) <= 5
assert [item["priority"] for item in report["recommendations"]] == ["P0", "P1", "P2"]
assert [re.match(r"ACMG-\d{3}", item["title"]).group(0) for item in report["recommendations"]] == [
    "ACMG-006", "ACMG-002", "ACMG-001"
]

digest, files = candidate_identity()
assert digest == EXPECTED_IDENTITY
assert identity["candidate"]["identity"] == EXPECTED_IDENTITY
assert identity["candidate"]["file_count"] == len(files) == 7
assert identity["files"] == files
assert execution["candidate_identity_before"]["digest"] == EXPECTED_IDENTITY
assert execution["candidate_identity_after"]["digest"] == EXPECTED_IDENTITY
assert execution["candidate_identity_before"]["files"] == execution["candidate_identity_after"]["files"] == files
assert not any(path.name == "__pycache__" or path.suffix == ".pyc" for path in CANDIDATE.rglob("*"))

for path in [
    "viewer.md", "finding-ledger.md", "scientific-source-notes.md", "execution-classifications.json",
    "evidence/unit-tests.log", "evidence/standalone-demo.log", "evidence/live-interface-smoke.log",
]:
    assert (ROOT / path).is_file(), path

hashes = json.loads((ROOT / "artifact-hashes.json").read_text(encoding="utf-8"))
assert len(hashes) == len({row["path"] for row in hashes})
for row in hashes:
    data = (ROOT / row["path"]).read_bytes()
    assert row["bytes"] == len(data), row["path"]
    assert row["sha256"] == hashlib.sha256(data).hexdigest(), row["path"]

print(json.dumps({
    "schema": "PASS",
    "identity": digest,
    "score": final["score"],
    "grade": final["grade"],
    "assertions": f"{passed}/{total}",
    "research_veto": research["gate"],
    "open_findings": ["ACMG-001", "ACMG-002", "ACMG-006"],
}, sort_keys=True))
