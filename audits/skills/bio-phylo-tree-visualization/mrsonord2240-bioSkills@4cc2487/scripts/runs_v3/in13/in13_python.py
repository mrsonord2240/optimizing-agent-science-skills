"""Input 1 (Canonical) + Input 3 (Edge) regression, combined in one process.

Input 1 prompt: "Draw my IQ-TREE phylogram (primates16.treefile) with SH-aLRT/UFBoot
dual support labeled, and export as a vector PDF."

Input 3 prompt: "This tree has 320 tips and the labels are unreadable -- fix the panel."
"""
import re
from Bio import Phylo
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

print('=== Input 1: dual-support labeling recipe, verbatim, on primates16.treefile ===')
tree = Phylo.read('data/iq/primates16.treefile', 'newick')
tree.ladderize()

for clade in tree.get_nonterminals():
    if clade.confidence is None and clade.name and re.fullmatch(r'[\d.]+/[\d.]+', clade.name):
        clade.sh_alrt, clade.ufboot = (float(v) for v in clade.name.split('/'))
        clade.name = None


def tip_only(clade):
    return clade.name if clade.is_terminal() else ''


def support_label(clade):
    if clade.is_terminal():
        return ''
    if getattr(clade, 'ufboot', None) is not None:
        return f'{clade.sh_alrt:.0f}/{clade.ufboot:.0f}'
    return f'{clade.confidence:.0f}' if clade.confidence is not None else ''


labels = [support_label(c) for c in tree.get_nonterminals() if support_label(c)]
raw_left = [c.name for c in tree.get_nonterminals() if c.name and re.fullmatch(r'[\d.]+/[\d.]+', c.name)]
print('Support labels drawn:', labels)
print('Raw un-split support strings left in .name:', raw_left)

fig, ax = plt.subplots(figsize=(12, 10))
Phylo.draw(tree, axes=ax, do_show=False, label_func=tip_only, branch_labels=support_label)
ax.set_title('Node support: SH-aLRT (%) / UFBoot (%)')
fig.savefig('in1_supported_tree.pdf', bbox_inches='tight')
plt.close(fig)
import os
print('Saved vector file, size:', os.path.getsize('in1_supported_tree.pdf'), 'bytes')

print()
print('=== Input 3: scaled-panel recipe on a 320-tip tree ===')
tree3 = Phylo.read('data/big320.nwk', 'newick')
n_tips = len(tree3.get_terminals())
print('n_tips =', n_tips)
if n_tips > 150:
    print('>~150 tips: switch to a circular layout or strips/rings (ggtree, iTOL) instead of a taller panel')
height = min(max(8, n_tips * 0.25), 40)
print('computed height (capped at 40):', height)

fig3, ax3 = plt.subplots(figsize=(10, height))
Phylo.draw(tree3, axes=ax3, do_show=False)
ax3.set_yticks([])
ax3.spines[['left', 'top', 'right']].set_visible(False)
fig3.savefig('in3_scaled_tree.pdf', bbox_inches='tight')
plt.close(fig3)
print('x axis label present:', ax3.get_xlabel() != '' or len(ax3.get_xticklabels()) > 0)
print('num x tick labels:', len(ax3.get_xticks()))
print('y ticks hidden:', len(ax3.get_yticks()) == 0)
