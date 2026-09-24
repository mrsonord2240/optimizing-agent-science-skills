#!/usr/bin/env python3
"""Score rMATS / leafcutter / Shiba / SUPPA2 output against the SYNTHETIC planted truth (data/sim/truth.tsv).
Usage: eval_sim.py truth.tsv outdir
Reads (whichever exist): outdir/rmats_{AvB,AvC}/out/SE.MATS.JC.txt, outdir/lc/ds_{AvB,AvC}_{cluster_significance,effect_sizes}.txt
Truth convention: delta_B_minus_A = planted PSI(B) - PSI(A). rMATS IncLevelDifference = mean(b1)-mean(b2) = A - B => expected sign = -delta.
leafcutter effect = second group - first group; on the SKIPPING intron (start=base+200,end=base+901) the expected sign is
-(delta) ... (PSI up in B => skipping usage down in B => negative).
"""
import sys, os, json
import numpy as np
import pandas as pd

truth = pd.read_csv(sys.argv[1], sep='\t')
out = sys.argv[2]
truth['base'] = truth['exonStart_0base'] - 500
truth = truth.set_index('gene')
strong = truth.index[truth['class'] == 'DS_strong']
weak = truth.index[truth['class'] == 'DS_weak']
null = truth.index[truth['class'].isin(['nochange', 'nochange_lowcov'])]
lowcov = truth.index[truth['class'] == 'nochange_lowcov']
summary = {}


def report(tool, cmp, called, dirn_ok=None, tested=None):
    """called: set of gene ids called significant; dirn_ok: dict gene->bool (only for called)"""
    is_null_cmp = cmp == 'AvC'
    r = {'called_total': len(called)}
    if is_null_cmp:
        r['false_positives'] = len(called)
        r['genes_tested'] = tested
    else:
        r['strong_detected'] = f'{len(called & set(strong))}/{len(strong)}'
        r['weak_detected'] = f'{len(called & set(weak))}/{len(weak)}'
        r['false_positives_null'] = len(called & set(null))
        r['false_positives_lowcov'] = len(called & set(lowcov))
        if dirn_ok is not None:
            tp = called & set(strong) | called & set(weak)
            r['direction_correct'] = f'{sum(dirn_ok.get(g, False) for g in tp)}/{len(tp)}'
        r['genes_tested'] = tested
    summary[f'{tool}|{cmp}'] = r
    print(f'{tool:34s} {cmp}: {json.dumps(r)}')


def load_rmats(cmp):
    p = f'{out}/rmats_{cmp}/out/SE.MATS.JC.txt'
    if not os.path.exists(p):
        return None
    se = pd.read_csv(p, sep='\t')
    se['gene'] = se['GeneID'].str.strip('"')
    return se


def minrep(s):
    return s.str.split(',').apply(lambda x: min(int(v) for v in x))


for cmp in ('AvB', 'AvC'):
    se = load_rmats(cmp)
    if se is None:
        continue
    se['min_inc'] = minrep(se['IJC_SAMPLE_1']).combine(minrep(se['IJC_SAMPLE_2']), min)
    se['min_skip'] = minrep(se['SJC_SAMPLE_1']).combine(minrep(se['SJC_SAMPLE_2']), min)
    d = se.set_index('gene')
    exp_sign = -np.sign(truth['delta_B_minus_A'])
    tested = int(d['FDR'].notna().sum())
    settings = {
        'rMATS standard (FDR<.05,|dPSI|>.10)': (d['FDR'] < 0.05) & (d['IncLevelDifference'].abs() > 0.10),
        'rMATS Skill full (+min_inc+min_skip>=10)': (d['FDR'] < 0.05) & (d['IncLevelDifference'].abs() > 0.10) & ((d['min_inc'] + d['min_skip']) >= 10),
        'rMATS FDR<.05 only': d['FDR'] < 0.05,
        'rMATS lenient (FDR<.10,|dPSI|>.05)': (d['FDR'] < 0.10) & (d['IncLevelDifference'].abs() > 0.05),
    }
    for name, mask in settings.items():
        called = set(d.index[mask])
        dirn = {g: bool(np.sign(d.loc[g, 'IncLevelDifference']) == exp_sign[g]) for g in called if g in truth.index and truth.loc[g, 'delta_B_minus_A'] != 0}
        report(name, cmp, called, dirn, tested)
    if cmp == 'AvB':
        se.to_csv(f'{out}/rmats_AvB_annot.tsv', sep='\t', index=False)
    summary[f'rmats_{cmp}_calls_std'] = sorted(set(d.index[settings['rMATS standard (FDR<.05,|dPSI|>.10)']]))

for cmp in ('AvB', 'AvC'):
    cs, es = f'{out}/lc/ds_{cmp}_cluster_significance.txt', f'{out}/lc/ds_{cmp}_effect_sizes.txt'
    if not os.path.exists(cs):
        continue
    c = pd.read_csv(cs, sep='\t')
    e = pd.read_csv(es, sep='\t')
    e['start'] = e['intron'].str.split(':').str[1].astype(int)
    e['end'] = e['intron'].str.split(':').str[2].astype(int)
    e['gene'] = ['G%03d' % (s // 3000) for s in e['start']]
    e['clu'] = e['intron'].str.extract(r'(clu_\d+)')[0]
    c['clu'] = c['cluster'].str.extract(r'(clu_\d+)')[0]
    # gene per cluster
    cg = e.groupby('clu')['gene'].first()
    c['gene'] = c['clu'].map(cg)
    ok = c[c['status'] == 'Success'].copy()
    # skipping intron effect per gene (start=base+200,end=base+901)
    skip = e[(e['end'] - e['start']) == 701].set_index('gene')['deltapsi']
    exp_sign = -np.sign(truth['delta_B_minus_A'])
    tested = int(len(ok))
    for name, mask in {'leafcutter FDR<.05': ok['p.adjust'] < 0.05,
                       'leafcutter FDR<.05 & |skip dPSI|>.10': (ok['p.adjust'] < 0.05) & ok['gene'].map(skip).abs().gt(0.10)}.items():
        called = set(ok.loc[mask, 'gene'])
        dirn = {g: bool(np.sign(skip.get(g, 0)) == exp_sign[g]) for g in called if g in truth.index and truth.loc[g, 'delta_B_minus_A'] != 0}
        report(name, cmp, called, dirn, tested)
        summary[f'leafcutter_{cmp}_calls_{name}'] = sorted(called)

for cmp in ('AvB', 'AvC'):
    p = f'{out}/shiba_{cmp}/out/results/splicing/PSI_SE.txt'
    if not os.path.exists(p):
        p = f'{out}/../in5b_{cmp}/out/results/splicing/PSI_SE.txt'
    if not os.path.exists(p) or (out.endswith('in5c') and '/in5b_' in p):
        continue
    sh = pd.read_csv(p, sep='\t')
    d = sh.set_index('gene_id')
    d = d[d.index.isin(truth.index)]
    tested = int(d['q'].notna().sum())
    exp_sign = np.sign(truth['delta_B_minus_A'])  # Shiba dPSI = alt - ref = (B or C) - A
    for name, mask in {'Shiba Diff events==Yes (q<.05,|dPSI|>.10,reads>=10)': d['Diff events'] == 'Yes',
                       'Shiba q<.05 only': d['q'] < 0.05}.items():
        called = set(d.index[mask])
        dirn = {g: bool(np.sign(d.loc[g, 'dPSI']) == exp_sign[g]) for g in called if truth.loc[g, 'delta_B_minus_A'] != 0}
        report(name, cmp, called, dirn, tested)
        summary[f'shiba_{cmp}_calls_{name}'] = sorted(called)

# concordance rMATS standard x leafcutter FDR<.05 & dPSI>.10 for AvB
try:
    a = set(summary['rmats_AvB_calls_std'])
    b = set(summary['leafcutter_AvB_calls_leafcutter FDR<.05 & |skip dPSI|>.10'])
    both = a & b
    print('concordance AvB: rMATS n=%d, leafcutter n=%d, both n=%d; both & null = %d; both & true DS = %d' % (
        len(a), len(b), len(both), len(both & set(null)), len(both & (set(strong) | set(weak)))))
    a = set(summary['rmats_AvC_calls_std'])
    b = set(summary['leafcutter_AvC_calls_leafcutter FDR<.05 & |skip dPSI|>.10'])
    print('concordance AvC (null): rMATS n=%d, leafcutter n=%d, both n=%d' % (len(a), len(b), len(a & b)))
except KeyError as ex:
    print('concordance skipped:', ex)

json.dump({k: v for k, v in summary.items() if isinstance(v, dict)}, open(f'{out}/sim_summary.json', 'w'), indent=1)
