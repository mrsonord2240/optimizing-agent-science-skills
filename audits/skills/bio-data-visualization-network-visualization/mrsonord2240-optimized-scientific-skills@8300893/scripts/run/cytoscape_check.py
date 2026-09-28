"""Exercise the copied Cytoscape automation and read back mapped state."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import networkx as nx
import py4cytoscape as p4c


ROOT = Path("/mnt/openscience/audits/bio-data-visualization-network-visualization")
SCRIPT = ROOT / "run/skill/examples/cytoscape_automation.py"
spec = importlib.util.spec_from_file_location("cytoscape_automation_audit", SCRIPT)
if spec is None or spec.loader is None:
    raise RuntimeError(SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

graph = nx.read_graphml(ROOT / "data/synth_ppi.graphml")
for node in graph:
    graph.nodes[node]["gene_type"] = "kinase" if node in {"G000", "G025", "G050"} else "other"
module.send_network_to_cytoscape(module.prepare_style_attributes(graph), title="Independent re-audit PPI")
style = module.apply_ppi_style()
out = ROOT / "out/input6_cytoscape"
pdf = module.export_figure(out / "ppi_network.pdf")
png = module.export_figure(out / "ppi_network.png", resolution=300)
# A second export proves overwrite behavior.
module.export_figure(out / "ppi_network.pdf")
module.export_figure(out / "ppi_network.png", resolution=300)

nodes = p4c.get_all_nodes()
edges = p4c.get_all_edges()
table = p4c.get_table_columns(
    "node", ["name", "degree", "gene_type", "display_label"]
)
degree = dict(graph.degree())
degree_match = all(int(row.degree) == degree[row["name"]] for _, row in table.iterrows())
display_labels = [value for value in table["display_label"].tolist() if str(value)]
kinase_shape = p4c.get_node_property(node_names=["G000"], visual_property="NODE_SHAPE")
other_shape = p4c.get_node_property(node_names=["G001"], visual_property="NODE_SHAPE")
edge_widths = p4c.get_edge_property(visual_property="EDGE_WIDTH")
results = {
    "style": style,
    "nodes": len(nodes),
    "edges": len(edges),
    "degree_match": degree_match,
    "nonempty_display_labels": len(display_labels),
    "display_label_names": sorted(display_labels),
    "kinase_shape": kinase_shape,
    "other_shape": other_shape,
    "edge_width_min": min(edge_widths.values()),
    "edge_width_max": max(edge_widths.values()),
    "pdf_bytes": pdf.stat().st_size,
    "png_bytes": png.stat().st_size,
    "overwrite_twice": True,
}
assert results["nodes"] == graph.number_of_nodes()
assert results["edges"] == graph.number_of_edges()
assert degree_match
assert results["nonempty_display_labels"] == 15
assert results["pdf_bytes"] > 1000 and results["png_bytes"] > 2000
assert "DIAMOND" in str(kinase_shape).upper()
assert "ELLIPSE" in str(other_shape).upper()
(ROOT / "logs/cytoscape_results.json").write_text(json.dumps(results, indent=2, default=str), encoding="utf-8")
print(json.dumps(results, indent=2, default=str))
