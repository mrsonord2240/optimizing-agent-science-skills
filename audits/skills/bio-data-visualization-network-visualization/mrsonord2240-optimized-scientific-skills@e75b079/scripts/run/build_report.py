"""Build and validate the independent re-audit JSON report and Markdown viewer."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
manifest = json.loads((ROOT / "data/input_manifest.json").read_text(encoding="utf-8"))


def assertion(text: str, result: str, note: str) -> dict[str, str]:
    return {"text": text, "result": result, "note": note}


scores = [
    {
        "basic": 38,
        "specialized": 58,
        "basic_dims": "Correctness 10/10; Reliability/clarity 9/10; Efficiency 9/10; Scope/safety 10/10",
        "spec_dims": "Method validity 20/20; Code 15/15; QC 9/10; Reproducibility 9/10; Security 5/5",
        "note": "Executed the copied static CLI on the synthetic 100-node/511-edge PPI. Four parseable nonblank PNGs were produced; widths span 0.5-4.0, legend swatches exactly match node colors, and all four views use the same capped 15-node label dictionary.",
        "execution_note": "run/run_python_cases.sh -> run/audit_python_cases.py; output metrics in logs/python_results.json and logs/artifact_metrics.json; visually inspected out/input1_static_ppi/network_communities.png.",
        "assertions": [
            assertion("All 100 nodes and 511 edges are represented in the static workflow", "PASS", "The CLI printed 100 nodes and 511 edges; image collections and the source graph agree."),
            assertion("Community nodes and legend swatches use one identical discrete palette", "PASS", "Independent RGBA equality check passed for all nodes."),
            assertion("Edge widths are bounded in the documented 0.5-4 point range", "PASS", "Observed minimum 0.5 and maximum 4.0."),
            assertion("Static views label only the documented adaptive capped subset", "PASS", "The focused regression intercepted all four draw calls and found one identical 15-node label dictionary."),
            assertion("Every output is parseable, nonblank, and visually inspected", "PASS", "Four PNGs are 2665-2850 by 2433 pixels with nonwhite fractions 0.261-0.495."),
        ],
    },
    {
        "basic": 38,
        "specialized": 58,
        "basic_dims": "Correctness 10/10; Reliability/clarity 9/10; Efficiency 9/10; Scope/safety 10/10",
        "spec_dims": "Method validity 20/20; Code 15/15; QC 9/10; Reproducibility 9/10; Security 5/5",
        "note": "All five Python layouts completed on 100 nodes with finite positions and fixed seeds. The WSL Graphviz route drew all 124 signed directed edges (60 activation, 64 repression); the arrowheads and both colors were visually confirmed.",
        "execution_note": "run/run_python_cases.sh and run/run_wsl_directed.sh; logs/python_results.json and logs/wsl_directed_results.json; visually inspected ForceAtlas2 and signed-GRN PNGs.",
        "assertions": [
            assertion("Spring, Kamada-Kawai, circular, spectral, and ForceAtlas2 all produce a nonblank figure", "PASS", "Five PNGs parsed at 1590x1313 with finite layout coordinates."),
            assertion("Stochastic layouts use reproducible seeds", "PASS", "Independent spring-layout reruns at seed 42 were identical."),
            assertion("The signed GRN preserves every directed edge", "PASS", "Instrumented draw calls contained all 124 graph edges."),
            assertion("Activation and repression receive distinct documented colors", "PASS", "60 '+' edges and 64 '-' edges were sent to separate colored draw calls."),
            assertion("The rendered GRN visibly contains arrowheads", "PASS", "Visual inspection confirms directed arrow tips throughout the dot hierarchy."),
        ],
    },
    {
        "basic": 38,
        "specialized": 58,
        "basic_dims": "Correctness 10/10; Reliability/clarity 9/10; Efficiency 9/10; Scope/safety 10/10",
        "spec_dims": "Method validity 20/20; Code 15/15; QC 9/10; Reproducibility 9/10; Security 5/5",
        "note": "The shipped 30-node demonstration completed and its four figures parsed. The legend colors, edge widths, hub emphasis, and one adaptive top-15 label set are correct in every view.",
        "execution_note": "run/audit_python_cases.py input3; output and metrics in logs/python_results.json; inspected the community and confidence files.",
        "assertions": [
            assertion("The shipped demo completes with four static figures", "PASS", "Four PNGs were produced from a 30-node/56-edge deterministic graph."),
            assertion("Community legend colors exactly match the node mapping", "PASS", "Independent palette equality check passed."),
            assertion("Confidence and degree encodings remain present", "PASS", "The confidence and degree views are nonblank and the helper returns bounded widths."),
            assertion("The adaptive label cap is applied consistently to every view", "PASS", "All four views receive the same adaptive label dictionary; the focused regression also proves the contract at N=100."),
            assertion("The demo is deterministic", "PASS", "Graph construction and spring layout both use seed 42."),
        ],
    },
    {
        "basic": 36,
        "specialized": 56,
        "basic_dims": "Correctness 9/10; Reliability/clarity 9/10; Efficiency 8/10; Scope/safety 10/10",
        "spec_dims": "Method validity 19/20; Code 14/15; QC 9/10; Reproducibility 9/10; Security 5/5",
        "note": "The R scripts wrote FR, Kamada-Kawai, circular, and 764-connection bundling PNGs; all parse and are visually correct. Both skill scripts exit 139 only after output because the shared R stack segfaults during package teardown; an independent package-only probe reproduces this, while base R exits 0.",
        "execution_note": "run/run_r_cases.sh plus independent run/run_r_runtime_probe.sh; logs/input4_*.log and logs/r_*probe*.log. All four requested artifacts exist and were visually inspected.",
        "assertions": [
            assertion("All three ggraph layouts contain the complete 100-node network", "PASS", "Each script message reports 100 nodes and each PNG is nonblank."),
            assertion("The hierarchical bundling fixture draws all 764 relations", "PASS", "The script printed 764 bundled connections and the circular bundles are visible."),
            assertion("The R recipes are syntactically complete and execute through ggsave", "PASS", "All ggsave calls completed and wrote parseable PNGs."),
            assertion("The post-output R crash is attributable to the shared package runtime, not skill control flow", "PASS", "A package-only igraph/ggraph/ggplot2 probe exits 139; a base-R probe exits 0."),
            assertion("The stochastic R layout records a fixed seed", "PASS", "ggraph_layouts.R sets seed 42 for every layout."),
        ],
    },
    {
        "basic": 38,
        "specialized": 58,
        "basic_dims": "Correctness 10/10; Reliability/clarity 9/10; Efficiency 9/10; Scope/safety 10/10",
        "spec_dims": "Method validity 20/20; Code 15/15; QC 9/10; Reproducibility 9/10; Security 5/5",
        "note": "Both 100-node PyVis HTML files are self-contained, preserve caller edge attributes, and render the four communities in Chrome. The saved document now contains exactly one heading and one title string.",
        "execution_note": "run/audit_python_cases.py plus run/screenshot_html.py; parsed HTML metrics in logs/python_results.json and screenshot out/input5_pyvis/network_styled_screenshot.png.",
        "assertions": [
            assertion("Basic and styled HTML files are self-contained and browser-renderable", "PASS", "Both exceed 740 KB, inline vis-network assets, and render in Chrome."),
            assertion("The caller graph retains its original edge weights", "PASS", "Deep-copy equality passed after create_interactive_network."),
            assertion("Styled node sizes, colors, and tooltips are present", "PASS", "Rendered communities and degree-sized hubs are visible; sample nodes are serialized."),
            assertion("The HTML presents one clean title", "PASS", "The browser screenshot shows one heading; the generated HTML contains one h1 and one title string."),
            assertion("Physics and interaction controls are available", "PASS", "Navigation controls render and the physics options are serialized."),
        ],
    },
    {
        "basic": 39,
        "specialized": 59,
        "basic_dims": "Correctness 10/10; Reliability/clarity 10/10; Efficiency 9/10; Scope/safety 10/10",
        "spec_dims": "Method validity 20/20; Code 15/15; QC 9/10; Reproducibility 10/10; Security 5/5",
        "note": "A private Cytoscape 3.10.4 process received exactly 100 nodes/511 edges, applied the final style before fitting, expanded the landscape layout, placed the 15 capped labels at distinct perimeter positions with outward anchors, and overwrote valid PNG/PDF exports twice. All 15 labels are individually legible in the original 816x358 export.",
        "execution_note": "run/run_cytoscape.sh -> run/cytoscape_check.py against py4cytoscape 1.13.0; logs/cytoscape_results.json and logs/visual_inspection.md. Private process group 1828921 was stopped, REST port 1234 was confirmed down, and the exact 277,912,361-byte audit-owned home/cache was removed.",
        "assertions": [
            assertion("Cytoscape receives exactly the source graph", "PASS", "Read-back returned 100 nodes and 511 edges."),
            assertion("Degree, label, confidence, and kinase-shape mappings apply", "PASS", "Degrees match NetworkX; 15 display labels are mapped; G000 is DIAMOND, G001 ELLIPSE, and widths span 1.0-3.987."),
            assertion("PNG and PDF exports are nonempty and overwrite safely", "PASS", "Both exports were written twice; PNG is 145,816 bytes and PDF 16,453 bytes."),
            assertion("All 15 intended labels are individually legible in the original-resolution export", "PASS", "Original-resolution inspection read G000, G010, G012, G025, G045, G046, G050, G061, G068, G078, G080, G082, G089, G090, and G099 without clipping or overlap."),
            assertion("Only the audit-owned Cytoscape process is stopped", "PASS", "The saved wrapper used a private setsid process group and confirmed REST down after targeted termination."),
        ],
    },
    {
        "basic": 38,
        "specialized": 58,
        "basic_dims": "Correctness 10/10; Reliability/clarity 9/10; Efficiency 9/10; Scope/safety 10/10",
        "spec_dims": "Method validity 20/20; Code 15/15; QC 9/10; Reproducibility 9/10; Security 5/5",
        "note": "Every advertised route resolves to a shipped file; unsupported HiveNetX, Datashader, and adjustText claims are gone. Same-seed positions are identical, a different seed changes coordinates, and native ForceAtlas2 returns 1,200 finite positions in 3.0 seconds.",
        "execution_note": "run/audit_python_cases.py input7; inventory and layout-artifact assertions in logs/python_results.json.",
        "assertions": [
            assertion("Every capability promised in the description has a shipped executable route", "PASS", "Static, layouts, signed GRN, bundling, PyVis, and Cytoscape files all exist."),
            assertion("Unsupported package promises were removed", "PASS", "HiveNetX, Datashader, and adjustText are absent from SKILL.md."),
            assertion("Same-seed stochastic layouts are reproducible", "PASS", "Maximum coordinate delta at seed 42 is 0."),
            assertion("Different seeds change drawing coordinates", "PASS", "Maximum coordinate delta between seeds 42 and 43 is 1.802."),
            assertion("The skill explicitly warns that layout is not biology", "PASS", "The central constraint and condition-comparison sections state this directly."),
        ],
    },
    {
        "basic": 35,
        "specialized": 55,
        "basic_dims": "Correctness 9/10; Reliability/clarity 9/10; Efficiency 7/10; Scope/safety 10/10",
        "spec_dims": "Method validity 18/20; Code 14/15; QC 9/10; Reproducibility 9/10; Security 5/5",
        "note": "The static CLI handles an unweighted disconnected graph and two isolates, widths default to 2.25, and the shared union layout covers both conditions. The layout CLI rejects an empty graph with a clear error and renders a singleton; one isolate is visually crowded under the legend.",
        "execution_note": "run/audit_python_cases.py input8; awkward-graph outputs in out/input8_awkward and logs/python_results.json.",
        "assertions": [
            assertion("Unweighted edges do not raise KeyError and receive visible widths", "PASS", "All three edges receive width 2.25."),
            assertion("Disconnected components and isolates remain in the output", "PASS", "The 6-node graph completes and the figure preserves the components; one isolate is partially under the legend."),
            assertion("Empty input is rejected explicitly", "PASS", "layouts.py exits 1 with 'The input graph is empty'."),
            assertion("Singleton input produces finite nonblank layouts", "PASS", "Spring and circular singleton PNGs parse and exceed 18 KB."),
            assertion("One union layout covers both condition networks", "PASS", "Both node sets are subsets of the one seed-42 union coordinate map."),
        ],
    },
    {
        "basic": 38,
        "specialized": 58,
        "basic_dims": "Correctness 10/10; Reliability/clarity 9/10; Efficiency 9/10; Scope/safety 10/10",
        "spec_dims": "Method validity 20/20; Code 15/15; QC 9/10; Reproducibility 9/10; Security 5/5",
        "note": "The directed-GraphML PyVis CLI probe exits 0, reports 65 nodes/124 edges/3 communities, writes two self-contained HTML files with one title each, and visibly renders direction arrowheads and all four regulator hubs.",
        "execution_note": "run/audit_python_cases.py input9 plus run/screenshot_html.py; HTML and screenshot evidence under out/input9_directed_pyvis.",
        "assertions": [
            assertion("The directed CLI exits successfully", "PASS", "Return code 0 with final network/community summary."),
            assertion("Both directed HTML files preserve all nodes and edges", "PASS", "65 nodes and 124 edges are reported; representative node IDs are serialized."),
            assertion("Direction is preserved in HTML", "PASS", "Both files contain arrow-to serialization and Chrome visibly shows arrowheads."),
            assertion("The styled route computes communities without rejecting a DiGraph", "PASS", "It reports three communities and completes."),
            assertion("The HTML is self-contained and browser-renderable", "PASS", "Both files exceed 715 KB and rendered without external assets."),
        ],
    },
    {
        "basic": 38,
        "specialized": 58,
        "basic_dims": "Correctness 10/10; Reliability/clarity 9/10; Efficiency 9/10; Scope/safety 10/10",
        "spec_dims": "Method validity 20/20; Code 15/15; QC 9/10; Reproducibility 9/10; Security 5/5",
        "note": "The normalized 5-node/4-edge arrow plot remains correct (2 activation, 2 repression), and the changed renderer now rejects explicit natural-language sign values before Graphviz can produce a misleading node-only figure.",
        "execution_note": "run/run_wsl_directed.sh instruments raw and normalized sign values; results in logs/wsl_directed_results.json. Both PNGs were opened side by side.",
        "assertions": [
            assertion("Natural-language sign values can be normalized to the documented plus/minus contract", "PASS", "The audit mapping converts activation to '+' and repression to '-'."),
            assertion("The normalized plot draws every source edge", "PASS", "Instrumented draw calls contain all 4 edges, split 2/2 by sign."),
            assertion("The normalized plot visibly shows arrowheads and both colors", "PASS", "Visual inspection confirms four directed colored edges."),
            assertion("The script rejects or reports unrecognized sign values instead of silently dropping edges", "PASS", "The validator raises a ValueError naming activation/repression before layout; the targeted inhibition probe independently confirms Graphviz is not called."),
            assertion("The output is reproducible", "PASS", "Graphviz dot and the explicit normalization mapping are deterministic."),
        ],
    },
    {
        "basic": 39,
        "specialized": 59,
        "basic_dims": "Correctness 10/10; Reliability/clarity 10/10; Efficiency 9/10; Scope/safety 10/10",
        "spec_dims": "Method validity 20/20; Code 15/15; QC 9/10; Reproducibility 10/10; Security 5/5",
        "note": "A new 61-node graph rendered four nonblank static panels with one identical 16-node label dictionary: the adaptive top 15 plus requested low-degree node R016. The PyVis output has one HTML-escaped heading.",
        "execution_note": "run/run_targeted_round2.sh -> run/targeted_round2_cases.py; exact counts in logs/round2_targeted_results.json; visually inspected out/input11_requested_labels/network_communities.png.",
        "assertions": [
            assertion("The requested low-degree node is retained in addition to the adaptive ranked set", "PASS", "R016 is absent from the rank-only set but present in the 16-node requested set."),
            assertion("Every static view uses exactly the same label dictionary", "PASS", "All four intercepted draw calls received the identical 16-node mapping."),
            assertion("All four static outputs are parseable and nonblank", "PASS", "The PNGs are 2705-2850 by 2433 pixels, 0.107-0.224 nonwhite, and each exceeds 0.84 MB."),
            assertion("The PyVis heading is emitted once and safely escaped", "PASS", "The 718,473-byte HTML has one h1, one escaped title, and no raw angle-bracket title."),
            assertion("The rendered labels are visually legible", "PASS", "The opened community panel shows the requested R016 and ranked labels at readable size without labeling all 61 nodes."),
        ],
    },
    {
        "basic": 39,
        "specialized": 58,
        "basic_dims": "Correctness 10/10; Reliability/clarity 10/10; Efficiency 9/10; Scope/safety 10/10",
        "spec_dims": "Method validity 20/20; Code 15/15; QC 9/10; Reproducibility 9/10; Security 5/5",
        "note": "An adversarial sign value is rejected before Graphviz layout and writes no figure. A 2,000-node path graph receives the documented 30-label cap, and mocked py4cytoscape calls prove the complete layout-style-scale-position-anchor-fit order.",
        "execution_note": "run/run_targeted_round2.sh -> run/targeted_round2_cases.py; logs/round2_targeted_results.json records sign rejection, graphviz_called false, 2,000 nodes, 30 labels, and the round-three call order.",
        "assertions": [
            assertion("An unknown explicit sign is rejected with the value named", "PASS", "ValueError names inhibition and explains the required plus/minus normalization."),
            assertion("Validation happens before Graphviz and leaves no output artifact", "PASS", "The forbidden layout hook was not called and input12_should_not_exist.png is absent."),
            assertion("The large Cytoscape handoff caps labels at 30", "PASS", "Exactly 30 of 2,000 display_label values are nonempty."),
            assertion("Cytoscape receives the display-label mapping", "PASS", "set_node_label_mapping is called once with display_label and PPIStyle."),
            assertion("Final fitting follows layout, styling, scaling, perimeter placement, and label anchoring", "PASS", "Recorded order is layout, style, x-scale 2.4, 30 node-position bypasses, 30 label-position bypasses, then fit."),
        ],
    },
    {
        "basic": 39,
        "specialized": 59,
        "basic_dims": "Correctness 10/10; Reliability/clarity 10/10; Efficiency 9/10; Scope/safety 10/10",
        "spec_dims": "Method validity 20/20; Code 15/15; QC 9/10; Reproducibility 10/10; Security 5/5",
        "note": "Basic and styled directed PyVis documents safely escaped a hostile closing-heading/script title, preserved all six caller edges and weights, serialized direction, retained Unicode node identifiers, and rendered the title as inert text in Chrome.",
        "execution_note": "run/run_fresh_final_cases.sh -> run/fresh_final_cases.py plus run/run_checks.sh; logs/fresh_final_results.json and out/input13_adversarial_html/styled_screenshot.png.",
        "assertions": [
            assertion("The hostile title cannot terminate the heading or execute a script", "PASS", "Both HTML files contain the escaped title, one h1, and no raw injected script element."),
            assertion("The caller graph and all edge weights remain unchanged", "PASS", "A deep-copy equality check passed after both PyVis render paths."),
            assertion("Direction is preserved for every edge", "PASS", "Both HTML files serialize arrows-to and the Chrome screenshot shows all six arrowheads."),
            assertion("Unicode and path-like node identifiers survive serialization", "PASS", "β-catenin renders correctly; all six identifiers are present as raw or JSON-escaped values."),
            assertion("Constant edge weights receive a visible fallback width", "PASS", "All six equal-weight edges map to the documented mid-range width 2.25."),
        ],
    },
    {
        "basic": 38,
        "specialized": 57,
        "basic_dims": "Correctness 10/10; Reliability/clarity 9/10; Efficiency 9/10; Scope/safety 10/10",
        "spec_dims": "Method validity 19/20; Code 15/15; QC 9/10; Reproducibility 9/10; Security 5/5",
        "note": "A fresh 501-node/1,494-edge scale-free PPI completed the native ForceAtlas2 route immediately above the decision-tree boundary. All coordinates are finite, same-seed reruns are identical, the figure is nonblank, and exactly 15 adaptive labels are used.",
        "execution_note": "run/run_fresh_final_cases.sh -> run/fresh_final_cases.py; logs/fresh_final_results.json and original-resolution inspection of out/input14_forceatlas_boundary/forceatlas2.png.",
        "assertions": [
            assertion("Native ForceAtlas2 covers all 501 graph nodes", "PASS", "The position mapping contains exactly 501 entries for the 501-node fixture."),
            assertion("Every ForceAtlas2 coordinate is finite", "PASS", "The independent NumPy finiteness check passed for the complete coordinate matrix."),
            assertion("The stochastic layout is reproducible at the documented seed", "PASS", "Two seed-42 computations have maximum coordinate delta 0."),
            assertion("Only the documented adaptive capped subset is labelled", "PASS", "The intercepted draw call contains exactly 15 labels."),
            assertion("The boundary figure is a parseable nonblank artifact", "PASS", "The 1590x1313 PNG is 774,062 bytes with nonwhite fraction 0.353139."),
        ],
    },
]

inputs: list[dict[str, object]] = []
for prompt, score in zip(manifest, scores, strict=True):
    assertions = score["assertions"]
    passed = sum(item["result"] == "PASS" for item in assertions)
    total = score["basic"] + score["specialized"]
    inputs.append(
        {
            "index": prompt["index"],
            "type": prompt["type"],
            "label": prompt["label"],
            "status": "COMPLETED",
            "status_flag": "✅",
            "note": score["note"],
            "executed": True,
            "execution_note": score["execution_note"],
            "basic": score["basic"],
            "specialized": score["specialized"],
            "total": total,
            "assertions_passed": passed,
            "assertions_total": len(assertions),
            "assertions": assertions,
        }
    )

execution_avg = round(sum(item["total"] for item in inputs) / len(inputs), 1)
assertions_passed = sum(item["assertions_passed"] for item in inputs)
assertions_total = sum(item["assertions_total"] for item in inputs)

report = {
    "meta": {
        "skill_name": "bio-data-visualization-network-visualization",
        "description": "Visualize biological networks (PPI, gene-regulatory, co-expression, pathway) with reproducible NetworkX layouts, degree and community encodings, signed directed edges, R hierarchical edge bundling, PyVis HTML, and Cytoscape automation. Use for static publication figures, interactive exploration, or Cytoscape export.",
        "evaluated_on": "2026-09-27",
        "evaluator_version": "skill-auditor@1.0",
        "category": "Data Analysis",
        "execution_mode": "D",
        "complexity": "Complex",
        "n_inputs": 14,
        "source": "mrsonord2240/optimized-scientific-skills@e75b079fdd97b9186aabc46bda2e5ecaedd74d1c:skills/bio-data-visualization-network-visualization",
        "audit_type": "independent final fixed-commit re-audit: all twelve prior inputs plus two fresh inputs",
        "auditor_independent": True,
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
            "scientific_integrity": {"result": "PASS", "detail": "No invented biological results, citations, or statistical values appear in any output."},
            "practice_boundaries": {"result": "PASS", "detail": "Outputs are network-visualization artifacts and make no diagnosis, prescription, or individual medical recommendation."},
            "methodological_ground": {"result": "PASS", "detail": "The skill explicitly separates force-directed drawing coordinates from biological measurements and requires one union layout for condition comparisons."},
            "code_usability": {"result": "PASS", "detail": "All advertised Python, R, Graphviz, PyVis, and live Cytoscape routes executed and produced checked artifacts. The R process exits 139 only during shared-package teardown, independently reproduced by a package-only probe after successful output."},
        },
    },
    "static_score": {
        "subtotal": 98,
        "max": 100,
        "categories": {
            "functional_suitability": {"score": 12, "max": 12, "note": "All promised routes execute correctly, including a live publication-readable Cytoscape export of the exact 100-node/511-edge fixture."},
            "reliability": {"score": 12, "max": 12, "note": "Unknown sign values fail before layout, reruns overwrite exports safely, and edge/input boundary cases surface explicit errors."},
            "performance_context": {"score": 7, "max": 8, "note": "The concise main file uses focused references and scripts; the four-panel static demonstration remains intentionally heavier than a single requested figure."},
            "agent_usability": {"score": 16, "max": 16, "note": "Decision tree, failure modes, complete commands, output checks, and the deterministic Cytoscape label-placement sequence are explicit."},
            "human_usability": {"score": 8, "max": 8, "note": "Natural prompts, GraphML support, repeatable requested labels, browser controls, and actionable validation errors are provided."},
            "security": {"score": 12, "max": 12, "note": "No secrets, dynamic code execution, exfiltration, unsafe shell construction, or destructive file behavior is present."},
            "maintainability": {"score": 12, "max": 12, "note": "Responsibilities are split across focused scripts and references, with deterministic regression coverage for every repaired contract."},
            "agent_specific": {"score": 19, "max": 20, "note": "Triggering, progressive disclosure, composable CLIs, explicit output paths, and stop conditions are strong; Cytoscape necessarily creates desktop-session state."},
        },
    },
    "dynamic_score": {
        "execution_avg": execution_avg,
        "max": 100,
        "assertion_pass_rate": {"passed": assertions_passed, "total": assertions_total},
        "inputs": inputs,
    },
    "final": {
        "static_weighted": 39.2,
        "dynamic_weighted": round(execution_avg * 0.6, 1),
        "score": 97,
        "max": 100,
        "grade": "Production Ready",
        "grade_symbol": "⭐",
        "deployable": True,
        "veto_override": False,
    },
    "key_strengths": [
        "Every advertised route has a shipped executable path and all fourteen audit inputs produced checked outputs.",
        "Force-directed interpretation guidance is scientifically explicit and condition comparisons reuse one layout.",
        "Community palettes, adaptive and requested labels, PyVis mutation/direction/title handling, and sign-domain validation are independently verified.",
        "Signed directed Graphviz output preserves all 124 edges with visible arrows and separate activation/repression colors.",
        "Cytoscape automation surfaces failures, applies the final style before fitting, places capped labels deterministically at distinct perimeter positions, and exports safely.",
    ],
    "recommendations": [],
}


# Strict pre-emit validation, including the final re-audit N=14 extension.
assert set(report) == {"meta", "veto_gates", "static_score", "dynamic_score", "final", "key_strengths", "recommendations"}
categories = report["static_score"]["categories"]
assert set(categories) == {"functional_suitability", "reliability", "performance_context", "agent_usability", "human_usability", "security", "maintainability", "agent_specific"}
assert sum(item["score"] for item in categories.values()) == report["static_score"]["subtotal"]
assert len(inputs) == report["meta"]["n_inputs"] == 14
assert all(3 <= len(item["assertions"]) <= 5 for item in inputs)
assert all(item["assertions_passed"] == sum(a["result"] == "PASS" for a in item["assertions"]) for item in inputs)
assert all(item["basic"] + item["specialized"] == item["total"] for item in inputs)
assert execution_avg == 95.7
assert assertions_passed == 70 and assertions_total == 70
assert report["final"]["static_weighted"] == 39.2
assert report["final"]["dynamic_weighted"] == 57.4
assert round(report["final"]["static_weighted"] + report["final"]["dynamic_weighted"]) == report["final"]["score"]
assert 2 <= len(report["key_strengths"]) <= 5
assert report["recommendations"] == []
assert report["veto_gates"]["skill_veto"]["gate"] == "PASS"
assert report["veto_gates"]["research_veto"]["gate"] == "PASS"

json_path = ROOT / "eval_report_bio-data-visualization-network-visualization_result.json"
json_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

lines = [
    "# Eval Viewer — bio-data-visualization-network-visualization",
    "",
    "Generated: 2026-09-27",
    "",
    f"- Source: `{report['meta']['source']}`",
    "- Independent re-auditor: **true**",
    "- Category: Data Analysis; execution mode: D (Hybrid); complexity: Complex",
    "- Re-audit size: **14 inputs** = all 12 prior-audit inputs rerun as regressions + 2 genuinely fresh final-pass inputs. This explicit re-audit mandate extends the generic schema's older 8-input enumeration.",
    "- Result: **97/100, ⭐ Production Ready, deployable true**; no veto fired; open findings P0/P1/P2 = **0/0/0**.",
    "",
    "## Summary Table",
    "",
    "| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |",
    "|---|---|---:|---:|---:|---:|---|",
]
for item in inputs:
    lines.append(f"| {item['index']} | {item['type']} | {item['basic']} | {item['specialized']} | {item['total']} | {item['assertions_passed']}/{item['assertions_total']} | {item['status_flag']} {item['status']} |")
lines += [
    "",
    f"**Execution average:** {execution_avg}/100  ",
    f"**Layer 1 average:** {sum(i['basic'] for i in inputs)/len(inputs):.1f}/40  ",
    f"**Layer 2 average:** {sum(i['specialized'] for i in inputs)/len(inputs):.1f}/60  ",
    f"**Assertion pass rate:** {assertions_passed}/{assertions_total} ({assertions_passed/assertions_total:.0%})",
    "",
    "## Veto Gates",
    "",
    "| Gate | Result | Evidence |",
    "|---|---|---|",
    "| T1 Operational stability | PASS | All routes produced checked outputs. The R 139 teardown is independently reproduced by loading the shared package stack without skill code. |",
    "| T2 Structural contract | PASS | Required frontmatter and all referenced files are present. |",
    "| T3 Determinism | PASS | Python and R stochastic layouts use seed 42; same-seed coordinates match. |",
    "| T4 Security | PASS | No eval/exec of user strings, credentials, exfiltration, or destructive commands. |",
    "| M1 Scientific integrity | PASS | No invented claims or statistics. |",
    "| M2 Practice boundaries | PASS | Visualization only; no individual diagnosis or treatment. |",
    "| M3 Methodological baseline | PASS | Layout coordinates are explicitly not biological measurements. |",
    "| M4 Code usability | PASS | Python, R, Graphviz, PyVis, and Cytoscape paths all executed and outputs were checked. |",
    "",
    "## Static Evaluation — 98/100",
    "",
    "| Category | Score | Note |",
    "|---|---:|---|",
]
for key, item in categories.items():
    lines.append(f"| {key.replace('_', ' ').title()} | {item['score']}/{item['max']} | {item['note']} |")
lines += [
    "",
    "## Execution Method and Environment",
    "",
    "The immutable provider checkout was copied byte-for-byte to `run/skill`; execution occurred only from that copy. Python used the data-visualization `py.sh` environment (networkx 3.6.1, matplotlib 3.11.2, pyvis 0.3.2). R used `r.sh` (R 4.4.3, igraph 2.3.0, ggraph 2.2.2, ggplot2 4.0.3). Graphviz and py4cytoscape ran in WSL `dv-cli`; a private Cytoscape 3.10.4/Xvfb process group was started and stopped by `run/run_cytoscape.sh`.",
    "",
    "The shared R package stack segfaults at interpreter teardown: the saved package-only probe reproduces status 139 after printing its completion line, while a base-R probe returns 0. The skill scripts completed `ggsave`, printed all expected counts, and their PNGs parse and were opened. This environment defect is recorded but not attributed to the skill.",
    "",
    "Representative saved commands:",
    "",
    "```text",
    "run/run_python_cases.sh      # fixtures plus Python regressions",
    "run/run_r_cases.sh           # ggraph layouts and edge bundling",
    "run/run_wsl_directed.sh      # signed Graphviz and sign-domain probe",
    "run/run_cytoscape.sh         # private live Cytoscape run",
    "run/run_checks.sh            # raster/PDF/HTML checks and Chrome screenshots",
    "run/run_skill_tests.sh       # shipped focused regression tests",
    "run/run_targeted_round2.sh   # two new label/sign/Cytoscape contract inputs",
    "run/run_fresh_final_cases.sh # hostile-title and 501-node fresh inputs",
    "```",
    "",
    "Key printed evidence:",
    "",
    "```text",
    "Static PPI: Network: 100 nodes, 511 edges; Communities: 4",
    "Layouts: spring/kamada-kawai/circular/spectral/forceatlas2: 100 finite positions each",
    "Signed GRN: 65 nodes, 124 edges; draw split [60, 64]",
    "R layouts: fr/kk/circle: 100 nodes; bundling: 764 connections",
    "PyVis directed: 65 nodes, 124 edges, 3 communities; return code 0",
    "Cytoscape 3.10.4 / py4cytoscape 1.13.0: 100 nodes, 511 edges; 15 distinct legible labels at 18 pt; layout span 1458.286 x 769.940",
    "Round-two regressions: 61-node requested label retained; 2,000-node cap=30; unknown sign rejected before layout",
    "Fresh cases: hostile title escaped; Unicode preserved; 501 ForceAtlas2 positions finite and deterministic",
    "Artifact checker: 43 PNG/PDF/HTML artifacts parsed and nonblank",
    "Shipped tests: PASS: adaptive labels, sign validation, PyVis heading, Cytoscape labels",
    "```",
    "",
    "## Detailed Outputs",
]
for prompt, item, score in zip(manifest, inputs, scores, strict=True):
    lines += [
        "",
        f"### Input {item['index']} — {prompt['type']}: {prompt['label']}",
        "",
        f"**Prompt:** {prompt['prompt']}",
        "",
        f"**Regression source:** {'Pre-fix input ' + str(prompt['regression_of']) if prompt['regression_of'] else 'New independent input'}",
        "",
        f"**Output and execution:** {item['note']}",
        "",
        f"**Evidence:** {item['execution_note']}",
        "",
        f"**Scores:** Basic {item['basic']}/40 ({score['basic_dims']}); Specialized {item['specialized']}/60 ({score['spec_dims']}); Total {item['total']}/100.",
        "",
        "**Assertions:**",
        "",
    ]
    for check in item["assertions"]:
        lines.append(f"- [{check['result']}] {check['text']} — {check['note']}")

lines += [
    "",
    "## Visual Inspection",
    "",
    "Opened and inspected at original resolution: canonical community view, both ForceAtlas2 sizes, signed Graphviz GRN, R FR, R edge bundling, awkward disconnected graph, normalized sign plot, three PyVis Chrome screenshots, the 61-node requested-label panel, and the live Cytoscape PNG. In the exact 816x358 Cytoscape export, all 15 intended labels were individually read and none is clipped, covered, or merged; see logs/visual_inspection.md.",
    "",
    "## Recommendations",
    "",
]
for rec in report["recommendations"]:
    lines += [
        f"### [{rec['priority']}] {rec['title']}",
        "",
        f"- Observed in: {rec['observed_in']}",
        f"- Problem: {rec['problem']}",
        f"- Root cause: {rec['root_cause']}",
        f"- Fix: {rec['fix']}",
        "",
    ]
if not report["recommendations"]:
    lines += ["No open P0, P1, or P2 findings.", ""]
lines += [
    "## Final Score and Floors",
    "",
    "| Component | Result | Production floor |",
    "|---|---:|---:|",
    "| Static | 98/100 | >=80 |",
    "| Execution average | 95.7/100 | >=85 |",
    "| Layer 1 average | 37.9/40 | >=32 |",
    "| Layer 2 average | 57.8/60 | >=48 |",
    "| Assertions | 70/70 = 100% | >=90% |",
    "| Vetoes | none | none |",
    "",
    "Final = 98×0.4 + 95.7×0.6 = 96.6, rounded to **97/100**. Grade: **⭐ Production Ready**. Deployable: **true**. Open P0/P1/P2: **0/0/0**.",
    "",
    "## Housekeeping",
    "",
    "The live audit folder contains only scripts, fixtures, logs, reports, and result artifacts. The exact task-created Cytoscape home/cache (1,028 files; 277,912,361 bytes) was deleted by run/cleanup_disposable.ps1 after the private process group stopped; REST port 1234 remains down. Generated bytecode caches are absent from run/. logs/provenance.json verifies immutable commit e75b079f, a clean audited skill subtree, a byte-identical execution copy, and no source or run __pycache__. No provider or records bytes were modified.",
]

viewer_path = ROOT / "eval_viewer_bio-data-visualization-network-visualization.md"
viewer_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
print(json_path)
print(viewer_path)
print("final", report["final"])
print("executed", sum(i["executed"] for i in inputs), "/", len(inputs))
print("assertions", assertions_passed, "/", assertions_total)
