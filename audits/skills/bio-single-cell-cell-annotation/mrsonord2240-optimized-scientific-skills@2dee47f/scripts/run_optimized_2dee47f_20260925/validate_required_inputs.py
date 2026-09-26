"""Execute the shipped CLI against inputs missing each required structural field."""
import runpy
import sys
from pathlib import Path

import scanpy as sc

ROOT = Path(r"F:\OpenScience\audits\bio-single-cell-cell-annotation\reaudit-optimized-scientific-skills@2dee47f-20260925")
SOURCE = Path(r"F:\OpenScience\audit-sources\optimized-scientific-skills-2dee47f\skills\bio-single-cell-cell-annotation\examples\celltypist_annotation.py")
MODEL = Path(r"F:\OpenScience\audit-envs\single-cell-transcriptomics-analyst\cache\celltypist\data\models\Immune_All_Low.pkl")
base = sc.read_h5ad(ROOT / "data" / "input1_clustered.h5ad")[:20].copy()

cases = {
    "counts": (lambda q: q.layers.pop("counts"), "raw counts"),
    "leiden": (lambda q: q.obs.pop("leiden"), "seeded over-clustering"),
    "umap": (lambda q: q.obsm.pop("X_umap"), "X_umap"),
}
for name, (mutate, expected) in cases.items():
    q = base.copy(); mutate(q)
    path = ROOT / "data" / f"validation_missing_{name}.h5ad"; q.write_h5ad(path)
    sys.argv = [
        str(SOURCE), "--input", str(path), "--model", str(MODEL),
        "--output", str(ROOT / "data" / f"validation_{name}_unexpected.h5ad"),
        "--figure", str(ROOT / "data" / f"validation_{name}_unexpected.png"),
        "--counts-output", str(ROOT / "data" / f"validation_{name}_unexpected.csv"),
    ]
    try:
        runpy.run_path(str(SOURCE), run_name="__main__")
    except ValueError as exc:
        assert expected in str(exc)
        print(f"missing_{name}=PASS error={exc}")
    else:
        raise AssertionError(f"missing {name} was not rejected")
