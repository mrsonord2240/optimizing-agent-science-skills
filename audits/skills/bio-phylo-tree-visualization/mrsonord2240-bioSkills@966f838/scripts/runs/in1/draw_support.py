"""Input 1 (Canonical): IQ-TREE SH-aLRT/UFBoot treefile -> Bio.Phylo phylogram with support, vector export.
Part A runs the Skill's recipe exactly as written; Part B is the adapted output an agent following the Skill should deliver."""
import os, re
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from Bio import Phylo

HERE = os.path.dirname(os.path.abspath(__file__))
TREE = os.path.join(HERE, '..', '..', 'data', 'iq', 'primates16.treefile')

# ---------------- Part A: SKILL.md recipe verbatim ("Label tips, and show support with its measure named") ----
tree = Phylo.read(TREE, 'newick')
tree.ladderize()

def tip_only(clade):
    return clade.name if clade.is_terminal() else ''

def support_label(clade):
    # the measure MUST be stated in the legend/caption; here values are bootstrap percentages
    if not clade.is_terminal() and clade.confidence is not None:
        return f'{clade.confidence:.0f}'
    return ''

fig, ax = plt.subplots(figsize=(12, 10))
Phylo.draw(tree, axes=ax, do_show=False, label_func=tip_only, branch_labels=support_label)
ax.set_title('Bootstrap support shown at internal nodes')
fig.savefig(os.path.join(HERE, 'A_supported_tree.svg'), bbox_inches='tight')
fig.savefig(os.path.join(HERE, 'A_supported_tree_view.png'), bbox_inches='tight', dpi=80)
internal = [c for c in tree.get_nonterminals()]
print('[A] internal clades:', len(internal))
print('[A] internal clades with .confidence set:', sum(c.confidence is not None for c in internal))
print('[A] internal clades whose .name holds the IQ-TREE label:', [c.name for c in internal if c.name][:6], '...')
branch_texts = [t.get_text() for t in ax.texts if t.get_text().strip() and not t.get_text().strip()[0].isalpha()]
print('[A] support labels actually drawn:', branch_texts)
print('[A] x-axis label:', repr(ax.get_xlabel()), '| rooted flag from file:', tree.rooted)
plt.close(fig)

# Also: SKILL.md drawing recipe with default label_func (what a quick look gives)
tree_d = Phylo.read(TREE, 'newick')
fig, ax = plt.subplots(figsize=(10, 8))
Phylo.draw(tree_d, axes=ax, do_show=False)
print('[A2] default label_func draws internal-node texts:', [t.get_text().strip() for t in ax.texts if '/' in t.get_text()][:5])
fig.savefig(os.path.join(HERE, 'A2_default_view.png'), bbox_inches='tight', dpi=80)
plt.close(fig)

# ---------------- Part B: adapted, following the Skill's doctrine (measure named, root declared, scale kept) ----
tree = Phylo.read(TREE, 'newick')
tree.root_with_outgroup('Microcebus_murinus', 'Otolemur_garnettii')   # rooting belongs to tree-manipulation; declared in caption
tree.ladderize()
sh_uf = {}
for c in tree.get_nonterminals():
    m = re.fullmatch(r'([\d.]+)/([\d.]+)', c.name or '')
    if m:
        sh_uf[c] = (float(m.group(1)), float(m.group(2)))
        c.name = None            # stop the label being drawn as a taxon name

def dual_label(clade):
    if clade in sh_uf:
        sh, uf = sh_uf[clade]
        star = '' if (sh >= 80 and uf >= 95) else ' *'
        return f'{sh:g}/{uf:g}{star}'
    return ''

def tip_label(clade):
    return clade.name.replace('_', ' ') if clade.is_terminal() else ''

n_tips = len(tree.get_terminals())
fig, ax = plt.subplots(figsize=(8, max(5, n_tips * 0.35)))
Phylo.draw(tree, axes=ax, do_show=False, label_func=tip_label, branch_labels=dual_label)
ax.set_xlabel('substitutions per site')
ax.set_ylabel('')
ax.set_yticks([])
for s in ('top', 'right', 'left'):
    ax.spines[s].set_visible(False)
ax.set_title('ML phylogram (IQ-TREE 2.4.0, HKY+F+G4); node labels = SH-aLRT (%) / UFBoot (%)', fontsize=10)
caption = ('Rooted on Strepsirrhini (Microcebus, Otolemur) as outgroup. Tips ladderized for legibility; ordering carries no '
           'phylogenetic meaning. * = fails the joint rule SH-aLRT >= 80 and UFBoot >= 95.')
fig.text(0.01, -0.02, caption, fontsize=8, wrap=True)
for ext in ('pdf', 'svg'):
    fig.savefig(os.path.join(HERE, f'B_primates16_support.{ext}'), bbox_inches='tight')
fig.savefig(os.path.join(HERE, 'B_primates16_support_view.png'), bbox_inches='tight', dpi=110)
plt.close(fig)
print('[B] dual labels drawn:', len(sh_uf), 'nodes; failing joint rule:',
      [f'{a:g}/{b:g}' for a, b in sh_uf.values() if not (a >= 80 and b >= 95)])

# Truth check: RF distance ML tree vs simulated tree (auditor verification)
import dendropy
tns = dendropy.TaxonNamespace()
t1 = dendropy.Tree.get(path=TREE, schema='newick', taxon_namespace=tns, preserve_underscores=True)
t2 = dendropy.Tree.get(path=os.path.join(HERE, '..', '..', 'data', 'primates16_true.nwk'), schema='newick',
                       taxon_namespace=tns, preserve_underscores=True)
from dendropy.calculate import treecompare
print('[check] unrooted RF(ML, true) =', treecompare.symmetric_difference(t1, t2, is_bipartitions_updated=False))
