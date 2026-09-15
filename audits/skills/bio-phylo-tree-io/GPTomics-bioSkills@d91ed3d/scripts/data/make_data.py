"""SYNTHETIC data generator for the bio-phylo-tree-io audit (2026-09-15).

Everything written here is synthetic. No real sequences or real study trees.
  - true10.nwk              hand-written 10-taxon true tree (known truth)
  - sim10.fa / sim10.nex    IQ-TREE 2.4.0 AliSim alignment from true10.nwk (HKY+G4, 900 bp, seed 7)
  - iq10.treefile           IQ-TREE 2.4.0 ML tree with SH-aLRT/UFBoot dual labels (-B 1000 -alrt 1000)
  - mb10.con.tre, mb10.run1.t, mb10.run2.t   MrBayes 3.2.7a very short run (20k gen, 2 runs)
  - mcc6.tree               HAND-WRITTEN BEAST/TreeAnnotator-style annotated MCC Nexus (TRANSLATE table,
                            [&R], posterior, height, height_95%_HPD={..}, rate, length_95%_HPD). Values invented
                            but internally consistent (ultrametric, HPD brackets contain heights).
  - mcc6_truth.tsv          the node values written into mcc6.tree, for checking parsers
  - names_odd.nwk + names_meta.tsv   tip names with spaces, quotes, commas, parentheses, non-ASCII
  - nhx8.nhx                NHX written by ete3 (S=, B=, D= tags)
  - phylo8.xml              phyloXML (typed taxonomy + two <confidence> elements per clade), hand-written
  - nex8.xml                NeXML written by DendroPy with node annotations
  - runA.t / runB.t         two posterior tree files with DIFFERENT TRANSLATE numbering (merge trap)
  - collab_post.nwk         Newick whose internal labels are posterior probabilities in [0,1]
usage: python make_data.py   (writes next to this script)
"""
import os
import re
import subprocess
import random

HERE = os.path.dirname(os.path.abspath(__file__))
BIN = r"F:\OpenScience\audit-envs\molecular-phylogenetics-analyst\tools\bin"
IQ = os.path.join(BIN, "iqtree2.exe")
MB = os.path.join(BIN, "mb.exe")

TRUE10 = ("((((Homo_sapiens:0.03,Pan_troglodytes:0.04):0.05,Gorilla_gorilla:0.07):0.06,"
          "(Macaca_mulatta:0.08,Papio_anubis:0.07):0.05):0.12,"
          "((Mus_musculus:0.10,Rattus_norvegicus:0.11):0.15,"
          "(Bos_taurus:0.12,Sus_scrofa:0.10):0.08):0.07,Gallus_gallus:0.40);")


def w(name, text):
    with open(os.path.join(HERE, name), "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)


def run(cmd, cwd=HERE):
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(" ".join(cmd) + "\n" + r.stdout[-3000:] + r.stderr[-3000:])
    return r.stdout


def fasta_to_nexus(fa, nex, mrbayes_block):
    seqs, name = {}, None
    for line in open(fa, encoding="utf-8"):
        line = line.strip()
        if line.startswith(">"):
            name = line[1:].split()[0]
            seqs[name] = []
        elif line:
            seqs[name].append(line)
    seqs = {k: "".join(v) for k, v in seqs.items()}
    L = len(next(iter(seqs.values())))
    out = ["#NEXUS", "begin data;", f"  dimensions ntax={len(seqs)} nchar={L};",
           "  format datatype=dna missing=? gap=-;", "  matrix"]
    out += [f"  {k:<20} {v}" for k, v in seqs.items()]
    out += ["  ;", "end;", mrbayes_block]
    w(nex, "\n".join(out) + "\n")


def make_iqtree():
    w("true10.nwk", TRUE10 + "\n")
    run([IQ, "--alisim", "sim10", "-m", "HKY{3.0}+F{0.3,0.2,0.2,0.3}+G4{0.5}", "-t", "true10.nwk",
         "--length", "900", "--seed", "7", "-af", "fasta", "-redo"])
    run([IQ, "-s", "sim10.fa", "-m", "HKY+G4", "-B", "1000", "-alrt", "1000", "-T", "1",
         "--seed", "7", "--prefix", "iq10", "-redo", "-quiet"])
    for ext in (".bionj", ".mldist", ".ckp.gz", ".model.gz", ".splits.nex", ".uniqueseq.phy"):
        p = os.path.join(HERE, "iq10" + ext)
        if os.path.exists(p):
            os.remove(p)


def make_mrbayes():
    block = ("begin mrbayes;\n  set autoclose=yes nowarn=yes seed=11 swapseed=12;\n  lset nst=2 rates=gamma;\n"
             "  mcmcp ngen=20000 samplefreq=100 printfreq=5000 diagnfreq=5000 nruns=2 nchains=2 "
             "filename=mb10;\n  mcmc;\n  sumt burninfrac=0.25;\n  sump burninfrac=0.25;\nend;\n")
    fasta_to_nexus(os.path.join(HERE, "sim10.fa"), "sim10.nex", block)
    run([MB, "sim10.nex"])
    for f in os.listdir(HERE):
        if f.startswith("mb10") and f.split(".")[-1] in ("ckp", "ckp~", "mcmc", "parts", "tstat", "vstat", "trprobs", "lstat", "pstat", "p"):
            os.remove(os.path.join(HERE, f))


# ---- hand-written BEAST/TreeAnnotator-style MCC (SYNTHETIC) ----
# taxa: 1 Homo_sapiens 2 Pan_troglodytes 3 Gorilla_gorilla 4 Macaca_mulatta 5 Papio_anubis 6 Callithrix_jacchus
MCC_NODES = [
    # clade, posterior, height, hpd_lo, hpd_hi, rate
    ("Homo_sapiens|Pan_troglodytes", 1.0, 6.4, 5.2, 7.7, 1.02),
    ("Gorilla_gorilla|Homo_sapiens|Pan_troglodytes", 0.9873, 8.9, 7.4, 10.6, 0.97),
    ("Macaca_mulatta|Papio_anubis", 0.6512, 10.1, 7.9, 12.5, 1.10),
    ("Gorilla_gorilla|Homo_sapiens|Macaca_mulatta|Pan_troglodytes|Papio_anubis", 1.0, 29.3, 25.0, 33.8, 0.91),
    ("ROOT", 1.0, 43.2, 38.1, 48.9, None),
]


def make_mcc():
    tip = lambda i, bl, rate: (f"{i}[&rate={rate},height=0.0,height_95%_HPD={{0.0,0.0}},height_median=0.0,"
                               f"length={bl},length_95%_HPD={{{round(bl*0.8,3)},{round(bl*1.2,3)}}}]:{bl}")
    def inner(sub, post, h, lo, hi, rate, bl):
        ann = f"[&posterior={post},height={h},height_95%_HPD={{{lo},{hi}}},height_median={h}"
        if rate is not None:
            ann += f",rate={rate},length={bl},length_95%_HPD={{{round(bl*0.7,3)},{round(bl*1.3,3)}}}"
        ann += "]"
        return f"({sub}){ann}" + (f":{bl}" if bl is not None else "")
    hp = inner(tip(1, 6.4, 1.01) + "," + tip(2, 6.4, 1.03), 1.0, 6.4, 5.2, 7.7, 1.02, round(8.9 - 6.4, 2))
    hpg = inner(hp + "," + tip(3, 8.9, 0.95), 0.9873, 8.9, 7.4, 10.6, 0.97, round(29.3 - 8.9, 2))
    mp = inner(tip(4, 10.1, 1.12) + "," + tip(5, 10.1, 1.08), 0.6512, 10.1, 7.9, 12.5, 1.10, round(29.3 - 10.1, 2))
    cat = inner(hpg + "," + mp, 1.0, 29.3, 25.0, 33.8, 0.91, round(43.2 - 29.3, 2))
    root = inner(cat + "," + tip(6, 43.2, 0.88), 1.0, 43.2, 38.1, 48.9, None, None)
    taxa = ["Homo_sapiens", "Pan_troglodytes", "Gorilla_gorilla", "Macaca_mulatta", "Papio_anubis", "Callithrix_jacchus"]
    txt = ["#NEXUS", "", "[SYNTHETIC: hand-written to mimic TreeAnnotator v2.7 MCC output; values invented for an audit]", "",
           "Begin taxa;", "\tDimensions ntax=6;", "\tTaxlabels"]
    txt += [f"\t\t{t}" for t in taxa] + ["\t\t;", "End;", "Begin trees;", "\tTranslate"]
    txt += [f"\t\t{i} {t}" + ("," if i < 6 else "") for i, t in enumerate(taxa, 1)]
    txt += [";", f"tree TREE1 = [&R] {root};", "End;", ""]
    w("mcc6.tree", "\n".join(txt))
    rows = ["clade\tposterior\theight\thpd_lo\thpd_hi\trate"]
    rows += [f"{c}\t{p}\t{h}\t{lo}\t{hi}\t{'' if r is None else r}" for c, p, h, lo, hi, r in MCC_NODES]
    w("mcc6_truth.tsv", "\n".join(rows) + "\n")


def make_names():
    w("names_odd.nwk",
      "((('Homo sapiens':0.03,'Pan troglodytes (bonobo, captive)':0.04)98:0.05,'O''Brien isolate 7':0.07)87:0.06,"
      "(Macaca_mulatta:0.08,'Cercopithèque_ascagne':0.07)100:0.05,('Rattus norvegicus':0.11,Mus_musculus:0.10)100:0.2);\n")
    w("names_meta.tsv", "taxon\thost_country\tn_samples\n"
      "Homo sapiens\tKenya\t12\nPan troglodytes (bonobo, captive)\tDRC\t3\nO'Brien isolate 7\tIreland\t1\n"
      "Macaca mulatta\tIndia\t8\nCercopithèque ascagne\tUganda\t2\nRattus norvegicus\tFrance\t20\nMus musculus\tFrance\t25\n")


def make_nhx_phyloxml_nexml():
    from ete3 import Tree
    t = Tree("(((A_sp1:0.1,A_sp2:0.12)0.9:0.05,B_sp1:0.2)0.8:0.1,((C_sp1:0.15,C_sp2:0.1)1:0.07,(D_sp1:0.3,D_sp2:0.25)0.95:0.02)0.7:0.1);", format=0)
    species = {"A_sp1": "Arabidopsis thaliana", "A_sp2": "Arabidopsis lyrata", "B_sp1": "Brassica rapa",
               "C_sp1": "Oryza sativa", "C_sp2": "Zea mays", "D_sp1": "Physcomitrium patens", "D_sp2": "Marchantia polymorpha"}
    for n in t.traverse():
        if n.is_leaf():
            n.add_feature("S", species[n.name].replace(" ", "_"))
        else:
            n.add_feature("B", int(round(n.support * 100)))
            n.add_feature("D", "N")
    t.write(outfile=os.path.join(HERE, "nhx8.nhx"), features=["S", "B", "D"], format=0)
    # phyloXML with typed taxonomy and two confidences per internal clade (hand-written, schema 1.10 layout)
    def leaf(n, bl, taxid, sci):
        return (f"<clade><name>{n}</name><branch_length>{bl}</branch_length><taxonomy><id provider=\"ncbi\">{taxid}</id>"
                f"<scientific_name>{sci}</scientific_name><rank>species</rank></taxonomy></clade>")
    def node(children, bl, bs, pp):
        return (f"<clade><branch_length>{bl}</branch_length><confidence type=\"bootstrap\">{bs}</confidence>"
                f"<confidence type=\"probability\">{pp}</confidence>{children}</clade>")
    a = node(leaf("A_sp1", 0.1, 3702, "Arabidopsis thaliana") + leaf("A_sp2", 0.12, 59689, "Arabidopsis lyrata"), 0.05, 90, 0.99)
    ab = node(a + leaf("B_sp1", 0.2, 3711, "Brassica rapa"), 0.1, 80, 0.97)
    c = node(leaf("C_sp1", 0.15, 4530, "Oryza sativa") + leaf("C_sp2", 0.1, 4577, "Zea mays"), 0.07, 100, 1.0)
    d = node(leaf("D_sp1", 0.3, 3218, "Physcomitrium patens") + leaf("D_sp2", 0.25, 3197, "Marchantia polymorpha"), 0.02, 95, 1.0)
    cd = node(c + d, 0.1, 70, 0.88)
    xml = ('<?xml version="1.0" encoding="UTF-8"?>\n<!-- SYNTHETIC audit file -->\n'
           '<phyloxml xmlns="http://www.phyloxml.org" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
           'xsi:schemaLocation="http://www.phyloxml.org http://www.phyloxml.org/1.10/phyloxml.xsd">\n'
           f'<phylogeny rooted="true"><name>plants8</name><clade>{ab}{cd}</clade></phylogeny>\n</phyloxml>\n')
    w("phylo8.xml", xml)
    import dendropy
    tr = dendropy.Tree.get(data=open(os.path.join(HERE, "true10.nwk")).read(), schema="newick", rooting="force-rooted")
    for nd in tr.postorder_internal_node_iter():
        nd.annotations.add_new("bootstrap", 100 if len(nd.leaf_nodes()) < 5 else 76)
    tr.write(path=os.path.join(HERE, "nex8.xml"), schema="nexml")


def make_translate_pair():
    taxa = ["Homo_sapiens", "Pan_troglodytes", "Gorilla_gorilla", "Macaca_mulatta", "Papio_anubis", "Mus_musculus"]
    topo = "(((Homo_sapiens,Pan_troglodytes),Gorilla_gorilla),(Macaca_mulatta,Papio_anubis),Mus_musculus)"
    random.seed(5)
    for fname, order in (("runA.t", taxa), ("runB.t", ["Mus_musculus", "Papio_anubis", "Macaca_mulatta",
                                                         "Gorilla_gorilla", "Pan_troglodytes", "Homo_sapiens"])):
        idx = {t: i for i, t in enumerate(order, 1)}
        lines = ["#NEXUS", "[SYNTHETIC posterior sample file, MrBayes .t layout]", "begin trees;", "   translate"]
        lines += [f"      {i} {t}" + ("," if i < len(order) else ";") for i, t in enumerate(order, 1)]
        for g in range(0, 1000, 100):
            bl = lambda: f"{random.uniform(0.01, 0.2):.4f}"
            s = re.sub(r"[A-Za-z_]+", lambda m: f"{idx[m.group(0)]}:{bl()}", topo)
            s = re.sub(r"\)(?=[,)])", lambda m: f"):{bl()}", s)
            lines.append(f"   tree gen.{g} = [&U] {s};")
        lines.append("end;")
        w(fname, "\n".join(lines) + "\n")


def make_collab():
    w("collab_post.nwk", "(((Homo_sapiens:0.03,Pan_troglodytes:0.04)1.00:0.05,Gorilla_gorilla:0.07)0.98:0.06,"
      "((Macaca_mulatta:0.08,Papio_anubis:0.07)0.62:0.05,(Mus_musculus:0.10,Rattus_norvegicus:0.11)0.99:0.15)0.54:0.07,Gallus_gallus:0.40);\n")


if __name__ == "__main__":
    make_iqtree()
    make_mrbayes()
    make_mcc()
    make_names()
    make_nhx_phyloxml_nexml()
    make_translate_pair()
    make_collab()
    print("done:", sorted(os.listdir(HERE)))
