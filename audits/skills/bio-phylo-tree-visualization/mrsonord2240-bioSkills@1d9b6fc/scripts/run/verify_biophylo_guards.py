from io import StringIO
from pathlib import Path
import re

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from Bio import Phylo

out_dir = Path("/mnt/openscience/audits/bio-phylo-tree-visualization/run")
tree = Phylo.read("/mnt/openscience/audits/bio-phylo-tree-visualization/data/tree.nwk", "newick")
tree.root_with_outgroup({"name": "OutA"}, {"name": "OutB"})
intended = {"Homo_sapiens", "Pan_troglodytes", "Gorilla_gorilla", "Pongo_abelii"}
mrca = tree.common_ancestor({"name": "Homo_sapiens"}, {"name": "Pongo_abelii"})
got = {tip.name for tip in mrca.get_terminals()}
assert got == intended, (got, intended)
mrca.color = "red"
fig, ax = plt.subplots(figsize=(8, 4))
Phylo.draw(tree, axes=ax, do_show=False)
pdf = out_dir / "rooted_colored.pdf"
fig.savefig(pdf)
plt.close(fig)
assert pdf.stat().st_size > 1000

support_tree = Phylo.read(StringIO("((A:0.1,B:0.1)88/97:0.1,(C:0.1,D:0.1)72/90:0.1);"), "newick")
for clade in support_tree.get_nonterminals():
    if clade.confidence is None and clade.name and re.fullmatch(r"[\d.]+/[\d.]+", clade.name):
        clade.sh_alrt, clade.ufboot = (float(v) for v in clade.name.split("/"))
        clade.name = None
labels = [f"{c.sh_alrt:.0f}/{c.ufboot:.0f}" for c in support_tree.get_nonterminals() if getattr(c, "ufboot", None) is not None]
assert labels == ["88/97", "72/90"], labels

n_tips = 201
if n_tips > 200:
    try:
        raise ValueError(f"{n_tips} tips > 200: Bio.Phylo cannot draw legible labels")
    except ValueError as exc:
        assert "cannot draw legible labels" in str(exc)
print(f"ASSERT mrca_tips={len(got)} support_labels={labels} rooted_pdf_bytes={pdf.stat().st_size} tip_cap_rejected=True")
