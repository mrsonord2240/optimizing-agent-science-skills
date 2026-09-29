#!/usr/bin/env python3
"""Strict v4 report, evidence-hash, and readiness checks for the re-audit."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
REPORT = ROOT / "report.json"
IDENTITY = ROOT / "source-identity.json"
CANDIDATE = Path("/mnt/openscience/wt/opt10-analytical-validation/skills/bio-analytical-validation")


def require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    data = json.loads(REPORT.read_text(encoding="utf-8"))
    source = json.loads(IDENTITY.read_text(encoding="utf-8"))
    errors: list[str] = []

    require(
        set(data) == {"meta", "veto_gates", "static_score", "dynamic_score", "final", "key_strengths", "recommendations"},
        "top-level keys differ from schema",
        errors,
    )
    require(
        set(data["meta"]) == {
            "skill_name", "description", "evaluated_on", "evaluator_version", "category", "execution_mode", "complexity", "n_inputs"
        },
        "meta keys differ from schema",
        errors,
    )
    require(
        set(data["veto_gates"]["skill_veto"]) == {"gate", "stability", "contract", "determinism", "security"},
        "skill-veto keys differ from schema",
        errors,
    )
    require(
        set(data["veto_gates"]["research_veto"]) == {
            "applicable", "gate", "scientific_integrity", "practice_boundaries", "methodological_ground", "code_usability"
        },
        "research-veto keys differ from schema",
        errors,
    )
    require(
        all(
            set(data["veto_gates"]["research_veto"][key]) == {"result", "detail"}
            for key in ("scientific_integrity", "practice_boundaries", "methodological_ground", "code_usability")
        ),
        "research-veto dimension shape differs from schema",
        errors,
    )

    category_keys = {
        "functional_suitability", "reliability", "performance_context", "agent_usability",
        "human_usability", "security", "maintainability", "agent_specific"
    }
    categories = data["static_score"]["categories"]
    require(set(categories) == category_keys, "static category keys differ from schema", errors)
    require(all(set(item) == {"score", "max", "note"} for item in categories.values()), "static category shape differs", errors)
    require(sum(item["score"] for item in categories.values()) == data["static_score"]["subtotal"], "static subtotal mismatch", errors)
    require(all(isinstance(item["score"], int) and 0 <= item["score"] <= item["max"] for item in categories.values()), "static score range/type mismatch", errors)

    inputs = data["dynamic_score"]["inputs"]
    require(len(inputs) == data["meta"]["n_inputs"], "dynamic input count mismatch", errors)
    passed = 0
    assertion_total = 0
    for item in inputs:
        require(
            set(item) == {
                "index", "type", "label", "status", "status_flag", "note", "basic", "specialized", "total",
                "assertions_passed", "assertions_total", "assertions"
            },
            f"input {item['index']} shape differs from schema",
            errors,
        )
        require(3 <= len(item["assertions"]) <= 5, f"input {item['index']} assertion count", errors)
        actual_passed = sum(assertion["result"] == "PASS" for assertion in item["assertions"])
        require(actual_passed == item["assertions_passed"], f"input {item['index']} pass count", errors)
        require(len(item["assertions"]) == item["assertions_total"], f"input {item['index']} assertion total", errors)
        require(item["basic"] + item["specialized"] == item["total"], f"input {item['index']} score addition", errors)
        require(all(set(assertion) == {"text", "result", "note"} for assertion in item["assertions"]), f"input {item['index']} assertion shape", errors)
        passed += actual_passed
        assertion_total += len(item["assertions"])

    execution_avg = round(sum(item["total"] for item in inputs) / len(inputs), 1)
    layer1_avg = round(sum(item["basic"] for item in inputs) / len(inputs), 1)
    layer2_avg = round(sum(item["specialized"] for item in inputs) / len(inputs), 1)
    require(execution_avg == data["dynamic_score"]["execution_avg"], "execution average mismatch", errors)
    require(data["dynamic_score"]["assertion_pass_rate"] == {"passed": passed, "total": assertion_total}, "assertion aggregate mismatch", errors)

    static_weighted = round(data["static_score"]["subtotal"] * 0.4, 1)
    dynamic_weighted = round(data["dynamic_score"]["execution_avg"] * 0.6, 1)
    final_score = round(static_weighted + dynamic_weighted)
    require(static_weighted == data["final"]["static_weighted"], "static weight mismatch", errors)
    require(dynamic_weighted == data["final"]["dynamic_weighted"], "dynamic weight mismatch", errors)
    require(final_score == data["final"]["score"], "final score mismatch", errors)
    require(2 <= len(data["key_strengths"]) <= 5, "key-strength cardinality", errors)
    priority_rank = {"P0": 0, "P1": 1, "P2": 2}
    priorities = [priority_rank[item["priority"]] for item in data["recommendations"]]
    require(priorities == sorted(priorities), "recommendation order", errors)

    any_gate_failed = any(
        gate["gate"] == "FAIL"
        for gate in (data["veto_gates"]["skill_veto"], data["veto_gates"]["research_veto"])
    )
    require(data["final"]["veto_override"] == any_gate_failed, "veto override mismatch", errors)
    require(data["final"]["grade"] == "Production Ready" and data["final"]["grade_symbol"] == "⭐", "grade mismatch", errors)
    require(data["final"]["deployable"] and not any_gate_failed, "deployability mismatch", errors)

    require(data["final"]["score"] >= 85, "final readiness floor", errors)
    require(data["static_score"]["subtotal"] >= 80, "static readiness floor", errors)
    require(execution_avg >= 85, "execution readiness floor", errors)
    require(layer1_avg >= 32, "Layer 1 readiness floor", errors)
    require(layer2_avg >= 48, "Layer 2 readiness floor", errors)
    require(passed / assertion_total >= 0.90, "assertion readiness floor", errors)
    require(not any(item["priority"] == "P0" for item in data["recommendations"]), "open P0 recommendation", errors)

    for relative, expected in source["audit_artifacts"].items():
        path = ROOT / relative
        require(path.is_file(), f"missing artifact {relative}", errors)
        if path.is_file():
            require(sha256(path) == expected, f"artifact hash mismatch {relative}", errors)

    manifest_lines = []
    for item in source["files"]:
        path = CANDIDATE / item["path"]
        raw = path.read_bytes()
        observed_sha = hashlib.sha256(raw).hexdigest()
        observed_blob = hashlib.sha1(f"blob {len(raw)}\0".encode() + raw).hexdigest()
        require(observed_sha == item["sha256"], f"candidate SHA mismatch {item['path']}", errors)
        require(observed_blob == item["git_blob"], f"candidate blob mismatch {item['path']}", errors)
        require(len(raw) == item["bytes"], f"candidate byte-count mismatch {item['path']}", errors)
        manifest_lines.append(f"{item['path']}\t{observed_sha}\t{observed_blob}\t{len(raw)}\n")
    content_identity = hashlib.sha256("".join(manifest_lines).encode("utf-8")).hexdigest()
    require(content_identity == source["candidate"]["content_sha256"], "candidate content identity mismatch", errors)

    result = {
        "schema": "skill-auditor report schema v4.0",
        "valid": not errors,
        "errors": errors,
        "candidate_identity": content_identity,
        "static_subtotal": data["static_score"]["subtotal"],
        "dynamic_average": execution_avg,
        "layer1_average": layer1_avg,
        "layer2_average": layer2_avg,
        "assertions": {"passed": passed, "total": assertion_total},
        "weighted": {"static": static_weighted, "dynamic": dynamic_weighted, "rounded_final": final_score},
        "readiness": "candidate-ready" if not errors else "rejected"
    }
    rendered = json.dumps(result, indent=2) + "\n"
    evidence_dir = ROOT / "evidence"
    evidence_dir.mkdir(parents=True, exist_ok=True)
    (evidence_dir / "schema-validation.json").write_text(rendered, encoding="utf-8", newline="\n")
    print(rendered, end="")
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
