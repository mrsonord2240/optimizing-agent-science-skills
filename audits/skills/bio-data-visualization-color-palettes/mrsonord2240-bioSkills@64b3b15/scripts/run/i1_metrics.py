# Computed checks of the Skill's colour claims. Python via py.sh.
import numpy as np, matplotlib, matplotlib.pyplot as plt, json, itertools, os, sys
import colorspacious as cs
from matplotlib.colors import to_rgb, to_hex
from cmcrameri import cm as cmc
import colorcet
print("matplotlib", matplotlib.__version__, "colorspacious", cs.__name__)
import importlib.metadata as md
for p in ["cmcrameri","colorcet","colorspacious","seaborn","numpy"]: print(p, md.version(p))

def ramp(cmap, n=256):
    return cmap(np.linspace(0,1,n))[:,:3]
def lab(rgb): return cs.cspace_convert(rgb, "sRGB1", "CIELab")
def ucs(rgb): return cs.cspace_convert(rgb, "sRGB1", "CAM02-UCS")

cmaps = {
 "viridis": plt.get_cmap("viridis"), "magma": plt.get_cmap("magma"), "inferno": plt.get_cmap("inferno"),
 "plasma": plt.get_cmap("plasma"), "cividis": plt.get_cmap("cividis"), "turbo": plt.get_cmap("turbo"),
 "jet": plt.get_cmap("jet"), "rainbow(mpl)": plt.get_cmap("rainbow"), "hsv": plt.get_cmap("hsv"),
 "batlow": cmc.batlow, "lipari(colorcet?)": None, "vik": cmc.vik, "roma": cmc.roma, "bam": cmc.bam,
 "romaO": cmc.romaO, "vikO": cmc.vikO, "twilight": plt.get_cmap("twilight"),
 "RdBu_r": plt.get_cmap("RdBu_r"), "coolwarm": plt.get_cmap("coolwarm"),
}
try:
    cmaps["lipari"] = cmc.lipari
except Exception as e: print("lipari missing in cmcrameri", e)
cmaps.pop("lipari(colorcet?)")
rows = []
for name, cmap in cmaps.items():
    rgb = ramp(cmap)
    L = lab(rgb)[:,0]
    dL = np.diff(L)
    step = np.linalg.norm(np.diff(ucs(rgb),axis=0),axis=1)
    mono = (dL>=-1e-9).all() or (dL<=1e-9).all()
    # fraction of steps in the dominant direction
    frac = max((dL>0).mean(), (dL<0).mean())
    cv = step.std()/step.mean()
    rows.append((name, round(L[0],1), round(L[-1],1), round(L.min(),1), round(L.max(),1), mono, round(frac,3), round(cv,3)))
print("\n%-14s %6s %6s %6s %6s  %-6s %-6s %-6s" % ("cmap","L0","L1","Lmin","Lmax","monot","frac","stepCV"))
for r in rows: print("%-14s %6s %6s %6s %6s  %-6s %-6s %-6s" % r)
json.dump([dict(zip(["name","L0","L1","Lmin","Lmax","monotonic","frac","stepCV"],r)) for r in rows], open("i1_cmap_metrics.json","w"), default=bool)

# midpoint colour of diverging maps
print("\nDiverging midpoints (value at 0.5), RGB hex and L*, distance from pure white in CIELab:")
for n in ["vik","roma","bam","RdBu_r","coolwarm"]:
    c = cmaps[n](0.5)[:3]; l = lab(np.array([c]))[0]
    print(n, to_hex(c), "L*=%.1f"%l[0], "chroma=%.1f"%np.hypot(l[1],l[2]), "dE76 vs white=%.1f"%np.linalg.norm(l-lab(np.array([[1,1,1.]]))[0]))

# endpoint luminance similarity of the Skill's custom diverging (#0072B2 white #D55E00)
for h in ["#0072B2","#D55E00","#4DBBD5","#E64B35"]:
    print(h, "L*=%.1f"%lab(np.array([to_rgb(h)]))[0][0])

# Does 'colorblind' style exist in matplotlib?
print("\nmatplotlib styles with 'color':", [s for s in plt.style.available if "color" in s.lower()])
print("plain 'colorblind' style present:", "colorblind" in plt.style.available)
import seaborn as sns
print("seaborn colorblind palette:", [to_hex(c) for c in sns.color_palette("colorblind")])
# classic style default cmap (pre-2.0) vs current default
import matplotlib as mpl, pathlib
cl = pathlib.Path(mpl.get_data_path())/"stylelib"/"classic.mplstyle"
for line in cl.read_text(encoding="utf-8").splitlines():
    if line.startswith("image.cmap"): print("classic.mplstyle:", line)
print("current default image.cmap:", mpl.rcParamsDefault["image.cmap"])
