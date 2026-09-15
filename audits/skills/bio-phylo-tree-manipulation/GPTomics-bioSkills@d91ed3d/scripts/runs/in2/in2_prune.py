"""Input 2 (Variant A): keep a taxon subset (not a clade) and prove every surviving patristic distance is unchanged,
in Bio.Phylo (Skill default) and ete3 (user's pipeline), plus the Skill's non-monophyly warning."""
import itertools, copy
from Bio import Phylo
from ete3 import Tree

TREE = '../../data/og16_ml.treefile'
keep = {'OutA', 'I1', 'I3', 'I6', 'Fast8', 'I9', 'I11', 'I13'}

tree = Phylo.read(TREE, 'newick')
pairs = list(itertools.combinations(sorted(keep), 2))
before = {p: tree.distance(*p) for p in pairs}

# Skill: extracting "the clade" of a non-monophyletic set pulls in extra taxa
mrca = tree.common_ancestor(*[tree.find_any(name=n) for n in keep - {'OutA'}])
print('MRCA clade of the 7 ingroup targets holds', len(mrca.get_terminals()), 'taxa (extra taxa -> use induced subtree)')

# Skill snippet (keep-set loop)
for term in list(tree.get_terminals()):
    if term.name not in keep:
        tree.prune(term)                             # collapses the degree-2 parent and sums branch lengths
after = {p: tree.distance(*p) for p in pairs}
dmax = max(abs(before[p] - after[p]) for p in pairs)
print('Bio.Phylo: taxa', len(tree.get_terminals()), '| max |d_before - d_after| over', len(pairs), 'pairs =', f'{dmax:.2e}')
print('Bio.Phylo leftover degree-2 nodes:', sum(1 for c in tree.get_nonterminals() if len(c.clades) == 1))
print('support labels still attached (valid for the FULL taxon set only):', [c.name for c in tree.get_nonterminals() if c.name])
Phylo.write(tree, 'og16_subset_biophylo.nwk', 'newick')

# ete3 as in the Skill, with and without the flag
for flag in (True, False):
    e = Tree(TREE, format=1)
    eb = {p: e.get_distance(*p) for p in pairs}
    e.prune(list(keep), preserve_branch_length=flag)
    ea = {p: e.get_distance(*p) for p in pairs}
    print(f'ete3 preserve_branch_length={flag}: max diff = {max(abs(eb[p]-ea[p]) for p in pairs):.4f}',
          '| Fast8-I1', round(eb[("Fast8","I1")], 4), '->', round(ea[("Fast8","I1")], 4))
    if flag:
        e.write(format=1, outfile='og16_subset_ete3.nwk')
print(open('og16_subset_biophylo.nwk').read().strip())
