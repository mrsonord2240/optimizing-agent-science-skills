import hashlib
import json
from pathlib import Path

RUN = Path(__file__).resolve().parents[1]
CANDIDATE = Path(r"F:\OpenScience\wt\opt10-adaptive-designs\skills\bio-clinical-biostatistics-adaptive-designs")
EXPECTED_IDENTITY = "73116b86978447d18f14945b236561b0685796da68f1a993420352c3c6953546"


def manifest_identity(root: Path) -> tuple[str, int, int]:
    rows = []
    for path in sorted((p for p in root.rglob("*") if p.is_file()), key=lambda p: p.relative_to(root).as_posix()):
        rel = path.relative_to(root).as_posix()
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        rows.append(f"{rel}\t{path.stat().st_size}\t{digest}")
    body = "\n".join(rows).encode("utf-8")
    return hashlib.sha256(body).hexdigest(), len(rows), len(body)


report = json.loads((RUN / "report.json").read_text(encoding="utf-8"))
source = json.loads((RUN / "source-identity.json").read_text(encoding="utf-8"))
inputs = json.loads((RUN / "inputs.json").read_text(encoding="utf-8"))

required_top = {"meta", "veto_gates", "static_score", "dynamic_score", "final", "key_strengths", "recommendations"}
assert set(report) == required_top
assert report["meta"]["n_inputs"] == 7 == len(inputs["inputs"])
assert report["meta"]["category"] == "Protocol Design"
assert report["meta"]["execution_mode"] == "D"

categories = report["static_score"]["categories"]
expected_categories = {
    "functional_suitability", "reliability", "performance_context", "agent_usability",
    "human_usability", "security", "maintainability", "agent_specific"
}
assert set(categories) == expected_categories
assert sum(item["score"] for item in categories.values()) == report["static_score"]["subtotal"] == 71
assert all(0 <= item["score"] <= item["max"] for item in categories.values())

rows = report["dynamic_score"]["inputs"]
assert len(rows) == report["meta"]["n_inputs"]
passed = total_assertions = 0
for index, row in enumerate(rows, start=1):
    assert row["index"] == index
    assert row["basic"] + row["specialized"] == row["total"]
    assert 3 <= len(row["assertions"]) <= 5
    row_passed = sum(a["result"] == "PASS" for a in row["assertions"])
    assert all(a["result"] in {"PASS", "FAIL"} for a in row["assertions"])
    assert row_passed == row["assertions_passed"]
    assert len(row["assertions"]) == row["assertions_total"]
    passed += row_passed
    total_assertions += len(row["assertions"])

average = round(sum(row["total"] for row in rows) / len(rows), 1)
assert average == report["dynamic_score"]["execution_avg"] == 50.4
assert {"passed": passed, "total": total_assertions} == report["dynamic_score"]["assertion_pass_rate"]
assert passed == 18 and total_assertions == 35

final = report["final"]
assert final["static_weighted"] == round(71 * 0.4, 1)
assert final["dynamic_weighted"] == round(50.4 * 0.6, 1)
assert final["score"] == round(final["static_weighted"] + final["dynamic_weighted"]) == 59
assert final["grade"] == "Reject" and not final["deployable"] and final["veto_override"]
assert report["veto_gates"]["skill_veto"]["gate"] == "FAIL"
assert report["veto_gates"]["research_veto"]["gate"] == "FAIL"

priority_order = {"P0": 0, "P1": 1, "P2": 2}
priorities = [priority_order[item["priority"]] for item in report["recommendations"]]
assert priorities == sorted(priorities)
assert len(report["key_strengths"]) in range(2, 6)

observed_identity, file_count, manifest_bytes = manifest_identity(CANDIDATE)
assert observed_identity == EXPECTED_IDENTITY
assert source["candidate"]["identity"] == EXPECTED_IDENTITY
assert source["candidate"]["file_count"] == file_count == 8
assert source["candidate"]["manifest_bytes"] == manifest_bytes == 764

required_files = [
    "viewer.md", "finding-ledger.md", "inputs.json", "execution-classifications.json",
    "scientific-source-notes.md", "source-identity.json", "commands.txt",
    "evidence/candidate-section-status.tsv", "evidence/full-script.log",
    "evidence/valid-api-smoke.json", "evidence/section-03.json",
    "evidence/section-06.json", "evidence/section-08.json"
]
assert all((RUN / rel).is_file() for rel in required_files)

result = {
    "schema": "scientific-skill-audit.validation.v1",
    "status": "PASS",
    "candidate_identity": observed_identity,
    "candidate_file_count": file_count,
    "candidate_manifest_bytes": manifest_bytes,
    "static_score": report["static_score"]["subtotal"],
    "execution_average": average,
    "assertions": {"passed": passed, "total": total_assertions},
    "final_score": final["score"],
    "grade": final["grade"],
    "recommendation_count": len(report["recommendations"]),
    "required_files_checked": len(required_files)
}
out = RUN / "evidence" / "schema-validation.json"
out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
print(json.dumps(result, indent=2))
