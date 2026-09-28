"""Execute and independently assert the Python portions of audit inputs 1-3, 5, 7-9."""

from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

import networkx as nx
import numpy as np
from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT = ROOT / "out"
LOGS = ROOT / "logs"
SKILL = ROOT / "run" / "skill"
LOGS.mkdir(parents=True, exist_ok=True)
RESULTS: dict[str, object] = {}


def run_cli(name: str, args: list[str], expected: set[int] | None = None) -> dict[str, object]:
    start = time.perf_counter()
    proc = subprocess.run(
        [sys.executable, *args],
        cwd=SKILL,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1", "MPLBACKEND": "Agg"},
    )
    result = {
        "returncode": proc.returncode,
        "seconds": round(time.perf_counter() - start, 3),
        "stdout": proc.stdout,
        "stderr": proc.stderr,
    }
    if expected is not None and proc.returncode not in expected:
        raise AssertionError(f"{name}: return code {proc.returncode}, expected {expected}\n{proc.stderr}")
    return result


def load_module(name: str, relative: str):
    spec = importlib.util.spec_from_file_location(name, SKILL / relative)
    if spec is None or spec.loader is None:
        raise RuntimeError(relative)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def image_info(path: Path) -> dict[str, object]:
    image = Image.open(path).convert("RGB")
    array = np.asarray(image)
    nonwhite = float(np.mean(np.any(array < 250, axis=2)))
    info = {
        "bytes": path.stat().st_size,
        "width": image.width,
        "height": image.height,
        "nonwhite": round(nonwhite, 6),
    }
    assert image.width > 100 and image.height > 100
    assert path.stat().st_size > 2000 and nonwhite > 0.001
    return info


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def input1_static_ppi() -> None:
    target = OUT / "input1_static_ppi"
    result = run_cli(
        "input1",
        [
            str(SKILL / "examples" / "network_plots.py"),
            "--graphml",
            str(DATA / "synth_ppi.graphml"),
            "--output-dir",
            str(target),
        ],
        {0},
    )
    graph = nx.read_graphml(DATA / "synth_ppi.graphml")
    module = load_module("network_plots_i1", "examples/network_plots.py")
    widths = module.visible_edge_widths(graph)
    communities, membership, colors = module.community_style(graph)
    palette = module.plt.colormaps["Set2"].resampled(len(communities))
    expected_colors = [palette(membership[node]) for node in graph]
    assert colors == expected_colors
    assert len(widths) == graph.number_of_edges()
    assert min(widths) >= 0.5 and max(widths) <= 4.0
    images = {p.name: image_info(p) for p in sorted(target.glob("*.png"))}
    assert len(images) == 4
    RESULTS["input1"] = {
        **result,
        "nodes": graph.number_of_nodes(),
        "edges": graph.number_of_edges(),
        "communities": len(communities),
        "legend_node_palette_exact": True,
        "edge_width_range": [min(widths), max(widths)],
        "images": images,
    }


def input2_layouts() -> None:
    target = OUT / "input2_layouts"
    result = run_cli(
        "input2 layouts",
        [
            str(SKILL / "scripts" / "layouts.py"),
            str(DATA / "synth_ppi.graphml"),
            "--output-dir",
            str(target),
        ],
        {0},
    )
    expected = {"spring", "kamada-kawai", "circular", "spectral", "forceatlas2"}
    images = {p.stem: image_info(p) for p in sorted(target.glob("*.png"))}
    assert set(images) == expected
    module = load_module("layouts_i2", "scripts/layouts.py")
    graph = nx.read_graphml(DATA / "synth_ppi.graphml")
    p1 = module.compute_layout(graph, "spring")
    p2 = module.compute_layout(graph, "spring")
    assert all(np.allclose(p1[node], p2[node]) for node in graph)
    RESULTS["input2_python"] = {
        **result,
        "layouts": images,
        "spring_seed_reproducible": True,
        "graph_nodes": len(graph),
    }


def input3_shipped_demo() -> None:
    target = OUT / "input3_shipped_demo"
    result = run_cli(
        "input3",
        [str(SKILL / "examples" / "network_plots.py"), "--output-dir", str(target)],
        {0},
    )
    images = {p.name: image_info(p) for p in sorted(target.glob("*.png"))}
    assert len(images) == 4
    module = load_module("network_plots_i3", "examples/network_plots.py")
    graph = module.build_demo_graph()
    communities, membership, colors = module.community_style(graph)
    palette = module.plt.colormaps["Set2"].resampled(len(communities))
    assert colors == [palette(membership[node]) for node in graph]
    RESULTS["input3"] = {
        **result,
        "images": images,
        "legend_node_palette_exact": True,
        "nodes": len(graph),
        "edges": graph.number_of_edges(),
    }


def input5_pyvis() -> None:
    target = OUT / "input5_pyvis"
    source_hash = file_hash(DATA / "synth_ppi.graphml")
    result = run_cli(
        "input5",
        [
            str(SKILL / "examples" / "interactive_network.py"),
            "--graphml",
            str(DATA / "synth_ppi.graphml"),
            "--output-dir",
            str(target),
        ],
        {0},
    )
    assert file_hash(DATA / "synth_ppi.graphml") == source_hash
    module = load_module("interactive_i5", "examples/interactive_network.py")
    graph = nx.read_graphml(DATA / "synth_ppi.graphml")
    before = copy.deepcopy(dict(graph.edges))
    direct = target / "direct_function.html"
    module.create_interactive_network(graph, direct)
    assert dict(graph.edges) == before
    html_files = {}
    for path in sorted(target.glob("*.html")):
        text = path.read_text(encoding="utf-8")
        assert path.stat().st_size > 100_000
        assert "vis-network.min.js" in text
        assert all(str(node) in text for node in list(graph)[:10])
        html_files[path.name] = {
            "bytes": path.stat().st_size,
            "inline_assets": True,
            "sample_nodes_present": True,
        }
    RESULTS["input5"] = {
        **result,
        "html": html_files,
        "caller_graph_unchanged": True,
        "source_graphml_unchanged": True,
    }


def input7_scope_and_artifact() -> None:
    text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    required = [
        "scripts/layouts.py",
        "scripts/directed_network.py",
        "scripts/edge_bundling.R",
        "examples/network_plots.py",
        "examples/interactive_network.py",
        "examples/cytoscape_automation.py",
    ]
    missing = [item for item in required if not (SKILL / item).exists()]
    assert not missing
    assert "HiveNetX" not in text and "Datashader" not in text and "adjustText" not in text
    graph = nx.read_graphml(DATA / "synth_ppi.graphml")
    same_a = nx.spring_layout(graph, seed=42)
    same_b = nx.spring_layout(graph, seed=42)
    different = nx.spring_layout(graph, seed=43)
    max_same = max(float(np.linalg.norm(same_a[n] - same_b[n])) for n in graph)
    max_diff = max(float(np.linalg.norm(same_a[n] - different[n])) for n in graph)
    assert max_same == 0.0 and max_diff > 0.01
    start = time.perf_counter()
    scale_graph = nx.barabasi_albert_graph(1200, 3, seed=42)
    positions = nx.forceatlas2_layout(scale_graph, seed=42, max_iter=50)
    seconds = time.perf_counter() - start
    assert len(positions) == 1200 and np.isfinite(np.asarray(list(positions.values()))).all()
    RESULTS["input7"] = {
        "missing_routes": missing,
        "unsupported_claims_removed": True,
        "same_seed_max_delta": max_same,
        "different_seed_max_delta": max_diff,
        "forceatlas2_1200_nodes_seconds": round(seconds, 3),
        "forceatlas2_positions": len(positions),
    }


def input8_awkward() -> None:
    target = OUT / "input8_awkward"
    result = run_cli(
        "input8 awkward",
        [
            str(SKILL / "examples" / "network_plots.py"),
            "--graphml",
            str(DATA / "awkward_unweighted.graphml"),
            "--output-dir",
            str(target),
        ],
        {0},
    )
    images = {p.name: image_info(p) for p in sorted(target.glob("*.png"))}
    module = load_module("network_plots_i8", "examples/network_plots.py")
    awkward = nx.read_graphml(DATA / "awkward_unweighted.graphml")
    widths = module.visible_edge_widths(awkward)
    assert len(widths) == 3 and len(set(widths)) == 1 and 0.5 <= widths[0] <= 4.0
    control = nx.read_graphml(DATA / "control.graphml")
    treatment = nx.read_graphml(DATA / "treatment.graphml")
    union = nx.compose(control, treatment)
    shared = nx.spring_layout(union, seed=42)
    assert set(control).issubset(shared) and set(treatment).issubset(shared)
    empty = run_cli(
        "input8 empty",
        [
            str(SKILL / "scripts" / "layouts.py"),
            str(DATA / "empty.graphml"),
            "--output-dir",
            str(target / "empty"),
        ],
        {1},
    )
    singleton = run_cli(
        "input8 singleton",
        [
            str(SKILL / "scripts" / "layouts.py"),
            str(DATA / "singleton.graphml"),
            "--output-dir",
            str(target / "singleton"),
            "--layouts",
            "spring,circular",
        ],
        None,
    )
    RESULTS["input8"] = {
        **result,
        "images": images,
        "unweighted_widths": widths,
        "shared_union_layout_covers_both": True,
        "empty_returncode": empty["returncode"],
        "empty_error_mentions_empty": "empty" in str(empty["stderr"]).lower(),
        "singleton": singleton,
    }


def input9_directed_pyvis_cli() -> None:
    target = OUT / "input9_directed_pyvis"
    result = run_cli(
        "input9",
        [
            str(SKILL / "examples" / "interactive_network.py"),
            "--graphml",
            str(DATA / "synth_grn.graphml"),
            "--output-dir",
            str(target),
        ],
        None,
    )
    html = {}
    graph = nx.read_graphml(DATA / "synth_grn.graphml")
    for path in sorted(target.glob("*.html")):
        text = path.read_text(encoding="utf-8")
        html[path.name] = {
            "bytes": path.stat().st_size,
            "directed_arrow_token": bool(
                re.search(r'"arrows"\s*:\s*"to"', text)
                or re.search(r'"arrows"\s*:\s*\{', text)
            ),
            "sample_nodes_present": all(str(node) in text for node in list(graph)[:10]),
        }
    assert len(html) == 2
    assert all(item["bytes"] > 100_000 for item in html.values())
    assert all(item["directed_arrow_token"] for item in html.values())
    RESULTS["input9"] = {
        **result,
        "html": html,
        "nodes": len(graph),
        "edges": graph.number_of_edges(),
    }


def main() -> None:
    input1_static_ppi()
    input2_layouts()
    input3_shipped_demo()
    input5_pyvis()
    input7_scope_and_artifact()
    input8_awkward()
    input9_directed_pyvis_cli()
    path = LOGS / "python_results.json"
    path.write_text(json.dumps(RESULTS, indent=2), encoding="utf-8")
    print(json.dumps(RESULTS, indent=2))


if __name__ == "__main__":
    main()
