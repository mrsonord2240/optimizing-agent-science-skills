"""
Input 2 (Variant A) -- "my test statistics are strongly correlated across genes;
is BH still valid or do I need BY?"

Code written by following SKILL.md sections "Dependence -- When BH Is Not Enough (BY)"
and "Python Equivalent (mind the default)".

SYNTHETIC simulation with planted ground truth, 400 replicate datasets per
dependence structure, so the realized FDP distribution (not just one draw) can be
compared against the nominal 0.05.

Dependence structures
  independent   : z_i iid
  positive block: blocks of 50, equicorrelation rho = +0.8   (PRDS regime)
  negative pair : blocks of 2,  correlation      rho = -0.95 (outside PRDS)
"""
import numpy as np
from scipy import stats
from statsmodels.stats.multitest import multipletests

RNG = np.random.default_rng(31415)
M, N_ALT, REPS, ALPHA = 5000, 500, 400, 0.05
MU_ALT = 3.2                      # alternative mean shift on the z scale

truth = np.zeros(M, dtype=bool)
truth[:N_ALT] = True
mu = np.where(truth, MU_ALT, 0.0)


def draw(structure):
    if structure == "independent":
        return RNG.normal(0.0, 1.0, M) + mu
    if structure == "positive_block":
        rho, bs = 0.8, 50
        nb = M // bs
        shared = RNG.normal(0.0, 1.0, nb).repeat(bs)
        return np.sqrt(rho) * shared + np.sqrt(1 - rho) * RNG.normal(0, 1, M) + mu
    if structure == "negative_pair":
        rho = -0.95
        e1 = RNG.normal(0, 1, M // 2)
        e2 = rho * e1 + np.sqrt(1 - rho ** 2) * RNG.normal(0, 1, M // 2)
        z = np.empty(M)
        z[0::2], z[1::2] = e1, e2
        return z + mu
    raise ValueError(structure)


def fdp_power(rej):
    R = rej.sum()
    V = (rej & ~truth).sum()
    return (V / R if R else 0.0), (rej & truth).sum() / N_ALT, R


print(f"SYNTHETIC: m={M}, true alternatives={N_ALT} (pi0={1-N_ALT/M:.3f}), "
      f"reps={REPS}, alpha={ALPHA}")
print(f"{'structure':16s} {'method':6s} {'meanFDP':>8s} {'sdFDP':>7s} "
      f"{'P(FDP>0.10)':>12s} {'power':>7s} {'mean R':>8s}")
for structure in ["independent", "positive_block", "negative_pair"]:
    acc = {m: {"fdp": [], "pow": [], "R": []} for m in ("fdr_bh", "fdr_by")}
    for _ in range(REPS):
        z = draw(structure)
        p = 2 * stats.norm.sf(np.abs(z))
        for m in ("fdr_bh", "fdr_by"):
            rej, _, _, _ = multipletests(p, alpha=ALPHA, method=m)
            f, pw, R = fdp_power(rej)
            acc[m]["fdp"].append(f); acc[m]["pow"].append(pw); acc[m]["R"].append(R)
    for m in ("fdr_bh", "fdr_by"):
        f = np.array(acc[m]["fdp"])
        print(f"{structure:16s} {m:6s} {f.mean():8.4f} {f.std():7.4f} "
              f"{(f > 0.10).mean():12.3f} {np.mean(acc[m]['pow']):7.4f} "
              f"{np.mean(acc[m]['R']):8.1f}")

# --- the trap the skill flags: statsmodels' default method is NOT BH --------
z = draw("independent")
p = 2 * stats.norm.sf(np.abs(z))
rej_default, _, _, _ = multipletests(p, alpha=ALPHA)
rej_bh, _, _, _ = multipletests(p, alpha=ALPHA, method="fdr_bh")
print(f"\nstatsmodels default (method='hs') rejections: {rej_default.sum()}  "
      f"vs explicit method='fdr_bh': {rej_bh.sum()}  "
      f"-> SKILL.md's 'far fewer significant calls' warning reproduced")
