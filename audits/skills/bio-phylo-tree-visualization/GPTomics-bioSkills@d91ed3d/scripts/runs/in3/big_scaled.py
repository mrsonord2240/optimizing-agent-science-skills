"""Input 3 (Edge): 320-tip tree. Part A = SKILL.md 'Scale the panel to tip count' recipe verbatim."""
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from Bio import Phylo

HERE = os.path.dirname(os.path.abspath(__file__))
tree = Phylo.read(os.path.join(HERE, '..', '..', 'data', 'big320.nwk'), 'newick')

n_tips = len(tree.get_terminals())
height = max(8, n_tips * 0.25)                  # ~0.25 in/tip keeps ~6-8 pt labels from colliding

fig, ax = plt.subplots(figsize=(10, height))
Phylo.draw(tree, axes=ax, do_show=False)
print('n_tips', n_tips, 'figure height (in)', height, 'x-label before axis off:', repr(ax.get_xlabel()))
ax.axis('off')
fig.savefig(os.path.join(HERE, 'scaled_tree.pdf'), bbox_inches='tight')
print('tick labels visible after axis(off):', ax.xaxis.get_visible() and ax.axison)
# default font size of tip labels drawn by Phylo.draw
sizes = {t.get_fontsize() for t in ax.texts}
print('tip label font sizes (pt):', sizes, '| text objects:', len(ax.texts))
plt.close(fig)
