"""Test the Skill's specific API claims exactly as written (Biopython 1.88, ete3 3.1.3, DendroPy 5.0.13)."""
from io import StringIO
import copy
from Bio import Phylo

def rd(s):
    return Phylo.read(StringIO(s), 'newick')

print('== C1 is_monophyletic return semantics')
t = rd('((A:1,B:1):1,(C:1,D:1):1);')
r = t.is_monophyletic([t.find_any(name='A'), t.find_any(name='B')])
print('  monophyletic ->', type(r).__name__, repr(r)[:40], 'bool=', bool(r))
r2 = t.is_monophyletic([t.find_any(name='A'), t.find_any(name='C')])
print('  not monophyletic ->', repr(r2))

print('== C2 SKILL outgroup snippet on an IQ-TREE-style unrooted (trifurcating) tree whose root sits next to OutA')
# IQ-TREE writes the first taxon (often the outgroup) at the basal trifurcation
iq = '(OutA:0.1,OutB:0.1,((I1:0.1,I2:0.1):0.1,(I3:0.1,I4:0.1):0.1):0.2);'
tree = rd(iq)
outgroup = [{'name': 'OutA'}, {'name': 'OutB'}]
if tree.is_monophyletic([tree.find_any(name='OutA'), tree.find_any(name='OutB')]):
    tree.root_with_outgroup(*outgroup)
    print('  rooted:', tree.format('newick').strip())
else:
    print('  SKILL SNIPPET SAYS: outgroup not monophyletic: root placement is unreliable, re-check taxon choice')
print('  (in the unrooted tree {OutA,OutB}|{I1..I4} IS a split)')
tree = rd(iq)
tree.root_with_outgroup(*outgroup)
print('  root_with_outgroup(*dicts) anyway ->', tree.format('newick').strip())
print('  after rooting, is_monophyletic(OutA,OutB)=', bool(tree.is_monophyletic([tree.find_any(name='OutA'), tree.find_any(name='OutB')])),
      ' ingroup mono=', bool(tree.is_monophyletic([tree.find_any(name=n) for n in ['I1', 'I2', 'I3', 'I4']])))
# case where outgroup straddles the arbitrary root
iq2 = '(I1:0.1,(I2:0.1,(I3:0.1,I4:0.1):0.1):0.1,(OutA:0.1,OutB:0.1):0.2);'
tree = rd(iq2)
print('  root at I1 trifurcation, outgroup clade intact: is_mono=', bool(tree.is_monophyletic([tree.find_any(name='OutA'), tree.find_any(name='OutB')])))

print('== C3 root_at_midpoint exists; root_with_midpoint does not')
t = rd('((A:1,B:1):1,(C:1,D:5):1);')
t.root_at_midpoint(); print('  midpoint:', t.format('newick').strip())
print('  hasattr root_with_midpoint:', hasattr(t, 'root_with_midpoint'))

print('== C4 Bio.Phylo prune sums branch lengths (patristic check), incl. pruning next to the root')
s = '((Human:0.1,Chimp:0.2):0.3,(Mouse:0.4,Rat:0.5):0.6,Zebrafish:1.0);'
t = rd(s)
pairs = [('Human', 'Rat'), ('Mouse', 'Rat'), ('Human', 'Zebrafish')]
before = {p: t.distance(*p) for p in pairs}
for term in list(t.get_terminals()):
    if term.name == 'Chimp':
        t.prune(term)
after = {p: t.distance(*p) for p in pairs}
print('  drop Chimp:', {f'{a}-{b}': (round(before[(a, b)], 6), round(after[(a, b)], 6)) for a, b in pairs})
# bifurcating rooted tree: pruning a child of a root child
s2 = '((A:0.1,B:0.2):0.3,(C:0.4,D:0.5):0.6);'
t = rd(s2); b = t.distance('B', 'C'); t.prune('A'); print('  rooted, drop A: B-C', b, '->', round(t.distance('B', 'C'), 6), t.format('newick').strip())
t = rd(s2); b = t.distance('C', 'D'); t.prune('A'); t.prune('B'); print('  rooted, drop A,B: C-D', b, '->', round(t.distance('C', 'D'), 6), t.format('newick').strip())
t = rd('(A:0.1,B:0.2,(C:0.4,D:0.5):0.6);'); b = t.distance('A', 'C'); t.prune('B')
print('  trifurcating root, drop B: A-C', b, '->', round(t.distance('A', 'C'), 6), t.format('newick').strip())

print('== C5 ete3 prune with / without preserve_branch_length')
from ete3 import Tree
for flag in (False, True):
    e = Tree(s)
    b = e.get_distance('Human', 'Mouse')
    e.prune(['Human', 'Mouse', 'Rat'], preserve_branch_length=flag)
    print(f'  preserve_branch_length={flag}: Human-Mouse {b} -> {e.get_distance("Human", "Mouse")}  {e.write(format=1)}')
e = Tree(s); print('  ete3 get_midpoint_outgroup:', e.get_midpoint_outgroup().get_leaf_names())

print('== C6 collapse_all on IQ-TREE dual labels SH-aLRT/UFBoot')
dual = '(OutA:0.1,OutB:0.1,((I1:0.1,I2:0.1)98.5/100:0.1,(I3:0.1,I4:0.1)45.2/62:0.1)88/97:0.2);'
t = rd(dual)
print('  internal (confidence, name):', [(c.confidence, c.name) for c in t.get_nonterminals()])
n0 = len(t.get_nonterminals())
t.collapse_all(lambda c: c.confidence is not None and c.confidence < 95)
print('  SKILL collapse (<95) internal nodes', n0, '->', len(t.get_nonterminals()), ' (expected 2 collapses of 45.2/62 node)')
single = '(OutA:0.1,OutB:0.1,((I1:0.1,I2:0.1)100:0.1,(I3:0.1,I4:0.1)62:0.1)97:0.2);'
t = rd(single); n0 = len(t.get_nonterminals())
t.collapse_all(lambda c: c.confidence is not None and c.confidence < 95)
print('  single-label UFBoot tree: internal nodes', n0, '->', len(t.get_nonterminals()), [(c.confidence) for c in t.get_nonterminals()])
print('  bare-number label 0.95 (posterior):', [c.confidence for c in rd('((A:1,B:1)0.95:1,C:1,D:1);').get_nonterminals()])

print('== C7 collapse_all with the root-clade guard? collapse_all also targets root?')
t = rd('((A:1,B:1)40:1,(C:1,D:1)30:1)20;')
try:
    t.collapse_all(lambda c: c.confidence is not None and c.confidence < 70)
    print('  ok:', t.format('newick').strip())
except Exception as ex:
    print('  ERROR', type(ex).__name__, ex)

print('== C8 DendroPy APIs named in the Skill')
import dendropy
d = dendropy.Tree.get(data=s, schema='newick', preserve_underscores=True)
for m in ['reroot_at_edge', 'reroot_at_midpoint', 'retain_taxa_with_labels', 'resolve_polytomies', 'ladderize']:
    print('  ', m, hasattr(d, m))
b = d.phylogenetic_distance_matrix().patristic_distance(d.taxon_namespace.get_taxon('Human'), d.taxon_namespace.get_taxon('Mouse'))
d.retain_taxa_with_labels(['Human', 'Mouse', 'Rat'], suppress_unifurcations=True)
a = d.phylogenetic_distance_matrix().patristic_distance(d.taxon_namespace.get_taxon('Human'), d.taxon_namespace.get_taxon('Mouse'))
print('  retain_taxa_with_labels(suppress_unifurcations=True) Human-Mouse', b, '->', a, d.as_string(schema='newick').strip())

print('== C9 ete3 resolve_polytomy / delete exist')
e = Tree('(A:1,B:1,C:1,D:1);')
print('  ', hasattr(e, 'resolve_polytomy'), hasattr(e, 'delete'), hasattr(e, 'detach'), hasattr(e, 'set_outgroup'))
