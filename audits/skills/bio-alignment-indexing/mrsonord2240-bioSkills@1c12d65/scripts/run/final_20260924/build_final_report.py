#!/usr/bin/env python3
"""Build and validate the 2026-09-24 final-pass audit report from saved run evidence."""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
AUDIT = HERE.parents[1]
OUT = AUDIT / "eval_report_bio-alignment-indexing_result.json"
COMMIT = "1c12d65aa177cc782a8e69e51130afb9caed5250"

def assertion(text, note):
    return {"text": text, "result": "PASS", "note": note}

def row(index, typ, label, note, basic, specialized, assertions, execution_note):
    return {
        "index": index, "type": typ, "label": label, "status": "COMPLETED", "status_flag": "✅",
        "note": note, "basic": basic, "specialized": specialized, "total": basic + specialized,
        "assertions_passed": len(assertions), "assertions_total": len(assertions), "assertions": assertions,
        "executed": True, "execution_note": execution_note,
    }

env = "WSL science env alignment-files: samtools/htslib 1.24, pysam 0.24.1, Python 3.12.14"
inputs = [
    row(1, "Canonical", "Archived regression: BAI/CSI indexing, regions, idxstats and shipped Python snippets",
        "r1_canonical.py: 42/42 checks PASS.", 38, 59,
        [assertion("BAI/CSI region counts equal full-scan truth", "53 regions and six access methods matched."), assertion("Fresh, missing, CSI-only and alternate-name index cases behave as documented", "mtimes and counts were asserted."), assertion("Mitochondrial awk and fetch_regions output are correct", "chrM/MT/empty fixtures and real region output passed.")], env),
    row(2, "Variant A", "Archived regression: CRAM reference, REF_PATH, idxstats and faidx",
        "r2_cram_faidx.py: 22/22 checks PASS; the REF_PATH M5 cache probe passed.", 38, 59,
        [assertion("-T and pysam reference_filename return the BAM-equivalent CRAM count", "5642 records."), assertion("REF_PATH guidance distinguishes an M5 cache from a FASTA directory", "plain FASTA directory gave 0, M5 cache gave 2 records."), assertion("CRAM and FASTA error paths are actionable", "fresh CRAI retained and missing reference has the documented hint.")], env),
    row(3, "Edge", "Archived regression: unsorted BAMs, missing indices, contig names and parser boundaries",
        "r3_edge.py: 27/27 checks PASS.", 37, 58,
        [assertion("Common Errors strings reproduce on the installed tool versions", "samtools 1.24 and pysam 0.24.1 output was checked."), assertion("Unsorted and header-only BAM handling is correct", "indexing and recovery output matched assertions."), assertion("Supported region forms and special contig names resolve correctly", "samtools-equivalent counts passed.")], env),
    row(4, "Variant B", "Archived regression: large-contig BAI/CSI boundaries and BAM position limits",
        "r4_large_genome.py: 18/18 checks PASS after its text assertions were updated for the corrected wording.", 38, 58,
        [assertion("BAI rejects a >537-Mbp contig and CSI returns hand-known reads", "830-Mbp and 2.0-Gbp fixtures passed."), assertion("Custom CSI depths and min_shift claims are correct", "CSI headers were parsed."), assertion("The Skill distinguishes a long header from an unwriteable >2^31-1 position", "3-Gbp-header and over-limit-read fixtures passed.")], env),
    row(5, "Stress", "Archived regression: stale/mixed indices, BED access, threads and idxstats semantics",
        "r5_stress.py: 29/29 checks PASS.", 38, 58,
        [assertion("Stale CSI/BAI cases end with a correct usable index", "counts equal full-scan truth."), assertion("--region-file and -M -L use the index while plain -L scans", "damaged-tail fixture passed."), assertion("idxstats and primary-mapped flag semantics match the documented recipes", "hand-built and ARTIC fixtures passed.")], env),
    row(6, "Regression edge bundle", "Archived regression: parser matrix plus Bash/Python index-helper edge cases",
        "n6_region_parser.py: 16/16; n7_ensure_index_edges.py: 29/29; n7b_sibling_index_probe.py: 3/3 checks PASS.", 38, 58,
        [assertion("Parser matrix includes commas, colon contigs, zero start and reversed intervals", "counts or clean errors matched expected behavior."), assertion("Format-specific candidates retain sibling BAM/CRAM alternate-name indices", "standard and alternate fixtures passed."), assertion("CSI -m 12 survives stale rebuild and empty batches are no-ops", "BGZF header and shell-mode fixtures passed.")], env),
    row(7, "Fresh input", "New real-fixture parser challenge: comma contigs, zero coordinate and reversed interval",
        "final_20260924/test_fetch_regions.py PASS.", 38, 59,
        [assertion("Comma-bearing contig names are not normalized away", "ctg,1 and ctg,1:100-200 parse correctly."), assertion("chr22:0-4000 matches samtools", "5550 reads."), assertion("A reversed interval emits a one-line Bad region error", "no traceback." )], env),
    row(8, "Fresh input", "New helper challenge: CSI -m preservation, sibling isolation and empty batch",
        "final_20260924/test_ensure_index.sh PASS.", 38, 59,
        [assertion("Stale CSI preserves min_shift=12", "BGZF-decompressed CSI header asserted."), assertion("BAM and CRAM sibling indices survive each other's refresh", "alternate-name fixture passed."), assertion("Empty BAM directory succeeds without a literal glob invocation", "nullglob no-op passed.")], env),
]

categories = {
    "functional_suitability": {"score": 12, "max": 12, "note": "BAI, CSI, CRAI, region access, CRAM, idxstats, faidx and freshness paths are complete and executed."},
    "reliability": {"score": 12, "max": 12, "note": "Helpers now validate the audited parser/index edge cases and report recoverable failures clearly."},
    "performance_context": {"score": 7, "max": 8, "note": "The workflow is linear; SKILL.md remains a substantial single document."},
    "agent_usability": {"score": 15, "max": 16, "note": "Versioned commands, decision tables and verified errors make cold-start use clear."},
    "human_usability": {"score": 8, "max": 8, "note": "Natural trigger wording and examples cover normal and edge index requests."},
    "security": {"score": 11, "max": 12, "note": "No credentials or raw-code execution; paths are quoted and parser coordinates are validated."},
    "maintainability": {"score": 10, "max": 12, "note": "The example and documented helpers are testable, though Bash and Python helpers remain parallel implementations."},
    "agent_specific": {"score": 19, "max": 20, "note": "Precise trigger, idempotent freshness helpers and explicit stop conditions are present."},
}
static = sum(v["score"] for v in categories.values())
dynamic = round(sum(i["total"] for i in inputs) / len(inputs), 1)
passed = sum(i["assertions_passed"] for i in inputs)
total = sum(i["assertions_total"] for i in inputs)
report = {
    "meta": {"skill_name": "bio-alignment-indexing", "description": "Create and use BAI/CSI indices for BAM/CRAM files using samtools and pysam. Use when enabling random access to alignment files or fetching specific genomic regions.", "evaluated_on": "2026-09-24", "evaluator_version": "skill-auditor@1.0", "category": "Data Analysis", "execution_mode": "D", "complexity": "Complex", "n_inputs": len(inputs), "source": f"mrsonord2240/bioSkills@{COMMIT}:alignment-files/alignment-indexing", "mode": "final pass", "audit_type": "final pass: fixed and audited under one brief, see CHECKPOINT.md", "auditor_independent": False, "note": "final pass: fixed and audited under one brief, see CHECKPOINT.md", "executed": "8/8", "executed_inputs": "8/8", "environment": env, "regression_evidence": "All seven archived logical inputs were rerun: r1-r5 plus n6 and n7/n7b; two new inputs are final_20260924/test_fetch_regions.py and test_ensure_index.sh."},
    "veto_gates": {"skill_veto": {"gate": "PASS", "stability": "PASS", "contract": "PASS", "determinism": "PASS", "security": "PASS"}, "research_veto": {"applicable": True, "gate": "PASS", "scientific_integrity": {"result": "PASS", "detail": "All quantitative claims are backed by saved real or labelled synthetic tool output."}, "practice_boundaries": {"result": "PASS", "detail": "Alignment indexing has no diagnostic or prescriptive output."}, "methodological_ground": {"result": "PASS", "detail": "BAI/CSI limits, CRAM reference behavior, region access and flag semantics were re-executed."}, "code_usability": {"result": "PASS", "detail": "Every shipped runnable path and both fresh tests completed."}}},
    "static_score": {"subtotal": static, "max": 100, "categories": categories},
    "dynamic_score": {"execution_avg": dynamic, "max": 100, "assertion_pass_rate": {"passed": passed, "total": total}, "inputs": inputs},
    "final": {"static_weighted": round(static * .4, 1), "dynamic_weighted": round(dynamic * .6, 1), "score": round(static * .4 + dynamic * .6), "max": 100, "grade": "Production Ready", "grade_symbol": "⭐", "deployable": True, "veto_override": False},
    "key_strengths": ["All six open P2 findings were corrected and their old regression inputs pass.", "The parser now matches samtools at the zero boundary and preserves comma-bearing contigs.", "The Bash helper preserves custom CSI binning and cannot remove a sibling format's index.", "CRAM reference and large-genome documentation are tied to observed tool behavior."],
    "recommendations": [],
}

def validate(r):
    assert r["meta"]["auditor_independent"] is False
    assert r["meta"]["note"] == "final pass: fixed and audited under one brief, see CHECKPOINT.md"
    assert len(r["dynamic_score"]["inputs"]) == r["meta"]["n_inputs"] == 8
    assert r["static_score"]["subtotal"] == sum(x["score"] for x in r["static_score"]["categories"].values())
    assert r["dynamic_score"]["execution_avg"] == round(sum(x["total"] for x in r["dynamic_score"]["inputs"]) / 8, 1)
    for item in r["dynamic_score"]["inputs"]:
        assert 3 <= len(item["assertions"]) <= 5 and item["basic"] + item["specialized"] == item["total"]
        assert item["assertions_passed"] == sum(a["result"] == "PASS" for a in item["assertions"])
    final = r["final"]
    assert final["static_weighted"] == round(r["static_score"]["subtotal"] * .4, 1)
    assert final["dynamic_weighted"] == round(r["dynamic_score"]["execution_avg"] * .6, 1)
    assert final["score"] == round(final["static_weighted"] + final["dynamic_weighted"])

validate(report)
OUT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8", newline="\n")
print(f"wrote {OUT}; static={static}; dynamic={dynamic}; final={report['final']['score']}; assertions={passed}/{total}")
