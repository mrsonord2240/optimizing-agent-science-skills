#!/usr/bin/env python3
import hashlib
import json
import math
from pathlib import Path

root = Path(__file__).resolve().parents[1]
report = json.loads((root / "report.json").read_text(encoding="utf-8"))
identity = json.loads((root / "source-identity.json").read_text(encoding="utf-8"))
checks = {}

def check(name, condition):
    checks[name] = bool(condition)

def keys(obj, expected):
    return isinstance(obj, dict) and set(obj) == set(expected)

check("top_level_exact", keys(report, ["meta", "veto_gates", "static_score", "dynamic_score", "final", "key_strengths", "recommendations"]))
meta = report["meta"]
check("meta_exact", keys(meta, ["skill_name", "description", "evaluated_on", "evaluator_version", "category", "execution_mode", "complexity", "n_inputs"]))
check("skill_identity", meta["skill_name"] == identity["skill_id"] and meta["n_inputs"] == 7)
sv = report["veto_gates"]["skill_veto"]
rv = report["veto_gates"]["research_veto"]
check("skill_veto_exact", keys(sv, ["gate", "stability", "contract", "determinism", "security"]))
check("skill_veto_consistent", sv["gate"] == ("FAIL" if "FAIL" in [sv[k] for k in ("stability", "contract", "determinism", "security")] else "PASS"))
check("research_veto_exact", keys(rv, ["applicable", "gate", "scientific_integrity", "practice_boundaries", "methodological_ground", "code_usability"]))
check("research_veto_components", all(keys(rv[k], ["result", "detail"]) for k in ("scientific_integrity", "practice_boundaries", "methodological_ground", "code_usability")))
check("research_veto_methodology", rv["applicable"] is True and rv["methodological_ground"]["result"] == "FAIL" and rv["gate"] == "FAIL")
ss = report["static_score"]
category_keys = ["functional_suitability", "reliability", "performance_context", "agent_usability", "human_usability", "security", "maintainability", "agent_specific"]
check("static_categories_exact", keys(ss["categories"], category_keys))
check("static_category_shapes_ranges", all(keys(ss["categories"][k], ["score", "max", "note"]) and type(ss["categories"][k]["score"]) is int and ss["categories"][k]["max"] > 0 and 0 <= ss["categories"][k]["score"] <= ss["categories"][k]["max"] and isinstance(ss["categories"][k]["note"], str) for k in category_keys))
check("static_subtotal", ss["subtotal"] == sum(ss["categories"][k]["score"] for k in category_keys) and ss["subtotal"] == 91 and ss["max"] == 100)
ds = report["dynamic_score"]
inputs = ds["inputs"]
check("dynamic_shapes", keys(ds, ["execution_avg", "max", "assertion_pass_rate", "inputs"]) and keys(ds["assertion_pass_rate"], ["passed", "total"]))
check("inputs_cardinality", len(inputs) == meta["n_inputs"] == 7 and [x["index"] for x in inputs] == list(range(1, 8)))
input_keys = ["index", "type", "label", "status", "status_flag", "basic", "specialized", "note", "total", "assertions_passed", "assertions_total", "assertions"]
input_shape_ok = all(keys(x, input_keys) and 3 <= len(x["assertions"]) <= 5 and all(keys(a, ["text", "result", "note"]) and a["result"] in ("PASS", "FAIL") for a in x["assertions"]) for x in inputs)
check("input_and_assertion_shapes", input_shape_ok)
input_math_ok = all(x["basic"] + x["specialized"] == x["total"] and x["assertions_passed"] == sum(a["result"] == "PASS" for a in x["assertions"]) and x["assertions_total"] == len(x["assertions"]) and x["status"] == "COMPLETED" and x["status_flag"] == ("✅" if x["total"] >= 75 else "⚠️") for x in inputs)
check("input_math_status", input_math_ok)
passed = sum(x["assertions_passed"] for x in inputs)
total = sum(x["assertions_total"] for x in inputs)
avg = round(sum(x["total"] for x in inputs) / len(inputs), 1)
check("dynamic_aggregates", ds["execution_avg"] == avg == 91.9 and ds["assertion_pass_rate"] == {"passed": passed, "total": total} == {"passed": 33, "total": 35} and ds["max"] == 100)
final = report["final"]
expected_static = round(ss["subtotal"] * .4, 1)
expected_dynamic = round(avg * .6, 1)
expected_score = round(expected_static + expected_dynamic)
check("final_exact", keys(final, ["static_weighted", "dynamic_weighted", "score", "max", "grade", "grade_symbol", "deployable", "veto_override"]))
check("final_arithmetic", final["static_weighted"] == expected_static == 36.4 and final["dynamic_weighted"] == expected_dynamic == 55.1 and final["score"] == expected_score == 92 and final["max"] == 100)
check("final_veto_and_grade", final["grade"] == "Reject" and final["grade_symbol"] == "❌" and final["veto_override"] is True and final["deployable"] is False)
check("strengths_recommendations", 2 <= len(report["key_strengths"]) <= 5 and len(report["recommendations"]) == 1 and report["recommendations"][0]["priority"] == "P0" and report["recommendations"][0]["observed_in"] == [6])
check("open_finding_identity", identity["audit"]["open_findings"] == ["AGO-009"] and identity["audit"]["closed_findings"] == ["AGO-004", "AGO-005"] and identity["audit"]["verdict"] == "Reject")
manifest = (root / "candidate-manifest.tsv").read_bytes()
check("candidate_manifest_identity", hashlib.sha256(manifest).hexdigest() == identity["candidate"]["content_sha256"] and len(manifest) == identity["candidate"]["manifest_bytes"] and len(manifest.splitlines()) == identity["candidate"]["file_count"] and identity["candidate"]["identity_before"] == identity["candidate"]["identity_after"])
viewer = (root / "viewer.md").read_text(encoding="utf-8")
check("viewer_consistency", "Execution Average:** 91.9" in viewer and "Assertion Pass Rate:** 33/35" in viewer and "Research veto: FAIL" in viewer and "AGO-009 P0" in viewer)
out = {"schema_reference": "skill-auditor/references/report_json_schema.md v4.0", "validation": "PASS" if all(checks.values()) else "FAIL", "checks": checks}
(root / "evidence" / "schema-validation.json").write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
print(json.dumps(out, indent=2))
raise SystemExit(0 if all(checks.values()) else 1)
