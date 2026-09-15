"""Input 9 data (SYNTHETIC): in 30 of the 150 rad gene trees rename S03 -> S03_b (a sample-name variant that a real
merged dataset carries), and write the species map a user would need."""
import re
src = r"F:/OpenScience/audits/bio-phylo-species-trees/runs_v2/in1/gene_trees.nwk"
lines = open(src, encoding="utf-8").read().splitlines()
out = []
for i, l in enumerate(lines):
    out.append(re.sub(r"\bS03\b", "S03_b", l) if i % 5 == 0 else l)
open("gene_trees_mixed.nwk", "w", encoding="utf-8", newline="\n").write("\n".join(out) + "\n")
names = sorted(set(re.findall(r"(S\d\d(?:_b)?)", "\n".join(out))))
open("name2species.txt", "w", encoding="utf-8", newline="\n").write("".join(f"{n}\t{n[:3]}\n" for n in names))
print("trees with S03_b:", sum("S03_b" in l for l in out), "of", len(out), "| leaf names:", names)
