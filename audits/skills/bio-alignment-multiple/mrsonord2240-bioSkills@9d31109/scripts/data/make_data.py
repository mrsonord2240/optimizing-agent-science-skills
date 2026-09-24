"""SYNTHETIC data for the bio-alignment-multiple audit (molecular-phylogenetics-analyst, 2026-09-11).

Nothing here is real sequence data. Every set is simulated with IQ-TREE 2.4.0 AliSim from a
known tree, so the TRUE alignment is known and alignment accuracy can be scored.

sets written to the directory of this script:
  prot15_*    15 protein sequences, LG+G4, 320 aa root, indels (canonical MSA input)
  cds10_*     10 coding sequences, GY(omega=0.2,kappa=3)+F3X4, 900 nt, codon indels; +protein translation
  mixed13_*   gene12 DNA set with 3 reverse-complemented members and 1 non-homologous sequence
  big1050_*   1050-tip viral-like gene (HKY+G, 1500 nt, indels); 1000 full-length + 50 partial amplicons
  twi8_*      8 very divergent proteins (twilight zone), LG+G4, 250 aa, indels
"""
import os
import random
import subprocess

from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord

HERE = os.path.dirname(os.path.abspath(__file__))
IQTREE = r"F:\OpenScience\audit-envs\molecular-phylogenetics-analyst\tools\bin\iqtree2.exe"

PROT15_TREE = ("(((((P01:0.10,P02:0.12):0.05,(P03:0.15,P04:0.11):0.06):0.08,((P05:0.20,P06:0.18):0.07,P07:0.25):0.05):0.10,"
               "(((P08:0.14,P09:0.16):0.09,P10:0.22):0.06,(P11:0.30,P12:0.28):0.08):0.07):0.12,"
               "(P13:0.35,(P14:0.25,P15:0.40):0.10):0.15);")
CDS10_TREE = ("((((Sp01:0.05,Sp02:0.06):0.03,(Sp03:0.08,Sp04:0.07):0.04):0.05,(Sp05:0.10,Sp06:0.09):0.06):0.08,"
              "((Sp07:0.12,Sp08:0.11):0.05,(Sp09:0.15,Sp10:0.14):0.07):0.06);")
GENE12_TREE = ("((((Homo_sapiens:0.020,Pan_troglodytes:0.025):0.030,Gorilla_gorilla:0.050):0.040,"
               "(Macaca_mulatta:0.060,Callithrix_jacchus:0.080):0.020):0.100,"
               "((Mus_musculus:0.090,Rattus_norvegicus:0.100):0.120,"
               "(Bos_taurus:0.080,(Canis_familiaris:0.070,Felis_catus:0.065):0.030):0.040):0.050,"
               "(Gallus_gallus:0.250,Xenopus_tropicalis:0.350):0.150);")
TWI8_TREE = ("((T1:1.3,T2:1.2):0.4,(T3:1.4,T4:1.25):0.35,((T5:1.3,T6:1.35):0.3,(T7:1.2,T8:1.4):0.3):0.2);")


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(r.stdout[-3000:] + r.stderr[-3000:])


def alisim(prefix, model, tree, length, seed, indel=None, size="POW{1.7/30},POW{1.7/30}", extra=()):
    cmd = [IQTREE, "--alisim", prefix, "-m", model, "-t", tree, "--length", str(length),
           "--seed", str(seed), "-af", "fasta", "-redo", *extra]
    if indel:
        cmd += ["--indel", indel, "--indel-size", size]
    run(cmd)


def tree_file(name, newick):
    p = os.path.join(HERE, name)
    with open(p, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(newick + "\n")
    return p


def clean_ids(path):
    recs = list(SeqIO.parse(path, "fasta"))
    for r in recs:
        r.description = ""
    SeqIO.write(recs, path, "fasta")
    return recs


def main():
    # prot15
    alisim(os.path.join(HERE, "prot15"), "LG+G4{0.8}", tree_file("prot15_true.nwk", PROT15_TREE), 320, 202,
           indel="0.03,0.03")
    os.replace(os.path.join(HERE, "prot15.fa"), os.path.join(HERE, "prot15_true_aln.fa"))
    os.replace(os.path.join(HERE, "prot15.unaligned.fa"), os.path.join(HERE, "prot15_unaligned.fa"))

    # cds10 (codon indels; indel sizes are in codons for codon data)
    alisim(os.path.join(HERE, "cds10"), "GY{0.2,3.0}+F3X4", tree_file("cds10_true.nwk", CDS10_TREE), 900, 303,
           indel="0.03,0.03", size="POW{1.7/10},POW{1.7/10}", extra=("-st", "CODON"))
    os.replace(os.path.join(HERE, "cds10.fa"), os.path.join(HERE, "cds10_true_codon_aln.fa"))
    os.replace(os.path.join(HERE, "cds10.unaligned.fa"), os.path.join(HERE, "cds10_cds.fa"))
    cds = clean_ids(os.path.join(HERE, "cds10_cds.fa"))
    prot = [SeqRecord(r.seq.translate(), id=r.id, description="") for r in cds]
    SeqIO.write(prot, os.path.join(HERE, "cds10_protein.fa"), "fasta")

    # mixed13: gene12 unaligned + 3 reverse complements + 1 non-homologous sequence
    alisim(os.path.join(HERE, "gene12"), "GTR{1.2,4.0,0.8,1.1,4.5,1.0}+F{0.28,0.22,0.24,0.26}+G4{0.6}",
           tree_file("gene12_true.nwk", GENE12_TREE), 1200, 101, indel="0.02,0.02")
    os.replace(os.path.join(HERE, "gene12.fa"), os.path.join(HERE, "gene12_true_aln.fa"))
    recs = clean_ids(os.path.join(HERE, "gene12.unaligned.fa"))
    os.remove(os.path.join(HERE, "gene12.unaligned.fa"))
    flip = {"Mus_musculus", "Felis_catus", "Xenopus_tropicalis"}
    out = []
    for r in recs:
        if r.id in flip:
            out.append(SeqRecord(r.seq.reverse_complement(), id=r.id, description=""))
        else:
            out.append(r)
    rng = random.Random(77)
    out.append(SeqRecord(Seq("".join(rng.choice("ACGT") for _ in range(1150))), id="Sample_X_contig7",
                         description=""))
    SeqIO.write(out, os.path.join(HERE, "mixed13.fa"), "fasta")

    # big1050
    alisim(os.path.join(HERE, "big1050"), "HKY{4.0}+F{0.3,0.2,0.2,0.3}+G4{0.5}", "RANDOM{yh/1050}", 1500, 404,
           indel="0.005,0.005", extra=("-rlen", "0.0005", "0.004", "0.02"))
    os.replace(os.path.join(HERE, "big1050.fa"), os.path.join(HERE, "big1050_true_aln.fa"))
    recs = clean_ids(os.path.join(HERE, "big1050.unaligned.fa"))
    os.remove(os.path.join(HERE, "big1050.unaligned.fa"))
    rng = random.Random(88)
    rng.shuffle(recs)
    ref, new = recs[:1000], recs[1000:]
    SeqIO.write(ref, os.path.join(HERE, "big1000_ref_unaligned.fa"), "fasta")
    frags = []
    for r in new:
        L = rng.randint(250, 450)
        s = rng.randint(0, len(r.seq) - L)
        frags.append(SeqRecord(r.seq[s:s + L], id=r.id + "_amp", description=""))
    SeqIO.write(frags, os.path.join(HERE, "new50_amplicons.fa"), "fasta")

    # twilight
    alisim(os.path.join(HERE, "twi8"), "LG+G4{1.0}", tree_file("twi8_true.nwk", TWI8_TREE), 250, 505,
           indel="0.02,0.02")
    os.replace(os.path.join(HERE, "twi8.fa"), os.path.join(HERE, "twi8_true_aln.fa"))
    os.replace(os.path.join(HERE, "twi8.unaligned.fa"), os.path.join(HERE, "twi8_unaligned.fa"))
    clean_ids(os.path.join(HERE, "twi8_unaligned.fa"))
    clean_ids(os.path.join(HERE, "prot15_unaligned.fa"))

    for f in os.listdir(HERE):
        if f.endswith(".log") or f.endswith(".treefile"):
            if f != "big1050.treefile":
                os.remove(os.path.join(HERE, f))
    print("SYNTHETIC data written to", HERE)


if __name__ == "__main__":
    main()
