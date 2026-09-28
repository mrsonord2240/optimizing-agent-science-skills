#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CANDIDATE = Path("/mnt/openscience/wt/opt10-chipseq-asb/skills/bio-chipseq-allele-specific-binding")


def require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def main() -> int:
    report = json.loads((ROOT / "report.json").read_text(encoding="utf-8"))
    source = json.loads((ROOT / "source-identity.json").read_text(encoding="utf-8"))
    errors: list[str] = []
    require(set(report) == {"meta", "veto_gates", "static_score", "dynamic_score", "final", "key_strengths", "recommendations"}, "top-level keys", errors)
    require(set(report["meta"]) == {"skill_name", "description", "evaluated_on", "evaluator_version", "category", "execution_mode", "complexity", "n_inputs"}, "meta keys", errors)
    require(set(report["veto_gates"]["skill_veto"]) == {"gate", "stability", "contract", "determinism", "security"}, "skill veto keys", errors)
    research = report["veto_gates"]["research_veto"]
    require(set(research) == {"applicable", "gate", "scientific_integrity", "practice_boundaries", "methodological_ground", "code_usability"}, "research veto keys", errors)
    categories = report["static_score"]["categories"]
    require(set(categories) == {"functional_suitability", "reliability", "performance_context", "agent_usability", "human_usability", "security", "maintainability", "agent_specific"}, "category keys", errors)
    require(sum(x["score"] for x in categories.values()) == report["static_score"]["subtotal"], "static subtotal", errors)
    inputs = report["dynamic_score"]["inputs"]
    require(len(inputs) == report["meta"]["n_inputs"], "input count", errors)
    passed = total = 0
    for item in inputs:
        require(3 <= len(item["assertions"]) <= 5, f"input {item['index']} assertion count", errors)
        observed = sum(x["result"] == "PASS" for x in item["assertions"])
        require(observed == item["assertions_passed"], f"input {item['index']} passes", errors)
        require(len(item["assertions"]) == item["assertions_total"], f"input {item['index']} assertion total", errors)
        require(item["basic"] + item["specialized"] == item["total"], f"input {item['index']} score", errors)
        passed += observed
        total += len(item["assertions"])
    execution = round(sum(x["total"] for x in inputs) / len(inputs), 1)
    require(execution == report["dynamic_score"]["execution_avg"], "dynamic average", errors)
    require(report["dynamic_score"]["assertion_pass_rate"] == {"passed": passed, "total": total}, "assertion aggregate", errors)
    sw = round(report["static_score"]["subtotal"] * 0.4, 1)
    dw = round(execution * 0.6, 1)
    require(report["final"]["static_weighted"] == sw, "static weight", errors)
    require(report["final"]["dynamic_weighted"] == dw, "dynamic weight", errors)
    require(report["final"]["score"] == round(sw + dw), "final score", errors)
    require(2 <= len(report["key_strengths"]) <= 5, "strength count", errors)
    ranks = {"P0": 0, "P1": 1, "P2": 2}
    priorities = [ranks[x["priority"]] for x in report["recommendations"]]
    require(priorities == sorted(priorities), "recommendation order", errors)
    rows = []
    for item in source["files"]:
        raw = (CANDIDATE / item["path"]).read_bytes()
        sha = hashlib.sha256(raw).hexdigest()
        blob = hashlib.sha1(f"blob {len(raw)}\0".encode() + raw).hexdigest()
        require(len(raw) == item["bytes"], f"bytes {item['path']}", errors)
        require(sha == item["sha256"], f"sha {item['path']}", errors)
        require(blob == item["git_blob"], f"blob {item['path']}", errors)
        rows.append(f"{item['path']}\t{sha}")
    identity = hashlib.sha256("\n".join(rows).encode()).hexdigest()
    require(identity == source["candidate"]["content_sha256"], "candidate identity", errors)
    result = {
        "schema": "skill-auditor report schema v4.0",
        "valid": not errors,
        "errors": errors,
        "candidate_identity": identity,
        "static_subtotal": report["static_score"]["subtotal"],
        "dynamic_average": execution,
        "assertions": {"passed": passed, "total": total},
        "weighted": {"static": sw, "dynamic": dw, "rounded_final": round(sw + dw)},
        "research_veto": research["gate"],
        "workflow_readiness": "needs-fix-CBA-009"
    }
    rendered = json.dumps(result, indent=2) + "\n"
    (ROOT / "evidence" / "schema-validation.json").write_text(rendered, encoding="utf-8", newline="\n")
    print(rendered, end="")
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
