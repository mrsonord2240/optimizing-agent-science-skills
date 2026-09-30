"""Quantify the CTCF aggregate footprint from TOBIAS corrected bigwigs (independent of PlotAggregate's PDF).
Usage: check_ctcf_profile.py <run_out_dir> <png_out>"""
import glob, sys, numpy as np, pyBigWig
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
out, png = sys.argv[1], sys.argv[2]
bed = sorted(glob.glob(f"{out}/bindetect/CTCF_MA0139.2/beds/CTCF_MA0139.2_cond1_bound.bed"))[0]
sites = [l.split("\t")[:3] for l in open(bed) if l.strip()]
print("CTCF MA0139.2 cond1-bound sites:", len(sites))
fig, ax = plt.subplots(figsize=(6,3.5)); res = {}
for cond in ("cond1","cond2"):
    bw = pyBigWig.open(glob.glob(f"{out}/{cond}/*_corrected.bw")[0]); acc = []
    for c,s,e in sites:
        s,e = int(s),int(e); m=(s+e)//2
        if m-100<0: continue
        v = np.nan_to_num(np.array(bw.values(c,m-100,m+100)))
        acc.append(v)
    p = np.mean(acc,axis=0); res[cond]=p
    ax.plot(np.arange(-100,100),p,label=cond)
    core = p[100-10:100+10].mean(); flank = np.r_[p[:40],p[-40:]].mean()
    print(f"{cond}: n={len(acc)} core(+/-10bp) mean={core:.4f} flank(60-100bp) mean={flank:.4f} flank-core={flank-core:.3f}")
ax.set_xlabel("position from motif centre (bp)"); ax.set_ylabel("mean corrected Tn5 signal"); ax.legend(); ax.set_title("CTCF MA0139.2 (cond1-bound sites)")
fig.tight_layout(); fig.savefig(png,dpi=120)
# corrected = observed - expected (signed residual), so use a difference, not a ratio
depth = {c:(np.r_[p[:40],p[-40:]].mean() - p[90:110].mean()) for c,p in res.items()}
print("flank-minus-core depth:", {c:round(float(v),3) for c,v in depth.items()})
assert all(v>0.5 for v in depth.values()), "no footprint dip at CTCF"
print("PASS CTCF footprint dip: flank exceeds core by >0.5 signal units in both conditions")
