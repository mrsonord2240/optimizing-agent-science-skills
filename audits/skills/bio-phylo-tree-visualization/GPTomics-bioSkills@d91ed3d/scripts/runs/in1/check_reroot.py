"""Auditor check (second, independent method): after Bio.Phylo root_with_outgroup, is each SH-aLRT/UFBoot label still
on the bipartition IQ-TREE computed it for? Compares split->label maps before and after rerooting, then writes a
corrected figure (C_) where labels are re-attached by split."""
import os, re
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from Bio import Phylo

HERE = os.path.dirname(os.path.abspath(__file__))
TREE = os.path.join(HERE, '..', '..', 'data', 'iq', 'primates16.treefile')

def splits(tree):
    alltips = frozenset(t.name for t in tree.get_terminals())
    out = {}
    for c in tree.get_nonterminals():
        if c.name and re.fullmatch(r'[\d.]+/[\d.]+', c.name):
            s = frozenset(t.name for t in c.get_terminals())
            key = min(s, alltips - s, key=lambda x: (len(x), sorted(x)))
            out[key] = c.name
    return out, alltips

orig = Phylo.read(TREE, 'newick')
before, alltips = splits(orig)
rer = Phylo.read(TREE, 'newick')
rer.root_with_outgroup('Microcebus_murinus', 'Otolemur_garnettii')
after, _ = splits(rer)
moved = 0
for k, lab in before.items():
    now = after.get(k)
    ok = now == lab
    moved += not ok
    print(f"{'OK   ' if ok else 'MOVED'} {lab:>9} true split {sorted(k)[:3]}{'...' if len(k) > 3 else ''} -> after reroot: {now}")
print('labels on the wrong split after Bio.Phylo root_with_outgroup:', moved, 'of', len(before))

# corrected figure: re-attach labels by split
tree = Phylo.read(TREE, 'newick')
tree.root_with_outgroup('Microcebus_murinus', 'Otolemur_garnettii')
tree.ladderize()
for c in tree.get_nonterminals():
    c.name = None
lab = {}
for c in tree.get_nonterminals():
    s = frozenset(t.name for t in c.get_terminals())
    key = min(s, alltips - s, key=lambda x: (len(x), sorted(x)))
    if key in before and len(s) < len(alltips):
        lab[c] = before[key]

def dual(c):
    if c in lab:
        a, b = map(float, lab[c].split('/'))
        return lab[c] + ('' if a >= 80 and b >= 95 else ' *')
    return ''

fig, ax = plt.subplots(figsize=(8, 6))
Phylo.draw(tree, axes=ax, do_show=False, label_func=lambda c: c.name.replace('_', ' ') if c.is_terminal() else '',
           branch_labels=dual)
ax.set_xlabel('substitutions per site'); ax.set_ylabel(''); ax.set_yticks([])
for s in ('top', 'right', 'left'):
    ax.spines[s].set_visible(False)
ax.set_title('ML phylogram (IQ-TREE 2.4.0, HKY+F+G4); node labels = SH-aLRT (%) / UFBoot (%)', fontsize=10)
fig.text(0.01, -0.03, 'Rooted on Strepsirrhini (outgroup); support re-attached by bipartition after rooting. Ladderized for '
         'legibility; ordering carries no phylogenetic meaning. * = fails SH-aLRT >= 80 and UFBoot >= 95.', fontsize=8, wrap=True)
for ext in ('pdf', 'svg'):
    fig.savefig(os.path.join(HERE, f'C_primates16_support.{ext}'), bbox_inches='tight')
fig.savefig(os.path.join(HERE, 'C_primates16_support_view.png'), bbox_inches='tight', dpi=110)
print('corrected labels placed:', len(lab))
