"""Input 5 (Stress): convert NHX, phyloXML and NeXML collaborator trees to Nexus, Newick and phyloXML; report exactly
what each conversion loses, with read-write-read round-trip diffs. SYNTHETIC data. Follows SKILL.md format tables."""
import os
import re
from Bio import Phylo
from Bio.Phylo.PhyloXML import Phylogeny, Confidence, Taxonomy
import dendropy
from ete3 import Tree as ETree

D = os.path.join(os.path.dirname(__file__), "..", "..", "data")
OUT = os.path.dirname(os.path.abspath(__file__))
P = lambda f: os.path.join(OUT, f)
report = []


def summarize_biophylo(path, fmt):
    t = Phylo.read(open(path, encoding="utf-8"), fmt)
    inner = t.get_nonterminals()
    nconf = sum(len(getattr(c, "confidences", []) or ([c.confidence] if c.confidence is not None else [])) for c in inner)
    ntax = sum(1 for c in t.get_terminals() if getattr(c, "taxonomies", None))
    colors = sum(1 for c in t.find_clades() if getattr(c, "color", None) is not None)
    return dict(tips=t.count_terminals(), confidences=nconf, taxonomy_tips=ntax, colored=colors, rooted=t.rooted)


# ---------- phyloXML source ----------
src = os.path.join(D, "phylo8.xml")
base = summarize_biophylo(src, "phyloxml")
print("phylo8.xml source:", base)
px = Phylo.read(src, "phyloxml")
px.root.clades[0].color = "red"          # to test "colors persist only in phyloXML"
Phylo.write(px, P("phylo8_colored.xml"), "phyloxml")
for fmt, ext in (("nexus", "nex"), ("newick", "nwk"), ("nexml", "nexml.xml"), ("phyloxml", "rt.xml")):
    out = P(f"from_phyloxml.{ext}")
    try:
        Phylo.convert(P("phylo8_colored.xml"), "phyloxml", out, fmt)
        s = summarize_biophylo(out, fmt)
        print(f"phyloXML -> {fmt}: {s}")
        report.append(("phyloXML", fmt, base, s))
    except Exception as e:
        print(f"phyloXML -> {fmt}: FAILED {type(e).__name__}: {str(e)[:150]}")
print("from_phyloxml.nwk:", open(P("from_phyloxml.nwk")).read().strip())
try:
    Phylo.convert(src, "phyloxml", P("from_phyloxml.cdao"), "cdao")
    print("phyloXML -> cdao: OK")
except Exception as e:
    print(f"phyloXML -> cdao: FAILED {type(e).__name__}: {str(e)[:150]}")

# ---------- NHX source ----------
nhx = os.path.join(D, "nhx8.nhx")
try:
    bt = Phylo.read(nhx, "newick")
    print("Bio.Phylo reads NHX as newick: tips", bt.count_terminals(), "| inner confidences", [c.confidence for c in bt.get_nonterminals()],
          "| tip comment", repr(bt.get_terminals()[0].comment))
except Exception as e:
    print("Bio.Phylo NHX read FAILED:", type(e).__name__, str(e)[:120])
et = ETree(nhx, format=0)
feat = {n.name: (getattr(n, "S", None), getattr(n, "B", None)) for n in et.traverse()}
print("ete3 NHX features S/B present:", sum(1 for v in feat.values() if v[0]), "species,", sum(1 for v in feat.values() if v[1]), "B tags")
# NHX -> phyloXML with typed taxonomy + bootstrap, via ete3 -> Bio.Phylo
bp = Phylo.read(nhx, "newick")
bpx = Phylogeny.from_tree(bp)
bpx.rooted = True
ete_inner = {tuple(sorted(n.get_leaf_names())): n for n in et.traverse() if not n.is_leaf()}
for c in bpx.find_clades():
    if c.is_terminal():
        sp = feat[c.name][0]
        c.taxonomies = [Taxonomy(scientific_name=sp.replace("_", " "))]
    else:
        key = tuple(sorted(x.name for x in c.get_terminals()))
        n = ete_inner.get(key)
        if n is not None and hasattr(n, "B"):
            c.confidences = [Confidence(float(n.B), "bootstrap")]
    c.comment = None
Phylo.write(bpx, P("from_nhx.xml"), "phyloxml")
print("NHX -> phyloXML (typed):", summarize_biophylo(P("from_nhx.xml"), "phyloxml"))
et.write(outfile=P("nhx_rt.nhx"), features=["S", "B", "D"], format=0)
print("ete3 NHX round trip identical:", open(P("nhx_rt.nhx")).read().strip() == open(nhx).read().strip())
Phylo.write(bp, P("from_nhx_biophylo.nwk"), "newick")
print("Bio.Phylo newick write of NHX tree keeps &&NHX:", "&&NHX" in open(P("from_nhx_biophylo.nwk")).read(),
      "| sample:", open(P("from_nhx_biophylo.nwk")).read()[:90])

# ---------- NeXML source ----------
nexml = os.path.join(D, "nex8.xml")
dn = dendropy.Tree.get(path=nexml, schema="nexml")
print("DendroPy NeXML annotations (bootstrap) on inner nodes:",
      [n.annotations.get_value("bootstrap") for n in dn.internal_nodes()])
try:
    bn = Phylo.read(nexml, "nexml")
    print("Bio.Phylo NeXML read: tips", bn.count_terminals(), "names", [t.name for t in bn.get_terminals()][:3],
          "| inner confidences", [c.confidence for c in bn.get_nonterminals()][:3])
except Exception as e:
    print("Bio.Phylo NeXML read FAILED:", type(e).__name__, str(e)[:150])
dn.write(path=P("from_nexml.nex"), schema="nexus")
dn.write(path=P("from_nexml.nwk"), schema="newick")
print("DendroPy NeXML -> nexus keeps bootstrap annotation:", "bootstrap" in open(P("from_nexml.nex")).read())
print("DendroPy NeXML -> newick:", open(P("from_nexml.nwk")).read().strip()[:160])
rt = dendropy.Tree.get(path=P("from_nexml.nex"), schema="nexus", extract_comment_metadata=True)
print("DendroPy nexus re-read bootstrap values:", [n.annotations.get_value("bootstrap") for n in rt.internal_nodes()])

# ---------- loss table ----------
print("\nLOSS TABLE (phyloXML source: 5 clades x 2 typed confidences = 10; 7 NCBI taxonomy tips; 1 colored clade)")
for s, fmt, b, a in report:
    lost = [k for k in ("confidences", "taxonomy_tips", "colored") if a[k] < b[k] + (1 if k == "colored" else 0)]
    print(f"  {s} -> {fmt:<8} confidences {a['confidences']:>2}/10  taxonomy {a['taxonomy_tips']}/7  colored {a['colored']}/1  rooted {a['rooted']}  LOST: {lost}")
