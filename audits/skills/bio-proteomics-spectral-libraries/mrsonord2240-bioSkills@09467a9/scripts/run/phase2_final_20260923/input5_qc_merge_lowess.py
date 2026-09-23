"""Fresh library QC/full-key merge plus nonlinear RT LOWESS comparison."""
import importlib.util
import json
from pathlib import Path
import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.nonparametric.smoothers_lowess import lowess

example = Path(r"F:\OpenScience\wt\proteomics-spectral-libraries\proteomics\spectral-libraries\examples\build_library.py")
spec = importlib.util.spec_from_file_location("build_library_example", example)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
lib_a = pd.DataFrame({"ModifiedSequence": ["AAA"] * 2, "PrecursorCharge": [2, 2], "ProteinId": ["P1", "P1"], "FragmentType": ["y", "y"], "FragmentSeriesNumber": [3, 4], "FragmentCharge": [1, 1], "LibraryIntensity": [0.7, 0.3]})
lib_b = pd.DataFrame({"ModifiedSequence": ["AAA", "AAA", "BBB"], "PrecursorCharge": [3, 3, 2], "ProteinId": ["P1", "P1", "P2"], "FragmentType": ["y", "y", "y"], "FragmentSeriesNumber": [3, 4, 2], "FragmentCharge": [1, 1, 1], "LibraryIntensity": [0.8, 0.2, 1.0]})
merged = module.merge_libraries([lib_a, lib_b])
stats_out = module.library_stats(merged)
assert stats_out["precursors"] == 3 and len(merged) == 5
irt = np.linspace(-25, 100, 21)
observed = 11 + 0.12 * irt + 0.0018 * irt ** 2
slope, intercept, _, _, _ = stats.linregress(irt, observed)
linear_ss = float(np.square(observed - (slope * irt + intercept)).sum())
smooth = lowess(observed, irt, frac=0.35, return_sorted=False)
lowess_ss = float(np.square(observed - smooth).sum())
assert lowess_ss < linear_ss / 10
print(json.dumps({"merged_stats": stats_out, "charge_states_retained": sorted(set(merged.loc[merged.ModifiedSequence == "AAA", "PrecursorCharge"])), "linear_residual_ss": round(linear_ss, 6), "lowess_residual_ss": round(lowess_ss, 6)}))
