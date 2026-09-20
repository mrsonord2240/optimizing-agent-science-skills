"""Probe: which denominator does pwalign::pid use for PID3/PID4 on the pairs where the Skill's PID4 differs (V0)?"""
import os, sys, pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, 'skill', 'examples')); sys.dont_write_bytecode = True
import identity_matrix as IM
df = pd.read_csv(os.path.join(HERE, 'data', 'derived', 'pid_pairs_R.tsv'), sep='\t', keep_default_na=False)
rows = []
for r in df.itertuples():
    n_id = sum(x == y and x != '-' for x, y in zip(r.a, r.b))
    la, lb = len(r.a.replace('-', '')), len(r.b.replace('-', ''))
    d4 = n_id / (r.PID4 / 100); d3 = n_id / (r.PID3 / 100)
    mean_region = (la + lb) / 2
    rows.append(dict(name=r.name, n_id=n_id, la=la, lb=lb, pfull=len(r.pfull), sfull=len(r.sfull), alnlen=len(r.a),
                     pw_PID4_denom=round(d4, 3), mean_region=mean_region, mean_full=(len(r.pfull) + len(r.sfull)) / 2, pw_PID3_denom=round(d3, 3), min_region=min(la, lb), typ=r.name.split('|')[-1]))
t = pd.DataFrame(rows)
t['d4_eq_region'] = (t.pw_PID4_denom - t.mean_region).abs() < 1e-6
t['d4_eq_full'] = (t.pw_PID4_denom - t.mean_full).abs() < 1e-6
t['d4_eq_aln'] = (t.pw_PID4_denom - t.alnlen).abs() < 1e-6
print(t.groupby('typ')[['d4_eq_region', 'd4_eq_full', 'd4_eq_aln']].sum().assign(n=t.groupby('typ').size()))
bad = t[~t.d4_eq_region]
print(len(bad), 'pairs where pwalign PID4 denominator != mean of ungapped aligned-region lengths')
print(bad[['name', 'n_id', 'la', 'lb', 'alnlen', 'pw_PID4_denom', 'mean_region', 'mean_full']].head(8).to_string())
# candidate: pwalign PID4 denominator = mean of (aligned length + ... ) i.e. mean of the two INCLUDING gap columns?  test: alnlen - gaps_in_other
t['cand_mean_with_terminal'] = 0.0
