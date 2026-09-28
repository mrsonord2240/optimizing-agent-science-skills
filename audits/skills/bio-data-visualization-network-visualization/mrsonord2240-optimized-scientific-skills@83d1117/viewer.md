> **Audit record for `bio-data-visualization-network-visualization`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/optimized-scientific-skills@83d1117](https://github.com/mrsonord2240/optimized-scientific-skills/tree/83d111751e849f11ad443491fade222c868c0f63/skills/bio-data-visualization-network-visualization) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-27 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-data-visualization-network-visualization

Generated: 2026-09-27

- Source: `mrsonord2240/optimized-scientific-skills@83d111751e849f11ad443491fade222c868c0f63:skills/bio-data-visualization-network-visualization`
- Independent re-auditor: **true**
- Category: Data Analysis; execution mode: D (Hybrid); complexity: Complex
- Re-audit size: **10 inputs** = all 8 pre-fix inputs rerun as regressions + 2 genuinely new inputs. This explicit re-audit mandate extends the generic schema's older 8-input enumeration.
- Result: **90/100, ⭐ Production Ready, deployable true**; no veto fired; open findings P0/P1/P2 = **0/1/3**.

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---:|---:|---:|---:|---|
| 1 | Canonical | 32 | 52 | 84 | 4/5 | ✅ COMPLETED |
| 2 | Variant A | 38 | 58 | 96 | 5/5 | ✅ COMPLETED |
| 3 | Variant B | 36 | 56 | 92 | 4/5 | ✅ COMPLETED |
| 4 | Variant B | 36 | 56 | 92 | 5/5 | ✅ COMPLETED |
| 5 | Edge | 35 | 55 | 90 | 4/5 | ✅ COMPLETED |
| 6 | Stress | 32 | 52 | 84 | 4/5 | ✅ COMPLETED |
| 7 | Scope Boundary | 38 | 58 | 96 | 5/5 | ✅ COMPLETED |
| 8 | Adversarial | 35 | 55 | 90 | 5/5 | ✅ COMPLETED |
| 9 | Variant A | 37 | 57 | 94 | 5/5 | ✅ COMPLETED |
| 10 | Edge | 32 | 49 | 81 | 4/5 | ✅ COMPLETED |

**Execution average:** 89.9/100  
**Layer 1 average:** 35.1/40  
**Layer 2 average:** 54.8/60  
**Assertion pass rate:** 45/50 (90%)

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

## Static Evaluation — 90/100

| Category | Score | Note |
|---|---:|---|
| Functional Suitability | 10/12 | Promised routes are present and correct; static labels and sign-domain validation remain incomplete. |
| Reliability | 10/12 | Errors surface and workflows are rerunnable, but unknown sign values are silently dropped. |
| Performance Context | 7/8 | The 207-line main file uses focused references and scripts; the four-view static route remains heavier than necessary. |
| Agent Usability | 15/16 | Decision tree, failure modes, commands, and output expectations are clear; one documented label rule is not implemented in the canonical example. |
| Human Usability | 7/8 | Natural prompts and broad GraphML support; sign normalization is documented but not enforced. |
| Security | 11/12 | No secrets, eval, network exfiltration, or destructive operations; graph attribute domains receive only partial validation. |
| Maintainability | 11/12 | Clean modular split and focused tests; tests do not cover all-node labels, unknown signs, duplicate titles, or Cytoscape legibility. |
| Agent Specific | 19/20 | Precise trigger, progressive disclosure, composable CLIs, explicit paths, and stop conditions; Cytoscape reruns create an additional network in the desktop session. |

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
```

Key printed evidence:

```text
Static PPI: Network: 100 nodes, 511 edges; Communities: 4
Layouts: spring/kamada-kawai/circular/spectral/forceatlas2: 100 finite positions each
Signed GRN: 65 nodes, 124 edges; draw split [60, 64]
R layouts: fr/kk/circle: 100 nodes; bundling: 764 connections
PyVis directed: 65 nodes, 124 edges, 3 communities; return code 0
Cytoscape: 100 nodes, 511 edges; degree_match true; DIAMOND/ELLIPSE; overwrite_twice true
Artifact checker: 35 PNG/PDF/HTML artifacts parsed and nonblank
Shipped tests: PASS: static mapping, unweighted widths, PyVis immutability, directed arrows
```

## Detailed Outputs

### Input 1 — Canonical: Static PPI on planted communities

**Prompt:** Render the supplied synthetic 100-node weighted PPI as reproducible static NetworkX figures. Size by degree, color by community, normalize edge widths, and label a capped set of hubs.

**Regression source:** Pre-fix input 1

**Output and execution:** Executed the copied static CLI on the synthetic 100-node/511-edge PPI. Four parseable nonblank PNGs were produced; widths span 0.5-4.0 and legend swatches exactly match node colors. Visual inspection found that three views label all 100 nodes instead of the promised capped subset.

**Evidence:** run/run_python_cases.sh -> run/audit_python_cases.py; output metrics in logs/python_results.json and logs/artifact_metrics.json; visually inspected out/input1_static_ppi/network_communities.png.

**Scores:** Basic 32/40 (Correctness 7/10; Reliability/clarity 7/10; Efficiency 8/10; Scope/safety 10/10); Specialized 52/60 (Method validity 17/20; Code 13/15; QC 8/10; Reproducibility 9/10; Security 5/5); Total 84/100.

**Assertions:**

- [PASS] All 100 nodes and 511 edges are represented in the static workflow — The CLI printed 100 nodes and 511 edges; image collections and the source graph agree.
- [PASS] Community nodes and legend swatches use one identical discrete palette — Independent RGBA equality check passed for all nodes.
- [PASS] Edge widths are bounded in the documented 0.5-4 point range — Observed minimum 0.5 and maximum 4.0.
- [FAIL] Static views label only the documented adaptive capped subset — Degree, community, and confidence views call draw_networkx_labels for every node; the 100-node image is visibly crowded.
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

**Output and execution:** The shipped 30-node demonstration completed and its four figures parsed. The original legend-color regression is fixed, edge widths are visible, and hub highlighting works; however three views still label all 30 nodes instead of the documented adaptive top 15.

**Evidence:** run/audit_python_cases.py input3; output and metrics in logs/python_results.json; inspected the community and confidence files.

**Scores:** Basic 36/40 (Correctness 9/10; Reliability/clarity 8/10; Efficiency 9/10; Scope/safety 10/10); Specialized 56/60 (Method validity 18/20; Code 15/15; QC 9/10; Reproducibility 9/10; Security 5/5); Total 92/100.

**Assertions:**

- [PASS] The shipped demo completes with four static figures — Four PNGs were produced from a 30-node/56-edge deterministic graph.
- [PASS] Community legend colors exactly match the node mapping — Independent palette equality check passed.
- [PASS] Confidence and degree encodings remain present — The confidence and degree views are nonblank and the helper returns bounded widths.
- [FAIL] The adaptive label cap is applied consistently to every view — Three views label all 30 nodes although the documented cap is 15 for N=30.
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

**Output and execution:** Both 100-node PyVis HTML files are self-contained, preserve caller edge attributes, and render the four communities in Chrome. The browser screenshot shows the title duplicated on consecutive lines.

**Evidence:** run/audit_python_cases.py plus run/screenshot_html.py; parsed HTML metrics in logs/python_results.json and screenshot out/input5_pyvis/network_styled_screenshot.png.

**Scores:** Basic 35/40 (Correctness 9/10; Reliability/clarity 8/10; Efficiency 8/10; Scope/safety 10/10); Specialized 55/60 (Method validity 18/20; Code 14/15; QC 9/10; Reproducibility 9/10; Security 5/5); Total 90/100.

**Assertions:**

- [PASS] Basic and styled HTML files are self-contained and browser-renderable — Both exceed 740 KB, inline vis-network assets, and render in Chrome.
- [PASS] The caller graph retains its original edge weights — Deep-copy equality passed after create_interactive_network.
- [PASS] Styled node sizes, colors, and tooltips are present — Rendered communities and degree-sized hubs are visible; sample nodes are serialized.
- [FAIL] The HTML presents one clean title — Chrome shows 'PPI Network with Communities' twice; the string occurs in two h1 elements.
- [PASS] Physics and interaction controls are available — Navigation controls render and the physics options are serialized.

### Input 6 — Stress: Live Cytoscape automation

**Prompt:** Send the 100-node attributed PPI to Cytoscape, apply degree, confidence, and gene-type mappings, and export overwriteable PNG and PDF files to the requested directory.

**Regression source:** Pre-fix input 6

**Output and execution:** A private Cytoscape 3.10.4 process received exactly 100 nodes/511 edges, mapped degree and gene type correctly, and overwrote valid PNG/PDF exports twice. The visual export is a dense unlabeled cluster, below the example's 'publication-quality' claim.

**Evidence:** run/run_cytoscape.sh -> run/cytoscape_check.py against py4cytoscape 1.13.0. Process group 1815839 was stopped and REST port 1234 confirmed down. Results in logs/cytoscape_results.json.

**Scores:** Basic 32/40 (Correctness 8/10; Reliability/clarity 6/10; Efficiency 8/10; Scope/safety 10/10); Specialized 52/60 (Method validity 17/20; Code 14/15; QC 8/10; Reproducibility 8/10; Security 5/5); Total 84/100.

**Assertions:**

- [PASS] Cytoscape receives exactly the source graph — Read-back returned 100 nodes and 511 edges.
- [PASS] Degree, confidence, and kinase-shape mappings apply — Degrees match NetworkX; G000 is DIAMOND, G001 ELLIPSE, widths span 1.0-3.987.
- [PASS] PNG and PDF exports are nonempty and overwrite safely — Both exports were written twice; PNG is 42,325 bytes and PDF 15,850 bytes.
- [FAIL] The exported figure is publication-readable without manual restyling — Visual inspection shows an unlabeled force-directed clump; nodes cannot be identified.
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

**Output and execution:** The new directed-GraphML PyVis CLI probe exits 0, reports 65 nodes/124 edges/3 communities, and writes two self-contained HTML files. Chrome visibly renders direction arrowheads and all four regulator hubs.

**Evidence:** run/audit_python_cases.py input9 plus run/screenshot_html.py; HTML and screenshot evidence under out/input9_directed_pyvis.

**Scores:** Basic 37/40 (Correctness 10/10; Reliability/clarity 9/10; Efficiency 8/10; Scope/safety 10/10); Specialized 57/60 (Method validity 20/20; Code 15/15; QC 9/10; Reproducibility 8/10; Security 5/5); Total 94/100.

**Assertions:**

- [PASS] The directed CLI exits successfully — Return code 0 with final network/community summary.
- [PASS] Both directed HTML files preserve all nodes and edges — 65 nodes and 124 edges are reported; representative node IDs are serialized.
- [PASS] Direction is preserved in HTML — Both files contain arrow-to serialization and Chrome visibly shows arrowheads.
- [PASS] The styled route computes communities without rejecting a DiGraph — It reports three communities and completes.
- [PASS] The HTML is self-contained and browser-renderable — Both files exceed 715 KB and rendered without external assets.

### Input 10 — Edge: Natural-language sign normalization

**Prompt:** My regulatory edge attribute uses the values activation and repression. Normalize those values and render every edge with arrowheads and the correct two-color sign mapping; do not silently drop an unrecognized sign.

**Regression source:** New independent input

**Output and execution:** Following the reference instruction to normalize noncanonical signs produces a correct 5-node/4-edge arrow plot (2 activation, 2 repression). Directly passing 'activation'/'repression' draws zero edges yet exits successfully, so the recipe lacks a guard against silent data loss.

**Evidence:** run/run_wsl_directed.sh instruments raw and normalized sign values; results in logs/wsl_directed_results.json. Both PNGs were opened side by side.

**Scores:** Basic 32/40 (Correctness 8/10; Reliability/clarity 8/10; Efficiency 6/10; Scope/safety 10/10); Specialized 49/60 (Method validity 16/20; Code 12/15; QC 8/10; Reproducibility 8/10; Security 5/5); Total 81/100.

**Assertions:**

- [PASS] Natural-language sign values can be normalized to the documented plus/minus contract — The audit mapping converts activation to '+' and repression to '-'.
- [PASS] The normalized plot draws every source edge — Instrumented draw calls contain all 4 edges, split 2/2 by sign.
- [PASS] The normalized plot visibly shows arrowheads and both colors — Visual inspection confirms four directed colored edges.
- [FAIL] The script rejects or reports unrecognized sign values instead of silently dropping edges — The raw run reports 4 graph edges but sends 0 edges to draw calls and still writes a PNG.
- [PASS] The output is reproducible — Graphviz dot and the explicit normalization mapping are deterministic.

## Visual Inspection

Opened and inspected: canonical community view, ForceAtlas2, signed Graphviz GRN, R FR, R edge bundling, live Cytoscape PNG, awkward disconnected graph, raw and normalized sign plots, undirected PyVis Chrome screenshot, and directed PyVis Chrome screenshot. The plots are nonblank and mappings are visible. The inspection is the basis for the all-node label, unlabeled Cytoscape, duplicate HTML title, and silent-sign findings.

## Recommendations

### [P1] Apply the adaptive label cap in every static view

- Observed in: [1, 3]
- Problem: network_plots.py labels every node in the degree, community, and confidence figures. The 100-node canonical output is visibly crowded and contradicts the core workflow and quantitative top-k rule.
- Root cause: Three render branches pass the full graph to draw_networkx_labels; only the separate hub figure uses a ranked subset.
- Fix: Compute the documented adaptive top-k set once and pass its label dictionary to all four static views, while retaining optional user-specified genes of interest.

### [P2] Reject unknown regulatory sign values

- Observed in: [10]
- Problem: The directed renderer silently draws zero edges when a sign column contains activation/repression rather than '+'/'-', yet exits successfully and writes a plausible node-only PNG.
- Root cause: The loop draws only two recognized values and never checks whether their union equals the graph edge set.
- Fix: Validate the sign domain before layout, list unknown values in a ValueError, and optionally accept an explicit activation/repression mapping flag.

### [P2] Make the Cytoscape export readable by default

- Observed in: [6]
- Problem: The live PNG is a dense unlabeled cluster, so the example does not meet its own publication-quality claim without manual Cytoscape work.
- Root cause: The style sets label font size but does not map node names to NODE_LABEL or fit/space labels after the force-directed layout.
- Fix: Populate and map an explicit label column, fit content after layout, and document when to suppress labels for large networks.

### [P2] Remove duplicated PyVis headings

- Observed in: [5, 9]
- Problem: Both browser-rendered styled HTML pages show the title twice on consecutive lines.
- Root cause: With pyvis 0.3.2 the supplied heading is emitted in two h1 elements by the active template path.
- Fix: Use a custom template or post-render check that guarantees exactly one h1 title, and add a browser-level regression assertion.

## Final Score and Floors

| Component | Result | Production floor |
|---|---:|---:|
| Static | 90/100 | >=80 |
| Execution average | 89.9/100 | >=85 |
| Layer 1 average | 35.1/40 | >=32 |
| Layer 2 average | 54.8/60 | >=48 |
| Assertions | 45/50 = 90% | >=90% |
| Vetoes | none | none |

Final = 90×0.4 + 89.9×0.6 = 89.9, rounded to **90/100**. Grade: **⭐ Production Ready**. Deployable: **true**. Open P0/P1/P2: **0/1/3**; open P1 does not block deployability under the audit brief.

## Housekeeping

The live audit folder contains only scripts, fixtures, logs, reports, and result artifacts. A task-created Cytoscape home/cache (1,006 files, 277,845,954 bytes) and two generated `__pycache__` directories were moved recoverably to `F:\OpenScience\audit-disposable` so the publisher will not copy them. The verified post-cleanup footprint is 104 files / 19.66 MiB total; `run/` is 33 files / 0.11 MiB and contains no vendored package tree. No skill bytes, fix log, provider commit, backlog, branch, or remote were modified.
