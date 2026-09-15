"""Input 1 (Canonical): fixed Skill's DendroPy snippet VERBATIM (paths only) on the SYNTHETIC hand-written MCC tree
mcc6.tree, plus the Skill's Phylo.convert warning checked. Auditor code is marked."""
import csv
from Bio import Phylo

import dendropy

tree = dendropy.Tree.get(path='../../data/mcc6.tree', schema='nexus', extract_comment_metadata=True)
rows = []                                                                 # auditor: collect for the truth check
for node in tree:
    if node.annotations.get_value('posterior') is not None:
        post = float(node.annotations.get_value('posterior'))   # DendroPy returns strings; cast
        hpd = [float(v) for v in node.annotations.get_value('height_95%_HPD')]   # raw BEAST key
        # persist post/hpd to a side table keyed by the clade before any conversion
        clade = 'ROOT' if node is tree.seed_node else '|'.join(sorted(l.taxon.label.replace(' ', '_') for l in node.leaf_iter()))
        rows.append((clade, post, hpd))
tree.write(path='topology.nwk', schema='newick', suppress_annotations=True, suppress_rooting=True)   # intentional, after extraction

# ---- auditor checks ----
print('typed rows:', rows[:2], '| n =', len(rows))
truth = {r['clade']: r for r in csv.DictReader(open('../../data/mcc6_truth.tsv', encoding='utf-8'), delimiter='\t')}
bad = [c for c, p, h in rows if c in truth and (abs(p - float(truth[c]['posterior'])) > 1e-9)]
print('clades matched to truth:', sum(c in truth for c, _, _ in rows), '| posterior mismatches:', bad)
print('topology.nwk:', open('topology.nwk').read().strip()[:120])
Phylo.convert('../../data/mcc6.tree', 'nexus', 'phylo_convert.nwk', 'newick')   # the Skill's WARNING line
raw = open('phylo_convert.nwk').read()
print("Phylo.convert Newick contains escaped '[\\[&':", raw.count('[\\[&'))
d = dendropy.Tree.get(path='phylo_convert.nwk', schema='newick', extract_comment_metadata=True)
print('DendroPy posteriors readable after Phylo.convert:', sum(n.annotations.get_value('posterior') is not None for n in d))
