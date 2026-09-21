import glob, numpy as np
from PIL import Image
for f in sorted(glob.glob("../figs/i5_phd_*.png"))+["../figs/i1_categorical_full_vs_subset.png","../figs/i2_diverging_heatmaps.png","../figs/i3_showcol_gray.png","../figs/i3_demoplot.png"]:
    a=np.asarray(Image.open(f).convert("RGB")); nw=(a.min(axis=2)<245).mean()
    print(f.split("/")[-1], a.shape[:2], "non-white %.3f"%nw)
