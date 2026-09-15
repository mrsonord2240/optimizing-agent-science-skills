"""Input 3 (Edge): tip names with spaces, quotes, commas, parentheses and non-ASCII; join to metadata.
Follows SKILL.md 'Whitespace, Underscore, or Non-ASCII Taxon Names': sanitize to [A-Za-z0-9_.], single-quote when
needed, round-trip-test labels against the metadata table before any join. SYNTHETIC data."""
import csv
import os
import re
import unicodedata
from io import StringIO
from Bio import Phylo
import dendropy
from ete3 import Tree as ETree

D = os.path.join(os.path.dirname(__file__), "..", "..", "data")
OUT = os.path.dirname(os.path.abspath(__file__))
src = os.path.join(D, "names_odd.nwk")
meta = list(csv.DictReader(open(os.path.join(D, "names_meta.tsv"), encoding="utf-8"), delimiter="\t"))
mkeys = [r["taxon"] for r in meta]

# attempt 1 passed the path (log: odd_names_attempt1_path_open.log) -> Windows cp1252 decode garbled the accented
# name; attempt 2 opens the file explicitly as UTF-8 for every parser.
bt = Phylo.read(open(src, encoding="utf-8"), "newick")
bnames = [t.name for t in bt.get_terminals()]
print("Bio.Phylo tips:", bnames)
print("Bio.Phylo inner confidences:", [c.confidence for c in bt.get_nonterminals()])
# attempt 2 wrote to a path: Windows cp1252 encoded the file (UnicodeDecodeError 0xe8 on UTF-8 re-read);
# attempt 3 writes through an explicit UTF-8 handle.
with open(os.path.join(OUT, "biophylo_rt.nwk"), "w", encoding="utf-8") as fh:
    Phylo.write(bt, fh, "newick")
print("Bio.Phylo written:", open(os.path.join(OUT, "biophylo_rt.nwk"), encoding="utf-8").read().strip())
bt2 = Phylo.read(open(os.path.join(OUT, "biophylo_rt.nwk"), encoding="utf-8"), "newick")
print("Bio.Phylo round-trip names identical:", [t.name for t in bt2.get_terminals()] == bnames)

dt = dendropy.Tree.get(file=open(src, encoding="utf-8"), schema="newick")
dnames = [n.taxon.label for n in dt.leaf_node_iter()]
print("DendroPy tips (default):", dnames)
dtp = dendropy.Tree.get(file=open(src, encoding="utf-8"), schema="newick", preserve_underscores=True)
print("DendroPy tips (preserve_underscores=True):", [n.taxon.label for n in dtp.leaf_node_iter()])
with open(os.path.join(OUT, "dendropy_rt.nwk"), "w", encoding="utf-8") as fh:
    dt.write(file=fh, schema="newick")
print("DendroPy written:", open(os.path.join(OUT, "dendropy_rt.nwk"), encoding="utf-8").read().strip())

try:
    et = ETree(src, format=0, quoted_node_names=True)
    print("ete3 tips (quoted_node_names=True):", et.get_leaf_names())
except Exception as e:
    print("ete3 raised:", type(e).__name__, str(e)[:150])
try:
    et = ETree(src, format=0)
    print("ete3 tips (default):", et.get_leaf_names())
except Exception as e:
    print("ete3 default raised:", type(e).__name__, str(e)[:150])

# naive join
for label, names in (("Bio.Phylo", bnames), ("DendroPy", dnames)):
    hit = sum(n in mkeys for n in names)
    print(f"naive exact join {label}: {hit}/{len(names)} matched; unmatched = {[n for n in names if n not in mkeys]}")

# sanitize per the Skill: [A-Za-z0-9_.], keep a mapping table, check collisions, then join via the mapping
def sanitize(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    s = re.sub(r"[^A-Za-z0-9_.]+", "_", s).strip("_")
    return s
key = lambda s: sanitize(s).lower()
mapping = {n: sanitize(n) for n in bnames}
assert len(set(mapping.values())) == len(mapping), "sanitization collision"
mindex = {key(k): k for k in mkeys}
joined = {n: mindex.get(key(n)) for n in bnames}
print("sanitized join:", sum(v is not None for v in joined.values()), "/", len(bnames))
for n in bnames:
    print(f"  {n!r:<42} -> {mapping[n]:<32} meta: {joined[n]!r}")
for c in bt.get_terminals():
    c.name = mapping[c.name]
Phylo.write(bt, os.path.join(OUT, "sanitized.nwk"), "newick")
with open(os.path.join(OUT, "label_map.tsv"), "w", encoding="utf-8", newline="") as fh:
    w = csv.writer(fh, delimiter="\t")
    w.writerow(["original_label", "sanitized_label", "metadata_taxon"])
    for n in bnames:
        w.writerow([n, mapping[n], joined[n]])
rt = Phylo.read(os.path.join(OUT, "sanitized.nwk"), "newick")
print("sanitized round trip labels match mapping:", sorted(t.name for t in rt.get_terminals()) == sorted(mapping.values()))
print("sanitized.nwk:", open(os.path.join(OUT, "sanitized.nwk")).read().strip())
