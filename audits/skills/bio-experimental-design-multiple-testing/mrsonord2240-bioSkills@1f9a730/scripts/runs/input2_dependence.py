"""Input 2 (Variant A, regression of pre-fix Input 2, independent re-run with a different
seed and rep count) -- BH vs BY under independence / positive-block / negative-pair dependence,
plus the statsmodels default-method trap. Follows SKILL.md 'Dependence' section and
'Python Equivalent'.
"""
import numpy as np
from statsmodels.stats.multitest import multipletests

rng = np.random.default_rng(9182026)
m = 5000
n_alt = 500
n_reps = 300
alpha = 0.05

def make_pvalues(structure, rng):
    z_null = np.zeros(m - n_alt)
    if structure == "independent":
        z_null = rng.normal(0, 1, m - n_alt)
    elif structure == "positive_block":
        # 50 blocks of 100, rho=0.8 within block
        rho = 0.8
        blocks = (m - n_alt) // 100
        z_null = np.zeros(m - n_alt)
        for b in range(blocks):
            common = rng.normal(0, 1)
            idio = rng.normal(0, 1, 100)
            z_null[b*100:(b+1)*100] = np.sqrt(rho) * common + np.sqrt(1 - rho) * idio
    elif structure == "negative_pair":
        rho = -0.95
        pairs = (m - n_alt) // 2
        z_null = np.zeros(m - n_alt)
        for k in range(pairs):
            cov = np.array([[1, rho], [rho, 1]])
            draw = rng.multivariate_normal([0, 0], cov)
            z_null[2*k:2*k+2] = draw
    z_alt = rng.normal(3.2, 1, n_alt)
    z = np.concatenate([z_null, z_alt])
    from scipy import stats
    p = 2 * (1 - stats.norm.cdf(np.abs(z)))
    is_alt = np.concatenate([np.zeros(m - n_alt, dtype=bool), np.ones(n_alt, dtype=bool)])
    return p, is_alt

print(f"{'structure':<16}{'method':<8}{'meanFDP':>9}{'sdFDP':>8}{'P(FDP>0.10)':>13}{'power':>8}{'meanR':>8}")
for structure in ["independent", "positive_block", "negative_pair"]:
    for method in ["fdr_bh", "fdr_by"]:
        fdps, powers, Rs = [], [], []
        for rep in range(n_reps):
            p, is_alt = make_pvalues(structure, rng)
            rej, padj, _, _ = multipletests(p, alpha=alpha, method=method)
            R = rej.sum()
            FP = (rej & ~is_alt).sum()
            TP = (rej & is_alt).sum()
            fdps.append(FP / R if R > 0 else 0.0)
            powers.append(TP / n_alt)
            Rs.append(R)
        fdps = np.array(fdps)
        print(f"{structure:<16}{method:<8}{fdps.mean():>9.4f}{fdps.std():>8.4f}{(fdps>0.10).mean():>13.3f}{np.mean(powers):>8.4f}{np.mean(Rs):>8.1f}")

# statsmodels default trap
p, is_alt = make_pvalues("independent", rng)
rej_default, _, _, _ = multipletests(p, alpha=0.05)
rej_bh, _, _, _ = multipletests(p, alpha=0.05, method="fdr_bh")
import statsmodels
print(f"\nstatsmodels {statsmodels.__version__} default rejections: {rej_default.sum()} vs explicit fdr_bh: {rej_bh.sum()}")
