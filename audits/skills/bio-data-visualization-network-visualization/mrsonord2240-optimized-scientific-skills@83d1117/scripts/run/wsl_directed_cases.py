"""Run and instrument the signed Graphviz recipe under the WSL dv-cli environment."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import networkx as nx


ROOT = Path("/mnt/openscience/audits/bio-data-visualization-network-visualization")
SCRIPT = ROOT / "run/skill/scripts/directed_network.py"
spec = importlib.util.spec_from_file_location("directed_network_audit", SCRIPT)
if spec is None or spec.loader is None:
    raise RuntimeError(SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def instrument(input_name: str, output_name: str, attr: str) -> dict[str, object]:
    graph = nx.read_graphml(ROOT / "data" / input_name)
    observed: list[int] = []
    original = module.nx.draw_networkx_edges

    def wrapped(*args, **kwargs):
        observed.append(len(kwargs.get("edgelist", [])))
        return original(*args, **kwargs)

    module.nx.draw_networkx_edges = wrapped
    try:
        output = module.render_directed(graph, ROOT / "out" / output_name, attr)
    finally:
        module.nx.draw_networkx_edges = original
    return {
        "nodes": graph.number_of_nodes(),
        "graph_edges": graph.number_of_edges(),
        "drawn_edges_by_sign": observed,
        "drawn_edges_total": sum(observed),
        "bytes": output.stat().st_size,
    }


results = {
    "input2_signed_grn": instrument("synth_grn.graphml", "input2_signed_grn.png", "sign"),
    "input10_raw_natural_signs": instrument(
        "natural_signs.graphml", "input10_raw_natural_signs.png", "regulation"
    ),
    "input10_normalized_signs": instrument(
        "normalized_signs.graphml", "input10_normalized_signs.png", "regulation"
    ),
}
assert results["input2_signed_grn"]["drawn_edges_total"] == results["input2_signed_grn"]["graph_edges"]
assert results["input10_raw_natural_signs"]["drawn_edges_total"] == 0
assert results["input10_normalized_signs"]["drawn_edges_total"] == results["input10_normalized_signs"]["graph_edges"]
(ROOT / "logs/wsl_directed_results.json").write_text(json.dumps(results, indent=2), encoding="utf-8")
print(json.dumps(results, indent=2))
