"""Build and validate the independent re-audit JSON and Markdown viewer."""

from __future__ import annotations

import json
from pathlib import Path
from statistics import mean


AUDIT = Path(r"F:\OpenScience\audits\bio-data-visualization-color-palettes")
SKILL = "bio-data-visualization-color-palettes"
SOURCE = (
    "mrsonord2240/optimized-scientific-skills@"
    "cd2cfef126db14008baf614af792317daf6ff1e1:"
    "skills/bio-data-visualization-color-palettes"
)


def assertion(text: str, result: str, note: str) -> dict:
    return {"text": text, "result": result, "note": note}


inputs = [
    {
        "index": 1,
        "type": "Canonical",
        "label": "Named Okabe-Ito mapping for seven cell types plus unassigned",
        "status": "COMPLETED",
        "status_flag": "✅",
        "note": (
            "The fixed named mapping stayed byte-for-byte stable after T cells were removed. "
            "Unassigned used #BBBBBB plus a distinct cross marker; R CIELAB minima after "
            "deutan/protan/tritan transforms were 14.93/20.71/16.17."
        ),
        "basic": 38,
        "specialized": 57,
        "total": 95,
        "assertions": [
            assertion("Every category is assigned through a named mapping and Unassigned is light grey", "PASS", "Seven chromatic names plus Unassigned=#BBBBBB were present."),
            assertion("Removing T cells does not recolor any remaining category", "PASS", "The full and subset ggplot_build mappings were identical for all shared levels."),
            assertion("All three CVD simulations produce finite positive minimum pairwise distances", "PASS", "R minima were 14.93, 20.71, and 16.17; Python independently returned 14.17, 13.96, and 10.97 in CAM02-UCS."),
            assertion("A redundant non-color encoding distinguishes the reserve class", "PASS", "Unassigned uses marker 4 while chromatic categories use marker 16."),
            assertion("The full and subset plots render non-blank with readable legends", "PASS", "Manual visual inspection confirmed stable colors, the grey cross class, and complete legends."),
        ],
        "executed": True,
        "execution_note": "Executed run/regressions.R on the 1,270-row synthetic UMAP; opened figs/i1_named_okabe_stability.png.",
    },
    {
        "index": 2,
        "type": "Variant A",
        "label": "vik log-fold-change heatmap with symmetric q99 bounds",
        "status": "COMPLETED",
        "status_flag": "✅",
        "note": (
            "The fixed guidance correctly separates built-in near-neutral centres from an exact-white "
            "custom ramp. q99 was 4.814764, vik sampled #EBE5E0 at its centre, and the odd 101-color "
            "custom ramp sampled #FFFFFF exactly."
        ),
        "basic": 39,
        "specialized": 58,
        "total": 97,
        "assertions": [
            assertion("Bounds are symmetric at plus/minus the 99th percentile of absolute LFC", "PASS", "The computed limits were -4.814764 and +4.814764."),
            assertion("Zero is anchored at the built-in vik centre", "PASS", "midpoint=0 and symmetric limits place zero at the measured #EBE5E0 centre."),
            assertion("The output does not mislabel vik's centre as pure white", "PASS", "The output explicitly reports the near-neutral built-in centre."),
            assertion("A custom ramp can deliberately sample exact white at zero", "PASS", "The 101-color custom ramp's 51st color was #FFFFFF."),
            assertion("Both diverging arms and the neutral region are visually legible", "PASS", "Manual inspection found no blank panel or lost midpoint; the skewed positive block and negative block remain distinct."),
        ],
        "executed": True,
        "execution_note": "Executed run/regressions.R on synthetic_skewed_lfc.csv; opened figs/i2_diverging_centres.png.",
    },
    {
        "index": 3,
        "type": "Edge",
        "label": "CVD and grayscale audit of sequential and rainbow-like candidates",
        "status": "COMPLETED",
        "status_flag": "✅",
        "note": (
            "The corrected workflow uses deutan/protan/tritan transforms and desaturates the actual "
            "palette. batlow remained luminance-monotonic; turbo was correctly identified as non-monotonic."
        ),
        "basic": 39,
        "specialized": 58,
        "total": 97,
        "assertions": [
            assertion("The grayscale check desaturates the actual palette", "PASS", "colorspace::desaturate(batlow) was rendered rather than a generic grey ramp."),
            assertion("batlow has monotonic CIELAB lightness", "PASS", "All successive L* differences had one direction."),
            assertion("turbo is not presented as luminance-monotonic", "PASS", "The regression asserted that turbo L* rises and then falls."),
            assertion("The CVD code performs deutan, protan, and tritan simulations and reports distances", "PASS", "Both R and Python produced finite minimum pairwise distances for all three simulations."),
            assertion("The simulated and grayscale panels are visually inspectable", "PASS", "Manual inspection confirmed six non-blank labeled swatches and visible turbo light-dark reversal."),
        ],
        "executed": True,
        "execution_note": "Executed run/regressions.R and run/regressions.py; opened figs/i3_grayscale_cvd.png.",
    },
    {
        "index": 4,
        "type": "Variant B",
        "label": "Migrate sequential, signed, and cyclic matplotlib panels away from jet",
        "status": "COMPLETED",
        "status_flag": "✅",
        "note": (
            "The migration chose batlow for magnitude, vik with symmetric q99 bounds for signed data, "
            "and romaO for phase. Zero normalized to 0.5 and romaO/vikO/twilight seam distances were below 2."
        ),
        "basic": 39,
        "specialized": 58,
        "total": 97,
        "assertions": [
            assertion("The sequential panel no longer uses jet or rainbow", "PASS", "It uses cmcrameri batlow."),
            assertion("The signed panel uses a diverging palette and symmetric data-derived limits", "PASS", "vik uses plus/minus q99=5.956655 and maps zero to 0.5."),
            assertion("The phase panel uses a cyclic palette", "PASS", "romaO is used from 0 to 2*pi."),
            assertion("Cyclic palette endpoints close without an artificial seam", "PASS", "romaO, vikO, and twilight endpoint distances were each below 2 CAM02-UCS units."),
            assertion("All three migrated panels render with visible data and color bars", "PASS", "Manual inspection confirmed three non-blank, appropriately encoded panels."),
        ],
        "executed": True,
        "execution_note": "Executed run/regressions.py on synthetic_spatial_expr.npy; opened figs/i4_jet_migration_fixed.png.",
    },
    {
        "index": 5,
        "type": "Stress",
        "label": "Run both shipped examples and assess 15-group and journal palettes",
        "status": "COMPLETED",
        "status_flag": "✅",
        "note": (
            "Both shipped examples reached their PASS sentinels and emitted non-empty outputs. "
            "The four-panel example follows batlow/vik/named-Okabe-Ito guidance. Journal palettes had "
            "deutan minima below 10, and tab20/Paired/Set3 were correctly rejected as hue-only accessibility solutions."
        ),
        "basic": 38,
        "specialized": 56,
        "total": 94,
        "assertions": [
            assertion("Both shipped R examples execute on self-contained synthetic data", "PASS", "palette_examples.R and palettes_phd.R ran and emitted non-empty PDF output."),
            assertion("The four-panel example follows the Skill's current palette guidance", "PASS", "It uses batlow, symmetric vik, named Okabe-Ito, and stable subsetting."),
            assertion("Journal palettes are not claimed to be universal accessibility defaults", "PASS", "Measured deutan minima were npg 9.66, aaas 8.96, and lancet 7.51."),
            assertion("The 15-group request is not answered with a supposedly CVD-safe hue-only palette", "PASS", "tab20, Paired, and Set3 each had deutan minimum distance below 10 and the output routes to redundant encodings."),
            assertion("The representative shipped example is visually sound", "PASS", "Manual inspection confirmed four populated panels, outlined midpoint points, and stable categorical colors."),
        ],
        "executed": True,
        "execution_note": "Executed copied fixed tests and examples from run/skill; opened figs/i5_palette_examples_fixed.png and verified all emitted PNGs with run/inspect_images.py.",
    },
    {
        "index": 6,
        "type": "Scope Boundary",
        "label": "Thirty clusters with a request for hue-only identity colors",
        "status": "COMPLETED",
        "status_flag": "✅",
        "note": (
            "The output declines to imply that 30 unique hues can be CVD-safe, then uses direct facet "
            "labels and a single accessible accent. All 30 labels are present and only one identity color is used."
        ),
        "basic": 38,
        "specialized": 55,
        "total": 93,
        "assertions": [
            assertion("The output refuses the false promise of 30 CVD-safe identity hues", "PASS", "It explicitly treats hue-only encoding beyond eight groups as unsafe."),
            assertion("A practical redundant alternative is produced", "PASS", "The plot uses direct facet labels rather than color identity."),
            assertion("All 30 clusters remain represented", "PASS", "The factor has 30 levels and the plot contains 30 labeled facets."),
            assertion("The alternative does not smuggle identity back into hue", "PASS", "ggplot_build found exactly one point color across all facets."),
            assertion("The 30-panel output is visually inspectable", "PASS", "Manual inspection confirmed filled free-scale panels and readable C01-C30 labels."),
        ],
        "executed": True,
        "execution_note": "New input executed in run/regressions.R; opened figs/i6_thirty_groups_faceted.png.",
    },
    {
        "index": 7,
        "type": "Adversarial",
        "label": "Nonzero reference midpoint with missing matrix cells",
        "status": "COMPLETED",
        "status_flag": "✅",
        "note": (
            "The output generalized the diverging principle to a scientifically meaningful reference of 0.5, "
            "masked 48 missing cells, and encoded them as #BBBBBB. The reference maps exactly to 0.5 in the norm."
        ),
        "basic": 37,
        "specialized": 54,
        "total": 91,
        "assertions": [
            assertion("The scientifically meaningful 0.5 reference maps to the diverging centre", "PASS", "TwoSlopeNorm(vcenter=0.5) returns 0.5 at the reference."),
            assertion("Missing values are not silently mapped to a quantitative color", "PASS", "The masked array uses cmap bad color #BBBBBB."),
            assertion("All missing cells are preserved as missing", "PASS", "The mask count is 48, matching the synthetic missing block."),
            assertion("The two arms use explicit symmetric conceptual bounds around the reference", "PASS", "The fraction limits are 0 and 1 around reference 0.5."),
            assertion("The reference and missing regions are visually distinct", "PASS", "Manual inspection shows a white reference block and a separate grey missing block."),
        ],
        "executed": True,
        "execution_note": "New input executed in run/regressions.py; opened figs/i7_nonzero_midpoint_missing.png.",
    },
]

for item in inputs:
    item["assertions_passed"] = sum(a["result"] == "PASS" for a in item["assertions"])
    item["assertions_total"] = len(item["assertions"])

categories = {
    "functional_suitability": {"score": 12, "max": 12, "note": "Completeness 4, correctness 4, appropriateness 4. Sequential, diverging, cyclic, categorical, CVD, grayscale, migration, and >8-group boundaries are consistent and executable."},
    "reliability": {"score": 10, "max": 12, "note": "Fault tolerance 3, error reporting 3, recoverability 4. Version-introspection and design fallbacks are clear, although arbitrary non-finite data and custom reference points require agent judgment."},
    "performance_context": {"score": 8, "max": 8, "note": "Token cost 4, efficiency 4. SKILL.md is 252 lines; the guide routes rather than duplicates, and executable depth lives in examples/tests."},
    "agent_usability": {"score": 15, "max": 16, "note": "Learnability 4, consistency 4, feedback design 3, error prevention 4. The workflow is internally consistent and preventive; a compact result-report contract would further standardize responses."},
    "human_usability": {"score": 7, "max": 8, "note": "Discoverability 4, forgiveness 3. Natural prompts cover common requests; unusual nonzero midpoints and missing encodings are handled by generalization rather than explicit examples."},
    "security": {"score": 11, "max": 12, "note": "Credential safety 4, input validation 3, data safety 4. No secrets, shell interpolation, network calls, destructive operations, or data retention are present."},
    "maintainability": {"score": 12, "max": 12, "note": "Modularity 4, modifiability 4, testability 4. Concise guide, two self-contained examples, and focused R/Python contract tests cleanly separate responsibilities."},
    "agent_specific": {"score": 18, "max": 20, "note": "Trigger precision 4, progressive disclosure 4, composability 3, idempotency 4, escape hatches 3. The trigger is precise and >8/>20 group limits are explicit; response integration points remain informal."},
}

static_subtotal = sum(value["score"] for value in categories.values())
execution_avg = round(mean(item["total"] for item in inputs), 1)
assertions_passed = sum(item["assertions_passed"] for item in inputs)
assertions_total = sum(item["assertions_total"] for item in inputs)
static_weighted = round(static_subtotal * 0.4, 1)
dynamic_weighted = round(execution_avg * 0.6, 1)
final_score = round(static_weighted + dynamic_weighted)

report = {
    "meta": {
        "skill_name": SKILL,
        "description": "Select colormaps and qualitative palettes for scientific figures using perceptual-uniformity, color-vision-deficiency safety, and luminance-monotonicity criteria. Covers Crameri, viridis-family, Okabe-Ito, ColorBrewer, and jet/rainbow migration.",
        "evaluated_on": "2026-09-27",
        "evaluator_version": "skill-auditor@1.0",
        "category": "Data Analysis",
        "execution_mode": "A",
        "complexity": "Complex",
        "n_inputs": 7,
        "source": SOURCE,
        "audit_type": "independent re-audit after fix",
        "auditor_independent": True,
        "executed": True,
        "execution_note": (
            "Executed all five archived inputs as regressions plus two genuinely new inputs. "
            "R and Python assertions reached PASS sentinels, Python exited 0, and all seven PNGs were "
            "manually opened plus pixel-checked. The shared R runtime currently exits 2816 during package "
            "teardown after successful output; a minimal ggplot2-only probe reproduces this outside the Skill, "
            "while a base-R probe exits 0. No Skill bytes or provider worktree files were modified."
        ),
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
            "scientific_integrity": {"result": "PASS", "detail": "No result was fabricated; all reported centers, bounds, distances, mappings, masks, and plot properties were computed from saved synthetic fixtures or installed palette implementations."},
            "practice_boundaries": {"result": "PASS", "detail": "The Skill selects scientific figure encodings and makes no diagnosis, prescription, treatment recommendation, or participant-level inference."},
            "methodological_ground": {"result": "PASS", "detail": "Palette type matches data semantics in all seven outputs; quantitative bounds, CVD simulation, grayscale testing, and redundant encodings are correctly separated."},
            "code_usability": {"result": "PASS", "detail": "R and Python code parsed, executed all assertions, and emitted checked artifacts. Python and pixel checks exited 0. The post-success R exit 2816 is environment-wide and independently reproduces on loading ggplot2 alone, not a Skill code failure."},
        },
    },
    "static_score": {"subtotal": static_subtotal, "max": 100, "categories": categories},
    "dynamic_score": {
        "execution_avg": execution_avg,
        "max": 100,
        "assertion_pass_rate": {"passed": assertions_passed, "total": assertions_total},
        "inputs": inputs,
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
        "grade_note": (
            "All Production Ready floors pass: static 93>=80, execution 94.9>=85, "
            "Layer 1 average 38.3>=32, Layer 2 average 56.6>=48, assertions 35/35=100%, "
            "no veto, and no open P0."
        ),
    },
    "key_strengths": [
        "The fixed guidance is internally consistent across sequential, diverging, cyclic, and categorical use cases, including measured built-in centres and data-derived symmetric limits.",
        "CVD and grayscale checks now execute in both R and Python and report finite distances while explicitly avoiding a false universal accessibility cutoff.",
        "Named categorical mappings remain stable across subsets, reserve grey is explicit, and redundant shape/facet strategies are used when hue cannot safely carry identity.",
        "Both shipped examples are self-contained, match the prose, and are backed by focused cross-language contract tests.",
    ],
    "recommendations": [
        {
            "priority": "P2",
            "title": "Add a compact palette-audit response contract",
            "observed_in": [],
            "problem": "The Skill specifies the computations but not a single standard response shape for reporting the chosen type, limits, midpoint, grayscale result, CVD minima, redundant encoding, and visual-inspection outcome.",
            "root_cause": "Feedback expectations are distributed across several sections rather than summarized as an output checklist.",
            "fix": "Add a short final-response checklist with palette name/type, normalization and bounds, CVD minima, luminance verdict, redundant encoding, and visual inspection status.",
        },
        {
            "priority": "P2",
            "title": "Show arbitrary reference points and missing values",
            "observed_in": [7],
            "problem": "The nonzero-reference case succeeded, but the Skill only demonstrates midpoint zero and does not explicitly show how to mask missing values with a non-quantitative bad color.",
            "root_cause": "Examples center on signed LFC/z-score data and assume finite numeric matrices.",
            "fix": "Add one compact Python or R note: set the diverging midpoint to the scientific reference value, mask non-finite cells, and assign missing values a separate neutral color such as #BBBBBB.",
        },
    ],
}

# Strict schema and arithmetic checks.
assert list(report) == ["meta", "veto_gates", "static_score", "dynamic_score", "final", "key_strengths", "recommendations"]
assert report["meta"]["source"] == SOURCE
assert report["meta"]["auditor_independent"] is True
assert len(categories) == 8 and static_subtotal == 93
assert len(inputs) == report["meta"]["n_inputs"] == 7
assert all(3 <= len(item["assertions"]) <= 5 for item in inputs)
assert all(item["basic"] + item["specialized"] == item["total"] for item in inputs)
assert all(item["assertions_passed"] == sum(a["result"] == "PASS" for a in item["assertions"]) for item in inputs)
assert execution_avg == 94.9
assert assertions_passed == assertions_total == 35
assert static_weighted == 37.2 and dynamic_weighted == 56.9 and final_score == 94
assert all(item["executed"] for item in inputs)
assert len(report["key_strengths"]) == 4
assert [item["priority"] for item in report["recommendations"]] == ["P2", "P2"]

report_path = AUDIT / f"eval_report_{SKILL}_result.json"
report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

prompts = [
    "Assign one CVD-safe Okabe-Ito color to each of these 7 cell types, reserve grey for ambient/unassigned. My UMAP has T, B, NK, monocyte, dendritic, platelet and erythroid cells plus unassigned cells; I'll also show a subset without the T cells.",
    "Use a diverging Crameri vik palette for a log-fold-change heatmap with symmetric bounds at +/- the 99th percentile of |LFC|. Zero must map to pure white.",
    "Run colorspace::cvd_emulator on the current palette and report whether the categories remain distinguishable under deuteranopia; also verify it prints correctly in grayscale. Candidates: viridis, cividis, batlow, turbo, rainbow.",
    "Find every plot in this notebook that uses cmap='jet' and replace it; the spatial map, the signed log-ratio panel and the phase panel are all affected.",
    "Run the shipped examples, then color 15 clusters and tell me whether npg/aaas/lancet are safe for the reviewers.",
    "I have 30 clusters and the journal wants one unique color per cluster. Just give me a CVD-safe 30-color palette; do not use shapes, labels, or facets.",
    "Plot a 0-to-1 fraction matrix where 0.5 is the biological reference, values above and below 0.5 are equally important, and some cells are missing. Use a publication-ready diverging encoding and make missing cells unambiguous.",
]

code_refs = [
    "run/regressions.R (named cell_colors, stable ggplot_build mapping, redundant shape)",
    "run/regressions.R (scale_fill_scico vik + odd-count custom gradient)",
    "run/regressions.R and run/regressions.py (desaturate/L* and complete CVD transforms)",
    "run/regressions.py (batlow, symmetric vik q99, romaO)",
    "run/skill/examples/*.R, run/skill/tests/*, and both regression scripts",
    "run/regressions.R (30 labeled free-scale facets, one accessible accent)",
    "run/regressions.py (masked array, TwoSlopeNorm(vcenter=0.5), set_bad('#BBBBBB'))",
]

viewer = [
    f"# Eval Viewer - {SKILL} (INDEPENDENT RE-AUDIT)",
    "",
    "Generated: 2026-09-27",
    f"Source: `{SOURCE}`",
    "Auditor independent: `true`",
    "Category: Data Analysis | Mode A | Complexity: Complex -> 7 inputs",
    "Data: saved synthetic fixtures only; provider Skill snapshot copied byte-for-byte under `run/skill/` (6/6 hashes matched).",
    "",
    "## Result",
    "",
    "| Metric | Result |",
    "|---|---|",
    f"| Static | **{static_subtotal}/100** |",
    f"| Execution average | **{execution_avg}/100** (Layer 1 38.3/40; Layer 2 56.6/60) |",
    f"| Final | **{final_score}/100** |",
    "| Grade | **Production Ready** |",
    "| Deployable | **true** |",
    "| Executed | **7/7** |",
    f"| Assertions | **{assertions_passed}/{assertions_total} (100%)** |",
    "| Vetoes | none |",
    "| Open P0/P1/P2 | **0/0/2** |",
    "",
    "All Production Ready floors pass. The five archived prompts were rerun as regressions; Inputs 6 and 7 are genuinely new.",
    "",
    "## Summary Table",
    "",
    "| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |",
    "|---:|---|---:|---:|---:|---:|---|",
]
for item in inputs:
    viewer.append(
        f"| {item['index']} | {item['type']} | {item['basic']} | {item['specialized']} | "
        f"{item['total']} | {item['assertions_passed']}/{item['assertions_total']} | {item['status_flag']} |"
    )

viewer.extend([
    "",
    "## Execution and visual evidence",
    "",
    "`run/run_all.out` records the full regression suite. `run/inspect_images.out` confirms seven PNGs at 1120-1820 px wide, non-white fractions 0.0169-0.7478, and >100 unique RGB values each. All seven PNGs were also opened manually.",
    "",
    "The shared R environment currently returns process code 2816 after successful package teardown. This is not Skill-specific: `run/r_package_exit_probe.R ggplot2` reproduces it, while `run/r_exit_probe.R` (base R only) exits 0. Every R audit script reached its explicit PASS sentinel and emitted parseable, non-empty artifacts; the independent Python contracts and image checks exit 0.",
    "",
    "## Detailed Outputs",
])

for item, prompt, code_ref in zip(inputs, prompts, code_refs):
    viewer.extend([
        "",
        f"### Input {item['index']} - {item['type']}: {item['label']}",
        "",
        f"**Prompt:** {prompt}",
        "",
        f"**Generated code / run:** `{code_ref}`",
        "",
        f"**Output:** {item['note']}",
        "",
        f"**Execution evidence:** {item['execution_note']}",
        "",
        f"**Scores:** Basic {item['basic']}/40 | Specialized {item['specialized']}/60 | Total {item['total']}/100",
        "",
        "**Assertions:**",
    ])
    for check in item["assertions"]:
        viewer.append(f"- [{check['result']}] {check['text']} - {check['note']}")

viewer.extend([
    "",
    "## Static evaluation",
    "",
    "| Category | Score | Note |",
    "|---|---:|---|",
])
for name, value in categories.items():
    viewer.append(f"| {name.replace('_', ' ').title()} | {value['score']}/{value['max']} | {value['note']} |")

viewer.extend([
    "",
    "## Veto gates",
    "",
    "- T1 Stability: PASS - every output was produced and checked; the R post-success exit is independently environment-wide.",
    "- T2 Contract: PASS - required frontmatter and shipped paths are present; report schema validated.",
    "- T3 Determinism: PASS - fixtures are fixed, examples seed randomness, and reruns reproduce asserted values.",
    "- T4 Security: PASS - no raw-string execution, credential handling, network access, or destructive operation.",
    "- M1 Scientific Integrity: PASS - all numeric claims are computed and saved.",
    "- M2 Practice Boundaries: PASS - visualization guidance only.",
    "- M3 Methodological Ground: PASS - encodings match data semantics and accessibility limits are explicit.",
    "- M4 Code Usability: PASS - R/Python contracts and all seven outputs executed; checked artifacts are non-blank.",
    "",
    "## Open recommendations",
    "",
    "- P2: Add a compact response contract covering palette type, limits/midpoint, CVD minima, luminance verdict, redundant encoding, and visual inspection.",
    "- P2: Add a compact example for arbitrary scientific reference points and explicit missing-value colors.",
    "",
    "## Evidence index",
    "",
    "- Full run: `run/run_all.out`",
    "- R regressions: `run/regressions.R`, `run/regressions_r.out`",
    "- Python regressions: `run/regressions.py`, `run/regressions_py.out`",
    "- Fixed Skill snapshot and tests: `run/skill/`",
    "- Pixel checks: `run/inspect_images.py`, `run/inspect_images.out`",
    "- Runtime probes: `run/r_exit_probe.R`, `run/r_exit_probe.out`, `run/r_package_exit_probe.R`",
    "- Figures: `figs/i1_named_okabe_stability.png` through `figs/i7_nonzero_midpoint_missing.png`",
])

viewer_path = AUDIT / f"eval_viewer_{SKILL}.md"
viewer_path.write_text("\n".join(viewer) + "\n", encoding="utf-8")
print("REPORT FINALIZATION PASS")
print(report_path)
print(viewer_path)
