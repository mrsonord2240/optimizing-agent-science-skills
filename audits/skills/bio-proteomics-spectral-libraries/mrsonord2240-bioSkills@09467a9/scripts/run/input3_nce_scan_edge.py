"""Input 3 (Edge/boundary): NCE scanning as the Skill instructs ("Do not blindly
use NCE=30 ... scan candidate NCE values ... pick the one maximizing spectral
contrast/correlation against a few real spectra"), plus an edge case: what
happens when Koina is asked to predict a peptide sequence containing a
non-standard / ambiguous residue (here, one with a lowercase artifact and one
absurdly long peptide) that the model may reject.
"""
import numpy as np
import pandas as pd
from koinapy import Koina

pep = 'LGGNEQVTR'
charge = 2
candidate_nces = [20, 25, 28, 30, 32, 35, 40]

# A tiny "real" spectrum (b/y ions, arbitrary but fixed relative intensities)
real_mz = np.array([175.119, 276.167, 171.113, 375.235, 228.134])
real_intensity = np.array([1.00, 0.62, 0.18, 0.35, 0.09])

best_nce, best_corr = None, -2
for nce in candidate_nces:
    inputs = pd.DataFrame({'peptide_sequences': [pep], 'precursor_charges': [charge], 'collision_energies': [nce]})
    out = Koina('Prosit_2019_intensity', 'koina.wilhelmlab.org:443').predict(inputs, disable_progress_bar=True)
    # align predicted fragments to the real spectrum by nearest m/z
    pred_mz = out['mz'].to_numpy()
    pred_int = out['intensities'].to_numpy() if 'intensities' in out.columns else out.iloc[:, -2].to_numpy()
    aligned = []
    for mz in real_mz:
        idx = np.argmin(np.abs(pred_mz - mz))
        aligned.append(pred_int[idx] if abs(pred_mz[idx] - mz) < 0.02 else 0.0)
    aligned = np.array(aligned)
    if aligned.std() > 0:
        corr = np.corrcoef(aligned, real_intensity)[0, 1]
    else:
        corr = -1
    print(f'NCE={nce:>3}  corr={corr:.3f}')
    if corr > best_corr:
        best_corr, best_nce = corr, nce

print(f'Best NCE = {best_nce} (corr={best_corr:.3f})')

# Edge case: malformed / boundary peptide inputs
edge_inputs = pd.DataFrame({
    'peptide_sequences': ['LGGNEQVTRX', 'K' * 60],  # invalid residue X; absurdly long peptide
    'precursor_charges': [2, 2],
    'collision_energies': [30, 30],
})
try:
    edge_out = Koina('Prosit_2019_intensity', 'koina.wilhelmlab.org:443').predict(edge_inputs, disable_progress_bar=True)
    print('Edge-case predict returned rows:', len(edge_out))
    print(edge_out.head(10))
except Exception as e:
    print('EDGE_CASE_ERROR:', type(e).__name__, str(e)[:300])
