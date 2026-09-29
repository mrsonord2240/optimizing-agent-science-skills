#!/usr/bin/env python3
"""Validate the strict final re-audit record and exact candidate binding."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


RUN = Path(__file__).resolve().parent
CANDIDATE = Path(r"F:\OpenScience\wt\opt10-codon-usage\skills\bio-codon-usage")
EXPECTED_IDENTITY = "3186a1debc804852b3ea016b9aeabebc4436a04791b84b13dba8669878d7e4dd"


def manifest(root: Path) -> tuple[bytes, int]:
    rows: list[str] = []
    files = sorted(
        (path for path in root.rglob("*") if path.is_file()),
        key=lambda path: path.relative_to(root).as_posix(),
    )
    for path in files:
        relative = path.relative_to(root).as_posix()
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        rows.append(f"{relative}\t{path.stat().st_size}\t{digest}")
    return "\n".join(rows).encode("utf-8"), len(files)


report = json.loads((RUN / "report.json").read_text(encoding="utf-8"))
source = json.loads((RUN / "source-identity.json").read_text(encoding="utf-8"))
inputs = json.loads((RUN / "generated-test-inputs.json").read_text(encoding="utf-8"))
execution = json.loads((RUN / "reaudit-results.json").read_text(encoding="utf-8"))
structural = json.loads((RUN / "evidence" / "structural-precheck.json").read_text(encoding="utf-8"))

required_top = {
    "meta",
    "veto_gates",
    "static_score",
    "dynamic_score",
    "final",
    "key_strengths",
    "recommendations",
}
assert set(report) == required_top
assert report["meta"]["n_inputs"] == len(inputs["inputs"]) == 5
assert report["meta"]["category"] == "Data Analysis"
assert report["meta"]["execution_mode"] == "B"
assert report["meta"]["complexity"] == "Moderate"
assert report["meta"]["evaluator_version"] == "skill-auditor@1.0"

skill_veto = report["veto_gates"]["skill_veto"]
assert set(skill_veto) == {"gate", "stability", "contract", "determinism", "security"}
assert all(value == "PASS" for value in skill_veto.values())
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
    assert research_veto[key]["result"] == "PASS" and research_veto[key]["detail"]

categories = report["static_score"]["categories"]
expected_categories = {
    "functional_suitability",
    "reliability",
    "performance_context",
    "agent_usability",
    "human_usability",
    "security",
    "maintainability",
    "agent_specific",
}
assert set(categories) == expected_categories
assert sum(item["score"] for item in categories.values()) == report["static_score"]["subtotal"] == 96
assert all(set(item) == {"score", "max", "note"} for item in categories.values())
assert all(0 <= item["score"] <= item["max"] and item["note"] for item in categories.values())

rows = report["dynamic_score"]["inputs"]
assert len(rows) == 5
passed = 0
total = 0
for index, row in enumerate(rows, start=1):
    assert row["index"] == index
    assert row["type"] == inputs["inputs"][index - 1]["type"]
    assert row["label"] == inputs["inputs"][index - 1]["label"]
    assert row["status"] == "COMPLETED" and row["status_flag"] == "✅"
    assert row["basic"] + row["specialized"] == row["total"]
    assert 3 <= len(row["assertions"]) <= 5
    assert all(set(item) == {"text", "result", "note"} for item in row["assertions"])
    assert all(item["result"] in {"PASS", "FAIL"} for item in row["assertions"])
    row_passed = sum(item["result"] == "PASS" for item in row["assertions"])
    assert row_passed == row["assertions_passed"]
    assert len(row["assertions"]) == row["assertions_total"]
    passed += row_passed
    total += len(row["assertions"])

average = round(sum(row["total"] for row in rows) / len(rows), 1)
assert average == report["dynamic_score"]["execution_avg"] == 97.4
assert report["dynamic_score"]["assertion_pass_rate"] == {"passed": passed, "total": total}
assert passed == total == 25

final = report["final"]
assert final["static_weighted"] == round(96 * 0.4, 1) == 38.4
assert final["dynamic_weighted"] == round(97.4 * 0.6, 1) == 58.4
assert final["score"] == round(final["static_weighted"] + final["dynamic_weighted"]) == 97
assert final["grade"] == "Production Ready" and final["grade_symbol"] == "⭐"
assert final["deployable"] is True and final["veto_override"] is False
assert 2 <= len(report["key_strengths"]) <= 5
assert report["recommendations"] == []

manifest_bytes, file_count = manifest(CANDIDATE)
observed_identity = hashlib.sha256(manifest_bytes).hexdigest()
assert observed_identity == EXPECTED_IDENTITY
assert (RUN / "candidate-manifest.tsv").read_bytes() == manifest_bytes
assert source["candidate"]["identity"] == EXPECTED_IDENTITY
assert source["candidate"]["file_count"] == file_count == 11
assert source["candidate"]["manifest_bytes"] == len(manifest_bytes) == 1051

assert execution["summary"]["passed"] == execution["summary"]["total"] == 57
assert execution["summary"]["failed"] == []
assert execution["runtime"]["biopython"] == "1.85"
assert all(item["pass"] is True for item in execution["checks"])
assert all(value == "PASS" for value in structural["step1_basic_veto"].values())
assert structural["step4_complexity"] == {"level": "Moderate", "n_inputs": 5}

required_files = [
    "report.json",
    "viewer.md",
    "source-identity.json",
    "candidate-manifest.tsv",
    "generated-test-inputs.json",
    "finding-ledger.md",
    "reaudit_harness.py",
    "reaudit-results.json",
    "reaudit-stderr.txt",
    "evidence/execution-classification.md",
    "evidence/scientific-source-notes.md",
    "evidence/commands.txt",
    "evidence/structural-precheck.json",
    "evidence/structural-precheck.stderr.txt",
]
assert all((RUN / relative).is_file() for relative in required_files)

result = {
    "schema": "scientific-skill-audit.validation.v1",
    "status": "PASS",
    "candidate_identity": observed_identity,
    "candidate_file_count": file_count,
    "candidate_manifest_bytes": len(manifest_bytes),
    "execution_checks": {"passed": 57, "total": 57},
    "static_score": 96,
    "execution_average": average,
    "assertions": {"passed": passed, "total": total},
    "final_score": 97,
    "grade": "Production Ready",
    "veto_gates": {"skill": "PASS", "research": "PASS"},
    "recommendation_count": 0,
    "required_files_checked": len(required_files),
}
(RUN / "evidence" / "schema-validation.json").write_text(
    json.dumps(result, indent=2) + "\n", encoding="utf-8"
)
print(json.dumps(result, indent=2))
