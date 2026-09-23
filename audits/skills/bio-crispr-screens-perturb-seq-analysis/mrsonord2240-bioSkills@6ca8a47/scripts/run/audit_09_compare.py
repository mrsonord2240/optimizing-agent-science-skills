"""Compare the two separately-produced Mixscape signature arrays."""
from pathlib import Path
import numpy as np

root = Path(r"F:\OpenScience\audits\bio-crispr-screens-perturb-seq-analysis\data")
a = np.load(root / "determinism_a.npy")
b = np.load(root / "determinism_b.npy")
assert np.array_equal(a, b), float(np.max(np.abs(a - b)))
print(f"array_equal={np.array_equal(a, b)}")
print(f"max_abs_diff={float(np.max(np.abs(a - b))):.1f}")
print(f"shape={a.shape}")
