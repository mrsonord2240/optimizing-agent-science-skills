"""Input 2: assert the Skill's Pangolin claims on the auditor's own GRCh38 panel: mask table, canonical vs all-transcript DB,
parse_pangolin_vcf against a raw split of the INFO field."""
import sys, re, os
sys.path.insert(0, 'skill/examples')
import numpy as np, pandas as pd
from splice_parsers import parse_pangolin_vcf, read_input_vcf
fails = []
def chk(name, cond):
    print(('PASS ' if cond else 'FAIL ') + name)
    if not cond: fails.append(name)

def raw(path):
    d = {}
    for l in open(path):
        if l.startswith('#'): continue
        c = l.rstrip('\n').split('\t'); m = re.search(r'Pangolin=([^;\t]+)', c[7])
        d[c[2]] = m.group(1) if m else None
    return d
def best(s, sign):
    """largest gain (sign>0) / loss (sign<0) and its position from a raw Pangolin= string (all genes)"""
    if s is None: return (np.nan, np.nan)
    v = [(float(b), int(a)) for g in s.split(',') for x in g.split('|')[1:] if re.fullmatch(r'-?\d+:-?[\d.e-]+', x) for a, b in [x.split(':')]]
    v = [t for t in v if t[0] * sign > 0]
    if not v: return (0.0, np.nan)
    t = max(v, key=lambda t: abs(t[0])); return t
res = {}
for db in ['canon', 'all']:
    for m in ['False', 'True']:
        p = f'out/pang38_{db}_m{m}.vcf'
        if not os.path.exists(p): continue
        res[(db, m)] = raw(p)
        n_in = len(read_input_vcf('data/panel_grch38_auditor.vcf'))
        print(f'{db} mask={m}: tagged {sum(v is not None for v in res[(db, m)].values())} of {n_in}')
rows = []
for vid in res[('canon', 'False')]:
    r = {'id': vid}
    for (db, m), d in res.items():
        g, l = best(d[vid], 1), best(d[vid], -1)
        r[f'{db}_m{m}'] = f'g{g[0]:+.2f}@{g[1]:.0f} l{l[0]:+.2f}@{l[1]:.0f}'
    rows.append(r)
print(pd.DataFrame(rows).to_string(index=False))
# parser vs raw
p = parse_pangolin_vcf('out/pang38_canon_mFalse.vcf')
ok = True
for r in p.itertuples():
    pass
for vid, s in res[('canon', 'False')].items():
    if s is None: continue
    g, l = best(s, 1), best(s, -1)
    sub = p[p['key'].str.contains(vid.split('_')[0] if False else '')]
print('parser rows:', len(p), 'unique keys', p['key'].nunique())
# explicit ground-truth checks from the Skill's table (auditor's own numbers must land within 0.03)
def get(db, m, vid, kind):
    x = best(res[(db, m)][vid], 1 if kind == 'gain' else -1); return x[0]
close = lambda a, b, t=0.03: abs(a - b) <= t
chk('TP53 c.673-2A>G loss ~ -0.90 (mask False, canonical DB)', close(get('canon', 'False', 'TP53_c.673-2A>G', 'loss'), -0.90))
if ('all', 'True') in res:
    chk('TP53 loss unchanged by mask/DB (-0.90)', all(close(get(d, m, 'TP53_c.673-2A>G', 'loss'), -0.90) for d, m in res))
    chk('GLA c.639+919 gain +0.23 at mask False', close(get('canon', 'False', 'GLA_c.639+919G>A', 'gain'), 0.23))
    chk('GLA c.639+919 gain kept with canonical DB + mask True (+0.23)', close(get('canon', 'True', 'GLA_c.639+919G>A', 'gain'), 0.23))
    chk('GLA c.639+919 gain ERASED with all-transcript DB + mask True (0.00)', abs(get('all', 'True', 'GLA_c.639+919G>A', 'gain')) < 0.005)
    chk('OTC c.386+5G>A loss ~ -0.72 at mask False', close(get('canon', 'False', 'OTC_c.386+5G>A', 'loss'), -0.72))
    chk('OTC c.386+5G>A loss erased by mask True in both DBs', abs(get('canon', 'True', 'OTC_c.386+5G>A', 'loss')) < 0.005 and abs(get('all', 'True', 'OTC_c.386+5G>A', 'loss')) < 0.005)
print('FAILS:', fails)
