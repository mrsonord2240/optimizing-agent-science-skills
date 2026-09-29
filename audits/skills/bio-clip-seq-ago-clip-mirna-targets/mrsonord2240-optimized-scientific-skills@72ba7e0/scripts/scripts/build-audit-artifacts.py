#!/usr/bin/env python3
"""Build strict v4 report and human-readable viewer from fresh audit evidence."""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EV = ROOT / "evidence"

def read(name: str) -> dict:
    return json.loads((EV / name).read_text(encoding="utf-8"))

before = read("candidate-identity-before.json")
after = read("candidate-identity-after.json")
parser = read("consensus-parser-independent.json")
float_forms = read("float-spellings-independent.json")
umi = read("umi-contract-independent.json")
hyb = read("hyb-repeatability.json")
pinned = read("hyb-pinned-manifest-check.json")
targetscan = read("targetscan-contract-independent.json")
secondary = read("secondary-routes-independent.json")

assert before["identity"] == after["identity"] == "e5366d51226e2ad2c96030cb26581bc84808194b7a17ef7bb376d337280d1b30"
assert before["file_count"] == after["file_count"] == 10
assert before["manifest_bytes"] == after["manifest_bytes"] == 989
assert parser["assertions_passed"] == 16
assert float_forms["assertions_passed"] == 27
assert umi["assertions_passed"] == 8 and umi["fail_closed"] is True
assert pinned["manifest_equal"] is True and pinned["accepted_rows"] == 111 and pinned["replicates"] == 2
assert targetscan["same_strand_only"] and targetscan["wrong_release_rejected"] and targetscan["out_of_range_rejected"]
assert secondary["assertions_passed"] == secondary["assertions_total"] == 5
assert hyb["all_nonstdout_files_byte_identical"] is True
assert hyb["repeatability_pass"] is True
assert all(row["same_after_first_timestamp_line"] and row["first_line_differs"] for row in hyb["stdout_logs"])

source_identity = {
    "skill_id": "bio-clip-seq-ago-clip-mirna-targets",
    "phase": "independent reaudit-scientific-skill",
    "origin": {
        "repository": "GPTomics/bioSkills", "commit": "d91ed3d563019e649dc854c56ccd62551359488a",
        "path": "clip-seq/ago-clip-mirna-targets", "subtree": "6326a423789826240d0840be6897ddd69b21d940",
        "checkout": "F:\\optimizing-agent-science-skills\\external\\GPTomics__bioSkills", "status": "clean",
    },
    "candidate": {
        "content_sha256": after["identity"], "identity_recipe": "sha256-manifest-v1: ordinal relative POSIX-path sort; each row is path TAB bytes TAB lowercase sha256; LF-joined without trailing LF; SHA-256 over UTF-8",
        "path": "F:\\OpenScience\\wt\\opt10-ago-clip\\skills\\bio-clip-seq-ago-clip-mirna-targets",
        "branch": "optimize/ten-20260928-lane4-ago-clip", "commit": "0bc0b31fc52742dbec1034f698103434cc9460c3",
        "status": "?? skills/bio-clip-seq-ago-clip-mirna-targets/", "identity_before": before["identity"],
        "identity_after": after["identity"], "file_count": after["file_count"], "manifest_bytes": after["manifest_bytes"],
    },
    "files": after["files"], "candidate_cache_artifacts": [],
    "independence": {"candidate_bytes_modified": False, "performed_candidate_fix": False, "performed_initial_audit": False, "performed_tooling_delta": False},
    "audit": {"verdict": "candidate-ready", "closed_findings": ["AGO-004", "AGO-005", "AGO-009"], "open_findings": [], "report": "report.json", "viewer": "viewer.md"},
    "tooling": {
        "environment_fingerprint_sha256": "fcd7556256ce1a32f3473718ad2f0fa3d1821039dc4994ecf4aa626fe97d7e5c",
        "environment_lock_sha256": "ba5f355bb2d907197f723c7424742517b0e4fb4839a4273382d2293c5b2f3340",
        "tools_md_sha256": "f94c31cfa09e69331c164602a850022d034551e7af840f5965ae181f8e0e9a3a",
        "rubric_zip_sha256": "e54e9ff8b0c3677abcfe657ad6ed92ba34dbdb8ad205c7157ad881f25afcf0de",
    },
}
(ROOT / "source-identity.json").write_text(json.dumps(source_identity, indent=2) + "\n", encoding="utf-8")

def assertion(text: str, note: str) -> dict[str, str]:
    return {"text": text, "result": "PASS", "note": note}

cases = [
    {
        "index": 1, "type": "Canonical", "label": "Fresh pinned Hyb cross-workflow repeatability",
        "basic": 39, "specialized": 58,
        "note": "Two independently staged two-replicate Hyb workflows retained 111 stable assignments each; structured products matched.",
        "assertions": [
            assertion("Two fresh workflows produce identical structured sites, targets, support, exclusions, and manifests", "All structured artifact hashes match across independent workflow roots."),
            assertion("Each underlying Hyb run has the advertised row schema and 111 assignments", "Four raw replicate files each contain 111 rows with 16 fields."),
            assertion("Each retained read has support from every replicate", "All 111 retained support rows show 2/2 and supporting indices 1,2."),
            assertion("Workflow manifests reconcile assignment and target counts", "Both manifests report 111 accepted, 0 excluded, 2 replicates, and 111 target rows."),
            assertion("Timestamped stdout differences are bounded and disclosed", "Only the first timestamp line differs; remaining stdout and all non-stdout files match."),
        ],
        "output": "Pinned Hyb commit 028ab6371ce793ca5e86f475fce1f2cc6ad3c677 ran twice from fresh output roots. Each workflow produced 111 accepted rows, 0 exclusions, 111 targets, and 2/2 support. Structured outputs and non-stdout files are identical; only stdout's first timestamp line varies.",
    },
    {
        "index": 2, "type": "Variant A", "label": "Wrapper failure and publication boundaries",
        "basic": 39, "specialized": 58,
        "note": "Fresh shipped regressions exercised literal paths, overwrite protection, failure propagation, replacement preservation, and cleanup.",
        "assertions": [
            assertion("Paths with spaces and literal wildcard characters are handled literally", "The shipped wrapper regression completed its spaced and wildcard-path fixture."),
            assertion("An existing output is protected without explicit replacement", "The repeat invocation returns status 73 and preserves the existing result."),
            assertion("A failing Hyb exit status reaches the caller", "The controlled status 42 is propagated."),
            assertion("A failed replacement preserves prior output", "The sentinel is unchanged after the forced replacement failure."),
            assertion("A failed staged run cleans its temporary stage", "The harness found no residual stage directory."),
        ],
        "output": "All seven shipped tests passed. Wrapper checks preserved existing output on failure, propagated subprocess errors, respected paths with spaces and literal wildcard characters, and removed failed stages.",
    },
    {
        "index": 3, "type": "Edge", "label": "Consensus schema, orientation, and finite expression parsing",
        "basic": 39, "specialized": 58,
        "note": "Parser normalization and the AGO-009 edge contract passed fresh finite, non-finite, malformed, missing, and threshold checks.",
        "assertions": [
            assertion("Both segment orientations normalize to the same miRNA-target contract", "Fresh orientation fixtures preserve correct IDs and coordinate fields."),
            assertion("Finite values above threshold are accepted and below-threshold values are excluded with a reason", "The 150-valued row is accepted; the 50-valued row receives below_expression_threshold at threshold 100."),
            assertion("All accepted NaN and infinity spellings fail before output publication", "Thirteen float() spellings, including signed/case variants of NaN, Inf, and Infinity, were rejected as expression values and thresholds with no result files."),
            assertion("Malformed, blank, and missing expression values fail closed", "Nonnumeric, blank, and short-row values failed with source-line diagnostics and no result files."),
            assertion("Non-finite thresholds fail before output publication", "NaN, +Inf, -Inf, Infinity, and -Infinity thresholds were rejected; no result files appeared."),
        ],
        "output": "The 16-case parser harness and 27-case expanded spelling harness passed. Finite +1.5e2/5e1 values at threshold 1e2 accepted only the above-threshold row and reason-coded the other. Thirteen Python float() spellings covering signed and case variants of NaN, Inf, and Infinity failed as both expression values and thresholds; malformed/blank/missing values also failed before result files were published.",
    },
    {
        "index": 4, "type": "Variant B", "label": "TargetScan spliced-coordinate and strand projection",
        "basic": 39, "specialized": 58,
        "note": "Fresh plus/minus exon-spanning fixtures preserved BED12 blocks and rejected release and range errors.",
        "assertions": [
            assertion("Plus- and minus-strand sites project to multi-block BED12", "Both UTR-relative fixtures produce two blocks with their original strands."),
            assertion("Split, strand-aware overlap excludes the opposite-strand peak", "Expected plus and minus overlaps remain; the wrong-strand peak is absent."),
            assertion("TargetScan release mismatch is rejected", "The version mismatch returns nonzero with a release-metadata diagnostic."),
            assertion("Out-of-range UTR sites fail closed", "The converter rejects the site rather than truncating it."),
            assertion("Manifest retains assembly and annotation provenance", "Output records GRCh38, GENCODEv49, and TargetScan 8.0."),
        ],
        "output": "Fresh exon-spanning plus/minus conversions and bedtools -split -s overlap passed; wrong-strand overlap was excluded. Release mismatch and out-of-range fixtures failed closed, and the manifest retained assembly and release fields.",
    },
    {
        "index": 5, "type": "Stress", "label": "Targeted miR-eCLIP UMI declaration and fail-closed behavior",
        "basic": 39, "specialized": 58,
        "assertions": [
            assertion("A declared 9-nt UMI extracts exactly nine R2-prefix bases", "The emitted header contains ACGTACGTA and the manifest records length 9."),
            assertion("A declared 10-nt UMI extracts exactly ten R2-prefix bases", "The emitted header contains ACGTACGTAC and the manifest records length 10."),
            assertion("Successful output binds length to library and protocol provenance", "Both manifests include library ID, protocol source, and input/output hashes."),
            assertion("Missing, zero, non-integer, or blank declarations fail without outputs", "All five declaration errors return nonzero and leave FASTQ/manifest absent."),
            assertion("R2 shorter than the declared length fails without outputs", "A 13-nt declaration against 12-nt R2 returns nonzero and publishes nothing."),
        ],
        "output": "Eight direct assertions passed: protocol-declared 9- and 10-nt extraction succeeded; absent, zero, non-integer, blank-library, blank-protocol, and too-short R2 cases failed closed. The upstream targeted-route 9-nt prose versus 10-nt default remains explicitly disclosed.",
    },
    {
        "index": 6, "type": "Scope Boundary", "label": "Unavailable biological and remote surfaces",
        "basic": 39, "specialized": 58,
        "assertions": [
            assertion("Direct chimera evidence remains distinct from computational predictions", "Method guidance labels ordinary AGO-CLIP assignments as inferred and chimera pairs as direct."),
            assertion("Human and mouse HEAP contexts are not conflated", "HEAP is kept within its Halo-Ago2 mouse model context."),
            assertion("Unrun full workflows require their real biological inputs", "Full Yeo and HEAP surfaces are recorded as unavailable without matched biological materials and references."),
            assertion("Unavailable DIANA service is reported rather than simulated as a result", "The HTTP 500 surface remains an explicit service availability limitation."),
            assertion("Synthetic evidence is not represented as biological validation", "No wet-lab or clinical conclusion is claimed by the bounded synthetic fixtures."),
        ],
        "output": "Static and route inspection preserved direct-versus-inferred evidence labels, species/model limits, and explicit unavailable states for full Yeo, HEAP wet-lab, and the failed DIANA endpoint. Bounded synthetic results are not presented as biological validation.",
    },
    {
        "index": 7, "type": "Adversarial", "label": "Secondary UMI, trimming, and soft-clip diagnostic boundaries",
        "basic": 38, "specialized": 56,
        "note": "Bounded synthetic fixtures passed and the soft-clip command remained labeled diagnostic-only.",
        "assertions": [
            assertion("The total-Yeo route extracts its documented ten-base read-1 UMI", "The fixture header contains the expected 10-nt suffix."),
            assertion("Paired adapter trimming retains the expected insert lengths", "Both trimmed reads are 20 nt after adapter removal."),
            assertion("The soft-clip diagnostic counts clipped records", "One 5M5S record is counted and the 10M control is not."),
            assertion("A soft-clip count is not represented as a chimera call", "Documentation describes it as a candidate-pool diagnostic only."),
            assertion("Synthetic checks remain distinguished from unavailable full biological workflows", "Full Yeo and wet-lab paths remain deferred with the required inputs recorded."),
        ],
        "output": "Fresh bounded route fixtures verified ten-base read-1 UMI extraction, adapter trimming to 20-nt inserts, and one soft-clipped record. The diagnostic remains diagnostic-only; complete biological pipelines remain input-deferred.",
    },
]

for case in cases:
    case["status"] = "COMPLETED"
    case["status_flag"] = "✅"
    case["total"] = case["basic"] + case["specialized"]
    case["assertions_passed"] = len(case["assertions"])
    case["assertions_total"] = len(case["assertions"])
    case["summary"] = case.pop("note", "All required bounded checks passed with inspected output.")

report_inputs = []
for case in cases:
    item = {key: value for key, value in case.items() if key not in ("output", "summary")}
    item["note"] = case["summary"]
    report_inputs.append(item)

avg = round(sum(c["total"] for c in cases) / len(cases), 1)
assertions_passed = sum(c["assertions_passed"] for c in cases)
assertions_total = sum(c["assertions_total"] for c in cases)
categories = {
    "functional_suitability": {"score": 11, "max": 12, "note": "Direct chimera, indirect assignment, coordinate projection, consensus filtering, and protocol-declared UMI routes align with their stated use; the finite-expression bypass is repaired and regression-tested."},
    "reliability": {"score": 11, "max": 12, "note": "Input checks, fail-closed validation, stable replicate consensus, atomic output publication, and useful diagnostics are present; external biological workflows still depend on matched inputs."},
    "performance_context": {"score": 8, "max": 8, "note": "Progressive references and bounded local fixtures keep routine reasoning separate from costly or unavailable biological execution."},
    "agent_usability": {"score": 15, "max": 16, "note": "Method selection, inputs, output schemas, provenance, and stop conditions are explicit; protocol-specific preprocessing still requires local protocol metadata."},
    "human_usability": {"score": 7, "max": 8, "note": "Clear workflow tables and failure guidance support review; several advanced routes require domain-specific reference preparation."},
    "security": {"score": 12, "max": 12, "note": "No credential handling or raw user-string evaluation is present; file validation and controlled atomic outputs are exercised."},
    "maintainability": {"score": 12, "max": 12, "note": "Documentation is separated into four references, scripts have focused responsibilities, and the shipped suite covers key contracts."},
    "agent_specific": {"score": 17, "max": 20, "note": "Triggering, progressive disclosure, reproducibility, and escape hatches are clear; correct biological interpretation still depends on human protocol and assay context."},
}
static = sum(value["score"] for value in categories.values())
static_weighted = round(static * 0.4, 1)
dynamic_weighted = round(avg * 0.6, 1)
score = round(static_weighted + dynamic_weighted)

report = {
    "meta": {
        "skill_name": "bio-clip-seq-ago-clip-mirna-targets",
        "description": "Identify direct miRNA-target interactions from AGO HITS-CLIP, AGO-CLEAR-CLIP (chimeric reads), HEAP (Halo-Ago2 mouse), chimeric eCLIP / miR-eCLIP (deep miRNA-target profiling), or CLASH using chimeric-read processing pipelines, seed-pairing analysis, and 3' auxiliary pairing rules. Use when distinguishing direct miRNA targets from indirect, integrating CLIP-derived target maps with TargetScan / miRDB / DIANA predictions, applying canonical 7mer-8mer seed matching with 3' UTR context, or recovering miRNA-mRNA chimeras at scale.",
        "evaluated_on": "2026-09-28", "evaluator_version": "skill-auditor@1.0", "category": "Data Analysis", "execution_mode": "D", "complexity": "Complex", "n_inputs": 7,
    },
    "veto_gates": {
        "skill_veto": {"gate": "PASS", "stability": "PASS", "contract": "PASS", "determinism": "PASS", "security": "PASS"},
        "research_veto": {
            "applicable": True, "gate": "PASS",
            "scientific_integrity": {"result": "PASS", "detail": "No unverified biological result, study size, p-value, DOI, or PMID was generated by the bounded audit fixtures; direct and inferred evidence remain labeled separately."},
            "practice_boundaries": {"result": "PASS", "detail": "The skill is a research analysis workflow and makes no patient-specific diagnostic or treatment recommendation."},
            "methodological_ground": {"result": "PASS", "detail": "Direct chimera evidence, AGO-binding evidence, and computational prediction are distinguished; species, assay, expression, and coordinate contexts are retained with explicit limitations."},
            "code_usability": {"result": "PASS", "detail": "All locally accessible shipped scripts and focused routes executed in the prepared environment; unavailable biological and remote surfaces are classified with their missing inputs or service failure."},
        },
    },
    "static_score": {"subtotal": static, "max": 100, "categories": categories},
    "dynamic_score": {"execution_avg": avg, "max": 100, "assertion_pass_rate": {"passed": assertions_passed, "total": assertions_total}, "inputs": report_inputs},
    "final": {"static_weighted": static_weighted, "dynamic_weighted": dynamic_weighted, "score": score, "max": 100, "grade": "Production Ready", "grade_symbol": "⭐", "deployable": True, "veto_override": False},
    "key_strengths": [
        "Fresh pinned Hyb workflows produced identical structured consensus outputs with per-read support for every retained assignment.",
        "Expression parsing rejects non-finite and malformed inputs before publishing outputs while reason-coding finite below-threshold exclusions.",
        "The Skill separates direct chimera evidence from inferred assignments and preserves coordinate, protocol, and provenance contracts.",
    ],
    "recommendations": [],
}

(ROOT / "report.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

lines = [
    "# Eval Viewer — AGO-CLIP and miRNA Target Identification", "", "Generated: 2026-09-28",
    "", "## Summary Table", "", "| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |", "|---|---|---:|---:|---:|---:|---|",
]
for case in cases:
    lines.append(f"| {case['index']} | {case['type']} | {case['basic']} | {case['specialized']} | {case['total']} | {case['assertions_passed']}/{case['assertions_total']} PASS | {case['status_flag']} |")
lines += ["", f"**Execution Average:** {avg} / 100", f"**Assertion Pass Rate:** {assertions_passed}/{assertions_total} ({assertions_passed / assertions_total:.1%})", "**Research veto:** PASS", "**Final score:** " + str(score) + " / 100 — ⭐ Production Ready", "**Candidate identity:** `sha256-manifest-v1 e5366d51226e2ad2c96030cb26581bc84808194b7a17ef7bb376d337280d1b30` (10 files; 989-byte manifest).", "", "## Detailed Outputs", ""]
for case in cases:
    lines += [f"### Input {case['index']} — {case['type']}: {case['label']}", "", f"**Outcome:** {case['output']}", f"**Scores:** Basic {case['basic']}/40 | Specialized {case['specialized']}/60 | Total {case['total']}/100", "**Assertions:**"]
    for item in case["assertions"]:
        lines.append(f"- [PASS] {item['text']} — {item['note']}")
    lines.append("")
lines += ["## Prior Finding Reconciliation", "", "- **AGO-004 (P0):** Rechecked with two new pinned Hyb workflows. Structured outputs and all non-stdout files match; stdout differs only in its first timestamp line.", "- **AGO-005 (P1):** Rechecked explicit targeted UMI lengths and invalid declarations. The upstream 9-nt prose versus 10-nt executable default remains disclosed; the local extractor requires protocol declaration.", "- **AGO-009 (P0):** Rechecked finite acceptance, below-threshold exclusion, NaN/infinity spellings, malformed/missing values, non-finite thresholds, and absent result files after invalid inputs. All checks pass.", "", "## Deferred Surfaces", "", "Full Yeo and HEAP biological runs remain input-deferred; the DIANA example endpoint returned HTTP 500. These surfaces were not claimed as executed. See `evidence/deferred-limitations.md` and `TOOLS.md`.", ""]
(ROOT / "viewer.md").write_text("\n".join(lines), encoding="utf-8")
print(json.dumps({"static": static, "execution_average": avg, "assertions": [assertions_passed, assertions_total], "score": score, "candidate": after["identity"]}, indent=2))
