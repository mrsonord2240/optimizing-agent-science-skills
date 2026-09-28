"""Fresh final-pass probes: HTML injection resistance and the 500-node layout boundary."""

from __future__ import annotations

import copy
import importlib.util
import json
import os
from pathlib import Path
from unittest.mock import patch

import networkx as nx
import numpy as np
from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "run/skill"
DATA = ROOT / "data"
OUT = ROOT / "out"
LOGS = ROOT / "logs"


def load_module(name: str, relative: str):
    spec = importlib.util.spec_from_file_location(name, SKILL / relative)
    if spec is None or spec.loader is None:
        raise RuntimeError(relative)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def png_metrics(path: Path) -> dict[str, object]:
    image = Image.open(path).convert("RGB")
    array = np.asarray(image)
    nonwhite = float(np.mean(np.any(array < 250, axis=2)))
    assert path.stat().st_size > 2000
    assert image.width > 100 and image.height > 100
    assert nonwhite > 0.001
    return {
        "bytes": path.stat().st_size,
        "width": image.width,
        "height": image.height,
        "nonwhite": round(nonwhite, 6),
    }


def input13_adversarial_html() -> dict[str, object]:
    """Ensure an adversarial title is escaped and graph data remain immutable."""
    interactive = load_module("interactive_final_adversarial", "examples/interactive_network.py")
    static = load_module("static_final_adversarial", "examples/network_plots.py")
    graph = nx.DiGraph()
    nodes = ["TP53", "β-catenin", "MIR-21", "node/../../x", "EGFR", "AKT1"]
    graph.add_nodes_from(nodes)
    for index, (source, target) in enumerate(zip(nodes, nodes[1:] + nodes[:1], strict=True)):
        graph.add_edge(source, target, weight=0.8, score=800 + index)
    before = copy.deepcopy(dict(graph.edges))
    title = '</h1><script>window.__audit_injected = true</script><h1>'
    target = OUT / "input13_adversarial_html"
    basic = interactive.create_interactive_network(graph, target / "basic.html", title)
    styled = interactive.create_styled_network(graph, target / "styled.html", title)
    assert dict(graph.edges) == before

    escaped_fragment = "&lt;/h1&gt;&lt;script&gt;window.__audit_injected = true&lt;/script&gt;&lt;h1&gt;"
    html_results: dict[str, object] = {}
    for path in (basic, styled):
        document = path.read_text(encoding="utf-8")
        assert document.count("<h1>") == 1
        assert escaped_fragment in document
        assert "<script>window.__audit_injected = true</script>" not in document
        assert '"arrows": "to"' in document or '"arrows":"to"' in document
        assert all(
            node in document or json.dumps(node, ensure_ascii=True)[1:-1] in document
            for node in nodes
        )
        html_results[path.name] = {
            "bytes": path.stat().st_size,
            "h1_count": document.count("<h1>"),
            "title_escaped": True,
            "direction_serialized": True,
            "unicode_nodes_present": True,
        }

    widths = static.visible_edge_widths(graph)
    assert len(widths) == graph.number_of_edges()
    assert len(set(widths)) == 1
    assert 0.5 <= widths[0] <= 4.0
    return {
        "nodes": graph.number_of_nodes(),
        "edges": graph.number_of_edges(),
        "caller_graph_unchanged": True,
        "constant_weight_width": widths[0],
        "html": html_results,
    }


def input14_forceatlas_boundary() -> dict[str, object]:
    """Run native ForceAtlas2 immediately above the decision tree's 500-node boundary."""
    layouts = load_module("layouts_final_boundary", "scripts/layouts.py")
    graph = nx.barabasi_albert_graph(501, 3, seed=20260927)
    graph = nx.relabel_nodes(graph, {node: f"B{node:04d}" for node in graph})
    for source, target in graph.edges():
        graph[source][target]["weight"] = 1.0
        graph[source][target]["score"] = 1000
    fixture = DATA / "fresh_501_ppi.graphml"
    nx.write_graphml(graph, fixture)

    captured: list[dict[str, str]] = []
    original_labels = layouts.nx.draw_networkx_labels

    def capture_labels(*args, **kwargs):
        captured.append(dict(kwargs["labels"]))
        return original_labels(*args, **kwargs)

    output = OUT / "input14_forceatlas_boundary" / "forceatlas2.png"
    with patch.object(layouts.nx, "draw_networkx_labels", capture_labels):
        layouts.render_layout(graph, "forceatlas2", output)
    assert len(captured) == 1
    assert len(captured[0]) == 15

    first = layouts.compute_layout(graph, "forceatlas2")
    second = layouts.compute_layout(graph, "forceatlas2")
    deltas = [float(np.linalg.norm(first[node] - second[node])) for node in graph]
    assert max(deltas) == 0.0
    assert len(first) == 501
    assert np.isfinite(np.asarray(list(first.values()), dtype=float)).all()
    return {
        "fixture": str(fixture.relative_to(ROOT)),
        "nodes": graph.number_of_nodes(),
        "edges": graph.number_of_edges(),
        "positions": len(first),
        "finite_positions": True,
        "adaptive_label_count": len(captured[0]),
        "same_seed_max_delta": max(deltas),
        "image": png_metrics(output),
    }


def main() -> None:
    os.environ.setdefault("PYTHONDONTWRITEBYTECODE", "1")
    results = {
        "input13": input13_adversarial_html(),
        "input14": input14_forceatlas_boundary(),
    }
    target = LOGS / "fresh_final_results.json"
    target.write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(results, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
