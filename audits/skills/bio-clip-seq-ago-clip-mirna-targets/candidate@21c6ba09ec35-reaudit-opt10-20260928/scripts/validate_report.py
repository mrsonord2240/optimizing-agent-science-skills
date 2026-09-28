#!/usr/bin/env python3
"""Validate strict re-audit schema, evidence hashes, semantic controls, and exact candidate bytes."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CANDIDATE = Path("/mnt/openscience/wt/opt10-ago-clip/skills/bio-clip-seq-ago-clip-mirna-targets")


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def main() -> int:
    report = json.loads((ROOT / "report.json").read_text(encoding="utf-8"))
    source = json.loads((ROOT / "source-identity.json").read_text(encoding="utf-8"))
    errors: list[str] = []

    require(set(report) == {"meta", "veto_gates", "static_score", "dynamic_score", "final", "key_strengths", "recommendations"}, "top-level schema keys", errors)
    require(set(report["meta"]) == {"skill_name", "description", "evaluated_on", "evaluator_version", "category", "execution_mode", "complexity", "n_inputs"}, "meta schema keys", errors)
    require(set(report["veto_gates"]["skill_veto"]) == {"gate", "stability", "contract", "determinism", "security"}, "skill-veto schema keys", errors)
    research = report["veto_gates"]["research_veto"]
    require(set(research) == {"applicable", "gate", "scientific_integrity", "practice_boundaries", "methodological_ground", "code_usability"}, "research-veto schema keys", errors)
    for key in ("scientific_integrity", "practice_boundaries", "methodological_ground", "code_usability"):
        require(set(research[key]) == {"result", "detail"}, f"research veto shape {key}", errors)

    category_keys = {"functional_suitability", "reliability", "performance_context", "agent_usability", "human_usability", "security", "maintainability", "agent_specific"}
    categories = report["static_score"]["categories"]
    require(set(categories) == category_keys, "static category keys", errors)
    require(sum(item["score"] for item in categories.values()) == report["static_score"]["subtotal"], "static subtotal", errors)
    require(all(set(item) == {"score", "max", "note"} and isinstance(item["score"], int) and 0 <= item["score"] <= item["max"] for item in categories.values()), "static category shape or range", errors)

    inputs = report["dynamic_score"]["inputs"]
    require(len(inputs) == report["meta"]["n_inputs"] == 5, "input count", errors)
    passed = 0
    assertion_total = 0
    for item in inputs:
        require(set(item) == {"index", "type", "label", "status", "status_flag", "note", "basic", "specialized", "total", "assertions_passed", "assertions_total", "assertions"}, f"input {item['index']} schema keys", errors)
        require(3 <= len(item["assertions"]) <= 5, f"input {item['index']} assertion count", errors)
        actual = sum(assertion["result"] == "PASS" for assertion in item["assertions"])
        require(actual == item["assertions_passed"], f"input {item['index']} assertion passes", errors)
        require(len(item["assertions"]) == item["assertions_total"], f"input {item['index']} assertion total", errors)
        require(item["basic"] + item["specialized"] == item["total"], f"input {item['index']} score sum", errors)
        require(all(set(assertion) == {"text", "result", "note"} and assertion["result"] in {"PASS", "FAIL"} for assertion in item["assertions"]), f"input {item['index']} assertion schema", errors)
        passed += actual
        assertion_total += len(item["assertions"])
    execution_avg = round(sum(item["total"] for item in inputs) / len(inputs), 1)
    require(execution_avg == report["dynamic_score"]["execution_avg"], "execution average", errors)
    require(report["dynamic_score"]["assertion_pass_rate"] == {"passed": passed, "total": assertion_total}, "assertion aggregate", errors)
    static_weighted = round(report["static_score"]["subtotal"] * 0.4, 1)
    dynamic_weighted = round(execution_avg * 0.6, 1)
    final_score = round(static_weighted + dynamic_weighted)
    require(static_weighted == report["final"]["static_weighted"], "static weighted", errors)
    require(dynamic_weighted == report["final"]["dynamic_weighted"], "dynamic weighted", errors)
    require(final_score == report["final"]["score"], "final score", errors)
    require(report["veto_gates"]["skill_veto"]["gate"] == "FAIL" and report["veto_gates"]["skill_veto"]["determinism"] == "FAIL", "determinism veto", errors)
    require(research["gate"] == "FAIL" and research["methodological_ground"]["result"] == "FAIL", "methodological veto", errors)
    require(report["final"]["grade"] == "Reject" and report["final"]["veto_override"] is True and report["final"]["deployable"] is False, "veto-overridden final grade", errors)
    require([x["priority"] for x in report["recommendations"]] == ["P0", "P1"], "ordered recommendations", errors)
    require(all(set(x) == {"priority", "title", "observed_in", "problem", "root_cause", "fix"} for x in report["recommendations"]), "recommendation schema", errors)

    for relative, expected in source["audit_artifacts"].items():
        path = ROOT / relative
        require(path.is_file(), f"missing artifact {relative}", errors)
        if path.is_file():
            require(sha(path) == expected, f"artifact hash {relative}", errors)

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
    identity = hashlib.sha256("\n".join(manifest_rows).encode()).hexdigest()
    require(identity == source["candidate"]["content_sha256"] == "21c6ba09ec3580896c35adbe5175ac2e7bf161870e912e46d2bbca42190cfebc", "candidate content identity", errors)

    repeatability = json.loads((ROOT / "evidence/hyb-repeatability.json").read_text(encoding="utf-8"))
    require(repeatability["pair_a"]["accepted"] == repeatability["pair_b"]["accepted"] == 94, "real Hyb accepted counts", errors)
    require(repeatability["pair_a"]["excluded"] == repeatability["pair_b"]["excluded"] == 17, "real Hyb excluded counts", errors)
    cross = repeatability["cross_pair"]
    require(cross["identical_sites_bytes"] is False and cross["identical_targets_bytes"] is False, "cross-pair output differs", errors)
    require(len(cross["accepted_only_in_a"]) == 7 and len(cross["accepted_only_in_b"]) == 7 and len(cross["changed_assignments_among_shared"]) == 4, "cross-pair difference counts", errors)
    targeted = json.loads((ROOT / "evidence/yeo-targeted-contract.json").read_text(encoding="utf-8"))
    require(targeted["cwl_prose_says_9nt"] is True and targeted["script_default_umi_length_10"] is True and targeted["cwl_supplies_umi_length"] is False and targeted["live_prefix_length"] == 10, "targeted Yeo mismatch", errors)
    targetscan = json.loads((ROOT / "evidence/targetscan-contract.json").read_text(encoding="utf-8"))
    require(all(targetscan[key] is True for key in ("plus_and_minus_multiblock", "same_strand_only", "wrong_release_rejected", "out_of_range_rejected")), "TargetScan assertions", errors)

    result = {
        "schema": "skill-auditor report schema v4.0",
        "valid": not errors,
        "errors": errors,
        "candidate_identity": identity,
        "static_subtotal": report["static_score"]["subtotal"],
        "dynamic_average": execution_avg,
        "assertions": {"passed": passed, "total": assertion_total},
        "weighted": {"static": static_weighted, "dynamic": dynamic_weighted, "rounded_final": final_score},
        "skill_veto": report["veto_gates"]["skill_veto"]["gate"],
        "research_veto": research["gate"],
        "readiness": "rejected",
        "open_findings": ["AGO-004", "AGO-005"],
    }
    rendered = json.dumps(result, indent=2) + "\n"
    (ROOT / "evidence/schema-validation.json").write_text(rendered, encoding="utf-8", newline="\n")
    print(rendered, end="")
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())

