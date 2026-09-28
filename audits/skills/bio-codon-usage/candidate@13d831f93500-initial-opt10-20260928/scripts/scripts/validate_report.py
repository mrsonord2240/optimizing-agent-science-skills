import hashlib
import json
from pathlib import Path

RUN = Path(__file__).resolve().parents[1]
CANDIDATE = Path(r"F:\OpenScience\wt\opt10-codon-usage\skills\bio-codon-usage")
EXPECTED_IDENTITY = "13d831f93500607c6f8cd7ce8b0ece7238af8400c80b750a3a6d95d2e5b4dc77"


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
inputs = json.loads((RUN / "generated-test-inputs.json").read_text(encoding="utf-8"))
execution = json.loads((RUN / "evidence" / "audit-results.json").read_text(encoding="utf-8"))

required_top = {"meta", "veto_gates", "static_score", "dynamic_score", "final", "key_strengths", "recommendations"}
assert set(report) == required_top
assert report["meta"]["n_inputs"] == 5 == len(inputs["inputs"])
assert report["meta"]["category"] == "Data Analysis"
assert report["meta"]["execution_mode"] == "B"
assert report["meta"]["complexity"] == "Moderate"

categories = report["static_score"]["categories"]
expected_categories = {
    "functional_suitability", "reliability", "performance_context", "agent_usability",
    "human_usability", "security", "maintainability", "agent_specific"
}
assert set(categories) == expected_categories
assert sum(item["score"] for item in categories.values()) == report["static_score"]["subtotal"] == 68
assert all(0 <= item["score"] <= item["max"] for item in categories.values())
assert all(isinstance(item["note"], str) and item["note"] for item in categories.values())

rows = report["dynamic_score"]["inputs"]
assert len(rows) == report["meta"]["n_inputs"]
passed = total_assertions = 0
for index, row in enumerate(rows, start=1):
    assert row["index"] == index
    assert row["basic"] + row["specialized"] == row["total"]
    assert 3 <= len(row["assertions"]) <= 5
    row_passed = sum(assertion["result"] == "PASS" for assertion in row["assertions"])
    assert all(assertion["result"] in {"PASS", "FAIL"} for assertion in row["assertions"])
    assert row_passed == row["assertions_passed"]
    assert len(row["assertions"]) == row["assertions_total"]
    expected_flag = "❌" if row["status"] in {"PARTIAL", "ERROR"} else ("✅" if row["total"] >= 75 else "⚠️")
    assert row["status_flag"] == expected_flag
    passed += row_passed
    total_assertions += len(row["assertions"])

average = round(sum(row["total"] for row in rows) / len(rows), 1)
assert average == report["dynamic_score"]["execution_avg"] == 50.8
assert {"passed": passed, "total": total_assertions} == report["dynamic_score"]["assertion_pass_rate"]
assert passed == 12 and total_assertions == 25

final = report["final"]
assert final["static_weighted"] == round(68 * 0.4, 1)
assert final["dynamic_weighted"] == round(50.8 * 0.6, 1)
assert final["score"] == round(final["static_weighted"] + final["dynamic_weighted"]) == 58
assert final["grade"] == "Reject" and final["grade_symbol"] == "❌"
assert not final["deployable"] and final["veto_override"]
assert report["veto_gates"]["skill_veto"]["gate"] == "FAIL"
assert report["veto_gates"]["research_veto"]["gate"] == "FAIL"

priority_order = {"P0": 0, "P1": 1, "P2": 2}
priorities = [priority_order[item["priority"]] for item in report["recommendations"]]
assert priorities == sorted(priorities)
assert [item["title"].split(":", 1)[0] for item in report["recommendations"]] == [
    "CODON-001", "CODON-002", "CODON-003", "CODON-004"
]
assert len(report["key_strengths"]) in range(2, 6)

observed_identity, file_count, manifest_bytes = manifest_identity(CANDIDATE)
assert observed_identity == EXPECTED_IDENTITY
assert source["candidate"]["identity"] == EXPECTED_IDENTITY
assert source["candidate"]["file_count"] == file_count == 9
assert source["candidate"]["manifest_bytes"] == manifest_bytes == 862
assert execution["candidate_identity"] == EXPECTED_IDENTITY
assert execution["checks_passed"] == execution["checks_total"] == 35

required_files = [
    "viewer.md", "finding-ledger.md", "generated-test-inputs.json", "source-identity.json",
    "audit_harness.py", "evidence/audit-results.json", "evidence/audit-transcript.txt",
    "evidence/candidate-manifest-current.tsv", "evidence/execution-classification.md",
    "evidence/research-checks.md", "evidence/commands.txt",
    "outputs/01-basic_analysis.stdout.txt", "outputs/02-rscu_analysis.stdout.txt",
    "outputs/03-cai_optimization.stdout.txt", "outputs/nc-heterogeneous.out",
    "outputs/nc-public_thra.out", "inputs/nc-heterogeneous.fasta", "inputs/nc-public_thra.fasta"
]
assert all((RUN / rel).is_file() for rel in required_files)

result = {
    "schema": "scientific-skill-audit.validation.v1",
    "status": "PASS",
    "candidate_identity": observed_identity,
    "candidate_file_count": file_count,
    "candidate_manifest_bytes": manifest_bytes,
    "execution_checks": {"passed": execution["checks_passed"], "total": execution["checks_total"]},
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
