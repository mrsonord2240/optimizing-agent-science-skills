"""Pixel measurement of the trackViewer T1 PNG: orange lollipop-head centroids vs y-axis tick rows."""
import numpy as np
from PIL import Image
import sys
f = sys.argv[1]
im = np.array(Image.open(f).convert("RGB")).astype(int)
H, W, _ = im.shape
orange = (abs(im[:,:,0]-0xD5)<8)&(abs(im[:,:,1]-0x5E)<8)&(abs(im[:,:,2]-0x00)<8)
from scipy import ndimage
lab, n = ndimage.label(orange)
print("image", W, H, "orange blobs", n)
for i in range(1, n+1):
    ys, xs = np.where(lab==i)
    if len(ys) < 200: continue
    print("blob", i, "centroid x=%.1f y=%.1f area=%d" % (xs.mean(), ys.mean(), len(ys)))
# axis ticks: dark pixels in a column band just left of the axis line; find the vertical axis line = long dark column
dark = (im.sum(axis=2) < 150)
cols = dark[:, :400].sum(axis=0); ax = int(np.argmax(cols)); print("y-axis line column", ax, "len", cols[ax])
ticks = [y for y in range(H) if dark[y, ax-12:ax-2].all()]
# group consecutive
g=[]; 
for y in ticks:
    if g and y-g[-1][-1] <= 1: g[-1].append(y)
    else: g.append([y])
print("tick rows (centre):", [round(np.mean(t),1) for t in g])
