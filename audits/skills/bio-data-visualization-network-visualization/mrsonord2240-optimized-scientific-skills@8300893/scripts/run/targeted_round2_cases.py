"""Independent round-2 probes for label, PyVis, sign, and Cytoscape fixes."""

from __future__ import annotations

import importlib.util
import json
import tempfile
from pathlib import Path
from unittest.mock import patch

import networkx as nx


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "run/skill"
OUT = ROOT / "out"
LOGS = ROOT / "logs"


def load_module(name: str, relative: str):
    spec = importlib.util.spec_from_file_location(name, SKILL / relative)
    if spec is None or spec.loader is None:
        raise RuntimeError(relative)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def input11_requested_labels_and_heading() -> dict[str, object]:
    """Use a new graph size and retain a deliberately low-degree requested label."""
    static = load_module("network_static_round2", "examples/network_plots.py")
    interactive = load_module("network_interactive_round2", "examples/interactive_network.py")
    graph = nx.barabasi_albert_graph(61, 2, seed=17)
    graph = nx.relabel_nodes(graph, {node: f"R{node:03d}" for node in graph})
    for index, (u, v) in enumerate(graph.edges()):
        graph[u][v]["weight"] = 0.4 + (index % 50) / 100
        graph[u][v]["score"] = int(graph[u][v]["weight"] * 1000)
    requested = min(graph, key=lambda node: (graph.degree(node), node))
    expected = static.adaptive_labels(graph, [requested])
    ranked_only = static.adaptive_labels(graph)
    assert requested not in ranked_only
    assert requested in expected
    assert len(expected) == 16

    seen: list[dict[str, str]] = []
    original = static.nx.draw_networkx_labels

    def capture(*args, **kwargs):
        seen.append(dict(kwargs["labels"]))
        return original(*args, **kwargs)

    target = OUT / "input11_requested_labels"
    with patch.object(static.nx, "draw_networkx_labels", capture):
        images = static.render_networks(graph, target, [requested])
    assert len(images) == 4 and all(path.stat().st_size > 2000 for path in images)
    assert len(seen) == 4 and all(labels == expected for labels in seen)

    html_path = target / "requested_labels_pyvis.html"
    interactive.create_styled_network(graph, html_path, "Requested <Marker> Network")
    html = html_path.read_text(encoding="utf-8")
    assert html.count("<h1>") == 1
    assert html.count("Requested &lt;Marker&gt; Network") == 1
    assert "Requested <Marker> Network" not in html
    return {
        "nodes": len(graph),
        "requested_low_degree_node": requested,
        "adaptive_label_count": len(expected),
        "identical_label_calls": len(seen),
        "images": [str(path.relative_to(ROOT)) for path in images],
        "html_bytes": html_path.stat().st_size,
        "h1_count": html.count("<h1>"),
        "escaped_title_count": html.count("Requested &lt;Marker&gt; Network"),
    }


def input12_preflight_and_cytoscape_cap() -> dict[str, object]:
    """Prove pre-layout sign rejection and the upper Cytoscape label cap/fit order."""
    directed = load_module("directed_round2", "scripts/directed_network.py")
    cytoscape = load_module("cytoscape_round2", "examples/cytoscape_automation.py")

    regulatory = nx.DiGraph()
    regulatory.add_edge("TF_A", "target_1", sign="+")
    regulatory.add_edge("TF_B", "target_2", sign="inhibition")
    layout_called = False

    def forbidden_layout(*_args, **_kwargs):
        nonlocal layout_called
        layout_called = True
        raise AssertionError("Graphviz was called before validation")

    with patch.object(directed.nx.nx_pydot, "graphviz_layout", forbidden_layout):
        try:
            directed.render_directed(
                regulatory, OUT / "input12_should_not_exist.png", "sign"
            )
        except ValueError as error:
            rejection = str(error)
        else:
            raise AssertionError("Unknown sign was accepted")
    assert "inhibition" in rejection
    assert not layout_called
    assert not (OUT / "input12_should_not_exist.png").exists()

    graph = nx.path_graph([f"C{i:04d}" for i in range(2000)])
    cytoscape.prepare_style_attributes(graph)
    labels = nx.get_node_attributes(graph, "display_label")
    assert len(labels) == 2000
    assert sum(bool(value) for value in labels.values()) == 30

    order: list[str] = []
    with (
        patch.object(cytoscape.p4c, "create_network_from_networkx", return_value=91),
        patch.object(
            cytoscape.p4c,
            "layout_network",
            side_effect=lambda *_args, **_kwargs: order.append("layout"),
        ),
        patch.object(
            cytoscape.p4c,
            "fit_content",
            side_effect=lambda *_args, **_kwargs: order.append("fit"),
        ),
    ):
        suid = cytoscape.send_network_to_cytoscape(graph, title="Cap probe")
    assert suid == 91
    assert order == ["layout", "fit"]

    with (
        patch.object(cytoscape.p4c, "create_visual_style"),
        patch.object(cytoscape.p4c, "set_node_size_mapping"),
        patch.object(cytoscape.p4c, "set_node_color_mapping"),
        patch.object(cytoscape.p4c, "set_edge_line_width_mapping"),
        patch.object(cytoscape.p4c, "set_node_shape_mapping"),
        patch.object(cytoscape.p4c, "set_node_label_mapping") as node_label,
        patch.object(cytoscape.p4c, "set_visual_style"),
    ):
        cytoscape.apply_ppi_style()
    node_label.assert_called_once_with("display_label", style_name="PPIStyle")
    return {
        "unknown_sign_rejected": True,
        "rejection": rejection,
        "graphviz_called": layout_called,
        "cytoscape_nodes": len(graph),
        "nonempty_display_labels": sum(bool(value) for value in labels.values()),
        "label_mapping_column": "display_label",
        "layout_fit_order": order,
    }


def main() -> None:
    results = {
        "input11": input11_requested_labels_and_heading(),
        "input12": input12_preflight_and_cytoscape_cap(),
    }
    target = LOGS / "round2_targeted_results.json"
    target.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
