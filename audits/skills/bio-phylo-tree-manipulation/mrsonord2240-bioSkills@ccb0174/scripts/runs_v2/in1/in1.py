"""Input 1 (Canonical): the fixed Skill's outgroup-rooting snippet VERBATIM (file name only) on the SYNTHETIC IQ-TREE
tree og16_ml.treefile; auditor checks against the simulated rooted tree."""
import sys
sys.path.insert(0, '..')
from rootsplit import score

from Bio import Phylo

tree = Phylo.read('../../data/og16_ml.treefile', 'newick')
outgroup = [{'name': 'OutA'}, {'name': 'OutB'}]      # multiple close outgroups beat a single long branch

tree.root_with_outgroup({'name': 'I1'})              # any INGROUP tip: makes the outgroup a clade of the temporary root
if tree.is_monophyletic([tree.find_any(**o) for o in outgroup]):
    stem = tree.common_ancestor(*outgroup).branch_length
    tree.root_with_outgroup(*outgroup, outgroup_branch_length=stem / 2)   # bifurcating root on the outgroup stem
else:
    print('outgroup not monophyletic: root placement is unreliable, re-check taxon choice')

# ---- auditor checks ----
ING = {'I%d' % i for i in range(1, 15) if i != 8} | {'Fast8'}
print('root children:', len(tree.root.clades), '|', score(tree, ['OutA', 'OutB']))
print('ingroup monophyletic:', bool(tree.is_monophyletic([tree.find_any(name=n) for n in ING])))
def ing_clades(t):
    return {frozenset(x.name for x in c.get_terminals()) for c in t.get_nonterminals()
            if frozenset(x.name for x in c.get_terminals()) <= ING}
print('rooted ingroup clades identical to TRUE:', ing_clades(tree) == ing_clades(Phylo.read('../../data/og16_true.nwk', 'newick')))
d0 = Phylo.read('../../data/og16_ml.treefile', 'newick').distance('I3', 'Fast8')
print('I3-Fast8 patristic before/after rooting: %.6f / %.6f' % (d0, tree.distance('I3', 'Fast8')))
Phylo.write(tree, 'og16_rooted.nwk', 'newick')
