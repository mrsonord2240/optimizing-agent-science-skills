> **Audit record for `bio-data-visualization-network-visualization`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/optimized-scientific-skills@8300893](https://github.com/mrsonord2240/optimized-scientific-skills/tree/83008933c5298af81fe4b4604a39b291817bb47f/skills/bio-data-visualization-network-visualization) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-27 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-data-visualization-network-visualization

Generated: 2026-09-27

- Source: `mrsonord2240/optimized-scientific-skills@83008933c5298af81fe4b4604a39b291817bb47f:skills/bio-data-visualization-network-visualization`
- Independent re-auditor: **true**
- Category: Data Analysis; execution mode: D (Hybrid); complexity: Complex
- Re-audit size: **12 inputs** = all 10 prior-audit inputs rerun as regressions + 2 genuinely new round-two inputs. This explicit re-audit mandate extends the generic schema's older 8-input enumeration.
- Result: **95/100, ⭐ Production Ready, deployable true**; no veto fired; open findings P0/P1/P2 = **0/0/1**.

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---:|---:|---:|---:|---|
| 1 | Canonical | 38 | 58 | 96 | 5/5 | ✅ COMPLETED |
| 2 | Variant A | 38 | 58 | 96 | 5/5 | ✅ COMPLETED |
| 3 | Variant B | 38 | 58 | 96 | 5/5 | ✅ COMPLETED |
| 4 | Variant B | 36 | 56 | 92 | 5/5 | ✅ COMPLETED |
| 5 | Edge | 38 | 58 | 96 | 5/5 | ✅ COMPLETED |
| 6 | Stress | 34 | 54 | 88 | 4/5 | ✅ COMPLETED |
| 7 | Scope Boundary | 38 | 58 | 96 | 5/5 | ✅ COMPLETED |
| 8 | Adversarial | 35 | 55 | 90 | 5/5 | ✅ COMPLETED |
| 9 | Variant A | 38 | 58 | 96 | 5/5 | ✅ COMPLETED |
| 10 | Edge | 38 | 58 | 96 | 5/5 | ✅ COMPLETED |
| 11 | Variant B | 39 | 59 | 98 | 5/5 | ✅ COMPLETED |
| 12 | Stress | 38 | 58 | 96 | 5/5 | ✅ COMPLETED |

**Execution average:** 94.7/100  
**Layer 1 average:** 37.3/40  
**Layer 2 average:** 57.3/60  
**Assertion pass rate:** 59/60 (98%)

## Veto Gates

| Gate | Result | Evidence |
|---|---|---|
| T1 Operational stability | PASS | All routes produced checked outputs. The R 139 teardown is independently reproduced by loading the shared package stack without skill code. |
| T2 Structural contract | PASS | Required frontmatter and all referenced files are present. |
| T3 Determinism | PASS | Python and R stochastic layouts use seed 42; same-seed coordinates match. |
| T4 Security | PASS | No eval/exec of user strings, credentials, exfiltration, or destructive commands. |
| M1 Scientific integrity | PASS | No invented claims or statistics. |
| M2 Practice boundaries | PASS | Visualization only; no individual diagnosis or treatment. |
| M3 Methodological baseline | PASS | Layout coordinates are explicitly not biological measurements. |
| M4 Code usability | PASS | Python, R, Graphviz, PyVis, and Cytoscape paths all executed and outputs were checked. |

## Static Evaluation — 96/100

| Category | Score | Note |
|---|---:|---|
| Functional Suitability | 11/12 | All promised routes execute correctly; live Cytoscape output still needs manual label sizing or collision handling for publication legibility. |
| Reliability | 12/12 | Unknown sign values fail before layout, reruns overwrite exports safely, and edge/input boundary cases surface explicit errors. |
| Performance Context | 7/8 | The concise main file uses focused references and scripts; the four-panel static demonstration remains intentionally heavier than a single requested figure. |
| Agent Usability | 15/16 | Decision tree, failure modes, commands, and output expectations are clear; Cytoscape label tuning remains a documented manual judgment. |
| Human Usability | 8/8 | Natural prompts, GraphML support, repeatable requested labels, browser controls, and actionable validation errors are provided. |
| Security | 12/12 | No secrets, dynamic code execution, exfiltration, unsafe shell construction, or destructive file behavior is present. |
| Maintainability | 12/12 | Responsibilities are split across focused scripts and references, with deterministic regression coverage for every repaired contract. |
| Agent Specific | 19/20 | Triggering, progressive disclosure, composable CLIs, explicit output paths, and stop conditions are strong; Cytoscape necessarily creates desktop-session state. |

## Execution Method and Environment

The immutable provider checkout was copied byte-for-byte to `run/skill`; execution occurred only from that copy. Python used the data-visualization `py.sh` environment (networkx 3.6.1, matplotlib 3.11.2, pyvis 0.3.2). R used `r.sh` (R 4.4.3, igraph 2.3.0, ggraph 2.2.2, ggplot2 4.0.3). Graphviz and py4cytoscape ran in WSL `dv-cli`; a private Cytoscape 3.10.4/Xvfb process group was started and stopped by `run/run_cytoscape.sh`.

The shared R package stack segfaults at interpreter teardown: the saved package-only probe reproduces status 139 after printing its completion line, while a base-R probe returns 0. The skill scripts completed `ggsave`, printed all expected counts, and their PNGs parse and were opened. This environment defect is recorded but not attributed to the skill.

Representative saved commands:

```text
run/run_python_cases.sh      # fixtures plus Python regressions
run/run_r_cases.sh           # ggraph layouts and edge bundling
run/run_wsl_directed.sh      # signed Graphviz and sign-domain probe
run/run_cytoscape.sh         # private live Cytoscape run
run/run_checks.sh            # raster/PDF/HTML checks and Chrome screenshots
run/run_skill_tests.sh       # shipped focused regression tests
run/run_targeted_round2.sh   # two new label/sign/Cytoscape contract inputs
```

Key printed evidence:

```text
Static PPI: Network: 100 nodes, 511 edges; Communities: 4
Layouts: spring/kamada-kawai/circular/spectral/forceatlas2: 100 finite positions each
Signed GRN: 65 nodes, 124 edges; draw split [60, 64]
R layouts: fr/kk/circle: 100 nodes; bundling: 764 connections
PyVis directed: 65 nodes, 124 edges, 3 communities; return code 0
Cytoscape: 100 nodes, 511 edges; 15 labels; degree_match true; DIAMOND/ELLIPSE; overwrite_twice true
Round-two probes: 61-node requested label retained; 2,000-node cap=30; unknown sign rejected before layout
Artifact checker: 39 PNG/PDF/HTML artifacts parsed and nonblank
Shipped tests: PASS: adaptive labels, sign validation, PyVis heading, Cytoscape labels
```

## Detailed Outputs

### Input 1 — Canonical: Static PPI on planted communities

**Prompt:** Render the supplied synthetic 100-node weighted PPI as reproducible static NetworkX figures. Size by degree, color by community, normalize edge widths, and label a capped set of hubs.

**Regression source:** Pre-fix input 1

**Output and execution:** Executed the copied static CLI on the synthetic 100-node/511-edge PPI. Four parseable nonblank PNGs were produced; widths span 0.5-4.0, legend swatches exactly match node colors, and all four views use the same capped 15-node label dictionary.

**Evidence:** run/run_python_cases.sh -> run/audit_python_cases.py; output metrics in logs/python_results.json and logs/artifact_metrics.json; visually inspected out/input1_static_ppi/network_communities.png.

**Scores:** Basic 38/40 (Correctness 10/10; Reliability/clarity 9/10; Efficiency 9/10; Scope/safety 10/10); Specialized 58/60 (Method validity 20/20; Code 15/15; QC 9/10; Reproducibility 9/10; Security 5/5); Total 96/100.

**Assertions:**

- [PASS] All 100 nodes and 511 edges are represented in the static workflow — The CLI printed 100 nodes and 511 edges; image collections and the source graph agree.
- [PASS] Community nodes and legend swatches use one identical discrete palette — Independent RGBA equality check passed for all nodes.
- [PASS] Edge widths are bounded in the documented 0.5-4 point range — Observed minimum 0.5 and maximum 4.0.
- [PASS] Static views label only the documented adaptive capped subset — The focused regression intercepted all four draw calls and found one identical 15-node label dictionary.
- [PASS] Every output is parseable, nonblank, and visually inspected — Four PNGs are 2665-2850 by 2433 pixels with nonwhite fractions 0.261-0.495.

### Input 2 — Variant A: Layout comparison and signed GRN

**Prompt:** Compare spring, Kamada-Kawai, circular, spectral, and native ForceAtlas2 layouts for the PPI, then render the directed signed GRN with Graphviz dot, arrows, and sign colors.

**Regression source:** Pre-fix input 2

**Output and execution:** All five Python layouts completed on 100 nodes with finite positions and fixed seeds. The WSL Graphviz route drew all 124 signed directed edges (60 activation, 64 repression); the arrowheads and both colors were visually confirmed.

**Evidence:** run/run_python_cases.sh and run/run_wsl_directed.sh; logs/python_results.json and logs/wsl_directed_results.json; visually inspected ForceAtlas2 and signed-GRN PNGs.

**Scores:** Basic 38/40 (Correctness 10/10; Reliability/clarity 9/10; Efficiency 9/10; Scope/safety 10/10); Specialized 58/60 (Method validity 20/20; Code 15/15; QC 9/10; Reproducibility 9/10; Security 5/5); Total 96/100.

**Assertions:**

- [PASS] Spring, Kamada-Kawai, circular, spectral, and ForceAtlas2 all produce a nonblank figure — Five PNGs parsed at 1590x1313 with finite layout coordinates.
- [PASS] Stochastic layouts use reproducible seeds — Independent spring-layout reruns at seed 42 were identical.
- [PASS] The signed GRN preserves every directed edge — Instrumented draw calls contained all 124 graph edges.
- [PASS] Activation and repression receive distinct documented colors — 60 '+' edges and 64 '-' edges were sent to separate colored draw calls.
- [PASS] The rendered GRN visibly contains arrowheads — Visual inspection confirms directed arrow tips throughout the dot hierarchy.

### Input 3 — Variant B: Shipped static demonstration

**Prompt:** Run the shipped static PPI example and verify that node colors match every community legend swatch and that confidence widths remain visible.

**Regression source:** Pre-fix input 3

**Output and execution:** The shipped 30-node demonstration completed and its four figures parsed. The legend colors, edge widths, hub emphasis, and one adaptive top-15 label set are correct in every view.

**Evidence:** run/audit_python_cases.py input3; output and metrics in logs/python_results.json; inspected the community and confidence files.

**Scores:** Basic 38/40 (Correctness 10/10; Reliability/clarity 9/10; Efficiency 9/10; Scope/safety 10/10); Specialized 58/60 (Method validity 20/20; Code 15/15; QC 9/10; Reproducibility 9/10; Security 5/5); Total 96/100.

**Assertions:**

- [PASS] The shipped demo completes with four static figures — Four PNGs were produced from a 30-node/56-edge deterministic graph.
- [PASS] Community legend colors exactly match the node mapping — Independent palette equality check passed.
- [PASS] Confidence and degree encodings remain present — The confidence and degree views are nonblank and the helper returns bounded widths.
- [PASS] The adaptive label cap is applied consistently to every view — All four views receive the same adaptive label dictionary; the focused regression also proves the contract at N=100.
- [PASS] The demo is deterministic — Graph construction and spring layout both use seed 42.

### Input 4 — Variant B: R layouts and hierarchical bundling

**Prompt:** Use the shipped R recipes to render FR, Kamada-Kawai, and circular layouts for the GraphML PPI, plus the executable hierarchical edge-bundling demonstration.

**Regression source:** Pre-fix input 4

**Output and execution:** The R scripts wrote FR, Kamada-Kawai, circular, and 764-connection bundling PNGs; all parse and are visually correct. Both skill scripts exit 139 only after output because the shared R stack segfaults during package teardown; an independent package-only probe reproduces this, while base R exits 0.

**Evidence:** run/run_r_cases.sh plus independent run/run_r_runtime_probe.sh; logs/input4_*.log and logs/r_*probe*.log. All four requested artifacts exist and were visually inspected.

**Scores:** Basic 36/40 (Correctness 9/10; Reliability/clarity 9/10; Efficiency 8/10; Scope/safety 10/10); Specialized 56/60 (Method validity 19/20; Code 14/15; QC 9/10; Reproducibility 9/10; Security 5/5); Total 92/100.

**Assertions:**

- [PASS] All three ggraph layouts contain the complete 100-node network — Each script message reports 100 nodes and each PNG is nonblank.
- [PASS] The hierarchical bundling fixture draws all 764 relations — The script printed 764 bundled connections and the circular bundles are visible.
- [PASS] The R recipes are syntactically complete and execute through ggsave — All ggsave calls completed and wrote parseable PNGs.
- [PASS] The post-output R crash is attributable to the shared package runtime, not skill control flow — A package-only igraph/ggraph/ggplot2 probe exits 139; a base-R probe exits 0.
- [PASS] The stochastic R layout records a fixed seed — ggraph_layouts.R sets seed 42 for every layout.

### Input 5 — Edge: Undirected PyVis supplement

**Prompt:** Create basic and styled self-contained PyVis HTML supplements for the PPI without mutating the original edge weights; include degree sizing, communities, tooltips, and physics controls.

**Regression source:** Pre-fix input 5

**Output and execution:** Both 100-node PyVis HTML files are self-contained, preserve caller edge attributes, and render the four communities in Chrome. The saved document now contains exactly one heading and one title string.

**Evidence:** run/audit_python_cases.py plus run/screenshot_html.py; parsed HTML metrics in logs/python_results.json and screenshot out/input5_pyvis/network_styled_screenshot.png.

**Scores:** Basic 38/40 (Correctness 10/10; Reliability/clarity 9/10; Efficiency 9/10; Scope/safety 10/10); Specialized 58/60 (Method validity 20/20; Code 15/15; QC 9/10; Reproducibility 9/10; Security 5/5); Total 96/100.

**Assertions:**

- [PASS] Basic and styled HTML files are self-contained and browser-renderable — Both exceed 740 KB, inline vis-network assets, and render in Chrome.
- [PASS] The caller graph retains its original edge weights — Deep-copy equality passed after create_interactive_network.
- [PASS] Styled node sizes, colors, and tooltips are present — Rendered communities and degree-sized hubs are visible; sample nodes are serialized.
- [PASS] The HTML presents one clean title — The browser screenshot shows one heading; the generated HTML contains one h1 and one title string.
- [PASS] Physics and interaction controls are available — Navigation controls render and the physics options are serialized.

### Input 6 — Stress: Live Cytoscape automation

**Prompt:** Send the 100-node attributed PPI to Cytoscape, apply degree, confidence, and gene-type mappings, and export overwriteable PNG and PDF files to the requested directory.

**Regression source:** Pre-fix input 6

**Output and execution:** A private Cytoscape 3.10.4 process received exactly 100 nodes/511 edges, mapped degree, labels, confidence, and gene type correctly, fit after layout, and overwrote valid PNG/PDF exports twice. The export remains a dense cluster whose 15 labels are tiny or overlapping, so it still needs manual restyling for publication.

**Evidence:** run/run_cytoscape.sh -> run/cytoscape_check.py against py4cytoscape 1.13.0. Process group 1815839 was stopped and REST port 1234 confirmed down. Results in logs/cytoscape_results.json.

**Scores:** Basic 34/40 (Correctness 8/10; Reliability/clarity 8/10; Efficiency 8/10; Scope/safety 10/10); Specialized 54/60 (Method validity 18/20; Code 14/15; QC 8/10; Reproducibility 9/10; Security 5/5); Total 88/100.

**Assertions:**

- [PASS] Cytoscape receives exactly the source graph — Read-back returned 100 nodes and 511 edges.
- [PASS] Degree, label, confidence, and kinase-shape mappings apply — Degrees match NetworkX; 15 display labels are mapped; G000 is DIAMOND, G001 ELLIPSE, and widths span 1.0-3.987.
- [PASS] PNG and PDF exports are nonempty and overwrite safely — Both exports were written twice; PNG is 42,966 bytes and PDF 16,228 bytes.
- [FAIL] The exported figure is publication-readable without manual restyling — Visual inspection shows a dense force-directed clump; the capped labels exist but are tiny and overlap.
- [PASS] Only the audit-owned Cytoscape process is stopped — The saved wrapper used a private setsid process group and confirmed REST down after targeted termination.

### Input 7 — Scope Boundary: Promised routes and layout-artifact claim

**Prompt:** Audit whether every visualization route promised by the skill has a runnable path, and demonstrate that force-directed proximity changes with seed and must not be interpreted as biology.

**Regression source:** Pre-fix input 7

**Output and execution:** Every advertised route resolves to a shipped file; unsupported HiveNetX, Datashader, and adjustText claims are gone. Same-seed positions are identical, a different seed changes coordinates, and native ForceAtlas2 returns 1,200 finite positions in 3.0 seconds.

**Evidence:** run/audit_python_cases.py input7; inventory and layout-artifact assertions in logs/python_results.json.

**Scores:** Basic 38/40 (Correctness 10/10; Reliability/clarity 9/10; Efficiency 9/10; Scope/safety 10/10); Specialized 58/60 (Method validity 20/20; Code 15/15; QC 9/10; Reproducibility 9/10; Security 5/5); Total 96/100.

**Assertions:**

- [PASS] Every capability promised in the description has a shipped executable route — Static, layouts, signed GRN, bundling, PyVis, and Cytoscape files all exist.
- [PASS] Unsupported package promises were removed — HiveNetX, Datashader, and adjustText are absent from SKILL.md.
- [PASS] Same-seed stochastic layouts are reproducible — Maximum coordinate delta at seed 42 is 0.
- [PASS] Different seeds change drawing coordinates — Maximum coordinate delta between seeds 42 and 43 is 1.802.
- [PASS] The skill explicitly warns that layout is not biology — The central constraint and condition-comparison sections state this directly.

### Input 8 — Adversarial: Awkward graphs and shared condition layout

**Prompt:** Exercise the recipes on an unweighted disconnected graph with isolates, empty and singleton graphs, and control/treatment networks that must reuse one union layout.

**Regression source:** Pre-fix input 8

**Output and execution:** The static CLI handles an unweighted disconnected graph and two isolates, widths default to 2.25, and the shared union layout covers both conditions. The layout CLI rejects an empty graph with a clear error and renders a singleton; one isolate is visually crowded under the legend.

**Evidence:** run/audit_python_cases.py input8; awkward-graph outputs in out/input8_awkward and logs/python_results.json.

**Scores:** Basic 35/40 (Correctness 9/10; Reliability/clarity 9/10; Efficiency 7/10; Scope/safety 10/10); Specialized 55/60 (Method validity 18/20; Code 14/15; QC 9/10; Reproducibility 9/10; Security 5/5); Total 90/100.

**Assertions:**

- [PASS] Unweighted edges do not raise KeyError and receive visible widths — All three edges receive width 2.25.
- [PASS] Disconnected components and isolates remain in the output — The 6-node graph completes and the figure preserves the components; one isolate is partially under the legend.
- [PASS] Empty input is rejected explicitly — layouts.py exits 1 with 'The input graph is empty'.
- [PASS] Singleton input produces finite nonblank layouts — Spring and circular singleton PNGs parse and exceed 18 KB.
- [PASS] One union layout covers both condition networks — Both node sets are subsets of the one seed-42 union coordinate map.

### Input 9 — Variant A: Directed PyVis CLI end to end

**Prompt:** Create a directed PyVis HTML supplement from the supplied signed GRN GraphML and report the network and community counts after the CLI completes.

**Regression source:** New independent input

**Output and execution:** The directed-GraphML PyVis CLI probe exits 0, reports 65 nodes/124 edges/3 communities, writes two self-contained HTML files with one title each, and visibly renders direction arrowheads and all four regulator hubs.

**Evidence:** run/audit_python_cases.py input9 plus run/screenshot_html.py; HTML and screenshot evidence under out/input9_directed_pyvis.

**Scores:** Basic 38/40 (Correctness 10/10; Reliability/clarity 9/10; Efficiency 9/10; Scope/safety 10/10); Specialized 58/60 (Method validity 20/20; Code 15/15; QC 9/10; Reproducibility 9/10; Security 5/5); Total 96/100.

**Assertions:**

- [PASS] The directed CLI exits successfully — Return code 0 with final network/community summary.
- [PASS] Both directed HTML files preserve all nodes and edges — 65 nodes and 124 edges are reported; representative node IDs are serialized.
- [PASS] Direction is preserved in HTML — Both files contain arrow-to serialization and Chrome visibly shows arrowheads.
- [PASS] The styled route computes communities without rejecting a DiGraph — It reports three communities and completes.
- [PASS] The HTML is self-contained and browser-renderable — Both files exceed 715 KB and rendered without external assets.

### Input 10 — Edge: Natural-language sign normalization

**Prompt:** My regulatory edge attribute uses the values activation and repression. Normalize those values and render every edge with arrowheads and the correct two-color sign mapping; do not silently drop an unrecognized sign.

**Regression source:** New independent input

**Output and execution:** The normalized 5-node/4-edge arrow plot remains correct (2 activation, 2 repression), and the changed renderer now rejects explicit natural-language sign values before Graphviz can produce a misleading node-only figure.

**Evidence:** run/run_wsl_directed.sh instruments raw and normalized sign values; results in logs/wsl_directed_results.json. Both PNGs were opened side by side.

**Scores:** Basic 38/40 (Correctness 10/10; Reliability/clarity 9/10; Efficiency 9/10; Scope/safety 10/10); Specialized 58/60 (Method validity 20/20; Code 15/15; QC 9/10; Reproducibility 9/10; Security 5/5); Total 96/100.

**Assertions:**

- [PASS] Natural-language sign values can be normalized to the documented plus/minus contract — The audit mapping converts activation to '+' and repression to '-'.
- [PASS] The normalized plot draws every source edge — Instrumented draw calls contain all 4 edges, split 2/2 by sign.
- [PASS] The normalized plot visibly shows arrowheads and both colors — Visual inspection confirms four directed colored edges.
- [PASS] The script rejects or reports unrecognized sign values instead of silently dropping edges — The validator raises a ValueError naming activation/repression before layout; the targeted inhibition probe independently confirms Graphviz is not called.
- [PASS] The output is reproducible — Graphviz dot and the explicit normalization mapping are deterministic.

### Input 11 — Variant B: Requested low-degree labels and escaped PyVis title

**Prompt:** Render a new 61-node graph while retaining a prespecified low-degree node in the adaptive label set, use that same label set in every static panel, and produce one safely escaped PyVis heading.

**Regression source:** New independent input

**Output and execution:** A new 61-node graph rendered four nonblank static panels with one identical 16-node label dictionary: the adaptive top 15 plus requested low-degree node R016. The PyVis output has one HTML-escaped heading.

**Evidence:** run/run_targeted_round2.sh -> run/targeted_round2_cases.py; exact counts in logs/round2_targeted_results.json; visually inspected out/input11_requested_labels/network_communities.png.

**Scores:** Basic 39/40 (Correctness 10/10; Reliability/clarity 10/10; Efficiency 9/10; Scope/safety 10/10); Specialized 59/60 (Method validity 20/20; Code 15/15; QC 9/10; Reproducibility 10/10; Security 5/5); Total 98/100.

**Assertions:**

- [PASS] The requested low-degree node is retained in addition to the adaptive ranked set — R016 is absent from the rank-only set but present in the 16-node requested set.
- [PASS] Every static view uses exactly the same label dictionary — All four intercepted draw calls received the identical 16-node mapping.
- [PASS] All four static outputs are parseable and nonblank — The PNGs are 2705-2850 by 2433 pixels, 0.107-0.224 nonwhite, and each exceeds 0.84 MB.
- [PASS] The PyVis heading is emitted once and safely escaped — The 718,473-byte HTML has one h1, one escaped title, and no raw angle-bracket title.
- [PASS] The rendered labels are visually legible — The opened community panel shows the requested R016 and ranked labels at readable size without labeling all 61 nodes.

### Input 12 — Stress: Unknown-sign preflight and large Cytoscape cap

**Prompt:** Reject an unknown regulatory sign before Graphviz runs, then verify that a 2,000-node Cytoscape handoff caps labels and fits content only after layout.

**Regression source:** New independent input

**Output and execution:** A new adversarial sign value is rejected before Graphviz layout and writes no figure. A 2,000-node path graph receives 30 nonempty Cytoscape labels, the documented cap, and the mocked py4cytoscape calls prove layout precedes fit and the display_label mapping is applied.

**Evidence:** run/run_targeted_round2.sh -> run/targeted_round2_cases.py; logs/round2_targeted_results.json records sign rejection, graphviz_called false, 2,000 nodes, 30 labels, and layout-then-fit order.

**Scores:** Basic 38/40 (Correctness 10/10; Reliability/clarity 10/10; Efficiency 8/10; Scope/safety 10/10); Specialized 58/60 (Method validity 20/20; Code 15/15; QC 9/10; Reproducibility 9/10; Security 5/5); Total 96/100.

**Assertions:**

- [PASS] An unknown explicit sign is rejected with the value named — ValueError names inhibition and explains the required plus/minus normalization.
- [PASS] Validation happens before Graphviz and leaves no output artifact — The forbidden layout hook was not called and input12_should_not_exist.png is absent.
- [PASS] The large Cytoscape handoff caps labels at 30 — Exactly 30 of 2,000 display_label values are nonempty.
- [PASS] Cytoscape receives the display-label mapping — set_node_label_mapping is called once with display_label and PPIStyle.
- [PASS] Content fitting happens after layout — The recorded call order is layout, then fit.

## Visual Inspection

Opened and inspected: canonical community view, ForceAtlas2, signed Graphviz GRN, R FR, R edge bundling, live Cytoscape PNG, awkward disconnected graph, normalized sign plot, both PyVis Chrome screenshots, and the new 61-node requested-label panel. The plots are nonblank and the repaired mappings are visible. The live Cytoscape image is the basis for the remaining label-legibility finding: labels exist, but are tiny and overlap in the dense cluster.

## Recommendations

### [P2] Improve Cytoscape label legibility after fitting

- Observed in: [6]
- Problem: The live 100-node export contains the intended 15 labels, but they are tiny and several overlap inside a dense force-directed cluster, so the default image still needs manual restyling for publication.
- Root cause: Capping labels and fitting the whole network do not provide label-aware collision avoidance or a font-size mapping, and node size dominates the 816-by-358 export.
- Fix: Set an explicit readable NODE_LABEL_FONT_SIZE, scale node sizes for export, and use a label-aware layout or post-layout collision strategy; add a visual regression at the 100-node fixture size.

## Final Score and Floors

| Component | Result | Production floor |
|---|---:|---:|
| Static | 96/100 | >=80 |
| Execution average | 94.7/100 | >=85 |
| Layer 1 average | 37.3/40 | >=32 |
| Layer 2 average | 57.3/60 | >=48 |
| Assertions | 59/60 = 98.3% | >=90% |
| Vetoes | none | none |

Final = 96×0.4 + 94.7×0.6 = 95.2, rounded to **95/100**. Grade: **⭐ Production Ready**. Deployable: **true**. Open P0/P1/P2: **0/0/1**.

## Housekeeping

The live audit folder contains only scripts, fixtures, logs, reports, and result artifacts. The round-two task-created Cytoscape home/cache (277.9 MB) was moved recoverably to `F:\OpenScience\scratch\network-round2-disposable`; generated bytecode caches are absent from `run/`. `logs/provenance.json` verifies immutable commit 83008933, a clean audited skill subtree, a byte-identical execution copy, and no source or run `__pycache__`. A separate zero-byte root `logs/py4cytoscape.log` is recorded as unrelated repository status and was not removed. No provider or records bytes were modified while finalizing this report.
