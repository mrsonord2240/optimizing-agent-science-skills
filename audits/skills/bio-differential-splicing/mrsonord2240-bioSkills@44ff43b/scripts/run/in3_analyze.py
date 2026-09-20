#!/usr/bin/env python3
"""Cross-tool comparison on the REAL chrX 2v2 (real = GBR vs YRI; perm = one GBR + one YRI per side).
Keys everything by Ensembl gene id (rMATS GeneID, Shiba gene_id, SUPPA2 event prefix; leafcutter via gene_name -> ENSG from the GTF).
Prints counts at the Skill's standard thresholds and overlaps. Usage: in3_analyze.py <runroot> <gtf>"""
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


def minrep(s):
    return s.str.split(',').apply(lambda x: min(int(v) for v in x))


res = {}
for cmp in ('real', 'perm'):
    sets = {}
    # rMATS
    tot_all, tot_std = 0, 0
    g_std, g_fdr = set(), set()
    for ev in ('SE', 'A3SS', 'A5SS', 'MXE', 'RI'):
        d = pd.read_csv(f'{root}/in3/rmats_{cmp}/out/{ev}.MATS.JC.txt', sep='\t')
        d['gene'] = d['GeneID'].str.strip('"')
        d['mi'] = minrep(d['IJC_SAMPLE_1']).combine(minrep(d['IJC_SAMPLE_2']), min)
        d['ms'] = minrep(d['SJC_SAMPLE_1']).combine(minrep(d['SJC_SAMPLE_2']), min)
        fdr = d['FDR'] < 0.05
        std = fdr & (d['IncLevelDifference'].abs() > 0.10)
        full = std & ((d['mi'] + d['ms']) >= 10)
        print(f'[{cmp}] rMATS {ev}: events {len(d)}, FDR<.05 {int(fdr.sum())}, +|dPSI|>.10 {int(std.sum())}, +min_inc+min_skip>=10 (Skill) {int(full.sum())}')
        g_fdr |= set(d.loc[fdr & (d["IncLevelDifference"].abs() > 0.10), 'gene'])
        g_std |= set(d.loc[full, 'gene'])
        if ev == 'SE' and cmp == 'real':
            # of the FDR&dPSI hits, how many have per-replicate min coverage < 10
            print('   SE hits failing the coverage filter:', int((std & ~full).sum()), 'of', int(std.sum()))
    sets['rMATS(Skill filter)'] = g_std
    sets['rMATS(FDR+dPSI only)'] = g_fdr
    # Shiba
    g_sh = set(); nsh = 0
    for ev in ('SE', 'FIVE', 'THREE', 'MXE', 'RI', 'MSE', 'AFE', 'ALE'):
        p = f'{root}/in3/shiba_{cmp}/out/results/splicing/PSI_{ev}.txt'
        if os.path.exists(p):
            d = pd.read_csv(p, sep='\t')
            y = d['Diff events'] == 'Yes'
            print(f'[{cmp}] Shiba {ev}: tested {len(d)}, Diff==Yes {int(y.sum())}')
            g_sh |= set(d.loc[y, 'gene_id']); nsh += int(y.sum())
    sets['Shiba'] = g_sh
    # leafcutter
    p = f'{root}/in3b/ds_{cmp}_cluster_significance.txt'
    c = pd.read_csv(p, sep='\t')
    ok = c[c['status'] == 'Success']
    sg = ok[ok['p.adjust'] < 0.05]
    print(f'[{cmp}] leafcutter: clusters tested {len(ok)}, p.adjust<.05 {len(sg)}, genes {sorted(set(sg["genes"].dropna()))[:12]}')
    gl = set()
    for s in sg['genes'].dropna():
        for x in str(s).split(','):
            if x in sym2ens:
                gl.add(sym2ens[x])
    sets['leafcutter'] = gl
    # SUPPA2
    for m in ('empirical', 'classical'):
        gs = set(); n_sig = 0; n_t = 0; n_nan = 0; minp = 1.0
        for ev in ('SE', 'A5', 'A3', 'MX', 'RI'):
            f = f'{root}/in3c/diff_{cmp}_{m}_{ev}.dpsi'
            d = pd.read_csv(f, sep='\t', index_col=0)
            d.columns = ['dpsi', 'p']
            n_t += len(d)
            n_nan += int(d['p'].isna().sum())
            d = d.dropna()
            if len(d):
                minp = min(minp, d['p'].min())
            s = d[(d['p'] < 0.05) & (d['dpsi'].abs() > 0.10)]
            n_sig += len(s)
            gs |= set(i.split(';')[0] for i in s.index)
        print(f'[{cmp}] SUPPA2 {m} (-gc): events {n_t}, p=NaN {n_nan}, min p {minp:.4f}, p<.05&|dPSI|>.10: {n_sig}')
        sets[f'SUPPA2 {m}'] = gs
    res[cmp] = sets

print()
for cmp, sets in res.items():
    print(f'== {cmp}: genes called per tool', {k: len(v) for k, v in sets.items()})
tools = ['rMATS(Skill filter)', 'leafcutter', 'Shiba', 'SUPPA2 empirical', 'SUPPA2 classical']
r = res['real']
print('pairwise overlap (real): |A&B| / min(|A|,|B|)')
for i, a in enumerate(tools):
    for b in tools[i + 1:]:
        print(f'  {a:22s} x {b:18s}: {len(r[a] & r[b])} / {min(len(r[a]), len(r[b]))}')
allthree = r['rMATS(Skill filter)'] & r['leafcutter'] & r['Shiba']
print('rMATS & leafcutter & Shiba (real):', sorted(ens2sym.get(g, g) for g in allthree))
print('rMATS & leafcutter (real):', sorted(ens2sym.get(g, g) for g in r['rMATS(Skill filter)'] & r['leafcutter']))
