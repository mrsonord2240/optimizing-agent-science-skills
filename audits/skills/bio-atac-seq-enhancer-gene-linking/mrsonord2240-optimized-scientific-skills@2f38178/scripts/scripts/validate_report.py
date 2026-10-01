import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
report = json.loads((ROOT / "report.json").read_text(encoding="utf-8"))
errors = []
need = lambda condition, message: errors.append(message) if not condition else None
need(set(report) == {"meta", "veto_gates", "static_score", "dynamic_score", "final", "key_strengths", "recommendations"}, "top-level keys mismatch")
meta = report["meta"]
need(meta["skill_name"] == "bio-atac-seq-enhancer-gene-linking", "skill identity mismatch")
dynamic = report["dynamic_score"]
inputs = dynamic["inputs"]
need(all(r["priority"] in ("P0","P1","P2") for r in report["recommendations"]), "P3 forbidden")
need(len(inputs) == meta["n_inputs"], "input count mismatch")
passed = total_assertions = 0
for expected_index, item in enumerate(inputs, 1):
    need(item["index"] == expected_index, f"input {expected_index}: index mismatch")
    need(0 <= item["basic"] <= 40 and 0 <= item["specialized"] <= 60, f"input {expected_index}: score outside range")
    need(item["basic"] + item["specialized"] == item["total"], f"input {expected_index}: total mismatch")
    assertions = item["assertions"]
    need(3 <= len(assertions) <= 5, f"input {expected_index}: assertion cardinality")
    item_passed = sum(a["result"] == "PASS" for a in assertions)
    need(item_passed == item["assertions_passed"], f"input {expected_index}: pass count mismatch")
    need(len(assertions) == item["assertions_total"], f"input {expected_index}: assertion total mismatch")
    passed += item_passed
    total_assertions += len(assertions)
    expected_flag = "❌" if item["status"] in ("PARTIAL", "ERROR") else ("✅" if item["total"] >= 75 else "⚠️")
    if any(a["result"] == "FAIL" for a in assertions):
        expected_flag = "❌"
    need(item["status_flag"] == expected_flag, f"input {expected_index}: status flag mismatch")
average = round(sum(item["total"] for item in inputs) / len(inputs), 1)
need(dynamic["execution_avg"] == average, "execution average mismatch")
need(dynamic["assertion_pass_rate"] == {"passed": passed, "total": total_assertions}, "assertion aggregate mismatch")
static = report["static_score"]
categories = static["categories"]
expected_categories = {
    "functional_suitability": 12, "reliability": 12, "performance_context": 8,
    "agent_usability": 16, "human_usability": 8, "security": 12,
    "maintainability": 12, "agent_specific": 20,
}
need(set(categories) == set(expected_categories), "static category keys mismatch")
for name, maximum in expected_categories.items():
    need(categories[name]["max"] == maximum and 0 <= categories[name]["score"] <= maximum, f"category {name}: range mismatch")
need(static["subtotal"] == sum(c["score"] for c in categories.values()), "static subtotal mismatch")
need(len(report["key_strengths"]) in (2, 3, 4, 5), "key strength cardinality")
priority_order = {"P0": 0, "P1": 1, "P2": 2}
priorities = [priority_order.get(item["priority"], 9) for item in report["recommendations"]]
need(priorities == sorted(priorities), "recommendations are not priority ordered")
research = report["veto_gates"]["research_veto"]
research_gate_placeholder = research["gate"] == "PASS" and report["veto_gates"]["skill_veto"]["gate"] == "PASS"
final = report["final"]
static_weighted = round(static["subtotal"] * 0.4, 1)
dynamic_weighted = round(dynamic["execution_avg"] * 0.6, 1)
need(final["static_weighted"] == static_weighted, "weighted static mismatch")
need(final["dynamic_weighted"] == dynamic_weighted, "weighted dynamic mismatch")
need(final["score"] == round(static_weighted + dynamic_weighted), "final score mismatch")
need(final["veto_override"] is False and final["deployable"] is True and research_gate_placeholder, "veto override/deployable mismatch")
need(research["applicable"] is True and research["gate"] in ("PASS", "FAIL"), "research gate mismatch")
need(report["veto_gates"]["skill_veto"]["gate"] in ("PASS", "FAIL"), "skill gate mismatch")
print(json.dumps({"schema":"skill-auditor report schema v4.0","valid":not errors,"errors":errors,
                  "static_subtotal":static["subtotal"],"dynamic_average":dynamic["execution_avg"],
                  "assertions":{"passed":passed,"total":total_assertions},"final_score":final["score"],
                  "skill_veto":report["veto_gates"]["skill_veto"]["gate"],
                  "research_veto":research["gate"],"open_findings":len(report["recommendations"])},indent=2))
if errors:
    raise SystemExit(1)
