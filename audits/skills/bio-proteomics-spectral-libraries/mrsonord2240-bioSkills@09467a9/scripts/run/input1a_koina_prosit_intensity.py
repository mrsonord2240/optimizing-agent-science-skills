"""Input 1 (Canonical), part A: live Koina Prosit fragment-intensity prediction.
Run with: F:\\OpenScience\\audit-envs\\mass-spec-proteomics-analyst\\Scripts\\python.exe
"""
import pandas as pd
from koinapy import Koina

inputs = pd.DataFrame({'peptide_sequences': ['LGGNEQVTR'], 'precursor_charges': [2], 'collision_energies': [30]})
k = Koina('Prosit_2019_intensity', 'koina.wilhelmlab.org:443')
out = k.predict(inputs)
print(type(out))
print(out.head())
