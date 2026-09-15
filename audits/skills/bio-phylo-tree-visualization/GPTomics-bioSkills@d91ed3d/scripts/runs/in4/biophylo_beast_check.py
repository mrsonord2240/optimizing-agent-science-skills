"""Input 4 check: what Bio.Phylo does with a BEAST/TreeAnnotator MCC Nexus (does it 'silently drop' annotations?)."""
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from Bio import Phylo

HERE = os.path.dirname(os.path.abspath(__file__))
tree = Phylo.read(os.path.join(HERE, '..', '..', 'data', 'beast_mcc.tree'), 'nexus')
root = tree.root
print('root.comment (raw string kept):', (root.comment or '')[:120])
kids = root.clades[0]
print('child confidence:', kids.confidence, '| child name:', kids.name, '| child comment:', (kids.comment or '')[:90])
print('tips:', [t.name for t in tree.get_terminals()][:4])
fig, ax = plt.subplots(figsize=(8, 5))
Phylo.draw(tree, axes=ax, do_show=False)
print('text objects drawn containing HPD:', sum('HPD' in t.get_text() for t in ax.texts))
fig.savefig(os.path.join(HERE, 'biophylo_beast_view.png'), bbox_inches='tight', dpi=80)
plt.close(fig)
