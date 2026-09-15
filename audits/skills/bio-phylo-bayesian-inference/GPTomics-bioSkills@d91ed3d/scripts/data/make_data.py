"""Generate SYNTHETIC alignments with known truth for the bio-phylo-bayesian-inference audit (2026-09-15).

All data are simulated with IQ-TREE 2.4.0 AliSim from trees written here; nothing is real sequence data.
  d12   : 12 taxa x 1500 bp, GTR+G4 (alpha 0.5), moderate branch lengths (canonical / under-run / SS)
  star8 : 8 taxa x 2000 bp, JC-like HKY+G, one internal branch = 0.0 (true polytomy) and one = 0.002
  many60: 60 taxa x 800 bp, HKY+G, very short branches (true tree length ~0.9) for branch-length-prior inflation
Outputs FASTA + NEXUS (MrBayes) + true newick + truth.txt.
"""
import os, random, subprocess
import dendropy

HERE = os.path.dirname(os.path.abspath(__file__))
IQ = r"F:\OpenScience\audit-envs\molecular-phylogenetics-analyst\tools\bin\iqtree2.exe"


def alisim(prefix, tree, model, length, seed):
    tf = os.path.join(HERE, prefix + "_true.nwk")
    with open(tf, "w", encoding="utf-8") as f:
        f.write(tree.strip() + "\n")
    out = os.path.join(HERE, prefix)
    subprocess.run([IQ, "--alisim", out, "-t", tf, "-m", model, "--length", str(length),
                    "--seed", str(seed), "-af", "fasta", "-redo"], check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    fa = out + ".fa"
    seqs, name = {}, None
    for line in open(fa, encoding="utf-8"):
        line = line.strip()
        if line.startswith(">"):
            name = line[1:].split()[0]; seqs[name] = []
        elif line:
            seqs[name].append(line)
    seqs = {k: "".join(v) for k, v in seqs.items()}
    L = len(next(iter(seqs.values())))
    with open(out + ".nex", "w", encoding="utf-8") as f:
        f.write("#NEXUS\nbegin data;\n  dimensions ntax=%d nchar=%d;\n  format datatype=dna missing=? gap=-;\n  matrix\n" % (len(seqs), L))
        for k, v in seqs.items():
            f.write("  %-14s %s\n" % (k, v))
        f.write("  ;\nend;\n")
    return seqs


# d12: fixed topology with moderate internal branches
d12 = ("((((Taxon01:0.08,Taxon02:0.10):0.04,(Taxon03:0.07,Taxon04:0.12):0.03):0.05,"
       "((Taxon05:0.09,Taxon06:0.06):0.06,Taxon07:0.15):0.02):0.04,"
       "(((Taxon08:0.11,Taxon09:0.08):0.05,Taxon10:0.13):0.03,(Taxon11:0.10,Taxon12:0.09):0.07):0.04);")
alisim("d12", d12, "GTR{1.2,3.5,0.8,1.1,4.2}+F{0.3,0.2,0.2,0.3}+G4{0.5}", 1500, 101)

# star8: A..H; internal branch joining (A,B) to (C,D) is ~0 -> effective polytomy of AB, CD, EFGH
star8 = ("(((A:0.10,B:0.12):0.05,(C:0.11,D:0.09):0.05):0.0005,((E:0.10,F:0.12):0.06,(G:0.08,H:0.11):0.06):0.0);")
# unrooted: the two root edges merge into ONE internal edge ABCD|EFGH of length 0.0005 (~1 expected change in 2000 bp)
alisim("star8", star8, "HKY{2.0}+F{0.25,0.25,0.25,0.25}+G4{1.0}", 2000, 202)

# many60: birth-death shape, then all branch lengths drawn short (mean 0.008)
random.seed(303)
rng = random.Random(303)
t = dendropy.simulate.treesim.birth_death_tree(birth_rate=1.0, death_rate=0.0, num_extant_tips=60, rng=rng)
for i, leaf in enumerate(t.leaf_node_iter()):
    leaf.taxon.label = "S%02d" % (i + 1)
for e in t.postorder_edge_iter():
    e.length = rng.uniform(0.002, 0.014)
t.is_rooted = False
nwk = t.as_string(schema="newick", suppress_rooting=True).strip()
alisim("many60", nwk, "HKY{3.0}+F{0.25,0.25,0.25,0.25}+G4{0.8}", 800, 303)
tl = sum(e.length for e in t.postorder_edge_iter() if e.tail_node is not None)

with open(os.path.join(HERE, "truth.txt"), "w", encoding="utf-8") as f:
    f.write("SYNTHETIC data, IQ-TREE 2.4.0 AliSim\n")
    f.write("d12: true TL = %.3f\n" % sum(float(x) for x in __import__('re').findall(r":([0-9.]+)", d12)))
    f.write("star8: true unrooted tree ((A,B),(C,D)) | ((E,F),(G,H)); the central edge ABCD|EFGH = 0.0005 (near-polytomy); AB, CD, EF, GH splits are well supported (0.05-0.06)\n")
    f.write("many60: true TL = %.4f (60 taxa, %d edges)\n" % (tl, sum(1 for e in t.postorder_edge_iter() if e.tail_node is not None)))
print(open(os.path.join(HERE, "truth.txt"), encoding="utf-8").read())
