"""Input 6 (Scope Boundary): user wants runA.t + runB.t concatenated, a consensus with posteriors, rooted on Mus, and a
figure. In scope here: a TRANSLATE-aware merge and label verification. Consensus/rooting/figure are routed to sibling
Skills. SYNTHETIC data: both files hold the same topology; runB numbers taxa in a different TRANSLATE order."""
import os
import re
import dendropy
from Bio import Phylo

D = os.path.join(os.path.dirname(__file__), "..", "..", "data")
OUT = os.path.dirname(os.path.abspath(__file__))
A, B = os.path.join(D, "runA.t"), os.path.join(D, "runB.t")


def translate(path):
    txt = open(path, encoding="utf-8").read()
    block = re.search(r"translate\s+(.*?);", txt, re.S | re.I).group(1)
    return dict(re.findall(r"(\d+)\s+([^,\s;]+)", block))


ta, tb = translate(A), translate(B)
print("runA translate:", ta)
print("runB translate:", tb)
print("TRANSLATE tables identical:", ta == tb)

# naive: what `cat`-style merging does -- runB tree lines under runA's translate table
txtA = open(A, encoding="utf-8").read().replace("end;", "")
treesB = [l for l in open(B, encoding="utf-8") if l.strip().startswith("tree ")]
naive = os.path.join(OUT, "naive_merged.t")
open(naive, "w", encoding="utf-8").write(txtA + "".join(treesB) + "end;\n")

tns = dendropy.TaxonNamespace()
nv = dendropy.TreeList.get(path=naive, schema="nexus", taxon_namespace=tns)
def splits(tl):
    out = []
    for t in tl:
        t.encode_bipartitions()
        out.append(frozenset(b.split_bitmask for b in t.bipartition_encoding if not b.is_trivial()))
    return out
ns = splits(nv)
print("naive merge: trees", len(nv), "| distinct topologies", len(set(ns)))
rtree = nv[len(nv) - 1]
print("naive merge, a runB tree as read:", rtree.as_string(schema="newick", suppress_edge_lengths=True).strip())

# translate-aware merge: read each file with its own table into one namespace
tns2 = dendropy.TaxonNamespace()
merged = dendropy.TreeList(taxon_namespace=tns2)
for p in (A, B):
    merged.extend(dendropy.TreeList.get(path=p, schema="nexus", taxon_namespace=tns2))
ms = splits(merged)
print("aware merge: trees", len(merged), "| distinct topologies", len(set(ms)), "| taxa", sorted(t.label for t in tns2))
labsA = {t.label for t in dendropy.TreeList.get(path=A, schema="nexus").taxon_namespace}
labsB = {t.label for t in dendropy.TreeList.get(path=B, schema="nexus").taxon_namespace}
print("tip-label sets equal across runs:", labsA == labsB)
print("rooting flags in merged trees (is_rooted):", {t.is_rooted for t in merged})
merged.write(path=os.path.join(OUT, "merged_AB.nex"), schema="nexus", translate_tree_taxa=True)
chk = list(Phylo.parse(os.path.join(OUT, "merged_AB.nex"), "nexus"))
print("merged_AB.nex re-read by Bio.Phylo:", len(chk), "trees; tips of last:", sorted(c.name for c in chk[-1].get_terminals()))
