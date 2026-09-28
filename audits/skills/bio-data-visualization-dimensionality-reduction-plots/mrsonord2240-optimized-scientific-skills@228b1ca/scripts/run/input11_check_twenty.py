"""New input 11: verify the 20-category end-to-end and loading-label contracts."""
from __future__ import annotations

from itertools import combinations
import importlib.util
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import scanpy as sc

ROOT = Path(r"F:\OpenScience\audits\bio-data-visualization-dimensionality-reduction-plots\run\twenty")
EXAMPLE = ROOT / "embedding_phd.py"
spec = importlib.util.spec_from_file_location("embedding_phd_twenty", EXAMPLE)
assert spec and spec.loader
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

expected = ["pca.pdf", "scree.pdf", "umap_clusters.pdf", "tsne.pdf", "phate.pdf"]
found = sorted(path.name for path in (ROOT / "figures").glob("*.pdf"))
print(f"expected figures={sorted(expected)}")
print(f"found figures={found}")
assert found == sorted(expected)
for name in expected:
    path = ROOT / "figures" / name
    content = path.read_bytes()
    valid_pdf = content.startswith(b"%PDF-") and b"%%EOF" in content[-1024:]
    print(f"{name}: bytes={path.stat().st_size}, valid_pdf={valid_pdf}")
    assert path.stat().st_size > 5_000
    assert valid_pdf

colors = module.categorical_colors(20)
print(f"twenty-category unique RGBA={len({tuple(color) for color in colors})}")
assert len({tuple(color) for color in colors}) == 20

adata = sc.read_h5ad(ROOT / "boundary_100x2000_20conditions.h5ad")
module.validate_input(adata)
sc.pp.highly_variable_genes(adata, n_top_genes=2_000, flavor="seurat_v3", subset=True)
sc.pp.normalize_total(adata, target_sum=1e4)
sc.pp.log1p(adata)
sc.pp.scale(adata, max_value=10)
sc.tl.pca(adata, n_comps=50, random_state=42)
scores = adata.obsm["X_pca"]
loadings = adata.varm["PCs"][:, :2]
strongest = np.argsort(np.linalg.norm(loadings, axis=1))[-5:]
arrow_scale = 0.12 * min(np.ptp(scores[:, 0]), np.ptp(scores[:, 1]))
loading_scale = arrow_scale / max(np.linalg.norm(loadings[strongest], axis=1))
endpoints = loadings[strongest] * loading_scale
labels = [str(adata.var_names[index]) for index in strongest]

def rendered_positions(save_path: Path | None = None) -> list[tuple[float, float]]:
    fig, ax = plt.subplots(figsize=(5, 4))
    ax.scatter(scores[:, 0], scores[:, 1], s=5, alpha=0.4)
    for dx, dy in endpoints:
        ax.arrow(0, 0, dx, dy, color="black", width=0.002 * arrow_scale)
    annotations = module.annotate_loading_labels(ax, endpoints, labels)
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    boxes = [annotation.get_window_extent(renderer) for annotation in annotations]
    assert all(not left.overlaps(right) for left, right in combinations(boxes, 2))
    positions = [annotation.get_position() for annotation in annotations]
    if save_path is not None:
        fig.savefig(save_path, dpi=180, bbox_inches="tight")
    plt.close(fig)
    return positions

proof = Path(r"F:\OpenScience\audits\bio-data-visualization-dimensionality-reduction-plots\figs\input11_loading_labels.png")
first_positions = rendered_positions(proof)
second_positions = rendered_positions()

print(f"loading positions first={first_positions}")
print(f"loading positions second={second_positions}")
print(f"deterministic={first_positions == second_positions}; non_overlapping=true")
assert first_positions == second_positions

stdout = (ROOT / "twenty_stdout.txt").read_text(encoding="utf-8")
print(f"caption contains N=100: {'N=100' in stdout}")
assert "N=100" in stdout
