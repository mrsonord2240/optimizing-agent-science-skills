#!/usr/bin/env python3
"""Strict schema, identity, execution, and hash validator for the final re-audit."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CANDIDATE = Path(
    r"F:\OpenScience\wt\opt10-acmg-classification\skills\bio-clinical-databases-acmg-classification"
)
EXPECTED_IDENTITY = "286df2647ef2e418d8302102c7522705f7b5ce4156cfaea6be5c8c36c6d55571"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def candidate_manifest() -> tuple[str, list[dict[str, object]], int]:
    rows = []
    files = []
    for path in sorted(
        (item for item in CANDIDATE.rglob("*") if item.is_file()),
        key=lambda item: item.relative_to(CANDIDATE).as_posix(),
    ):
        relative = path.relative_to(CANDIDATE).as_posix()
        digest = sha256(path)
        size = path.stat().st_size
        rows.append(f"{relative}\t{size}\t{digest}")
        files.append({"path": relative, "bytes": size, "sha256": digest})
    manifest = "\n".join(rows).encode("utf-8")
    return hashlib.sha256(manifest).hexdigest(), files, len(manifest)


report = json.loads((ROOT / "report.json").read_text(encoding="utf-8"))
identity = json.loads((ROOT / "source-identity.json").read_text(encoding="utf-8"))
execution = json.loads((ROOT / "evidence" / "execution.json").read_text(encoding="utf-8"))
inputs = json.loads((ROOT / "inputs.json").read_text(encoding="utf-8"))
classes = json.loads((ROOT / "execution-classifications.json").read_text(encoding="utf-8"))
hashes = json.loads((ROOT / "artifact-hashes.json").read_text(encoding="utf-8"))

assert list(report) == [
    "meta", "veto_gates", "static_score", "dynamic_score", "final", "key_strengths", "recommendations"
]
assert report["meta"] == {
    "skill_name": "bio-clinical-databases-acmg-classification",
    "description": report["meta"]["description"],
    "evaluated_on": "2026-09-28",
    "evaluator_version": "skill-auditor@1.0",
    "category": "Data Analysis",
    "execution_mode": "D",
    "complexity": "Complex",
    "n_inputs": 7,
}
assert report["meta"]["description"]

skill_veto = report["veto_gates"]["skill_veto"]
assert set(skill_veto) == {"gate", "stability", "contract", "determinism", "security"}
assert skill_veto["gate"] == "PASS"
assert all(skill_veto[key] == "PASS" for key in ("stability", "contract", "determinism", "security"))
research = report["veto_gates"]["research_veto"]
assert set(research) == {
    "applicable", "gate", "scientific_integrity", "practice_boundaries", "methodological_ground", "code_usability"
}
assert research["applicable"] is True and research["gate"] == "PASS"
for key in ("scientific_integrity", "practice_boundaries", "methodological_ground", "code_usability"):
    assert research[key]["result"] == "PASS" and research[key]["detail"]

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
assert report["static_score"]["subtotal"] == sum(value["score"] for value in categories.values()) == 95
assert report["static_score"]["max"] == 100

rows = report["dynamic_score"]["inputs"]
assert len(rows) == len(inputs) == report["meta"]["n_inputs"] == 7
assert [row["index"] for row in rows] == list(range(1, 8))
assert [item["index"] for item in inputs] == list(range(1, 8))
passed = 0
total = 0
for row in rows:
    assert row["status"] == "COMPLETED" and row["status_flag"] == "✅"
    assert row["basic"] + row["specialized"] == row["total"]
    assertions = row["assertions"]
    assert 3 <= len(assertions) <= 5
    assert all(set(item) == {"text", "result", "note"} for item in assertions)
    assert all(item["result"] in {"PASS", "FAIL"} for item in assertions)
    row_passed = sum(item["result"] == "PASS" for item in assertions)
    assert row["assertions_passed"] == row_passed
    assert row["assertions_total"] == len(assertions)
    passed += row_passed
    total += len(assertions)
average = round(sum(row["total"] for row in rows) / len(rows), 1)
assert average == report["dynamic_score"]["execution_avg"] == 97.3
assert report["dynamic_score"]["assertion_pass_rate"] == {"passed": passed, "total": total}
assert (passed, total) == (28, 28)

final = report["final"]
assert final["static_weighted"] == round(95 * 0.4, 1) == 38.0
assert final["dynamic_weighted"] == round(97.3 * 0.6, 1) == 58.4
assert final["score"] == round(final["static_weighted"] + final["dynamic_weighted"]) == 96
assert final == {
    "static_weighted": 38.0,
    "dynamic_weighted": 58.4,
    "score": 96,
    "max": 100,
    "grade": "Production Ready",
    "grade_symbol": "⭐",
    "deployable": True,
    "veto_override": False,
}
assert 2 <= len(report["key_strengths"]) <= 5
assert report["recommendations"] == []

actual_identity, files, manifest_bytes = candidate_manifest()
assert actual_identity == EXPECTED_IDENTITY
assert identity["schema"] == "sha256-manifest-v1"
assert identity["origin"] == {
    "repository": "GPTomics/bioSkills",
    "commit": "d91ed3d563019e649dc854c56ccd62551359488a",
    "path": "clinical-databases/acmg-classification",
    "subtree": "b4c1f4dd04a6a53f3eba2aa56da5d830ba325e1a",
}
assert identity["candidate"]["identity"] == EXPECTED_IDENTITY
assert identity["candidate"]["manifest_bytes"] == manifest_bytes == 644
assert identity["candidate"]["file_count"] == len(files) == 7
assert identity["files"] == files
assert execution["candidate_identity"]["content_sha256"] == EXPECTED_IDENTITY
assert execution["all_checks_pass"] is True
assert len(execution["invalid_probes"]) == 25
assert sum(len(value) for value in execution["predictor_endpoints"].values()) == 26
assert len(execution["pvs1"]["states"]) == 9
assert len(execution["pvs1"]["contradictions"]) == 3
assert len(execution["oddspath"]) == 14
assert len(execution["somatic_tiers"]) == 6
assert execution["live_interfaces"]["genebe"]["variant_records"] >= 1
assert execution["live_interfaces"]["cspec"]["version_records"] >= 1
assert classes["candidate_identity"] == EXPECTED_IDENTITY
assert all(item["status"] == "PASS" for item in classes["surfaces"] if item["classification"] == "EXECUTED")

unit_log = (ROOT / "evidence" / "unit-tests.log").read_text(encoding="utf-8")
assert "Ran 24 tests" in unit_log and unit_log.rstrip().endswith("OK")
assert "GeneBe coordinate contract: PASS" in (ROOT / "evidence" / "live-interface-smoke.log").read_text(encoding="utf-8")
assert "CSpec versioned-gene contract: PASS" in (ROOT / "evidence" / "live-interface-smoke.log").read_text(encoding="utf-8")
assert "NON-DIAGNOSTIC TRAINING EXAMPLE" in (ROOT / "evidence" / "standalone-demo.log").read_text(encoding="utf-8")
assert "compile=PASS" in (ROOT / "evidence" / "preflight.log").read_text(encoding="utf-8")

assert len(hashes) == len({item["path"] for item in hashes})
for item in hashes:
    path = ROOT / item["path"]
    assert path.is_file(), item["path"]
    assert path.stat().st_size == item["bytes"], item["path"]
    assert sha256(path) == item["sha256"], item["path"]

assert not any(path.name == "__pycache__" or path.suffix == ".pyc" for path in CANDIDATE.rglob("*"))

print(json.dumps({
    "validated": True,
    "candidate_identity": actual_identity,
    "score": final["score"],
    "grade": final["grade"],
    "assertions": f"{passed}/{total}",
    "artifact_hashes": len(hashes),
}, indent=2))
