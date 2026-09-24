#!/usr/bin/env python3
"""Score rMATS / leafcutter / Shiba output on SYNTHETIC sim2 against the planted truth (data/sim2/truth.tsv), per design size n.
Usage: eval_sim2.py <truth.tsv> <dir with n<N>/{rmats,shiba}_{AvB,AvC}/ and n<N>/lc/> <n> [<n> ...]
Call rule everywhere: FDR (or p.adjust / q) < 0.05 and |dPSI| > 0.10 (+ per-replicate coverage filter for rMATS = the Skill's snippet).
A gene is called if any of its events is called. Classes: DS_strong (28), DS_moderate (8), DS_weak (6); null classes = null, null_overdisp, null_lowcov.
Direction is scored on SE genes only (rMATS IncLevelDifference = A - B, so expected sign = -sign(delta); Shiba dPSI = alt - ref = B - A; leafcutter on the skipping intron)."""
import sys, os, json
import numpy as np, pandas as pd

truth = pd.read_csv(sys.argv[1], sep='\t', keep_default_na=False).set_index('gene')   # class 'null' must not become NaN
root = sys.argv[2]
ns = [int(x) for x in sys.argv[3:]]
strong = set(truth.index[truth['class'] == 'DS_strong']); mod = set(truth.index[truth['class'] == 'DS_moderate']); weak = set(truth.index[truth['class'] == 'DS_weak'])
null = set(truth.index[truth['class'].str.startswith('null')])
se_ds = set(truth.index[(truth['etype'] == 'SE') & truth['class'].str.startswith('DS')])
summary = {}


def row(tool, n, cmp, called, dirn=None, tested=None):
    r = {'called': len(called)}
    if cmp == 'AvC':
        r['false_calls'] = len(called)
    else:
        r['strong'] = f'{len(called & strong)}/{len(strong)}'
        r['moderate'] = f'{len(called & mod)}/{len(mod)}'
        r['weak'] = f'{len(called & weak)}/{len(weak)}'
        r['false_calls'] = len(called & null)
        if dirn is not None:
            tp = called & se_ds
            r['dir_ok_SE'] = f'{sum(dirn.get(g, False) for g in tp)}/{len(tp)}'
    r['tested'] = tested
    summary[f'{tool}|n={n}|{cmp}'] = r
    print(f'{tool:34s} n={n} {cmp}: {json.dumps(r)}', flush=True)
    return r


minrep = lambda s: s.astype(str).str.split(',').apply(lambda x: min(int(v) for v in x))   # n=1: a bare integer, not a comma list
for n in ns:
    d0 = f'{root}/n{n}'
    for cmp in ('AvB', 'AvC'):
        # ---- rMATS (SE, A5SS, A3SS) ----
        frames = []
        for ev in ('SE', 'A5SS', 'A3SS'):
            p = f'{d0}/rmats_{cmp}/out/{ev}.MATS.JC.txt'
            if os.path.exists(p):
                d = pd.read_csv(p, sep='\t')
                d['ev'] = ev
                frames.append(d)
        if frames:
            d = pd.concat(frames, ignore_index=True)
            d['gene'] = d['GeneID'].str.strip('"')
            d['mi'] = minrep(d['IJC_SAMPLE_1']).combine(minrep(d['IJC_SAMPLE_2']), min)
            d['ms'] = minrep(d['SJC_SAMPLE_1']).combine(minrep(d['SJC_SAMPLE_2']), min)
            std = (d['FDR'] < 0.05) & (d['IncLevelDifference'].abs() > 0.10)
            full = std & ((d['mi'] + d['ms']) >= 10)
            for name, mask in (('rMATS FDR+dPSI', std), ('rMATS Skill filter (+cov>=10)', full)):
                called = set(d.loc[mask, 'gene'])
                dd = d[(d['ev'] == 'SE')].set_index('gene')
                dirn = {g: bool(np.sign(dd.loc[g, 'IncLevelDifference'].iloc[0] if hasattr(dd.loc[g, 'IncLevelDifference'], 'iloc') else dd.loc[g, 'IncLevelDifference']) == -np.sign(truth.loc[g, 'delta_cond1_minus_cond0']))
                        for g in called if g in dd.index and g in se_ds}
                row(name, n, cmp, called, dirn, int(d['FDR'].notna().sum()))
        # ---- leafcutter ----
        cs, es = f'{d0}/lc/ds_{cmp}_cluster_significance.txt', f'{d0}/lc/ds_{cmp}_effect_sizes.txt'
        if os.path.exists(cs):
            c = pd.read_csv(cs, sep='\t')
            e = pd.read_csv(es, sep='\t')
            e['start'] = e['intron'].str.split(':').str[1].astype(int)
            e['end'] = e['intron'].str.split(':').str[2].astype(int)
            e['gene'] = ['G%03d' % (s // 3000) for s in e['start']]
            e['clu'] = e['intron'].str.extract(r'(clu_\d+)')[0]
            c['clu'] = c['cluster'].str.extract(r'(clu_\d+)')[0]
            c['gene'] = c['clu'].map(e.groupby('clu')['gene'].first())
            ok = c[c['status'] == 'Success']
            emax = e.assign(a=e['deltapsi'].abs()).groupby('gene')['a'].max()
            for name, mask in (('leafcutter FDR', ok['p.adjust'] < 0.05), ('leafcutter FDR+max|dPSI|>.10', (ok['p.adjust'] < 0.05) & ok['gene'].map(emax).gt(0.10))):
                called = set(ok.loc[mask, 'gene'])
                skip = e[(e['end'] - e['start']) == 701].set_index('gene')['deltapsi']
                dirn = {g: bool(np.sign(skip.get(g, 0)) == -np.sign(truth.loc[g, 'delta_cond1_minus_cond0'])) for g in called if g in se_ds}
                row(name, n, cmp, called, dirn, int(len(ok)))
        # ---- Shiba ----
        frames = []
        for ev in ('SE', 'FIVE', 'THREE'):
            p = f'{d0}/shiba_{cmp}/out/results/splicing/PSI_{ev}.txt'
            if os.path.exists(p):
                d = pd.read_csv(p, sep='\t')
                d['ev'] = ev
                frames.append(d)
        if frames:
            d = pd.concat(frames, ignore_index=True)
            d = d[d['gene_id'].isin(truth.index)]
            called = set(d.loc[d['Diff events'] == 'Yes', 'gene_id'])
            dd = d[d['ev'] == 'SE'].set_index('gene_id')
            dirn = {g: bool(np.sign(dd.loc[g, 'dPSI']) == np.sign(truth.loc[g, 'delta_cond1_minus_cond0'])) for g in called if g in dd.index and g in se_ds}
            row('Shiba Diff==Yes', n, cmp, called, dirn, int(d['q'].notna().sum()))
json.dump(summary, open(f'{root}/summary_{"_".join(map(str, ns))}.json', 'w'), indent=1)
