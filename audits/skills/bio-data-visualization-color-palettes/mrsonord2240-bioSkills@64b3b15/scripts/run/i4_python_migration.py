# Input 4: migrate a spatial-expression matplotlib figure from jet to a perceptually-uniform map; diverging + cyclic data.  SYNTHETIC field.
import numpy as np, matplotlib, matplotlib.pyplot as plt, json
from cmcrameri import cm
import colorspacious as cs
from scipy.stats import spearmanr
from matplotlib.colors import to_hex
rng = np.random.default_rng(20260920)
yy, xx = np.mgrid[0:120, 0:160]
data = 8*np.exp(-(((xx-45)/22)**2+((yy-40)/16)**2)) + 4*np.exp(-(((xx-115)/12)**2+((yy-80)/25)**2)) + 0.4*xx/160 + rng.normal(0,0.15,xx.shape)
np.save("../data/synthetic_spatial_expr.npy", data)   # SYNTHETIC
print("data range %.2f..%.2f"%(data.min(), data.max()))
maps = {"jet":plt.get_cmap("jet"), "rainbow":plt.get_cmap("rainbow"), "turbo":plt.get_cmap("turbo"), "viridis":plt.get_cmap("viridis"), "cividis":plt.get_cmap("cividis"), "batlow (cm.batlow)":cm.batlow}
norm = plt.Normalize(data.min(), data.max())
fig, axs = plt.subplots(2,3, figsize=(13,7), constrained_layout=True)
print("\nRank correlation between data value and the LUMINANCE (CIELab L*) of the rendered pixel: 1.0 = grayscale preserves order")
res={}
for ax,(n,c) in zip(axs.ravel(), maps.items()):
    im = ax.imshow(data, cmap=c, norm=norm); ax.set_title(n); ax.axis("off"); fig.colorbar(im, ax=ax, fraction=.04)
    rgb = c(norm(data))[...,:3].reshape(-1,3)
    L = cs.cspace_convert(rgb,"sRGB1","CIELab")[:,0]
    rho = spearmanr(data.ravel(), L).statistic; res[n]=round(float(rho),3)
    print("%-20s rho(data, L*) = %.3f"%(n, rho))
fig.savefig("../figs/i4_jet_migration.png", dpi=110); plt.close(fig)
json.dump(res, open("i4_rho.json","w"))

# ---- Skill python blocks verbatim (data = the field, diverging data below)
plt.imshow(data, cmap=cm.batlow); plt.close()              # sequential
sig = data - data.mean()                                    # signed, skewed
vmax = max(abs(sig.min()), abs(sig.max()))
fig,axs=plt.subplots(1,3,figsize=(15,4),constrained_layout=True)
for ax,(t,kw,cmp) in zip(axs,[("vik, vmin/vmax = data min/max (the Skill's error)",dict(vmin=sig.min(),vmax=sig.max()),cm.vik),("vik symmetric (Skill fix)",dict(vmin=-vmax,vmax=vmax),cm.vik),("RdBu_r, vmin=-2 vmax=2 (Skill block)",dict(vmin=-2,vmax=2),plt.get_cmap("RdBu_r"))]):
    im=ax.imshow(sig,cmap=cmp,**kw); ax.set_title(t,fontsize=9); ax.axis("off"); fig.colorbar(im,ax=ax,fraction=.04)
    lo,hi=kw["vmin"],kw["vmax"]; frac0=(0-lo)/(hi-lo)
    print("%-52s zero maps to %.3f of the colour range -> %s (centre colour %s)"%(t,frac0,to_hex(cmp(frac0)),to_hex(cmp(0.5))))
fig.savefig("../figs/i4_diverging_python.png",dpi=110); plt.close(fig)
print("share of pixels beyond +-2 on the RdBu_r +-2 block (silently saturated):", round(float((np.abs(sig)>2).mean()),3))

# ---- cyclic: phase data 0..2pi; seam must be invisible
phase = np.arctan2(yy-60, xx-80) % (2*np.pi)
print("\nCyclic maps: colour distance across the seam (value 0 vs 2pi-eps), CAM02-UCS dE; lower = seamless")
fig,axs=plt.subplots(1,4,figsize=(16,4),constrained_layout=True)
for ax,(n,c) in zip(axs,{"viridis (linear seq; Skill: avoid)":plt.get_cmap("viridis"),"twilight (mpl, Skill list)":plt.get_cmap("twilight"),"cm.romaO":cm.romaO,"cm.vikO":cm.vikO}.items()):
    a=cs.cspace_convert(np.array([c(0.0)[:3]]),"sRGB1","CAM02-UCS"); b=cs.cspace_convert(np.array([c(1.0)[:3]]),"sRGB1","CAM02-UCS")
    print("%-36s seam dE = %.1f  (%s -> %s)"%(n,np.linalg.norm(a-b),to_hex(c(0.0)),to_hex(c(1.0))))
    ax.imshow(phase,cmap=c,vmin=0,vmax=2*np.pi); ax.set_title(n,fontsize=9); ax.axis("off")
fig.savefig("../figs/i4_cyclic.png",dpi=110); plt.close(fig)
# names in Skill exist
for nme in ["batlow","lipari","vik","roma","bam","romaO","vikO"]: print(nme, hasattr(cm,nme), end=" | ")
print()
print("matplotlib turbo since:", "exists", "turbo" in plt.colormaps())
