"""Input 5 (Stress): two-locus SYNTHETIC MCMCTree analysis with three calibrations, clock=2 vs clock=3,
two independent chains each, plus the Skill's specific claims:
  (a) shipped examples/mcmctree_setup.py control files run as written (after pointing them at data)
  (b) '>'/'<' calibration notation 'silently ignored' vs B()/L()
  (c) RootAge = <1.0 (unquoted, as the shipped example writes it) vs U(1.0)
"""
import json
import os
import re
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "common"))
import mct  # noqa: E402

DATA = os.path.join(HERE, "..", "..", "data")
EX = os.path.join(HERE, "..", "examples", "asis_ctl")
truth = json.load(open(os.path.join(DATA, "species_truth.json")))["node_ages"]
CT = {"AB": truth["AB"], "CD": truth["CD"], "ABCD": truth["ABCD"], "EF": truth["EF"], "GH": truth["GH"],
      "EFGH": truth["EFGH"], "ABCDEFGH": truth["root"]}


def fossil_block(d):
    txt = open(os.path.join(d, "stdout.txt"), encoding="utf-8", errors="replace").read()
    m = re.search(r"Fossil calibration information used\.\s*\n(.*?)(?:\n\s*\n|\d+ bytes)", txt, re.S)
    return m.group(1).strip() if m else "(no calibration block printed)"


def last(d):
    lines = [l for l in open(os.path.join(d, "stdout.txt"), encoding="utf-8", errors="replace").read().splitlines()
             if l.strip() and l.strip() != "--stderr--"]
    return lines[-1] if lines else ""


def prep(d, phy, tree, **kw):
    shutil.rmtree(d, ignore_errors=True)
    os.makedirs(d)
    shutil.copy(os.path.join(DATA, phy), d)
    open(os.path.join(d, "tree.nwk"), "w", newline="\n").write(tree)
    mct.write_ctl(d, seqfile=phy, treefile="tree.nwk", **kw)


def summary(d):
    nm = mct.node_map(d)
    return {nm[k]: v for k, v in mct.parse_times(d).items()}


print("=== (a) shipped example control files, as written ===")
# 5-taxon alignment named as in the example's tree (SYNTHETIC: taxa A,B,C,E,G of loc1 renamed)
seqs = {l.split()[0]: l.split()[1] for l in open(os.path.join(DATA, "loc1.phy")).read().splitlines()[1:] if l.strip()}
ren = {"human": "A", "chimp": "B", "gorilla": "C", "mouse": "E", "rat": "G"}
for tag, ctl in (("ex_prior", "mcmctree_prior.ctl"), ("ex_bv", "mcmctree_step1_bv.ctl"),
                 ("ex_post", "mcmctree_step2_post.ctl")):
    d = os.path.join(HERE, tag)
    shutil.rmtree(d, ignore_errors=True)
    os.makedirs(d)
    with open(os.path.join(d, "alignment.phy"), "w", newline="\n") as fh:
        fh.write(f"5 {len(seqs['A'])}\n" + "".join(f"{k}  {seqs[v]}\n" for k, v in ren.items()))
    # the example prints this tree but never writes it; written verbatim, with and without the PAML header line
    tree = "((((human, chimp) 'B(0.06, 0.08, 0.025, 0.025)', gorilla) 'L(0.12, 0.05, 1.0, 0.025)', mouse), rat);"
    open(os.path.join(d, "calibrated_tree.nwk"), "w", newline="\n").write(tree + "\n")
    shutil.copy(os.path.join(EX, ctl), os.path.join(d, ctl))
    if tag == "ex_post" and os.path.exists(os.path.join(HERE, "ex_bv", "out.BV")):
        shutil.copy(os.path.join(HERE, "ex_bv", "out.BV"), os.path.join(d, "in.BV"))
    rc, _ = mct.run(d, ctl=ctl, timeout=600)
    print(f"[{tag}] {ctl} as written: exit={rc} :: {last(d)}")

# minimal fix 1: BDparas flag only
d = os.path.join(HERE, "ex_prior_fix1")
shutil.rmtree(d, ignore_errors=True)
shutil.copytree(os.path.join(HERE, "ex_prior"), d)
t = open(os.path.join(d, "mcmctree_prior.ctl")).read().replace("BDparas = 1 1 0.1", "BDparas = 1 1 0.1 m")
t = t.replace("burnin = 50000", "burnin = 2000").replace("nsample = 20000", "nsample = 2000")
open(os.path.join(d, "mcmctree_prior.ctl"), "w", newline="\n").write(t)
rc, _ = mct.run(d, ctl="mcmctree_prior.ctl", timeout=600)
print(f"[ex_prior_fix1] + BDparas flag (tree file without 'ntaxa ntree' header): exit={rc} :: {last(d)}")
print("   calibrations read:", fossil_block(d).replace("\n", " | "))

print("\n=== (b) '>'/'<' notation vs B()/L() (prior only, usedata=0) ===")
trees = {
    "BLU": "8 1\n(((A,B)'L(0.15)',(C,D)),((E,F),(G,H)'B(0.35, 0.55)'))'B(0.8, 1.2)';\n",
    "gtlt": "8 1\n(((A,B)'>0.15',(C,D)),((E,F),(G,H)'>0.35<0.55'))'>0.8<1.2';\n",
}
nota = {}
for tag, tree in trees.items():
    d = os.path.join(HERE, f"nota_{tag}")
    prep(d, "loc1.phy", tree, usedata=0)
    rc, _ = mct.run(d)
    nota[tag] = summary(d)
    print(f"[{tag}] exit={rc}; calibrations read: {fossil_block(d).replace(chr(10), ' | ')}")
for c in ("AB", "GH", "ABCDEFGH", "EF"):
    a, b = nota["BLU"][c], nota["gtlt"][c]
    print(f"   {c:9s} B/L/U prior {a[0]:.3f} [{a[1]:.3f},{a[2]:.3f}]   >/< prior {b[0]:.3f} [{b[1]:.3f},{b[2]:.3f}]")

print("\n=== (c) RootAge = <1.0 (unquoted, as in the shipped example) vs U(1.0) ===")
for tag, ra in (("ra_lt", "<1.0"), ("ra_U", "U(1.0)")):
    d = os.path.join(HERE, tag)
    prep(d, "loc1.phy", "8 1\n(((A,B)'L(0.15)',(C,D)),((E,F),(G,H)'B(0.35, 0.55)'));\n", usedata=0, rootage=ra)
    rc, _ = mct.run(d)
    s = summary(d)["ABCDEFGH"]
    print(f"[{tag}] RootAge = {ra}: exit={rc}; root effective prior {s[0]:.3f} [{s[1]:.3f},{s[2]:.3f}]; "
          f"calibrations: {fossil_block(d).replace(chr(10), ' | ')}")

print("\n=== (d) two loci, clock 2 vs 3, two chains each ===")
TREE = "8 1\n(((A,B)'L(0.15, 0.1, 1, 0.025)',(C,D)),((E,F),(G,H)'B(0.35, 0.55, 0.025, 0.025)'))'B(0.8, 1.2, 0.025, 0.025)';\n"
d = os.path.join(HERE, "bv2")
prep(d, "species2loci.phy", TREE, usedata=3, ndata=2, rgene="2 12 1")
rc, _ = mct.run(d)
print(f"[bv2] usedata=3 ndata=2 exit={rc}")
d = os.path.join(HERE, "prior2")
prep(d, "species2loci.phy", TREE, usedata=0, ndata=2, rgene="2 12 1")
mct.run(d)
prior = summary(d)
runs = {}
for clock in (2, 3):
    for seed in (11, 22):
        d = os.path.join(HERE, f"c{clock}_s{seed}")
        prep(d, "species2loci.phy", TREE, usedata="2 in.BV", ndata=2, clock=clock, seed=seed, rgene="2 12 1")
        shutil.copy(os.path.join(HERE, "bv2", "out.BV"), os.path.join(d, "in.BV"))
        rc, out = mct.run(d)
        runs[(clock, seed)] = summary(d)
        acc = re.findall(r"\n\s*100%\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)", out)
        print(f"[clock={clock} seed={seed}] exit={rc}")
print(f"{'clade':9s} {'true':>5s} {'eff.prior':>22s} " + " ".join(f"{'c%d s%d' % k:>22s}" for k in runs))
brk = {k: 0 for k in runs}
for c, t in CT.items():
    row = f"{c:9s} {t:5.2f} {prior[c][0]:.3f}[{prior[c][1]:.2f},{prior[c][2]:.2f}]  "
    for k, s in runs.items():
        v = s[c]
        ok = v[1] <= t <= v[2]
        brk[k] += ok
        row += f" {v[0]:.3f}[{v[1]:.2f},{v[2]:.2f}]{'*' if not ok else ' '}"
    print(row)
print("true age inside 95% HPD (of 7):", {f"clock{k[0]}_seed{k[1]}": v for k, v in brk.items()})
for clock in (2, 3):
    diffs = [abs(runs[(clock, 11)][c][0] - runs[(clock, 22)][c][0]) for c in CT]
    print(f"clock={clock}: max |mean age difference| between chains = {max(diffs):.4f}")
json.dump({"prior": prior, "runs": {f"{k[0]}_{k[1]}": v for k, v in runs.items()}, "notation": nota},
          open(os.path.join(HERE, "in5_results.json"), "w"), indent=1)
