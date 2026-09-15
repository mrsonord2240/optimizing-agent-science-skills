"""Input 5 claim check (regression) + Input 9 (NEW) infinite-sites plot. SYNTHETIC data.
(b) '>0.35<0.55' vs B(0.35,0.55) prior-only on PAML 4.10.10 (fixed Skill: mis-parse only in 4.9b-4.9d)
(c) Input 9: posterior CI width vs posterior mean age across nodes, 1 locus (in5) vs 2 loci (in8):
    slope through the origin and R^2, as the Skill's infinite-sites plot describes."""
import json, os, re, shutil, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "common"))
import mct  # noqa: E402
DATA = os.path.join(HERE, "..", "data")
part = sys.argv[1]
if part == "claims":
    trees = {"BLU": "8 1\n(((A,B)'L(0.15, 0.1, 1, 0.025)',(C,D)),((E,F),(G,H)'B(0.35, 0.55, 0.025, 0.025)'))'B(0.8, 1.2, 0.025, 0.025)';\n",
             "gtlt": "8 1\n(((A,B)'>0.15',(C,D)),((E,F),(G,H)'>0.35<0.55'))'>0.8<1.2';\n"}
    for tag, tr in trees.items():
        d = os.path.join(HERE, "in5_claims", tag)
        shutil.rmtree(d, ignore_errors=True); os.makedirs(d)
        shutil.copy(os.path.join(DATA, "loc1.phy"), d)
        open(os.path.join(d, "tree.nwk"), "w", newline="\n").write(tr)
        mct.write_ctl(d, seqfile="loc1.phy", treefile="tree.nwk", usedata=0)
        rc, _ = mct.run(d)
        txt = open(os.path.join(d, "stdout.txt"), errors="replace").read()
        i = txt.find("Fossil calibration information used")
        blk = " | ".join(l.strip() for l in txt[i:].splitlines()[1:4]) if i >= 0 else "(none)"
        t = {mct.node_map(d)[k]: v for k, v in mct.parse_times(d).items()}
        print(f"[{tag}] exit {rc}; calibrations: {blk}; GH prior {t['GH']}; AB prior {t['AB']}")
else:
    for tag in ("in5", "in8"):
        r = json.load(open(os.path.join(HERE, tag, "results.json")))["post"]
        m = np.array([v[0] for v in r.values()]); w = np.array([v[2] - v[1] for v in r.values()])
        b = (m @ w) / (m @ m)
        r2 = 1 - ((w - b * m) ** 2).sum() / ((w - w.mean()) ** 2).sum()
        print(f"{tag}: nodes {len(m)}; CI width = {b:.3f} x mean age (through origin); R^2 = {r2:.3f}; "
              f"mean width {w.mean():.3f}")
