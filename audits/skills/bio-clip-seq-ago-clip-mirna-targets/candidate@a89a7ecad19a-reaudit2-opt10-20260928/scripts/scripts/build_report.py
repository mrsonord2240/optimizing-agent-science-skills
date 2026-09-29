#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def assertion(text: str, passed: bool, note: str) -> dict[str, str]:
    return {"text": text, "result": "PASS" if passed else "FAIL", "note": note}


cases = [
    {
        "index": 1, "type": "Canonical", "label": "Pinned Hyb workflow-level repeatability",
        "status": "COMPLETED", "status_flag": "✅", "basic": 39, "specialized": 58,
        "note": "Two independent complete two-replicate workflows on official Hyb test reads each retained 111 assignments; raw and structured results matched across workflows.",
        "output": "Pair A and Pair B each produced four total underlying single-thread Hyb runs across the two workflows: each raw file had 111 rows and 16 fields. Both manifests reported 111 accepted, 0 excluded, and two replicates. The five structured files and all non-stdout files were byte-identical; each stdout log differed only in its first wall-clock timestamp line. All 111 support rows recorded 2/2 runs, indices 1,2, accepted=true.",
        "assertions": [
            assertion("Both fresh workflow pairs produce identical sites, targets, support, exclusions, and manifest bytes", True, "All five structured output SHA-256 values matched across the two separately published workflows."),
            assertion("Every raw Hyb run contains 111 rows with the expected 16-field schema", True, "Four raw outputs were inspected; all had 111 rows and only 16-field rows."),
            assertion("Every accepted read has identical assignment support in both replicates", True, "All 111 support records show two of two runs, supporting indices 1,2, and accepted=true."),
            assertion("Manifest counts reconcile with emitted sites and targets", True, "Each manifest reports 111 accepted, 0 excluded, two replicates, and 111 target rows."),
            assertion("The reproducibility comparison accounts for timestamped stdout", True, "Stdout is intentionally not byte-identical: only its first wall-clock timestamp line differs; subsequent lines match."),
        ],
    },
    {
        "index": 2, "type": "Variant A", "label": "Wrapper path, failure, and publication boundaries",
        "status": "COMPLETED", "status_flag": "✅", "basic": 39, "specialized": 58,
        "note": "The independent wrapper harness passed literal-path handling, overwrite refusal, error propagation, replacement preservation, and stage cleanup.",
        "output": "The wrapper completed with a path containing spaces and a literal wildcard; refused an existing output with status 73; propagated a controlled Hyb status 42; preserved the old sentinel on failed replacement; and left no stage residue.",
        "assertions": [
            assertion("Paths containing spaces and literal wildcard characters remain literal", True, "The wrapper completed with the spaced and literal-star input/tool/output paths."),
            assertion("Existing results are protected without an explicit replace option", True, "The second run returned 73 and preserved the completed result."),
            assertion("A failing Hyb status is propagated to the caller", True, "The controlled subprocess status 42 was returned."),
            assertion("A failed replacement preserves the prior final output", True, "The sentinel remained unchanged after the failed replacement attempt."),
            assertion("Failed runs clean the staging directory", True, "No matching temporary stage directory remained."),
        ],
    },
    {
        "index": 3, "type": "Edge", "label": "Consensus parser orientation and input contracts",
        "status": "COMPLETED", "status_flag": "✅", "basic": 39, "specialized": 58,
        "note": "Synthetic parser fixtures and strict failure controls passed; the separately tested NaN expression case is reported in Input 6.",
        "output": "The parser preserved both 16-column orientations, expression provenance, structured aggregation and distinct missing/unstable reason codes. Malformed Hyb rows and a malformed expression header failed closed. The 9 independent control assertions passed.",
        "assertions": [
            assertion("Both segment orientations normalize to the correct miRNA and target fields", True, "Mirna-first and target-first fixtures produced the expected normalized fields."),
            assertion("Expression values, units, and source are retained in accepted rows", True, "The 150 TPM fixture and matched-small-RNA source were preserved."),
            assertion("Missing and discordant replicate assignments receive distinct reasons", True, "The parser emitted missing_from_replicate and unstable_assignment separately."),
            assertion("Malformed Hyb field count fails before valid output publication", True, "A three-field row failed with an expected-16 diagnostic."),
            assertion("Malformed expression header fails closed", True, "The reduced header was rejected before a result was emitted."),
        ],
    },
    {
        "index": 4, "type": "Variant B", "label": "TargetScan spliced-coordinate projection",
        "status": "COMPLETED", "status_flag": "✅", "basic": 39, "specialized": 58,
        "note": "Plus/minus exon-spanning fixtures projected to BED12, and strand-aware overlap and release/range guards behaved as documented.",
        "output": "The plus-strand site projected to chr1:107-204 as two BED12 blocks; the minus-strand site projected to chr2:306-403 as two blocks. bedtools intersect -split -s retained the two matching-strand peaks. Release mismatch and out-of-range cases failed closed.",
        "assertions": [
            assertion("UTR-relative plus and minus sites project to multi-block BED12", True, "Both one-based inclusive spliced sites became two-block genomic BED12 rows."),
            assertion("Strand-aware block overlap excludes the opposite-strand peak", True, "The plus-good and minus-good peaks overlapped; plus-wrong-strand did not."),
            assertion("A TargetScan release mismatch is rejected", True, "The converter returned nonzero with a release-metadata diagnostic."),
            assertion("A site outside its mapped UTR fails closed", True, "The converter returned nonzero rather than truncating the input site."),
            assertion("Output manifest preserves assembly and annotation release", True, "Manifest identifies GRCh38, GENCODEv49, and TargetScan 8.0."),
        ],
    },
    {
        "index": 5, "type": "Stress", "label": "Targeted-Yeo protocol-declared UMI contract",
        "status": "COMPLETED", "status_flag": "✅", "basic": 39, "specialized": 58,
        "note": "Independent synthetic FASTQ fixtures confirmed explicit 9- and 10-nt extraction and rejected omitted, invalid, blank, and too-long declarations without outputs.",
        "output": "The local targeted extractor emitted exactly the declared 9-nt and 10-nt R2 prefixes and bound each to library/protocol metadata and input/output hashes. Missing length, zero, non-integer, blank library, blank protocol, and too-short R2 each failed closed with no output files (8/8 assertions).",
        "assertions": [
            assertion("A declared 9-nt UMI extracts exactly nine R2-prefix bases", True, "The result header contained ACGTACGTA."),
            assertion("A declared 10-nt UMI extracts exactly ten R2-prefix bases", True, "The result header contained ACGTACGTAC."),
            assertion("The manifest binds the explicit length to library and protocol provenance", True, "Both success manifests recorded length, library id, protocol source, and hashes."),
            assertion("An omitted or invalid UMI declaration is rejected without outputs", True, "Missing, zero, non-integer, blank-library, and blank-protocol cases returned nonzero and left no outputs."),
            assertion("R2 shorter than the declared UMI fails closed", True, "The 13-nt request against a 12-nt R2 failed without output files."),
        ],
    },
    {
        "index": 6, "type": "Edge", "label": "Non-finite matched-expression threshold input",
        "status": "COMPLETED", "status_flag": "⚠️", "basic": 26, "specialized": 38,
        "note": "A bounded parser fixture with expression_value=NaN and threshold 100 returned a complete result and accepted the read, bypassing the expression gate.",
        "output": "With two identical valid Hyb rows and expression_value=NaN at a required threshold of 100, the command exited 0, accepted one consensus row, and published expression_value=nan in sites.tsv. Python float accepts NaN, and the current comparison `nan < 100` is false.",
        "assertions": [
            assertion("The parser rejects non-finite expression measurements", False, "A NaN expression value was accepted and published."),
            assertion("A value that cannot satisfy a threshold of 100 is not accepted", False, "The NaN row passed the 100 threshold and appeared in accepted sites."),
            assertion("The result retains the supplied expression provenance", True, "The emitted row retained the value, TPM unit, and matched-small-RNA source."),
            assertion("The manifest and structured outputs reconcile for the observed behavior", True, "The complete manifest reported one accepted row, matching sites.tsv."),
            assertion("The fixture remains within the documented computational-assignment scope", True, "The test uses only bounded synthetic Hyb and expression inputs."),
        ],
    },
    {
        "index": 7, "type": "Stress", "label": "Total-Yeo UMI, paired trimming, and soft-clip diagnostic",
        "status": "COMPLETED", "status_flag": "✅", "basic": 38, "specialized": 56,
        "note": "Bounded synthetic tests confirmed the documented ten-base read-1 UMI route, paired adapter trimming, and a diagnostic-only soft-clip count.",
        "output": "UMI-tools appended the ten-base read-1 prefix, cutadapt removed the fixture adapters while retaining 20-nt paired reads, and the samtools/awk diagnostic counted one 5M5S record while excluding a 10M control. These are synthetic route checks, not a full biological Yeo workflow or peak caller.",
        "assertions": [
            assertion("The total-Yeo route extracts the documented ten-base read-1 UMI", True, "UMI-tools added the expected 10-nt prefix to the read identifier."),
            assertion("Paired adapter trimming retains the expected fixture inserts", True, "Both trimmed reads had length 20 after adapter removal."),
            assertion("The soft-clip diagnostic counts clipped alignments correctly", True, "One 5M5S record was counted and the 10M record was not."),
            assertion("The diagnostic is not described as a chimera call", True, "Candidate documentation labels it as a candidate-pool diagnostic only."),
            assertion("Synthetic checks remain distinguished from unavailable biological workflows", True, "The full Yeo and wet-lab HEAP paths remain explicitly deferred."),
        ],
    },
]

for case in cases:
    case["total"] = case["basic"] + case["specialized"]
    case["assertions_passed"] = sum(item["result"] == "PASS" for item in case["assertions"])
    case["assertions_total"] = len(case["assertions"])
    case["status_flag"] = "⚠️" if case["total"] < 75 else case["status_flag"]

static_categories = {
    "functional_suitability": {"score": 10, "max": 12, "note": "The core direct-chimera, indirect-assignment, coordinate, and explicit UMI workflows are implemented; non-finite expression values bypass the optional expression threshold."},
    "reliability": {"score": 10, "max": 12, "note": "Strong validation, atomic publication, failure propagation, consensus support, and reproducibility controls are shipped; expression-value validation has a reproducible edge defect."},
    "performance_context": {"score": 8, "max": 8, "note": "Progressive disclosure and scoped workflow routing avoid unnecessary full-pipeline execution."},
    "agent_usability": {"score": 15, "max": 16, "note": "Method branches, required provenance, output schemas, and stop conditions are explicit; finite expression requirements are not enforced."},
    "human_usability": {"score": 7, "max": 8, "note": "Trigger language and workflow interpretation are clear, with a remaining edge in expression filtering."},
    "security": {"score": 12, "max": 12, "note": "No secrets or arbitrary code execution paths found; paths and output replacement are validated and controlled."},
    "maintainability": {"score": 12, "max": 12, "note": "Documentation, scripts, and regression tests are modular and traceable to pinned sources."},
    "agent_specific": {"score": 17, "max": 20, "note": "Clear routing and auditable output contracts; several biological and remote surfaces still depend on external inputs or service availability."},
}
static_subtotal = sum(item["score"] for item in static_categories.values())
execution_avg = round(sum(case["total"] for case in cases) / len(cases), 1)
assertion_passed = sum(case["assertions_passed"] for case in cases)
assertion_total = sum(case["assertions_total"] for case in cases)
static_weighted = round(static_subtotal * 0.4, 1)
dynamic_weighted = round(execution_avg * 0.6, 1)
final_score = round(static_weighted + dynamic_weighted)

report = {
    "meta": {
        "skill_name": "bio-clip-seq-ago-clip-mirna-targets",
        "description": "Identify direct miRNA-target interactions from AGO HITS-CLIP, AGO-CLEAR-CLIP, HEAP, chimeric eCLIP / miR-eCLIP, or CLASH, and reconcile direct chimeras with computational predictions.",
        "evaluated_on": "2026-09-28", "evaluator_version": "skill-auditor@1.0",
        "category": "Data Analysis", "execution_mode": "D", "complexity": "Moderate", "n_inputs": len(cases),
    },
    "veto_gates": {
        "skill_veto": {"gate": "PASS", "stability": "PASS", "contract": "PASS", "determinism": "PASS", "security": "PASS"},
        "research_veto": {
            "applicable": True, "gate": "FAIL",
            "scientific_integrity": {"result": "PASS", "detail": "No DOI, PMID, biological result, study size, p-value, or execution state was fabricated in the evaluated outputs."},
            "practice_boundaries": {"result": "PASS", "detail": "The skill remains a research-analysis workflow and provides no patient-specific diagnosis or treatment recommendation."},
            "methodological_ground": {"result": "FAIL", "detail": "The expression filter accepts non-finite NaN as a valid expression measurement; under a threshold of 100, the comparison evaluates false and admits that read into the direct-target result."},
            "code_usability": {"result": "PASS", "detail": "All shipped scripts and tested accessible commands executed in the prepared environment; the defect is incorrect input acceptance rather than inability to run."},
        },
    },
    "static_score": {"subtotal": static_subtotal, "max": 100, "categories": static_categories},
    "dynamic_score": {
        "execution_avg": execution_avg, "max": 100,
        "assertion_pass_rate": {"passed": assertion_passed, "total": assertion_total},
        "inputs": [{key: value for key, value in case.items() if key != "output"} for case in cases],
    },
    "final": {"static_weighted": static_weighted, "dynamic_weighted": dynamic_weighted, "score": final_score, "max": 100, "grade": "Reject", "grade_symbol": "❌", "deployable": False, "veto_override": True},
    "key_strengths": [
        "Fresh pinned Hyb reruns produced identical cross-workflow assignments, structured outputs, and manifests.",
        "The wrapper and parser preserve atomic publication, explicit error handling, schema validation, and per-read support evidence.",
        "TargetScan spliced-coordinate projection, strand-aware overlap, and protocol-declared targeted UMI extraction passed focused execution checks.",
    ],
    "recommendations": [
        {
            "priority": "P0", "title": "Reject non-finite expression values before thresholding", "observed_in": [6],
            "problem": "A matched-expression row with `expression_value=NaN` is converted by `float()` and accepted at a threshold of 100 because NaN compares false to `< 100`. The generated direct-target table therefore includes a read whose expression does not meet a numeric threshold.",
            "root_cause": "The expression parser validates float syntax but does not require a finite value before the threshold comparison.",
            "fix": "Require `math.isfinite(expression_value)` before storing each expression row and fail closed with the line number and field name. Add NaN, positive infinity, and negative infinity regression cases, and verify that no consensus result is published for those inputs.",
        }
    ],
}

(ROOT / "report.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

viewer = [
    "# Eval Viewer — bio-clip-seq-ago-clip-mirna-targets",
    "",
    "Generated: 2026-09-28",
    "",
    "## Summary Table",
    "",
    "| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |",
    "|---|---|---:|---:|---:|---:|---|",
]
for case in cases:
    viewer.append(f"| {case['index']} | {case['type']} | {case['basic']} | {case['specialized']} | {case['total']} | {case['assertions_passed']}/{case['assertions_total']} PASS | {case['status_flag']} |")
viewer.extend(["", f"**Execution Average:** {execution_avg} / 100", f"**Assertion Pass Rate:** {assertion_passed}/{assertion_total} ({assertion_passed / assertion_total * 100:.1f}%)", "", "## Detailed Outputs", ""])
for case in cases:
    viewer.extend([f"### Input {case['index']} — {case['type']}", "", f"**Label:** {case['label']}", f"**Status:** {case['status']} — {case['note']}", f"**Observed output:** {case['output']}", f"**Scores:** Basic {case['basic']}/40 | Specialized {case['specialized']}/60 | Total {case['total']}/100", "**Assertions:**"])
    for item in case["assertions"]:
        viewer.append(f"- [{item['result']}] {item['text']} — {item['note']}")
    viewer.append("")
viewer.extend([
    "## Veto and Readiness",
    "",
    "- Skill veto: PASS (stability, contract, determinism, and security PASS).",
    "- Research veto: FAIL on methodological ground because NaN expression values bypass the required threshold.",
    "- Numeric final score: 92/100 after schema rounding; veto override forces grade Reject and deployable=false.",
    "- Open finding: AGO-009 P0. AGO-004 and AGO-005 are closed on this exact candidate identity.",
    "",
    "## Unexecuted and Deferred Surfaces",
    "",
    "- Full Yeo chimeric-eCLIP requires real biological reads and species-matched repeat/genome STAR indices.",
    "- HEAP reproduction requires Halo-Ago2 experimental material and wet-lab execution.",
    "- The documented DIANA microT-CDS example endpoint was previously unavailable (HTTP 500); no service recovery was assumed.",
    "- AGO peak calling is not bundled; the soft-clip count is only a diagnostic, as the Skill states.",
    "",
])
(ROOT / "viewer.md").write_text("\n".join(viewer), encoding="utf-8")

print(json.dumps({"report": str(ROOT / "report.json"), "viewer": str(ROOT / "viewer.md"), "static_subtotal": static_subtotal, "execution_avg": execution_avg, "assertions": {"passed": assertion_passed, "total": assertion_total}, "score": final_score, "grade": report["final"]["grade"], "research_veto": report["veto_gates"]["research_veto"]["gate"]}, indent=2))
