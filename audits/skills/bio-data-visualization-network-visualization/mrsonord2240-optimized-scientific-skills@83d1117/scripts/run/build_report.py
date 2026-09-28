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
        "basic": 32,
        "specialized": 52,
        "basic_dims": "Correctness 7/10; Reliability/clarity 7/10; Efficiency 8/10; Scope/safety 10/10",
        "spec_dims": "Method validity 17/20; Code 13/15; QC 8/10; Reproducibility 9/10; Security 5/5",
        "note": "Executed the copied static CLI on the synthetic 100-node/511-edge PPI. Four parseable nonblank PNGs were produced; widths span 0.5-4.0 and legend swatches exactly match node colors. Visual inspection found that three views label all 100 nodes instead of the promised capped subset.",
        "execution_note": "run/run_python_cases.sh -> run/audit_python_cases.py; output metrics in logs/python_results.json and logs/artifact_metrics.json; visually inspected out/input1_static_ppi/network_communities.png.",
        "assertions": [
            assertion("All 100 nodes and 511 edges are represented in the static workflow", "PASS", "The CLI printed 100 nodes and 511 edges; image collections and the source graph agree."),
            assertion("Community nodes and legend swatches use one identical discrete palette", "PASS", "Independent RGBA equality check passed for all nodes."),
            assertion("Edge widths are bounded in the documented 0.5-4 point range", "PASS", "Observed minimum 0.5 and maximum 4.0."),
            assertion("Static views label only the documented adaptive capped subset", "FAIL", "Degree, community, and confidence views call draw_networkx_labels for every node; the 100-node image is visibly crowded."),
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
        "basic": 36,
        "specialized": 56,
        "basic_dims": "Correctness 9/10; Reliability/clarity 8/10; Efficiency 9/10; Scope/safety 10/10",
        "spec_dims": "Method validity 18/20; Code 15/15; QC 9/10; Reproducibility 9/10; Security 5/5",
        "note": "The shipped 30-node demonstration completed and its four figures parsed. The original legend-color regression is fixed, edge widths are visible, and hub highlighting works; however three views still label all 30 nodes instead of the documented adaptive top 15.",
        "execution_note": "run/audit_python_cases.py input3; output and metrics in logs/python_results.json; inspected the community and confidence files.",
        "assertions": [
            assertion("The shipped demo completes with four static figures", "PASS", "Four PNGs were produced from a 30-node/56-edge deterministic graph."),
            assertion("Community legend colors exactly match the node mapping", "PASS", "Independent palette equality check passed."),
            assertion("Confidence and degree encodings remain present", "PASS", "The confidence and degree views are nonblank and the helper returns bounded widths."),
            assertion("The adaptive label cap is applied consistently to every view", "FAIL", "Three views label all 30 nodes although the documented cap is 15 for N=30."),
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
        "basic": 35,
        "specialized": 55,
        "basic_dims": "Correctness 9/10; Reliability/clarity 8/10; Efficiency 8/10; Scope/safety 10/10",
        "spec_dims": "Method validity 18/20; Code 14/15; QC 9/10; Reproducibility 9/10; Security 5/5",
        "note": "Both 100-node PyVis HTML files are self-contained, preserve caller edge attributes, and render the four communities in Chrome. The browser screenshot shows the title duplicated on consecutive lines.",
        "execution_note": "run/audit_python_cases.py plus run/screenshot_html.py; parsed HTML metrics in logs/python_results.json and screenshot out/input5_pyvis/network_styled_screenshot.png.",
        "assertions": [
            assertion("Basic and styled HTML files are self-contained and browser-renderable", "PASS", "Both exceed 740 KB, inline vis-network assets, and render in Chrome."),
            assertion("The caller graph retains its original edge weights", "PASS", "Deep-copy equality passed after create_interactive_network."),
            assertion("Styled node sizes, colors, and tooltips are present", "PASS", "Rendered communities and degree-sized hubs are visible; sample nodes are serialized."),
            assertion("The HTML presents one clean title", "FAIL", "Chrome shows 'PPI Network with Communities' twice; the string occurs in two h1 elements."),
            assertion("Physics and interaction controls are available", "PASS", "Navigation controls render and the physics options are serialized."),
        ],
    },
    {
        "basic": 32,
        "specialized": 52,
        "basic_dims": "Correctness 8/10; Reliability/clarity 6/10; Efficiency 8/10; Scope/safety 10/10",
        "spec_dims": "Method validity 17/20; Code 14/15; QC 8/10; Reproducibility 8/10; Security 5/5",
        "note": "A private Cytoscape 3.10.4 process received exactly 100 nodes/511 edges, mapped degree and gene type correctly, and overwrote valid PNG/PDF exports twice. The visual export is a dense unlabeled cluster, below the example's 'publication-quality' claim.",
        "execution_note": "run/run_cytoscape.sh -> run/cytoscape_check.py against py4cytoscape 1.13.0. Process group 1815839 was stopped and REST port 1234 confirmed down. Results in logs/cytoscape_results.json.",
        "assertions": [
            assertion("Cytoscape receives exactly the source graph", "PASS", "Read-back returned 100 nodes and 511 edges."),
            assertion("Degree, confidence, and kinase-shape mappings apply", "PASS", "Degrees match NetworkX; G000 is DIAMOND, G001 ELLIPSE, widths span 1.0-3.987."),
            assertion("PNG and PDF exports are nonempty and overwrite safely", "PASS", "Both exports were written twice; PNG is 42,325 bytes and PDF 15,850 bytes."),
            assertion("The exported figure is publication-readable without manual restyling", "FAIL", "Visual inspection shows an unlabeled force-directed clump; nodes cannot be identified."),
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
        "basic": 37,
        "specialized": 57,
        "basic_dims": "Correctness 10/10; Reliability/clarity 9/10; Efficiency 8/10; Scope/safety 10/10",
        "spec_dims": "Method validity 20/20; Code 15/15; QC 9/10; Reproducibility 8/10; Security 5/5",
        "note": "The new directed-GraphML PyVis CLI probe exits 0, reports 65 nodes/124 edges/3 communities, and writes two self-contained HTML files. Chrome visibly renders direction arrowheads and all four regulator hubs.",
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
        "basic": 32,
        "specialized": 49,
        "basic_dims": "Correctness 8/10; Reliability/clarity 8/10; Efficiency 6/10; Scope/safety 10/10",
        "spec_dims": "Method validity 16/20; Code 12/15; QC 8/10; Reproducibility 8/10; Security 5/5",
        "note": "Following the reference instruction to normalize noncanonical signs produces a correct 5-node/4-edge arrow plot (2 activation, 2 repression). Directly passing 'activation'/'repression' draws zero edges yet exits successfully, so the recipe lacks a guard against silent data loss.",
        "execution_note": "run/run_wsl_directed.sh instruments raw and normalized sign values; results in logs/wsl_directed_results.json. Both PNGs were opened side by side.",
        "assertions": [
            assertion("Natural-language sign values can be normalized to the documented plus/minus contract", "PASS", "The audit mapping converts activation to '+' and repression to '-'."),
            assertion("The normalized plot draws every source edge", "PASS", "Instrumented draw calls contain all 4 edges, split 2/2 by sign."),
            assertion("The normalized plot visibly shows arrowheads and both colors", "PASS", "Visual inspection confirms four directed colored edges."),
            assertion("The script rejects or reports unrecognized sign values instead of silently dropping edges", "FAIL", "The raw run reports 4 graph edges but sends 0 edges to draw calls and still writes a PNG."),
            assertion("The output is reproducible", "PASS", "Graphviz dot and the explicit normalization mapping are deterministic."),
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
        "n_inputs": 10,
        "source": "mrsonord2240/optimized-scientific-skills@83d111751e849f11ad443491fade222c868c0f63:skills/bio-data-visualization-network-visualization",
        "audit_type": "independent fixed-commit re-audit: eight pre-fix regressions plus two new inputs",
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
        "subtotal": 90,
        "max": 100,
        "categories": {
            "functional_suitability": {"score": 10, "max": 12, "note": "Promised routes are present and correct; static labels and sign-domain validation remain incomplete."},
            "reliability": {"score": 10, "max": 12, "note": "Errors surface and workflows are rerunnable, but unknown sign values are silently dropped."},
            "performance_context": {"score": 7, "max": 8, "note": "The 207-line main file uses focused references and scripts; the four-view static route remains heavier than necessary."},
            "agent_usability": {"score": 15, "max": 16, "note": "Decision tree, failure modes, commands, and output expectations are clear; one documented label rule is not implemented in the canonical example."},
            "human_usability": {"score": 7, "max": 8, "note": "Natural prompts and broad GraphML support; sign normalization is documented but not enforced."},
            "security": {"score": 11, "max": 12, "note": "No secrets, eval, network exfiltration, or destructive operations; graph attribute domains receive only partial validation."},
            "maintainability": {"score": 11, "max": 12, "note": "Clean modular split and focused tests; tests do not cover all-node labels, unknown signs, duplicate titles, or Cytoscape legibility."},
            "agent_specific": {"score": 19, "max": 20, "note": "Precise trigger, progressive disclosure, composable CLIs, explicit paths, and stop conditions; Cytoscape reruns create an additional network in the desktop session."},
        },
    },
    "dynamic_score": {
        "execution_avg": execution_avg,
        "max": 100,
        "assertion_pass_rate": {"passed": assertions_passed, "total": assertions_total},
        "inputs": inputs,
    },
    "final": {
        "static_weighted": 36.0,
        "dynamic_weighted": round(execution_avg * 0.6, 1),
        "score": 90,
        "max": 100,
        "grade": "Production Ready",
        "grade_symbol": "⭐",
        "deployable": True,
        "veto_override": False,
    },
    "key_strengths": [
        "Every advertised route now has a shipped executable path and all ten audit inputs produced checked outputs.",
        "Force-directed interpretation guidance is scientifically explicit and condition comparisons reuse one layout.",
        "The original community-palette, PyVis mutation/direction, and Cytoscape mapping/export regressions are fixed.",
        "Signed directed Graphviz output preserves all 124 edges with visible arrows and separate activation/repression colors.",
        "Cytoscape automation now surfaces failures, applies mappings, uses absolute paths, and overwrites exports safely.",
    ],
    "recommendations": [
        {
            "priority": "P1",
            "title": "Apply the adaptive label cap in every static view",
            "observed_in": [1, 3],
            "problem": "network_plots.py labels every node in the degree, community, and confidence figures. The 100-node canonical output is visibly crowded and contradicts the core workflow and quantitative top-k rule.",
            "root_cause": "Three render branches pass the full graph to draw_networkx_labels; only the separate hub figure uses a ranked subset.",
            "fix": "Compute the documented adaptive top-k set once and pass its label dictionary to all four static views, while retaining optional user-specified genes of interest.",
        },
        {
            "priority": "P2",
            "title": "Reject unknown regulatory sign values",
            "observed_in": [10],
            "problem": "The directed renderer silently draws zero edges when a sign column contains activation/repression rather than '+'/'-', yet exits successfully and writes a plausible node-only PNG.",
            "root_cause": "The loop draws only two recognized values and never checks whether their union equals the graph edge set.",
            "fix": "Validate the sign domain before layout, list unknown values in a ValueError, and optionally accept an explicit activation/repression mapping flag.",
        },
        {
            "priority": "P2",
            "title": "Make the Cytoscape export readable by default",
            "observed_in": [6],
            "problem": "The live PNG is a dense unlabeled cluster, so the example does not meet its own publication-quality claim without manual Cytoscape work.",
            "root_cause": "The style sets label font size but does not map node names to NODE_LABEL or fit/space labels after the force-directed layout.",
            "fix": "Populate and map an explicit label column, fit content after layout, and document when to suppress labels for large networks.",
        },
        {
            "priority": "P2",
            "title": "Remove duplicated PyVis headings",
            "observed_in": [5, 9],
            "problem": "Both browser-rendered styled HTML pages show the title twice on consecutive lines.",
            "root_cause": "With pyvis 0.3.2 the supplied heading is emitted in two h1 elements by the active template path.",
            "fix": "Use a custom template or post-render check that guarantees exactly one h1 title, and add a browser-level regression assertion.",
        },
    ],
}


# Strict pre-emit validation, including the re-audit-mandated N=10 extension.
assert set(report) == {"meta", "veto_gates", "static_score", "dynamic_score", "final", "key_strengths", "recommendations"}
categories = report["static_score"]["categories"]
assert set(categories) == {"functional_suitability", "reliability", "performance_context", "agent_usability", "human_usability", "security", "maintainability", "agent_specific"}
assert sum(item["score"] for item in categories.values()) == report["static_score"]["subtotal"]
assert len(inputs) == report["meta"]["n_inputs"] == 10
assert all(3 <= len(item["assertions"]) <= 5 for item in inputs)
assert all(item["assertions_passed"] == sum(a["result"] == "PASS" for a in item["assertions"]) for item in inputs)
assert all(item["basic"] + item["specialized"] == item["total"] for item in inputs)
assert execution_avg == 89.9
assert assertions_passed == 45 and assertions_total == 50
assert report["final"]["static_weighted"] == 36.0
assert report["final"]["dynamic_weighted"] == 53.9
assert round(report["final"]["static_weighted"] + report["final"]["dynamic_weighted"]) == report["final"]["score"]
assert 2 <= len(report["key_strengths"]) <= 5
assert [item["priority"] for item in report["recommendations"]] == ["P1", "P2", "P2", "P2"]
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
    "- Re-audit size: **10 inputs** = all 8 pre-fix inputs rerun as regressions + 2 genuinely new inputs. This explicit re-audit mandate extends the generic schema's older 8-input enumeration.",
    "- Result: **90/100, ⭐ Production Ready, deployable true**; no veto fired; open findings P0/P1/P2 = **0/1/3**.",
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
    f"**Layer 1 average:** {sum(i['basic'] for i in inputs)/10:.1f}/40  ",
    f"**Layer 2 average:** {sum(i['specialized'] for i in inputs)/10:.1f}/60  ",
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
    "## Static Evaluation — 90/100",
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
    "Cytoscape: 100 nodes, 511 edges; degree_match true; DIAMOND/ELLIPSE; overwrite_twice true",
    "Artifact checker: 35 PNG/PDF/HTML artifacts parsed and nonblank",
    "Shipped tests: PASS: static mapping, unweighted widths, PyVis immutability, directed arrows",
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
    "Opened and inspected: canonical community view, ForceAtlas2, signed Graphviz GRN, R FR, R edge bundling, live Cytoscape PNG, awkward disconnected graph, raw and normalized sign plots, undirected PyVis Chrome screenshot, and directed PyVis Chrome screenshot. The plots are nonblank and mappings are visible. The inspection is the basis for the all-node label, unlabeled Cytoscape, duplicate HTML title, and silent-sign findings.",
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
lines += [
    "## Final Score and Floors",
    "",
    "| Component | Result | Production floor |",
    "|---|---:|---:|",
    "| Static | 90/100 | >=80 |",
    "| Execution average | 89.9/100 | >=85 |",
    "| Layer 1 average | 35.1/40 | >=32 |",
    "| Layer 2 average | 54.8/60 | >=48 |",
    "| Assertions | 45/50 = 90% | >=90% |",
    "| Vetoes | none | none |",
    "",
    "Final = 90×0.4 + 89.9×0.6 = 89.9, rounded to **90/100**. Grade: **⭐ Production Ready**. Deployable: **true**. Open P0/P1/P2: **0/1/3**; open P1 does not block deployability under the audit brief.",
    "",
    "## Housekeeping",
    "",
    "The live audit folder contains only scripts, fixtures, logs, reports, and result artifacts. A task-created Cytoscape home/cache (1,006 files, 277,845,954 bytes) and two generated `__pycache__` directories were moved recoverably to `F:\\OpenScience\\audit-disposable` so the publisher will not copy them. The verified post-cleanup footprint is 104 files / 19.66 MiB total; `run/` is 33 files / 0.11 MiB and contains no vendored package tree. No skill bytes, fix log, provider commit, backlog, branch, or remote were modified.",
]

viewer_path = ROOT / "eval_viewer_bio-data-visualization-network-visualization.md"
viewer_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
print(json_path)
print(viewer_path)
print("final", report["final"])
print("executed", sum(i["executed"] for i in inputs), "/", len(inputs))
print("assertions", assertions_passed, "/", assertions_total)
