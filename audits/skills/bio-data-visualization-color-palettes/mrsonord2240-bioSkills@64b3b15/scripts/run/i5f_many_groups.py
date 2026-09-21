import numpy as np, itertools, colorspacious as cs, matplotlib.pyplot as plt
from matplotlib.colors import to_rgb, to_hex
def sim(rgb,k): return np.clip(cs.cspace_convert(rgb,{"name":"sRGB1+CVD","cvd_type":k,"severity":100},"sRGB1"),0,1)
def stats(h):
    rgb=np.array([to_rgb(x) for x in h]); out=[]
    for k in [None,"deuteranomaly"]:
        s=rgb if k is None else sim(rgb,k); u=cs.cspace_convert(s,"sRGB1","CAM02-UCS")
        d=[np.linalg.norm(u[i]-u[j]) for i,j in itertools.combinations(range(len(h)),2)]
        out.append((min(d), sum(x<10 for x in d)))
    return out
rd=lambda n:[l.strip() for l in open(f"../data/pal_{n}.txt",encoding="utf-8") if l.strip()]
tab20=[to_hex(c) for c in plt.get_cmap("tab20").colors]
cands={"tab20 (n=20)":tab20,"tab20 first 15":tab20[:15],"Paired (n=12)":rd("paired12"),"Set3 (n=12)":rd("set3_12"),"Polychrome 36 first 15":rd("polychrome36")[:15],"Polychrome 36 first 20":rd("polychrome36")[:20],"Alphabet first 15":rd("alphabet26")[:15],
"Okabe-Ito 8 (reference)":['#E69F00','#56B4E9','#009E73','#F0E442','#0072B2','#D55E00','#CC79A7','#000000']}
print("%-26s %-28s %-28s"%("palette","normal: min dE / pairs<10","deutan: min dE / pairs<10"))
for n,h in cands.items():
    a,b=stats(h); print("%-26s %6.1f / %-3d               %6.1f / %-3d"%(n,a[0],a[1],b[0],b[1]))
