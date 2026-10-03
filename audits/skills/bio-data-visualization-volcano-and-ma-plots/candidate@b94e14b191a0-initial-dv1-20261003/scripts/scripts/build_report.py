#!/usr/bin/env python3
"""Fill derived fields of a skill-auditor v4 report from a spec. Usage: build_report.py spec.json report.json

Spec supplies meta, veto_gates, static categories (score+note), inputs (basic, specialized, status, assertions),
key_strengths, recommendations. Derived: subtotal, totals, flags, averages, weights, grade."""
import json
import sys
from pathlib import Path

spec = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
MAX = {"functional_suitability": 12, "reliability": 12, "performance_context": 8, "agent_usability": 16,
       "human_usability": 8, "security": 12, "maintainability": 12, "agent_specific": 20}
cats = {k: {"score": v["score"], "max": MAX[k], "note": v["note"]} for k, v in spec["static"].items()}
sub = sum(v["score"] for v in cats.values())
inputs = []
for n, i in enumerate(spec["inputs"], 1):
    a = i["assertions"]
    tot = i["basic"] + i["specialized"]
    flag = "❌" if i["status"] in ("PARTIAL", "ERROR") else ("✅" if tot >= 75 else "⚠️")
    inputs.append({"index": n, "type": i["type"], "label": i["label"], "status": i["status"], "status_flag": flag,
                   "note": i["note"], "basic": i["basic"], "specialized": i["specialized"], "total": tot,
                   "assertions_passed": sum(x["result"] == "PASS" for x in a), "assertions_total": len(a),
                   "assertions": a})
avg = round(sum(i["total"] for i in inputs) / len(inputs), 1)
sw, dw = round(sub * 0.4, 1), round(avg * 0.6, 1)
score = round(sw + dw)
grade, sym = ("Production Ready", "⭐") if score >= 85 else ("Limited Release", "✅") if score >= 75 else ("Beta Only", "⚠️") if score >= 60 else ("Reject", "❌")
sv, rv = spec["veto_gates"]["skill_veto"], spec["veto_gates"]["research_veto"]
fail = sv["gate"] == "FAIL" or rv["gate"] == "FAIL"
if fail:
    grade, sym = "Reject", "❌"
report = {
    "meta": {**spec["meta"], "evaluator_version": "skill-auditor@1.0", "n_inputs": len(inputs)},
    "veto_gates": spec["veto_gates"],
    "static_score": {"subtotal": sub, "max": 100, "categories": cats},
    "dynamic_score": {"execution_avg": avg, "max": 100,
                      "assertion_pass_rate": {"passed": sum(i["assertions_passed"] for i in inputs),
                                              "total": sum(i["assertions_total"] for i in inputs)},
                      "inputs": inputs},
    "final": {"static_weighted": sw, "dynamic_weighted": dw, "score": score, "max": 100, "grade": grade,
              "grade_symbol": sym, "deployable": grade in ("Production Ready", "Limited Release") and not fail,
              "veto_override": fail},
    "key_strengths": spec["key_strengths"],
    "recommendations": sorted(spec["recommendations"], key=lambda r: r["priority"]),
}
Path(sys.argv[2]).write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(f"static={sub} exec_avg={avg} final={score} grade={grade}")
