"""SYNTHETIC PSM tables for the bio-proteomics-peptide-identification audit (2026-09-11). Seeded.

Score model (XCorr-like, higher = better): every spectrum has 40 null candidates (half target, half decoy
peptides in the precursor window) whose scores are Gumbel(1.2, 0.25); a 'true' spectrum also has its correct
target peptide, score Normal(3.6, 0.9). Ground truth columns (is_correct, spectrum_is_true) are kept in the
files so the audit can measure the realised false discovery proportion (FDP); a user's file would not have them.

comet_concat.txt   : Comet-style .txt from ONE concatenated target+decoy search, 12,000 spectra (40% true),
                     num_output_lines = 5 (Comet's default) -> up to 5 ranked rows per scan ('num' = rank).
pulldown_nodecoy.tsv, pulldown_topdecoy.tsv : single-bait pulldown (Edge input). 38 spectra (26 true, 12 junk)
                     simulated; the 5 rows whose top hit was a decoy are dropped (as when a user exports an
                     engine-filtered list) -> 33 top-1 target PSMs, 11 of them false. topdecoy: the best-scoring
                     row relabelled as a decoy hit, to exercise the snippet when rank 1 is a decoy.
separate_target.tsv, separate_decoy.tsv : the SAME 12,000 spectra searched separately against the target DB
                     and against the decoy DB (best hit per spectrum in each), for the Stress input.
"""
import numpy as np
import pandas as pd

OUT = 'F:/OpenScience/audits/bio-proteomics-peptide-identification/data/'
rng = np.random.default_rng(1109)
AA = list('ACDEFGHIKLMNPQRSTVWY')


def rpep():
    return ''.join(rng.choice(AA, size=int(rng.integers(7, 20)))) + rng.choice(['K', 'R'])


def simulate(n_spec, frac_true, n_null=40):
    rows_t, rows_d, cands = [], [], []
    for scan in range(1, n_spec + 1):
        true = rng.random() < frac_true
        c = []
        for j in range(n_null):
            dec = j % 2 == 1
            c.append((rng.gumbel(1.2, 0.25), dec, False))
        if true:
            c.append((rng.normal(3.6, 0.9), False, True))
        cands.append((scan, true, c))
    return cands


def comet_rows(cands, top=5):
    rows = []
    for scan, true, c in cands:
        c = sorted(c, key=lambda x: -x[0])[:top]
        best = c[0][0]
        for rank, (s, dec, corr) in enumerate(c, 1):
            nxt = c[rank][0] if rank < len(c) else s * 0.9
            prot = ('DECOY_' if dec else '') + f'sp|P{int(rng.integers(10000, 99999))}|PROT_HUMAN'
            rows.append({'scan': scan, 'num': rank, 'charge': int(rng.choice([2, 3])),
                         'xcorr': round(s, 4), 'delta_cn': round(max(0.0, (best - nxt) / best), 4),
                         'e-value': float(f'{10 ** (-(s - 1.3) * 2.2 + rng.normal(0, 0.2)):.3e}'),
                         'plain_peptide': rpep(), 'protein': prot,
                         'is_correct': corr, 'spectrum_is_true': true})
    return pd.DataFrame(rows)


cands = simulate(12000, 0.40)
comet = comet_rows(cands)
comet.to_csv(OUT + 'comet_concat.txt', sep='\t', index=False)

# separate searches of the same spectra: best target hit and best decoy hit per spectrum
st, sd = [], []
for scan, true, c in cands:
    t = max([x for x in c if not x[1]], key=lambda x: x[0])
    d = max([x for x in c if x[1]], key=lambda x: x[0])
    st.append({'scan': scan, 'score': round(t[0], 4), 'protein': f'sp|P{scan:05d}|T_HUMAN', 'is_correct': t[2],
               'spectrum_is_true': true})
    sd.append({'scan': scan, 'score': round(d[0], 4), 'protein': f'DECOY_sp|P{scan:05d}|D_HUMAN',
               'is_correct': False, 'spectrum_is_true': true})
pd.DataFrame(st).to_csv(OUT + 'separate_target.tsv', sep='\t', index=False)
pd.DataFrame(sd).to_csv(OUT + 'separate_decoy.tsv', sep='\t', index=False)

# tiny pulldown, top-1 PSMs only: 26 bait/prey PSMs (true) + 12 junk spectra
pc = simulate(38, 0.0)
pull = []
for i, (scan, _, c) in enumerate(pc):
    if i < 26:
        c = c + [(rng.normal(3.2, 0.7), False, True)]
    s, dec, corr = max(c, key=lambda x: x[0])
    pull.append({'scan': scan, 'score': round(s, 4), 'peptide': rpep(),
                 'protein': ('DECOY_' if dec else '') + 'sp|Q9BAIT|BAIT_HUMAN', 'is_correct': corr})
pull = pd.DataFrame(pull)
# version A as simulated; version B: the single best-scoring row happens to be a decoy (it does happen)
nod = pull[~pull['protein'].str.startswith('DECOY_')].copy()
nod.to_csv(OUT + 'pulldown_nodecoy.tsv', sep='\t', index=False)
topd = nod.copy()
i = topd['score'].idxmax()
topd.loc[i, 'protein'] = 'DECOY_sp|Q9XXXX|RND_HUMAN'
topd.loc[i, 'is_correct'] = False
topd.to_csv(OUT + 'pulldown_topdecoy.tsv', sep='\t', index=False)
print('comet rows', len(comet), 'scans', comet['scan'].nunique(), '| rank-1 decoys', int(comet.query('num==1')['protein'].str.startswith('DECOY_').sum()))
print('pulldown rows', len(nod), 'decoys in original draw', int(pull['protein'].str.startswith('DECOY_').sum()))
