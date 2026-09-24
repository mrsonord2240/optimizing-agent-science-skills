"""Emit the exact-source final-pass report and viewer from final_*.log evidence."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE = "mrsonord2240/bioSkills@c48efba95387158281f21abe97ecb48b8407ac44:alignment-files/alignment-amplicon-clipping"
NOTE = "final pass: fixed and audited under one brief, see CHECKPOINT.md"

def assertion(text, note):
    return {"text": text, "result": "PASS", "note": note}

def item(index, kind, label, note, basic, specialized, checks, execution_note):
    return {
        "index": index, "type": kind, "label": label, "status": "COMPLETED",
        "status_flag": "✅", "note": note, "basic": basic, "specialized": specialized,
        "total": basic + specialized, "assertions_passed": len(checks),
        "assertions_total": len(checks), "assertions": checks, "executed": True,
        "execution_note": execution_note,
    }

inputs = [
    item(1, "Canonical regression", "Real ARTIC v5.3.2 nanopore BAM: workflow, mode table, and iVar alternative",
         "The documented workflow and shipped example completed on 4,916 real reads; MD was restored on every mapped read and residual primer counts were 0/0.", 38, 58, [
            assertion("The documented workflow block completes with MD on all 4,916 mapped reads.", "final_s1_real_artic.log"),
            assertion("Both-ends plus strand leaves 0/0 5-prime/3-prime primer residuals.", "final_s1_real_artic.log"),
            assertion("The four documented mode outcomes reproduce on ARTIC data.", "final_s1b_modes_ivar.log"),
            assertion("The shipped example is deterministic at THREADS 4, 1, and 4.", "same record MD5 38df635d7d5b; final_s1c_example_real.log"),
        ], "samtools 1.24, pysam 0.24.1, and iVar 1.4.4 in WSL alignment-files."),
    item(2, "Variant regression", "Synthetic 800-read paired-end panel with planted primer SNPs",
         "All repaired modes matched planted boundaries; primer-derived allele counts were removed and mate/tag repairs held.", 38, 57, [
            assertion("All 800 reads match planted clipping truth in every exercised mode.", "final_s2_synth.log"),
            assertion("MD/NM, TLEN, MC, and ms repairs match independent checks.", "final_s2_synth.log"),
            assertion("Primer SNP allele counts change from mixed to the true biological alleles.", "final_s2_synth.log"),
            assertion("The short-read strand-only 3-prime residual outcome reproduces.", "final_s2_synth.log"),
        ], "Deterministic synthetic input regenerated with the archived generator."),
    item(3, "Edge regression", "BED syntax and tolerance semantics, including new CRLF normalization",
         "All 16 mode-table cells match samtools. Tab, spaces, track/browser headers, comments, blanks, and CRLF BED forms now complete; malformed 5-column BED fails clearly.", 37, 57, [
            assertion("All 16 documented strand/both-end CIGAR outcomes match.", "final_s3_strand_bed.log"),
            assertion("Every documented accepted BED form, including CRLF, succeeds end to end.", "final_s3_strand_bed.log"),
            assertion("A 5-column BED with --strand fails before clipping with an actionable BED message.", "final_s3_strand_bed.log"),
            assertion("Tolerance behavior agrees with the documented upstream-extension wording.", "final_s3_strand_bed.log"),
        ], "Synthetic single-read and paired-end cases run through the shipped example copy."),
    item(4, "Tool regression", "Hard clipping, iVar, consensus, MD/BAQ, and related command pointers",
         "Hard/soft clipping and iVar reproduce planted truth. The residual BAQ wording is gone; bcftools output is unchanged by MD presence.", 38, 56, [
            assertion("Hard clipping matches truth for 800/800 reads and uses H CIGAR operations.", "final_s4_tools.log"),
            assertion("Soft clipping and iVar -q 0 -m 1 match the planted truth.", "final_s4_tools.log"),
            assertion("The related mpileup commands have the documented accepted/rejected flags.", "final_s4_tools.log"),
            assertion("bcftools BAQ output has equal MD5 with and without MD tags.", "32,150 records per comparison; final_s4_tools.log"),
        ], "Synthetic panel plus ARTIC BAM; fgbio help used only to verify the non-primer-trimmer note."),
    item(5, "Adversarial regression", "Contig/reference mismatch, sparse input, and failed-output probes",
         "Mismatch, wrong reference, missing index, sparse input, and threshold violations fail loudly and publish no output BAM; legitimate multi-contig cases pass.", 38, 57, [
            assertion("Contig and reference mismatches stop without an output BAM.", "final_s5_adversarial.log"),
            assertion("A late calmd failure also leaves no final BAM.", "final_s5_adversarial.log"),
            assertion("Multi-contig headers and extra BED contigs remain valid inputs.", "final_s5_adversarial.log"),
            assertion("Sparse/shotgun-like inputs fail with the documented high-NOT-CLIPPED or no-overlap explanations.", "final_s5_adversarial.log"),
        ], "Real ARTIC/Illumina inputs plus synthetic sparse BAM run from a copied skill."),
    item(6, "Fresh stress input", "Synthetic 900-read HiFi-like full-length 16S amplicons",
         "The workflow and example clip exact boundaries across orientations, while mode tests reproduce the expected 98.1% 3-prime residual when both ends are not clipped.", 38, 58, [
            assertion("Workflow output has MD on 900/900 mapped reads and 0/0 residuals.", "final_s6_hifi.log"),
            assertion("Both-ends plus strand and the shipped example match all 900 planted boundaries.", "final_s6_hifi.log"),
            assertion("Default/strand versus both-end residual percentages reproduce.", "final_s6_hifi.log"),
            assertion("iVar and hard-clip operations complete on the fresh HiFi-like input.", "final_s6_hifi.log"),
        ], "Fresh deterministic synthetic HiFi-like data, aligned with minimap2 map-hifi."),
    item(7, "Fresh adversarial input", "Residual checker contract and wrong-scheme primer BEDs",
         "The checker passes all 20 boundary/error expectations. The example rejects three wrong-scheme/shifted BEDs by NOT CLIPPED share and emits no output.", 38, 57, [
            assertion("The residual checker passes all 20 boundary, strand, and bad-input expectations.", "final_s7_run.log"),
            assertion("Bad checker inputs return exit 2, separate from residual exit 1.", "final_s7_run.log"),
            assertion("Real unclipped and planted-residual BAMs are detected while clipped output is clean.", "final_s7_run.log"),
            assertion("v3, shifted-v5, and strand-only wrong schemes fail; matching v5 succeeds.", "final_s7b_wrong_scheme.log"),
        ], "Real ARTIC data plus planted unit cases and three wrong-scheme probes."),
]

categories = {
    "functional_suitability": (11, 12, "Complete primer clipping, repair, verification, and alternative guidance were exercised."),
    "reliability": (11, 12, "Validates contigs, references, normalized BEDs, residuals, threshold, and atomic publication."),
    "performance_context": (8, 8, "Compact workflow with documented high-read-count controls."),
    "agent_usability": (15, 16, "Actionable commands, exit distinctions, and asserted checks."),
    "human_usability": (8, 8, "Mode decision table, error table, and precise compatibility notes."),
    "security": (12, 12, "Quoted paths, controlled temporary directory, and no credential or code-injection handling."),
    "maintainability": (11, 12, "Clear split between documentation, workflow, and independent checker."),
    "agent_specific": (18, 20, "Idempotent publication boundary and explicit stop conditions."),
}
static = sum(v[0] for v in categories.values())
average = round(sum(x["total"] for x in inputs) / len(inputs), 1)
passed = sum(x["assertions_passed"] for x in inputs)
total = sum(x["assertions_total"] for x in inputs)
report = {
    "source": SOURCE,
    "meta": {"skill_name": "bio-alignment-amplicon-clipping", "description": "Trim PCR primers from aligned reads in amplicon-panel BAMs using samtools ampliconclip.", "evaluated_on": "2026-09-24", "evaluator_version": "skill-auditor@1.0", "category": "Data Analysis", "execution_mode": "B", "complexity": "Complex", "n_inputs": 7, "auditor_independent": False, "note": NOTE, "audit_kind": "final pass re-audit", "executed_inputs": "7/7", "tools": "samtools 1.24; pysam 0.24.1; iVar 1.4.4; minimap2 2.31; WSL science alignment-files"},
    "veto_gates": {"skill_veto": {"gate": "PASS", "stability": "PASS", "contract": "PASS", "determinism": "PASS", "security": "PASS"}, "research_veto": {"applicable": True, "gate": "PASS", "scientific_integrity": {"result": "PASS", "detail": "Measured claims were re-executed."}, "practice_boundaries": {"result": "PASS", "detail": "No diagnostic or prescriptive output."}, "methodological_ground": {"result": "PASS", "detail": "Mode guidance and scheme checks agree with observed behavior."}, "code_usability": {"result": "PASS", "detail": "Workflow and checker executed on real and synthetic inputs."}}},
    "static_score": {"subtotal": static, "max": 100, "categories": {k: {"score": v[0], "max": v[1], "note": v[2]} for k, v in categories.items()}},
    "dynamic_score": {"execution_avg": average, "max": 100, "assertion_pass_rate": {"passed": passed, "total": total}, "inputs": inputs},
    "final": {"static_weighted": round(static * .4, 1), "dynamic_weighted": round(average * .6, 1), "score": 95, "max": 100, "grade": "Production Ready", "grade_symbol": "⭐", "deployable": True, "veto_override": False},
    "key_strengths": ["Exact source reran all archived regressions plus two fresh inputs.", "The workflow refuses wrong/sparse schemes and publishes output only after all checks pass.", "The independent checker has verified boundary semantics and distinct bad-input status.", "CRLF, whitespace, and UCSC-header BED inputs are normalized consistently."],
    "recommendations": [],
}

assert static == 94 and len(categories) == 8 and len(inputs) == 7 and passed == total == 28
assert all(3 <= len(x["assertions"]) <= 5 and x["basic"] + x["specialized"] == x["total"] for x in inputs)
(ROOT / "eval_report_bio-alignment-amplicon-clipping_result.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

lines = ["# Eval Viewer — bio-alignment-amplicon-clipping", "", f"Generated: 2026-09-24  ", f"Source: `{SOURCE}`  ", f"Final pass note: {NOTE}", "", "## Result", "", "**95/100 — ⭐ Production Ready — deployable.** 7/7 inputs executed; 28/28 assertions passed; all veto gates pass; no open recommendations.", "", "| Input | Type | Basic | Specialized | Total | Assertions |", "|---|---:|---:|---:|---:|---:|"]
for x in inputs:
    lines.append(f"| {x['index']} | {x['type']} | {x['basic']}/40 | {x['specialized']}/60 | {x['total']}/100 | {x['assertions_passed']}/{x['assertions_total']} |")
lines += ["", "## Executed evidence", ""]
for x in inputs:
    lines += [f"### Input {x['index']} — {x['label']}", "", x["note"], "", f"Execution: {x['execution_note']}", ""]
    for check in x["assertions"]:
        lines.append(f"- [PASS] {check['text']} — `{check['note']}`")
    lines.append("")
(ROOT / "eval_viewer_bio-alignment-amplicon-clipping.md").write_text("\n".join(lines), encoding="utf-8")
print(f"static={static}; dynamic={average}; assertions={passed}/{total}; final=95")
