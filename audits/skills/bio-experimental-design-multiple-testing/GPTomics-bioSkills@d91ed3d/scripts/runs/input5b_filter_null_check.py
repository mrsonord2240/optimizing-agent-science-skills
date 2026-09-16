"""Direct check of the null-independence property the SKILL.md filtering rule rests on.
For each candidate filter statistic, is the NULL p-value distribution still Uniform(0,1)
among the features the filter retains?  SYNTHETIC, 200 replicates."""
import numpy as np
from scipy import stats
RNG = np.random.default_rng(24680)
M, N_ALT, NPG, REPS = 6000, 500, 6, 200
df = 2*NPG-2
res = {k: [] for k in ("all nulls","top50% overall variance","top50% overall mean",
                       "top50% within-group variance","preliminary t-test p<0.5")}
ks = {k: [] for k in res}
for _ in range(REPS):
    tr = np.zeros(M, bool); tr[:N_ALT] = True
    eff = np.where(tr, RNG.uniform(0.9,2.4,M)*RNG.choice([-1.,1.],M), 0.0)
    mu = np.clip(RNG.normal(6,2,M),1,14)
    a = RNG.normal(mu[:,None],1.0,(M,NPG)); b = RNG.normal((mu+eff)[:,None],1.0,(M,NPG))
    sp2 = (a.var(1,ddof=1)+b.var(1,ddof=1))/2
    t = (b.mean(1)-a.mean(1))/np.sqrt(sp2*2/NPG)
    pv = 2*stats.t.sf(np.abs(t), df)
    allx = np.hstack([a,b]); ov, om = allx.var(1,ddof=1), allx.mean(1)
    masks = {"all nulls": np.ones(M,bool),
             "top50% overall variance": ov>=np.median(ov),
             "top50% overall mean": om>=np.median(om),
             "top50% within-group variance": sp2>=np.median(sp2),
             "preliminary t-test p<0.5": pv<0.5}
    for k,mk in masks.items():
        sel = mk & ~tr
        pn = pv[sel]
        res[k].append((pn<0.05).mean())
        # rescale the pre-test filter's truncated support before the KS test
        ref = pn/0.5 if k.startswith("preliminary") else pn
        ks[k].append(stats.kstest(ref,'uniform').statistic)
print(f"{'filter':32s} {'P(null p<0.05 | kept)':>22s} {'(target 0.05)':>14s} {'mean KS D':>10s}")
for k in res:
    print(f"{k:32s} {np.mean(res[k]):22.4f} {'':14s} {np.mean(ks[k]):10.4f}")
