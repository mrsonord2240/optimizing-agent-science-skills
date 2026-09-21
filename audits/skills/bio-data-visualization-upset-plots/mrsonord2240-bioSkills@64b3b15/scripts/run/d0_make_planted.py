"""SYNTHETIC planted-overlap gene sets (labelled synthetic). 8 sets: D is a strict subset of A, H is empty, >6 sets.
Writes data/planted_sets.tsv (set<TAB>gene) and data/planted_truth.json (independent set-operation truth)."""
import json, itertools
patterns = {  # membership pattern -> number of genes (exclusive)
 'A':12,'B':9,'C':7,'AB':6,'AC':3,'BC':4,'ABC':2,'AD':5,'ABD':2,'E':6,'EF':4,'EFG':3,'G':2,'CG':1}
names = list('ABCDEFGH')
sets = {n:[] for n in names}
gid = 0
for pat,cnt in patterns.items():
    for _ in range(cnt):
        gid += 1
        g = f'GENE{gid:03d}'
        for ch in pat: sets[ch].append(g)
# 5 genes in the universe that are in no set at all must NOT appear
with open('F:/OpenScience/audits/bio-data-visualization-upset-plots/data/planted_sets.tsv','w',encoding='utf-8') as f:
    f.write('set\tgene\n')
    for n in names:
        for g in sets[n]: f.write(f'{n}\t{g}\n')
S = {n:set(v) for n,v in sets.items()}
truth = {'set_sizes':{n:len(S[n]) for n in names}, 'exclusive':{}, 'inclusive':{}}
for k in range(1,len(names)+1):
    for combo in itertools.combinations(names,k):
        inter = set.intersection(*[S[c] for c in combo])
        others = [S[n] for n in names if n not in combo]
        excl = inter - (set.union(*others) if others else set())
        if excl: truth['exclusive']['-'.join(combo)] = len(excl)
        if inter: truth['inclusive']['-'.join(combo)] = len(inter)
truth['n_union'] = len(set.union(*S.values()))
json.dump(truth, open('F:/OpenScience/audits/bio-data-visualization-upset-plots/data/planted_truth.json','w'), indent=1)
print(truth['set_sizes']); print(len(truth['exclusive']),'nonzero exclusive intersections; union',truth['n_union'])
print(truth['exclusive'])
with open('F:/OpenScience/audits/bio-data-visualization-upset-plots/data/planted_truth.tsv','w',encoding='utf-8') as f:
    f.write('combo\texclusive\tinclusive\n')
    for k in range(1,len(names)+1):
        for combo in itertools.combinations(names,k):
            key='-'.join(combo)
            e=truth['exclusive'].get(key,0); i=truth['inclusive'].get(key,0)
            if e or i: f.write(f'{key}\t{e}\t{i}\n')
