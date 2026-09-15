"""Input 1 Step D: bifurcating root on the outgroup STEM with outgroup_branch_length; ingroup clades vs truth."""
import sys
sys.path.insert(0, '..')
from Bio import Phylo
from rootsplit import score
TREE = '../../data/og16_ml.treefile'
t = Phylo.read(TREE, 'newick')
t.root_with_outgroup({'name': 'I1'})
stem = t.common_ancestor({'name': 'OutA'}, {'name': 'OutB'}).branch_length
t.root_with_outgroup({'name': 'OutA'}, {'name': 'OutB'}, outgroup_branch_length=stem / 2)
ok, d = score(t, ['OutA', 'OutB']); print('with outgroup_branch_length:', d, '| matches TRUE root:', ok)
ING = {'I%d' % i for i in range(1, 15) if i != 8} | {'Fast8'}
def ing_clades(tr):
    return {frozenset(x.name for x in c.get_terminals()) for c in tr.get_nonterminals() if frozenset(x.name for x in c.get_terminals()) <= ING}
true = Phylo.read('../../data/og16_true.nwk', 'newick')
print('rooted ingroup clades identical to TRUE:', ing_clades(t) == ing_clades(true))
Phylo.write(t, 'og16_rooted.nwk', 'newick'); print(open('og16_rooted.nwk').read().strip())
