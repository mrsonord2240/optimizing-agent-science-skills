"""Builds a 5-sample MAGeCK-format count table (Plasmid, Day0_r1, Day0_r2, Endpoint_r1,
Endpoint_r2) to test the FIXED examples/screen_qc.py's stage-aware bands end to end.
Plasmid/Endpoint_r1/Endpoint_r2 are real HAP1 TKOv3 columns (T0, T18A, T18B). Day0_r1/r2 are
synthetic lognormal count vectors, seeded, calibrated to a Gini around 0.15 -- deliberately
between the plasmid pass/fail band (0.10/0.20, so it would FAIL as a plasmid) and the day_0
band (0.12/0.25, so it WARNs as day_0) -- to test whether the same magnitude of inequality is
scored differently depending on the declared stage. Clearly synthetic; stated as such in the
audit report."""
import pandas as pd, numpy as np

REAL = r'F:\OpenScience\audits\bio-crispr-screens-screen-qc\data\hap1_tkov3_canonical.txt'
OUT = r'F:\OpenScience\audits\bio-crispr-screens-screen-qc\data\stage5_mixed.count.txt'

df = pd.read_csv(REAL, sep='\t')
n = len(df)

rng1 = np.random.default_rng(101)
rng2 = np.random.default_rng(102)


def lognormal_counts(rng, n, sigma, mean_total=800):
    x = rng.lognormal(mean=0, sigma=sigma, size=n)
    x = x / x.mean() * mean_total
    return np.round(x).astype(float)


def gini(x):
    x = np.sort(x[x > 0].astype(float))
    if x.size == 0:
        return np.nan
    nn = x.size
    cumx = np.cumsum(x)
    return (nn + 1 - 2 * np.sum(cumx) / cumx[-1]) / nn


# calibrate sigma to hit Gini ~0.15
best_sigma = None
for sigma in np.arange(0.30, 0.60, 0.02):
    trial = lognormal_counts(np.random.default_rng(1), 20000, sigma)
    g = gini(trial)
    if abs(g - 0.15) < 0.01:
        best_sigma = sigma
        break
if best_sigma is None:
    best_sigma = 0.42  # fallback, checked separately below

day0_r1 = lognormal_counts(rng1, n, best_sigma)
day0_r2 = lognormal_counts(rng2, n, best_sigma)

out = pd.DataFrame({
    'sgRNA': df['SEQUENCE'],
    'Gene': df['GENE'],
    'Plasmid': df['HAP1_T0'],
    'Day0_r1': day0_r1,
    'Day0_r2': day0_r2,
    'Endpoint_r1': df['HAP1_T18A'],
    'Endpoint_r2': df['HAP1_T18B'],
})
out.to_csv(OUT, sep='\t', index=False)

print('sigma used:', best_sigma)
print('Gini(Plasmid)     =', round(gini(out['Plasmid'].values), 4))
print('Gini(Day0_r1)     =', round(gini(out['Day0_r1'].values), 4))
print('Gini(Day0_r2)     =', round(gini(out['Day0_r2'].values), 4))
print('Gini(Endpoint_r1) =', round(gini(out['Endpoint_r1'].values), 4))
print('Gini(Endpoint_r2) =', round(gini(out['Endpoint_r2'].values), 4))
print('wrote', OUT, 'rows=', len(out))
