"""Fresh canonical Koina Prosit-intensity/iRT request plus synthetic iRT calibration.

Usage: shared audit Python. The observed RT values below are explicitly synthetic.
"""
import json
import numpy as np
import pandas as pd
from scipy import stats
from koinapy import Koina

inputs = pd.DataFrame({
    "peptide_sequences": ["LGGNEQVTR", "VEATFGVDESNAK", "YILAGVENSK"],
    "precursor_charges": [2, 2, 2],
    "collision_energies": [30, 30, 30],
})
fragments = Koina("Prosit_2019_intensity", "koina.wilhelmlab.org:443").predict(inputs)
irt = Koina("Prosit_2019_irt", "koina.wilhelmlab.org:443").predict(inputs[["peptide_sequences"]])
assert len(fragments) > len(inputs), "expected multiple fragment rows per precursor"
assert "annotation" in {str(c).lower() for c in fragments.columns}, fragments.columns.tolist()
irt_col = next(c for c in irt.columns if str(c).lower() in {"irt", "prediction"})
predicted = np.asarray(irt[irt_col], dtype=float)
observed = 7.5 + 0.21 * predicted  # synthetic observed RT for the audit only
slope, intercept, r, _, _ = stats.linregress(predicted, observed)
assert r * r > 0.95
print(json.dumps({"fragment_rows": len(fragments), "fragment_columns": fragments.columns.tolist(),
                  "irt_rows": len(irt), "irt_r2": round(float(r * r), 6),
                  "rt_slope": round(float(slope), 6), "rt_intercept": round(float(intercept), 6)}))
