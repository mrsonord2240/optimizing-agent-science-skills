"""New use case: run the shipped CLI offline with an explicit model and custom destinations."""
import os
import runpy
import sys
from pathlib import Path
from unittest.mock import patch

ROOT = Path(r"F:\OpenScience\audits\bio-single-cell-cell-annotation\reaudit-optimized-scientific-skills@2dee47f-20260925")
SOURCE = Path(r"F:\OpenScience\audit-sources\optimized-scientific-skills-2dee47f\skills\bio-single-cell-cell-annotation\examples\celltypist_annotation.py")
MODEL = Path(r"F:\OpenScience\audit-envs\single-cell-transcriptomics-analyst\cache\celltypist\data\models\Immune_All_Low.pkl")
CACHE = ROOT / "data" / "input6_empty_cache"
CACHE.mkdir(exist_ok=True)
os.environ["CELLTYPIST_FOLDER"] = str(CACHE)

# The cache override must precede importing CellTypist, which computes models_path at import time.
import celltypist
import scanpy as sc

assert Path(celltypist.models.models_path).resolve().is_relative_to(CACHE.resolve())

source = sc.read_h5ad(ROOT / "data" / "input1_clustered.h5ad")[:240].copy()
source.write_h5ad(ROOT / "data" / "input6_query.h5ad")
network_calls: list[str] = []


def blocked(*args, **kwargs):
    network_calls.append(str(args[0]) if args else "unknown")
    raise AssertionError("network acquisition attempted")


def invoke(model: str, stem: str) -> None:
    sys.argv = [
        str(SOURCE), "--input", str(ROOT / "data" / "input6_query.h5ad"),
        "--model", model,
        "--output", str(ROOT / "data" / f"{stem}.h5ad"),
        "--figure", str(ROOT / "data" / f"{stem}.png"),
        "--counts-output", str(ROOT / "data" / f"{stem}.csv"),
    ]
    runpy.run_path(str(SOURCE), run_name="__main__")


with patch("requests.sessions.Session.request", blocked), \
     patch("urllib.request.urlopen", blocked), \
     patch.object(celltypist.models, "download_models", blocked), \
     patch.object(celltypist.models, "get_all_models", blocked):
    invoke(str(MODEL), "input6_custom")
    try:
        invoke("definitely_missing_model.pkl", "input6_missing")
    except FileNotFoundError as exc:
        print(f"missing_model_error={exc}")
    else:
        raise AssertionError("missing uncached model did not fail")

for suffix in ("h5ad", "png", "csv"):
    path = ROOT / "data" / f"input6_custom.{suffix}"
    assert path.is_file() and path.stat().st_size > 0
assert not network_calls
assert not any(CACHE.rglob("*.pkl"))
print(f"explicit_model={MODEL}")
print(f"isolated_models_path={celltypist.models.models_path}")
print("network_acquisition_calls=0")
print("custom_output_destinations=PASS")
