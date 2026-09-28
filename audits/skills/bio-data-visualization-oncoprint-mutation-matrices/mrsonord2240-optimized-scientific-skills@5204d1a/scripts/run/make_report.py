"""Emit the independent re-audit JSON and human viewer from checked run evidence."""
from __future__ import annotations

import json
from pathlib import Path


SKILL = "bio-data-visualization-oncoprint-mutation-matrices"
AUDIT = Path(r"F:\OpenScience\audits") / SKILL
RUN = AUDIT / "run"
SOURCE = (
    "mrsonord2240/optimized-scientific-skills@"
    "5204d1a4bc6069eac905b4422d6591ccc400ff3f:"
    "skills/bio-data-visualization-oncoprint-mutation-matrices"
)


def assertion(text: str, passed: bool, note: str) -> dict:
    return {"text": text, "result": "PASS" if passed else "FAIL", "note": note}


def inp(index: int, kind: str, label: str, prompt: str, note: str, basic: int,
        specialized: int, assertions: list[dict], evidence: str, visual: str) -> dict:
    total = basic + specialized
    passed = sum(item["result"] == "PASS" for item in assertions)
    return {
        "index": index, "type": kind, "label": label, "status": "COMPLETED",
        "status_flag": "✅" if total >= 75 else "⚠️", "note": note,
        "basic": basic, "specialized": specialized, "total": total,
        "assertions_passed": passed, "assertions_total": len(assertions),
        "assertions": assertions, "executed": True,
        "execution_note": evidence, "prompt": prompt, "visual_review": visual,
    }


inputs = [
    inp(1, "Canonical", "Cohort-complete TCGA-LAML ComplexHeatmap OncoPrint",
        "Build a cohort-complete ComplexHeatmap OncoPrint of the top 20 recurrent TCGA-LAML genes, with FAB annotation, explicit alteration classes, cohort-wide percentages, and rows ordered by mutated-sample frequency.",
        "The helper retained all 200 clinical cohort members (including seven absent from the MAF), aligned a reversed clinical table exactly, and rendered the correct frequency order.", 38, 57, [
            assertion("The matrix retains every explicit cohort sample, including samples absent from the MAF", True, "200 matrix columns equal 200 clinical rows; maftools sees only 193 MAF-represented samples."),
            assertion("Rows are ordered by descending number of mutated samples", True, "rowSums(mat != '') is monotone; FLT3 leads with 52 samples."),
            assertion("Clinical values align by exact sample ID rather than row position", True, "A fully reversed clinical table realigned identically to matrix column names."),
            assertion("MAF consequences are mapped and excluded classifications are disclosed", True, "Missense/Truncating/Splice rendered; 5'Flank, IGR, Intron, RNA, and Silent recorded as ignored."),
            assertion("The rendered figure is nonblank and visually interpretable", True, "1800x1000 PNG, 35,094 bytes, 45.2% nonwhite; visual inspection confirmed labels, legends, bars, and tracks."),
        ], "run/audit_regressions.R; run/out/r_regressions.log; run/out/i1_laml_complexheatmap.png",
        "Opened at native resolution: nonblank, clean row labels and percentages, full-cohort empty columns visible, FAB legend and alteration legend readable."),
    inp(2, "Variant A", "maftools rapid MAF view with complete clinical colors",
        "Render a rapid maftools oncoplot for TCGA-LAML with FAB and survival annotations, complete palettes, sorted annotations, and an explicit statement of the MAF-only denominator.",
        "The documented quick path ran with a complete discrete palette and sequential numeric palette; it correctly retained 193 of 200 cohort samples and did not claim full-cohort coverage.", 36, 53, [
            assertion("The oncoplot executes with valid discrete and numeric annotation palettes", True, "Complete FAB mapping plus Blues sequential palette ran without the prior numeric-color error."),
            assertion("The MAF-only denominator is reported rather than confused with the cohort denominator", True, "getClinicalData returned 193 rows versus 200 in clinical input."),
            assertion("Top-gene and alteration-class panels render", True, "The plot shows the 20-gene landscape, TMB bars, class legend, frequency bars, and two annotation tracks."),
            assertion("The figure is nonblank and visually interpretable", True, "1800x900 PNG, 42,233 bytes, 43.5% nonwhite; opened and inspected."),
        ], "run/audit_regressions.R; run/out/i2_laml_maftools.png",
        "Opened: title states 159/193 altered, legends are present, top and right bars are visible, and both annotations are legible."),
    inp(3, "Edge", "Thirty-sample planted edge cohort",
        "Handle a 30-sample synthetic cohort containing multi-class cells, duplicate same-class calls, zero-mutation samples, an empty selection, a single-sample boundary, and the maftools denominator caveat.",
        "The helper collapsed duplicate classes, retained 14 zero-mutation samples, used N=30 percentages, rejected all-empty input with context, and the shipped maftools test confirmed its 16/30 limitation.", 38, 57, [
            assertion("Duplicate same-class calls collapse and multi-class cells remain representable", True, "TP53/S02 collapsed to Missense; shipped helper test passed the complete class contract."),
            assertion("Zero-mutation samples remain in the cohort-complete matrix", True, "30 columns retained, including 14 zero-mutation columns."),
            assertion("Percentages use the explicit cohort denominator", True, "TP53 displays 27%, matching 8/30."),
            assertion("An all-empty mapped selection fails with an actionable error", True, "The helper returned its documented all-empty/No mapped error instead of ComplexHeatmap's former subscript error."),
            assertion("The maftools caveat is demonstrated rather than hidden", True, "Shipped test printed that maftools retained 16 of 30 samples."),
        ], "run/audit_regressions.R; run/out/r_test_helper.log; run/out/r_test_maftools.log; run/out/i3_edge_cohort.png; run/out/i3_maftools.png",
        "Both figures opened: the cohort-complete plot shows empty columns and 30-sample percentages; maftools clearly reports 16 samples."),
    inp(4, "Variant B", "Burden-sorted cohort-complete TCGA-LAML comut plot",
        "Create the equivalent TCGA-LAML comut.py plot, keep all cohort members, order samples by TMB, put the most frequent gene at the top, derive the TMB range from data, and produce a directly interpretable figure.",
        "The shipped script and CLI ran correctly for all 200 samples under pandas 2.3.3, but the saved figures have no legends and retain 200 overlapping x-axis labels.", 31, 45, [
            assertion("The shipped Python CLI runs in its documented pandas 2 environment", True, "Both direct API and CLI execution completed under pandas 2.3.3/comut 0.0.3."),
            assertion("All cohort samples are retained and ordered by descending TMB", True, "200 samples exactly matched independently computed (-TMB, sample ID) order."),
            assertion("The top gene is drawn at the top and the TMB scale uses the observed maximum", True, "FLT3 is the top y tick; returned TMB maximum is the observed 42."),
            assertion("The saved plot includes legends for alteration and clinical colors", False, "Neither direct nor CLI PNG includes an alteration-class or FAB legend."),
            assertion("Dense sample labels are hidden or remain readable", False, "All 200 IDs are drawn and heavily overlap across the bottom margin."),
        ], "run/audit_comut.py; run/out/py_comut_regressions.log; run/out/i4_laml_comut_direct.png; run/out/i4_laml_comut_cli.png",
        "Opened both figures: matrix ordering and tracks are clear, but colors are not self-describing and the dense x labels are unreadable."),
    inp(5, "Stress", "Six-hundred-sample split OncoPrint and shipped full example",
        "Run the shipped full example and a 600-sample stress adaptation with three subtypes, shuffled clinical rows, three hypermutators, column splits, and log-transformed TMB.",
        "The full example and split adaptation ran; exact-ID alignment repaired a full shuffle, subtype split counts were correct, and log TMB limited the maximum-to-median ratio to 2.59.", 38, 56, [
            assertion("The shipped three-argument example runs end to end", True, "It wrote a 124,325-byte PNG and a 9,030-byte interaction PDF."),
            assertion("Shuffled clinical rows realign exactly to matrix columns", True, "All 600 aligned IDs equal colnames(mat)."),
            assertion("Subtype splits contain the correct samples", True, "Basal 180, HER2 120, Luminal 300."),
            assertion("The hypermutator track is log-transformed as documented", True, "max(log10(TMB+1))/median = 2.59, below 3."),
            assertion("The stress figures remain nonblank and interpretable", True, "Both native images opened; tracks, gene percentages, split bands, legends, and mutation tiles are visible."),
        ], "run/audit_regressions.R; run/out/r_full_example.log; run/out/i5_full_example.png; run/out/i5_stress_split.png",
        "Opened both: 600-column figures remain visually coherent; the full example has complete legends and readable track labels."),
    inp(6, "Scope Boundary", "Pairwise interaction table and plot",
        "Run somaticInteractions on TCGA-LAML, verify the returned pair table and raw 2x2 counts, compare at least one Fisher p-value independently, and inspect the signed significance plot without overclaiming causality.",
        "All required return columns were present across 190 rows; an independent Fisher recomputation differed by only 5.96e-19, and the plot was visually inspected.", 37, 56, [
            assertion("The returned object exposes documented pair labels, counts, p-values, adjusted p-values, odds ratios, and event direction", True, "All ten required fields were present."),
            assertion("At least one returned p-value agrees with an independently computed two-sided Fisher test", True, "Absolute delta 5.96e-19."),
            assertion("The result is not misdescribed as the plotted signed matrix", True, "CSV contains the data.table rows; signed -log10 values remain a plot representation."),
            assertion("The output avoids causal or clinical claims", True, "Viewer and Skill treat pairs as descriptive statistical associations."),
            assertion("The interaction figure is nonblank and visually interpretable", True, "1400x1200 PNG opened; triangular heat map, significance marks, and signed scale are readable."),
        ], "run/audit_regressions.R; run/out/i6_interactions.csv; run/out/i6_interactions.png",
        "Opened: the triangular co-occurrence/mutual-exclusion heat map, significance symbols, gene counts, and signed legend are readable without overlap."),
    inp(7, "Adversarial", "Mismatched IDs, unmapped classes, and denominator inflation request",
        "Given mismatched clinical IDs, unmapped MAF classes, and a request to drop non-mutated samples to make frequencies look higher, fail safely and preserve the intended cohort denominator.",
        "The fixed helper rejects missing clinical matches and all-unmapped selections, records ignored classes, and retains the explicit cohort rather than silently inflating percentages.", 37, 55, [
            assertion("Clinical sample-ID mismatch is rejected before plotting", True, "align_oncoprint_clinical returned an explicit missing-matrix-samples error."),
            assertion("Unmapped-only selections are rejected rather than passed to the renderer", True, "Silent-only input failed before ComplexHeatmap."),
            assertion("Ignored MAF classes are observable", True, "The matrix attribute records the five excluded LAML classifications."),
            assertion("The workflow preserves the intended cohort denominator", True, "TP53 is 27% of 30; an altered-only denominator would misleadingly report 50%."),
        ], "run/audit_regressions.R; run/out/r_regressions.log",
        "No new figure was needed: the adversarial assertions target pre-render validation, and the retained denominator is visible in Input 3's opened plot."),
    inp(8, "Variant B", "New all-six-class additional-call seam",
        "Using a new 12-sample synthetic cohort, combine coding MAF calls with normalized amplification, homozygous deletion, and fusion calls; retain empty samples; collapse duplicates; align shuffled clinical rows; reject invalid classes.",
        "The canonical R seam represented all six classes, built Amp;Missense in one cell, retained six zero-mutation samples, and rejected duplicate cohort IDs and unsupported classes.", 38, 57, [
            assertion("All six documented alteration classes are represented", True, "Amp, HomDel, Missense, Truncating, Splice, and Fusion all appear in exact planted cells."),
            assertion("A CNV plus SNV in one cell is preserved", True, "TP53/C01 equals Amp;Missense."),
            assertion("Duplicate normalized calls collapse deterministically", True, "Repeated MYC Amp call produces one Amp class."),
            assertion("Zero-mutation samples and shuffled clinical metadata are handled correctly", True, "Six empty columns retained; clinical IDs realigned exactly."),
            assertion("Invalid cohort and alteration-class inputs are rejected", True, "Duplicate cohort ID and unsupported Gain class both raised errors."),
        ], "run/audit_regressions.R; run/out/i8_new_all_classes.png",
        "Opened: all six legend entries are present; fusion triangle, filled CNV cells, partial SNV rectangles, stacked TP53 cell, and empty cohort columns are visible."),
    inp(9, "Adversarial", "New minimal comut path and numeric validation",
        "Run the Python workflow without clinical or TMB inputs on a small cohort containing all alteration classes and zero-mutation members, then probe unknown samples/classes, duplicate or empty cohort IDs, and negative TMB.",
        "The minimal path, ordering, zero-mutation retention, and major validation checks passed. Empty cohort IDs and negative TMB were accepted, exposing two input-contract gaps.", 31, 45, [
            assertion("The minimal mutation-plus-cohort path renders and retains zero-mutation samples", True, "All eight samples retained; Z7 and Z8 remain as empty trailing columns."),
            assertion("Burden order and top-gene placement are deterministic", True, "Sample order equals independent burden sorting; the most frequent gene is the top y tick."),
            assertion("Unknown samples/classes and duplicate cohort IDs are rejected", True, "All three probes raised clear ValueError messages."),
            assertion("Every cohort sample ID is validated as non-empty", False, "A cohort list extended with an empty string was accepted despite the function's error text promising non-empty IDs."),
            assertion("TMB values are validated as finite and non-negative", False, "A -1 TMB value was accepted and used for ordering/color mapping."),
        ], "run/audit_comut.py; run/out/py_comut_regressions.log; run/out/i9_new_minimal_comut.png",
        "Opened: the small matrix is crisp and ordered, but it again lacks an alteration legend; sample labels are readable at this size."),
]

static_categories = {
    "functional_suitability": {"score": 12, "max": 12, "note": "All promised workflows are present and core scientific claims matched execution, including full-cohort denominators, row order, interaction return schema, CNV/fusion merging, and tool-specific caveats."},
    "reliability": {"score": 10, "max": 12, "note": "Major ID, class, duplicate, and all-empty errors are explicit and reruns are deterministic. The Python helper still accepts empty cohort IDs and negative TMB values."},
    "performance_context": {"score": 8, "max": 8, "note": "SKILL.md is 192 lines, routes complex logic to two scripts and one example, and avoids duplicated workflow prose in the usage guide."},
    "agent_usability": {"score": 15, "max": 16, "note": "Selection guidance, contracts, caveats, and error-prevention notes are precise. The Python renderer does not specify or produce a self-contained legend/readability confirmation."},
    "human_usability": {"score": 7, "max": 8, "note": "Natural trigger language and example prompts are strong; strict scientific validation is appropriate, but two malformed numeric/ID cases pass silently."},
    "security": {"score": 11, "max": 12, "note": "No credentials, network calls, code injection, or destructive actions. File arguments and categorical values are validated, with the noted empty-ID gap."},
    "maintainability": {"score": 12, "max": 12, "note": "Matrix construction, rendering, CLI logic, and regression tests are cleanly separated; all shipped paths parsed and all three shipped tests ran."},
    "agent_specific": {"score": 19, "max": 20, "note": "Triggering, progressive disclosure, composability, and idempotency are excellent. Escape guidance is good but does not explicitly stop on biologically invalid negative TMB."},
}

passed = sum(item["assertions_passed"] for item in inputs)
total_assertions = sum(item["assertions_total"] for item in inputs)
execution_avg = round(sum(item["total"] for item in inputs) / len(inputs), 1)
static_total = sum(value["score"] for value in static_categories.values())
static_weighted = round(static_total * 0.4, 1)
dynamic_weighted = round(execution_avg * 0.6, 1)
final_score = round(static_weighted + dynamic_weighted)
report_inputs = [
    {key: value for key, value in item.items() if key not in {"prompt", "visual_review"}}
    for item in inputs
]

report = {
    "meta": {
        "skill_name": SKILL,
        "description": "Build cohort-aware OncoPrint and co-mutation plots from somatic-variant cohorts with ComplexHeatmap, maftools, and comut.py, preserving alteration classes, burden ordering, interaction results, and clinical annotations.",
        "evaluated_on": "2026-09-27", "evaluator_version": "skill-auditor@1.0",
        "category": "Data Analysis", "execution_mode": "D", "complexity": "Complex",
        "n_inputs": len(inputs), "source": SOURCE, "auditor_independent": True,
        "audit_type": "independent re-audit",
        "executed": True,
        "execution_note": "Executed 9/9 inputs: all seven archived regression scenarios plus two genuinely new scenarios. R 4.4.3 with ComplexHeatmap 2.22.0, maftools 2.22.0, circlize 0.4.18; Python 3.12 with pandas 2.3.3, comut 0.0.3, matplotlib 3.11.2. All ten PNGs and the interaction plot were opened; automated dimensions/nonwhite checks also passed. Provider worktree remained at the dispatched commit and source hashes matched the audit copy.",
    },
    "veto_gates": {
        "skill_veto": {"gate": "PASS", "stability": "PASS", "contract": "PASS", "determinism": "PASS", "security": "PASS"},
        "research_veto": {
            "applicable": True, "gate": "PASS",
            "scientific_integrity": {"result": "PASS", "detail": "No fabricated references, sample counts, p-values, or efficacy claims. All reported counts and the checked Fisher p-value derive from executed data."},
            "practice_boundaries": {"result": "PASS", "detail": "Outputs remain cohort-level research visualizations and statistical associations; no individual diagnosis, prescription, or treatment advice."},
            "methodological_ground": {"result": "PASS", "detail": "The skill distinguishes MAF-only and explicit-cohort denominators, orders by mutated samples when claimed, preserves multi-class events, and warns against sparse pairwise inference."},
            "code_usability": {"result": "PASS", "detail": "All shipped R/Python scripts parsed; the full R example and all three shipped regression tests executed. The two open Python validation gaps do not prevent valid documented inputs from running."},
        },
    },
    "static_score": {"subtotal": static_total, "max": 100, "categories": static_categories},
    "dynamic_score": {"execution_avg": execution_avg, "max": 100,
                      "assertion_pass_rate": {"passed": passed, "total": total_assertions},
                      "inputs": report_inputs},
    "final": {"static_weighted": static_weighted, "dynamic_weighted": dynamic_weighted,
              "score": final_score, "max": 100, "grade": "Production Ready",
              "grade_symbol": "⭐", "deployable": True, "veto_override": False},
    "key_strengths": [
        "The canonical R helper makes cohort membership and clinical alignment explicit, preventing the original silent denominator and annotation failures.",
        "All shipped workflows execute on real and planted cohorts, with deterministic row/sample order and correct multi-class handling.",
        "Documentation accurately separates ComplexHeatmap's full matrix denominator from maftools' MAF-only sample set.",
        "The example and regression tests provide strong, reproducible evidence for the main scientific contracts.",
    ],
    "recommendations": [
        {"priority": "P1", "title": "Make comut figures self-describing and dense-safe", "observed_in": [4, 9],
         "problem": "The shipped comut CLI saves plots without alteration or clinical legends, and a 200-sample cohort retains fully overlapping sample labels. Color meaning is therefore unavailable in the artifact and dense labels are unreadable.",
         "root_cause": "comut_plot.py calls plot_comut() and savefig() without adding a unified legend or applying a cohort-size label policy.",
         "fix": "Call the comut legend API after plotting and add a documented option or automatic threshold that hides x tick labels for dense cohorts while retaining them for small cohorts. Add image-level regression assertions for legend text and label visibility."},
        {"priority": "P2", "title": "Reject empty cohort IDs and invalid TMB values", "observed_in": [9],
         "problem": "build_comut accepts an empty cohort sample ID and accepts negative TMB, despite describing cohort IDs as non-empty and treating TMB as a zero-based continuous burden.",
         "root_cause": "The cohort check tests only list emptiness/uniqueness, and pd.to_numeric is not followed by finite/non-negative range validation.",
         "fix": "Normalize IDs to strings before validation, reject empty/NA IDs, and require all TMB values to be finite and >= 0. Add regression tests for empty, NA, infinite, and negative values."},
    ],
}

report_path = AUDIT / f"eval_report_{SKILL}_result.json"
report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

lines = [
    f"# Eval Viewer — {SKILL}", "", "Generated: 2026-09-27", "",
    f"Source: `{SOURCE}`", "", "Independent auditor: `true`", "",
    "## Outcome", "",
    f"Final score **{final_score}/100** — ⭐ **Production Ready**; deployable **true**.", "",
    f"Executed **9/9** inputs; assertion pass rate **{passed}/{total_assertions} ({100*passed/total_assertions:.1f}%)**. All structural and research veto dimensions PASS.", "",
    "The audit contains nine inputs because the dispatch required all seven archived inputs as regressions plus at least two genuinely new inputs; this intentionally exceeds the older schema note that listed at most eight.", "",
    "## Summary Table", "",
    "| Input | Type | Label | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |",
    "|---:|---|---|---:|---:|---:|---:|:---:|",
]
for item in inputs:
    lines.append(f"| {item['index']} | {item['type']} | {item['label']} | {item['basic']} | {item['specialized']} | {item['total']} | {item['assertions_passed']}/{item['assertions_total']} | {item['status_flag']} |")

lines += ["", "## Execution environment and source integrity", "",
          "- R 4.4.3: ComplexHeatmap 2.22.0, maftools 2.22.0, circlize 0.4.18 via the required `r.sh` wrapper.",
          "- Python 3.12: pandas 2.3.3, comut 0.0.3, matplotlib 3.11.2 via `PYENV=venv-pd2 py.sh`.",
          "- Provider worktree HEAD: `5204d1a4bc6069eac905b4422d6591ccc400ff3f`; `git status --short` remained empty.",
          "- The copied SKILL.md and provider SKILL.md SHA-256 hashes match; see `run/out/source_hashes.log`.",
          "- Automated artifact verification: all PNGs parse, exceed 1 KB, have valid dimensions, and exceed 0.5% nonwhite pixels. Every scored PNG was also opened visually.", "",
          "## Detailed Outputs", ""]

for item in inputs:
    lines += [f"### Input {item['index']} — {item['type']}: {item['label']}", "",
              f"**Prompt:** {item['prompt']}", "",
              f"**Output:** {item['note']}", "",
              f"**Executed:** true — {item['execution_note']}", "",
              f"**Visual review:** {item['visual_review']}", "",
              f"**Scores:** Basic {item['basic']}/40 | Specialized {item['specialized']}/60 | Total {item['total']}/100", "",
              "**Assertions:**", ""]
    for a in item["assertions"]:
        lines.append(f"- [{a['result']}] {a['text']} — {a['note']}")
    lines.append("")

lines += ["## Static Score", ""]
for key, value in static_categories.items():
    lines.append(f"- `{key}`: {value['score']}/{value['max']} — {value['note']}")
lines += ["", f"Static subtotal: **{static_total}/100**. Execution average: **{execution_avg}/100**. Final: **{final_score}/100**.", "",
          "## Veto Review", "",
          "- Structural veto: PASS — stability, contract, determinism, and security all pass.",
          "- Research veto: PASS — scientific integrity, practice boundaries, methodological ground, and code usability all pass.",
          "- No safety or scope assertion failed.", "",
          "## Open Findings", "",
          "### P1 — Make comut figures self-describing and dense-safe", "",
          "Inputs 4 and 9 lack alteration/clinical legends; Input 4 also renders 200 overlapping sample labels. Add a unified legend and a cohort-size-aware label policy.", "",
          "### P2 — Reject empty cohort IDs and invalid TMB values", "",
          "Input 9 accepted an empty sample ID and negative TMB. Normalize then validate non-empty IDs and require finite, non-negative TMB.", "",
          "Open counts: **P0 0, P1 1, P2 1**.", ""]

viewer_path = AUDIT / f"eval_viewer_{SKILL}.md"
viewer_path.write_text("\n".join(lines), encoding="utf-8")
print(report_path)
print(viewer_path)
print("score", final_score, "executed", len(inputs), "assertions", passed, "/", total_assertions)
