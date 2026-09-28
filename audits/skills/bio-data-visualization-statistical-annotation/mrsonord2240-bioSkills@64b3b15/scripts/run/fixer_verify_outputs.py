"""Fixer evidence: assert corrected p-values and non-blank rendered figures."""

from pathlib import Path

import numpy as np
import pandas as pd
from PIL import Image

out = Path(r"F:\OpenScience\audits\bio-data-visualization-statistical-annotation\run\fixer-output")


def check_csv(name: str, column: str, expected: list[float], tolerance: float = 1e-8) -> None:
    observed = pd.read_csv(out / name)[column].to_numpy(float)
    np.testing.assert_allclose(observed, expected, atol=tolerance, rtol=0)
    print("VALUES PASS", name, " ".join(f"{x:.8g}" for x in observed))


check_csv("r-border.results.csv", "p.adj", [0.0843168138901077, 0.000959824489236254, 0.0843168138901077])
check_csv("py-border.results.csv", "p_adj", [0.08769108332035273, 0.0009598244892362539, 0.08769108332035273])
check_csv("r-paired.results.csv", "p.adj", [0.0023193359375])
check_csv("py-paired.results.csv", "p_adj", [0.0023193359375])
check_csv("r-nested-cli.results.csv", "p.adj", [0.396429046491586], tolerance=1e-6)
check_csv("r-four-dunn-cli.results.csv", "p.adj",
          [0.881353765159766, 0.00217020126343008, 0.375123723918108,
           0.00245186759391559, 0.375123723918108, 0.375123723918108])
check_csv("r-four-tukey-cli.results.csv", "p.adj",
          [0.988909705240931, 0.000386847836196247, 0.245731512581709,
           0.000342782556574495, 0.174354300414173, 0.239890512641457])

images = [
    out / "r-border.png",
    out / "py-border.png",
    out / "r-paired.png",
    out / "py-paired.png",
    out / "r-nested-cli.png",
    out / "example" / "pairwise-adjusted.png",
    out / "example" / "ggsignif-adjusted.png",
]
for path in images:
    image = np.asarray(Image.open(path).convert("RGB"))
    nonwhite = np.mean(np.any(image < 250, axis=2))
    assert image.shape[0] >= 500 and image.shape[1] >= 500 and nonwhite > 0.01
    print("IMAGE PASS", path.name, f"{image.shape[1]}x{image.shape[0]}", f"nonwhite={nonwhite:.3f}")
