#!/usr/bin/env python3
"""Independent bounded re-audit for the exact ACMG candidate."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path
import subprocess
import sys


CANDIDATE = Path(os.environ["ACMG_CANDIDATE"])
OUT = Path(os.environ["ACMG_AUDIT_OUT"])
MODULE_PATH = CANDIDATE / "scripts" / "acmg_classify.py"
EXPECTED_IDENTITY = "286df2647ef2e418d8302102c7522705f7b5ce4156cfaea6be5c8c36c6d55571"


def file_sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def candidate_identity() -> dict[str, object]:
    rows: list[str] = []
    for path in sorted(
        (item for item in CANDIDATE.rglob("*") if item.is_file()),
        key=lambda item: item.relative_to(CANDIDATE).as_posix(),
    ):
        rel = path.relative_to(CANDIDATE).as_posix()
        rows.append(f"{rel}\t{path.stat().st_size}\t{file_sha(path)}")
    manifest = "\n".join(rows).encode("utf-8")
    return {
        "identity_scheme": "sha256-manifest-v1",
        "content_sha256": hashlib.sha256(manifest).hexdigest(),
        "manifest_bytes": len(manifest),
        "file_count": len(rows),
        "manifest_rows": rows,
    }


def load_candidate():
    spec = importlib.util.spec_from_file_location("reaudit_acmg", MODULE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("candidate module could not be loaded")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def observe_exception(call) -> dict[str, str]:
    try:
        call()
    except Exception as exc:
        return {"type": type(exc).__name__, "message": str(exc)}
    raise AssertionError("invalid probe unexpectedly succeeded")


def checked(function, cases):
    observations = []
    for value, expected in cases:
        actual = function(value)
        assert actual == expected, (value, expected, actual)
        observations.append({"input": value, "expected": expected, "actual": actual})
    return observations


def pvs1(module, **overrides):
    args = {
        "variant_type": "nonsense",
        "is_nmd_predicted": True,
        "coding_pct_removed": 0.01,
        "in_critical_region": False,
        "is_disease_relevant_transcript": True,
        "lof_mechanism_established": True,
    }
    args.update(overrides)
    return module.pvs1_decision_tree(**args)


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    module = load_candidate()
    identity = candidate_identity()
    assert identity["content_sha256"] == EXPECTED_IDENTITY
    assert identity["file_count"] == 7

    result: dict[str, object] = {
        "candidate_identity": identity,
        "runtime": {
            "python": sys.version,
            "requests": module.requests.__version__,
            "candidate": str(CANDIDATE),
        },
    }

    invalid = {
        "criteria_string": lambda: module.tavtigian_classify("PS3"),
        "criteria_non_string": lambda: module.tavtigian_classify([1]),
        "criteria_unknown": lambda: module.tavtigian_classify(["UNKNOWN"]),
        "criteria_duplicate": lambda: module.tavtigian_classify(["PS3", "PS3"]),
        "retired_pp5": lambda: module.tavtigian_classify(["PP5"]),
        "retired_bp6": lambda: module.tavtigian_classify(["BP6"]),
        "pvs1_family": lambda: module.tavtigian_classify(["PVS1_VeryStrong", "PVS1_Strong"]),
        "ps3_family": lambda: module.tavtigian_classify(["PS3", "PS3_Moderate"]),
        "pm2_alias_family": lambda: module.tavtigian_classify(["PM2", "PM2_Supporting"]),
        "pp3_family": lambda: module.tavtigian_classify(["PP3_3pt", "PP3_Strong"]),
        "bp4_family": lambda: module.tavtigian_classify(["BP4_3pt", "BP4_Strong"]),
        "pp3_bp4_conflict": lambda: module.tavtigian_classify(["PP3_Strong", "BP4_Strong"]),
        "revel_bool": lambda: module.revel_pp3_bp4(True),
        "revel_nan": lambda: module.revel_pp3_bp4(math.nan),
        "revel_above_one": lambda: module.revel_pp3_bp4(1.01),
        "splice_below_zero": lambda: module.spliceai_walker2023(-0.01),
        "whiffin_zero_penetrance": lambda: module.whiffin_max_credible_af(0.01, penetrance=0),
        "bs1_bad_order": lambda: module.bs1_ba1(0.01, 0.06, 0.05),
        "genebe_bad_chrom": lambda: module.genebe_api("chr0", 1, "A", "C"),
        "genebe_bad_position": lambda: module.genebe_api("1", 0, "A", "C"),
        "genebe_bad_allele": lambda: module.genebe_api("1", 1, "A", "-"),
        "cspec_path_injection": lambda: module.cspec_gene_versions("../GATM"),
        "somatic_empty_source": lambda: module.cancer_amp_tier(
            "none", same_tumor_type=False, clinical_significance="uncertain",
            knowledgebase="", access_date="2026-09-28"
        ),
        "somatic_bad_level": lambda: module.cancer_amp_tier(
            -1, same_tumor_type=False, clinical_significance="uncertain",
            knowledgebase="CIViC-1", access_date="2026-09-28"
        ),
        "somatic_conflict": lambda: module.cancer_amp_tier(
            "clinical_trial", same_tumor_type=False, clinical_significance="benign",
            knowledgebase="CIViC-1", access_date="2026-09-28"
        ),
    }
    result["invalid_probes"] = {name: observe_exception(call) for name, call in invalid.items()}

    result["predictor_endpoints"] = {
        "revel": checked(module.revel_pp3_bp4, [
            (0.003, "BP4_VeryStrong"), (0.003001, "BP4_Strong"),
            (0.016, "BP4_Strong"), (0.016001, "BP4_Moderate"),
            (0.183, "BP4_Moderate"), (0.183001, "BP4_Supporting"),
            (0.290, "BP4_Supporting"), (0.290001, None),
            (0.644, "PP3_Supporting"), (0.773, "PP3_Moderate"),
            (0.932, "PP3_Strong"),
        ]),
        "bayesdel": checked(module.bayesdel_pp3_bp4, [
            (-0.36, "BP4_Moderate"), (-0.359999, "BP4_Supporting"),
            (-0.18, "BP4_Supporting"), (-0.179999, None),
            (0.13, "PP3_Supporting"), (0.27, "PP3_Moderate"),
            (0.50, "PP3_Strong"),
        ]),
        "alphamissense": checked(module.alphamissense_pp3_bp4, [
            (0.070, "BP4_3pt"), (0.071, "BP4_Moderate"),
            (0.100, "BP4_Supporting"), (0.170, None),
            (0.792, "PP3_Supporting"), (0.906, "PP3_Moderate"),
            (0.972, "PP3_3pt"), (0.990, "PP3_Strong"),
        ]),
    }
    assert module.STRENGTH_POINTS["BP4_3pt"] == -3
    assert module.STRENGTH_POINTS["PP3_3pt"] == 3

    date_cases = {
        "valid_non_leap": "2026-02-28",
        "valid_leap": "2024-02-29",
        "invalid_month": "2026-13-01",
        "invalid_day": "2026-02-30",
        "invalid_non_leap": "2025-02-29",
        "noncanonical": "2026-9-28",
    }
    valid_dates = {}
    for name in ("valid_non_leap", "valid_leap"):
        value = date_cases[name]
        valid_dates[name] = module.cancer_amp_tier(
            "none", same_tumor_type=False, clinical_significance="uncertain",
            knowledgebase="CIViC-1", access_date=value,
        )["access_date"]
    invalid_dates = {}
    for name in ("invalid_month", "invalid_day", "invalid_non_leap", "noncanonical"):
        value = date_cases[name]
        invalid_dates[name] = observe_exception(lambda value=value: module.cancer_amp_tier(
            "none", same_tumor_type=False, clinical_significance="uncertain",
            knowledgebase="CIViC-1", access_date=value,
        ))
    result["iso_dates"] = {"valid": valid_dates, "invalid": invalid_dates}

    pvs1_states = {
        "lof_gate": pvs1(module, lof_mechanism_established=False),
        "transcript_gate": pvs1(module, is_disease_relevant_transcript=False),
        "splice_review_stop": pvs1(
            module, variant_type="splice_donor", is_nmd_predicted=False,
            coding_pct_removed=0, splice_consequence=None,
        ),
        "splice_rescue_stop": pvs1(
            module, variant_type="splice_donor", is_nmd_predicted=True,
            coding_pct_removed=0, splice_consequence="nmd",
        ),
        "splice_nmd": pvs1(
            module, variant_type="splice_donor", is_nmd_predicted=True,
            coding_pct_removed=0, splice_consequence="nmd", rescue_transcript_excluded=True,
        ),
        "splice_no_impact": pvs1(
            module, variant_type="splice_acceptor", is_nmd_predicted=False,
            coding_pct_removed=0, splice_consequence="no_impact", rescue_transcript_excluded=True,
        ),
        "initiation": pvs1(module, variant_type="initiation", is_nmd_predicted=False),
        "single_exon_critical": pvs1(
            module, variant_type="single_exon_del", is_nmd_predicted=False,
            coding_pct_removed=1.0, in_critical_region=True,
        ),
        "multi_exon_noncritical": pvs1(
            module, variant_type="multi_exon_del", is_nmd_predicted=False,
            coding_pct_removed=0.5, in_critical_region=False,
        ),
    }
    assert pvs1_states == {
        "lof_gate": None,
        "transcript_gate": None,
        "splice_review_stop": module.PVS1_REVIEW_REQUIRED,
        "splice_rescue_stop": module.PVS1_REVIEW_REQUIRED,
        "splice_nmd": "PVS1_VeryStrong",
        "splice_no_impact": None,
        "initiation": "PVS1_Moderate",
        "single_exon_critical": "PVS1_VeryStrong",
        "multi_exon_noncritical": "PVS1_Strong",
    }
    contradictions = {
        "false_vs_nmd": observe_exception(lambda: pvs1(
            module, variant_type="splice_donor", is_nmd_predicted=False,
            coding_pct_removed=0, splice_consequence="nmd", rescue_transcript_excluded=True,
        )),
        "true_vs_in_frame": observe_exception(lambda: pvs1(
            module, variant_type="splice_acceptor", is_nmd_predicted=True,
            coding_pct_removed=0.05, splice_consequence="in_frame_disruptive",
            rescue_transcript_excluded=True,
        )),
        "true_vs_no_impact": observe_exception(lambda: pvs1(
            module, variant_type="splice_acceptor", is_nmd_predicted=True,
            coding_pct_removed=0, splice_consequence="no_impact", rescue_transcript_excluded=True,
        )),
    }
    assert all(item["type"] == "ValueError" for item in contradictions.values())
    result["pvs1"] = {"states": pvs1_states, "contradictions": contradictions}

    result["oddspath"] = checked(module.ps3_oddspath, [
        (350.000001, "PS3_VeryStrong"), (350, "PS3"),
        (18.700001, "PS3"), (18.7, "PS3_Moderate"),
        (4.300001, "PS3_Moderate"), (4.3, "PS3_Supporting"),
        (2.100001, "PS3_Supporting"), (2.1, None),
        (0.48, None), (0.479999, "BS3_Supporting"),
        (0.23, "BS3_Supporting"), (0.229999, "BS3_Moderate"),
        (0.053, "BS3_Moderate"), (0.052999, "BS3"),
    ])
    framework = (CANDIDATE / "references" / "acmg-framework.md").read_text(encoding="utf-8")
    assert "OddsPath > 4.3 for Moderate and > 18.7 for Strong" in framework
    assert "OddsPath > 4.3 for Strong" not in framework
    result["oddspath_prose"] = {
        "correct_sentence_present": True,
        "obsolete_sentence_absent": True,
    }

    retained = module.classify_with_subsumption(
        ["PVS1_VeryStrong", "PP3_Strong", "PM2_Supporting"]
    )
    assert retained["criteria"] == ["PVS1_VeryStrong", "PM2_Supporting"]
    assert retained["review_required"] is True
    assert "not for patient diagnosis" in retained["clinical_use"]
    result["germline_guard"] = retained

    somatic_cases = {
        "Tier I-A": ("regulatory_approved", True, "oncogenic"),
        "Tier I-B": ("professional_guideline", True, "oncogenic"),
        "Tier II-C": ("clinical_trial", False, "likely_oncogenic"),
        "Tier II-D": ("preclinical", False, "oncogenic"),
        "Tier III": ("none", False, "uncertain"),
        "Tier IV": ("none", False, "benign"),
    }
    somatic = {}
    for expected, (level, same, significance) in somatic_cases.items():
        value = module.cancer_amp_tier(
            level, same_tumor_type=same, clinical_significance=significance,
            knowledgebase="CIViC evidence record CIViC-1", access_date="2026-09-28",
        )
        assert value["tier"] == expected
        assert value["review_required"] is True
        assert "not for patient diagnosis" in value["clinical_use"]
        somatic[expected] = value
    assert somatic["Tier III"]["rationale"] != somatic["Tier IV"]["rationale"]
    result["somatic_tiers"] = somatic

    demo = subprocess.run(
        [sys.executable, "-B", str(MODULE_PATH)],
        check=True, capture_output=True, text=True,
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
    )
    demo_markers = [
        "NON-DIAGNOSTIC TRAINING EXAMPLE", "not for patient diagnosis",
        "disease=unresolved", "transcript=unresolved", "VCEP=not checked",
        "assay validity=unreviewed", "PS3_Moderate", "qualified review",
    ]
    assert all(marker in demo.stdout for marker in demo_markers)
    assert "BP4_Supporting" not in demo.stdout
    result["standalone_demo"] = {
        "stdout": demo.stdout,
        "stderr": demo.stderr,
        "required_markers": demo_markers,
        "discordant_bp4_present": False,
    }

    live_genebe = module.genebe_api("17", 28364411, "C", "A", timeout=30)
    variants = live_genebe.get("variants", [])
    assert isinstance(variants, list) and variants
    live_cspec = module.cspec_gene_versions("GATM", timeout=30)
    versions = live_cspec.get("data", [])
    assert isinstance(versions, list) and versions
    assert all("/version/" in row.get("@id", "") for row in versions)
    result["live_interfaces"] = {
        "genebe": {
            "input": "hg38 chr17:28364411 C>A public documentation example",
            "variant_records": len(variants),
            "first_record": {
                key: variants[0].get(key)
                for key in ("chr", "pos", "ref", "alt", "gene_symbol", "acmg_classification")
                if key in variants[0]
            },
        },
        "cspec": {
            "input": "GATM",
            "version_records": len(versions),
            "ids": [row.get("@id") for row in versions],
        },
    }

    result["all_checks_pass"] = True
    destination = OUT / "execution.json"
    destination.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "all_checks_pass": True,
        "candidate_identity": identity["content_sha256"],
        "invalid_probes": len(result["invalid_probes"]),
        "predictor_endpoint_cases": sum(len(items) for items in result["predictor_endpoints"].values()),
        "pvs1_states": len(pvs1_states),
        "pvs1_contradictions": len(contradictions),
        "oddspath_cases": len(result["oddspath"]),
        "somatic_tiers": len(somatic),
        "genebe_records": len(variants),
        "cspec_versions": len(versions),
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
