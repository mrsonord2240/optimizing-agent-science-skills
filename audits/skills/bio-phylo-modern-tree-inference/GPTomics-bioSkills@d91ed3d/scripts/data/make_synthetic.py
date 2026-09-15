"""SYNTHETIC data generator for the molecular-phylogenetics-analyst audit (2026-09-11).

Every file this script writes is simulated. Nothing here is real sequence data.
Trees are hand-written or simulated with DendroPy; sequences are simulated with
IQ-TREE 2.4.0 AliSim under stated models and seeds, so the true tree is known.

usage: python make_synthetic.py OUTDIR set [set ...]
sets:  gene12   12-taxon DNA gene, true tree + true alignment + unaligned seqs
       prot15   15-taxon protein family with indels (unaligned + true alignment)
       ils      8-taxon, 40-locus data simulated under the multispecies coalescent
       virus    30 heterochronous tips with sampling dates (strict clock)
       lba      8-taxon DNA with two long branches (long-branch-attraction bait)
"""
import os
import random
import subprocess
import sys

IQTREE = r"F:\OpenScience\audit-envs\molecular-phylogenetics-analyst\tools\bin\iqtree2.exe"

GENE12_TREE = ("((((Homo_sapiens:0.020,Pan_troglodytes:0.025):0.030,Gorilla_gorilla:0.050):0.040,"
               "(Macaca_mulatta:0.060,Callithrix_jacchus:0.080):0.020):0.100,"
               "((Mus_musculus:0.090,Rattus_norvegicus:0.100):0.120,"
               "(Bos_taurus:0.080,(Canis_familiaris:0.070,Felis_catus:0.065):0.030):0.040):0.050,"
               "(Gallus_gallus:0.250,Xenopus_tropicalis:0.350):0.150);")

PROT15_TREE = ("(((((P01:0.10,P02:0.12):0.05,(P03:0.15,P04:0.11):0.06):0.08,((P05:0.20,P06:0.18):0.07,P07:0.25):0.05):0.10,"
               "(((P08:0.14,P09:0.16):0.09,P10:0.22):0.06,(P11:0.30,P12:0.28):0.08):0.07):0.12,"
               "(P13:0.35,(P14:0.25,P15:0.40):0.10):0.15);")

# long-branch-attraction bait: true tree ((A,B),(C,D)) ... with long A and C
LBA_TREE = ("((((Fast_A:0.90,Slow_B:0.05):0.02,(Fast_C:0.90,Slow_D:0.05):0.02):0.02,"
            "(Slow_E:0.06,Slow_F:0.07):0.03):0.05,(Out_G:0.10,Out_H:0.12):0.05);")


def alisim(prefix, model, tree_file, length, seed, indel=None):
    cmd = [IQTREE, "--alisim", prefix, "-m", model, "-t", tree_file,
           "--length", str(length), "--seed", str(seed), "-af", "fasta", "-redo"]
    if indel:
        cmd += ["--indel", indel, "--indel-size", "POW{1.7/30},POW{1.7/30}"]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(r.stdout[-2000:] + r.stderr[-2000:])


def write(path, text):
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)


def make_gene12(out):
    write(os.path.join(out, "gene12_true.nwk"), GENE12_TREE + "\n")
    alisim(os.path.join(out, "gene12"), "GTR{1.2,4.0,0.8,1.1,4.5,1.0}+F{0.28,0.22,0.24,0.26}+G4{0.6}",
           os.path.join(out, "gene12_true.nwk"), 1200, 101, indel="0.02,0.02")
    os.replace(os.path.join(out, "gene12.fa"), os.path.join(out, "gene12_true_aln.fa"))
    os.replace(os.path.join(out, "gene12.unaligned.fa"), os.path.join(out, "gene12_unaligned.fa"))


def make_prot15(out):
    write(os.path.join(out, "prot15_true.nwk"), PROT15_TREE + "\n")
    alisim(os.path.join(out, "prot15"), "LG+G4{0.8}", os.path.join(out, "prot15_true.nwk"), 320, 202,
           indel="0.03,0.03")
    os.replace(os.path.join(out, "prot15.fa"), os.path.join(out, "prot15_true_aln.fa"))
    os.replace(os.path.join(out, "prot15.unaligned.fa"), os.path.join(out, "prot15_unaligned.fa"))


def make_lba(out):
    write(os.path.join(out, "lba_true.nwk"), LBA_TREE + "\n")
    alisim(os.path.join(out, "lba"), "GTR{1,5,1,1,5,1}+F{0.25,0.25,0.25,0.25}+G4{0.3}",
           os.path.join(out, "lba_true.nwk"), 3000, 303)
    os.replace(os.path.join(out, "lba.fa"), os.path.join(out, "lba_aln.fa"))


def make_ils(out, n_loci=40, locus_len=600):
    import dendropy
    from dendropy.simulate import treesim
    rng = random.Random(404)
    # species tree in coalescent units (pop_size=1 so branch length = generations/N);
    # two short successive internodes (0.15, 0.2) around (Sp_C,Sp_D,Sp_E)
    sp_newick = ("(((((Sp_A:0.4,Sp_B:0.4):1.5,((Sp_C:0.35,Sp_D:0.35):0.20,Sp_E:0.55):1.35):0.15,"
                 "Sp_F:2.05):1.0,Sp_G:3.05):2.0,Sp_H:5.05);")
    sp = dendropy.Tree.get(data=sp_newick, schema="newick")
    write(os.path.join(out, "ils_species_true.nwk"), sp.as_string(schema="newick").replace("[&R] ", ""))
    gene_tns = dendropy.TaxonNamespace()
    mapping = {}
    for t in sp.taxon_namespace:
        g = gene_tns.require_taxon(label=t.label)
        mapping.setdefault(t, []).append(g)
    tmap = dendropy.TaxonNamespaceMapping(domain_taxon_namespace=gene_tns, range_taxon_namespace=sp.taxon_namespace,
                                          mapping_fn=lambda gt: sp.taxon_namespace.get_taxon(label=gt.label))
    for nd in sp.postorder_node_iter():
        nd.edge.pop_size = 1.0
    os.makedirs(os.path.join(out, "ils_loci"), exist_ok=True)
    gene_trees = []
    for i in range(1, n_loci + 1):
        gt = treesim.contained_coalescent_tree(containing_tree=sp, gene_to_containing_taxon_map=tmap,
                                               default_pop_size=1.0, rng=rng)
        scale = rng.uniform(0.02, 0.05)  # substitutions per coalescent unit for this locus
        for e in gt.postorder_edge_iter():
            if e.length is not None:
                e.length = e.length * scale
        nwk = gt.as_string(schema="newick", suppress_rooting=True).strip()
        gene_trees.append(nwk)
        tf = os.path.join(out, "ils_loci", f"locus{i:02d}_true.nwk")
        write(tf, nwk + "\n")
        alisim(os.path.join(out, "ils_loci", f"locus{i:02d}"), "HKY{3.0}+F{0.3,0.2,0.2,0.3}+G4{0.7}", tf,
               locus_len, 5000 + i)
        os.remove(tf)
        tl = tf + ".log"
        if os.path.exists(tl):
            os.remove(tl)
    write(os.path.join(out, "ils_true_gene_trees.nwk"), "\n".join(gene_trees) + "\n")


def make_virus(out, n=30, rate=2.0e-3, length=3000):
    """Heterochronous serial coalescent (constant Ne*g = 4 years), sampling 2000-2020."""
    rng = random.Random(505)
    dates = sorted(round(rng.uniform(2000.0, 2020.0), 2) for _ in range(n))
    names = [f"V{i+1:02d}|{d:.2f}" for i, d in enumerate(dates)]
    present = max(dates)
    # (time before present, node newick, node height)
    events = sorted(((present - d, names[i]) for i, d in enumerate(dates)), key=lambda x: x[0])
    theta = 4.0
    active = []  # list of (label, height)
    t = 0.0
    idx = 0
    while idx < len(events) or len(active) > 1:
        k = len(active)
        wait = rng.expovariate(k * (k - 1) / 2 / theta) if k >= 2 else float("inf")
        nxt_sample = events[idx][0] if idx < len(events) else float("inf")
        if t + wait < nxt_sample:
            t += wait
            a, b = rng.sample(range(k), 2)
            (la, ha), (lb, hb) = active[a], active[b]
            for j in sorted((a, b), reverse=True):
                active.pop(j)
            active.append((f"({la}:{(t-ha)*rate:.6f},{lb}:{(t-hb)*rate:.6f})", t))
        else:
            t = nxt_sample
            active.append((events[idx][1], t))
            idx += 1
    tree = active[0][0] + ";"
    tmrca = present - active[0][1]
    safe = tree.replace("|", "_")
    write(os.path.join(out, "virus_true.nwk"), safe + "\n")
    alisim(os.path.join(out, "virus"), "HKY{4.0}+F{0.3,0.2,0.2,0.3}+G4{1.0}", os.path.join(out, "virus_true.nwk"),
           length, 606)
    os.replace(os.path.join(out, "virus.fa"), os.path.join(out, "virus_aln.fa"))
    with open(os.path.join(out, "virus_dates.tsv"), "w", encoding="utf-8", newline="\n") as fh:
        for nm, d in zip(names, dates):
            fh.write(f"{nm.replace('|', '_')}\t{d:.2f}\n")
    write(os.path.join(out, "virus_truth.txt"),
          f"SYNTHETIC. clock rate = {rate} subs/site/yr (strict); true TMRCA = {tmrca:.2f}\n")


if __name__ == "__main__":
    outdir = sys.argv[1]
    os.makedirs(outdir, exist_ok=True)
    for s in sys.argv[2:]:
        {"gene12": make_gene12, "prot15": make_prot15, "ils": make_ils, "virus": make_virus,
         "lba": make_lba}[s](outdir)
        print("made", s)
    for f in os.listdir(outdir):
        if f.endswith(".log") or f.endswith(".nwk.log"):
            os.remove(os.path.join(outdir, f))
