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


raw_graph = nx.read_graphml(ROOT / "data/natural_signs.graphml")
graphviz_called = False
original_layout = module.nx.nx_pydot.graphviz_layout


def forbidden_layout(*_args, **_kwargs):
    global graphviz_called
    graphviz_called = True
    raise AssertionError("Graphviz was called before sign validation")


module.nx.nx_pydot.graphviz_layout = forbidden_layout
try:
    try:
        module.render_directed(
            raw_graph, ROOT / "out/input10_raw_natural_signs.png", "regulation"
        )
    except ValueError as error:
        raw_rejection = str(error)
    else:
        raise AssertionError("Natural-language sign values were accepted")
finally:
    module.nx.nx_pydot.graphviz_layout = original_layout

results = {
    "input2_signed_grn": instrument("synth_grn.graphml", "input2_signed_grn.png", "sign"),
    "input10_raw_natural_signs": {
        "rejected": True,
        "error": raw_rejection,
        "graphviz_called": graphviz_called,
        "output_exists": (ROOT / "out/input10_raw_natural_signs.png").exists(),
    },
    "input10_normalized_signs": instrument(
        "normalized_signs.graphml", "input10_normalized_signs.png", "regulation"
    ),
}
assert results["input2_signed_grn"]["drawn_edges_total"] == results["input2_signed_grn"]["graph_edges"]
assert "activation" in results["input10_raw_natural_signs"]["error"]
assert "repression" in results["input10_raw_natural_signs"]["error"]
assert not graphviz_called
assert not results["input10_raw_natural_signs"]["output_exists"]
assert results["input10_normalized_signs"]["drawn_edges_total"] == results["input10_normalized_signs"]["graph_edges"]
(ROOT / "logs/wsl_directed_results.json").write_text(json.dumps(results, indent=2), encoding="utf-8")
print(json.dumps(results, indent=2))
