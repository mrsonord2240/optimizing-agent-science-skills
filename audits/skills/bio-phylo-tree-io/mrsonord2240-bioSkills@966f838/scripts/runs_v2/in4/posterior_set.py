"""Input 4 (Variant B): MrBayes posterior .t files and .con.tre. SYNTHETIC (MrBayes 3.2.7a, 20k gen on AliSim data).
Follows SKILL.md: Phylo.read for one tree, Phylo.parse for many; DendroPy TreeList; check object length."""
import os
from Bio import Phylo
import dendropy

D = os.path.join(os.path.dirname(__file__), "..", "..", "data")
runs = [os.path.join(D, f"mb10.run{i}.t") for i in (1, 2)]

# Skill claim: Phylo.read raises on a multi-tree file
try:
    Phylo.read(runs[0], 'nexus')
    print("Phylo.read on .t: NO exception")
except Exception as e:
    print("Phylo.read on .t raised:", type(e).__name__, str(e)[:100])
try:
    Phylo.read(os.path.join(os.path.dirname(__file__), "empty.nwk"), 'newick')
except Exception as e:
    print("Phylo.read on empty file raised:", type(e).__name__, str(e)[:100])

# Bio.Phylo parse
counts = []
for r in runs:
    ts = list(Phylo.parse(r, 'nexus'))
    counts.append(len(ts))
    print(os.path.basename(r), "Phylo.parse trees:", len(ts), "first tip names:", sorted(t.name for t in ts[0].get_terminals())[:3])

# DendroPy: both runs, shared namespace, 25% burn-in per run
tns = dendropy.TaxonNamespace()
post = dendropy.TreeList(taxon_namespace=tns)
for r in runs:
    tl = dendropy.TreeList.get(path=r, schema="nexus", taxon_namespace=tns)
    n = len(tl)
    burn = int(0.25 * n)
    post.extend(tl[burn:])
    print(os.path.basename(r), "DendroPy trees:", n, "burn-in dropped:", burn)
print("post-burn-in posterior sample:", len(post), "taxa:", len(tns))

# .con.tre: Bio.Phylo vs DendroPy on MrBayes FigTree-style comments
con = os.path.join(D, "mb10.con.tre")
try:
    ct = Phylo.read(con, 'nexus')
    print("Bio.Phylo con.tre: tips", ct.count_terminals(), "| inner confidences", [c.confidence for c in ct.get_nonterminals()][:4],
          "| comment sample", repr(ct.get_nonterminals()[1].comment)[:80])
except Exception as e:
    print("Bio.Phylo on con.tre raised:", type(e).__name__, str(e)[:160])
dt = dendropy.Tree.get(path=con, schema="nexus", extract_comment_metadata=True)
for nd in dt.internal_nodes():
    p = nd.annotations.get_value("prob")
    tips = sorted(l.taxon.label for l in nd.leaf_iter())
    if len(tips) < len(tns):
        print(f"clade prob={p} ({type(p).__name__}) size={len(tips)} :: {', '.join(tips)}")
# consensus support check: the split frequencies from the sample vs con.tre prob
from collections import Counter
freq = Counter()
for t in post:
    t.encode_bipartitions()  # auditor fix: first draft called TreeList.encode_bipartitions (does not exist)
    for b in t.bipartition_encoding:
        freq[b.split_bitmask] += 1
print("sample split frequency range (non-trivial):",
      sorted(round(v / len(post), 3) for k, v in freq.items() if bin(k).count('1') not in (1, len(tns) - 1))[:6])
