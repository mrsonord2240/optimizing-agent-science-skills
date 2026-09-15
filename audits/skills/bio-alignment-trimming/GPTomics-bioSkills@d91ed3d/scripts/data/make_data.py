"""SYNTHETIC data for the bio-alignment-trimming audit (molecular-phylogenetics-analyst, re-generated 2026-09-15).

Nothing here is real sequence data. Sequences are simulated with IQ-TREE 2.4.0 AliSim (with indels)
from known trees, then aligned with MAFFT 7.526 L-INS-i, so each input is a realistic *estimated*
MSA whose true tree is known.

  prot15_linsi.fasta      single protein gene, 15 taxa (canonical trimming input)
  dna_super/              12 taxa x 20 DNA loci x 800 nt, mid-depth; per-locus MSAs + concatenation
  unbal33_linsi.fasta     30 shallow ingroup taxa + 3 distant outgroups, 1,000 nt DNA
  deep_super/             16 taxa x 12 protein loci x 250 aa, deep/long branches; per-locus MSAs + concatenation
  cds10_codon_aln.fasta   10-taxon codon alignment (protein-guided, PAL2NAL) for the selection-analysis input
"""
import os
import random
import subprocess

from Bio import SeqIO, AlignIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord

HERE = os.path.dirname(os.path.abspath(__file__))
TOOLS = r"F:\OpenScience\audit-envs\molecular-phylogenetics-analyst\tools"
IQTREE = os.path.join(TOOLS, "bin", "iqtree2.exe")
MAFFT = os.path.join(TOOLS, "mafft-win", "mafft.bat")
PAL2NAL = os.path.join(TOOLS, "bin", "pal2nal.pl")

PROT15_TREE = ("(((((P01:0.10,P02:0.12):0.05,(P03:0.15,P04:0.11):0.06):0.08,((P05:0.20,P06:0.18):0.07,P07:0.25):0.05):0.10,"
               "(((P08:0.14,P09:0.16):0.09,P10:0.22):0.06,(P11:0.30,P12:0.28):0.08):0.07):0.12,"
               "(P13:0.35,(P14:0.25,P15:0.40):0.10):0.15);")
DNA12_TREE = ("((((T01:0.04,T02:0.05):0.03,(T03:0.06,T04:0.05):0.02):0.04,((T05:0.07,T06:0.06):0.03,T07:0.09):0.02):0.05,"
              "(((T08:0.05,T09:0.06):0.04,T10:0.08):0.03,(T11:0.10,T12:0.12):0.04):0.05);")
CDS10_TREE = ("((((Sp01:0.05,Sp02:0.06):0.03,(Sp03:0.08,Sp04:0.07):0.04):0.05,(Sp05:0.10,Sp06:0.09):0.06):0.08,"
              "((Sp07:0.12,Sp08:0.11):0.05,(Sp09:0.15,Sp10:0.14):0.07):0.06);")


def run(cmd, **kw):
    r = subprocess.run(cmd, capture_output=True, text=True, **kw)
    if r.returncode != 0:
        raise RuntimeError(" ".join(cmd) + "\n" + r.stdout[-2000:] + r.stderr[-2000:])
    return r


def write_tree(name, nwk):
    p = os.path.join(HERE, name)
    open(p, "w", encoding="utf-8", newline="\n").write(nwk + "\n")
    return p


def alisim(prefix, model, tree, length, seed, indel, size="POW{1.7/20},POW{1.7/20}", extra=()):
    run([IQTREE, "--alisim", prefix, "-m", model, "-t", tree, "--length", str(length), "--seed", str(seed),
         "-af", "fasta", "-redo", "--indel", indel, "--indel-size", size, *extra])
    for suf in (".fa",):
        os.replace(prefix + suf, prefix + "_true_aln.fa")
    recs = list(SeqIO.parse(prefix + ".unaligned.fa", "fasta"))
    for r in recs:
        r.description = ""
    SeqIO.write(recs, prefix + "_unaligned.fa", "fasta")
    os.remove(prefix + ".unaligned.fa")


def mafft_linsi(inp, out):
    with open(out, "w") as fh:
        r = subprocess.run([MAFFT, "--localpair", "--maxiterate", "1000", inp], stdout=fh, stderr=subprocess.PIPE,
                           text=True)
    if r.returncode:
        raise RuntimeError(r.stderr)
    recs = list(SeqIO.parse(out, "fasta"))
    for r in recs:
        r.seq = r.seq.upper()
        r.description = ""
    SeqIO.write(recs, out, "fasta")


def concat(paths, out_fa, out_nex):
    alns = [AlignIO.read(p, "fasta") for p in paths]
    ids = sorted(r.id for r in alns[0])
    seqs = {i: [] for i in ids}
    parts, start = [], 1
    for p, a in zip(paths, alns):
        d = {r.id: str(r.seq) for r in a}
        for i in ids:
            seqs[i].append(d[i])
        L = a.get_alignment_length()
        parts.append((os.path.splitext(os.path.basename(p))[0], start, start + L - 1))
        start += L
    SeqIO.write([SeqRecord(Seq("".join(seqs[i])), id=i, description="") for i in ids], out_fa, "fasta")
    with open(out_nex, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("#nexus\nbegin sets;\n")
        for n, a, b in parts:
            fh.write(f"  charset {n} = {a}-{b};\n")
        fh.write("end;\n")


def random_tree(n_in, n_out, seed):
    rng = random.Random(seed)
    nodes = [(f"In{i+1:02d}", 0.0) for i in range(n_in)]
    t = 0.0
    while len(nodes) > 1:  # coalescent-shaped shallow ingroup
        k = len(nodes)
        t += rng.expovariate(k * (k - 1) / 2) * 0.01
        a, b = rng.sample(range(k), 2)
        (na, ha), (nb, hb) = nodes[a], nodes[b]
        for j in sorted((a, b), reverse=True):
            nodes.pop(j)
        nodes.append((f"({na}:{t-ha:.5f},{nb}:{t-hb:.5f})", t))
    ingroup, h = nodes[0]
    return f"({ingroup}:{0.35 - h:.5f},((Out1:0.30,Out2:0.28):0.10,Out3:0.40):0.10);"


def main():
    # prot15 single gene
    alisim(os.path.join(HERE, "prot15"), "LG+G4{0.8}", write_tree("prot15_true.nwk", PROT15_TREE), 320, 202, "0.03,0.03",
           size="POW{1.7/30},POW{1.7/30}")
    mafft_linsi(os.path.join(HERE, "prot15_unaligned.fa"), os.path.join(HERE, "prot15_linsi.fasta"))

    # DNA supermatrix, mid-depth
    d = os.path.join(HERE, "dna_super")
    os.makedirs(d, exist_ok=True)
    tf = write_tree("dna12_true.nwk", DNA12_TREE)
    paths = []
    for i in range(1, 21):
        pre = os.path.join(d, f"locus{i:02d}")
        alisim(pre, "GTR{1.5,4.5,0.9,1.2,5.0,1.0}+F{0.3,0.2,0.2,0.3}+G4{0.5}", tf, 800, 1000 + i, "0.03,0.03")
        mafft_linsi(pre + "_unaligned.fa", pre + ".aln.fasta")
        paths.append(pre + ".aln.fasta")
    concat(paths, os.path.join(d, "supermatrix.fasta"), os.path.join(d, "supermatrix.nex"))

    # unbalanced 30 + 3
    tr = random_tree(30, 3, 55)
    write_tree("unbal33_true.nwk", tr)
    alisim(os.path.join(HERE, "unbal33"), "HKY{4.0}+F{0.3,0.2,0.2,0.3}+G4{0.5}", os.path.join(HERE, "unbal33_true.nwk"),
           1000, 606, "0.02,0.02")
    mafft_linsi(os.path.join(HERE, "unbal33_unaligned.fa"), os.path.join(HERE, "unbal33_linsi.fasta"))

    # deep protein supermatrix (16 taxa, long branches)
    rng = random.Random(9)
    names = [f"D{i+1:02d}" for i in range(16)]
    def build(ns):
        if len(ns) == 1:
            return ns[0]
        m = len(ns) // 2
        return f"({build(ns[:m])}:{rng.uniform(0.05, 0.25):.3f},{build(ns[m:])}:{rng.uniform(0.05, 0.25):.3f})"
    deep = build(names) + ";"
    import re
    deep = re.sub(r"(D\d\d)", lambda m: m.group(1) + f":{rng.uniform(0.4, 1.0):.3f}", deep)
    deep = re.sub(r"(D\d\d:[0-9.]+):[0-9.]+", r"\1", deep)
    write_tree("deep16_true.nwk", deep)
    d = os.path.join(HERE, "deep_super")
    os.makedirs(d, exist_ok=True)
    paths = []
    for i in range(1, 13):
        pre = os.path.join(d, f"gene{i:02d}")
        alisim(pre, "LG+G4{0.7}", os.path.join(HERE, "deep16_true.nwk"), 250, 2000 + i, "0.03,0.03",
               size="POW{1.7/30},POW{1.7/30}")
        mafft_linsi(pre + "_unaligned.fa", pre + ".aln.fasta")
        paths.append(pre + ".aln.fasta")
    concat(paths, os.path.join(d, "supermatrix.fasta"), os.path.join(d, "supermatrix.nex"))

    # codon alignment (protein-guided)
    alisim(os.path.join(HERE, "cds10"), "GY{0.2,3.0}+F3X4", write_tree("cds10_true.nwk", CDS10_TREE), 900, 303,
           "0.03,0.03", size="POW{1.7/10},POW{1.7/10}", extra=("-st", "CODON"))
    cds = list(SeqIO.parse(os.path.join(HERE, "cds10_unaligned.fa"), "fasta"))
    SeqIO.write([SeqRecord(r.seq.translate(), id=r.id, description="") for r in cds],
                os.path.join(HERE, "cds10_prot.fa"), "fasta")
    mafft_linsi(os.path.join(HERE, "cds10_prot.fa"), os.path.join(HERE, "cds10_prot_aln.fa"))
    with open(os.path.join(HERE, "cds10_codon_aln.fasta"), "w") as fh:
        r = subprocess.run(["perl", PAL2NAL, os.path.join(HERE, "cds10_prot_aln.fa"),
                            os.path.join(HERE, "cds10_unaligned.fa"), "-output", "fasta"], stdout=fh,
                           stderr=subprocess.PIPE, text=True)
    if r.returncode:
        raise RuntimeError(r.stderr)

    # replicate single protein genes (same true tree as prot15, 10 seeds) for trimmed-vs-untrimmed accuracy
    d = os.path.join(HERE, "reps")
    os.makedirs(d, exist_ok=True)
    for i in range(1, 11):
        pre = os.path.join(d, f"rep{i:02d}")
        alisim(pre, "LG+G4{0.8}", os.path.join(HERE, "prot15_true.nwk"), 320, 7000 + i, "0.05,0.05",
               size="POW{1.7/30},POW{1.7/30}")
        mafft_linsi(pre + "_unaligned.fa", pre + ".aln.fasta")

    for root, _, files in os.walk(HERE):
        for f in files:
            if f.endswith(".log"):
                os.remove(os.path.join(root, f))
    print("SYNTHETIC data written to", HERE)


if __name__ == "__main__":
    main()
