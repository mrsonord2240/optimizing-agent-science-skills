> **Audit record for `bio-data-visualization-network-visualization`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@64b3b15](https://github.com/mrsonord2240/bioSkills/tree/64b3b150c9b989c102f7ee69e0bb07c16842d894/data-visualization/network-visualization) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-20 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval viewer: bio-data-visualization-network-visualization

- Source: `mrsonord2240/bioSkills@64b3b150c9b989c102f7ee69e0bb07c16842d894:data-visualization/network-visualization` (unmodified upstream), first audit, evaluated 2026-09-20
- Category Data Analysis, Mode A, Complex, 8 inputs, **8/8 executed**
- **Final 74, Beta Only, not deployable.** No veto fired, no open P0. Static 71 (x0.4 = 28.4), execution average 76.1 (x0.6 = 45.7). Assertions 24/40 (60%), below the 80% floor, which alone would cap the grade at Beta Only.
- Environment: `F:\OpenScience\audit-envs\data-visualization` (`py.sh`, `r.sh`, WSL `science` env `dv-cli` with Cytoscape 3.10.4 headless under Xvfb, py4cytoscape 1.13.0, Graphviz 13.1.2 + pydot; headless Chrome for HTML). Every script is in `run/`; figures in `out/`.
- Data: SYNTHETIC `data/synth_ppi.graphml` (100 genes, 4 planted communities of 25, 3 planted hubs of degree 46-48, 511 weighted edges; `run/make_data.py`), SYNTHETIC `data/synth_grn.graphml` (5-TF cascade + 60 targets, 65 nodes, 124 directed signed edges), and the real `public-data/networks/string_tp53_neighbors.tsv` (STRING v12, 10 genes, 32 edges).

## Method

Each SKILL.md code block was extracted verbatim into `run/blocks/` and executed (blocks 1-7), then the three shipped examples were run from copies. Matplotlib output was audited from the live figure objects (`run/figaudit.py`: node/edge collections, size arrays, colour arrays, labels, arrow patches), PyVis HTML was parsed back to its node/edge JSON, Cytoscape state was read back through REST (node/edge counts, tables, `NODE_SIZE`, `NODE_FILL_COLOR`), and PNG/PDF/SVG outputs were opened.

## Skill veto and research veto

| Gate | Result |
| --- | --- |
| Skill veto (stability, contract, determinism, security) | PASS |
| Scientific integrity | PASS (HiveNetX does not exist on PyPI: a P1 gap, no fabricated result) |
| Practice boundaries | PASS |
| Methodological ground | PASS |
| Code usability | PASS, borderline: R block 2 is a parse error, block 4 uses undefined names, `cytoscape_automation.py` swallows a TypeError. Flagship static and interactive examples run correctly, so P1 and not a veto (consistent with the sibling data-visualization audits). |

Shipped means present: `SKILL.md`, `usage-guide.md`, `examples/network_plots.py`, `interactive_network.py`, `cytoscape_automation.py` all exist. No `references/` is claimed. The three related Skills (`coexpression-networks`, `interaction-databases`, `cell-communication`) exist.

## Static score 71/100

| Category | Score | Note |
| --- | --- | --- |
| Functional suitability | 8/12 | FA2, hive, Datashader, adjustText, Python bundling named but not coded; block 2 does not parse |
| Reliability | 6/12 | Correct numbers, but silent faults in the shipped examples |
| Performance / context | 6/8 | 320 lines, no references layer |
| Agent usability | 12/16 | Strong decision tree and failure modes; blocks are non-self-contained fragments |
| Human usability | 6/8 | Prompts for FA2/hive/bundling cannot be met |
| Security | 11/12 | Clean |
| Maintainability | 8/12 | Version line stale where it matters |
| Agent-specific | 14/20 | Good trigger; description over-promises |

## Inputs

| # | Type | Input | Basic | Spec. | Total | Assertions |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Canonical | SKILL static block, synthetic planted graph | 35 | 49 | 84 | 4/5 |
| 2 | Variant A | Layout block, GRN, Graphviz, FA2 | 32 | 46 | 78 | 3/5 |
| 3 | Variant B | Shipped `network_plots.py` | 33 | 47 | 80 | 4/5 |
| 4 | Variant B | R: ggraph/igraph, bundling | 32 | 45 | 77 | 3/5 |
| 5 | Edge | PyVis HTML | 29 | 41 | 70 | 2/5 |
| 6 | Stress | Cytoscape headless + real STRING + export | 31 | 45 | 76 | 3/5 |
| 7 | Scope Boundary | Promised vs shipped, layout-artifact claim, scale | 29 | 39 | 68 | 2/5 |
| 8 | Adversarial | Awkward graphs, two-condition, real STRING | 31 | 45 | 76 | 3/5 |

Execution average 76.1. Layer 1 average 31.5/40, Layer 2 average 44.6/60.

### Input 1: SKILL static block on the planted graph (`run/i1_static.py`)

Block 5 was exec'd verbatim with `G` loaded and `plt.savefig` hooked to capture the figure. Printed:

```
drawn nodes 100 graph nodes 100
drawn edge segments 511 graph edges 511
size mapping exact: True
n communities 4 sizes [24, 25, 25, 26]
color array equals community idx: True
ARI vs planted blocks 0.973
louvain n 4 ARI greedy vs louvain 0.973
labels drawn 43 nodes with degree>=10 43 planted hubs [G000,G025,G050] labelled? [True, True, True]
layout reproducible same seed: True | differs other seed: True | drawn positions equal spring_layout(seed=42): True
edge widths unique [0.5]
```

`out/i1_static.png` opened: non-blank, readable but a hairball; 43 overlapping labels; no legend for size or community; four tab20 colours are picked by normalising 0..3 across the map (legend-less, so harmless here, but see input 3).

### Input 2: layouts, directed GRN, Graphviz (`run/i2_layouts.py`, `i7b_directed.py`, `i7c_dot.py`)

- Block 1 verbatim: `NameError: name 'np' is not defined`. `hub_nodes`, `periphery_nodes`, `top_nodes` are placeholders.
- With names supplied: spring, kamada_kawai, circular, shell, spectral, bipartite all return 100 finite positions; kk and spectral are deterministic without a seed; shell puts hubs at radius 0.5 and periphery at 1.0. `graphviz_layout` fails in the Windows venv (no pydot).
- WSL dv-cli, Graphviz `dot` on the GRN: 65 positions, TF0..TF4 y = 378, 306, 234, 162, 90, all 124 regulator->target edges point downward, layout identical on re-run.
- Networkx layered drawing of the DiGraph: 65/65 nodes, 124/124 arrow patches.
- `nx.forceatlas2_layout(G, seed=42)` exists in networkx 3.6.1 and is reproducible; the Skill never mentions it.

### Input 3: shipped `network_plots.py` (`run/i3_shipped_static.py`, `i3b_debug.py`, `i3c_legend.py`)

```
network_degree.png       nodes 30 edge segs 56 labels 30
network_communities.png  nodes 30 edge segs 56 labels 30
network_hubs.png         nodes 30 edge segs 56 labels 5
network_confidence.png   nodes 30 edge segs 56 labels 30
P1 size==100+150*deg: True  color==degree: True  edge widths == 2*weight: True
P3 labelled == top5 hubs: True ['Gene1','Gene2','Gene5','Gene6','Gene9']
P4 edge colours match thresholds: True {'#cccccc': 27, '#f39b7f': 22, '#e64b35': 7}
community 1 node #66c2a5 legend #66c2a5 MATCH
community 2 node #8da0cb legend #fc8d62 MISMATCH
community 3 node #ffd92f legend #8da0cb MISMATCH
community 4 node #b3b3b3 legend #e78ac3 MISMATCH
```

The community figure (opened) shows yellow and grey nodes that the legend calls orange and pink. Mechanism: `nx.draw_networkx_nodes(node_color=[0..3], cmap=Set2)` normalises 0..3 across the whole map while the legend uses `palette(i)`.

### Input 4: R route (`run/i6_r.R`)

```
igraph 2.3.0 ggraph 2.2.2 ggplot2 4.0.3
block 2 verbatim: PARSE ERROR: <text>:9:0: unexpected end of input  (dangling '+' after the graphopt line)
layout fr / kk / circle / graphopt: nodes drawn 100 (graph 100), 511 edge groups each
ggraph fr same seed identical: TRUE | other seed differs: TRUE | no set.seed: two calls identical: FALSE | kk deterministic: TRUE
louvain communities: 4, modularity 0.585; contingency block x community = diag(25,25,25,25)
node table matches degree: TRUE  colour col matches louvain: TRUE
block 4 verbatim: ERROR: No layout function defined for objects of class <function>
block 4 on ggraph flare (graph/from_idx/to_idx defined): connections 764, paths in layer 764
```

`out/i6_comm.png` (four clean clusters, hubs large, degree and edge-weight legends) and `out/i6_bundle.png` (circular dendrogram with bundled arcs) opened.

### Input 5: PyVis (`run/i4_pyvis.py`)

```
network_basic.html  bytes 15244 nodes 40 edges 76 (graph 40/76)
network_styled.html bytes 17068 nodes 40 edges 76
styled: size==10+5*deg True  colour==palette[community] True  edge set equals graph True
G edge attrs after example ran: {'score': 624, 'width': 0.6247}  any edge still has weight: False
styled edge widths distinct values: [1.5]   (intended 3*weight, 1.2-3.0)
SKILL block verbatim: NameError palette ; with palette: 40 nodes, 76 edges, size ok, colour ok, tooltips ok
Network().from_nx(DiGraph): arrows in edges? False ; Network(directed=True): 124/124 'to'
2000-node HTML 312683 bytes
```

Headless-Chrome screenshot `out/ex_pyvis/styled.png` opened: 4 coloured communities, hubs large, controls present, heading rendered twice.

### Input 6: Cytoscape (`run/i5_run.sh` + `i5_cyto_skill.py`, `i5b`, `i5c`, `i5d`, `i5e`, `i5f`)

```
SKILL block 7 verbatim on synth_ppi: cytoscape nodes 100 / graph 100, edges 511 / 511; degree column matches nx: True
G000 degree 46 NODE_SIZE 120.0 FILL #BD0026 ; G001 deg 9 -> 76.0 #FD9A4C ; G030 deg 7 -> 68.0 #FEB36C   (60 + (d-5)/15*60 checks)
network.pdf 14681 B; 2nd run: CyError "This file already exists and will not be overwritten: network.pdf"
shipped cytoscape_automation.py: prints 'Cytoscape is running.', 'Network created (SUID 128)'; then nothing.
  with the bare except replaced by traceback.print_exc(): TypeError: set_node_shape_mapping() got an unexpected keyword argument 'mapping_type'
  files written: []   ATM shape: ELLIPSE (should be DIAMOND)
graph without 'degree' attribute: no error, mapping on absent column silently ignored (G000 size 50 default)
real STRING (10 nodes, 32 edges): Cytoscape 10/32; exports png 28616 B, pdf 2322 B, svg 22801 B; GraphML re-read by networkx 10/32; SIF 32 lines, Cytoscape SIF import 10/32
directed GRN: create_network_from_networkx 65/124; default EDGE_TARGET_ARROW_SHAPE 'NONE'; hierarchical layout ok
force-directed twice in Cytoscape gives identical positions (deterministic per network)
```

PNG (`out/cyto2/string.png`) and the PDF rendered with Ghostscript (`out/cyto2/string_pdf.png`) opened: the same 10-gene network, labels overlap under the circular layout. Cytoscape's own GraphML import in a session that has already imported networks sometimes reports one extra node named after the network (tool behaviour, out of Skill scope; the `create_network_from_networkx` route gave exact counts). One early import returned an HTTP 500 immediately after Cytoscape started and succeeded on retry (not counted against the Skill).

### Input 7: promised versus shipped (`run/i8_layout_artifact.py`, timings in `run/i7_edge.py`)

```
seed 1..5 closest planted block pair: (0,1) (0,1) (1,3) (1,3) (1,3)   -> layout distances change with the seed although blocks are symmetric
forceatlas: only inside pyvis options (block 6) | fa2, HiveNetX, pyveplot, datashader, adjustText, geom_conn_bundle: no executable python block (hive = comment lines)
pip index: fa2_modified 0.4 yes | pyveplot 1.0.2 yes | HiveNetX: No matching distribution
spring_layout 500 nodes / 1491 edges 1.7 s ; 2000 / 5991 18.6 s ; 5000 / 14991 104.4 s ; nx.forceatlas2_layout 2000 nodes 18.5 s
```

### Input 8: awkward graphs (`run/i7_edge.py`)

```
union layout draws A and B; layout of A only for B -> NetworkXError: Node 'X1' has no position
edge width one-liner on unweighted graph -> KeyError 'weight' ; raw weights 0.106-0.999 (sub-point widths, no normalisation shown)
directed random (30) OK 30/30 nodes (arrow patches, 0 LineCollection edges) ; self loop 512/512 ; 5 isolates 105/105 ; two components 10/10 ; empty 0/0 ; single edge 2/2 ; int ids 3/3
real STRING TP53 axis: 10/10 nodes 32/32 edges, communities 2, labelled 0   (max degree 9 < 10)
pdf 6683 B, %PDF-1.4
```

## Recommendations (see the JSON for full text)

- **P1** `examples/cytoscape_automation.py` fails silently: drop `mapping_type` from `set_node_shape_mapping`, replace the bare `except: pass`, add `overwrite_file=True`.
- **P1** Community legend in `network_plots.py` disagrees with node colours for 3 of 4 communities.
- **P1** PyVis `from_nx` pops `weight` into `width` and mutates the caller's graph: the styled example loses edge weights; SKILL PyVis block uses undefined `palette`; no `directed=True` guidance.
- **P1** SKILL.md blocks not runnable as written (`np`, R block 2 parse error, block 4 undefined names, Cytoscape block never sets `degree`).
- **P1** ForceAtlas2, hive, Datashader, adjustText, Python bundling promised without code; HiveNetX not on PyPI; the usage-guide 5000-node prompt cannot be met.
- **P2** Fixed `degree >= 10` hub rule (43/100 and 0/10 labels), unguarded edge-width lookup; no directed-GRN styling recipe (arrows, sign, pydot/Graphviz prerequisite); stale statements (native `nx.forceatlas2_layout`, graphopt is not OpenOrd, duplicated PyVis heading, relative Cytoscape export path).

## Housekeeping

- No writes into `F:\OpenScience\external\`; no `__pycache__` anywhere (checked with `find`). Skill copy at `run/skill/`.
- Own Cytoscape/Java/Xvfb processes stopped after each WSL run; the one earlier `pkill -f cytoscape` inside the stock `wsl_cytoscape.sh stop` terminated only that helper shell. A pre-existing `Xvfb :99` in WSL belongs to another session and was left alone. No Rscript was killed.
- `BACKLOG.md` / `INDEX.md` not touched; nothing committed.
