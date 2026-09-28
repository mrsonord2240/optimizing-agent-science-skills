#!/usr/bin/env python3
"""Strict local validation for the initial ACMG audit record."""

from __future__ import annotations

import hashlib
import json
import pathlib
import re


ROOT = pathlib.Path(__file__).resolve().parents[1]
CANDIDATE = pathlib.Path(
    r"F:\OpenScience\wt\opt10-acmg-classification\skills\bio-clinical-databases-acmg-classification"
)
EXPECTED_IDENTITY = "719fd2d6eb6f21107a7b590de6d9c3c94930940d718509b7a9c43b55065f0678"


def candidate_identity() -> str:
    rows = []
    for path in sorted(
        (p for p in CANDIDATE.rglob("*") if p.is_file()),
        key=lambda p: p.relative_to(CANDIDATE).as_posix(),
    ):
        data = path.read_bytes()
        rows.append(
            f"{path.relative_to(CANDIDATE).as_posix()}\t{len(data)}\t{hashlib.sha256(data).hexdigest()}"
        )
    return hashlib.sha256("\n".join(rows).encode()).hexdigest()


report = json.loads((ROOT / "report.json").read_text(encoding="utf-8"))
identity = json.loads((ROOT / "source-identity.json").read_text(encoding="utf-8"))
evidence = json.loads((ROOT / "evidence" / "execution.json").read_text(encoding="utf-8"))
inputs = json.loads((ROOT / "inputs.json").read_text(encoding="utf-8"))

assert list(report) == [
    "meta", "veto_gates", "static_score", "dynamic_score", "final", "key_strengths", "recommendations"
]
assert report["meta"]["evaluator_version"] == "skill-auditor@1.0"
assert report["meta"]["n_inputs"] == len(inputs) == len(report["dynamic_score"]["inputs"]) == 7

expected_categories = {
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
assert set(categories) == set(expected_categories)
assert all(set(value) == {"score", "max", "note"} for value in categories.values())
assert all(value["max"] == expected_categories[key] for key, value in categories.items())
assert all(0 <= value["score"] <= value["max"] for value in categories.values())
assert report["static_score"]["subtotal"] == sum(value["score"] for value in categories.values())

rows = report["dynamic_score"]["inputs"]
assert [row["index"] for row in rows] == list(range(1, 8))
for row in rows:
    assert 3 <= len(row["assertions"]) <= 5
    assert row["assertions_total"] == len(row["assertions"])
    assert row["assertions_passed"] == sum(a["result"] == "PASS" for a in row["assertions"])
    assert row["basic"] + row["specialized"] == row["total"]
    assert all(a["result"] in {"PASS", "FAIL"} for a in row["assertions"])
passed = sum(row["assertions_passed"] for row in rows)
total = sum(row["assertions_total"] for row in rows)
assert report["dynamic_score"]["assertion_pass_rate"] == {"passed": passed, "total": total}
assert report["dynamic_score"]["execution_avg"] == round(sum(row["total"] for row in rows) / len(rows), 1)

final = report["final"]
assert final["static_weighted"] == round(report["static_score"]["subtotal"] * 0.4, 1)
assert final["dynamic_weighted"] == round(report["dynamic_score"]["execution_avg"] * 0.6, 1)
assert final["score"] == round(final["static_weighted"] + final["dynamic_weighted"])
assert final["grade"] == "Reject" and final["grade_symbol"] == "❌"
assert final["veto_override"] is True and final["deployable"] is False
assert report["veto_gates"]["research_veto"]["gate"] == "FAIL"
assert 2 <= len(report["key_strengths"]) <= 5

priority_rank = {"P0": 0, "P1": 1, "P2": 2}
assert [priority_rank[item["priority"]] for item in report["recommendations"]] == sorted(
    priority_rank[item["priority"]] for item in report["recommendations"]
)
assert [re.match(r"ACMG-(\d{3})", item["title"]).group(0) for item in report["recommendations"]] == [
    f"ACMG-{index:03d}" for index in range(1, 10)
]

assert candidate_identity() == EXPECTED_IDENTITY
assert identity["candidate"]["identity"] == EXPECTED_IDENTITY
assert evidence["candidate_identity"]["digest"] == EXPECTED_IDENTITY
assert len(identity["files"]) == evidence["candidate_identity"]["file_count"] == 5
assert (ROOT / "viewer.md").is_file()
assert (ROOT / "finding-ledger.md").is_file()
assert (ROOT / "scientific-source-notes.md").is_file()
assert (ROOT / "execution-classifications.json").is_file()

print(json.dumps({
    "schema": "PASS",
    "score": final["score"],
    "assertions": f"{passed}/{total}",
    "identity": EXPECTED_IDENTITY,
    "findings": len(report["recommendations"]),
}, sort_keys=True))
