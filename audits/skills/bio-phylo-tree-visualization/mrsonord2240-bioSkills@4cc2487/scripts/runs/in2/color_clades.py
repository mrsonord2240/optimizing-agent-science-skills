"""Input 2 (Variant A): colour great apes red and Old World monkeys blue, ladderize, export PDF + SVG.
Part A = SKILL.md 'Color branches by group' recipe verbatim; Part B = adapted clade-level colouring."""
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from Bio import Phylo
from Bio.Phylo.PhyloXML import BranchColor

HERE = os.path.dirname(os.path.abspath(__file__))
TREE = os.path.join(HERE, '..', '..', 'data', 'iq', 'primates16.treefile')
tree = Phylo.read(TREE, 'newick')

# ---- Part A: verbatim ----
xtree = tree.as_phyloxml()                     # phyloXML carries branch color through draw()
for clade in xtree.find_clades():
    if clade.name and clade.name.startswith('Homo'):
        clade.color = BranchColor.from_name('red')

fig, ax = plt.subplots(figsize=(10, 8))
Phylo.draw(xtree, axes=ax, do_show=False)
fig.savefig(os.path.join(HERE, 'A_colored_tree.pdf'), bbox_inches='tight')
fig.savefig(os.path.join(HERE, 'A_colored_tree_view.png'), bbox_inches='tight', dpi=80)
plt.close(fig)
print('[A] clades coloured:', [c.name for c in xtree.find_clades() if c.color is not None])
print('[A] internal names printed as labels:', [c.name for c in xtree.get_nonterminals() if c.name][:4])

# plain Newick tree: does clade.color really need phyloXML? (Skill's Common Errors claim)
t2 = Phylo.read(TREE, 'newick')
next(t2.find_clades('Homo_sapiens')).color = 'red'
print('[A] plain Newick Clade accepts .color =', next(t2.find_clades('Homo_sapiens')).color)

# ---- Part B: adapted ----
tree = Phylo.read(TREE, 'newick')
tree.root_with_outgroup('Microcebus_murinus', 'Otolemur_garnettii')
tree.ladderize()
for c in tree.get_nonterminals():
    c.name = None                               # drop IQ-TREE SH-aLRT/UFBoot strings (not requested here)
apes = tree.common_ancestor('Homo_sapiens', 'Pan_troglodytes', 'Pan_paniscus', 'Gorilla_gorilla', 'Pongo_abelii')
owm = tree.common_ancestor('Macaca_mulatta', 'Papio_anubis', 'Chlorocebus_sabaeus', 'Colobus_guereza')
apes.color = 'red'
owm.color = 'blue'
print('[B] great-ape MRCA tips:', sorted(t.name for t in apes.get_terminals()))
print('[B] OWM MRCA tips:', sorted(t.name for t in owm.get_terminals()))
fig, ax = plt.subplots(figsize=(8, 6))
Phylo.draw(tree, axes=ax, do_show=False, label_func=lambda c: c.name.replace('_', ' ') if c.is_terminal() else '')
ax.set_xlabel('substitutions per site'); ax.set_ylabel(''); ax.set_yticks([])
ax.set_title('Primate ML tree: red = great apes (Hominidae), blue = Old World monkeys (Cercopithecidae)', fontsize=9)
fig.text(0.01, -0.02, 'Rooted on Strepsirrhini; ladderized for legibility, ordering carries no phylogenetic meaning.', fontsize=8)
for ext in ('pdf', 'svg'):
    fig.savefig(os.path.join(HERE, f'B_colored.{ext}'), bbox_inches='tight')
fig.savefig(os.path.join(HERE, 'B_colored_view.png'), bbox_inches='tight', dpi=100)
plt.close(fig)
print('[B] saved B_colored.pdf/.svg')
