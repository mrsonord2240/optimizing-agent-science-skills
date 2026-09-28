#!/usr/bin/env python3
"""Validate the v4 diagnostic report, evidence hashes, and exact candidate."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
CANDIDATE = Path(
    "/mnt/openscience/wt/opt10-ago-clip/skills/"
    "bio-clip-seq-ago-clip-mirna-targets"
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def main() -> int:
    report = json.loads((ROOT / "report.json").read_text(encoding="utf-8"))
    source = json.loads((ROOT / "source-identity.json").read_text(encoding="utf-8"))
    errors: list[str] = []

    require(
        set(report) == {
            "meta", "veto_gates", "static_score", "dynamic_score", "final",
            "key_strengths", "recommendations",
        },
        "top-level schema keys",
        errors,
    )
    require(
        set(report["meta"]) == {
            "skill_name", "description", "evaluated_on", "evaluator_version",
            "category", "execution_mode", "complexity", "n_inputs",
        },
        "meta schema keys",
        errors,
    )
    require(
        set(report["veto_gates"]["skill_veto"]) == {
            "gate", "stability", "contract", "determinism", "security",
        },
        "skill-veto schema keys",
        errors,
    )
    research = report["veto_gates"]["research_veto"]
    require(
        set(research) == {
            "applicable", "gate", "scientific_integrity", "practice_boundaries",
            "methodological_ground", "code_usability",
        },
        "research-veto schema keys",
        errors,
    )
    require(
        all(
            set(research[key]) == {"result", "detail"}
            for key in (
                "scientific_integrity", "practice_boundaries",
                "methodological_ground", "code_usability",
            )
        ),
        "research-veto dimension shape",
        errors,
    )

    category_keys = {
        "functional_suitability", "reliability", "performance_context",
        "agent_usability", "human_usability", "security", "maintainability",
        "agent_specific",
    }
    categories = report["static_score"]["categories"]
    require(set(categories) == category_keys, "static category keys", errors)
    require(
        sum(item["score"] for item in categories.values())
        == report["static_score"]["subtotal"],
        "static subtotal",
        errors,
    )
    require(
        all(
            set(item) == {"score", "max", "note"}
            and isinstance(item["score"], int)
            and 0 <= item["score"] <= item["max"]
            for item in categories.values()
        ),
        "static category shape or range",
        errors,
    )

    inputs = report["dynamic_score"]["inputs"]
    require(len(inputs) == report["meta"]["n_inputs"], "input count", errors)
    passed = 0
    assertion_total = 0
    for item in inputs:
        require(
            set(item) == {
                "index", "type", "label", "status", "status_flag", "note",
                "basic", "specialized", "total", "assertions_passed",
                "assertions_total", "assertions",
            },
            f"input {item['index']} schema keys",
            errors,
        )
        require(3 <= len(item["assertions"]) <= 5, f"input {item['index']} assertion count", errors)
        actual_passed = sum(x["result"] == "PASS" for x in item["assertions"])
        require(actual_passed == item["assertions_passed"], f"input {item['index']} passed assertions", errors)
        require(len(item["assertions"]) == item["assertions_total"], f"input {item['index']} total assertions", errors)
        require(item["basic"] + item["specialized"] == item["total"], f"input {item['index']} score sum", errors)
        require(
            all(set(x) == {"text", "result", "note"} and x["result"] in {"PASS", "FAIL"} for x in item["assertions"]),
            f"input {item['index']} assertion schema",
            errors,
        )
        passed += actual_passed
        assertion_total += len(item["assertions"])

    execution_avg = round(sum(x["total"] for x in inputs) / len(inputs), 1)
    require(execution_avg == report["dynamic_score"]["execution_avg"], "execution average", errors)
    require(
        report["dynamic_score"]["assertion_pass_rate"]
        == {"passed": passed, "total": assertion_total},
        "assertion aggregate",
        errors,
    )
    static_weighted = round(report["static_score"]["subtotal"] * 0.4, 1)
    dynamic_weighted = round(execution_avg * 0.6, 1)
    final_score = round(static_weighted + dynamic_weighted)
    require(static_weighted == report["final"]["static_weighted"], "static weighted", errors)
    require(dynamic_weighted == report["final"]["dynamic_weighted"], "dynamic weighted", errors)
    require(final_score == report["final"]["score"], "final score", errors)
    require(report["final"]["grade"] == "Reject", "diagnostic grade", errors)
    require(report["final"]["grade_symbol"] == "❌", "diagnostic grade symbol", errors)
    require(report["final"]["veto_override"] is True, "veto override", errors)
    require(report["final"]["deployable"] is False, "deployability", errors)
    require(2 <= len(report["key_strengths"]) <= 5, "strength cardinality", errors)
    rank = {"P0": 0, "P1": 1, "P2": 2}
    priorities = [rank[x["priority"]] for x in report["recommendations"]]
    require(priorities == sorted(priorities), "recommendation order", errors)

    for relative, expected in source["audit_artifacts"].items():
        path = ROOT / relative
        require(path.is_file(), f"missing artifact {relative}", errors)
        if path.is_file():
            require(sha256(path) == expected, f"artifact hash {relative}", errors)

    manifest_rows: list[str] = []
    for item in source["candidate"]["files"]:
        path = CANDIDATE / item["path"]
        raw = path.read_bytes()
        observed_sha = hashlib.sha256(raw).hexdigest()
        observed_blob = hashlib.sha1(f"blob {len(raw)}\0".encode() + raw).hexdigest()
        require(len(raw) == item["bytes"], f"candidate bytes {item['path']}", errors)
        require(observed_sha == item["sha256"], f"candidate SHA {item['path']}", errors)
        require(observed_blob == item["git_blob"], f"candidate blob {item['path']}", errors)
        manifest_rows.append(f"{item['path']}\t{len(raw)}\t{observed_sha}")
    content_identity = hashlib.sha256("\n".join(manifest_rows).encode()).hexdigest()
    require(
        content_identity == source["candidate"]["content_sha256"],
        "candidate content identity",
        errors,
    )

    result = {
        "schema": "skill-auditor report schema v4.0",
        "valid": not errors,
        "errors": errors,
        "candidate_identity": content_identity,
        "static_subtotal": report["static_score"]["subtotal"],
        "dynamic_average": execution_avg,
        "assertions": {"passed": passed, "total": assertion_total},
        "weighted": {
            "static": static_weighted,
            "dynamic": dynamic_weighted,
            "rounded_final": final_score,
        },
        "research_veto": research["gate"],
        "readiness": "rejected",
    }
    rendered = json.dumps(result, indent=2) + "\n"
    evidence = ROOT / "evidence" / "schema-validation.json"
    evidence.write_text(rendered, encoding="utf-8", newline="\n")
    print(rendered, end="")
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
