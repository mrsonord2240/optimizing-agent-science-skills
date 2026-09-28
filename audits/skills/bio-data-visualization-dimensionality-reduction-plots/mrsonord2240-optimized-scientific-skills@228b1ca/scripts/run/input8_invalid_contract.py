"""New input 8: verify the fixed CLI rejects two invalid AnnData contracts clearly."""
from __future__ import annotations

import importlib.util
from pathlib import Path

import anndata as ad
import numpy as np
import pandas as pd

ROOT = Path(r"F:\OpenScience\audits\bio-data-visualization-dimensionality-reduction-plots\run\example")
spec = importlib.util.spec_from_file_location("embedding_phd", ROOT / "embedding_phd.py")
assert spec and spec.loader
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

rng = np.random.default_rng(20260927)
fractional = ad.AnnData(
    rng.random((120, 2_000)),
    obs=pd.DataFrame({"condition": ["control"] * 120}, index=[f"f{i}" for i in range(120)]),
)
missing_condition = ad.AnnData(
    rng.poisson(1.0, (120, 2_000)),
    obs=pd.DataFrame(index=[f"m{i}" for i in range(120)]),
)

cases = [("fractional/log-like values", fractional, "raw"), ("missing condition", missing_condition, "condition")]
for label, value, expected in cases:
    try:
        module.validate_input(value)
    except ValueError as exc:
        print(f"{label}: ValueError: {exc}")
        assert expected in str(exc)
    else:
        raise AssertionError(f"{label} was incorrectly accepted")
