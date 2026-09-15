"""Input 3 (Edge): collapse UFBoot<95 branches and zero-length branches on an IQ-TREE tree run with -B 1000 -alrt 1000
(dual 'SH-aLRT/UFBoot' labels) that contains two exact duplicate sequences.  SYNTHETIC data."""
from Bio import Phylo

TREE = 'edge16.treefile'

print('--- Step A: Skill snippet as written')
tree = Phylo.read(TREE, 'newick')              # support parsed into clade.confidence
n0 = len(tree.get_nonterminals())
print('confidence values:', [c.confidence for c in tree.get_nonterminals()])
print('name values      :', [c.name for c in tree.get_nonterminals()])
tree.collapse_all(lambda c: c.confidence is not None and c.confidence < 70)   # 70 for std bootstrap; use 95 for UFBoot2
tree.collapse_all(lambda c: c.confidence is not None and c.confidence < 95)
tree.collapse_all(lambda c: c.branch_length is not None and c.branch_length < 1e-8)   # collapse genuinely-zero branches
print('internal nodes', n0, '->', len(tree.get_nonterminals()), '(no error raised)')

print('--- Step B: adapted - parse the dual label from clade.name, collapse on UFBoot < 95')
def ufboot(c):
    if c.name and '/' in c.name:
        return float(c.name.split('/')[1])
    return c.confidence
tree = Phylo.read(TREE, 'newick')
d_before = tree.distance('I6', 'Fast8')
low = [(c.name, [t.name for t in c.get_terminals()]) for c in tree.get_nonterminals() if ufboot(c) is not None and ufboot(c) < 95]
print('UFBoot<95 nodes:', low)
tree.collapse_all(lambda c: ufboot(c) is not None and ufboot(c) < 95)
print('internal nodes', n0, '->', len(tree.get_nonterminals()), '| I6-Fast8 patristic', round(d_before, 6), '->', round(tree.distance('I6', 'Fast8'), 6))

print('--- Step C: zero-length threshold vs IQ-TREE 1e-6 branch floor')
tree = Phylo.read(TREE, 'newick')
bl = [(c.name or '(internal)', c.branch_length) for c in tree.find_clades() if c.branch_length is not None]
print('branches < 1e-8 :', [b for b in bl if b[1] < 1e-8])
print('branches <= 1e-6:', [b for b in bl if b[1] <= 1e-6])
print('duplicates I1/I1_dup and I5/I5_dup form clades of zero-length tips; UFBoot on (I5,I5_dup) =',
      [c.name for c in tree.get_nonterminals() if {t.name for t in c.get_terminals()} == {'I5', 'I5_dup'}])
tree.collapse_all(lambda c: ufboot(c) is not None and ufboot(c) < 95)
Phylo.write(tree, 'edge16_collapsed.nwk', 'newick')
Phylo.draw_ascii(tree)
