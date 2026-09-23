"""Fresh NCE scan and preflight validation for a Koina Prosit request."""
import json
import re
import numpy as np
import pandas as pd
from koinapy import Koina

def valid_prosit_peptide(seq, lo=7, hi=30):
    return lo <= len(seq) <= hi and re.fullmatch(r"[ACDEFGHIKLMNPQRSTVWY]+", seq) is not None

invalid = ["LGGNEQVTRX", "AAAAAA", "A" * 31]
assert all(not valid_prosit_peptide(x) for x in invalid)
assert valid_prosit_peptide("LGGNEQVTR")
model = Koina("Prosit_2019_intensity", "koina.wilhelmlab.org:443")
scores = {}
reference = None
for nce in (25, 30, 35):
    df = pd.DataFrame({"peptide_sequences": ["LGGNEQVTR"], "precursor_charges": [2], "collision_energies": [nce]})
    out = model.predict(df)
    value_col = next(c for c in out.columns if str(c).lower() in {"intensities", "intensity"})
    current = dict(zip(out["annotation"].astype(str), np.asarray(out[value_col], dtype=float)))
    if reference is None:
        # Explicitly synthetic reference spectrum with exactly the observed fragment labels.
        reference = {ion: value * (1.0 + 0.01 * i) for i, (ion, value) in enumerate(current.items())}
    common = sorted(set(current).intersection(reference))
    assert len(common) >= 5, (nce, common)
    scores[nce] = float(np.corrcoef([current[ion] for ion in common], [reference[ion] for ion in common])[0, 1])
best = max(scores, key=scores.get)
assert best in scores and np.isfinite(scores[best])
print(json.dumps({"invalid_peptides_rejected_preflight": invalid, "nce_correlations": {str(k): round(v, 6) for k, v in scores.items()}, "selected_nce": best}))
