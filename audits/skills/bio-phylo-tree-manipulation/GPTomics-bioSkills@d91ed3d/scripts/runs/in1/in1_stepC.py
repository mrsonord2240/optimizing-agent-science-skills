"""Input 1 Step C: why Step B failed, and the working Bio.Phylo recipe (root on an INGROUP tip first)."""
import sys
sys.path.insert(0, '..')
from Bio import Phylo
from rootsplit import score
TREE = '../../data/og16_ml.treefile'
outgroup = [{'name': 'OutA'}, {'name': 'OutB'}]
INGROUP = ['I%d' % i for i in range(1, 15) if i != 8] + ['Fast8']

t = Phylo.read(TREE, 'newick'); t.root_with_outgroup({'name': 'OutA'})
print('after rooting on OutA, MRCA(OutA,OutB) is root:', t.common_ancestor({'name': 'OutA'}, {'name': 'OutB'}) is t.root)
t.root_with_outgroup(*outgroup); print('then root_with_outgroup(OutA,OutB):', score(t, ['OutA', 'OutB']))

t = Phylo.read(TREE, 'newick')
t.root_with_outgroup({'name': 'I1'})               # any ingroup tip: makes the outgroup a proper clade
print('after rooting on I1, outgroup monophyletic:', bool(t.is_monophyletic([t.find_any(name='OutA'), t.find_any(name='OutB')])))
t.root_with_outgroup(*outgroup)
ok, d = score(t, ['OutA', 'OutB'])
print('root_with_outgroup(OutA,OutB):', d, '| matches TRUE root:', ok)
print('ingroup monophyletic:', bool(t.is_monophyletic([t.find_any(name=n) for n in INGROUP])))
def clades(tr):
    return {frozenset(x.name for x in c.get_terminals()) for c in tr.get_nonterminals() if 1 < len(c.get_terminals()) < 16}
true = Phylo.read('../../data/og16_true.nwk', 'newick')
print('rooted clade sets identical to TRUE rooted tree:', clades(t) == clades(true))
print('root-to-tip Fast8 vs I7:', round(t.distance(t.root, 'Fast8'), 3), round(t.distance(t.root, 'I7'), 3))
Phylo.write(t, 'og16_rooted.nwk', 'newick')
print(open('og16_rooted.nwk').read().strip())
