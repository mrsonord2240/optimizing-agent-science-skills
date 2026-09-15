"""Inputs 5 and 8 (auditor driver around the SHIPPED helper, imported unmodified from the fork):
  in5: helper pipeline on loc1.phy (1 locus) with the Input-1 calibrated tree  -> prior/bv/post
  in8: helper pipeline on species2loci.phy (2 loci) with ndata = 2 passed through **ctl_options
Then specified / effective prior / posterior tables via the audit's out.txt parser. SYNTHETIC data."""
import json, os, shutil, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, r"F:\OpenScience\external\mrsonord2240__bioSkills\phylogenetics\divergence-dating\examples")
sys.path.insert(0, os.path.join(HERE, "common"))
import mcmctree_setup as ms  # noqa: E402  (shipped helper, read-only import)
import mct  # noqa: E402

os.environ["PATH"] = mct.BIN + os.pathsep + os.environ["PATH"]
DATA = os.path.join(HERE, "..", "data")
truth = json.load(open(os.path.join(DATA, "species_truth.json")))["node_ages"]
CT = {"AB": truth["AB"], "CD": truth["CD"], "ABCD": truth["ABCD"], "EF": truth["EF"], "GH": truth["GH"],
      "EFGH": truth["EFGH"], "ABCDEFGH": truth["root"]}
which = sys.argv[1]
tag, phy, extra = {"in5": ("in5", "loc1.phy", {}), "in8": ("in8", "species2loci.phy", {"ndata": 2})}[which]
out = os.path.join(HERE, tag)
shutil.rmtree(out, ignore_errors=True); os.makedirs(out)
shutil.copy(os.path.join(DATA, phy), out)
newick = "(((A,B)ab,(C,D)),((E,F),(G,H)gh))root;"
cal = {"ab": ms.format_calibration("L", 0.15, 0.1, 1, 0.025), "gh": ms.format_calibration("B", 0.35, 0.55, 0.025, 0.025)}
calibrated = ms.build_calibrated_tree(newick, cal)
calibrated = calibrated.replace(")root;", ")'B(0.8, 1.2, 0.025, 0.025)';")
tree = ms.write_tree_file(os.path.join(out, "calibrated.tre"), calibrated, 8)
print("tree file:", open(tree).read().strip().replace("\n", " | "))
dirs = ms.generate_prior_and_posterior_configs(os.path.join(out, phy), tree, out, rgene_gamma="2 8 1", **extra)
print("ctl (post):", " ; ".join(l for l in open(os.path.join(dirs["post"], "mcmctree.ctl")).read().splitlines()
                               if l.split("=")[0].strip() in ("usedata", "ndata", "BDparas", "RootAge", "seed", "mcmcfile")))
try:
    ms.run_pipeline(dirs)
    print("run_pipeline: OK")
except Exception as e:
    print("run_pipeline FAILED:", type(e).__name__, e)
for d in dirs.values():
    so = os.path.join(d, "out.txt")
    print(os.path.basename(d), "out.txt" if os.path.exists(so) else "NO out.txt", "| files:", sorted(os.listdir(d))[:12])
if os.path.exists(os.path.join(dirs["post"], "in.BV")):
    print("in.BV bytes:", os.path.getsize(os.path.join(dirs["post"], "in.BV")))
res = {}
for step in ("prior", "post"):
    try:
        res[step] = {mct.node_map(dirs[step])[k]: v for k, v in mct.parse_times(dirs[step]).items()}
    except Exception as e:
        print(step, "parse failed:", e)
if len(res) == 2:
    print(f"{'clade':10s} {'true':>5s}  eff.prior mean [HPD]        posterior mean [HPD]        in HPD")
    for c, t in CT.items():
        p, q = res["prior"][c], res["post"][c]
        print(f"{c:10s} {t:5.2f}  {p[0]:.3f} [{p[1]:.3f},{p[2]:.3f}]   {q[0]:.3f} [{q[1]:.3f},{q[2]:.3f}]   {q[1] <= t <= q[2]}")
    json.dump(res, open(os.path.join(out, "results.json"), "w"), indent=1)
