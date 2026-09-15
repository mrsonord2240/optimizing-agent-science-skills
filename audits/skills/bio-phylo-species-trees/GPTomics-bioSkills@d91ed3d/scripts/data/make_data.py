"""SYNTHETIC data generator for the bio-phylo-species-trees audit (2026-09-15).

Everything written here is simulated; nothing is real sequence data.
Gene trees: DendroPy 5.0.13 multispecies-coalescent simulation (contained_coalescent_tree) inside a known species
tree given in coalescent units (pop_size = 1). Per-locus alignments: IQ-TREE 2.4.0 AliSim. True trees are written next
to the data so every species-tree estimate can be compared to truth by RF distance.

usage: python make_data.py OUTDIR set [set ...]
sets:
  rad    10-species rapid radiation (internodes 0.15-0.55 CU), 150 loci x 500 bp          (Input 1)
  az     6-taxon anomaly-zone tree (two successive 0.03-CU internodes), 400 loci x 400 bp  (Input 2)
  short  same 10-species radiation, 150 loci x 120 bp, ~25% of loci missing 1-2 taxa        (Input 3)
  intro  8 species, symmetric ILS at one branch + 30% of loci from a C->(D,E) introgression
         history, 200 loci x 500 bp                                                         (Input 4)
  fam    8 species, 150 multi-copy gene families (duplication above the root, copy 2 retained
         in the A-E clade, 10% random gene loss), gene names Sp_X_1 / Sp_X_2, 500 bp        (Input 5)
  az2k   supplementary: deeper anomaly zone (two successive 0.01-CU internodes), 2000 loci x 200 bp,
         used to stress-test the Skill's claim that concatenation converges on the wrong tree     (Input 2)
"""
import os
import random
import subprocess
import sys

import dendropy
from dendropy.simulate import treesim

IQTREE = r"F:\OpenScience\audit-envs\molecular-phylogenetics-analyst\tools\bin\iqtree2.exe"

RAD = ("((((((S01:1.0,S02:1.0):0.2,S03:1.2):0.15,(S04:0.8,S05:0.8):0.55):0.3,"
       "((S06:0.9,S07:0.9):0.4,S08:1.3):0.35):1.0,S09:2.65):1.5,S10:4.15);")
AZ = "(((((Sp_A:1.0,Sp_B:1.0):0.03,Sp_C:1.03):0.03,Sp_D:1.06):2.0,Sp_E:3.06):2.0,Sp_O:5.06);"
AZ_DEEP = "(((((Sp_A:1.0,Sp_B:1.0):0.01,Sp_C:1.01):0.01,Sp_D:1.02):2.0,Sp_E:3.02):2.0,Sp_O:5.02);"
INTRO_SP = ("(((((Sp_A:0.5,Sp_B:0.5):0.25,Sp_C:0.75):1.0,(Sp_D:0.5,Sp_E:0.5):1.25):1.0,"
            "(Sp_F:1.0,Sp_G:1.0):1.75):1.25,Sp_H:4.0);")
INTRO_ALT = ("((((Sp_A:0.5,Sp_B:0.5):1.25,(Sp_C:0.6,(Sp_D:0.5,Sp_E:0.5):0.1):1.15):1.0,"
             "(Sp_F:1.0,Sp_G:1.0):1.75):1.25,Sp_H:4.0);")


def write(path, text):
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)


def alisim(prefix, model, tree_file, length, seed):
    cmd = [IQTREE, "--alisim", prefix, "-m", model, "-t", tree_file, "--length", str(length),
           "--seed", str(seed), "-af", "fasta", "-redo"]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(r.stdout[-2000:] + r.stderr[-2000:])
    for ext in (".log",):
        if os.path.exists(tree_file + ext):
            os.remove(tree_file + ext)


class MSC:
    def __init__(self, newick):
        self.sp = dendropy.Tree.get(data=newick, schema="newick", preserve_underscores=True)
        self.gtns = dendropy.TaxonNamespace([t.label for t in self.sp.taxon_namespace])
        sp = self.sp
        self.tmap = dendropy.TaxonNamespaceMapping(
            domain_taxon_namespace=self.gtns, range_taxon_namespace=sp.taxon_namespace,
            mapping_fn=lambda gt: sp.taxon_namespace.get_taxon(label=gt.label))

    def gene_tree(self, rng):
        return treesim.contained_coalescent_tree(containing_tree=self.sp, gene_to_containing_taxon_map=self.tmap,
                                                 default_pop_size=1.0, rng=rng)


def scale(tree, s):
    for e in tree.postorder_edge_iter():
        if e.length is not None:
            e.length *= s


def nwk(tree):
    return tree.as_string(schema="newick", suppress_rooting=True).strip().replace("'", "")


def read_fasta(path):
    seqs, name = {}, None
    for line in open(path, encoding="utf-8"):
        line = line.strip()
        if line.startswith(">"):
            name = line[1:].split()[0]
            seqs[name] = []
        elif name:
            seqs[name].append(line)
    return {k: "".join(v) for k, v in seqs.items()}


def write_fasta(path, seqs):
    write(path, "".join(f">{k}\n{v}\n" for k, v in seqs.items()))


def simulate_loci(out, species_nwk, n_loci, length, seed, alt_nwk=None, alt_frac=0.0, missing_frac=0.0):
    rng = random.Random(seed)
    msc = MSC(species_nwk)
    alt = MSC(alt_nwk) if alt_nwk else None
    loci = os.path.join(out, "loci")
    os.makedirs(loci, exist_ok=True)
    write(os.path.join(out, "species_true.nwk"), species_nwk + "\n")
    true_gts, origin, concat = [], [], {}
    taxa = sorted(t.label for t in msc.sp.taxon_namespace)
    for i in range(1, n_loci + 1):
        use_alt = alt is not None and rng.random() < alt_frac
        gt = (alt if use_alt else msc).gene_tree(rng)
        true_gts.append(nwk(gt))
        origin.append("introgressed" if use_alt else "species")
        scale(gt, rng.uniform(0.03, 0.06))  # substitutions per coalescent unit for this locus
        tf = os.path.join(loci, f"L{i:03d}_true.nwk")
        write(tf, nwk(gt) + "\n")
        alpha = rng.uniform(0.5, 1.2)
        alisim(os.path.join(loci, f"L{i:03d}"), f"HKY{{3.0}}+F{{0.3,0.2,0.2,0.3}}+G4{{{alpha:.2f}}}", tf, length,
               seed * 10 + i)
        os.remove(tf)
        fa = os.path.join(loci, f"L{i:03d}.fa")
        seqs = read_fasta(fa)
        if missing_frac and rng.random() < missing_frac:
            for t in rng.sample(taxa, rng.choice([1, 2])):
                seqs.pop(t, None)
            write_fasta(fa, seqs)
        for t in taxa:
            concat.setdefault(t, []).append(seqs.get(t, "-" * length))
    write(os.path.join(out, "true_gene_trees.nwk"), "\n".join(true_gts) + "\n")
    write(os.path.join(out, "locus_origin.txt"), "\n".join(origin) + "\n")
    write_fasta(os.path.join(out, "concat.fasta"), {t: "".join(v) for t, v in concat.items()})


def height(tree):
    return max(lf.distance_from_root() for lf in tree.leaf_node_iter())


def make_fam(out, n=150, length=500, seed=77):
    rng = random.Random(seed)
    msc = MSC(INTRO_SP)
    clade2 = ["Sp_A", "Sp_B", "Sp_C", "Sp_D", "Sp_E"]
    fams = os.path.join(out, "loci")
    os.makedirs(fams, exist_ok=True)
    write(os.path.join(out, "species_true.nwk"), INTRO_SP + "\n")
    mapping, true_fams = set(), []
    for i in range(1, n + 1):
        g1 = msc.gene_tree(rng)
        g2 = msc.gene_tree(rng)
        g2.prune_taxa_with_labels([t for t in ["Sp_F", "Sp_G", "Sp_H"]])
        for lf in g1.leaf_node_iter():
            lf.taxon = dendropy.Taxon(label=lf.taxon.label + "_1")
        for lf in g2.leaf_node_iter():
            lf.taxon = dendropy.Taxon(label=lf.taxon.label + "_2")
        h1, h2 = height(g1), height(g2)
        hd = max(h1, h2) + 0.5
        body1 = nwk(g1).rstrip(";")
        body2 = nwk(g2).rstrip(";")
        fam = dendropy.Tree.get(data=f"({body1}:{hd - h1:.6f},{body2}:{hd - h2:.6f});", schema="newick",
                                preserve_underscores=True)
        leaves = [lf.taxon.label for lf in fam.leaf_node_iter()]
        lost = [lb for lb in leaves if rng.random() < 0.10]
        if len(leaves) - len(lost) >= 6 and lost:
            fam.prune_taxa_with_labels(lost)
        scale(fam, rng.uniform(0.03, 0.06))
        true_fams.append(nwk(fam))
        for lf in fam.leaf_node_iter():
            mapping.add((lf.taxon.label, lf.taxon.label.rsplit("_", 1)[0]))
        tf = os.path.join(fams, f"F{i:03d}_true.nwk")
        write(tf, nwk(fam) + "\n")
        alisim(os.path.join(fams, f"F{i:03d}"), "HKY{3.0}+F{0.3,0.2,0.2,0.3}+G4{0.8}", tf, length, seed * 10 + i)
        os.remove(tf)
    write(os.path.join(out, "true_family_trees.nwk"), "\n".join(true_fams) + "\n")
    write(os.path.join(out, "gene2species.txt"), "".join(f"{g}\t{s}\n" for g, s in sorted(mapping)))


if __name__ == "__main__":
    base = sys.argv[1]
    for s in sys.argv[2:]:
        d = os.path.join(base, s)
        os.makedirs(d, exist_ok=True)
        if s == "rad":
            simulate_loci(d, RAD, 150, 500, 11)
        elif s == "az":
            simulate_loci(d, AZ, 400, 400, 22)
        elif s == "short":
            simulate_loci(d, RAD, 150, 120, 33, missing_frac=0.25)
        elif s == "intro":
            simulate_loci(d, INTRO_SP, 200, 500, 44, alt_nwk=INTRO_ALT, alt_frac=0.30)
            write(os.path.join(d, "introgression_alt_tree.nwk"), INTRO_ALT + "\n")
        elif s == "fam":
            make_fam(d)
        elif s == "az2k":
            # supplementary stress test of the Skill's concatenation claim: deeper anomaly zone, many short loci
            simulate_loci(d, AZ_DEEP, 2000, 200, 55)
        print("made", s, flush=True)
