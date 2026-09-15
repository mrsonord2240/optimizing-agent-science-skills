"""SYNTHETIC data generator for the bio-phylo-divergence-dating audit (2026-09-15).

Every file written here is simulated; nothing is real sequence data.

sets
  species  8-taxon ultrametric TIME tree (ages in units of 100 Myr), branch rates drawn
           independently from a lognormal around a known mean rate per locus
           (relaxed clock, known truth); two loci simulated with IQ-TREE 2.4.0 AliSim.
  virus    30 heterochronous tips sampled 2000-2020 under a strict clock of 2e-3
           subs/site/yr (serial coalescent), 3000 bp.
  nosig    30 tips sampled within 0.4 yr (2019.0-2019.4), rate 2e-3, deep coalescent
           (theta 20 yr): negligible temporal signal by construction.

usage: python make_data.py OUTDIR
"""
import json
import math
import os
import random
import subprocess
import sys

IQTREE = r"F:\OpenScience\audit-envs\molecular-phylogenetics-analyst\tools\bin\iqtree2.exe"

# true node ages (100 Myr units)
AGES = {"AB": 0.20, "CD": 0.35, "ABCD": 0.60, "EF": 0.15, "GH": 0.45, "EFGH": 0.80, "root": 1.00}
TOPO = "(((A,B)AB,(C,D)CD)ABCD,((E,F)EF,(G,H)GH)EFGH)root;"
PARENT = {"A": "AB", "B": "AB", "C": "CD", "D": "CD", "E": "EF", "F": "EF", "G": "GH", "H": "GH",
          "AB": "ABCD", "CD": "ABCD", "EF": "EFGH", "GH": "EFGH", "ABCD": "root", "EFGH": "root"}
LOCI = {"loc1": {"rate": 0.25, "len": 4000, "model": "HKY{4.0}+F{0.3,0.2,0.2,0.3}+G4{0.5}", "seed": 11},
        "loc2": {"rate": 0.10, "len": 3000, "model": "HKY{3.0}+F{0.25,0.25,0.25,0.25}+G4{0.8}", "seed": 12}}


def write(path, text):
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)


def alisim(prefix, model, tree_file, length, seed):
    cmd = [IQTREE, "--alisim", prefix, "-m", model, "-t", tree_file, "--length", str(length),
           "--seed", str(seed), "-af", "fasta", "-redo"]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(r.stdout[-2000:] + r.stderr[-2000:])


def age(n):
    return AGES.get(n, 0.0)


def phylo_newick(bl):
    def sub(n):
        kids = [k for k, p in PARENT.items() if p == n]
        if not kids:
            return f"{n}:{bl[n]:.6f}"
        inner = ",".join(sub(k) for k in sorted(kids))
        return f"({inner}):{bl[n]:.6f}" if n != "root" else f"({inner});"
    return sub("root")


def read_fasta(p):
    seqs, name = {}, None
    for line in open(p, encoding="utf-8"):
        line = line.strip()
        if line.startswith(">"):
            name = line[1:].split()[0]
            seqs[name] = []
        elif name:
            seqs[name].append(line)
    return {k: "".join(v) for k, v in seqs.items()}


def make_species(out):
    rng = random.Random(2026)
    truth = {"units": "100 Myr", "node_ages": AGES, "loci": {}}
    phy_blocks = []
    for loc, cfg in LOCI.items():
        bl = {}
        rates = {}
        for n, p in PARENT.items():
            r = cfg["rate"] * math.exp(rng.gauss(-0.5 * 0.2 ** 2, 0.2))  # lognormal, sd(log)=0.2, mean=rate
            rates[n] = r
            bl[n] = (age(p) - age(n)) * r
        nwk = phylo_newick(bl)
        tf = os.path.join(out, f"{loc}_true_subs.nwk")
        write(tf, nwk + "\n")
        alisim(os.path.join(out, loc), cfg["model"], tf, cfg["len"], cfg["seed"])
        seqs = read_fasta(os.path.join(out, f"{loc}.fa"))
        block = f"{len(seqs)} {cfg['len']}\n" + "".join(f"{k}  {v}\n" for k, v in sorted(seqs.items()))
        write(os.path.join(out, f"{loc}.phy"), block)
        phy_blocks.append(block)
        truth["loci"][loc] = {"mean_rate_per_100Myr": cfg["rate"], "branch_rates": rates, "length": cfg["len"],
                              "model": cfg["model"]}
    write(os.path.join(out, "species2loci.phy"), "\n".join(phy_blocks))
    write(os.path.join(out, "species_topology.nwk"), TOPO + "\n")
    tt = "(((A:0.2,B:0.2):0.4,(C:0.35,D:0.35):0.25):0.4,((E:0.15,F:0.15):0.65,(G:0.45,H:0.45):0.35):0.2);"
    write(os.path.join(out, "species_timetree_true.nwk"), tt + "\n")
    write(os.path.join(out, "species_truth.json"), json.dumps(truth, indent=1))


def serial_coalescent(rng, dates, theta, rate):
    present = max(dates)
    names = [f"V{i+1:02d}_{d:.2f}" for i, d in enumerate(dates)]
    events = sorted(((present - d, names[i]) for i, d in enumerate(dates)), key=lambda x: x[0])
    active, t, idx = [], 0.0, 0
    while idx < len(events) or len(active) > 1:
        k = len(active)
        wait = rng.expovariate(k * (k - 1) / 2 / theta) if k >= 2 else float("inf")
        nxt = events[idx][0] if idx < len(events) else float("inf")
        if t + wait < nxt:
            t += wait
            a, b = rng.sample(range(k), 2)
            (la, ha), (lb, hb) = active[a], active[b]
            for j in sorted((a, b), reverse=True):
                active.pop(j)
            active.append((f"({la}:{(t-ha)*rate:.6f},{lb}:{(t-hb)*rate:.6f})", t))
        else:
            t = nxt
            active.append((events[idx][1], t))
            idx += 1
    return active[0][0] + ";", present - active[0][1], names


def make_virus(out, tag, lo, hi, theta, seed, rate=2.0e-3, n=30, length=3000):
    rng = random.Random(seed)
    dates = sorted(round(rng.uniform(lo, hi), 3) for _ in range(n))
    tree, tmrca, names = serial_coalescent(rng, dates, theta, rate)
    write(os.path.join(out, f"{tag}_true.nwk"), tree + "\n")
    alisim(os.path.join(out, tag), "HKY{4.0}+F{0.3,0.2,0.2,0.3}+G4{1.0}", os.path.join(out, f"{tag}_true.nwk"),
           length, seed + 1)
    os.replace(os.path.join(out, f"{tag}.fa"), os.path.join(out, f"{tag}_aln.fa"))
    write(os.path.join(out, f"{tag}_dates.tsv"), "".join(f"{nm}\t{d:.3f}\n" for nm, d in zip(names, dates)))
    write(os.path.join(out, f"{tag}_truth.json"),
          json.dumps({"synthetic": True, "strict_clock_rate": rate, "true_tmrca": round(tmrca, 3),
                      "sampling_span": [lo, hi], "theta_years": theta}, indent=1))


if __name__ == "__main__":
    outdir = sys.argv[1]
    os.makedirs(outdir, exist_ok=True)
    make_species(outdir)
    make_virus(outdir, "virus", 2000.0, 2020.0, 4.0, 505)
    make_virus(outdir, "nosig", 2019.0, 2019.4, 20.0, 707)
    for f in os.listdir(outdir):
        if f.endswith(".log"):
            os.remove(os.path.join(outdir, f))
    print("SYNTHETIC data written to", outdir)
