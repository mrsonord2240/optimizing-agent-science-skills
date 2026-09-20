"""Input 1 (Canonical), part B: live Koina iRT prediction + calibration against
simulated observed RT, following the Skill's calibrate_irt() pattern from
examples/build_library.py (R^2 > 0.95 gate).
Run with: F:\\OpenScience\\audit-envs\\mass-spec-proteomics-analyst\\Scripts\\python.exe
"""
import pandas as pd
import numpy as np
from koinapy import Koina
from scipy import stats

peps = ['LGGNEQVTR', 'GAGSSEPVTGLDAK', 'VEATFGVDESNAK', 'YILAGVENSK', 'TPVISGGPYEYR']
inputs = pd.DataFrame({'peptide_sequences': peps, 'precursor_charges': [2] * len(peps)})
k = Koina('Prosit_2019_irt', 'koina.wilhelmlab.org:443')
out = k.predict(inputs)
print(out[['peptide_sequences', 'irt']])

irt = out.set_index('peptide_sequences')['irt']
rng = np.random.default_rng(2)
observed = 5.0 + 0.2 * irt.values + rng.normal(0, 0.15, len(irt))
slope, intercept, r, _, _ = stats.linregress(irt.values, observed)
print(f'Calibration fit: RT = {slope:.3f}*iRT + {intercept:.3f}, R2={r**2:.3f}')
