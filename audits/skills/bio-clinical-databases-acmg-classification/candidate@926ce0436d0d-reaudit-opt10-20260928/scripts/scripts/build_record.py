#!/usr/bin/env python3
"""Build the strict modular re-audit record from independent raw evidence."""

from __future__ import annotations

import hashlib
import json
import pathlib


ROOT = pathlib.Path(__file__).resolve().parents[1]
EVIDENCE = json.loads((ROOT / "evidence" / "execution.json").read_text(encoding="utf-8"))
CANDIDATE = pathlib.Path(
    r"F:\OpenScience\wt\opt10-acmg-classification\skills\bio-clinical-databases-acmg-classification"
)
IDENTITY = "926ce0436d0d9fd1fb73a5f2b83728adfb622cf6f8ec41c8c00ad8d8300e8c07"


def assertion(text: str, passed: bool, note: str) -> dict:
    return {"text": text, "result": "PASS" if passed else "FAIL", "note": note}


inputs = [
    {
        "index": 1,
        "type": "Canonical",
        "label": "Guarded synthetic germline evidence ledger",
        "prompt": "Run the shipped training example for a synthetic germline variant and inspect predictor selection, PS3 calibration, unresolved context, classification output, and the non-diagnostic qualified-review boundary.",
    },
    {
        "index": 2,
        "type": "Variant A",
        "label": "PVS1 prerequisites and splice stop states",
        "prompt": "Exercise LoF-mechanism and transcript-relevance gates, NMD and 10 percent branches, canonical-splice consequence and rescue review, plus contradictory NMD inputs.",
    },
    {
        "index": 3,
        "type": "Edge",
        "label": "Brnich OddsPath exact boundaries and mirrors",
        "prompt": "Evaluate exact and adjacent pathogenic and benign Brnich Table 3 OddsPath boundaries, nonpositive and non-finite inputs, and agreement between code and reference prose.",
    },
    {
        "index": 4,
        "type": "Variant B",
        "label": "Tavtigian scoring and evidence-family integrity",
        "prompt": "Exercise all classification endpoints, unknown and duplicate criteria, PVS1 subsumption, multiple strengths from one criterion family, opposing predictor codes, and criteria retired by current ClinGen guidance.",
    },
    {
        "index": 5,
        "type": "Stress",
        "label": "Bergquist and Pejaver calibrated predictor endpoints",
        "prompt": "Re-run the full AlphaMissense interval table including the -3/+3 point bands and fresh exact REVEL, BayesDel, and SpliceAI endpoint cases with invalid-domain controls.",
    },
    {
        "index": 6,
        "type": "Scope Boundary",
        "label": "Population and somatic evidence validation",
        "prompt": "Exercise Whiffin, BS1/BA1, all six distinct AMP tiers, germline/somatic vocabulary separation, strict numeric/enumerated validation, provenance, and access-date validation.",
    },
    {
        "index": 7,
        "type": "Adversarial",
        "label": "Current public GeneBe and ClinGen CSpec interfaces",
        "prompt": "Run the shipped bounded live smoke and direct candidate helpers against current public GeneBe coordinate and CSpec versioned-gene routes, including invalid preflight inputs and the no-PHI boundary.",
    },
]

rows = [
    {
        "index": 1,
        "type": "Canonical",
        "label": inputs[0]["label"],
        "status": "COMPLETED",
        "status_flag": "✅",
        "note": "The demo exited zero, used one predictor, mapped OddsPath 8 to PS3 Moderate, printed unresolved context and the qualified-review boundary; it remains a compact sketch rather than a complete versioned evidence ledger.",
        "basic": 34,
        "specialized": 50,
        "assertions": [
            assertion("The shipped standalone demonstration executes successfully.", True, "Exit status was zero and output was retained in standalone-demo.log."),
            assertion("The demonstration uses one computational predictor and does not stack discordant BP4 evidence.", True, "Output retained REVEL only and contained no BP4 criterion."),
            assertion("OddsPath 8 is represented as PS3 Moderate.", True, "The retained criteria list contains PS3_Moderate."),
            assertion("The output states unresolved disease, transcript, VCEP, and assay-validity context plus a non-diagnostic qualified-review boundary.", True, "All four unresolved fields and the medical-use guard were printed."),
            assertion("The demonstration emits a complete versioned evidence ledger with sources, overrides, exclusions, and access dates.", False, "The compact demo warns that context is unresolved but does not emit the complete ledger promised by the main workflow."),
        ],
    },
    {
        "index": 2,
        "type": "Variant A",
        "label": inputs[1]["label"],
        "status": "COMPLETED",
        "status_flag": "⚠️",
        "note": "The prerequisite gates, NMD and 10 percent branches, and splice review stop states passed, but contradictory NMD inputs silently produced PVS1 Very Strong.",
        "basic": 30,
        "specialized": 43,
        "assertions": [
            assertion("PVS1 is withheld when the LoF disease mechanism is not established.", True, "The function returned no evidence."),
            assertion("PVS1 is withheld for a disease-irrelevant transcript.", True, "The function returned no evidence."),
            assertion("Canonical splice calls stop for missing consequence or rescue-transcript review.", True, "Both incomplete cases returned PVS1_REVIEW_REQUIRED."),
            assertion("NMD and exact/above 10 percent branches produce the documented strengths.", True, "Very Strong, Moderate, and Strong observations matched the documented branches."),
            assertion("Contradictory splice NMD signals are rejected before strength assignment.", False, "is_nmd_predicted=False with splice_consequence=nmd returned PVS1_VeryStrong."),
        ],
    },
    {
        "index": 3,
        "type": "Edge",
        "label": inputs[2]["label"],
        "status": "COMPLETED",
        "status_flag": "✅",
        "note": "All 14 exact/adjacent OddsPath cases and invalid-domain guards passed; one failure-mode sentence still calls greater than 4.3 Strong, contradicting the corrected table and code.",
        "basic": 36,
        "specialized": 53,
        "assertions": [
            assertion("Pathogenic OddsPath bands implement Supporting, Moderate, Strong, and Very Strong at the documented boundaries.", True, "All pathogenic exact and adjacent cases matched Brnich Table 3."),
            assertion("Benign mirror bands implement Supporting, Moderate, and Strong at the documented boundaries.", True, "All benign exact and adjacent cases matched."),
            assertion("Nonpositive, non-finite, boolean, and string OddsPath inputs are rejected.", True, "All six invalid probes raised actionable type or value errors."),
            assertion("The reference threshold table agrees with the executable mapping.", True, "The table uses greater than 2.1, 4.3, 18.7, and 350 and the reciprocal benign mirrors."),
            assertion("All Brnich explanatory prose is internally consistent with the corrected table.", False, "Failure mode 6 still states that greater than 4.3 is required for Strong before its next sentence correctly calls that band Moderate."),
        ],
    },
    {
        "index": 4,
        "type": "Variant B",
        "label": inputs[3]["label"],
        "status": "COMPLETED",
        "status_flag": "⚠️",
        "note": "Numeric endpoints, exact duplicate rejection, and basic subsumption passed; retired PP5/BP6, same-family multiple strengths, aliases, and opposed computational evidence remain accepted and can change a category.",
        "basic": 23,
        "specialized": 24,
        "assertions": [
            assertion("The 10, 9, 6, 5, -1, -6, and -7 Tavtigian classification endpoints are correct.", True, "All seven endpoint fixtures matched."),
            assertion("Unknown criteria, exact duplicates, and a string in place of a criterion sequence are rejected.", True, "All three basic validation probes raised."),
            assertion("Only one strength or alias from each ACMG evidence family can be counted.", False, "PVS1 Very Strong plus PVS1 Strong scored 12; PM2 plus PM2 Supporting was also double-counted."),
            assertion("ClinGen-retired PP5 and BP6 are rejected by the current-rule scorer.", False, "Both remain in STRENGTH_POINTS; PP5 changed a five-point VUS fixture to six-point Likely Pathogenic."),
            assertion("Opposing computational evidence is surfaced as a conflict instead of arithmetically cancelled.", False, "PP3 Strong plus BP4 Strong was accepted and returned a zero-point VUS without a conflict field."),
        ],
    },
    {
        "index": 5,
        "type": "Stress",
        "label": inputs[4]["label"],
        "status": "COMPLETED",
        "status_flag": "⚠️",
        "note": "All 17 AlphaMissense cases and all SpliceAI cases passed, including explicit +/-3 point labels; four REVEL and two BayesDel exact benign endpoints were assigned to the next weaker band or to no evidence.",
        "basic": 27,
        "specialized": 35,
        "assertions": [
            assertion("All Bergquist AlphaMissense intervals, including the indeterminate interval, match the cited table.", True, "All 17 exact and fresh values matched."),
            assertion("The Bergquist -3 and +3 point intervals remain explicit point codes.", True, "BP4_3pt and PP3_3pt were returned and carry -3/+3 points."),
            assertion("Out-of-domain AlphaMissense inputs and exact SpliceAI endpoints are handled correctly.", True, "All invalid AlphaMissense probes rejected; SpliceAI 0.10, 0.15, and 0.20 matched."),
            assertion("REVEL exact benign-side endpoints use the inclusive boundaries documented by the candidate.", False, "0.003, 0.016, 0.183, and 0.290 were placed in the next interval or made indeterminate."),
            assertion("BayesDel exact benign-side endpoints use the inclusive boundaries documented by the candidate.", False, "-0.36 became Supporting and -0.18 became indeterminate rather than Moderate and Supporting."),
        ],
    },
    {
        "index": 6,
        "type": "Scope Boundary",
        "label": inputs[5]["label"],
        "status": "COMPLETED",
        "status_flag": "✅",
        "note": "Population helpers, numeric guards, all six somatic tiers, and the qualified-review boundary passed; the YYYY-MM-DD regex accepted the impossible date 2026-99-99.",
        "basic": 33,
        "specialized": 49,
        "assertions": [
            assertion("Whiffin, PM2 Supporting, BS1, and BA1 bounded cases produce the documented outcomes.", True, "All four population cases matched and invalid numeric domains rejected."),
            assertion("Germline and somatic classification vocabularies remain separate.", True, "Germline returned P/LP/VUS/LB/B vocabulary while somatic returned Tier labels."),
            assertion("Tier I-A, I-B, II-C, II-D, III, and IV are independently reachable.", True, "All six tier cases matched and III/IV had distinct rationales."),
            assertion("Somatic enum conflicts, empty provenance, and unsupported oncogenic evidence are rejected.", True, "All four invalid somatic probes raised actionable errors."),
            assertion("The access date is a real calendar date, not only a digit pattern.", False, "2026-99-99 was accepted and preserved in a Tier III result."),
        ],
    },
    {
        "index": 7,
        "type": "Adversarial",
        "label": inputs[6]["label"],
        "status": "COMPLETED",
        "status_flag": "✅",
        "note": "The shipped live smoke and independent direct calls passed: GeneBe returned one public documentation-example record and CSpec returned six GATM version records; preflight guards ran before requests.",
        "basic": 37,
        "specialized": 57,
        "assertions": [
            assertion("The current GeneBe coordinate helper succeeds and returns a parsed variant list.", True, "One record was returned for the public documentation coordinate."),
            assertion("The current ClinGen CSpec versioned-gene helper succeeds and returns version identifiers.", True, "Six GATM version records were returned."),
            assertion("Invalid chromosome, position, symbol, and timeout inputs fail before a network request.", True, "All four preflight cases rejected."),
            assertion("The former CSpec UI route is marked stale and the current REST workflow is documented.", True, "Both statements are present in the reference."),
            assertion("The public-interface workflow explicitly prohibits PHI and uses only public examples.", True, "The skill and live-smoke docstring prohibit patient/private data; retained inputs are public documentation examples."),
        ],
    },
]

for row in rows:
    row["total"] = row["basic"] + row["specialized"]
    row["assertions_passed"] = sum(a["result"] == "PASS" for a in row["assertions"])
    row["assertions_total"] = len(row["assertions"])

execution_avg = round(sum(row["total"] for row in rows) / len(rows), 1)
passed = sum(row["assertions_passed"] for row in rows)
total = sum(row["assertions_total"] for row in rows)

report = {
    "meta": {
        "skill_name": "bio-clinical-databases-acmg-classification",
        "description": "Builds a non-diagnostic ACMG/AMP or AMP/ASCO/CAP evidence ledger using current ClinGen SVI methods, calibrated PP3/BP4 and PS3/BS3 thresholds, PVS1 prerequisite gates, and explicit somatic tiers. Use for training or qualified-review support, never stand-alone patient diagnosis or treatment decisions.",
        "evaluated_on": "2026-09-28",
        "evaluator_version": "skill-auditor@1.0",
        "category": "Data Analysis",
        "execution_mode": "D",
        "complexity": "Complex",
        "n_inputs": 7,
    },
    "veto_gates": {
        "skill_veto": {
            "gate": "PASS",
            "stability": "PASS",
            "contract": "PASS",
            "determinism": "PASS",
            "security": "PASS",
        },
        "research_veto": {
            "applicable": True,
            "gate": "FAIL",
            "scientific_integrity": {
                "result": "PASS",
                "detail": "No output fabricated patient results, studies, identifiers, sample sizes, p-values, or treatment effects; all observations trace to candidate execution, public documentation examples, or identified primary guidance.",
            },
            "practice_boundaries": {
                "result": "PASS",
                "detail": "The skill, germline result, somatic result, and demonstration prohibit diagnostic or treatment use, require qualified review, and prohibit PHI in public interfaces.",
            },
            "methodological_ground": {
                "result": "FAIL",
                "detail": "The scorer accepts ClinGen-retired PP5/BP6, double-counts multiple strengths or aliases from one criterion family, silently cancels opposing computational evidence, and mis-bins exact documented REVEL/BayesDel endpoints; PP5 and same-family duplication demonstrably changed classifications.",
            },
            "code_usability": {
                "result": "PASS",
                "detail": "All three Python files compiled; 16 shipped tests, the standalone demo, the bounded live smoke, and direct current GeneBe/CSpec calls executed successfully in the pinned environment.",
            },
        },
    },
    "static_score": {
        "subtotal": 76,
        "max": 100,
        "categories": {
            "functional_suitability": {"score": 9, "max": 12, "note": "The major workflows are present and ACMG-001 through ACMG-005, ACMG-007 through ACMG-009 are materially improved, but current-rule scoring can still be changed by retired or duplicate evidence."},
            "reliability": {"score": 7, "max": 12, "note": "Typed/domain guards and runnable regressions are strong; evidence-family uniqueness, conflicting PVS1 state, semantic dates, and exact inclusive boundaries remain unsafe."},
            "performance_context": {"score": 7, "max": 8, "note": "The concise main skill routes detail into one method reference and one reusable implementation with little redundant execution."},
            "agent_usability": {"score": 12, "max": 16, "note": "Authority order, stop states, and result guards are clear, but the executable does not enforce all current-rule exclusions or emit the complete ledger promised by the workflow."},
            "human_usability": {"score": 7, "max": 8, "note": "Natural triggers, readable tables, explicit uncertainty, and medical-use boundaries are present; one Brnich sentence conflicts with the corrected table."},
            "security": {"score": 11, "max": 12, "note": "No credentials, PHI, raw-code execution, or destructive behavior exists; bounded public calls validate key request fields and explicitly prohibit patient data."},
            "maintainability": {"score": 9, "max": 12, "note": "The module and 16-test suite are readable and deterministic, but regressions omit retired criteria, criterion-family duplication, exact benign endpoints, semantic dates, and contradictory PVS1 state."},
            "agent_specific": {"score": 14, "max": 20, "note": "Triggering, progressive disclosure, deterministic helpers, and escape hatches are good; incomplete conflict/alias validation prevents safe composition into a current evidence ledger."},
        },
    },
    "dynamic_score": {
        "execution_avg": execution_avg,
        "max": 100,
        "assertion_pass_rate": {"passed": passed, "total": total},
        "inputs": rows,
    },
    "final": {
        "static_weighted": 30.4,
        "dynamic_weighted": round(execution_avg * 0.6, 1),
        "score": round(30.4 + round(execution_avg * 0.6, 1)),
        "max": 100,
        "grade": "Reject",
        "grade_symbol": "❌",
        "deployable": False,
        "veto_override": True,
    },
    "key_strengths": [
        "The corrected Brnich code and table passed all 14 exact and adjacent pathogenic/benign boundary cases, including Very Strong above 350.",
        "The Bergquist AlphaMissense implementation passed all 17 cases and preserves the published -3/+3 point bands without rounding them to legacy strengths.",
        "LoF mechanism, transcript relevance, and incomplete canonical-splice review now stop PVS1, while all germline and somatic results retain a non-diagnostic qualified-review boundary.",
        "Current GeneBe coordinate and ClinGen CSpec versioned-gene interfaces passed bounded public live execution, and Tier III and Tier IV are distinct.",
    ],
    "recommendations": [
        {
            "priority": "P0",
            "title": "ACMG-006: Enforce current evidence-family integrity",
            "observed_in": [4, 5, 6],
            "problem": "The scorer accepts retired PP5/BP6, multiple strengths or aliases from the same criterion family, and opposed PP3/BP4 evidence; exact documented REVEL/BayesDel benign endpoints and semantic access dates are also validated incorrectly. PP5 and same-family duplication changed returned classifications.",
            "root_cause": "Validation is keyed to exact strings and regex shapes rather than current ClinGen criterion families, mutual-exclusion rules, inclusive threshold semantics, and typed calendar dates.",
            "fix": "Remove PP5/BP6 from accepted current criteria; define criterion families and reject multiple strengths, aliases, or opposed codes before summation; fix inclusive REVEL/BayesDel benign endpoints; parse access_date as an ISO calendar date. Add exact regressions for every observation in evidence/execution.json.",
        },
        {
            "priority": "P1",
            "title": "ACMG-002: Reject contradictory PVS1 state",
            "observed_in": [2],
            "problem": "A canonical splice fixture with is_nmd_predicted false and splice_consequence nmd silently returned PVS1 Very Strong.",
            "root_cause": "The splice branch ignores is_nmd_predicted once the consequence string is supplied and does not reconcile duplicate representations of the NMD conclusion.",
            "fix": "Use one canonical NMD field or reject contradictory fields before any strength assignment; add contradictory true/false and consequence cases plus deletion/initiation review-state regressions.",
        },
        {
            "priority": "P2",
            "title": "ACMG-001: Remove residual Brnich contradiction",
            "observed_in": [3],
            "problem": "The corrected table and code call greater than 4.3 Moderate, but failure mode 6 still says greater than 4.3 is required for Strong.",
            "root_cause": "One explanatory sentence was not updated with the repaired threshold table.",
            "fix": "Change the sentence to state that greater than 4.3 is Moderate and greater than 18.7 is Strong, then add a documentation consistency assertion.",
        },
    ],
}

(ROOT / "inputs.json").write_text(json.dumps(inputs, indent=2) + "\n", encoding="utf-8")
(ROOT / "report.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

manifest = EVIDENCE["candidate_identity_before"]
source_identity = {
    "schema": "sha256-manifest-v1",
    "skill": "bio-clinical-databases-acmg-classification",
    "origin": {
        "repository": "GPTomics/bioSkills",
        "commit": "d91ed3d563019e649dc854c56ccd62551359488a",
        "path": "clinical-databases/acmg-classification",
        "subtree": "b4c1f4dd04a6a53f3eba2aa56da5d830ba325e1a",
    },
    "candidate": {
        "path": str(CANDIDATE),
        "branch": "optimize/ten-20260928-lane3-acmg-classification",
        "product_head": "0bc0b31fc52742dbec1034f698103434cc9460c3",
        "identity": IDENTITY,
        "identity_label": "sha256-manifest-v1:" + IDENTITY,
        "manifest_bytes": manifest["manifest_bytes"],
        "file_count": manifest["file_count"],
    },
    "independence": {
        "auditor": "/root/lane3_acmg_reaudit",
        "performed_initial_audit": False,
        "performed_fix": False,
        "audit_phase": "reaudit-scientific-skill",
    },
    "environment": {
        "tool_record": r"F:\OpenScience\audit-envs\bio-clinical-databases-acmg-classification\TOOLS.md",
        "tool_record_sha256": "96651ce26387bcd9e04369b381b6dc5cafac6fa64f0ba5d8d1c43ac25ec85161",
        "fingerprint_sha256": "be04749b5d2581594940a228004479fe7c8511f371fc30b5c7dad5cf38a07cd7",
        "python": "3.12.14",
        "requests": "2.32.5",
        "isolation": "private mount namespace; lazy-unmounted /mnt/f; /mnt/openscience only; WSL_INTEROP unset",
    },
    "audited_on": "2026-09-28",
    "files": manifest["files"],
}
(ROOT / "source-identity.json").write_text(
    json.dumps(source_identity, indent=2) + "\n", encoding="utf-8"
)

execution_classifications = {
    "skill": "bio-clinical-databases-acmg-classification",
    "candidate_identity": IDENTITY,
    "surfaces": [
        {"surface": "scripts/acmg_classify.py compile/import", "classification": "EXECUTED", "status": "PASS", "evidence": "evidence/execution.json#surface_runs.compile"},
        {"surface": "tests/test_acmg_classify.py", "classification": "EXECUTED", "status": "PASS", "evidence": "evidence/unit-tests.log"},
        {"surface": "scripts/acmg_classify.py standalone demo", "classification": "EXECUTED", "status": "PASS_WITH_FINDINGS", "evidence": "evidence/standalone-demo.log"},
        {"surface": "tests/live_interface_smoke.py", "classification": "EXECUTED", "status": "PASS", "evidence": "evidence/live-interface-smoke.log"},
        {"surface": "all 15 candidate callables through independent fixtures", "classification": "EXECUTED", "status": "FAIL_WITH_REPRODUCED_FINDINGS", "evidence": "evidence/execution.json#workflows"},
        {"surface": "GeneBe public coordinate endpoint", "classification": "EXECUTED", "status": "PASS", "evidence": "evidence/execution.json#workflows.interfaces.live.genebe"},
        {"surface": "ClinGen CSpec versioned-gene endpoint", "classification": "EXECUTED", "status": "PASS", "evidence": "evidence/execution.json#workflows.interfaces.live.cspec"},
        {"surface": "InterVar 2.2+ with ANNOVAR data", "classification": "DOCUMENTED_ONLY", "status": "BLOCKED_RESTRICTED_DATA", "evidence": "TOOLS.md inventory; ANNOVAR registration and annotation data required"},
        {"surface": "AutoPVS1 external implementation", "classification": "DOCUMENTED_ONLY", "status": "UNPINNED_NO_SHIPPED_CALLABLE", "evidence": "TOOLS.md inventory"},
        {"surface": "VarSome, Franklin/Genoox, ClinGen VCI manual curation", "classification": "RESTRICTED_MANUAL", "status": "NOT_EXECUTED", "evidence": "TOOLS.md inventory"},
        {"surface": "other named evidence sources and knowledgebases", "classification": "DOCUMENTED_ONLY", "status": "NO_SHIPPED_WRAPPER", "evidence": "TOOLS.md inventory"},
    ],
}
(ROOT / "execution-classifications.json").write_text(
    json.dumps(execution_classifications, indent=2) + "\n", encoding="utf-8"
)

finding_ledger = """# Independent re-audit finding ledger

Candidate: `sha256-manifest-v1:926ce0436d0d9fd1fb73a5f2b83728adfb622cf6f8ec41c8c00ad8d8300e8c07`

| ID | Initial severity | Re-audit state | Re-audit severity | Evidence | Required disposition |
|---|---|---|---|---|---|
| ACMG-001 | P0 | reopened | P2 | `evidence/execution.json#static_checks` | Correct the residual `>4.3 for Strong` sentence; code and table otherwise pass. |
| ACMG-002 | P0 | reopened | P1 | `evidence/execution.json#workflows.pvs1.conflict` | Reject contradictory NMD fields before PVS1 strength assignment. |
| ACMG-003 | P0 | fixed | none | `evidence/execution.json#workflows.alphamissense` | Accepted: 17/17 bands, +/-3 point labels, and invalid domains pass. |
| ACMG-004 | P1 | fixed | none | `evidence/execution.json#workflows.interfaces.live.genebe` | Accepted: current coordinate contract returned one public record. |
| ACMG-005 | P1 | fixed | none | `evidence/execution.json#workflows.interfaces.live.cspec` | Accepted: current versioned-gene route returned six GATM versions. |
| ACMG-006 | P1 | reopened | P0 | `evidence/execution.json#workflows.tavtigian`, `#workflows.other_predictor_boundaries`, `#workflows.somatic.invalid_date` | Remove PP5/BP6; reject evidence-family duplicates/aliases and opposing codes; fix exact inclusive predictor endpoints; parse real dates. |
| ACMG-007 | P1 | fixed | none | `evidence/standalone-demo.log` | Accepted: one predictor, PS3 Moderate, unresolved context, uncertainty, and guard printed. |
| ACMG-008 | P1 | fixed | none | `SKILL.md`, `evidence/standalone-demo.log`, guarded result observations | Accepted: non-diagnostic boundary and qualified review are enforced in documentation/results. |
| ACMG-009 | P2 | fixed | none | `evidence/execution.json#workflows.somatic.cases` | Accepted: I-A, I-B, II-C, II-D, III, and IV are distinct and guarded. |

No new standalone ID is opened: the newly reproduced validation failures are additional manifestations of the still-open ACMG-006 evidence/domain-validation defect. Candidate readiness is rejected because ACMG-006 fires the methodological veto and the readiness floors are not met.
"""
(ROOT / "finding-ledger.md").write_text(finding_ledger, encoding="utf-8")

source_notes = """# Scientific source notes

- Brnich et al. 2020 primary open article, Table 3: <https://pmc.ncbi.nlm.nih.gov/articles/PMC6938631/>. It states `<0.053` BS3, `<0.23` moderate, `<0.48` supporting, `0.48-2.1` indeterminate, and `>2.1`, `>4.3`, `>18.7`, `>350` pathogenic Supporting through Very Strong. Candidate code and table match; one explanatory sentence does not.
- Bergquist et al. 2025, *Genetics in Medicine* 27:101402, PMID 40084623, DOI 10.1016/j.gim.2025.101402: <https://pubmed.ncbi.nlm.nih.gov/40084623/> and author-hosted paper <https://ccs.neu.edu/home/radivojac/papers/bergquist_genetmed_2025.pdf>. Candidate AlphaMissense bands and explicit -3/+3 point labels match the table.
- ClinGen SVI current guidance index (updated July 2025): <https://www.clinicalgenome.org/tools/clingen-variant-classification-guidance/>. It points to the PP5/BP6 reputable-source recommendation.
- Biesecker and Harrison 2018, ClinGen SVI, PMID 29543229: <https://pmc.ncbi.nlm.nih.gov/articles/PMC6709533/>. PP5/BP6 rely on assertions not linked to primary evidence and risk double counting; the current ClinGen VCEP SOP states they should not be applied in any context. The candidate still accepts both.
- ClinGen Variant Curation SOP v1: <https://www.clinicalgenome.org/site/assets/files/3677/clingen_variant-curation_sopv1.pdf>. The reputable-source section says PP5/BP6 should not be applied and are disabled in the VCI.
- ClinGen SVI splicing guidance: <https://pmc.ncbi.nlm.nih.gov/articles/PMC9980257/>. Canonical splice PVS1 strength depends on predicted/observed transcript consequence and review of rescue mechanisms. The new stop states pass, but contradictory NMD representations are not reconciled.
- GeneBe official API documentation: <https://docs.genebe.net/docs/api/overview/>. The current single-variant GET uses `chr`, `pos`, `ref`, `alt`, and `genome`; candidate live execution passed.
- ClinGen CSpec current read-only service was verified at <https://cspec.genome.network/cspec/srvc> and the GATM version route on 2026-09-28; candidate live execution returned six version records.

The live inputs were public documentation examples and a public gene symbol. No patient, private, authenticated, proprietary, or protected-health data was used.
"""
(ROOT / "scientific-source-notes.md").write_text(source_notes, encoding="utf-8")

viewer_lines = [
    "# Eval Viewer — bio-clinical-databases-acmg-classification",
    "",
    "Generated: 2026-09-28",
    "",
    f"Candidate: `sha256-manifest-v1:{IDENTITY}`",
    "",
    "## Decision",
    "",
    "**Rejected for candidate-ready transition.** Final diagnostic score is 76/100, but the Research Veto fails Methodological Ground. Static 76, execution 75.9, Layer 1 average 31.4/40, Layer 2 average 44.4/60, and assertions 26/35 all miss one or more production floors.",
    "",
    "## Summary table",
    "",
    "| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |",
    "|---:|---|---:|---:|---:|---:|:---:|",
]
for row in rows:
    viewer_lines.append(
        f"| {row['index']} | {row['type']} | {row['basic']} | {row['specialized']} | {row['total']} | {row['assertions_passed']}/{row['assertions_total']} | {row['status_flag']} |"
    )
viewer_lines += [
    "",
    "## Veto gates",
    "",
    "- Structural veto: PASS.",
    "- Scientific integrity: PASS.",
    "- Practice boundaries: PASS.",
    "- Methodological Ground: **FAIL** — retired evidence and evidence-family double counting can change classifications; exact documented predictor endpoints are also wrong.",
    "- Code usability: PASS.",
    "",
    "## Detailed outputs",
    "",
]
for item, row in zip(inputs, rows):
    viewer_lines += [
        f"### Input {row['index']} — {row['label']}",
        "",
        f"**Prompt:** {item['prompt']}",
        "",
        f"**Observed output:** {row['note']}",
        "",
        f"**Scores:** Basic {row['basic']}/40 | Specialized {row['specialized']}/60 | Total {row['total']}/100",
        "",
        "**Assertions:**",
        "",
    ]
    for a in row["assertions"]:
        viewer_lines.append(f"- [{a['result']}] {a['text']} — {a['note']}")
    viewer_lines += ["", "Raw observations: `evidence/execution.json`.", ""]
viewer_lines += [
    "## Open findings",
    "",
    "- P0 ACMG-006: current evidence-family and strict-validation defects remain open.",
    "- P1 ACMG-002: contradictory PVS1 NMD fields remain open.",
    "- P2 ACMG-001: one residual Brnich prose contradiction remains open.",
    "",
    "See `finding-ledger.md`, `scientific-source-notes.md`, and `execution-classifications.json` for the compact evidence map and documented-only surfaces.",
]
(ROOT / "viewer.md").write_text("\n".join(viewer_lines) + "\n", encoding="utf-8")

hash_targets = [
    "report.json", "viewer.md", "source-identity.json", "inputs.json",
    "execution-classifications.json", "finding-ledger.md", "scientific-source-notes.md",
    "scripts/run_reaudit.py", "scripts/run_isolated.sh", "scripts/build_record.py", "scripts/validate_report.py",
    "evidence/execution.json", "evidence/candidate-manifest.json",
    "evidence/unit-tests.log", "evidence/standalone-demo.log", "evidence/live-interface-smoke.log",
]
hashes = []
for relative in hash_targets:
    data = (ROOT / relative).read_bytes()
    hashes.append({"path": relative, "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()})
(ROOT / "artifact-hashes.json").write_text(json.dumps(hashes, indent=2) + "\n", encoding="utf-8")

print(json.dumps({
    "report": str(ROOT / "report.json"),
    "score": report["final"]["score"],
    "grade": report["final"]["grade"],
    "assertions": f"{passed}/{total}",
    "identity": IDENTITY,
    "open_findings": ["ACMG-001", "ACMG-002", "ACMG-006"],
}, sort_keys=True))
