"""New input 10: exhaustively test categorical colors through 20 and >20 guards."""
from __future__ import annotations

import importlib.util
from pathlib import Path

import numpy as np

EXAMPLE = Path(r"F:\OpenScience\audits\bio-data-visualization-dimensionality-reduction-plots\run\example\embedding_phd.py")
spec = importlib.util.spec_from_file_location("embedding_phd_palette", EXAMPLE)
assert spec and spec.loader
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

for count in range(1, 21):
    first = module.categorical_colors(count)
    second = module.categorical_colors(count)
    unique = len({tuple(color) for color in first})
    print(f"count={count:02d} shape={first.shape} unique={unique} deterministic={np.array_equal(first, second)}")
    assert first.shape == (count, 4)
    assert unique == count
    assert np.array_equal(first, second)

for count in (0, 21, 25, 50):
    try:
        module.categorical_colors(count)
    except ValueError as error:
        message = str(error)
        print(f"guard count={count}: {message}")
        assert "facet" in message
        assert "alternative encoding" in message
    else:
        raise AssertionError(f"categorical_colors({count}) did not stop")

print("palette cardinality and fallback guard assertions passed")
