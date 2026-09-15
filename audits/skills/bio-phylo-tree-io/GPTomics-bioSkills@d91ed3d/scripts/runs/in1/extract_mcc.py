"""Input 1 (Canonical): BEAST MCC -> side table of posteriors/HPDs, then plain Newick. Follows SKILL.md
'Preserve BEAST/MrBayes Annotations Before Down-Converting'. Data are SYNTHETIC (data/mcc6.tree)."""
import csv
import os
import sys
import dendropy
from Bio import Phylo

D = os.path.join(os.path.dirname(__file__), "..", "..", "data")
MCC = os.path.join(D, "mcc6.tree")
OUT = os.path.dirname(os.path.abspath(__file__))

# --- 1. Skill snippet, as written (paths adapted) ---
tree = dendropy.Tree.get(path=MCC, schema='nexus', extract_comment_metadata=True)
rows = []
for node in tree:
    if node.annotations.get_value('posterior') is not None:
        post = node.annotations.get_value('posterior')
        hpd = node.annotations.get_value('height_95%_HPD')
        print("SKILL-SNIPPET node:", type(post).__name__, repr(post), "| hpd:", type(hpd).__name__, repr(hpd))
        clade = "|".join(sorted(l.taxon.label.replace(" ", "_") for l in node.leaf_iter()))
        if node is tree.seed_node:
            clade = "ROOT"
        rows.append((clade, post, hpd))
print("tree.is_rooted =", tree.is_rooted)

# --- 2. side table (typed) ---
side = os.path.join(OUT, "mcc6_node_annotations.tsv")
with open(side, "w", newline="", encoding="utf-8") as fh:
    wr = csv.writer(fh, delimiter="\t")
    wr.writerow(["clade", "posterior", "height", "height_95_HPD_lower", "height_95_HPD_upper", "rate"])
    for node in tree.postorder_node_iter():
        if node.is_leaf():
            continue
        g = node.annotations.get_value
        hpd = g('height_95%_HPD')
        lo, hi = (float(hpd[0]), float(hpd[1])) if isinstance(hpd, (list, tuple)) else (None, None)
        clade = "ROOT" if node is tree.seed_node else "|".join(sorted(l.taxon.label.replace(" ", "_") for l in node.leaf_iter()))
        wr.writerow([clade, float(g('posterior')), float(g('height')), lo, hi, g('rate') and float(g('rate'))])
print("wrote", side)

# --- 3. verify side table vs truth ---
truth = {r["clade"]: r for r in csv.DictReader(open(os.path.join(D, "mcc6_truth.tsv"), encoding="utf-8"), delimiter="\t")}
got = {r["clade"]: r for r in csv.DictReader(open(side, encoding="utf-8"), delimiter="\t")}
bad = 0
for c, t in truth.items():
    g = got.get(c)
    ok = g is not None and all(abs(float(g[a]) - float(t[b])) < 1e-9 for a, b in
                               (("posterior", "posterior"), ("height", "height"),
                                ("height_95_HPD_lower", "hpd_lo"), ("height_95_HPD_upper", "hpd_hi")))
    bad += not ok
    print(f"TRUTH-CHECK {c[:40]:<40} {'OK' if ok else 'MISMATCH'}")
print("truth mismatches:", bad)

# --- 4. stripped topology, exactly as the Skill writes it ---
nwk = os.path.join(OUT, "topology.nwk")
tree.write(path=nwk, schema='newick', suppress_annotations=True)
print("topology.nwk:", open(nwk).read().strip())
nwk2 = os.path.join(OUT, "topology_norooting.nwk")
tree.write(path=nwk2, schema='newick', suppress_annotations=True, suppress_rooting=True)
print("topology_norooting.nwk:", open(nwk2).read().strip())

# --- 5. Skill claims about Bio.Phylo ---
bt = Phylo.read(MCC, 'nexus')
inner = [c for c in bt.get_nonterminals()]
print("Bio.Phylo: n tips", bt.count_terminals(), "tip names", [t.name for t in bt.get_terminals()])
print("Bio.Phylo: root.comment =", repr(inner[0].comment)[:120])
print("Bio.Phylo: confidences =", [c.confidence for c in inner], "rooted =", bt.rooted)
Phylo.convert(MCC, 'nexus', os.path.join(OUT, "phylo_convert.nwk"), 'newick')
s = open(os.path.join(OUT, "phylo_convert.nwk")).read().strip()
print("Phylo.convert newick contains '[&':", "[&" in s, "| HPD present:", "HPD" in s)
print("Phylo.convert newick:", s[:200])
Phylo.convert(MCC, 'nexus', os.path.join(OUT, "phylo_convert.nex"), 'nexus')
s = open(os.path.join(OUT, "phylo_convert.nex")).read()
print("Phylo.convert nexus->nexus keeps HPD:", "HPD" in s)
