"""Inputs 1-3: the fixed Skill's Bio.Phylo recipes VERBATIM (file names only) on SYNTHETIC data; auditor checks after
each block. in1 = support recipe on the IQ-TREE primate treefile; in2 = colour recipe on the same Newick; in3 = scaled
panel recipe on the 320-tip tree."""
import os, sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import to_rgb
part = sys.argv[1]
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data')
os.makedirs(part, exist_ok=True); os.chdir(part)

if part == 'in1':
    from Bio import Phylo
    tree = Phylo.read(os.path.join(D, 'iq', 'primates16.treefile'), 'newick')
    tree.ladderize()             # legibility only; ordering carries NO phylogenetic meaning -- say so in the caption

    def tip_only(clade):
        return clade.name if clade.is_terminal() else ''

    import re

    for clade in tree.get_nonterminals():            # IQ-TREE -B + --alrt: '88.5/92' stays in clade.name, confidence None
        if clade.confidence is None and clade.name and re.fullmatch(r'[\d.]+/[\d.]+', clade.name):
            clade.sh_alrt, clade.ufboot = (float(v) for v in clade.name.split('/'))   # SH-aLRT / UFBoot (last)
            clade.name = None                        # otherwise the default label_func prints the raw string

    def support_label(clade):
        # the measure MUST be stated in the legend/caption
        if clade.is_terminal():
            return ''
        if getattr(clade, 'ufboot', None) is not None:
            return f'{clade.sh_alrt:.0f}/{clade.ufboot:.0f}'
        return f'{clade.confidence:.0f}' if clade.confidence is not None else ''

    if not any(support_label(c) for c in tree.get_nonterminals()):
        print('WARNING: no internal clade has readable support -- the figure will show none')
    fig, ax = plt.subplots(figsize=(12, 10))
    Phylo.draw(tree, axes=ax, do_show=False, label_func=tip_only, branch_labels=support_label)
    ax.set_title('Node support: SH-aLRT (%) / UFBoot (%)')   # name the measure(s) the file actually holds
    fig.savefig('supported_tree.svg', bbox_inches='tight')
    # ---- auditor ----
    drawn = [t.get_text().strip() for t in ax.texts if '/' in t.get_text()]
    print('support labels drawn:', len(drawn), drawn[:6], '| raw names left:', [c.name for c in tree.get_nonterminals() if c.name])
    print('title:', ax.get_title(), '| xlabel:', ax.get_xlabel())
    plt.close(fig)
    from Bio.Phylo.BaseTree import Tree
    t0 = Phylo.read(__import__('io').StringIO('((A:1,B:1):1,(C:1,D:1):1);'), 'newick')
    print('label-free tree warning fires:', not any(support_label(c) for c in t0.get_nonterminals()))
elif part == 'in2':
    from Bio import Phylo
    tree = Phylo.read(os.path.join(D, 'iq', 'primates16.treefile'), 'newick')
    tree.common_ancestor({'name': 'Homo_sapiens'}, {'name': 'Pongo_abelii'}).color = 'red'   # works on a Newick-read tree

    fig, ax = plt.subplots(figsize=(10, 8))
    Phylo.draw(tree, axes=ax, do_show=False)       # as_phyloxml() is needed only to EXPORT colors to phyloXML
    fig.savefig('colored_tree.pdf', bbox_inches='tight')
    # ---- auditor: count red line segments and the clade they cover ----
    reds = 0
    for coll in ax.collections:
        for c in coll.get_colors():
            reds += tuple(round(x, 3) for x in c[:3]) == (1.0, 0.0, 0.0)
    for ln in ax.lines:
        reds += to_rgb(ln.get_color()) == (1.0, 0.0, 0.0)
    mrca = tree.common_ancestor({'name': 'Homo_sapiens'}, {'name': 'Pongo_abelii'})
    print('red segments drawn:', reds, '| MRCA tips:', sorted(t.name for t in mrca.get_terminals()))
    print('internal raw labels still printed by default label_func:', [t.get_text().strip() for t in ax.texts if '/' in t.get_text()][:3])
    plt.close(fig)
else:
    from Bio import Phylo
    tree = Phylo.read(os.path.join(D, 'big320.nwk'), 'newick')
    n_tips = len(tree.get_terminals())
    if n_tips > 150:
        print('>~150 tips: switch to a circular layout or strips/rings (ggtree, iTOL) instead of a taller panel')
    height = min(max(8, n_tips * 0.25), 40)         # ~0.25 in/tip keeps ~6-8 pt labels from colliding; capped

    fig, ax = plt.subplots(figsize=(10, height))
    Phylo.draw(tree, axes=ax, do_show=False)
    ax.set_yticks([])                               # hide only the meaningless y ticks and spines
    ax.spines[['left', 'top', 'right']].set_visible(False)
    fig.savefig('scaled_tree.pdf', bbox_inches='tight')
    # ---- auditor ----
    print('n_tips', n_tips, '| height', height, '| xlabel', repr(ax.get_xlabel()),
          '| x tick labels', [t.get_text() for t in ax.get_xticklabels() if t.get_text()][:7])
    fig.canvas.draw()
    bbox = [t.get_window_extent() for t in ax.texts[:50]]
    overl = sum(bbox[i].overlaps(bbox[i + 1]) for i in range(len(bbox) - 1))
    print('adjacent tip-label overlaps in first 50 labels:', overl, '| font size', {t.get_fontsize() for t in ax.texts})
    plt.close(fig)
