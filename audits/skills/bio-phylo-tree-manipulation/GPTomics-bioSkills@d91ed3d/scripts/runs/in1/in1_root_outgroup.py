"""Input 1 (Canonical): root the IQ-TREE ML tree on OutA+OutB and check ingroup monophyly.
Step A = the Skill's snippet verbatim (file name changed). Step B = adaptation after Step A misfires."""
import sys
sys.path.insert(0, '..')
from Bio import Phylo
from rootsplit import score

TREE = '../../data/og16_ml.treefile'
INGROUP = ['I%d' % i for i in range(1, 15) if i != 8] + ['Fast8']

print('--- Step A: Skill snippet as written')
tree = Phylo.read(TREE, 'newick')
outgroup = [{'name': 'OutA'}, {'name': 'OutB'}]      # multiple close outgroups beat a single long branch

if tree.is_monophyletic([tree.find_any(name='OutA'), tree.find_any(name='OutB')]):
    tree.root_with_outgroup(*outgroup)               # root_with_outgroup, NOT root_with_midpoint
    print('rooted:', score(tree, ['OutA', 'OutB']))
else:
    print('outgroup not monophyletic: root placement is unreliable, re-check taxon choice')

print('root children as read:', [len(c.get_terminals()) for c in tree.root.clades])

print('--- Step B: adapted - treat the input as unrooted; root on one outgroup tip first, then test the split')
tree = Phylo.read(TREE, 'newick')
tree.root_with_outgroup({'name': 'OutA'})           # move the arbitrary basal trifurcation off the outgroup pair
og = [tree.find_any(name=n) for n in ('OutA', 'OutB')]
ing = [tree.find_any(name=n) for n in INGROUP]
# after rooting on OutA, {OutA,OutB} is a split iff the ingroup is monophyletic
print('ingroup monophyletic after rooting on OutA:', bool(tree.is_monophyletic(ing)))
tree.root_with_outgroup(*outgroup)
ok, desc = score(tree, ['OutA', 'OutB'])
print('rooted on OutA+OutB:', desc, '| matches TRUE root:', ok)
print('ingroup monophyletic:', bool(tree.is_monophyletic([tree.find_any(name=n) for n in INGROUP])),
      '| outgroup monophyletic:', bool(tree.is_monophyletic([tree.find_any(name=n) for n in ('OutA', 'OutB')])))
# root-branch support is not root confidence: report the support label on the ingroup stem
stem = tree.common_ancestor(*[tree.find_any(name=n) for n in INGROUP])
print('ingroup stem label (SH-aLRT/UFBoot, a clade-support value, NOT root confidence):', stem.name, stem.confidence)
Phylo.write(tree, 'og16_rooted.nwk', 'newick')
true = Phylo.read('../../data/og16_true.nwk', 'newick')
# topology check of rooted ingroup vs truth via ingroup clades
def clades(t):
    s = set()
    for c in t.get_nonterminals():
        names = frozenset(x.name for x in c.get_terminals())
        if 1 < len(names) < len(t.get_terminals()):
            s.add(names)
    return s
print('rooted clade sets identical to true rooted tree:', clades(tree) == clades(true))
Phylo.draw_ascii(tree)
