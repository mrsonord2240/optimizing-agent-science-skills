"""Input 1 (Canonical): MCMCTree approximate-likelihood dating of an 8-taxon SYNTHETIC locus with
fossil-style soft calibrations, following the Skill: prior-only (usedata=0) -> usedata=3 (in.BV)
-> usedata=2, then specified-vs-effective-prior-vs-posterior per calibrated node."""
import json
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "common"))
import mct  # noqa: E402

DATA = os.path.join(HERE, "..", "..", "data")
truth = json.load(open(os.path.join(DATA, "species_truth.json")))["node_ages"]
clade_truth = {"AB": truth["AB"], "CD": truth["CD"], "ABCD": truth["ABCD"], "EF": truth["EF"],
               "GH": truth["GH"], "EFGH": truth["EFGH"], "ABCDEFGH": truth["root"]}

# fossil minimum 0.15 for (A,B) (true 0.20); soft joint bounds for (G,H) (true 0.45); root soft bounds
TREE = "8 1\n(((A,B)'L(0.15, 0.1, 1, 0.025)',(C,D)),((E,F),(G,H)'B(0.35, 0.55, 0.025, 0.025)'))'B(0.8, 1.2, 0.025, 0.025)';\n"
specified = {"AB": "L(0.15, 0.1, 1, 0.025)", "GH": "B(0.35, 0.55)", "ABCDEFGH": "B(0.8, 1.2)"}

res = {}
# 'post_asis' = the Skill's literal "usedata = 2"; 'post' = manual form "usedata = 2 in.BV" (pamlDOC p.48)
for step, usedata in (("prior", 0), ("bv", 3), ("post_asis", 2), ("post", "2 in.BV")):
    d = os.path.join(HERE, step)
    shutil.rmtree(d, ignore_errors=True)
    os.makedirs(d, exist_ok=True)
    shutil.copy(os.path.join(DATA, "loc1.phy"), d)
    open(os.path.join(d, "tree.nwk"), "w", newline="\n").write(TREE)
    mct.write_ctl(d, seqfile="loc1.phy", treefile="tree.nwk", usedata=usedata)
    if step.startswith("post"):
        shutil.copy(os.path.join(HERE, "bv", "out.BV"), os.path.join(d, "in.BV"))  # rename out.BV -> in.BV
    rc, out = mct.run(d)
    tail = open(os.path.join(d, "stdout.txt"), encoding="utf-8", errors="replace").read().strip().splitlines()[-1]
    print(f"[{step}] usedata={usedata} exit={rc} last line: {tail}")
    if step in ("prior", "post"):
        res[step] = {mct.node_map(d)[k]: v for k, v in mct.parse_times(d).items()}
shutil.rmtree(os.path.join(HERE, "post_try"), ignore_errors=True)

print(f"\n{'clade':10s} {'true':>5s} {'specified':24s} {'eff.prior mean [95% HPD]':28s} {'posterior mean [95% HPD]':28s} bracket")
for clade, t in clade_truth.items():
    p = res["prior"][clade]
    q = res["post"][clade]
    ok = q[1] <= t <= q[2]
    print(f"{clade:10s} {t:5.2f} {specified.get(clade, '-'):24s} {p[0]:.3f} [{p[1]:.3f}, {p[2]:.3f}]{'':8s} "
          f"{q[0]:.3f} [{q[1]:.3f}, {q[2]:.3f}]{'':8s} {'YES' if ok else 'NO'}")
json.dump(res, open(os.path.join(HERE, "in1_results.json"), "w"), indent=1)
