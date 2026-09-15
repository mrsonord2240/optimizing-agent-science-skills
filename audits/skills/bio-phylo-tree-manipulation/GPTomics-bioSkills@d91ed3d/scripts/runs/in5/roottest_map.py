"""Map IQ-TREE --root-test candidate IDs (branchID in rootnr.roottest.trees) to root bipartitions; score vs TRUE root X|Y."""
import sys, re; sys.path.insert(0, '../..')
import pandas as pd
from io import StringIO
from Bio import Phylo
from rootsplit import score
d = pd.read_csv('rootnr.roottest.csv', comment='#')
trees = {}
for l in open('rootnr.roottest.trees'):
    m = re.match(r'\[\s*branchID=(\d+)[^\]]*\](.*)', l.strip())
    if m:
        trees[int(m.group(1))] = m.group(2)
X = ['X%d' % i for i in range(1, 10)]
for _, r in d.iterrows():
    ok, desc = score(Phylo.read(StringIO(trees[int(r.ID)]), 'newick'), X)
    if r['p-AU'] >= 0.05:
        print(f"ID {int(r.ID):2d} deltaL {r.deltaL:6.2f} p-AU {r['p-AU']:.3f} true={ok} {desc}")
print('root positions NOT rejected by AU (p>=0.05):', int((d['p-AU'] >= 0.05).sum()), 'of', len(d))
