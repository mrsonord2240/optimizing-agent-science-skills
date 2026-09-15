# Synthetic: copy the 40 simulated ILS loci, dropping 1-2 taxa from every third locus
# (realistic phylogenomic missing data) to test gCF/sCF with incomplete gene trees.
import os, random
from Bio import SeqIO
random.seed(7)
src = r"F:/OpenScience/audits/bio-phylo-modern-tree-inference/data/ils_loci"
dst = r"F:/OpenScience/audits/bio-phylo-modern-tree-inference/runs_v2/in9/loci_missing"
os.makedirs(dst, exist_ok=True)
dropped = {}
for i, fn in enumerate(sorted(os.listdir(src))):
    recs = list(SeqIO.parse(os.path.join(src, fn), "fasta"))
    if i % 3 == 0:
        k = 1 + (i % 2)
        drop = set(random.sample([r.id for r in recs], k))
        recs = [r for r in recs if r.id not in drop]
        dropped[fn] = sorted(drop)
    SeqIO.write(recs, os.path.join(dst, fn), "fasta")
for k, v in dropped.items():
    print(k, v)
print("loci with missing taxa:", len(dropped))
