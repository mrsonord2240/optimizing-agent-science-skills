import numpy as np, itertools, colorspacious as cs
from matplotlib.colors import to_rgb
names=["T cell","B cell","NK cell","Monocyte","Dendritic","Platelet","Erythroid","Unassigned"]
h=['#E69F00','#56B4E9','#009E73','#F0E442','#0072B2','#D55E00','#CC79A7','#999999']
def sim(rgb,k): return np.clip(cs.cspace_convert(rgb,{"name":"sRGB1+CVD","cvd_type":k,"severity":100},"sRGB1"),0,1)
rgb=np.array([to_rgb(x) for x in h])
for k in [None,"deuteranomaly","protanomaly","tritanomaly"]:
    s=rgb if k is None else sim(rgb,k); u=cs.cspace_convert(s,"sRGB1","CAM02-UCS")
    d=sorted(((np.linalg.norm(u[i]-u[j]),names[i],names[j]) for i,j in itertools.combinations(range(8),2)))[:3]
    print(k or "normal", [(round(a,1),b,c) for a,b,c in d])
print("Grey (#999999) vs each type, deutan-sim CAM02-UCS dE:")
s=sim(rgb,"deuteranomaly"); u=cs.cspace_convert(s,"sRGB1","CAM02-UCS")
for i in range(7): print(" ",names[i], round(float(np.linalg.norm(u[i]-u[7])),1))
