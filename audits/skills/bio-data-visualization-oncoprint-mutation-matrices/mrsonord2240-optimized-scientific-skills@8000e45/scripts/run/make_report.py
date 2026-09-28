"""Emit the independent re-audit JSON and human viewer from checked run evidence."""
from __future__ import annotations

import json
from pathlib import Path


SKILL = "bio-data-visualization-oncoprint-mutation-matrices"
AUDIT = Path(r"F:\OpenScience\audits") / SKILL
RUN = AUDIT / "run"
SOURCE = (
    "mrsonord2240/optimized-scientific-skills@"
    "8000e4567f1b47a812706874f7091fdc21816df2:"
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
        "The shipped script and CLI retained all 200 samples in deterministic TMB order, rendered complete alteration and FAB legends, and automatically hid the unreadable dense sample labels.", 38, 57, [
            assertion("The shipped Python CLI runs in its documented pandas 2 environment", True, "Both direct API and CLI execution completed under pandas 2.3.3/comut 0.0.3."),
            assertion("All cohort samples are retained and ordered by descending TMB", True, "200 samples exactly matched independently computed (-TMB, sample ID) order."),
            assertion("The top gene is drawn at the top and the TMB scale uses the observed maximum", True, "FLT3 is the top y tick; returned TMB maximum is the observed 42."),
            assertion("The saved plot includes legends for alteration and clinical colors", True, "Rendered legend text contains Mutations, Clinical, every observed alteration class, and all eight FAB values."),
            assertion("Dense sample labels are hidden or remain readable", True, "Rendered-text inspection found no visible x-axis sample labels for the 200-sample cohort."),
        ], "run/audit_comut.py; run/out/py_comut_regressions.log; run/out/i4_laml_comut_direct.png; run/out/i4_laml_comut_cli.png",
        "Opened both figures: the mutation/FAB legends are complete and readable, while the 200 dense sample labels are correctly absent."),
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
        "The minimal path, ordering, zero-mutation retention, and all validation checks passed; empty cohort IDs and negative TMB were rejected with explicit ValueError messages.", 38, 57, [
            assertion("The minimal mutation-plus-cohort path renders and retains zero-mutation samples", True, "All eight samples retained; Z7 and Z8 remain as empty trailing columns."),
            assertion("Burden order and top-gene placement are deterministic", True, "Sample order equals independent burden sorting; the most frequent gene is the top y tick."),
            assertion("Unknown samples/classes and duplicate cohort IDs are rejected", True, "All three probes raised clear ValueError messages."),
            assertion("Every cohort sample ID is validated as non-empty", True, "An empty cohort ID was rejected with 'must not be empty or NA'."),
            assertion("TMB values are validated as finite and non-negative", True, "A -1 TMB value was rejected with 'finite and non-negative'."),
        ], "run/audit_comut.py; run/out/py_comut_regressions.log; run/out/i9_new_minimal_comut.png",
        "Opened: the small matrix is crisp and ordered, its alteration legend is complete, and its eight sample labels are readable."),
    inp(10, "Edge", "Exact sample-label threshold and unified-legend boundary",
        "Render a 50-sample comut plot and a 51-sample version with mutation and four-level clinical tracks. Verify the default visibility boundary, force 51 labels with an override, hide all labels with threshold zero, and confirm every displayed color is named in the artifact.",
        "At exactly 50 samples every ordered label rendered; at 51 the labels were absent by default; threshold 51 restored all 51; threshold zero hid all 50. Mutation and clinical legend groups and every observed value rendered with nonzero text bounds.", 39, 58, [
            assertion("The default policy renders all sample labels at the documented 50-sample boundary", True, "The 50 rendered labels exactly equal plot.samples in deterministic order."),
            assertion("The default policy hides sample labels immediately above the boundary", True, "The 51-sample figure has zero visible x-label text artists."),
            assertion("The documented threshold override can force or suppress labels", True, "Threshold 51 rendered all 51 labels; threshold 0 hid all labels in the 50-sample plot."),
            assertion("The unified legend names both track groups and all observed values", True, "Rendered text includes Clinical, Mutations, Alpha/Beta/Gamma/Delta, and Missense/Truncating/Splice."),
            assertion("Every boundary figure is nonblank and visually coherent", True, "Three PNGs are 1220 pixels wide, 20-43 KB, and 40.4-41.3% nonwhite; all were opened."),
        ], "run/audit_comut.py; run/out/py_comut_regressions.log; run/out/i10_boundary_50_labels.png; run/out/i10_boundary_51_hidden.png; run/out/i10_boundary_51_forced.png",
        "Opened all three: legends are complete; 50 labels are individually rendered, the 51-label default is clean, and the forced 51-label override behaves as documented."),
    inp(11, "Adversarial", "Normalized-ID collisions and file-level invalid TMB",
        "Run the CLI with surrounding whitespace in otherwise valid IDs, then submit a cohort whose IDs collide after stripping, a quoted whitespace-only cohort ID, and infinite TMB. Also probe NaN, positive/negative infinity, and a small negative TMB through the public function.",
        "Valid surrounding whitespace normalized to N01/N02/N03 and rendered through both API and CLI. Duplicate-after-strip, whitespace-only, NaN, both infinities, and negative TMB were all rejected; CLI transcripts retained the documented error messages.", 39, 59, [
            assertion("Surrounding ID whitespace is normalized consistently across mutation, clinical, TMB, and cohort inputs", True, "The direct and CLI paths produced ordered samples N01, N02, N03 and nonblank figures."),
            assertion("Cohort IDs that collide after normalization are rejected", True, "Both direct and CLI probes reported that IDs must be unique after normalization."),
            assertion("A file-level whitespace-only cohort ID is rejected", True, "The quoted TSV value reached validation and produced 'must not be empty or NA'."),
            assertion("Non-finite and negative TMB values are rejected", True, "NaN, +Inf, -Inf, and -0.01 failed directly; CLI infinite TMB failed with the documented message."),
            assertion("Validation failures do not create output figures", True, "All three invalid CLI calls returned nonzero and the should-not-exist targets were absent."),
        ], "run/audit_comut.py; run/out/py_comut_regressions.log; run/out/i11_validation_cli.log; run/out/i11_normalized_ids.png; run/out/i11_normalized_ids_cli.png",
        "Opened direct and CLI figures: both show the same normalized sample order, complete clinical/mutation legends, readable labels, and valid zero-based TMB mapping."),
]

static_categories = {
    "functional_suitability": {"score": 12, "max": 12, "note": "All promised workflows are present and core scientific claims matched execution, including full-cohort denominators, row order, interaction return schema, CNV/fusion merging, and tool-specific caveats."},
    "reliability": {"score": 12, "max": 12, "note": "Major ID, class, duplicate, all-empty, label-threshold, and burden-value failures are explicit; valid reruns and invalid-input rejection are deterministic."},
    "performance_context": {"score": 8, "max": 8, "note": "SKILL.md is concise, routes complex logic to two scripts and one example, and avoids duplicated workflow prose in the usage guide."},
    "agent_usability": {"score": 16, "max": 16, "note": "Selection guidance, contracts, output expectations, legend policy, label threshold, caveats, and error-prevention notes are precise and executable."},
    "human_usability": {"score": 8, "max": 8, "note": "Natural trigger language is strong; defaults produce self-describing dense-safe artifacts, and the documented override preserves intentional control."},
    "security": {"score": 12, "max": 12, "note": "No credentials, network calls, code injection, or destructive actions; identifiers, categorical values, and numeric burden data are validated before rendering."},
    "maintainability": {"score": 12, "max": 12, "note": "Matrix construction, rendering, CLI logic, and regression tests are cleanly separated; all shipped paths parsed and all three shipped tests ran."},
    "agent_specific": {"score": 20, "max": 20, "note": "Triggering, progressive disclosure, composability, idempotency, strict stop conditions, and explicit CLI overrides are all well calibrated."},
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
        "execution_note": "Executed 11/11 inputs: all nine archived round-one scenarios plus two genuinely new round-two scenarios. R 4.4.3 with ComplexHeatmap 2.22.0, maftools 2.22.0, circlize 0.4.18; Python 3.12 with pandas 2.3.3, comut 0.0.3, matplotlib 3.11.2. Sixteen scored PNGs were opened via a contact sheet, the four round-two-critical artifacts were also opened at native resolution, and automated parse/dimension/nonwhite checks passed. Provider worktree remained at the dispatched commit and source hashes matched the audit copy.",
    },
    "veto_gates": {
        "skill_veto": {"gate": "PASS", "stability": "PASS", "contract": "PASS", "determinism": "PASS", "security": "PASS"},
        "research_veto": {
            "applicable": True, "gate": "PASS",
            "scientific_integrity": {"result": "PASS", "detail": "No fabricated references, sample counts, p-values, or efficacy claims. All reported counts and the checked Fisher p-value derive from executed data."},
            "practice_boundaries": {"result": "PASS", "detail": "Outputs remain cohort-level research visualizations and statistical associations; no individual diagnosis, prescription, or treatment advice."},
            "methodological_ground": {"result": "PASS", "detail": "The skill distinguishes MAF-only and explicit-cohort denominators, orders by mutated samples when claimed, preserves multi-class events, and warns against sparse pairwise inference."},
            "code_usability": {"result": "PASS", "detail": "All shipped R/Python scripts parsed; the full R example, all three shipped regression tests, all archived cases, and both new boundary/adversarial cases executed. Valid inputs rendered and invalid identifiers/burdens failed before output."},
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
    "recommendations": [],
}

report_path = AUDIT / f"eval_report_{SKILL}_result.json"
report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

lines = [
    f"# Eval Viewer — {SKILL}", "", "Generated: 2026-09-27", "",
    f"Source: `{SOURCE}`", "", "Independent auditor: `true`", "",
    "## Outcome", "",
    f"Final score **{final_score}/100** — ⭐ **Production Ready**; deployable **true**.", "",
    f"Executed **11/11** inputs; assertion pass rate **{passed}/{total_assertions} ({100*passed/total_assertions:.1f}%)**. All structural and research veto dimensions PASS.", "",
    "The audit contains eleven inputs because the dispatch required all nine archived round-one inputs as regressions plus at least two genuinely new round-two inputs; this intentionally exceeds the older schema note that listed at most eight.", "",
    "## Summary Table", "",
    "| Input | Type | Label | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |",
    "|---:|---|---|---:|---:|---:|---:|:---:|",
]
for item in inputs:
    lines.append(f"| {item['index']} | {item['type']} | {item['label']} | {item['basic']} | {item['specialized']} | {item['total']} | {item['assertions_passed']}/{item['assertions_total']} | {item['status_flag']} |")

lines += ["", "## Execution environment and source integrity", "",
          "- R 4.4.3: ComplexHeatmap 2.22.0, maftools 2.22.0, circlize 0.4.18 via the required `r.sh` wrapper.",
          "- Python 3.12: pandas 2.3.3, comut 0.0.3, matplotlib 3.11.2 via `PYENV=venv-pd2 py.sh`.",
          "- Provider worktree HEAD: `8000e4567f1b47a812706874f7091fdc21816df2`; `git status --short` remained empty.",
          "- The copied SKILL.md and provider SKILL.md SHA-256 hashes match; see `run/out/source_hashes.log`.",
          "- Automated artifact verification: all scored PNGs parse, exceed 1 KB, have valid dimensions, and exceed 0.5% nonwhite pixels. Sixteen scored PNGs were opened in the contact sheet; four round-two-critical figures were also opened at native resolution.", "",
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
          "No open recommendations. The round-one P1 legend/dense-label finding and P2 ID/TMB-validation finding both passed regression and two new boundary/adversarial scenarios.", "",
          "Open counts: **P0 0, P1 0, P2 0**.", ""]

viewer_path = AUDIT / f"eval_viewer_{SKILL}.md"
viewer_path.write_text("\n".join(lines), encoding="utf-8")
print(report_path)
print(viewer_path)
print("score", final_score, "executed", len(inputs), "assertions", passed, "/", total_assertions)
