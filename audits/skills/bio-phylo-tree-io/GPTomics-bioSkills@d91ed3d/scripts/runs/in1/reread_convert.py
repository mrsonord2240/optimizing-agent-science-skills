"""Input 1 follow-up: is the Newick written by Phylo.convert (nexus->newick) usable, and do annotations survive?"""
import os
from Bio import Phylo
import dendropy
H = os.path.dirname(os.path.abspath(__file__))
p = os.path.join(H, "phylo_convert.nwk")
raw = open(p, encoding="utf-8").read()
print("raw first 160 chars:", raw[:160])
print("count '[\\[&':", raw.count("[\\[&"), "| count '[&':", raw.count("[&"))
t = Phylo.read(p, "newick")
print("Bio.Phylo re-read root comment:", repr(t.root.comment)[:100])
print("Bio.Phylo re-read tip names:", [x.name for x in t.get_terminals()])
try:
    d = dendropy.Tree.get(path=p, schema="newick", extract_comment_metadata=True)
    ann = [(n.annotations.get_value("posterior"), n.annotations.get_value("height_95%_HPD")) for n in d.internal_nodes()]
    print("DendroPy re-read posterior/HPD:", ann)
    print("DendroPy tips:", [x.label for x in d.taxon_namespace])
except Exception as e:
    print("DendroPy re-read raised:", type(e).__name__, str(e)[:200])
