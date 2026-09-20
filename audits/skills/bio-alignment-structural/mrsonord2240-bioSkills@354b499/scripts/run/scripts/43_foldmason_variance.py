"""Quantify run-to-run variance of Foldmason --refine-iters 100 (3 unseeded runs on the same 5 real structures):
fraction of aligned residue pairs shared between runs, for every sequence pair (cwd = run/work/det)."""
import itertools
def fa(p):
    d = {}; k = None
    for l in open(p):
        l = l.strip()
        if l.startswith('>'): k = l[1:].split()[0]; d[k] = ''
        elif k: d[k] += l
    return d
def pairs(x, y):
    i = j = 0; o = set()
    for c, d in zip(x, y):
        if c != '-': i += 1
        if d != '-': j += 1
        if c != '-' and d != '-': o.add((i, j))
    return o
runs = [fa(f'o_r100{i}_aa.fa') for i in (1, 2, 3)]
fr = []
for a, b in itertools.combinations(range(3), 2):
    for p, q in itertools.combinations(list(runs[0]), 2):
        s, t = pairs(runs[a][p], runs[a][q]), pairs(runs[b][p], runs[b][q])
        fr.append(len(s & t) / max(len(s | t), 1))
print('mean Jaccard of aligned pairs between two unseeded runs: %.3f  min %.3f' % (sum(fr)/len(fr), min(fr)))
print('columns per run:', [len(next(iter(r.values()))) for r in runs])
# same-family pairs only (globin-globin: 1MBN/1A3N/2LHB ; kinase-kinase: 1ATP/1HCK) vs cross-family
fam = {'1MBN': 'g', '1A3N': 'g', '2LHB': 'g', '1ATP': 'k', '1HCK': 'k'}
same, cross = [], []
for a, b in itertools.combinations(range(3), 2):
    for p, q in itertools.combinations(list(runs[0]), 2):
        s, t = pairs(runs[a][p], runs[a][q]), pairs(runs[b][p], runs[b][q]); j = len(s & t) / max(len(s | t), 1)
        (same if fam[p.split('_')[0]] == fam[q.split('_')[0]] else cross).append((j, p, q))
print('same-family pairs: mean %.3f min %.3f | cross-family: mean %.3f min %.3f' % (sum(x[0] for x in same)/len(same), min(same)[0], sum(x[0] for x in cross)/len(cross), min(cross)[0]))
print('worst same-family:', min(same))
