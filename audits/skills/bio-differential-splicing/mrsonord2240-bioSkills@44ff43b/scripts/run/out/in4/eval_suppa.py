import sys, numpy as np, pandas as pd
truth = pd.read_csv(sys.argv[1], sep='\t').set_index('gene')
exp_sign = np.sign(truth['delta_B_minus_A'])   # SUPPA2 dPSI = mean(cond2) - mean(cond1) = B - A (verified in lib/diff_tools.py calculate_delta_psi and on G000)
strong = set(truth.index[truth['class'] == 'DS_strong']); weak = set(truth.index[truth['class'] == 'DS_weak'])
null = set(truth.index[truth['class'].isin(['nochange', 'nochange_lowcov'])])
for cmp in ('AvB', 'AvC'):
    for m in ('empirical', 'classical'):
        d = pd.read_csv(f'diff_{cmp}_{m}_SE.dpsi', sep='\t', index_col=0)
        d.columns = ['dpsi', 'p']
        d.index = [i.split(';')[0] for i in d.index]
        n_nan = int(d['p'].isna().sum()); dd = d.dropna()
        called = set(dd.index[(dd['p'] < 0.05) & (dd['dpsi'].abs() > 0.10)])
        r = dict(events=len(d), p_nan=n_nan, min_p=float(dd['p'].min()), n_called=len(called))
        if cmp == 'AvB':
            r.update(strong=f'{len(called & strong)}/{len(strong)}', weak=f'{len(called & weak)}/{len(weak)}', FP_null=len(called & null),
                     dir_ok=f"{sum(np.sign(dd.loc[g,'dpsi']) == exp_sign[g] for g in called & (strong | weak))}/{len(called & (strong | weak))}")
        else:
            r['FP_null'] = len(called)
        print(f'SUPPA2 {m:9s} {cmp}:', r)
