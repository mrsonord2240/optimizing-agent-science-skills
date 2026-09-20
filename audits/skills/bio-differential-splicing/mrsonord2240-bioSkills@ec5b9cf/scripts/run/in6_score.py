#!/usr/bin/env python3
"""Score rMATS --paired-stats (PAIRADISE) vs unpaired rMATS on SYNTHETIC sim2p against planted truth. Usage: in6_score.py truth.tsv <in6 dir>
Pairs: b1 = N1..N5, b2 = T1..T5; rMATS IncLevelDifference = mean(b1) - mean(b2) = normal - tumor, so expected sign = -sign(delta(tumor - normal))."""
import sys, os
import numpy as np, pandas as pd
truth = pd.read_csv(sys.argv[1], sep='\t', keep_default_na=False).set_index('gene'); w = sys.argv[2]
strong = set(truth.index[truth['class'] == 'DS_strong']); mod = set(truth.index[truth['class'] == 'DS_moderate']); weak = set(truth.index[truth['class'] == 'DS_weak'])
null = set(truth.index[truth['class'].str.startswith('null')]); se_ds = set(truth.index[(truth['etype'] == 'SE') & truth['class'].str.startswith('DS')])
minrep = lambda s: s.astype(str).str.split(',').apply(lambda x: min(int(v) for v in x))
for name in ('pf', 'up'):
    frames = []
    for ev in ('SE', 'A5SS', 'A3SS'):
        p = f'{w}/{name}/out/{ev}.MATS.JC.txt'
        d = pd.read_csv(p, sep='\t'); d['ev'] = ev; frames.append(d)
    d = pd.concat(frames, ignore_index=True)
    assert 'FDR' in d.columns and len(d) > 50, f'{name}: table must have FDR and events'
    d['gene'] = d['GeneID'].str.strip('"')
    d['mi'] = minrep(d['IJC_SAMPLE_1']).combine(minrep(d['IJC_SAMPLE_2']), min); d['ms'] = minrep(d['SJC_SAMPLE_1']).combine(minrep(d['SJC_SAMPLE_2']), min)
    call = (d['FDR'] < 0.05) & (d['IncLevelDifference'].abs() > 0.10) & ((d['mi'] + d['ms']) >= 10)
    c = set(d.loc[call, 'gene'])
    se = d[d['ev'] == 'SE'].set_index('gene')
    dirn = sum(np.sign(se.loc[g, 'IncLevelDifference']) == -np.sign(truth.loc[g, 'delta_cond1_minus_cond0']) for g in c & se_ds if g in se.index)
    print(f'{"PAIRADISE (--paired-stats)" if name == "pf" else "unpaired rMATS LRT"}: events {len(d)}, FDR NaN {int(d["FDR"].isna().sum())}, called {len(c)} | strong {len(c & strong)}/{len(strong)} moderate {len(c & mod)}/{len(mod)} weak {len(c & weak)}/{len(weak)} | false calls (null genes) {len(c & null)} | direction correct (SE) {dirn}/{len(c & se_ds)}')
