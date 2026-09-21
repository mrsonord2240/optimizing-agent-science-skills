import json
A = lambda t, r, n: {"text": t, "result": "PASS" if r else "FAIL", "note": n}


def inp(i, typ, label, note, b, s, assertions, exe, en):
    p = sum(1 for a in assertions if a["result"] == "PASS")
    return {"index": i, "type": typ, "label": label, "status": "COMPLETED",
            "status_flag": "✅" if b + s >= 75 else "⚠️", "note": note, "basic": b, "specialized": s,
            "total": b + s, "assertions_passed": p, "assertions_total": len(assertions),
            "assertions": assertions, "executed": exe, "execution_note": en}


inputs = [
    inp(1, "Canonical", "SKILL 'NetworkX + matplotlib' block verbatim on a synthetic 100-node graph with 4 planted communities and 3 planted hubs",
        "Block runs verbatim once G exists. Drawn 100 nodes / 511 edges = graph; sizes exactly 100+50*degree; colour array equals an independent greedy_modularity run (ARI vs planted blocks 0.973, Louvain agrees at 0.973); spring layout with seed 42 reproducible and seed-sensitive. PNG opened: non-blank, but a hairball with 43 of 100 nodes labelled and overlapping.",
        35, 49, [
            A("Drawn node and edge counts equal the input graph", True, "PathCollection 100 offsets, LineCollection 511 segments vs G 100/511"),
            A("Node size encodes degree exactly as stated (100 + 50*degree)", True, "np.allclose over all 100 nodes"),
            A("Community colours equal an independent computation with the same algorithm and recover the planted blocks", True, "colour array == greedy_modularity index; ARI 0.973 vs planted, 0.973 vs Louvain seed 42; 4 communities of 24-26"),
            A("Layout is reproducible under the stated seed and drawn positions equal spring_layout(seed=42)", True, "same seed identical, seed 43 differs, drawn offsets == layout"),
            A("Hub labels are legible and identify the planted hubs without clutter", False, "fixed threshold degree>=10 labels 43 of 100 nodes; the 3 planted hubs (deg 46-48) are among them but labels overlap; no legend for size or community")],
        True, "Executed: run/i1_static.py (block 5 of SKILL.md exec'd from run/blocks, savefig hooked to capture the figure), out/i1_static.png opened. SYNTHETIC data/synth_ppi.graphml made by run/make_data.py."),
    inp(2, "Variant A", "SKILL 'Layout Algorithms' block, every layout line, plus directed gene-regulatory network with Graphviz dot in WSL and networkx ForceAtlas2",
        "Block verbatim fails NameError 'np' (only networkx imported). With np/hub_nodes/periphery_nodes/top_nodes supplied 6 of 7 layouts return 100 finite positions; the 7th (graphviz_layout) needs pydot, absent from the Windows venv but working in WSL dv-cli where the dot layout of a 65-node/124-edge GRN puts all 124 regulator->target edges downward and is deterministic. Directed graph drawn with 124/124 arrow patches. ForceAtlas2 has no code in the Skill; networkx 3.6.1 ships forceatlas2_layout (reproducible, 18.5 s at n=2000).",
        32, 46, [
            A("The layout block runs verbatim with only G defined", False, "NameError: name 'np' is not defined on the first line; hub_nodes, periphery_nodes and top_nodes are also placeholders"),
            A("Every layout returns a finite position for each node, and seeded ones are reproducible", True, "spring/kk/circular/shell/spectral/bipartite 100/100 finite; kk and spectral are deterministic without a seed"),
            A("The hierarchical (dot) layout respects edge direction for a regulatory cascade", True, "WSL Graphviz 13.1.2: TF0..TF4 strictly descending, 124/124 edges point downward, layout identical on re-run"),
            A("Directed edges are drawn as arrows by the Skill's networkx layered calls", True, "124/124 FancyArrowPatch on the DiGraph"),
            A("The ForceAtlas2 route the Skill recommends for >500-node scale-free graphs is given as runnable code", False, "only a prose pointer to fa2_modified or Gephi; nx.forceatlas2_layout in the installed networkx is not mentioned")],
        True, "Executed: run/i2_layouts.py, run/i7b_directed.py, run/i7c_dot.py (WSL dv-cli, pydot + Graphviz). SYNTHETIC data/synth_grn.graphml."),
    inp(3, "Variant B", "Shipped examples/network_plots.py from a copy: four figures, content of each captured from the matplotlib figure",
        "Runs and writes 4 PNGs of 30 nodes / 56 edges. Size = 100+150*degree, colour = degree, edge width = 2*weight, top-5 hub labels and the three edge-confidence colours all match a recomputation. Defect: in the community figure the legend swatches use palette(i) while nodes are coloured by a normalised colour array, so 3 of the 4 legend colours differ from the node colours (community 2 legend orange, nodes blue; community 4 legend pink, nodes grey).",
        33, 47, [
            A("Four PNGs are written and node/edge counts equal the graph (30/56)", True, "all four figures 30 nodes, 56 edge segments, 0.57-0.95 MB"),
            A("Node size, node colour and edge width encode degree/degree/weight exactly as stated", True, "np.allclose on sizes, colour array == degree, edge widths == 2*weight"),
            A("Edge-confidence colours follow the stated thresholds (>=900, >=700, else grey)", True, "56/56 edge colours equal the recomputed hex; 7 red, 22 salmon, 27 grey"),
            A("Hub figure labels exactly the top-5 degree nodes", True, "Gene1, Gene2, Gene5, Gene6, Gene9; no tie at rank 5 (next degree 4)"),
            A("Community legend colours equal the colours the nodes are drawn with", False, "communities 2, 3, 4: legend #fc8d62/#8da0cb/#e78ac3 vs node #8da0cb/#ffd92f/#b3b3b3; figure opened and mislabels which community is which")],
        True, "Executed: run/i3_shipped_static.py, i3b_debug.py, i3c_legend.py in out/ex_static (copy, no writes to the source clone); out/ex_static/network_communities.png and network_confidence.png opened."),
    inp(4, "Variant B", "R route: ggraph/igraph layouts, community colouring, edge bundling (SKILL blocks 2 and 4 verbatim, then repaired)",
        "Block 2 verbatim is a parse error (ends on a dangling '+'), block 4 verbatim errors (graph/from_idx/to_idx undefined). Repaired: fr/kk/circle/graphopt each draw 100 nodes and 511 edges; set.seed(42) makes 'fr' reproducible (without it two calls differ; kk is deterministic); igraph Louvain (seed 42) recovers the 4 planted blocks 25/25/25/25 (modularity 0.585); degree size and community colour columns match; the bundle example on ggraph's flare data draws all 764 connections. Figures opened.",
        32, 45, [
            A("Block 2 (ggraph layouts) runs as written once g exists", False, "parse error: unexpected end of input after the trailing '+' on the graphopt line"),
            A("Block 4 (edge bundling) runs as written", False, "'No layout function defined for objects of class function' because graph, from_idx, to_idx are never defined; works on flare once defined"),
            A("Each ggraph layout draws every node and edge of the input", True, "fr, kk, circle, graphopt: 100 nodes, 511 edge groups each, PNGs 98-134 KB"),
            A("set.seed makes the fr layout reproducible and its absence does not", True, "identical with seed 42 twice, different with 43, two unseeded calls differ"),
            A("igraph community assignment matches the planted communities and the plotted colour column equals it", True, "Louvain contingency table diagonal 25/25/25/25; d$comm == membership")],
        True, "Executed: run/i6_r.R through r.sh (R 4.4.3, igraph 2.3.0, ggraph 2.2.2, ggplot2 4.0.3); out/i6_comm.png and out/i6_bundle.png opened."),
    inp(5, "Edge", "PyVis interactive HTML: shipped interactive_network.py and the SKILL PyVis block, HTML parsed back and compared with the graph",
        "HTML written and parsed: 40/40 nodes, 76/76 edges, size = 10+5*degree, colour = palette[community]; screenshot in headless Chrome renders (heading duplicated). Defects: pyvis from_nx rewrites the caller's graph (weight popped into width), so the example's second (styled) network gets uniform edge width 1.5 instead of 3*weight and its community summary is computed on the mutated graph; the SKILL block uses an undefined palette; PyVis on a directed graph draws no arrowheads unless Network(directed=True), which the Skill never mentions.",
        29, 41, [
            A("HTML node and edge counts equal the graph, with size and colour encoding degree and community", True, "40/40 nodes, 76/76 edges, sizes and colours match; edge set identical"),
            A("Edge weight is encoded in the styled network's edge width (3*weight)", False, "G lost every 'weight' after the first from_nx call; all 76 styled edges have width 1.5"),
            A("The SKILL PyVis block runs as written given G, degrees and node_to_community from the previous block", False, "NameError: palette is never defined (works once defined: 40 nodes, sizes and colours right)"),
            A("A directed regulatory network keeps its direction in the HTML", False, "Network().from_nx(DiGraph): 0 of 124 edges carry arrows; only Network(directed=True) gives 124/124"),
            A("The 2000-node PyVis limit claim is realistic", True, "2000-node HTML 313 KB; opens, size well under the 100 MB failure mode")],
        True, "Executed: run/i4_pyvis.py (pyvis 0.3.2), Chrome headless screenshot out/ex_pyvis/styled.png opened. Examples ran from out/ex_pyvis, not from the clone."),
    inp(6, "Stress", "Cytoscape 3.10.4 headless via py4cytoscape 1.13.0 in WSL: SKILL block verbatim, shipped cytoscape_automation.py, real STRING TP53 network, export and re-import",
        "SKILL block verbatim: 100 nodes / 511 edges in Cytoscape, degree column equals networkx, size mapping [1,5,20]->[30,60,120] gives 120 / 76 / 68 for degree 46 / 9 / 7 (interpolation correct), colours correct, PDF written (14.7 KB). Real STRING (10 nodes, 32 edges): PNG, vector PDF (rendered with gs) and SVG export, Cytoscape SIF and GraphML round-trip to 10/32. Defects: shipped example's set_node_shape_mapping(mapping_type=) raises TypeError, swallowed by a trailing bare 'except: pass', so the example prints 'Network created' and never styles or exports; re-running the SKILL block fails because export_image refuses to overwrite network.pdf; a graph without a degree attribute silently keeps the default style.",
        31, 45, [
            A("SKILL Cytoscape block: node/edge counts and the degree-to-size/colour mapping are correct in Cytoscape", True, "100/511; sizes 120/76/68 and fills #BD0026/#FD9A4C/#FEB36C for degree 46/9/7"),
            A("Exports (PNG, PDF, SVG) of the real STRING network exist, parse and are non-blank", True, "PNG 28.6 KB opened, PDF rendered with gs shows the same network, SVG 22.8 KB"),
            A("Shipped cytoscape_automation.py applies its style and exports its figures when Cytoscape is running", False, "TypeError set_node_shape_mapping() got an unexpected keyword argument 'mapping_type', swallowed by the final bare except; no PDF/PNG written, ATM shape stays ELLIPSE"),
            A("The SKILL block can be re-run in the same directory", False, "CyError 'This file already exists and will not be overwritten: network.pdf'; no overwrite_file=True"),
            A("SIF and GraphML exported from Cytoscape re-read with the same counts", True, "networkx re-read 10/32 for GraphML, SIF 32 lines, Cytoscape re-imports SIF as 10/32")],
        True, "Executed in WSL dv-cli: run/i5_cyto_skill.py, i5b_cyto_more.py, i5c_debug.py, i5d_import.py, i5e_graphml.py, i5f_import_dbg.py via run/i5_run.sh (own Cytoscape/Xvfb killed after each run). Real data public-data/networks/string_tp53_neighbors.tsv."),
    inp(7, "Scope Boundary", "Promised-versus-shipped: hive plots, ForceAtlas2, datashader, the layout-is-not-biology warning and the usage-guide's 5000-node prompt",
        "The central warning is true and was demonstrated: the closest pair of four symmetric planted blocks changes with the seed (pairs (0,1) then (1,3)). But the description and usage-guide promise ForceAtlas2, hive plots, edge bundling in Python, adjustText labelling and Datashader, and none has runnable code (hive is three comment lines; HiveNetX does not exist on PyPI; fa2_modified and pyveplot do). spring_layout costs 1.7 s at 500 nodes, 18.6 s at 2000 and 104 s at 5000 nodes.",
        29, 39, [
            A("The 'layout is an artifact, not biology' claim holds on planted structure", True, "closest block pair differs across seeds 1-5 although all inter-block densities are equal"),
            A("Every layout/render route named in the description has an executable recipe in SKILL.md", False, "hive plot = comment lines; ForceAtlas2, Datashader, adjustText and Python edge bundling have no code"),
            A("Every package the Skill tells the agent to use exists", False, "pip index: HiveNetX no matching distribution; fa2_modified 0.4 and pyveplot 1.0.2 exist"),
            A("The usage-guide prompt '5000-node network, ForceAtlas2, bundled edges, rasterized PDF' can be satisfied from the Skill", False, "no recipe for any of the four parts; nx.spring_layout takes 104 s at n=5000 and the Skill's own legibility limit is ~2000 edges"),
            A("Stated scale thresholds (spring layout ~2000 edges, PyVis ~2000 nodes) are consistent with measurements", True, "6k-edge layout 18.6 s, 15k-edge 104 s; 2000-node HTML 313 KB")],
        True, "Executed: run/i8_layout_artifact.py, timing block in run/i7_edge.py; pip index versions for fa2_modified, fa2, pyveplot, HiveNetX, nxviz (no installs)."),
    inp(8, "Adversarial", "Awkward graphs through the SKILL block: unweighted, directed, self-loop, isolates, empty, single edge, two conditions, real 10-gene STRING",
        "Block 5 draws all nodes on every awkward graph (self-loop 512/512 edges, 5 isolates, two components, empty, single edge, integer ids; directed graphs draw as arrows). Union-layout comparison works and a layout from only one condition fails loudly (NetworkXError: Node 'X1' has no position). The Skill's own edge-width fix raises KeyError on an unweighted graph and shows no normalisation although raw weights (0.1-1.0) are sub-point line widths. On the real STRING TP53 network the fixed 'degree >= 10' hub rule labels 0 of 10 nodes.",
        31, 45, [
            A("Union-layout two-condition comparison works as the Skill prescribes", True, "one spring_layout(union) draws A and B; layout of A alone raises NetworkXError for the new node"),
            A("Edge-width fix using G[u][v]['weight'] works on a graph without weights", False, "KeyError 'weight'; no guard and no normalisation to a visible range although weights 0.1-1.0 give sub-point lines"),
            A("Self-loops, isolated nodes, disconnected components, empty and single-edge graphs draw all nodes and edges", True, "512/512, 105/105, 10/10, 0/0, 2/2 with no exception"),
            A("The hub-label rule labels the hubs of a real small PPI network", False, "STRING TP53 axis max degree 9 < 10: 0 labels, TP53 unlabelled; on the 100-node planted graph 43 labels"),
            A("Directed networks are drawn with direction by the networkx layered calls", True, "124/124 arrowheads on the 65-node GRN; the +/- edge sign attribute is not encoded by any recipe")],
        True, "Executed: run/i7_edge.py, run/i7b_directed.py. Real public-data STRING TP53 edges and SYNTHETIC graphs."),
]
n = len(inputs)
avg = round(sum(i["total"] for i in inputs) / n, 1)
cats = {
    "functional_suitability": (8, 12, "Completeness 2/4: ForceAtlas2, hive, Datashader, adjustText and Python edge bundling are named in the description but have no code; correctness 3/4: layout-artifact and thresholds hold, but block 2 does not parse and 'graphopt' is called OpenOrd-style (graphopt is not OpenOrd); appropriateness 3/4."),
    "reliability": (6, 12, "Every recipe that ran produced correct counts and mappings, but the examples carry silent faults: legend colours that differ from node colours, pyvis destroying edge weights, a bare except hiding a TypeError, an export that refuses to be re-run."),
    "performance_context": (6, 8, "320-line SKILL.md with no references/ layer; failure-mode prose is compact; usage-guide repeats the tips."),
    "agent_usability": (12, 16, "Decision tree, Goal/Approach blocks, failure-mode table and quantitative thresholds are strong; blocks are fragments (np, palette, degrees, hub_nodes undefined) and none says what it needs."),
    "human_usability": (6, 8, "Natural example prompts; prompts for FA2, hive and bundling cannot be satisfied from the Skill."),
    "security": (11, 12, "No credentials, eval or network. Cytoscape and file exports write into the cwd; Cytoscape REST is local."),
    "maintainability": (8, 12, "Version line present but stale where it matters (py4cytoscape 1.13 signatures, networkx 3.4+ native forceatlas2_layout, matplotlib 3.11); shipped examples untested against py4cytoscape."),
    "agent_specific": (14, 20, "Precise trigger with concrete layout names; cross-referenced Skills exist (coexpression-networks, interaction-databases, cell-communication); no references/ layer and the description promises more than the body delivers."),
}
sub = sum(v[0] for v in cats.values())
final_score = round(sub * 0.4 + avg * 0.6)
grade = "Production Ready" if final_score >= 85 else "Limited Release" if final_score >= 75 else "Beta Only" if final_score >= 60 else "Reject"
rep = {
    "meta": {
        "skill_name": "bio-data-visualization-network-visualization",
        "description": "Visualize biological networks (PPI, gene-regulatory, co-expression, pathway) with layout algorithm choice (ForceAtlas2, Fruchterman-Reingold, Kamada-Kawai, hive plots), edge bundling, community-based coloring, and reproducible seeds using NetworkX, PyVis, igraph, and Cytoscape automation. Use when rendering biological networks for static publication, interactive HTML exploration, or Cytoscape-format export.",
        "evaluated_on": "2026-09-20", "evaluator_version": "skill-auditor@1.0", "category": "Data Analysis",
        "execution_mode": "A", "complexity": "Complex", "n_inputs": n,
        "source": "mrsonord2240/bioSkills@64b3b150c9b989c102f7ee69e0bb07c16842d894:data-visualization/network-visualization",
        "audit_type": "first audit of the unmodified upstream Skill (staging commit 64b3b15); role unspecified, scored as a standalone plotting Skill",
        "executed": True,
        "execution_note": "Executed 8/8 inputs. Windows venv (networkx 3.6.1, pyvis 0.3.2, python-igraph 1.0.0, matplotlib 3.11.2, datashader 0.19.1) via py.sh; R 4.4.3 (igraph 2.3.0, ggraph 2.2.2, ggplot2 4.0.3) via r.sh; WSL science dv-cli (Cytoscape 3.10.4 headless under Xvfb, py4cytoscape 1.13.0, Graphviz 13.1.2 + pydot) via run/i5_run.sh; headless Chrome for the PyVis HTML. Every SKILL.md code block and all three shipped examples were run; figures were opened. Scripts run from the audit folder or copies; no writes into the source clone (no __pycache__). Only own Cytoscape/Xvfb processes were stopped."},
    "veto_gates": {
        "skill_veto": {"gate": "PASS", "stability": "PASS", "contract": "PASS", "determinism": "PASS", "security": "PASS"},
        "research_veto": {
            "applicable": True, "gate": "PASS",
            "scientific_integrity": {"result": "PASS", "detail": "No fabricated statistic or citation found; the central layout-is-not-biology claim reproduced (closest block pair changes with the seed) and the thresholds are consistent with measurements. HiveNetX is named but does not exist on PyPI (recorded as a P1 gap, not a fabricated result)."},
            "practice_boundaries": {"result": "PASS", "detail": "Network drawing skill; no diagnostic or prescriptive content."},
            "methodological_ground": {"result": "PASS", "detail": "The Skill warns against reading positions as biology and prescribes shared layouts for comparisons; both verified. No fallacy found."},
            "code_usability": {"result": "PASS", "detail": "Both shipped Python examples with a working stack run and their figures/HTML are correct; SKILL blocks 1, 6 and 7 run once their named variables exist. Not clean: block 2 (R) is a syntax error as written, block 4 uses undefined names, and examples/cytoscape_automation.py hides a TypeError behind a bare except so its style and export steps never happen. Recorded as P1 rather than a veto because the flagship static and interactive examples run and every underlying call works with the corrections listed."}}},
    "static_score": {"subtotal": sub, "max": 100, "categories": {k: {"score": v[0], "max": v[1], "note": v[2]} for k, v in cats.items()}},
    "dynamic_score": {"execution_avg": avg, "max": 100,
                      "assertion_pass_rate": {"passed": sum(i["assertions_passed"] for i in inputs), "total": sum(i["assertions_total"] for i in inputs)},
                      "inputs": inputs},
    "final": {"static_weighted": round(sub * 0.4, 1), "dynamic_weighted": round(avg * 0.6, 1), "score": final_score, "max": 100,
              "grade": grade, "grade_symbol": "⚠️" if grade == "Beta Only" else "✅", "deployable": grade in ("Production Ready", "Limited Release"), "veto_override": False},
    "key_strengths": [
        "The core plotting recipes are numerically right: node/edge counts, degree-to-size, community colours, edge-confidence colours and hub labels all matched independent recomputation, and community assignments recovered 4 planted blocks (ARI 0.973 greedy, 100% Louvain in R).",
        "Seeded layouts are reproducible in networkx, ggraph/igraph and Cytoscape, and the Skill's central warning that positions are artifacts was demonstrated (closest planted block pair changes with the seed).",
        "All three routes work end to end on real tools: Matplotlib PNG/PDF, PyVis HTML (parsed and rendered), Cytoscape 3.10.4 with degree mappings verified at 120/76/68, and export/re-import of SIF/GraphML with unchanged counts.",
        "The decision tree, failure-mode table and quantitative thresholds are compact and accurate (spring layout 18.6 s at 6k edges, 2000-node PyVis 313 KB)."],
    "recommendations": [
        {"priority": "P1", "title": "examples/cytoscape_automation.py fails silently", "observed_in": [6],
         "problem": "set_node_shape_mapping(..., mapping_type='d') raises TypeError on py4cytoscape 1.13.0 and the closing bare 'except Exception: pass' swallows it, so with Cytoscape running the example prints 'Network created', applies no style and writes no PDF/PNG.",
         "root_cause": "The function is always discrete and takes no mapping_type; the run block catches everything without reporting.",
         "fix": "Drop mapping_type from the shape call, replace the bare except with one that prints the traceback, and pass overwrite_file=True to export_image."},
        {"priority": "P1", "title": "Community legend in network_plots.py mislabels communities", "observed_in": [3],
         "problem": "Legend swatches use plt.cm.Set2(i) while nodes are coloured by a normalised community index, so 3 of the 4 legend colours differ from the node colours.",
         "root_cause": "cmap normalisation maps 0..3 to the ends of Set2, not to indices 0..3.",
         "fix": "Colour nodes with [palette(node_to_community[n]) for n in G.nodes()] (or a ListedColormap with vmin=0, vmax=len(communities)-1) so legend and nodes share one mapping."},
        {"priority": "P1", "title": "PyVis from_nx destroys edge weights and mutates the graph", "observed_in": [5],
         "problem": "After from_nx the graph has no 'weight' (moved into 'width'), so the second network in interactive_network.py gets uniform width 1.5 and its printed communities are computed on the mutated graph; the SKILL PyVis block also uses an undefined palette and never mentions Network(directed=True), so regulatory networks lose arrowheads.",
         "root_cause": "pyvis rewrites edge attributes in place and the recipes never copy the graph or define palette.",
         "fix": "Call net.from_nx(G.copy()) or build with add_node/add_edge, compute communities before any from_nx, define palette in the block, and show Network(directed=True) for GRNs."},
        {"priority": "P1", "title": "SKILL.md code blocks are not runnable as written", "observed_in": [2, 4, 6],
         "problem": "The layout block uses np without import and placeholder names; ggraph block 2 ends on a dangling '+' (parse error); the bundling block uses undefined graph/from_idx/to_idx and fails; the Cytoscape block never creates the 'degree' node attribute it maps, then silently keeps the default style.",
         "root_cause": "Fragments were written as prose sketches and not tested.",
         "fix": "Make each block self-contained (imports, a small toy G, degree assigned with nx.set_node_attributes) and test them; add a working flare-based bundling example."},
        {"priority": "P1", "title": "Description promises recipes that do not exist", "observed_in": [2, 7],
         "problem": "ForceAtlas2, hive plots, Datashader, adjustText labelling and Python edge bundling have no code; HiveNetX is not on PyPI; the usage-guide prompt for a 5000-node ForceAtlas2, bundled, rasterized network cannot be met (nx.spring_layout takes 104 s at n=5000).",
         "root_cause": "Decision-tree rows were added without matching recipes.",
         "fix": "Add short tested recipes (nx.forceatlas2_layout in networkx >= 3.4, a Datashader raster of a large edge list, pyveplot or a hand-written hive), or remove the names from the description; replace HiveNetX with a real package."},
        {"priority": "P2", "title": "Hub-label rule and edge-width advice are not adaptive", "observed_in": [1, 8],
         "problem": "'degree >= 10' labels 43 of 100 nodes on a dense graph and 0 of 10 on the real STRING TP53 network; the edge-width one-liner raises KeyError on unweighted graphs and shows no normalisation although raw weights are sub-point widths.",
         "root_cause": "Fixed thresholds and unguarded attribute access.",
         "fix": "Label the top-k (about 15-30) by degree or a quantile, use G[u][v].get('weight', 1) and rescale widths to 0.5-4 pt."},
        {"priority": "P2", "title": "Directed regulatory networks have no styling recipe", "observed_in": [2, 6, 8],
         "problem": "Cytoscape draws no arrowheads by default (EDGE_TARGET_ARROW_SHAPE NONE, and the shipped style sets NONE), the '+'/'-' regulation sign is never encoded, and the networkx dot layout needs pydot plus Graphviz which the prerequisites do not list.",
         "root_cause": "The directed row of the decision tree has no recipe or prerequisites.",
         "fix": "Add a GRN example: DiGraph, dot layout, arrowheads, colour by sign, and list pydot/Graphviz under Prerequisites."},
        {"priority": "P2", "title": "Stale or inexact statements", "observed_in": [2, 6],
         "problem": "networkx >= 3.4 has forceatlas2_layout but the Skill points to fa2_modified or Gephi; ggraph 'graphopt' is labelled OpenOrd-style (it is not); the PyVis heading appears twice; the block writes network.pdf relative to Cytoscape's working directory.",
         "root_cause": "Version drift and unchecked comments.",
         "fix": "Update the layout notes, use absolute output paths for Cytoscape exports and drop the heading duplication."}],
}
json.dump(rep, open('eval_report_bio-data-visualization-network-visualization_result.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print('static', sub, 'avg', avg, rep['final'], rep['dynamic_score']['assertion_pass_rate'], [i['total'] for i in inputs],
      'L1', sum(i['basic'] for i in inputs) / n, 'L2', sum(i['specialized'] for i in inputs) / n)
