"""Create deterministic boundary fixtures and the ten-input audit manifest."""

from __future__ import annotations

import json
from pathlib import Path

import networkx as nx


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)

    awkward = nx.Graph()
    awkward.add_nodes_from(["A", "B", "C", "D", "isolate-1", "isolate-2"])
    awkward.add_edges_from([("A", "B"), ("B", "C"), ("C", "D")])
    nx.write_graphml(awkward, DATA / "awkward_unweighted.graphml")

    empty = nx.Graph()
    nx.write_graphml(empty, DATA / "empty.graphml")
    singleton = nx.Graph()
    singleton.add_node("only-node")
    nx.write_graphml(singleton, DATA / "singleton.graphml")

    control = nx.Graph()
    control.add_edges_from([("A", "B"), ("B", "C"), ("C", "D")])
    treatment = nx.Graph()
    treatment.add_edges_from([("A", "B"), ("B", "C"), ("C", "E")])
    nx.write_graphml(control, DATA / "control.graphml")
    nx.write_graphml(treatment, DATA / "treatment.graphml")

    natural = nx.DiGraph()
    natural.add_edges_from(
        [
            ("TF1", "G1", {"regulation": "activation"}),
            ("TF1", "G2", {"regulation": "repression"}),
            ("TF2", "G2", {"regulation": "activation"}),
            ("TF2", "G3", {"regulation": "repression"}),
        ]
    )
    nx.write_graphml(natural, DATA / "natural_signs.graphml")
    normalized = natural.copy()
    mapping = {"activation": "+", "repression": "-"}
    for _, _, attrs in normalized.edges(data=True):
        attrs["regulation"] = mapping[attrs["regulation"]]
    nx.write_graphml(normalized, DATA / "normalized_signs.graphml")

    prompts = [
        {
            "index": 1,
            "type": "Canonical",
            "label": "Static PPI on planted communities",
            "prompt": "Render the supplied synthetic 100-node weighted PPI as reproducible static NetworkX figures. Size by degree, color by community, normalize edge widths, and label a capped set of hubs.",
            "regression_of": 1,
        },
        {
            "index": 2,
            "type": "Variant A",
            "label": "Layout comparison and signed GRN",
            "prompt": "Compare spring, Kamada-Kawai, circular, spectral, and native ForceAtlas2 layouts for the PPI, then render the directed signed GRN with Graphviz dot, arrows, and sign colors.",
            "regression_of": 2,
        },
        {
            "index": 3,
            "type": "Variant B",
            "label": "Shipped static demonstration",
            "prompt": "Run the shipped static PPI example and verify that node colors match every community legend swatch and that confidence widths remain visible.",
            "regression_of": 3,
        },
        {
            "index": 4,
            "type": "Variant B",
            "label": "R layouts and hierarchical bundling",
            "prompt": "Use the shipped R recipes to render FR, Kamada-Kawai, and circular layouts for the GraphML PPI, plus the executable hierarchical edge-bundling demonstration.",
            "regression_of": 4,
        },
        {
            "index": 5,
            "type": "Edge",
            "label": "Undirected PyVis supplement",
            "prompt": "Create basic and styled self-contained PyVis HTML supplements for the PPI without mutating the original edge weights; include degree sizing, communities, tooltips, and physics controls.",
            "regression_of": 5,
        },
        {
            "index": 6,
            "type": "Stress",
            "label": "Live Cytoscape automation",
            "prompt": "Send the 100-node attributed PPI to Cytoscape, apply degree, confidence, and gene-type mappings, and export overwriteable PNG and PDF files to the requested directory.",
            "regression_of": 6,
        },
        {
            "index": 7,
            "type": "Scope Boundary",
            "label": "Promised routes and layout-artifact claim",
            "prompt": "Audit whether every visualization route promised by the skill has a runnable path, and demonstrate that force-directed proximity changes with seed and must not be interpreted as biology.",
            "regression_of": 7,
        },
        {
            "index": 8,
            "type": "Adversarial",
            "label": "Awkward graphs and shared condition layout",
            "prompt": "Exercise the recipes on an unweighted disconnected graph with isolates, empty and singleton graphs, and control/treatment networks that must reuse one union layout.",
            "regression_of": 8,
        },
        {
            "index": 9,
            "type": "Variant A",
            "label": "Directed PyVis CLI end to end",
            "prompt": "Create a directed PyVis HTML supplement from the supplied signed GRN GraphML and report the network and community counts after the CLI completes.",
            "regression_of": None,
        },
        {
            "index": 10,
            "type": "Edge",
            "label": "Natural-language sign normalization",
            "prompt": "My regulatory edge attribute uses the values activation and repression. Normalize those values and render every edge with arrowheads and the correct two-color sign mapping; do not silently drop an unrecognized sign.",
            "regression_of": None,
        },
    ]
    (DATA / "input_manifest.json").write_text(
        json.dumps(prompts, indent=2), encoding="utf-8"
    )
    print("prepared", len(prompts), "inputs")


if __name__ == "__main__":
    main()
