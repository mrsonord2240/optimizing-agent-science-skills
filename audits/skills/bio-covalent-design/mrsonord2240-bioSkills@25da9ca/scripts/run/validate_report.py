"""Check the emitted report against the audit JSON contract's cardinality rules."""
import json
from pathlib import Path

path = Path(__file__).resolve().parent.parent / "eval_report_bio-covalent-design_result.json"
report = json.loads(path.read_text(encoding="utf-8"))
assert set(report) == {"meta", "veto_gates", "static_score", "dynamic_score", "final", "key_strengths", "recommendations"}
assert report["meta"]["auditor_independent"] is False
assert report["meta"]["source"] == "mrsonord2240/bioSkills@25da9caf792f45b49a58ecdab30027a2cfea5945:chemoinformatics/covalent-design"
assert set(report["static_score"]["categories"]) == {"functional_suitability", "reliability", "performance_context", "agent_usability", "human_usability", "security", "maintainability", "agent_specific"}
assert report["static_score"]["subtotal"] == sum(item["score"] for item in report["static_score"]["categories"].values())
inputs = report["dynamic_score"]["inputs"]
assert len(inputs) == report["meta"]["n_inputs"] == 11
assert all(3 <= len(row["assertions"]) <= 5 for row in inputs)
assert all(row["basic"] + row["specialized"] == row["total"] for row in inputs)
assert all(row["assertions_passed"] == sum(item["result"] == "PASS" for item in row["assertions"]) for row in inputs)
assert report["dynamic_score"]["execution_avg"] == round(sum(row["total"] for row in inputs) / len(inputs), 1)
assert report["final"]["score"] == round(report["final"]["static_weighted"] + report["final"]["dynamic_weighted"])
assert report["final"]["deployable"] is True and report["final"]["veto_override"] is False
assert report["veto_gates"]["skill_veto"]["gate"] == "PASS"
assert report["veto_gates"]["research_veto"]["gate"] == "PASS"
print("report_schema_and_arithmetic=PASS")
