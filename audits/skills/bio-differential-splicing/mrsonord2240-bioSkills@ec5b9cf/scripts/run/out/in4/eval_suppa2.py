import sys, numpy as np, pandas as pd
truth = pd.read_csv(sys.argv[1], sep='\t', keep_default_na=False).set_index('gene')
sign = np.sign(truth['delta_cond1_minus_cond0'])           # SUPPA2 dPSI = mean(cond2) - mean(cond1) = B - A
strong = set(truth.index[truth['class'] == 'DS_strong']); mod = set(truth.index[truth['class'] == 'DS_moderate']); weak = set(truth.index[truth['class'] == 'DS_weak'])
null = set(truth.index[truth['class'].str.startswith('null')]); se_ds = set(truth.index[(truth['etype'] == 'SE') & truth['class'].str.startswith('DS')])
print('planted: strong %d, moderate %d, weak %d, null genes %d' % (len(strong), len(mod), len(weak), len(null)))
for n in (2, 3, 4, 5, 6):
    for m in ('empirical', 'classical'):
        out = {}
        for cmp in ('AvB', 'AvC'):
            fr = []
            for ev in ('SE', 'A5', 'A3'):
                d = pd.read_csv(f'd_n{n}_{cmp}_{m}_{ev}.dpsi', sep='\t', index_col=0); d.columns = ['dpsi', 'p']; d.index = [i.split(';')[0] for i in d.index]; fr.append(d)
            d = pd.concat(fr); nn = int(d['p'].isna().sum()); d = d.dropna()
            called = set(d.index[(d['p'] < 0.05) & (d['dpsi'].abs() > 0.10)])
            out[cmp] = (called, float(d['p'].min()), len(d), nn, d)
        cb, minp, ne, nn, d = out['AvB']
        dirn = sum(np.sign(d.loc[g, 'dpsi']) == sign[g] for g in cb & se_ds)
        print(f'SUPPA2 {m:9s} n={n}: events {ne} (p NaN {nn}) | strong {len(cb & strong)}/{len(strong)} moderate {len(cb & mod)}/{len(mod)} weak {len(cb & weak)}/{len(weak)} | '
              f'false calls {len(cb & null)}/{len(cb)} | dir(SE) {dirn}/{len(cb & se_ds)} | min p {minp:.4f} | calls on NULL A-vs-C: {len(out["AvC"][0])}')
