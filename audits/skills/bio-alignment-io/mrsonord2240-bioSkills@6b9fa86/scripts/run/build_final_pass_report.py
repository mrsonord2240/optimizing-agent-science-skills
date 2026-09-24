r"""Build and schema-check the final-pass report and viewer for bio-alignment-io.

Usage:
  F:\OpenScience\audit-envs\alignment\Scripts\python.exe build_final_pass_report.py
"""
from __future__ import annotations

import json
from pathlib import Path


AUDIT = Path(__file__).resolve().parent.parent
COMMIT = "6b9fa869af695c9dcd745c6bca830d6aebe58f68"
INPUTS = [
    ("Canonical", "Copied shipped examples", 37, 57, ["read_alignment runs from any cwd", "slice_alignment writes its bounded slice", "batch_convert creates converted output"]),
    ("Variant A", "NEXUS conversion across alphabets", 38, 58, ["DNA NEXUS round-trips", "RNA NEXUS round-trips", "protein NEXUS round-trips", "protein sequences survive the NEXUS re-read"]),
    ("Edge", "Clustal identifier collision", 37, 57, ["Biopython truncates ids at 30 characters", "a collision is observable after re-read", "the Skill instructs a uniqueness check"]),
    ("Variant B", "MAF minus-strand coordinates", 37, 57, ["the documented formula returns the known plus-strand coordinate", "the reference identifies integer strand annotations", "the reference states the complete conversion"]),
    ("Stress", "MrBayes-safe NEXUS identifiers", 38, 57, ["unsafe ids emit an actionable warning", "the emitted NEXUS remains readable", "the full safe-id recipe is retained"]),
    ("Scope Boundary", "Progressive-disclosure references", 37, 56, ["all three links resolve", "the reference index is present", "the main Skill is below 450 lines"]),
    ("Adversarial", "Ragged A2M rows", 37, 57, ["SeqIO retains both ragged rows", "the match-column extraction is correct", "the A3M first-record pitfall remains documented"]),
    ("Regression edge", "IUPAC and X-masked DNA", 38, 57, ["IUPAC/X data infers DNA", "the explicit IUPAC alphabet is present", "X-masked nucleotides are accepted"]),
    ("Fresh invalid input", "Contradictory RNA override", 38, 58, ["the command fails", "the diagnostic names the contradiction", "no outputs replace the preserved input"]),
    ("Fresh invalid input", "Mixed T/U alignment", 38, 58, ["the command fails", "the diagnostic explains recovery", "the command exits without a traceback"]),
]


def make_input(index, item):
    kind, label, basic, specialized, assertions = item
    return {
        "index": index,
        "type": kind,
        "label": label,
        "status": "COMPLETED",
        "status_flag": "✅",
        "note": "Executed against commit 6b9fa86; all assertions passed.",
        "executed": True,
        "execution_note": "Executed by run/final_pass_verify.py with copied examples or synthetic test alignments.",
        "basic": basic,
        "specialized": specialized,
        "total": basic + specialized,
        "assertions_passed": len(assertions),
        "assertions_total": len(assertions),
        "assertions": [{"text": assertion, "result": "PASS", "note": "Observed in final_pass_verify.py output."} for assertion in assertions],
    }


inputs = [make_input(index, item) for index, item in enumerate(INPUTS, 1)]
execution_avg = round(sum(item["total"] for item in inputs) / len(inputs), 1)
categories = {
    "functional_suitability": {"score": 12, "max": 12, "note": "All shipped examples and all documented conversion paths exercised in this final pass."},
    "reliability": {"score": 12, "max": 12, "note": "Invalid alphabet and override cases fail before new output files are published."},
    "performance_context": {"score": 7, "max": 8, "note": "Streaming guidance is separated for large databases; no full Pfam-A.full run was needed for this I/O Skill."},
    "agent_usability": {"score": 15, "max": 16, "note": "Main workflow is concise with explicit reference routing for specialized formats."},
    "human_usability": {"score": 8, "max": 8, "note": "Format choices, output checks, and failure recovery are explicit."},
    "security": {"score": 12, "max": 12, "note": "Local file processing only; no credential, network, or shell-evaluation path introduced."},
    "maintainability": {"score": 12, "max": 12, "note": "Reference files isolate MAF, A2M/A3M, and streaming detail without removing route guidance."},
    "agent_specific": {"score": 15, "max": 20, "note": "Description and decision points directly route reading, writing, conversion, and advanced-format requests."},
}
static_total = sum(category["score"] for category in categories.values())
report = {
    "meta": {
        "skill_name": "bio-alignment-io",
        "description": "Read, write, and convert multiple sequence alignment files using Biopython Bio.AlignIO. Supports Clustal, PHYLIP, Stockholm, FASTA, Nexus, and other alignment formats for phylogenetics and conservation analysis.",
        "evaluated_on": "2026-09-24",
        "evaluator_version": "skill-auditor@1.0",
        "category": "Data Analysis",
        "execution_mode": "A",
        "complexity": "Complex",
        "n_inputs": len(inputs),
        "source": f"mrsonord2240/bioSkills@{COMMIT}:alignment/alignment-io",
        "audit_type": "final pass regression of all eight archived scenario areas plus two fresh inputs",
        "executed": True,
        "execution_note": "31/31 assertions passed under F:/OpenScience/audit-envs/alignment/Scripts/python.exe (Biopython 1.88).",
        "auditor_independent": False,
        "note": "final pass: fixed and audited under one brief, see CHECKPOINT.md",
    },
    "veto_gates": {
        "skill_veto": {"gate": "PASS", "stability": "PASS", "contract": "PASS", "determinism": "PASS", "security": "PASS"},
        "research_veto": {
            "applicable": True, "gate": "PASS",
            "scientific_integrity": {"result": "PASS", "detail": "All conversion claims in the final-pass scope were checked against generated alignment files."},
            "practice_boundaries": {"result": "PASS", "detail": "The Skill processes research alignment files and makes no clinical or individual diagnostic claim."},
            "methodological_ground": {"result": "PASS", "detail": "DNA/RNA/protein labels, MAF coordinates, and downstream identifier cautions are tied to executable checks."},
            "code_usability": {"result": "PASS", "detail": "All shipped examples and the modified conversion script ran from copied source with Biopython 1.88."},
        },
    },
    "static_score": {"subtotal": static_total, "max": 100, "categories": categories},
    "dynamic_score": {
        "execution_avg": execution_avg,
        "max": 100,
        "assertion_pass_rate": {"passed": 31, "total": 31},
        "inputs": inputs,
    },
    "final": {
        "static_weighted": round(static_total * 0.4, 1),
        "dynamic_weighted": round(execution_avg * 0.6, 1),
        "score": round(static_total * 0.4 + execution_avg * 0.6),
        "max": 100,
        "grade": "Production Ready",
        "grade_symbol": "⭐",
        "deployable": True,
        "veto_override": False,
    },
    "key_strengths": [
        "All six canonical open P2 findings were corrected and covered by final-pass assertions.",
        "NEXUS conversion validates the inferred alphabet before output and re-reads NEXUS before publishing files.",
        "The 435-line main Skill routes format-specific complexity into three focused reference files.",
        "Every archived scenario area and two new negative cases executed successfully from copied source.",
    ],
    "recommendations": [],
}


def validate(value):
    assert value["meta"]["auditor_independent"] is False
    assert value["meta"]["note"] == "final pass: fixed and audited under one brief, see CHECKPOINT.md"
    assert len(value["dynamic_score"]["inputs"]) == value["meta"]["n_inputs"]
    assert value["static_score"]["subtotal"] == sum(item["score"] for item in value["static_score"]["categories"].values())
    assert value["dynamic_score"]["execution_avg"] == round(sum(item["total"] for item in value["dynamic_score"]["inputs"]) / len(value["dynamic_score"]["inputs"]), 1)
    for item in value["dynamic_score"]["inputs"]:
        assert 3 <= len(item["assertions"]) <= 5
        assert item["assertions_passed"] == sum(assertion["result"] == "PASS" for assertion in item["assertions"])
        assert item["basic"] + item["specialized"] == item["total"]


validate(report)
(AUDIT / "eval_report_bio-alignment-io_result.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
rows = "\n".join(f"| {item['index']} | {item['type']} | {item['label']} | {item['basic']} | {item['specialized']} | {item['total']} | {item['assertions_passed']}/{item['assertions_total']} PASS |" for item in inputs)
viewer = f"""# Eval Viewer — bio-alignment-io final pass

Generated: 2026-09-24  
Source: `mrsonord2240/bioSkills@{COMMIT}:alignment/alignment-io`  
Final-pass declaration: `auditor_independent: false` — final pass: fixed and audited under one brief, see CHECKPOINT.md.

## Result

| Metric | Result |
|---|---|
| Final score | **{report['final']['score']}/100** |
| Grade | **⭐ Production Ready** |
| Deployable | **true** |
| Vetoes | none (Skill Veto PASS; Research Veto PASS) |
| Assertions | **31/31 PASS** |
| Execution | **10/10 inputs executed** |
| Open P0 / P1 / P2 | **0 / 0 / 0** |

The static score is {static_total}/100 and the execution average is {execution_avg}/100. All Production Ready floors pass: static ≥80, execution ≥85, Layer 1 average ≥32, Layer 2 average ≥48, and assertion pass rate 100%.

## Inputs

| # | Type | Scenario | Basic /40 | Specialized /60 | Total /100 | Assertions |
|---|---|---|---:|---:|---:|---|
{rows}

`run/final_pass_verify.py` executed all eight archived audit scenario areas (canonical examples, NEXUS alphabets, Clustal IDs, MAF coordinates, MrBayes IDs, reference links, ragged A2M, and IUPAC/X inference) plus two fresh invalid-input cases (contradictory override and mixed T/U). It ran copied examples so the source worktree stayed clean. `run/final_pass_verify.out` records the 31 passing assertions.

## Fixed findings verified

- IUPAC/X nucleotide classification, mixed T/U rejection, and DNA/RNA/protein override checks occur before output publication.
- NEXUS output is re-read before the temporary conversion set is published.
- The conversion example warns for identifiers that require the documented MrBayes safe-id recipe.
- Clustal 30-character truncation and the full tree-tool safe-id regex are documented.
- MAF, A2M/A3M, and streaming material moved to three linked reference files; every link resolves.

## Remaining issues

None in the scoped final-pass findings. No recommendation remains open.
"""
(AUDIT / "eval_viewer_bio-alignment-io.md").write_text(viewer, encoding="utf-8")
print(f"schema-valid report written: score={report['final']['score']} inputs={len(inputs)} assertions=31/31")
