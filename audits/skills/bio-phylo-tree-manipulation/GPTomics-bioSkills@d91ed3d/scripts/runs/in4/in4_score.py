"""Input 4 (Variant B): outgroup-free rooting of the deep 20-taxon tree - midpoint vs MAD vs MinVar, scored
against the TRUE (simulated) root X|Y.  MAD and FastRoot were run on the command line exactly as the Skill writes them."""
import sys
sys.path.insert(0, '..')
from io import StringIO
from Bio import Phylo
from rootsplit import score

X = ['X%d' % i for i in range(1, 10)]
res = {}
t = Phylo.read('deep20.nwk', 'newick'); t.root_at_midpoint()
res['midpoint (Bio.Phylo root_at_midpoint)'] = score(t, X)
mad = open('deep20.nwk.rooted').read().strip()
res['MAD 2.2 (mad.py deep20.nwk)'] = score(Phylo.read(StringIO(mad), 'newick'), X)
res['MinVar (FastRoot.py -m MV)'] = score(Phylo.read('rooted.nwk', 'newick'), X)
for k, (ok, d) in res.items():
    print(f'{k:40s} correct={ok}  {d}')
agree = res['MAD 2.2 (mad.py deep20.nwk)'][1] == res['MinVar (FastRoot.py -m MV)'][1]
print('MAD and MinVar agree:', agree)
