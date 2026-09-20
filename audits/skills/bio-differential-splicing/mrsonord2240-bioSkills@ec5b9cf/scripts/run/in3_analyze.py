#!/usr/bin/env python3
"""Cross-tool summary on the REAL chrX 2v2 (real = GBR vs YRI; perm = one GBR + one YRI per side). Keys by Ensembl gene id.
Usage: in3_analyze.py <in3 dir> <gtf>. Asserts: all tables non-empty; prints the Skill-quoted numbers for comparison."""
import sys, re, os
import numpy as np, pandas as pd

root, gtf = sys.argv[1], sys.argv[2]
sym2ens, ens2sym = {}, {}
for l in open(gtf):
    f = l.rstrip('\n').split('\t')
    if len(f) > 8 and f[2] == 'transcript':
        g = re.search(r'gene_id "([^"]+)"', f[8]).group(1)
        n = re.search(r'gene_name "([^"]+)"', f[8])
        if n:
            sym2ens.setdefault(n.group(1), g)
            ens2sym[g] = n.group(1)
minrep = lambda s: s.str.split(',').apply(lambda x: min(int(v) for v in x))
res = {}
for cmp in ('real', 'perm'):
    sets = {}
    g_std, g_fdr, tot = set(), set(), 0
    for ev in ('SE', 'A3SS', 'A5SS', 'MXE', 'RI'):
        d = pd.read_csv(f'{root}/rmats_{cmp}/rmats_output/{ev}.MATS.JC.txt', sep='\t')
        tot += len(d)
        d['gene'] = d['GeneID'].str.strip('"')
        d['mi'] = minrep(d['IJC_SAMPLE_1']).combine(minrep(d['IJC_SAMPLE_2']), min)
        d['ms'] = minrep(d['SJC_SAMPLE_1']).combine(minrep(d['SJC_SAMPLE_2']), min)
        fdr = d['FDR'] < 0.05
        std = fdr & (d['IncLevelDifference'].abs() > 0.10)
        full = std & ((d['mi'] + d['ms']) >= 10)
        print(f'[{cmp}] rMATS {ev}: events {len(d)}, FDR<.05 {int(fdr.sum())}, +|dPSI|>.10 {int(std.sum())}, +coverage>=10 (Skill filter) {int(full.sum())}')
        g_fdr |= set(d.loc[std, 'gene'])
        g_std |= set(d.loc[full, 'gene'])
    assert tot > 200, 'rMATS tables must have events'
    sets['rMATS(Skill filter)'] = g_std
    sets['rMATS(FDR+dPSI)'] = g_fdr
    g_sh = set()
    for ev in ('SE', 'FIVE', 'THREE', 'MXE', 'RI', 'MSE', 'AFE', 'ALE'):
        p = f'{root}/shiba_{cmp}/shiba_out/results/splicing/PSI_{ev}.txt'
        if os.path.exists(p):
            d = pd.read_csv(p, sep='\t')
            y = d['Diff events'] == 'Yes'
            print(f'[{cmp}] Shiba {ev}: tested {len(d)}, Diff==Yes {int(y.sum())}')
            g_sh |= set(d.loc[y, 'gene_id'])
    sets['Shiba'] = g_sh
    c = pd.read_csv(f'{root}/lc/ds_{cmp}_cluster_significance.txt', sep='\t')
    ok = c[c['status'] == 'Success']
    sg = ok[ok['p.adjust'] < 0.05]
    print(f'[{cmp}] leafcutter: clusters tested {len(ok)}, p.adjust<.05 {len(sg)}')
    sets['leafcutter'] = {sym2ens[x] for s in sg['genes'].dropna() for x in str(s).split(',') if x in sym2ens}
    for m, pre in (('empirical', 'diff'), ('classical', 'diffc')):
        gs, n_sig, n_t, n_nan, minp = set(), 0, 0, 0, 1.0
        for ev in ('SE', 'A5', 'A3', 'MX', 'RI'):
            f = f'{root}/suppa/{cmp}/{pre}_{ev}.dpsi'
            d = pd.read_csv(f, sep='\t', index_col=0)
            d.columns = ['dpsi', 'p']
            n_t += len(d)
            n_nan += int(d['p'].isna().sum())
            d = d.dropna()
            if len(d):
                minp = min(minp, d['p'].min())
            s = d[(d['p'] < 0.05) & (d['dpsi'].abs() > 0.10)]
            n_sig += len(s)
            gs |= {i.split(';')[0] for i in s.index}
        print(f'[{cmp}] SUPPA2 {m} (-gc): events {n_t}, p=NaN {n_nan}, min p {minp:.4f}, p<.05&|dPSI|>.10: {n_sig}')
        sets[f'SUPPA2 {m}'] = gs
    res[cmp] = sets
for cmp, sets in res.items():
    print(f'== {cmp}: genes called per tool', {k: len(v) for k, v in sets.items()})
tools = ['rMATS(Skill filter)', 'leafcutter', 'Shiba', 'SUPPA2 empirical']
r = res['real']
for i, a in enumerate(tools):
    for b in tools[i + 1:]:
        print(f'  overlap {a:22s} x {b:18s}: {len(r[a] & r[b])} (of {len(r[a])}, {len(r[b])})')
print('rMATS(FDR+dPSI) x leafcutter (real):', sorted(ens2sym.get(g, g) for g in r['rMATS(FDR+dPSI)'] & r['leafcutter']))
