"""Independent assertions on reaudit-run/rt/{A,B,C,D,E,N}; run in a python with numpy, pandas, pymupdf (live env bio-atac-seq-footprinting)."""
import glob, os, sys
import numpy as np, pandas as pd, fitz
R = "/mnt/openscience/audit-envs/bio-atac-seq-footprinting/reaudit-run/rt"
L = "/mnt/openscience/audits/bio-atac-seq-footprinting/reaudit-run"
ok = True
def check(name, cond, detail=""):
    global ok; ok &= bool(cond); print(("PASS " if cond else "FAIL ") + name, detail)
def log(n): return open(f"{L}/logs/r2_{n}.log", errors="replace").read()
def load_prof(out, cond):
    prof = {}
    for line in open(f"{out}/validation/ctcf_{cond}_aggregate.txt"):
        if line.startswith("#") or not line.strip(): continue
        sig, reg, vals = line.rstrip("\n").split("\t")
        prof[(sig, reg)] = np.array(vals.split(","), float)
    return prof
def dip(p): return np.r_[p[:len(p)//5], p[-len(p)//5:]].mean() - p[len(p)//2-10:len(p)//2+10].mean()

a = log("A"); check("A exit 0", "A rc=0" in a)
res = pd.read_csv(f"{R}/A/bindetect/bindetect_results.txt", sep="\t")
exp = res[res.cond1_cond2_pvalue <= 0.05].assign(a=lambda d: d.cond1_cond2_change.abs()).sort_values("a", ascending=False).head(20)
rows = [l.split("\t") for l in a.split("=== Top differential motifs")[1].split("\n")[1:] if l.count("\t") == 2]
check("A summary == independent |change| ranking (p<=0.05)", [r[0] for r in rows] == list(exp.output_prefix), f"{len(rows)} rows, top {rows[0][0]}")
g = res.set_index("output_prefix")
for k, sgn in (("GATA1_MA0035.5", -1), ("IRF4_MA1419.2", 1), ("EBF1_MA0154.4", 1)):
    if k in g.index: check(f"A {k} change sign", np.sign(g.loc[k, "cond1_cond2_change"]) == sgn, f'{g.loc[k,"cond1_cond2_change"]:.3f}')
print("  all prefixes:", list(g.index))
n_ctcf = int(res[res.output_prefix.str.startswith("CTCF")].iloc[0]["total_tfbs"])
for cond in ("cond1", "cond2"):
    pdf = f"{R}/A/validation/ctcf_{cond}_aggregate.pdf"
    check(f"A {cond} pdf/txt non-empty", os.path.getsize(pdf) > 10000)
    fitz.open(pdf)[0].get_pixmap(dpi=90).save(f"{L}/out/r2_A_ctcf_{cond}.png")
    p = load_prof(f"{R}/A", cond)
    for sig in ("uncorrected", "corrected"):
        print(f"  A {cond} {sig:11s} flank-core: bound={dip(p[(sig,'bound')]):6.2f} unbound={dip(p[(sig,'unbound')]):6.2f} all={dip(p[(sig,'all')]):6.2f}")
    b, u = p[("corrected", "bound")], p[("corrected", "unbound")]
    check(f"A {cond} corrected bound dip > unbound dip + 1", dip(b) > dip(u) + 1)
    m = len(b)//2; check(f"A {cond} bound minimum within 10 bp of centre", abs(int(np.argmin(b[m-30:m+30])) - 30) <= 10)
for n, want in (("B", 3), ("C", 0)):
    t = log(n); check(f"{n} rc {want}", f"{n} rc={want}" in t)
    check(f"{n} WARNING names missing CTCF and validation empty", "WARNING: no CTCF motif" in t and len(os.listdir(f"{R}/{n}/validation")) == 0)
tb = log("B"); check("B error line + differential table still printed", "ERROR: no CTCF positive control" in tb and "IRF4" in tb)
check("C no ERROR line", "ERROR" not in log("C"))
td = log("D"); check("D missing input rc 2 and no outdir created", "D rc=2" in td and "input not found" in td and not os.path.exists(f"{R}/Dout"))
te = log("E"); check("E spaces in all paths rc 0", "E rc=0" in te)
check("E outputs in 'out dir', no stray out/dir", os.path.isdir(f"{R}/out dir/bindetect") and not os.path.exists(f"{R}/out") and not os.path.exists(f"{R}/dir"))
ea = pd.read_csv(f"{R}/out dir/bindetect/bindetect_results.txt", sep="\t")
check("E results identical to A", np.allclose(ea.set_index("output_prefix").cond1_cond2_change, g.cond1_cond2_change.reindex(ea.output_prefix).values), "")
# negative control: corrected == uncorrected
tn = log("N"); print("  N rc:", "N rc=0" in tn, "| warning/error lines:", [l for l in tn.splitlines() if l.startswith(("WARNING","ERROR"))])
for cond in ("cond1", "cond2"):
    p = load_prof(f"{R}/N", cond)
    print(f"  N {cond} corrected(=uncorrected) flank-core bound={dip(p[('corrected','bound')]):.2f} unbound={dip(p[('corrected','unbound')]):.2f} | A corrected bound={dip(load_prof(R+'/A',cond)[('corrected','bound')]):.2f}")
na = pd.read_csv(f"{R}/N/bindetect/bindetect_results.txt", sep="\t").set_index("output_prefix")
print("  N vs A CTCF_MA0139.2 change:", na.loc["CTCF_MA0139.2","cond1_cond2_change"], g.loc["CTCF_MA0139.2","cond1_cond2_change"])
print("ALL PASS" if ok else "SOME FAILED"); sys.exit(0 if ok else 1)
