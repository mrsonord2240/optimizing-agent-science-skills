import numpy as np, json, itertools, matplotlib.pyplot as plt
import colorspacious as cs
from matplotlib.colors import to_rgb, to_hex
from cmcrameri import cm as cmc
import seaborn as sns

def sim(rgb, kind, sev=100):
    return np.clip(cs.cspace_convert(rgb, {"name":"sRGB1+CVD","cvd_type":kind,"severity":sev}, "sRGB1"),0,1)
def ucs(rgb): return cs.cspace_convert(np.clip(rgb,0,1), "sRGB1", "CAM02-UCS")
def minpair(hexes, kind=None):
    rgb = np.array([to_rgb(h) for h in hexes])
    if kind: rgb = sim(rgb, kind)
    u = ucs(rgb); best=(1e9,None)
    for i,j in itertools.combinations(range(len(hexes)),2):
        d=np.linalg.norm(u[i]-u[j])
        if d<best[0]: best=(d,(hexes[i],hexes[j]))
    return best

pal = {
 "Okabe-Ito 8 (Skill hexes)": ['#E69F00','#56B4E9','#009E73','#F0E442','#0072B2','#D55E00','#CC79A7','#000000'],
 "Okabe-Ito 7 (no black)": ['#E69F00','#56B4E9','#009E73','#F0E442','#0072B2','#D55E00','#CC79A7'],
 "Tol bright 7": ['#4477AA','#EE6677','#228833','#CCBB44','#66CCEE','#AA3377','#BBBBBB'],
 "npg 8": ['#E64B35','#4DBBD5','#00A087','#3C5488','#F39B7F','#8491B4','#91D1C2','#DC0000'],
 "aaas 8": ['#3B4992','#EE0000','#008B45','#631879','#008280','#BB0021','#5F559B','#A20056'],
 "lancet 8": ['#00468B','#ED0000','#42B540','#0099B4','#925E9F','#FDAF91','#AD002A','#ADB6B6'],
 "jama 7": ['#374E55','#DF8F44','#00A1D5','#B24745','#79AF97','#6A6599','#80796B'],
 "jco 8": ['#0073C2','#EFC000','#868686','#CD534C','#7AA6DC','#003C67','#8F7700','#3B3B3B'],
 "nejm 8": ['#BC3C29','#0072B5','#E18727','#20854E','#7876B1','#6F99ADFF'[:7],'#FFDC91','#EE4C97'],
 "ColorBrewer Set1 (first 5)": ['#E41A1C','#377EB8','#4DAF4A','#984EA3','#FF7F00'],
 "ColorBrewer Dark2 8": ['#1B9E77','#D95F02','#7570B3','#E7298A','#66A61E','#E6AB02','#A6761D','#666666'],
 "example NPG-style 5 (palette_examples.R)": ['#E64B35','#4DBBD5','#00A087','#3C5488','#F39B7F'],
 "Up/Down/NS (Skill DE convention)": ['#D55E00','#0072B2','#999999'],
 "Skill custom cats (Control/Treat/Vehicle)": ['#0072B2','#D55E00','#009E73'],
 "seaborn colorblind 10": [to_hex(c) for c in sns.color_palette("colorblind")],
}
print("Min pairwise CAM02-UCS distance (higher = safer; ~10+ comfortably distinct, <5 hard to tell) and the closest pair")
print("%-42s %-16s %-16s %-16s %-16s" % ("palette","normal","deutan","protan","tritan"))
out={}
for n,h in pal.items():
    r=[]
    cells=[]
    for k in [None,"deuteranomaly","protanomaly","tritanomaly"]:
        d,pr=minpair(h,k); r.append((round(d,1),pr)); cells.append("%5.1f %s/%s"%(d,pr[0][1:],pr[1][1:]))
    out[n]=[x[0] for x in r]
    print("%-42s %s" % (n," | ".join(cells)))
json.dump(out,open("i2_cvd_minpair.json","w"),indent=1)

# Sequential maps: how much does the ramp change under CVD (mean deltaE normal vs simulated) and is L* still monotonic
print("\nSequential ramps: mean dE(normal vs deutan-sim / protan-sim) and L* monotonic under deutan")
for name,cmap in {"viridis":plt.get_cmap("viridis"),"cividis":plt.get_cmap("cividis"),"magma":plt.get_cmap("magma"),"plasma":plt.get_cmap("plasma"),"batlow":cmc.batlow,"turbo":plt.get_cmap("turbo"),"jet":plt.get_cmap("jet"),"rainbow":plt.get_cmap("rainbow")}.items():
    rgb=cmap(np.linspace(0,1,256))[:,:3]
    res=[]
    for k in ["deuteranomaly","protanomaly"]:
        s=sim(rgb,k); d=np.linalg.norm(ucs(rgb)-ucs(s),axis=1).mean()
        L=cs.cspace_convert(s,"sRGB1","CIELab")[:,0]; dL=np.diff(L)
        res.append((round(d,1), bool((dL>=-1e-9).all() or (dL<=1e-9).all())))
    print("%-9s deutan dE=%5.1f mono=%s | protan dE=%5.1f mono=%s"%(name,res[0][0],res[0][1],res[1][0],res[1][1]))

# Diverging: are the two arms of vik / RdBu_r / custom Okabe ramp separable under deutan at the extremes and at +-1 sd
print("\nDiverging endpoint separation (dE CAM02-UCS) under deutan / protan / normal")
for name,(a,b) in {"vik":(cmc.vik(0.0),cmc.vik(1.0)),"roma":(cmc.roma(0.0),cmc.roma(1.0)),"RdBu_r":(plt.get_cmap("RdBu_r")(0.0),plt.get_cmap("RdBu_r")(1.0)),"custom #0072B2/#D55E00":(to_rgb('#0072B2')+(1,),to_rgb('#D55E00')+(1,)),"palette_examples #4DBBD5/#E64B35":(to_rgb('#4DBBD5')+(1,),to_rgb('#E64B35')+(1,)),"red/green (#D7191C/#1A9641)":(to_rgb('#D7191C')+(1,),to_rgb('#1A9641')+(1,))}.items():
    rgb=np.array([a[:3],b[:3]]); r=[]
    for k in [None,"deuteranomaly","protanomaly"]:
        s=rgb if k is None else sim(rgb,k); u=ucs(s); r.append(round(float(np.linalg.norm(u[0]-u[1])),1))
    print("%-34s normal %5.1f deutan %5.1f protan %5.1f"%(name,*r))
