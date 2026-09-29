#!/usr/bin/env python3
"""Strict local validator for skill-auditor report schema v4.0."""
from __future__ import annotations
import hashlib, json, math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
report = json.loads((ROOT / "report.json").read_text(encoding="utf-8"))
identity = json.loads((ROOT / "source-identity.json").read_text(encoding="utf-8"))
checks: dict[str, bool] = {}
def check(name: str, value: bool) -> None: checks[name] = bool(value)
def exact(value: object, expected: list[str]) -> bool:
    return isinstance(value, dict) and set(value) == set(expected)

top = ["meta", "veto_gates", "static_score", "dynamic_score", "final", "key_strengths", "recommendations"]
meta_keys = ["skill_name", "description", "evaluated_on", "evaluator_version", "category", "execution_mode", "complexity", "n_inputs"]
check("top_level_exact", exact(report, top))
meta = report["meta"]
check("meta_exact", exact(meta, meta_keys))
check("skill_identity", meta["skill_name"] == identity["skill_id"] and meta["n_inputs"] == 7 and meta["evaluator_version"] == "skill-auditor@1.0")
vg = report["veto_gates"]
sv, rv = vg["skill_veto"], vg["research_veto"]
check("veto_shapes", exact(vg, ["skill_veto", "research_veto"]) and exact(sv, ["gate", "stability", "contract", "determinism", "security"]) and exact(rv, ["applicable", "gate", "scientific_integrity", "practice_boundaries", "methodological_ground", "code_usability"]))
check("skill_veto_consistency", sv["gate"] == ("FAIL" if "FAIL" in [sv[k] for k in ("stability", "contract", "determinism", "security")] else "PASS"))
check("research_veto_consistency", rv["applicable"] is True and rv["gate"] == ("FAIL" if any(rv[k]["result"] == "FAIL" for k in ("scientific_integrity", "practice_boundaries", "methodological_ground", "code_usability")) else "PASS") and all(exact(rv[k], ["result", "detail"]) for k in ("scientific_integrity", "practice_boundaries", "methodological_ground", "code_usability")))
ss = report["static_score"]
maxes = {"functional_suitability":12, "reliability":12, "performance_context":8, "agent_usability":16, "human_usability":8, "security":12, "maintainability":12, "agent_specific":20}
check("static_shape_and_ranges", exact(ss, ["subtotal", "max", "categories"]) and exact(ss["categories"], list(maxes)) and all(exact(ss["categories"][k], ["score", "max", "note"]) and type(ss["categories"][k]["score"]) is int and ss["categories"][k]["max"] == m and 0 <= ss["categories"][k]["score"] <= m and isinstance(ss["categories"][k]["note"], str) for k,m in maxes.items()))
static_sum = sum(ss["categories"][k]["score"] for k in maxes)
check("static_subtotal", ss["subtotal"] == static_sum and ss["max"] == 100)
ds = report["dynamic_score"]
inputs = ds["inputs"]
input_keys = ["index", "type", "label", "status", "status_flag", "basic", "specialized", "note", "total", "assertions_passed", "assertions_total", "assertions"]
check("dynamic_shapes", exact(ds, ["execution_avg", "max", "assertion_pass_rate", "inputs"]) and exact(ds["assertion_pass_rate"], ["passed", "total"]) and len(inputs) == meta["n_inputs"] == 7)
check("input_and_assertion_shapes", all(exact(item, input_keys) and 3 <= len(item["assertions"]) <= 5 and all(exact(a, ["text", "result", "note"]) and a["result"] in ("PASS", "FAIL") for a in item["assertions"]) for item in inputs))
check("input_math_status", [item["index"] for item in inputs] == list(range(1,8)) and all(item["basic"] + item["specialized"] == item["total"] and item["assertions_passed"] == sum(a["result"] == "PASS" for a in item["assertions"]) and item["assertions_total"] == len(item["assertions"]) and item["status"] == "COMPLETED" and item["status_flag"] == ("✅" if item["total"] >= 75 else "⚠️") for item in inputs))
passed = sum(x["assertions_passed"] for x in inputs); total = sum(x["assertions_total"] for x in inputs)
avg = round(sum(x["total"] for x in inputs) / len(inputs), 1)
check("dynamic_aggregates", ds["execution_avg"] == avg and ds["assertion_pass_rate"] == {"passed":passed,"total":total} and ds["max"] == 100)
f = report["final"]
check("final_shape", exact(f, ["static_weighted", "dynamic_weighted", "score", "max", "grade", "grade_symbol", "deployable", "veto_override"]))
sw = round(ss["subtotal"] * .4, 1); dw = round(avg * .6, 1); final_score = round(sw + dw)
check("final_arithmetic", f["static_weighted"] == sw and f["dynamic_weighted"] == dw and f["score"] == final_score and f["max"] == 100)
veto = sv["gate"] == "FAIL" or rv["gate"] == "FAIL"
grade = "Production Ready" if final_score >= 85 else "Limited Release" if final_score >= 75 else "Beta Only" if final_score >= 60 else "Reject"
symbol = {"Production Ready":"⭐", "Limited Release":"✅", "Beta Only":"⚠️", "Reject":"❌"}[grade]
check("readiness_gate", f["grade"] == grade and f["grade_symbol"] == symbol and f["veto_override"] is veto and f["deployable"] is (grade in ("Production Ready", "Limited Release") and not veto) and ss["subtotal"] >= 80 and avg >= 85 and sum(x["basic"] for x in inputs)/7 >= 32 and sum(x["specialized"] for x in inputs)/7 >= 48 and passed/total >= .9 and not veto)
check("strengths_recommendations", 2 <= len(report["key_strengths"]) <= 5 and report["recommendations"] == [])
manifest = (ROOT / "candidate-manifest.tsv").read_bytes()
check("candidate_manifest_identity", hashlib.sha256(manifest).hexdigest() == identity["candidate"]["content_sha256"] and len(manifest) == identity["candidate"]["manifest_bytes"] and len(manifest.splitlines()) == identity["candidate"]["file_count"] and identity["candidate"]["identity_before"] == identity["candidate"]["identity_after"])
viewer = (ROOT / "viewer.md").read_text(encoding="utf-8")
check("viewer_consistency", f"Execution Average:** {avg}" in viewer and f"Assertion Pass Rate:** {passed}/{total}" in viewer and "Research veto:** PASS" in viewer and identity["candidate"]["content_sha256"] in viewer)
out = {"schema_reference":"skill-auditor/references/report_json_schema.md v4.0", "validation":"PASS" if all(checks.values()) else "FAIL", "checks":checks}
(ROOT / "evidence" / "schema-validation.json").write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
print(json.dumps(out, indent=2))
raise SystemExit(0 if all(checks.values()) else 1)
