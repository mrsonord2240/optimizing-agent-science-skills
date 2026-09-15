"""SYNTHETIC TMT PSM table for the bio-proteomics-differential-abundance audit (2026-09-11). NOT REAL DATA.

Two TMT10plex batches (plex A, plex B), channel layout as the shared tmt_design.csv: 126..130C carry
5 Control + 4 Treatment per plex, 131 = pooled reference. 800 proteins; 80 truly changed
(|log2FC| 0.6-1.6 before MS2 ratio compression x0.6). Each protein has a per-plex PSM count
(geometric, mean ~5; plex B samples ~30% fewer PSMs); PSM-level reporter noise SD 0.45 log2, so
protein precision genuinely scales with PSM count - the situation DEqMS is built for.
Outputs: tmt_psms.csv (protein, plex, psm_id, channel columns), tmt_psm_design.csv, tmt_psm_truth.csv.
"""
import os
import numpy as np
import pandas as pd

OUT = os.path.dirname(os.path.abspath(__file__))
rng = np.random.default_rng(911)
chans = ['126', '127N', '127C', '128N', '128C', '129N', '129C', '130N', '130C', '131']
roles = ['C', 'C', 'C', 'C', 'T', 'T', 'T', 'T', 'C', 'REF']
NP = 800
prot = [f'TP{i:04d}' for i in range(NP)]
effect = np.zeros(NP)
idx = rng.permutation(NP)[:80]
effect[idx[:40]] = rng.uniform(0.6, 1.6, 40)
effect[idx[40:]] = -rng.uniform(0.6, 1.6, 40)
base = rng.normal(16, 1.5, NP)
design, rows = [], []
for plex, scale in (('A', 1.0), ('B', 0.7)):
    samples = []
    ci = ti = 0
    for c, r in zip(chans, roles):
        if r == 'C':
            ci += 1; s = f'{plex}_C{ci}'
        elif r == 'T':
            ti += 1; s = f'{plex}_T{ti}'
        else:
            s = f'{plex}_REF'
        samples.append(s)
        design.append({'plex': plex, 'channel': c, 'sample': s,
                       'condition': {'C': 'Control', 'T': 'Treatment', 'REF': 'Reference'}[r]})
    bio = {s: rng.normal(0, 0.15, NP) for s in samples if not s.endswith('REF')}  # biological replicate spread
    load = {s: rng.normal(0, 0.2) for s in samples}
    plex_off = 0.8 if plex == 'B' else 0.0
    for i in range(NP):
        k = int(rng.geometric(1 / (5.0 * scale)))
        for p in range(k):
            pep = rng.normal(0, 1.0)
            vals = {}
            true_ch = []
            for c, r, s in zip(chans, roles, samples):
                if r == 'REF':
                    continue
                x = base[i] + pep + plex_off + (0.6 * effect[i] if r == 'T' else 0.0) + bio[s][i] + load[s]
                true_ch.append(x)
                vals[c] = x + rng.normal(0, 0.45)
            vals['131'] = np.mean(true_ch) + load[samples[-1]] + rng.normal(0, 0.45)
            rows.append({'protein': prot[i], 'plex': plex, 'psm_id': f'{plex}{i}_{p}',
                         **{f'Abundance {c}': round(2 ** v, 1) for c, v in vals.items()}})
pd.DataFrame(rows).to_csv(os.path.join(OUT, 'tmt_psms.csv'), index=False)
pd.DataFrame(design).to_csv(os.path.join(OUT, 'tmt_psm_design.csv'), index=False)
pd.DataFrame({'protein': prot, 'true_log2fc': effect, 'compressed_log2fc': 0.6 * effect,
              'class': np.where(effect > 0, 'up', np.where(effect < 0, 'down', 'null'))}
             ).to_csv(os.path.join(OUT, 'tmt_psm_truth.csv'), index=False)
print('PSM rows', len(rows))
