#!/usr/bin/env python3
"""Validate the re-audit JSON contract, cardinalities, and arithmetic."""

from __future__ import annotations

import json
from pathlib import Path


BASE = Path("/mnt/openscience/audits/bio-vcf-statistics/reaudit-optimized-scientific-skills@2dee47f-20260925")
REPORT = BASE / "eval_report_bio-vcf-statistics_result.json"


def main() -> None:
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    assert set(report) == {
        "meta", "veto_gates", "static_score", "dynamic_score", "final",
        "key_strengths", "recommendations",
    }
    assert report["meta"]["n_inputs"] == len(report["dynamic_score"]["inputs"]) == 7
    assert report["meta"]["source"] == (
        "mrsonord2240/optimized-scientific-skills@"
        "2dee47f80dac6f3ba5c78b53ea9ec132a87cf5db:skills/bio-vcf-statistics"
    )
    assert report["meta"]["auditor_independent"] is True

    skill_veto = report["veto_gates"]["skill_veto"]
    assert set(skill_veto) == {"gate", "stability", "contract", "determinism", "security"}
    research_veto = report["veto_gates"]["research_veto"]
    assert set(research_veto) == {
        "applicable", "gate", "scientific_integrity", "practice_boundaries",
        "methodological_ground", "code_usability",
    }
    assert research_veto["applicable"] is True and research_veto["gate"] == "PASS"
    assert all(research_veto[key]["result"] == "PASS" for key in (
        "scientific_integrity", "practice_boundaries", "methodological_ground", "code_usability"
    ))

    categories = report["static_score"]["categories"]
    assert set(categories) == {
        "functional_suitability", "reliability", "performance_context", "agent_usability",
        "human_usability", "security", "maintainability", "agent_specific",
    }
    assert report["static_score"]["subtotal"] == sum(value["score"] for value in categories.values()) == 92

    passed = 0
    total = 0
    totals = []
    for expected_index, item in enumerate(report["dynamic_score"]["inputs"], 1):
        assert item["index"] == expected_index
        assert 3 <= len(item["assertions"]) <= 5
        item_passed = sum(a["result"] == "PASS" for a in item["assertions"])
        assert item["assertions_passed"] == item_passed
        assert item["assertions_total"] == len(item["assertions"])
        assert item["basic"] + item["specialized"] == item["total"]
        passed += item_passed
        total += len(item["assertions"])
        totals.append(item["total"])
    assert report["dynamic_score"]["assertion_pass_rate"] == {"passed": passed, "total": total}
    assert (passed, total) == (26, 28)
    execution_avg = round(sum(totals) / len(totals), 1)
    assert execution_avg == report["dynamic_score"]["execution_avg"] == 90.3

    final = report["final"]
    assert final["static_weighted"] == round(92 * 0.4, 1) == 36.8
    assert final["dynamic_weighted"] == round(execution_avg * 0.6, 1) == 54.2
    assert final["score"] == round(final["static_weighted"] + final["dynamic_weighted"]) == 91
    assert final["grade"] == "Production Ready" and final["grade_symbol"] == "⭐"
    assert final["deployable"] is True and final["veto_override"] is False
    assert 2 <= len(report["key_strengths"]) <= 5
    priorities = [item["priority"] for item in report["recommendations"]]
    assert priorities == sorted(priorities, key={"P0": 0, "P1": 1, "P2": 2}.get)
    assert priorities == ["P2", "P2"]
    print("PASS schema: 7 top-level nodes, 8 static categories, 7 inputs")
    print("PASS arithmetic: static=92 dynamic=90.3 final=91 assertions=26/28")
    print("PASS decision: Production Ready, deployable=true, veto_override=false")
    print("PASS recommendations: P0=0 P1=0 P2=2")


if __name__ == "__main__":
    main()
