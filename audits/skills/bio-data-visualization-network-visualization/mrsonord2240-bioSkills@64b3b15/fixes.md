# bio-data-visualization-network-visualization fixes

## 2026-09-27

| finding | priority | change | verified (ran / help / docs) | notes |
| --- | --- | --- | --- | --- |
| `examples/cytoscape_automation.py` fails silently | P1 | Removed the invalid `mapping_type` argument from `set_node_shape_mapping`, populated every mapped column before upload, replaced the swallowing handler with traceback plus nonzero failure, resolved exports to absolute paths, and enabled `overwrite_file=True`. Added optional GraphML input. | **Ran:** py4cytoscape 1.13.0 against Cytoscape 3.10.4 under Xvfb. The demo and the 100-node/511-edge audit GraphML both created networks, applied `PPIStyle`, and exported non-empty PDF/PNG twice without collision. Demo PNG visibly contains diamond kinase nodes; audit PNG and PDFs parse. | No broad exception remains. The private Cytoscape process group was stopped; REST port 1234 was confirmed down. |
| Community legend mislabels communities | P1 | `examples/network_plots.py` now uses one resampled `Set2` palette for both node RGBA values and legend swatches. | **Ran:** regression asserts each node color equals `palette[membership]`; the audit GraphML rendered 100 nodes and 4 communities. Opened PNG shows all four swatches matching node colors. | Original normalized scalar colors and direct integer palette lookup disagreed for 3/4 groups. |
| PyVis mutates edge weights and loses direction | P1 | Basic conversion now uses `graph.copy()`; styled conversion adds nodes/edges explicitly; communities are computed first; palette is defined; both networks set `directed=graph.is_directed()`; HTML assets are inlined. | **Ran:** pyvis 0.3.2 regression preserves a directed edge's `weight=0.75` and finds the `to` arrow in HTML. Audit GraphML produced 100-node/511-edge basic and styled HTML (744,892 and 760,431 bytes) with audit node IDs present. | No caller graph is handed directly to mutating `from_nx`. |
| SKILL code blocks are not runnable | P1 | Replaced fragments with executable CLIs: `scripts/layouts.py`, `scripts/ggraph_layouts.R`, and `scripts/edge_bundling.R`; routed static/PyVis/Cytoscape workflows to corrected examples. The bundling script defines the flare hierarchy and both endpoint indices. | **Ran:** all Python files compile. R scripts executed through `r.sh`; ggraph rendered `fr`, `kk`, and `circle` with all 100 audit nodes; bundling rendered 764 connections. | The dangling R `+`, undefined `np`, and undefined `graph`/indices are gone. |
| Description promises recipes that do not exist | P1 | Kept only capabilities backed by runnable paths: native NetworkX ForceAtlas2, R hierarchical bundling, static NetworkX, PyVis, signed directed Graphviz, and Cytoscape. Deleted unsupported HiveNetX/hive-plot, Datashader, and adjustText claims. | **Ran:** networkx 3.6.1 rendered spring, Kamada-Kawai, circular, spectral, and native ForceAtlas2 on all 100 audit nodes; every coordinate set was finite and every PNG non-blank. R bundling executed as above. | HiveNetX does not exist on PyPI; deleting the unsupported promise was the bounded correction. |
| Hub labels and edge widths are not adaptive | P2 | Replaced fixed degree cutoff guidance with capped ranked top-k labels. Added a helper that reads `data.get('weight', 1.0)`, handles constant/unweighted graphs, and rescales widths to 0.5-4 points. | **Ran:** regression on an unweighted path returns three widths in range; the 100-node audit network renders normalized widths and ranked hubs. | Exact operational threshold now has one home in `SKILL.md`. |
| Directed regulatory networks lack a styling recipe | P2 | Added `scripts/directed_network.py`: directed GraphML, Graphviz `dot`, arrowheads, and activation/repression colors; documented both pydot and Graphviz prerequisites. | **Ran:** pydot 4.0.1 + Graphviz 13.1.2 under WSL rendered the 65-node/124-edge signed audit GRN; PNG is 685,804 bytes, non-white fraction 0.135, and visual inspection confirms arrows plus both sign colors. | Script rejects undirected inputs instead of silently discarding direction. |
| Stale or inexact statements | P2 | Uses native `nx.forceatlas2_layout` for networkx 3.4+; removed the inaccurate graphopt/OpenOrd comment and duplicate PyVis heading; Cytoscape exports use resolved absolute paths. | **Ran:** native ForceAtlas2 rendered 100 finite positions; live Cytoscape wrote the requested absolute paths and overwrote them on subsequent runs. | Version text records the tested 2026-09-27 stack. |

### Deduplication, split, and executable moves

- Split the original 318-line `SKILL.md` to 207 lines. Method-specific material now lives in
  `references/python-layouts.md`, `references/r-layouts.md`, and
  `references/interactive-and-cytoscape.md`; the decision-tree rows and Reference Files index point to
  the appropriate file. The main file plus references contain 326 total / 225 non-blank lines versus
  318 total / 220 non-blank originally; intentional deletions are itemized below. All Markdown fences
  are balanced.
- Moved/repaired the old Python layout block to `scripts/layouts.py`, the ggraph layout block to
  `scripts/ggraph_layouts.R`, and the undefined bundling fragment to `scripts/edge_bundling.R`.
- Moved/repaired the old static, PyVis, and Cytoscape inline workflows to the already shipped
  `examples/network_plots.py`, `examples/interactive_network.py`, and
  `examples/cytoscape_automation.py`; `SKILL.md` retains only short invocations.
- Deleted `usage-guide.md` prerequisites, agent workflow, thresholds, and tips because their canonical
  homes are the Version Compatibility, Core Workflow, Failure Modes, and Quantitative Thresholds
  sections of `SKILL.md`. The guide now contains only an overview, prompts, and related Skills.
- Deleted unsupported HiveNetX/hive-plot, Datashader, and adjustText passages rather than advertising
  methods with no executable. Deleted the inaccurate graphopt-as-OpenOrd sentence. ForceAtlas2 and
  hierarchical bundling remain, each backed by a tested script.

### Validation summary

- Focused Python regression: PASS for community palette identity, unweighted edge widths, PyVis graph
  immutability, and directed arrow serialization.
- Audit-data executions: 5 Python layouts, 4 static views, 2 standalone PyVis documents, 3 R layouts,
  one signed directed Graphviz view, and one live Cytoscape PDF/PNG pair.
- Fixture execution: 764-connection ggraph flare bundling and live Cytoscape demo proving discrete
  kinase shapes.
- Render assertions: every PNG parsed at more than 100 px per side and non-white fraction above 0.001;
  both Cytoscape PDFs have valid `%PDF-` headers. Representative static, directed, bundling, and
  Cytoscape PNGs were opened and inspected.
- Audit data under `F:\OpenScience\audits\bio-data-visualization-network-visualization\data` was read
  only. No finding is left unfixed.

## 2026-09-27 round-2 follow-up

| finding | priority | change | verified (ran / help / docs) | notes |
| --- | --- | --- | --- | --- |
| Apply the adaptive label cap in every static view | P1 | Added one degree-ranked adaptive-label helper, reused its dictionary in all four static panels, and added repeatable `--label NODE` support for prespecified genes of interest. | **ran**: the focused regression intercepted all four label calls on a 100-node graph and proved they receive the same capped dictionary; the 100-node/511-edge audit PPI rendered four figures and the community figure was opened at original resolution. | The hub panel still emphasizes its top five nodes, but label eligibility is now consistent. |
| Reject unknown regulatory sign values | P2 | Added a pre-layout domain validator that raises a `ValueError` listing unknown values and the required `+`/`-` normalization. | **ran**: the unit probe rejected `activation`; the audit `natural_signs.graphml` rejected both `activation` and `repression` before Graphviz and wrote no image. | Missing attributes retain the documented activation default; explicit unknown values cannot disappear silently. |
| Make the Cytoscape export readable by default | P2 | Added a capped `display_label` node column, mapped it to `NODE_LABEL`, and called `fit_content()` after the force-directed layout. | **ran**: focused mocks asserted exactly 15 nonempty labels for 100 nodes, the label mapping call, and layout-then-fit order; py4cytoscape 1.13 signatures were inspected. | The reference tells users to suppress or reduce labels if a large export still crowds. |
| Remove duplicated PyVis headings | P2 | Saved with an empty template heading, removed template-generated heading blocks, and injected exactly one HTML-escaped title. | **ran**: directed PyVis regression retained arrows/immutability and asserted one `<h1>`; the 100-node styled audit HTML contains one heading and one title string. | The helper fails loudly if a future template omits `<body>`. |

Round-2 validation:

- `tests/test_network_recipes.py` passed the adaptive-label, sign-domain, PyVis heading, Cytoscape label, graph-immutability, edge-width, and community-color contracts.
- The current static CLI rendered four nonempty 100-node/511-edge audit figures; `network_communities.png` was opened and contains a capped readable label subset with matching legend colors.
- The current PyVis CLI emitted two self-contained audit HTML files; the styled file has exactly one `<h1>` and one `PPI Network with Communities` title.
- Native Python lacks `pydot`, so the unchanged normalized Graphviz render was not repeated there; the round-one independent audit already executed that route under WSL. The changed sign validator executes before that dependency and was exercised directly.
- Unfixed round-2 findings: none (4/4 fixed).

## 2026-09-27 round-3 follow-up

| finding | priority | change | verified (ran / help / docs) | notes |
| --- | --- | --- | --- | --- |
| Improve Cytoscape label legibility after fitting | P2 | Applied the final style before fitting; set an explicit 18-point label font and an 18-56 node-size range; expanded the force layout 2.4-fold across the landscape x axis; then deterministically spaced the capped labelled hubs around the layout perimeter in their original angular order and anchored each label outward before the final fit. Added focused operation-order, style-value, distinct-position, and anchor tests. | **ran**: the focused suite passed; Python compilation and `git diff --check` passed. A private Cytoscape 3.10.4 / py4cytoscape 1.13.0 run rendered the exact 100-node/511-edge audit GraphML to an 816x358 PNG and PDF, retained 15 labels, reported font size 18 and node widths 28.5-56, and produced 1,458.3 x 769.9 layout spans. The final PNG was opened at original resolution and all 15 capped labels are individually legible. | Evidence is under `F:\OpenScience\scratch\network-round3`; the private process group was stopped and REST port 1234 was confirmed down. |

Round-3 validation:

- Exact audit-size output: `ppi_network_round3.png` is 816x358 and 145,815 bytes;
  `ppi_network_round3.pdf` is 16,458 bytes.
- `tests/test_network_recipes.py` passes the earlier contracts plus final-style-before-fit,
  2.4-fold landscape spacing, 15 distinct hub positions, outward label anchors, the 18-point font,
  and the 18-56 node-size mapping.
- Unfixed round-3 findings: none (1/1 fixed).
