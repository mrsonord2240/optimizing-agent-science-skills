"""Input 3 (Edge): the fixed Skill's collapse snippet VERBATIM (file name; cutoff 95 as its comment prescribes for
UFBoot2) on the SYNTHETIC IQ-TREE -B 1000 -alrt 1000 tree edge16.treefile with two duplicate sequences."""
from Bio import Phylo

TREE = 'edge16.treefile'
n0 = len(Phylo.read(TREE, 'newick').get_nonterminals())
d0 = Phylo.read(TREE, 'newick').distance('I6', 'Fast8')

tree = Phylo.read(TREE, 'newick')              # single-number labels parse into clade.confidence

def support(c):                                      # IQ-TREE -B + --alrt writes '98.5/100' -> kept in c.name, confidence None
    if c.confidence is not None:
        return c.confidence
    if c.name and '/' in c.name:
        return float(c.name.split('/')[-1])          # last field = UFBoot
    return None

assert any(support(c) is not None for c in tree.get_nonterminals()), 'no readable support: collapse would silently do nothing'
tree.collapse_all(lambda c: support(c) is not None and support(c) < 95)   # 70 for std bootstrap; use 95 for UFBoot2
tree.collapse_all(lambda c: c.branch_length is not None and c.branch_length <= 1e-6)   # zero-length: match the writer's floor (IQ-TREE 1e-6)
tree.ladderize()                                     # display order only; rotation changes no biology

print('internal nodes', n0, '->', len(tree.get_nonterminals()))
print('I6-Fast8 patristic %.6f -> %.6f' % (d0, tree.distance('I6', 'Fast8')))
print('remaining labels:', [c.name for c in tree.get_nonterminals()])
print('tips still present:', len(tree.get_terminals()))
Phylo.write(tree, 'edge16_collapsed.nwk', 'newick')
Phylo.draw_ascii(tree)
# single-number labels + unreadable-support guard
t2 = Phylo.read(__import__('io').StringIO('((A:1,B:1):1,(C:1,D:1):1);'), 'newick')
try:
    assert any(support(c) is not None for c in t2.get_nonterminals()), 'no readable support: collapse would silently do nothing'
except AssertionError as e:
    print('guard on label-free tree:', e)
