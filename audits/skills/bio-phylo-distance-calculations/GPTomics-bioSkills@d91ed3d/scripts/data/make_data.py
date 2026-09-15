"""SYNTHETIC data generator for the bio-phylo-distance-calculations audit (2026-09-15).

Every file written here is simulated; nothing is real sequence data. Trees are hand-written or
simulated with DendroPy 5.0.13 (seeded); sequences are simulated with IQ-TREE 2.4.0 AliSim under
stated models and seeds, so the true unrooted topology of every alignment is known.

usage: python make_data.py [OUTDIR]      (default: directory of this script)

sets written
  barcode20   20 specimens, 658 bp, shallow (max root-to-tip ~0.06), HKY+G, mild rate variation
  deep12      12 taxa, 1500 bp, long terminal branches (0.35-0.9) and short internodes, GTR+G(0.4)
  sat12       deep12 topology with every branch x4 (saturated)
  comp8       8 taxa, 3000 bp, non-stationary: GC-rich and AT-rich terminal branches alternate
              across the two true clades (compositional-attraction bait)
  noclock8    8 taxa, 1200 bp, strongly non-clocklike (UPGMA trap)
  prot15      15 protein sequences, 300 aa, LG+G4
  big150      150 taxa, 1000 bp, birth-death tree with lognormal rate noise, HKY+G
"""
import math
import os
import random
import subprocess
import sys

import dendropy
from dendropy.model.birthdeath import birth_death_tree

IQTREE = r"F:\OpenScience\audit-envs\molecular-phylogenetics-analyst\tools\bin\iqtree2.exe"
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(__file__))


def write(name, text):
    with open(os.path.join(OUT, name), "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)


def alisim(prefix, model, tree_name, length, seed, extra=()):
    cmd = [IQTREE, "--alisim", os.path.join(OUT, prefix), "-m", model, "-t", os.path.join(OUT, tree_name),
           "--length", str(length), "--seed", str(seed), "-af", "fasta", "-redo", *extra]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(r.stdout[-2000:] + r.stderr[-2000:])
    log = os.path.join(OUT, tree_name + ".log")
    if os.path.exists(log):
        os.remove(log)


def random_tree(n, height, seed, noise_sd, prefix):
    rng = random.Random(seed)
    t = birth_death_tree(birth_rate=1.0, death_rate=0.0, num_extant_tips=n, rng=rng)
    t.calc_node_ages()
    h = t.seed_node.age
    for i, leaf in enumerate(t.leaf_node_iter()):
        leaf.taxon.label = f"{prefix}{i + 1:03d}" if n > 99 else f"{prefix}{i + 1:02d}"
    for e in t.postorder_edge_iter():
        if e.length is not None:
            e.length = max(e.length / h * height * math.exp(rng.gauss(0, noise_sd)), 1e-4)
    return t.as_string(schema="newick", suppress_rooting=True, suppress_internal_node_labels=True).strip()


# --- hand-written trees --------------------------------------------------------------------------
DEEP12 = ("(((T01:0.90,T02:0.35):0.06,(T03:0.40,T04:0.85):0.05):0.04,((T05:0.80,T06:0.45):0.07,"
          "(T07:0.38,T08:0.88):0.05):0.05,((T09:0.50,T10:0.90):0.06,(T11:0.85,T12:0.42):0.05):0.04);")


def scale_newick(nwk, k):
    t = dendropy.Tree.get(data=nwk, schema="newick")
    for e in t.postorder_edge_iter():
        if e.length is not None:
            e.length *= k
    return t.as_string(schema="newick", suppress_rooting=True).strip()


# comp8: true clades (GC1,AT1,GC2,AT2) | (GC3,AT3,GC4,AT4); pairs ((GC1,AT1),(GC2,AT2)) etc.
GCF = "GTR{1,4,1,1,4,1}+F{0.10,0.40,0.40,0.10}"
ATF = "GTR{1,4,1,1,4,1}+F{0.40,0.10,0.10,0.40}"
COMP8 = ("(((GC1:0.45[&model=%s],AT1:0.45[&model=%s]):0.03,(GC2:0.45[&model=%s],AT2:0.45[&model=%s]):0.03):0.03,"
         "((GC3:0.45[&model=%s],AT3:0.45[&model=%s]):0.03,(GC4:0.45[&model=%s],AT4:0.45[&model=%s]):0.03):0.03);"
         % (GCF, ATF, GCF, ATF, GCF, ATF, GCF, ATF))
COMP8_TOPO = "(((GC1,AT1),(GC2,AT2)),((GC3,AT3),(GC4,AT4)));"

# noclock8: fast lineage F1 is sister to slow S1; slow S2..S4 form the other side
NOCLOCK8 = ("(((S1:0.02,F1:0.55):0.04,(S2:0.02,F2:0.50):0.04):0.03,((S3:0.03,S4:0.03):0.05,"
            "(S5:0.02,S6:0.03):0.05):0.03);")


def main():
    os.makedirs(OUT, exist_ok=True)
    # barcode20
    write("barcode20_true.nwk", random_tree(20, 0.06, 11, 0.25, "sp") + "\n")
    alisim("barcode20", "HKY{12}+F{0.30,0.15,0.15,0.40}+G4{0.5}", "barcode20_true.nwk", 658, 1101)
    # deep12 and saturated copy
    write("deep12_true.nwk", DEEP12 + "\n")
    alisim("deep12", "GTR{1,6,1,1,6,1}+F{0.30,0.20,0.20,0.30}+G4{0.4}", "deep12_true.nwk", 1500, 1202)
    write("sat12_true.nwk", scale_newick(DEEP12, 4.0) + "\n")
    alisim("sat12", "GTR{1,6,1,1,6,1}+F{0.30,0.20,0.20,0.30}+G4{0.4}", "sat12_true.nwk", 1500, 1203)
    # comp8 (branch-specific non-stationary models; root model equal frequencies)
    write("comp8_sim.nwk", COMP8 + "\n")
    write("comp8_true.nwk", COMP8_TOPO + "\n")
    alisim("comp8", "GTR{1,4,1,1,4,1}+F{0.25,0.25,0.25,0.25}", "comp8_sim.nwk", 3000, 1304)
    # noclock8
    write("noclock8_true.nwk", NOCLOCK8 + "\n")
    alisim("noclock8", "HKY{4}+F{0.25,0.25,0.25,0.25}", "noclock8_true.nwk", 1200, 1405)
    # prot15
    write("prot15_true.nwk", random_tree(15, 0.8, 15, 0.3, "P") + "\n")
    alisim("prot15", "LG+G4{0.8}", "prot15_true.nwk", 300, 1506)
    # big150
    write("big150_true.nwk", random_tree(150, 0.35, 150, 0.4, "t") + "\n")
    alisim("big150", "HKY{5}+F{0.28,0.22,0.22,0.28}+G4{0.6}", "big150_true.nwk", 1000, 1607)
    write("README.txt", "ALL FILES IN THIS FOLDER ARE SYNTHETIC (IQ-TREE 2.4.0 AliSim from the *_true.nwk trees; "
                        "see make_data.py for models and seeds).\n")
    print("done")


if __name__ == "__main__":
    main()
