import gzip, os, numpy as np
W = os.environ['NP'] + '/work/a3'
res = []
def chk(n, ok, i=''): res.append(bool(ok)); print('PASS' if ok else 'FAIL', n, i)
def lines(f): return [l.rstrip('\n').split('\t') for l in gzip.open(f'{W}/out.{f}.gz', 'rt')]
nucpos = lines('nucpos.bed'); occpk = lines('occpeaks.bed'); nfr = lines('nfrpos.bed'); comb = lines('nucmap_combined.bed')
chk('nucpos.bed non-empty (nucleosome calls are the headline output)', len(nucpos) > 0, f'{len(nucpos)} rows')
chk('occpeaks non-empty', len(occpk) > 0, str(len(occpk)))
occ = np.array([float(x) for x in (l.rstrip('\n').split('\t')[3] for l in gzip.open(f'{W}/out.occ.bedgraph.gz', 'rt')) if x.lower() != 'nan'])
chk('occupancy in [0,1] and non-degenerate', occ.min() >= 0 and occ.max() <= 1.0001 and occ.std() > 0.02, f'n={len(occ)} min={occ.min():.3f} max={occ.max():.3f} sd={occ.std():.3f} mean={occ.mean():.3f}')
tss = [int(l.split('\t')[1]) for l in open(f'{W}/tss.bed')]
d = np.array([min(abs(int(l[1]) - t) for t in tss) for l in nfr]) if nfr else np.array([])
chk('NFR positions lie within 300 bp of a TSS (median)', len(d) > 0 and np.median(d) < 300, f'n={len(nfr)} median distance {np.median(d) if len(d) else None}')
# nucmap_combined rows: how many come from called positions vs occupancy peaks
print('nucmap_combined rows', len(comb), '| first row', comb[0][:8] if comb else None)
chk('nucmap_combined contains called nucleosomes (>= as many as occpeaks + nucpos)', len(comb) >= len(occpk) + len(nucpos) and len(nucpos) > 0, f'{len(comb)} vs {len(occpk)}+{len(nucpos)}')
print('SUMMARY', sum(res), '/', len(res))
