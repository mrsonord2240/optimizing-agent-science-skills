#!/usr/bin/env python3
"""Independent exhaustive re-audit harness for the fixed ACMG skill.

The harness is deliberately outside the candidate and never writes into it.
It records raw observations; scoring and scientific interpretation remain in the
audit report.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import pathlib
import subprocess
import sys
from datetime import datetime, timezone
from typing import Any, Callable


ROOT = pathlib.Path(os.environ["ACMG_REAUDIT_ROOT"])
CANDIDATE = pathlib.Path(os.environ["ACMG_CANDIDATE"])
EXPECTED_IDENTITY = "926ce0436d0d9fd1fb73a5f2b83728adfb622cf6f8ec41c8c00ad8d8300e8c07"


def load_module():
    path = CANDIDATE / "scripts" / "acmg_classify.py"
    spec = importlib.util.spec_from_file_location("reaudit_candidate_acmg", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def manifest_identity() -> dict[str, Any]:
    rows: list[str] = []
    files: list[dict[str, Any]] = []
    for path in sorted(
        (p for p in CANDIDATE.rglob("*") if p.is_file()),
        key=lambda p: p.relative_to(CANDIDATE).as_posix(),
    ):
        rel = path.relative_to(CANDIDATE).as_posix()
        data = path.read_bytes()
        digest = hashlib.sha256(data).hexdigest()
        rows.append(f"{rel}\t{len(data)}\t{digest}")
        files.append({"path": rel, "bytes": len(data), "sha256": digest})
    manifest = "\n".join(rows).encode("utf-8")
    return {
        "schema": "sha256-manifest-v1",
        "digest": hashlib.sha256(manifest).hexdigest(),
        "manifest_bytes": len(manifest),
        "file_count": len(files),
        "files": files,
        "rows": rows,
    }


def run(command: list[str], timeout: int = 120) -> dict[str, Any]:
    completed = subprocess.run(
        command,
        cwd=CANDIDATE,
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
        text=True,
        capture_output=True,
        timeout=timeout,
        check=False,
    )
    return {
        "command": command,
        "returncode": completed.returncode,
        "stdout": completed.stdout,
        "stderr": completed.stderr,
    }


def observe(label: str, call: Callable[[], Any], expected: Any = None, *, has_expected: bool = True) -> dict[str, Any]:
    try:
        actual = call()
        row: dict[str, Any] = {"label": label, "status": "RETURNED", "actual": actual}
        if has_expected:
            row["expected"] = expected
            row["match"] = actual == expected
        return row
    except Exception as exc:  # noqa: BLE001 - the exception itself is retained as evidence
        row = {"label": label, "status": "RAISED", "error": f"{type(exc).__name__}: {exc}"}
        if has_expected:
            row["expected"] = expected
            row["match"] = False
        return row


def expect_rejection(label: str, call: Callable[[], Any]) -> dict[str, Any]:
    try:
        actual = call()
        return {"label": label, "rejected": False, "actual": actual}
    except Exception as exc:  # noqa: BLE001
        return {"label": label, "rejected": True, "error": f"{type(exc).__name__}: {exc}"}


def main() -> None:
    started = datetime.now(timezone.utc).isoformat()
    before = manifest_identity()
    if before["digest"] != EXPECTED_IDENTITY:
        raise SystemExit(f"identity mismatch before execution: {before['digest']}")
    module = load_module()

    unit = run([
        sys.executable, "-B", "-m", "unittest", "discover", "-s", "tests", "-p", "test_*.py", "-v"
    ])
    demo = run([sys.executable, "-B", "scripts/acmg_classify.py"])
    live = run([sys.executable, "-B", "tests/live_interface_smoke.py"], timeout=180)
    compile_runs = [
        run([
            sys.executable, "-B", "-X", "pycache_prefix=/tmp/acmg-reaudit-pycache",
            "-m", "py_compile", str(path),
        ])
        for path in [
            CANDIDATE / "scripts" / "acmg_classify.py",
            CANDIDATE / "tests" / "test_acmg_classify.py",
            CANDIDATE / "tests" / "live_interface_smoke.py",
        ]
    ]

    oddspath_expectations = [
        (351.0, "PS3_VeryStrong"), (350.0, "PS3"), (19.0, "PS3"),
        (18.7, "PS3_Moderate"), (5.0, "PS3_Moderate"),
        (4.3, "PS3_Supporting"), (2.2, "PS3_Supporting"), (2.1, None),
        (0.48, None), (0.47, "BS3_Supporting"), (0.23, "BS3_Supporting"),
        (0.22, "BS3_Moderate"), (0.053, "BS3_Moderate"), (0.052, "BS3"),
    ]
    oddspath = [
        observe(f"OddsPath {value}", lambda value=value: module.ps3_oddspath(value), expected)
        for value, expected in oddspath_expectations
    ]
    oddspath_invalid = [
        expect_rejection(f"OddsPath rejects {value!r}", lambda value=value: module.ps3_oddspath(value))
        for value in [0, -0.1, True, float("nan"), float("inf"), "8"]
    ]

    def pvs1(**overrides: Any) -> Any:
        values = {
            "variant_type": "nonsense",
            "is_nmd_predicted": True,
            "coding_pct_removed": 0.01,
            "in_critical_region": False,
            "is_disease_relevant_transcript": True,
            "lof_mechanism_established": True,
        }
        values.update(overrides)
        return module.pvs1_decision_tree(**values)

    pvs1_cases = [
        observe("LoF mechanism absent", lambda: pvs1(lof_mechanism_established=False), None),
        observe("disease transcript absent", lambda: pvs1(is_disease_relevant_transcript=False), None),
        observe("nonsense NMD", lambda: pvs1(), "PVS1_VeryStrong"),
        observe("escape exactly 10 percent", lambda: pvs1(is_nmd_predicted=False, coding_pct_removed=0.10), "PVS1_Moderate"),
        observe("escape above 10 percent", lambda: pvs1(is_nmd_predicted=False, coding_pct_removed=0.100001), "PVS1_Strong"),
        observe("splice consequence missing", lambda: pvs1(variant_type="splice_donor", is_nmd_predicted=False, coding_pct_removed=0), module.PVS1_REVIEW_REQUIRED),
        observe("splice rescue review missing", lambda: pvs1(variant_type="splice_donor", is_nmd_predicted=True, coding_pct_removed=0, splice_consequence="nmd"), module.PVS1_REVIEW_REQUIRED),
        observe("splice NMD reviewed", lambda: pvs1(variant_type="splice_donor", is_nmd_predicted=True, coding_pct_removed=0, splice_consequence="nmd", rescue_transcript_excluded=True), "PVS1_VeryStrong"),
        observe("splice no impact", lambda: pvs1(variant_type="splice_acceptor", is_nmd_predicted=False, coding_pct_removed=0, splice_consequence="no_impact", rescue_transcript_excluded=True), None),
    ]
    pvs1_conflict = observe(
        "contradictory splice NMD signals",
        lambda: pvs1(
            variant_type="splice_donor", is_nmd_predicted=False, coding_pct_removed=0,
            splice_consequence="nmd", rescue_transcript_excluded=True,
        ),
        "REJECT_CONTRADICTORY_INPUT",
    )
    pvs1_variant_fresh = [
        observe("initiation returns bounded moderate", lambda: pvs1(variant_type="initiation", is_nmd_predicted=False), "PVS1_Moderate"),
        observe("multi-exon noncritical deletion", lambda: pvs1(variant_type="multi_exon_del", is_nmd_predicted=False), "PVS1_Strong"),
    ]

    alpha_expectations = [
        (0.0, "BP4_3pt"), (0.070, "BP4_3pt"), (0.071, "BP4_Moderate"),
        (0.099, "BP4_Moderate"), (0.100, "BP4_Supporting"),
        (0.169, "BP4_Supporting"), (0.170, None), (0.564, None),
        (0.791, None), (0.792, "PP3_Supporting"), (0.905, "PP3_Supporting"),
        (0.906, "PP3_Moderate"), (0.971, "PP3_Moderate"),
        (0.972, "PP3_3pt"), (0.989, "PP3_3pt"), (0.990, "PP3_Strong"),
        (1.0, "PP3_Strong"),
    ]
    alpha = [
        observe(f"AlphaMissense {value}", lambda value=value: module.alphamissense_pp3_bp4(value), expected)
        for value, expected in alpha_expectations
    ]
    alpha_invalid = [
        expect_rejection(f"AlphaMissense rejects {value!r}", lambda value=value: module.alphamissense_pp3_bp4(value))
        for value in [-0.001, 1.001, True, float("nan"), "0.9"]
    ]

    predictor_edges = {
        "revel": [
            observe("REVEL exact 0.003", lambda: module.revel_pp3_bp4(0.003), "BP4_VeryStrong"),
            observe("REVEL exact 0.016", lambda: module.revel_pp3_bp4(0.016), "BP4_Strong"),
            observe("REVEL exact 0.183", lambda: module.revel_pp3_bp4(0.183), "BP4_Moderate"),
            observe("REVEL exact 0.290", lambda: module.revel_pp3_bp4(0.290), "BP4_Supporting"),
            observe("REVEL exact 0.644", lambda: module.revel_pp3_bp4(0.644), "PP3_Supporting"),
            observe("REVEL exact 0.932", lambda: module.revel_pp3_bp4(0.932), "PP3_Strong"),
        ],
        "bayesdel": [
            observe("BayesDel exact -0.36", lambda: module.bayesdel_pp3_bp4(-0.36), "BP4_Moderate"),
            observe("BayesDel exact -0.18", lambda: module.bayesdel_pp3_bp4(-0.18), "BP4_Supporting"),
            observe("BayesDel exact 0.13", lambda: module.bayesdel_pp3_bp4(0.13), "PP3_Supporting"),
            observe("BayesDel exact 0.50", lambda: module.bayesdel_pp3_bp4(0.50), "PP3_Strong"),
        ],
        "spliceai": [
            observe("SpliceAI exact 0.10", lambda: module.spliceai_walker2023(0.10), "BP4_Supporting"),
            observe("SpliceAI 0.15", lambda: module.spliceai_walker2023(0.15), None),
            observe("SpliceAI exact 0.20", lambda: module.spliceai_walker2023(0.20), "PP3_Supporting"),
        ],
    }

    scoring_boundaries = [
        observe("10 points", lambda: module.tavtigian_classify(["PVS1_VeryStrong", "PM2_Supporting", "PP3_Supporting"])["classification"], "Pathogenic"),
        observe("9 points", lambda: module.tavtigian_classify(["PVS1_VeryStrong", "PM2_Supporting"])["classification"], "Likely Pathogenic"),
        observe("6 points", lambda: module.tavtigian_classify(["PS3", "PM2_Supporting", "PP3_Supporting"])["classification"], "Likely Pathogenic"),
        observe("5 points", lambda: module.tavtigian_classify(["PS3", "PP3_Supporting"])["classification"], "VUS"),
        observe("minus 1", lambda: module.tavtigian_classify(["BP1"])["classification"], "Likely Benign"),
        observe("minus 6", lambda: module.tavtigian_classify(["BS1", "BP1", "BP2"])["classification"], "Likely Benign"),
        observe("minus 7", lambda: module.tavtigian_classify(["BS1", "BP1", "BP2", "BP3"])["classification"], "Benign"),
    ]
    scoring_rejections = [
        expect_rejection("unknown criterion", lambda: module.tavtigian_classify(["NOT_A_CRITERION"])),
        expect_rejection("exact duplicate criterion", lambda: module.tavtigian_classify(["PS3", "PS3"])),
        expect_rejection("string instead of sequence", lambda: module.tavtigian_classify("PS3")),
    ]
    semantic_duplicates = [
        observe("two PVS1 strengths", lambda: module.tavtigian_classify(["PVS1_VeryStrong", "PVS1_Strong"]), "REJECT_SEMANTIC_DUPLICATE"),
        observe("PM2 alias plus PM2 Supporting", lambda: module.tavtigian_classify(["PS3", "PM2", "PM2_Supporting"]), "REJECT_SEMANTIC_DUPLICATE"),
        observe("opposed PP3 and BP4", lambda: module.tavtigian_classify(["PP3_Strong", "BP4_Strong"]), "REJECT_CONFLICT"),
    ]
    retired_criteria = [
        observe("PP5 can cross VUS to LP", lambda: module.tavtigian_classify(["PS3", "PM2_Supporting", "PP5"]), "REJECT_RETIRED_PP5"),
        observe("BP6 accepted", lambda: module.tavtigian_classify(["BS1", "BP6"]), "REJECT_RETIRED_BP6"),
    ]
    subsumption = [
        observe(
            "PVS1 subsumes PP3 and PM4",
            lambda: module.classify_with_subsumption(["PVS1_VeryStrong", "PP3_Strong", "PM4", "PM2_Supporting"])["criteria"],
            ["PVS1_VeryStrong", "PM2_Supporting"],
        ),
        observe(
            "result carries guard",
            lambda: all([
                module.tavtigian_classify(["PM2_Supporting"])["review_required"],
                "not for patient diagnosis" in module.tavtigian_classify(["PM2_Supporting"])["clinical_use"],
            ]),
            True,
        ),
    ]

    population = [
        observe("Whiffin default", lambda: round(module.whiffin_max_credible_af(0.001), 8), 0.0005),
        observe("zero observed PM2", lambda: module.bs1_ba1(0.0, 0.001), "PM2_Supporting"),
        observe("above BS1 threshold", lambda: module.bs1_ba1(0.002, 0.001), "BS1"),
        observe("above BA1 threshold", lambda: module.bs1_ba1(0.051, 0.001), "BA1"),
    ]
    numeric_validation = [
        expect_rejection("zero penetrance", lambda: module.whiffin_max_credible_af(0.001, penetrance=0)),
        expect_rejection("negative prevalence", lambda: module.whiffin_max_credible_af(-0.1)),
        expect_rejection("nonfinite frequency", lambda: module.bs1_ba1(float("nan"), 0.001)),
        expect_rejection("bool score", lambda: module.revel_pp3_bp4(True)),
    ]

    def tier(level: str, significance: str = "oncogenic", same: bool = False, date: str = "2026-09-28") -> Any:
        return module.cancer_amp_tier(
            level,
            same_tumor_type=same,
            clinical_significance=significance,
            knowledgebase="CIViC evidence record CIViC-1",
            access_date=date,
        )

    somatic = [
        observe("Tier I-A", lambda: tier("regulatory_approved", same=True)["tier"], "Tier I-A"),
        observe("Tier I-B", lambda: tier("professional_guideline", same=True)["tier"], "Tier I-B"),
        observe("Tier II-C", lambda: tier("clinical_trial")["tier"], "Tier II-C"),
        observe("Tier II-D", lambda: tier("preclinical")["tier"], "Tier II-D"),
        observe("Tier III", lambda: tier("none", "uncertain")["tier"], "Tier III"),
        observe("Tier IV", lambda: tier("none", "benign")["tier"], "Tier IV"),
        observe("somatic result carries guard", lambda: tier("none", "uncertain")["review_required"], True),
    ]
    somatic_invalid = [
        expect_rejection("invalid evidence enum", lambda: tier(-1)),
        expect_rejection("oncogenic without evidence", lambda: tier("none", "oncogenic")),
        expect_rejection("benign with actionable evidence", lambda: tier("preclinical", "benign")),
        expect_rejection("empty knowledgebase", lambda: module.cancer_amp_tier("none", same_tumor_type=False, clinical_significance="uncertain", knowledgebase="", access_date="2026-09-28")),
    ]
    invalid_date = observe(
        "semantically impossible access date",
        lambda: tier("none", "uncertain", date="2026-99-99"),
        "REJECT_INVALID_DATE",
    )

    interface_preflight = [
        expect_rejection("invalid chromosome", lambda: module.genebe_api("chr0", 1, "A", "C")),
        expect_rejection("negative position", lambda: module.genebe_api("1", -1, "A", "C")),
        expect_rejection("invalid CSpec symbol", lambda: module.cspec_gene_versions("../bad")),
        expect_rejection("invalid timeout", lambda: module.cspec_gene_versions("GATM", timeout=0)),
    ]
    live_candidate = {}
    try:
        genebe = module.genebe_api("17", 28364411, "C", "A")
        variants = genebe.get("variants", [])
        live_candidate["genebe"] = {
            "status": "PASS" if isinstance(variants, list) and variants else "FAIL",
            "record_count": len(variants) if isinstance(variants, list) else None,
            "first_record_keys": sorted(variants[0]) if isinstance(variants, list) and variants else [],
        }
    except Exception as exc:  # noqa: BLE001
        live_candidate["genebe"] = {"status": "ERROR", "error": f"{type(exc).__name__}: {exc}"}
    try:
        cspec = module.cspec_gene_versions("GATM")
        versions = cspec.get("data", [])
        live_candidate["cspec"] = {
            "status": "PASS" if isinstance(versions, list) and versions else "FAIL",
            "record_count": len(versions) if isinstance(versions, list) else None,
            "version_ids": [row.get("@id") for row in versions] if isinstance(versions, list) else [],
        }
    except Exception as exc:  # noqa: BLE001
        live_candidate["cspec"] = {"status": "ERROR", "error": f"{type(exc).__name__}: {exc}"}

    static_text = (CANDIDATE / "references" / "acmg-framework.md").read_text(encoding="utf-8")
    static_checks = {
        "practice_boundary_in_skill": "not a medical device" in (CANDIDATE / "SKILL.md").read_text(encoding="utf-8"),
        "stale_cspec_route_marked": "former `/cspec/ui/svi/all` GET route is stale" in static_text,
        "brnich_table_corrected": "> 4.3 to 18.7 | Moderate" in static_text and "> 18.7 to 350 | Strong" in static_text,
        "contradictory_brnich_sentence_present": "requires OddsPath > 4.3 for Strong" in static_text,
        "pp5_bp6_retirement_documented": "PP5" in static_text and "should not" in static_text,
    }

    after = manifest_identity()
    if after["digest"] != before["digest"]:
        raise SystemExit(f"candidate changed during re-audit: {before['digest']} -> {after['digest']}")

    result = {
        "phase": "independent-reaudit",
        "started_at": started,
        "completed_at": datetime.now(timezone.utc).isoformat(),
        "runtime": {"python": sys.version, "requests": getattr(module.requests, "__version__", "unknown")},
        "candidate_identity_before": before,
        "candidate_identity_after": after,
        "surface_runs": {"compile": compile_runs, "unit_tests": unit, "standalone_demo": demo, "live_interface_smoke": live},
        "workflows": {
            "oddspath": {"cases": oddspath, "invalid": oddspath_invalid},
            "pvs1": {"cases": pvs1_cases, "conflict": pvs1_conflict, "fresh_variant_cases": pvs1_variant_fresh},
            "alphamissense": {"cases": alpha, "invalid": alpha_invalid},
            "other_predictor_boundaries": predictor_edges,
            "tavtigian": {
                "boundaries": scoring_boundaries,
                "basic_rejections": scoring_rejections,
                "semantic_duplicates": semantic_duplicates,
                "retired_criteria": retired_criteria,
                "subsumption": subsumption,
            },
            "population": {"cases": population, "invalid": numeric_validation},
            "somatic": {"cases": somatic, "invalid": somatic_invalid, "invalid_date": invalid_date},
            "interfaces": {"preflight": interface_preflight, "live": live_candidate},
        },
        "static_checks": static_checks,
    }
    (ROOT / "evidence" / "execution.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    (ROOT / "evidence" / "candidate-manifest.json").write_text(
        json.dumps(before, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    (ROOT / "evidence" / "unit-tests.log").write_text(
        unit["stdout"] + unit["stderr"], encoding="utf-8"
    )
    (ROOT / "evidence" / "standalone-demo.log").write_text(
        demo["stdout"] + demo["stderr"], encoding="utf-8"
    )
    (ROOT / "evidence" / "live-interface-smoke.log").write_text(
        live["stdout"] + live["stderr"], encoding="utf-8"
    )
    summary = {
        "candidate_identity": before["digest"],
        "identity_stable": before["digest"] == after["digest"] == EXPECTED_IDENTITY,
        "unit_tests_exit": unit["returncode"],
        "demo_exit": demo["returncode"],
        "live_smoke_exit": live["returncode"],
        "compile_exits": [row["returncode"] for row in compile_runs],
        "oddspath_matches": sum(row.get("match") is True for row in oddspath),
        "oddspath_total": len(oddspath),
        "pvs1_matches": sum(row.get("match") is True for row in pvs1_cases),
        "pvs1_total": len(pvs1_cases),
        "alpha_matches": sum(row.get("match") is True for row in alpha),
        "alpha_total": len(alpha),
        "predictor_edge_matches": sum(
            row.get("match") is True for rows in predictor_edges.values() for row in rows
        ),
        "predictor_edge_total": sum(len(rows) for rows in predictor_edges.values()),
        "live": live_candidate,
        "known_failures": {
            "pvs1_conflicting_signals_rejected": pvs1_conflict.get("match") is True,
            "semantic_duplicate_or_conflict_rejections": sum(row.get("match") is True for row in semantic_duplicates),
            "retired_criteria_rejections": sum(row.get("match") is True for row in retired_criteria),
            "semantic_access_date_rejected": invalid_date.get("match") is True,
            "brnich_reference_self_consistent": not static_checks["contradictory_brnich_sentence_present"],
        },
    }
    print(json.dumps(summary, sort_keys=True))


if __name__ == "__main__":
    main()
