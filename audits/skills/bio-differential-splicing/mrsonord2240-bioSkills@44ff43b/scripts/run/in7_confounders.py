#!/usr/bin/env python3
"""Input 7 (adversarial/ambiguous): 'my samples were prepared in two batches, batch is partly confounded with condition; adjust for it'.
Runs the SKILL.md 'Confounder Handling' statsmodels snippet (verbatim block marked below) on the SYNTHETIC sim (A vs B, 3v3) with an
arbitrary batch (A1,A2,B1 = batch1; A3,B2,B3 = batch2 -> imbalanced) and a random RIN, per event, then tests residuals by group with
Wilcoxon (rank-sum) exactly as the Skill instructs. Compares against OLS logit_psi ~ group + batch (group term tested).
Truth: 24 strong + 6 weak DS genes (data/sim/truth.tsv); no batch effect was simulated, so any loss of power is due to the method."""
import sys
import numpy as np
import pandas as pd
from scipy.stats import mannwhitneyu
import statsmodels.formula.api as smf

sim = sys.argv[1]
truth = pd.read_csv(f'{sim}/truth.tsv', sep='\t').set_index('gene')
cnt = pd.read_csv(f'{sim}/counts.tsv', sep='\t')
cnt = cnt[cnt['sample'].str[0].isin(['A', 'B'])].copy()
cnt = cnt[cnt['M'] >= 20]                       # events with usable coverage in a replicate (drop the low-coverage genes' noise)
ok_genes = cnt.groupby('gene').size()
ok_genes = ok_genes[ok_genes == 6].index
cnt['psi'] = cnt['n_inc'] / cnt['M']
batch = {'A1': 'b1', 'A2': 'b1', 'B1': 'b1', 'A3': 'b2', 'B2': 'b2', 'B3': 'b2'}
rng = np.random.default_rng(7)
rin = {s: float(rng.normal(8, 0.5)) for s in batch}
rows = []
for g in ok_genes:
    psi = cnt[cnt['gene'] == g].copy()
    psi['batch'] = psi['sample'].map(batch)
    psi['RIN'] = psi['sample'].map(rin)
    psi['group'] = np.where(psi['sample'].str[0] == 'A', 0, 1)
    # ---- verbatim from SKILL.md 'Confounder Handling' ----
    eps = 1e-3
    psi['logit_psi'] = np.log((psi['psi'].clip(eps, 1 - eps)) / (1 - psi['psi'].clip(eps, 1 - eps)))
    psi['psi_resid'] = smf.ols('logit_psi ~ batch + RIN', data=psi).fit().resid
    # then test psi_resid by group via Wilcoxon
    # ---- end verbatim ----
    a = psi.loc[psi.group == 0, 'psi_resid']; b = psi.loc[psi.group == 1, 'psi_resid']
    p_wil = mannwhitneyu(a, b, alternative='two-sided').pvalue
    fit = smf.ols('logit_psi ~ group + batch + RIN', data=psi).fit()
    rows.append((g, p_wil, float(fit.pvalues['group']), truth.loc[g, 'class']))
res = pd.DataFrame(rows, columns=['gene', 'p_wilcoxon_resid', 'p_ols_group', 'class'])
print('events with NaN OLS p (dropped from the OLS tally):', int(res['p_ols_group'].isna().sum()))
res = res.dropna().reset_index(drop=True)
print('events analysed:', len(res))
print('min Wilcoxon p on residuals (3v3): %.4f  (theoretical minimum for 3 vs 3 two-sided rank-sum = 0.1)' % res['p_wilcoxon_resid'].min())
strong = res['class'] == 'DS_strong'
print('strong DS events analysed:', int(strong.sum()))
print('Skill residual+Wilcoxon: p<0.05 among strong DS: %d ; p<0.10: %d' % ((res.loc[strong, 'p_wilcoxon_resid'] < 0.05).sum(), (res.loc[strong, 'p_wilcoxon_resid'] <= 0.10).sum()))
print('OLS logit_psi ~ group + batch + RIN (group coef): p<0.05 among strong DS: %d / %d ; false positives among null: %d / %d' % (
    (res.loc[strong, 'p_ols_group'] < 0.05).sum(), strong.sum(),
    (res.loc[res['class'].str.startswith('nochange'), 'p_ols_group'] < 0.05).sum(), res['class'].str.startswith('nochange').sum()))
assert res['p_wilcoxon_resid'].min() >= 0.0999, 'Wilcoxon 3v3 cannot go below p=0.1'
print('ASSERT OK: residual+Wilcoxon route cannot reach p<0.05 at 3v3 (min p 0.1)')
