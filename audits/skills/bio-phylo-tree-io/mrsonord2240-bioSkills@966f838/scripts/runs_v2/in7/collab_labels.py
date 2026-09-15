"""Input 7 (Adversarial): user insists the internal numbers are bootstraps, wants them stored as bootstrap in phyloXML
and everything < 70 collapsed. Follows SKILL.md 'support value scales' and '.confidence vs .name'. SYNTHETIC data."""
import os
from Bio import Phylo
from Bio.Phylo.PhyloXML import Phylogeny, Confidence

D = os.path.join(os.path.dirname(__file__), "..", "..", "data")
OUT = os.path.dirname(os.path.abspath(__file__))
t = Phylo.read(os.path.join(D, "collab_post.nwk"), "newick")
inner = [c for c in t.get_nonterminals() if c.confidence is not None or c.name]
vals = [c.confidence for c in inner]
print("slot check (confidence, name):", [(c.confidence, c.name) for c in t.get_nonterminals()])
print("values:", vals, "| min", min(vals), "max", max(vals))
scale = "posterior-like [0,1]" if max(vals) <= 1.0 else "percentage [0,100]"
print("inferred scale:", scale)
print("clades that 'collapse < 70' would remove:", sum(v < 70 for v in vals), "of", len(vals))
print("clades below 0.95 if these are posteriors:", sum(v < 0.95 for v in vals), "of", len(vals))
print("clades below 0.70 if these are proportions of bootstrap replicates:", sum(v < 0.70 for v in vals), "of", len(vals))
# deliver phyloXML with provenance left explicit, no collapsing
px = Phylogeny.from_tree(t)
for c in px.get_nonterminals():
    if c.confidence is not None:
        v = c.confidence
        c.confidences = [Confidence(v, "unknown_0-1_scale_provenance_unconfirmed")]
Phylo.write(px, os.path.join(OUT, "collab_typed.xml"), "phyloxml")
back = Phylo.read(os.path.join(OUT, "collab_typed.xml"), "phyloxml")
print("phyloXML re-read:", [[(x.type, x.value) for x in c.confidences] for c in back.get_nonterminals() if c.confidences])
