"""Input 2 (Variant A): split IQ-TREE 'SH-aLRT/UFBoot' labels. SYNTHETIC data (AliSim from data/true10.nwk).
Follows SKILL.md: inspect .confidence vs .name in Bio.Phylo; know what wrote the file."""
import csv
import os
from Bio import Phylo
import dendropy

D = os.path.join(os.path.dirname(__file__), "..", "..", "data")
OUT = os.path.dirname(os.path.abspath(__file__))
tf = os.path.join(D, "iq10.treefile")

tree = Phylo.read(tf, 'newick')
print("Bio.Phylo inner (confidence, name):", [(c.confidence, c.name) for c in tree.get_nonterminals()])

rows = []
for c in tree.get_nonterminals():
    lab = c.name if c.name is not None else (None if c.confidence is None else str(c.confidence))
    if lab is None:
        continue
    if "/" not in lab:
        raise ValueError(f"expected SH-aLRT/UFBoot, got {lab!r}")
    sh, uf = (float(x) for x in lab.split("/"))
    assert 0 <= sh <= 100 and 0 <= uf <= 100
    tips = sorted(t.name for t in c.get_terminals())
    rows.append((sh, uf, "STRONG" if sh >= 80 and uf >= 95 else "weak", ",".join(tips)))
with open(os.path.join(OUT, "iq10_support.tsv"), "w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh, delimiter="\t")
    w.writerow(["SH_aLRT", "UFBoot", "joint_80_95", "clade"])
    w.writerows(rows)
for r in rows:
    print(f"{r[0]:>6} {r[1]:>5}  {r[2]:<6} {r[3]}")

# write back a typed copy: phyloXML with two <confidence> elements
from Bio.Phylo.PhyloXML import Confidence, Phylogeny
px = Phylogeny.from_tree(tree)
for c in px.get_nonterminals():
    if c.name and "/" in c.name:
        sh, uf = (float(x) for x in c.name.split("/"))
        c.confidences = [Confidence(sh, "SH-aLRT"), Confidence(uf, "UFBoot")]
        c.name = None
Phylo.write(px, os.path.join(OUT, "iq10_typed.xml"), 'phyloxml')
back = Phylo.read(os.path.join(OUT, "iq10_typed.xml"), 'phyloxml')
print("phyloXML round trip confidences:", [[(x.type, x.value) for x in c.confidences] for c in back.get_nonterminals()][:3])

# truth check: RF distance to simulated tree (unrooted)
tns = dendropy.TaxonNamespace()
t_true = dendropy.Tree.get(path=os.path.join(D, "true10.nwk"), schema="newick", taxon_namespace=tns)
t_ml = dendropy.Tree.get(path=tf, schema="newick", taxon_namespace=tns)
from dendropy.calculate import treecompare
print("RF(ML, true) =", treecompare.symmetric_difference(t_true, t_ml))
# how DendroPy treats the dual label by default
print("DendroPy inner labels:", [n.label for n in t_ml.internal_nodes()][:4])
