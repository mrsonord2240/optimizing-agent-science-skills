"""Build the round-two color-palettes audit report and human viewer."""

from __future__ import annotations

import json
from pathlib import Path


AUDIT = Path(r"F:\OpenScience\audits\bio-data-visualization-color-palettes")
SKILL = "bio-data-visualization-color-palettes"


def assertion(text: str, note: str) -> dict:
    return {"text": text, "result": "PASS", "note": note}


cases = [
    {
        "index": 1,
        "type": "Canonical",
        "label": "Named Okabe-Ito mapping for seven cell types plus unassigned",
        "prompt": "Assign stable colors to seven cell types plus Unassigned, preserve identities after subsetting, and check CVD behavior.",
        "output": "A named seven-color Okabe-Ito mapping plus Unassigned=#BBBBBB remained stable after T cells were removed. Unassigned also used a cross marker. R CIELAB minima after deutan/protan/tritan transforms were 14.93/20.71/16.17.",
        "evidence": "run/regressions.R; figs/i1_named_okabe_stability.png",
        "basic": 38,
        "specialized": 57,
        "assertions": [
            assertion("Every category is assigned through a named mapping and Unassigned is light grey", "Seven chromatic names plus Unassigned=#BBBBBB were present."),
            assertion("Removing T cells does not recolor any remaining category", "Full and subset ggplot_build mappings were identical for shared levels."),
            assertion("All three CVD simulations produce finite positive minimum distances", "R minima were 14.93, 20.71, and 16.17; Python independently returned 14.17, 13.96, and 10.97."),
            assertion("A redundant non-color encoding distinguishes the reserve class", "Unassigned uses marker 4 while chromatic categories use marker 16."),
            assertion("The full and subset plots render non-blank with readable legends", "The opened figure showed stable colors, the grey cross class, and complete legends."),
        ],
    },
    {
        "index": 2,
        "type": "Variant A",
        "label": "vik log-fold-change heatmap with symmetric q99 bounds",
        "prompt": "Use vik for a signed LFC heatmap, anchor zero, derive symmetric robust bounds, and compare its built-in centre to an exact-white custom ramp.",
        "output": "The q99 absolute-LFC bound was 4.814764. vik sampled #EBE5E0 at the centre, while the odd 101-color custom ramp sampled #FFFFFF exactly; both arms and the neutral region remained visible.",
        "evidence": "run/regressions.R; figs/i2_diverging_centres.png",
        "basic": 39,
        "specialized": 58,
        "assertions": [
            assertion("Bounds are symmetric at plus/minus the 99th percentile of absolute LFC", "The computed limits were -4.814764 and +4.814764."),
            assertion("Zero is anchored at the built-in vik centre", "midpoint=0 and symmetric limits place zero at #EBE5E0."),
            assertion("The output does not mislabel vik's centre as pure white", "The measured near-neutral centre is reported explicitly."),
            assertion("A custom ramp can deliberately sample exact white at zero", "The 101-color custom ramp's 51st color was #FFFFFF."),
            assertion("Both diverging arms and the neutral region are visually legible", "The opened heatmaps showed the positive block, negative block, and midpoint without blank panels."),
        ],
    },
    {
        "index": 3,
        "type": "Edge",
        "label": "CVD and grayscale audit of sequential and rainbow-like candidates",
        "prompt": "Audit batlow and turbo under grayscale plus deutan, protan, and tritan simulation, and report whether luminance is monotonic.",
        "output": "The actual batlow palette remained luminance-monotonic after desaturation; turbo rose then fell in L*. All three CVD transformations returned finite positive distances and the six swatches rendered correctly.",
        "evidence": "run/regressions.R and run/regressions.py; figs/i3_grayscale_cvd.png",
        "basic": 39,
        "specialized": 58,
        "assertions": [
            assertion("The grayscale check desaturates the actual palette", "colorspace::desaturate(batlow) was rendered, not a generic grey ramp."),
            assertion("batlow has monotonic CIELAB lightness", "All successive L* differences had one direction."),
            assertion("turbo is not presented as luminance-monotonic", "The regression asserted that turbo L* rises and then falls."),
            assertion("The CVD code performs all three simulations and reports distances", "Both R and Python produced finite minima for deutan/protan/tritan variants."),
            assertion("The simulated and grayscale panels are visually inspectable", "The opened figure showed six labeled, populated swatches and turbo's light-dark reversal."),
        ],
    },
    {
        "index": 4,
        "type": "Variant B",
        "label": "Migrate sequential, signed, and cyclic panels away from jet",
        "prompt": "Replace jet across a magnitude panel, a signed panel, and a phase panel with semantically correct palettes and preserve cyclic closure.",
        "output": "The migration used batlow for magnitude, vik with symmetric q99=5.956655 for signed data, and romaO for phase. Zero normalized to 0.5; tested cyclic seams stayed below two CAM02-UCS units.",
        "evidence": "run/regressions.py; figs/i4_jet_migration_fixed.png",
        "basic": 39,
        "specialized": 58,
        "assertions": [
            assertion("The sequential panel no longer uses jet or rainbow", "It uses cmcrameri batlow."),
            assertion("The signed panel uses a diverging palette and symmetric data-derived limits", "vik uses plus/minus q99 and maps zero to 0.5."),
            assertion("The phase panel uses a cyclic palette", "romaO is used from zero to 2*pi."),
            assertion("Cyclic endpoints close without an artificial seam", "romaO, vikO, and twilight endpoint distances were each below two CAM02-UCS units."),
            assertion("All three panels render with visible data and color bars", "The opened output contained three populated, appropriately encoded panels."),
        ],
    },
    {
        "index": 5,
        "type": "Stress",
        "label": "Run shipped examples and assess many-group and journal palettes",
        "prompt": "Run both shipped examples, then assess a 15-group request and the npg/aaas/lancet palettes for accessibility claims.",
        "output": "Both examples reached PASS sentinels and emitted non-empty artifacts. The representative figure used batlow, symmetric vik, and stable named mappings. Journal and many-group palettes retained close CVD pairs, so the output did not claim universal safety.",
        "evidence": "run/skill/examples, run/run_fixed_tests.R, run/regressions.*, figs/i5_palette_examples_fixed.png",
        "basic": 38,
        "specialized": 56,
        "assertions": [
            assertion("Both shipped R examples execute on self-contained synthetic data", "Both ran and emitted non-empty PDF output."),
            assertion("The four-panel example follows the current guidance", "It uses batlow, symmetric vik, named Okabe-Ito, and stable subsetting."),
            assertion("Journal palettes are not claimed as universal accessibility defaults", "Measured deutan minima were npg 9.66, aaas 8.96, and lancet 7.51."),
            assertion("The 15-group request is not answered with a supposedly CVD-safe hue-only palette", "tab20, Paired, and Set3 each had a deutan minimum below 10."),
            assertion("The representative shipped example is visually sound", "The opened four-panel figure was populated and its categorical identities stayed stable."),
        ],
    },
    {
        "index": 6,
        "type": "Scope Boundary",
        "label": "Thirty clusters with a request for hue-only identity colors",
        "prompt": "Give me 30 unique CVD-safe identity hues and do not use labels, shapes, or facets.",
        "output": "The response declined the false accessibility promise and produced 30 directly labeled facets using one accessible accent. All clusters remained represented without smuggling identity back into hue.",
        "evidence": "run/regressions.R; figs/i6_thirty_groups_faceted.png",
        "basic": 38,
        "specialized": 55,
        "assertions": [
            assertion("The output refuses the false promise of 30 CVD-safe identity hues", "Hue-only encoding beyond eight groups is identified as unsafe."),
            assertion("A practical redundant alternative is produced", "The plot uses direct facet labels."),
            assertion("All 30 clusters remain represented", "The factor has 30 levels and the opened plot has 30 labeled facets."),
            assertion("The alternative does not smuggle identity back into hue", "ggplot_build found exactly one point color across all facets."),
            assertion("The 30-panel output is visually inspectable", "The opened output showed populated C01-C30 facets with readable labels."),
        ],
    },
    {
        "index": 7,
        "type": "Adversarial",
        "label": "Nonzero 0.5 reference with missing matrix cells",
        "prompt": "Plot a 0-to-1 fraction matrix centered on the scientific reference 0.5 and make missing cells unambiguous.",
        "output": "TwoSlopeNorm mapped the declared reference to 0.5, 48 missing cells stayed masked, and #BBBBBB separated missingness from the quantitative palette. The opened figure showed distinct white-reference and grey-missing regions.",
        "evidence": "run/regressions.py; figs/i7_nonzero_midpoint_missing.png",
        "basic": 38,
        "specialized": 58,
        "assertions": [
            assertion("The 0.5 scientific reference maps to the diverging centre", "TwoSlopeNorm(vcenter=0.5) returns 0.5 at the reference."),
            assertion("Missing values are not silently mapped to a quantitative color", "The copied colormap uses #BBBBBB as its bad color."),
            assertion("All missing cells are preserved as missing", "The mask count is 48, matching the synthetic block."),
            assertion("The response reports reference, bounds, and masked count", "The current guidance explicitly requires these fields."),
            assertion("Reference and missing regions are visually distinct", "The opened figure shows the white reference block separately from the grey missing block."),
        ],
    },
    {
        "index": 8,
        "type": "Stress",
        "label": "Two new cases: response contract and arbitrary physical reference",
        "prompt": "Case A: return a complete palette-audit contract for a masked sequential heatmap. Case B: center a physical scale on 37.2, mask NaN and both infinities, and reject a reference on a bound.",
        "output": "Case A emitted all seven contract fields with cividis, percentile bounds, 30 masked cells, monotonic L*, explicit not-applicable CVD entries, a redundant-encoding rationale, and an inspection artifact. Case B mapped 37.2 to 0.5, masked five NaN/+Inf/-Inf cells in grey, and raised ValueError when vmin equaled the reference.",
        "evidence": "run/input8_response_contract.json, run/input9_response_contract.json, run/regressions.py, figs/i8_response_contract.png, figs/i9_arbitrary_reference_nonfinite.png",
        "basic": 39,
        "specialized": 59,
        "assertions": [
            assertion("Case A contains every response-contract field", "The JSON has exactly palette/type, normalization/bounds/reference, missingness, CVD, luminance, redundant encoding, and visual inspection."),
            assertion("Case A computes rather than invents contract values", "Bounds, 30 masked cells, and minimum L* delta came from the saved synthetic array."),
            assertion("Case B maps the arbitrary reference 37.2 to the palette centre", "TwoSlopeNorm returned exactly 0.5 for 37.2."),
            assertion("Case B preserves all NaN, +Inf, and -Inf cells as missing", "Five mixed non-finite cells remained masked and used #BBBBBB."),
            assertion("Both new figures are non-blank and independently inspectable", "Both opened outputs showed the expected scale, reference behavior, and visible grey missing cells; pixel checks also passed."),
        ],
    },
]

for case in cases:
    case["status"] = "COMPLETED"
    case["status_flag"] = "✅"
    case["total"] = case["basic"] + case["specialized"]
    case["assertions_passed"] = sum(a["result"] == "PASS" for a in case["assertions"])
    case["assertions_total"] = len(case["assertions"])
    case["note"] = case["output"]
    case["executed"] = True
    case["execution_note"] = f"Executed and checked: {case['evidence']}."

dynamic_inputs = []
for case in cases:
    dynamic_inputs.append({
        key: case[key]
        for key in (
            "index", "type", "label", "status", "status_flag", "note", "basic",
            "specialized", "total", "assertions_passed", "assertions_total",
            "assertions", "executed", "execution_note",
        )
    })

execution_avg = round(sum(c["total"] for c in cases) / len(cases), 1)
assertion_passed = sum(c["assertions_passed"] for c in cases)
assertion_total = sum(c["assertions_total"] for c in cases)
static_total = 98
static_weighted = round(static_total * 0.4, 1)
dynamic_weighted = round(execution_avg * 0.6, 1)
final_score = round(static_weighted + dynamic_weighted)

report = {
    "meta": {
        "skill_name": SKILL,
        "description": "Select colormaps and qualitative palettes for scientific figures using perceptual uniformity, color-vision-deficiency safety, luminance behavior, data semantics, explicit non-finite handling, and a compact response contract.",
        "evaluated_on": "2026-09-27",
        "evaluator_version": "skill-auditor@1.0",
        "category": "Data Analysis",
        "execution_mode": "A",
        "complexity": "Complex",
        "n_inputs": 8,
        "source": "mrsonord2240/optimized-scientific-skills@99b1d0ad49174e647b358c58d487f5c20aa56c5c:skills/bio-data-visualization-color-palettes",
        "audit_type": "independent round-two re-audit after follow-up fix",
        "auditor_independent": True,
        "executed": True,
        "execution_note": "Executed all seven archived scored inputs plus a two-case round-two stress input (nine distinct cases total). All 40 assertions passed and all nine PNGs were pixel-checked and opened. R runs reached PASS sentinels and emitted checked outputs before the shared launcher returned 2816; a base-R probe exited 0 while a ggplot2-only probe reproduced exit 2816, separating package teardown from Skill execution. Provider HEAD, status, and SHA-256 hashes were identical before and after.",
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
            "gate": "PASS",
            "scientific_integrity": {"result": "PASS", "detail": "All centers, bounds, distances, mask counts, normalization results, and image properties were computed from saved synthetic fixtures or installed palette implementations."},
            "practice_boundaries": {"result": "PASS", "detail": "The Skill selects scientific figure encodings and makes no diagnosis, prescription, treatment recommendation, or participant-level inference."},
            "methodological_ground": {"result": "PASS", "detail": "Palette types match data semantics; quantitative references, robust bounds, non-finite masking, CVD checks, grayscale testing, and redundant encodings are kept distinct."},
            "code_usability": {"result": "PASS", "detail": "R and Python code parsed, reached PASS sentinels, satisfied all assertions, and emitted nine non-blank checked artifacts. The post-success R exit is independently reproducible with ggplot2 alone and is not a Skill failure."},
        },
    },
    "static_score": {
        "subtotal": static_total,
        "max": 100,
        "categories": {
            "functional_suitability": {"score": 12, "max": 12, "note": "Completeness 4, correctness 4, appropriateness 4. Sequential, diverging, cyclic, categorical, CVD, grayscale, many-group, nonzero-reference, and missing-value workflows are complete and consistent."},
            "reliability": {"score": 11, "max": 12, "note": "Fault tolerance 4, error reporting 3, recoverability 4. Non-finite values are explicitly masked and invalid diverging bounds are rejected; underlying library errors remain plain rather than structured."},
            "performance_context": {"score": 8, "max": 8, "note": "Token cost 4, efficiency 4. SKILL.md is 283 lines, the guide routes instead of duplicating, and executable depth remains in examples/tests."},
            "agent_usability": {"score": 16, "max": 16, "note": "Learnability 4, consistency 4, feedback design 4, error prevention 4. The seven-field response checklist makes completion and verification observable."},
            "human_usability": {"score": 8, "max": 8, "note": "Discoverability 4, forgiveness 4. Natural prompts cover standard cases, while arbitrary references and NaN/infinity handling are explicit."},
            "security": {"score": 12, "max": 12, "note": "Credential safety 4, input validation 4, data safety 4. There are no secrets, raw-string execution, network calls, destructive operations, or data-retention hazards; bounds and finite values are checked."},
            "maintainability": {"score": 12, "max": 12, "note": "Modularity 4, modifiability 4, testability 4. A concise guide, self-contained examples, and focused R/Python contract tests cleanly separate responsibilities."},
            "agent_specific": {"score": 19, "max": 20, "note": "Trigger precision 4, progressive disclosure 4, composability 4, idempotency 4, escape hatches 3. The response contract creates a clean integration seam; broad stop/handoff guidance is naturally limited for this advisory visualization Skill."},
        },
    },
    "dynamic_score": {
        "execution_avg": execution_avg,
        "max": 100,
        "assertion_pass_rate": {"passed": assertion_passed, "total": assertion_total},
        "inputs": dynamic_inputs,
    },
    "final": {
        "static_weighted": static_weighted,
        "dynamic_weighted": dynamic_weighted,
        "score": final_score,
        "max": 100,
        "grade": "Production Ready",
        "grade_symbol": "⭐",
        "deployable": True,
        "veto_override": False,
        "grade_note": "All Production Ready floors pass: static 98>=80, execution 95.9>=85, Layer 1 average 38.5>=32, Layer 2 average 57.4>=48, assertions 40/40=100%, no veto, no open P0, and no open P1.",
    },
    "key_strengths": [
        "The response contract makes palette type, normalization, missingness, CVD behavior, luminance, redundant encoding, and visual verification explicit and machine-checkable.",
        "Arbitrary scientific references and NaN/+Inf/-Inf values are handled without allowing missing data to enter the quantitative color scale.",
        "Categorical identity mappings remain stable across subsets and switch to labels or facets when hue cannot safely carry identity.",
        "Shipped examples and focused tests execute in both R and Python against preserved synthetic fixtures, with nine visually inspected outputs.",
    ],
    "recommendations": [],
}

report_path = AUDIT / f"eval_report_{SKILL}_result.json"
report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

lines = [
    f"# Eval Viewer — {SKILL}",
    "",
    "Generated: 2026-09-27",
    "",
    "## Summary",
    "",
    "This independent round-two re-audit held provider commit `99b1d0ad49174e647b358c58d487f5c20aa56c5c` immutable. It reran all seven archived inputs and added two genuinely new cases inside the eighth scored stress input, for nine distinct executed cases.",
    "",
    "| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |",
    "|---:|---|---:|---:|---:|---:|---|",
]
for case in cases:
    lines.append(f"| {case['index']} | {case['type']} | {case['basic']} | {case['specialized']} | {case['total']} | {case['assertions_passed']}/{case['assertions_total']} | ✅ |")
lines += [
    "",
    f"**Execution average:** {execution_avg}/100  ",
    f"**Assertion pass rate:** {assertion_passed}/{assertion_total} (100%)  ",
    "**Executed:** 8/8 scored inputs; 9/9 distinct cases  ",
    "**Vetoes:** none  ",
    "**Open findings:** 0 P0, 0 P1, 0 P2",
    "",
    "## Detailed outputs",
]
for case in cases:
    lines += [
        "",
        f"### Input {case['index']} — {case['type']}: {case['label']}",
        "",
        f"**Prompt:** {case['prompt']}",
        "",
        f"**Output:** {case['output']}",
        "",
        f"**Execution evidence:** `{case['evidence']}`",
        "",
        f"**Scores:** Basic {case['basic']}/40 | Specialized {case['specialized']}/60 | Total {case['total']}/100",
        "",
        "**Assertions:**",
    ]
    for item in case["assertions"]:
        lines.append(f"- [PASS] {item['text']} — {item['note']}")

lines += [
    "",
    "## Static evaluation",
    "",
    "| Category | Score | Note |",
    "|---|---:|---|",
]
labels = {
    "functional_suitability": "Functional Suitability",
    "reliability": "Reliability",
    "performance_context": "Performance / Context",
    "agent_usability": "Agent Usability",
    "human_usability": "Human Usability",
    "security": "Security",
    "maintainability": "Maintainability",
    "agent_specific": "Agent-Specific",
}
for key, category in report["static_score"]["categories"].items():
    lines.append(f"| {labels[key]} | {category['score']}/{category['max']} | {category['note']} |")

lines += [
    "",
    "## Veto gates",
    "",
    "- T1 Stability: PASS — all outputs were produced and checked; the R package-teardown exit is environment-wide.",
    "- T2 Contract: PASS — required frontmatter, shipped paths, and report fields are present and consistent.",
    "- T3 Determinism: PASS — saved fixtures and fixed seeds reproduce asserted values.",
    "- T4 Security: PASS — no raw-string execution, credential handling, network access, or destructive operations.",
    "- M1 Scientific Integrity: PASS — every numerical claim is computed and preserved in run evidence.",
    "- M2 Practice Boundaries: PASS — visualization guidance only.",
    "- M3 Methodological Ground: PASS — encodings match data semantics and accessibility limitations are explicit.",
    "- M4 Code Usability: PASS — all R/Python PASS sentinels and checked artifacts were produced.",
    "",
    "## Environment-exit distinction",
    "",
    "Every R Skill run reached its PASS sentinel and emitted checked output before the shared launcher returned exit 2816. `run/r_exit_probe.R` exited 0; `run/r_package_exit_probe.R` printed `loaded ggplot2 4.0.3` and then returned 2816. This reproduces the teardown behavior without Skill code, so it is recorded as environment behavior rather than an execution failure.",
    "",
    "## Source integrity",
    "",
    "`run/source_integrity_before.out` and `run/source_integrity_after.out` are byte-identical. Both record provider HEAD `99b1d0ad49174e647b358c58d487f5c20aa56c5c`, an empty status, and the same SHA-256 digest for every Skill file.",
    "",
    "## Open recommendations",
    "",
    "None. The two prior P2 findings are closed by the response contract and explicit arbitrary-reference/non-finite guidance, and the independent runs found no replacement defects.",
    "",
    "## Evidence index",
    "",
    "- Full run: `run/run_all.ps1`, `run/run_all.out`",
    "- R regressions and environment probes: `run/regressions.R`, `run/regressions_r.out`, `run/r_exit_probe.*`, `run/r_package_exit_probe.*`",
    "- Python regressions and new response contracts: `run/regressions.py`, `run/regressions_py.out`, `run/input8_response_contract.json`, `run/input9_response_contract.json`",
    "- Fixed Skill snapshot and tests: `run/skill/`, `run/fixed_contracts_*.out`, `run/fixed_examples_r.out`",
    "- Pixel checks and manual visual review: `run/inspect_images.py`, `run/inspect_images.out`, `figs/i1_*.png` through `figs/i9_*.png`",
    "- Provider immutability: `run/source_integrity.ps1`, `run/source_integrity_before.out`, `run/source_integrity_after.out`",
]

viewer_path = AUDIT / f"eval_viewer_{SKILL}.md"
viewer_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

assert report["static_score"]["subtotal"] == sum(
    c["score"] for c in report["static_score"]["categories"].values()
)
assert len(report["dynamic_score"]["inputs"]) == report["meta"]["n_inputs"]
assert all(3 <= len(c["assertions"]) <= 5 for c in report["dynamic_score"]["inputs"])
assert all(c["basic"] + c["specialized"] == c["total"] for c in report["dynamic_score"]["inputs"])
assert all(c["assertions_passed"] == sum(a["result"] == "PASS" for a in c["assertions"]) for c in report["dynamic_score"]["inputs"])
assert report["dynamic_score"]["execution_avg"] == round(
    sum(c["total"] for c in report["dynamic_score"]["inputs"]) / report["meta"]["n_inputs"], 1
)
assert report["dynamic_score"]["assertion_pass_rate"] == {"passed": 40, "total": 40}
assert report["final"]["static_weighted"] == round(report["static_score"]["subtotal"] * 0.4, 1)
assert report["final"]["dynamic_weighted"] == round(report["dynamic_score"]["execution_avg"] * 0.6, 1)
assert report["final"]["score"] == 97
assert report["final"]["grade"] == "Production Ready"
assert report["final"]["deployable"] is True
assert report["final"]["veto_override"] is False
assert report["recommendations"] == []

print(f"REPORT FINALIZATION PASS score={final_score} inputs={len(cases)} cases=9 assertions={assertion_passed}/{assertion_total}")
