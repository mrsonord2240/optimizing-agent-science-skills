# Generated while following bio-phylo-modern-tree-inference (Input 1).
# Reads the IQ-TREE .treefile whose internal labels are "SH-aLRT/UFBoot" and applies the
# joint rule from the Skill: strong iff SH-aLRT >= 80 AND UFBoot >= 95.
import re
import sys
from Bio import Phylo

treefile = sys.argv[1] if len(sys.argv) > 1 else "run1.treefile"
tree = Phylo.read(treefile, "newick")

rows = []
for clade in tree.get_nonterminals():
    label = clade.name if clade.name else (str(clade.confidence) if clade.confidence is not None else None)
    if not label or "/" not in label:
        continue
    alrt, ufb = (float(x) for x in label.split("/")[:2])
    tips = sorted(t.name for t in clade.get_terminals())
    strong = alrt >= 80 and ufb >= 95
    rows.append((alrt, ufb, strong, tips))

print(f"{'SH-aLRT':>8} {'UFBoot':>7}  verdict   clade (as drawn on the unrooted ML tree)")
for alrt, ufb, strong, tips in sorted(rows, key=lambda r: len(r[3])):
    verdict = "STRONG " if strong else "weak   "
    print(f"{alrt:8.1f} {ufb:7.0f}  {verdict}  {','.join(tips)}")
n_strong = sum(r[2] for r in rows)
print(f"\n{n_strong}/{len(rows)} internal branches pass SH-aLRT>=80 AND UFBoot>=95")
