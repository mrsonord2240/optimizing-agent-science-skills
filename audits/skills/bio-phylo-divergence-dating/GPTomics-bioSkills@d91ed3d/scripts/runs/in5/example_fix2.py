"""Shipped examples/mcmctree_setup.py: which minimal edits make its control files + tree string run on PAML 4.10.10?
fix1 = BDparas flag; fix2 = fix1 + 'ntaxa ntree' header line in the tree file (the example never writes the tree file)."""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "common"))
import mct  # noqa: E402


def last(d):
    lines = [l for l in open(os.path.join(d, "stdout.txt"), encoding="utf-8", errors="replace").read().splitlines()
             if l.strip() and l.strip() != "--stderr--"]
    return lines[-1] if lines else ""


def calblock(d):
    t = open(os.path.join(d, "stdout.txt"), encoding="utf-8", errors="replace").read()
    i = t.find("Fossil calibration information used")
    return " | ".join(l.strip() for l in t[i:].splitlines()[1:4]) if i >= 0 else "(none)"


src = os.path.join(HERE, "ex_prior")
steps = [("fix2_prior", "mcmctree_prior.ctl", None), ("fix2_bv", "mcmctree_step1_bv.ctl", None),
         ("fix2_post_asis", "mcmctree_step2_post.ctl", None),
         ("fix3_post_inBV", "mcmctree_step2_post.ctl", ("usedata = 2", "usedata = 2 in.BV"))]
for tag, ctl, extra in steps:
    d = os.path.join(HERE, tag)
    shutil.rmtree(d, ignore_errors=True)
    os.makedirs(d)
    shutil.copy(os.path.join(src, "alignment.phy"), d)
    tree = open(os.path.join(src, "calibrated_tree.nwk")).read()
    open(os.path.join(d, "calibrated_tree.nwk"), "w", newline="\n").write("5 1\n" + tree)
    t = open(os.path.join(HERE, "..", "examples", "asis_ctl", ctl)).read()
    t = t.replace("BDparas = 1 1 0.1", "BDparas = 1 1 0.1 m")
    t = t.replace("burnin = 50000", "burnin = 5000").replace("nsample = 20000", "nsample = 5000")  # speed only
    if extra:
        t = t.replace(*extra)
    open(os.path.join(d, ctl), "w", newline="\n").write(t)
    if "post" in tag and os.path.exists(os.path.join(HERE, "fix2_bv", "out.BV")):
        shutil.copy(os.path.join(HERE, "fix2_bv", "out.BV"), os.path.join(d, "in.BV"))
    rc, _ = mct.run(d, ctl=ctl, timeout=900)
    print(f"[{tag}] exit={rc} :: {last(d)}")
    print("    calibrations:", calblock(d))
    print("    files:", sorted(os.listdir(d)))
