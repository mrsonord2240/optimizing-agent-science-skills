# Input 5 - separate target and decoy searches of the same 12,000 spectra, merged. What the Skill prescribes
# (Elias-Gygi 2x-decoy "for separate searches") vs the literature estimators, scored against ground truth.
import numpy as np
import pandas as pd

D = 'F:/OpenScience/audits/bio-proteomics-peptide-identification/data/'
T = pd.read_csv(D + 'separate_target.tsv', sep='\t')
Dc = pd.read_csv(D + 'separate_decoy.tsv', sep='\t')
merged = pd.concat([T, Dc], ignore_index=True)
merged['is_decoy'] = merged['protein'].str.startswith('DECOY_')
print(f'merged rows {len(merged)} (targets {len(T)}, decoys {len(Dc)}); true target PSMs {int(T["is_correct"].sum())}')

ts = np.sort(T['score'].to_numpy())[::-1]
ds = np.sort(Dc['score'].to_numpy())
corr = T.sort_values('score', ascending=False)['is_correct'].to_numpy()


def counts_at(thr):
    t = np.arange(1, len(ts) + 1)                      # targets >= each target score (ranked)
    d = len(ds) - np.searchsorted(ds, thr, side='left')  # decoys >= threshold
    return t, d


t, d = counts_at(ts)


def qv(fdr):
    return np.minimum.accumulate(fdr[::-1])[::-1]


def report(tag, q):
    k = q <= 0.01
    n = int(k.sum())
    fdp = 1 - corr[k].mean() if n else float('nan')
    print(f'{tag:<58} kept={n:>5}  true FDP={fdp:.4f}')


# (1) what the Skill prescribes for separate searches: Elias-Gygi 2*d/(t+d)
report('(1) Skill: "Elias-Gygi 2x-decoy" 2d/(t+d), separate', qv(2 * d / (t + d)))
# (2) Kall et al. 2008 separate-search estimator, pi0 = 1 (d/t)
report('(2) Kall 2008 separate, pi0=1: d/t', qv(d / t))
# (3) Kall et al. 2008 with pi0 estimated (fraction of target scores below the decoy median, x2)
pi0 = min(1.0, (T['score'] < np.median(ds)).sum() / (0.5 * len(ds)))
report(f'(3) Kall 2008 separate, pi0-hat={pi0:.3f}: pi0*d/t', qv(pi0 * d / t))
# (4) turn it into target-decoy competition: per scan keep the higher of target/decoy, then d/t (Percolator -Y)
m = merged.sort_values('score', ascending=False).drop_duplicates('scan')
m = m.reset_index(drop=True)
tc = (~m['is_decoy']).cumsum(); dcnt = m['is_decoy'].cumsum()
q4 = qv((dcnt / tc.clip(lower=1)).to_numpy())
k4 = (q4 <= 0.01) & ~m['is_decoy'].to_numpy()
print(f'{"(4) per-scan competition (TDC) then d/t":<58} kept={int(k4.sum()):>5}  true FDP={1 - m.loc[k4, "is_correct"].mean():.4f}')
# (5) the Skill's CONCATENATED snippet run naively on the merged file (no competition)
s = merged.sort_values('score', ascending=False).reset_index(drop=True)
q5 = qv((s['is_decoy'].cumsum() / (~s['is_decoy']).cumsum()).to_numpy())
k5 = (q5 <= 0.01) & ~s['is_decoy'].to_numpy()
print(f'{"(5) Skill concatenated snippet on the merged file":<58} kept={int(k5.sum()):>5}  true FDP={1 - s.loc[k5, "is_correct"].mean():.4f}')
# oracle
fdp_run = np.cumsum(~corr) / np.arange(1, len(corr) + 1)
print(f'{"oracle: largest list with true FDP <= 1%":<58} kept={int(np.max(np.where(fdp_run <= 0.01)[0]) + 1):>5}')
# estimate vs truth at a fixed list size
for n in [2000, 2600, 3000]:
    thr = ts[n - 1]; dd = int((ds >= thr).sum())
    print(f'   top {n} targets: true FDP {1 - corr[:n].mean():.4f} | 2d/(t+d) {2 * dd / (n + dd):.4f} | d/t {dd / n:.4f} | pi0*d/t {pi0 * dd / n:.4f}')
