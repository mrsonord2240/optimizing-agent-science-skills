"""Input 7 (Adversarial): PI wants the (G,H) fossil (0.40 = 40 Ma; true SYNTHETIC age 0.45) used as a fixed
point age. Compare a near-point calibration with the Skill's soft-minimum encoding on the same in.BV."""
import json
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "common"))
import mct  # noqa: E402

DATA = os.path.join(HERE, "..", "..", "data")
BV = os.path.join(HERE, "..", "in1", "bv", "out.BV")  # branch-length MLEs depend only on topology + data
truth = json.load(open(os.path.join(DATA, "species_truth.json")))["node_ages"]
CT = {"AB": truth["AB"], "CD": truth["CD"], "ABCD": truth["ABCD"], "EF": truth["EF"], "GH": truth["GH"],
      "EFGH": truth["EFGH"], "ABCDEFGH": truth["root"]}
CAL = {"point": "B(0.399, 0.401, 1e-300, 1e-300)", "softmin": "L(0.40, 0.1, 1, 0.025)"}
res = {}
for tag, cal in CAL.items():
    tree = f"8 1\n(((A,B),(C,D)),((E,F),(G,H)'{cal}'))'B(0.8, 1.2, 0.025, 0.025)';\n"
    for step, ud in (("prior", 0), ("post", "2 in.BV")):
        d = os.path.join(HERE, f"{tag}_{step}")
        shutil.rmtree(d, ignore_errors=True)
        os.makedirs(d)
        shutil.copy(os.path.join(DATA, "loc1.phy"), d)
        shutil.copy(BV, os.path.join(d, "in.BV"))
        open(os.path.join(d, "tree.nwk"), "w", newline="\n").write(tree)
        mct.write_ctl(d, seqfile="loc1.phy", treefile="tree.nwk", usedata=ud)
        rc, _ = mct.run(d)
        nm = mct.node_map(d)
        res[f"{tag}_{step}"] = {nm[k]: v for k, v in mct.parse_times(d).items()}
        print(f"[{tag} {step}] calibration {cal} exit={rc}")
print(f"\n{'clade':9s} {'true':>5s} {'point: post mean [HPD]':>28s} {'soft-min: post mean [HPD]':>28s}")
for c, t in CT.items():
    p, s = res["point_post"][c], res["softmin_post"][c]
    fp = "" if p[1] <= t <= p[2] else " MISS"
    fs = "" if s[1] <= t <= s[2] else " MISS"
    print(f"{c:9s} {t:5.2f}  {p[0]:.3f} [{p[1]:.3f},{p[2]:.3f}]{fp:5s}   {s[0]:.3f} [{s[1]:.3f},{s[2]:.3f}]{fs}")
json.dump(res, open(os.path.join(HERE, "in7_results.json"), "w"), indent=1)
