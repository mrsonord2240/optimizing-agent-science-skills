import sys, numpy as np
from PIL import Image
sys.path.insert(0, r'F:\OpenScience\audits\bio-data-visualization-multipanel-figures\run')
from bbox import words
OUT = r'F:\OpenScience\audits\bio-data-visualization-multipanel-figures\out'
def panel(name, hexc):
    im = np.array(Image.open(OUT + '/' + name + '.png').convert('RGB')).astype(int)
    rgb = [int(hexc[i:i+2], 16) for i in (1, 3, 5)]
    m = (abs(im - rgb) < 6).all(axis=2)
    ys, xs = np.where(m)
    return (xs.min(), xs.max(), ys.min(), ys.max()) if len(xs) else None
def w(name): return words(OUT + '/' + name + '.bbox.html')
def find(ws, t): return [x for x in ws if x[0] == t]
print("== F1 tag alignment (offset = panel left edge - tag left edge, pt)")
for n in ['f1_default', 'f1_fix_annot', 'f1_fix_amp', 'f1_fix_amp_bold8']:
    W, H, ws = w(n)
    p1 = panel(n, '#ff0000'); p2 = panel(n, '#00ff00')
    ta = min(find(ws, 'a'), key=lambda z: z[2]); tb = min(find(ws, 'b'), key=lambda z: z[2])
    o1 = p1[0] - ta[1]; o2 = p2[0] - tb[1]
    print(f'{n:18s} tag a x={ta[1]:.1f} y={ta[2]:.1f}-{ta[4]:.1f} h={ta[4]-ta[2]:.1f}; tag b x={tb[1]:.1f}; panel1 x0={p1[0]} panel2 x0={p2[0]}; offset1={o1:.1f} offset2={o2:.1f} diff={abs(o1-o2):.1f}  panel top y0={p1[2]}')
print("== F2 legends (count of 'ctrl' words in text layer)")
for n in ['f2_same', 'f2_diffpal', 'f2_dropone', 'f2_colour_vs_fill']:
    W, H, ws = w(n)
    print(f'{n:20s} ctrl={len(find(ws,"ctrl"))} trt={len(find(ws,"trt"))} legend-title g={len(find(ws,"g"))}')
print("== F5 cowplot alignment of stacked panels (px)")
for n in ['f5_cow_ncol1_none', 'f5_cow_ncol1_v', 'f5_cow_ncol1_h', 'f5_cow_ncol1_hv', 'f5b_cow_noaxis_none', 'f5b_cow_noaxis_v', 'f5b_cow_noaxis_hv']:
    a = panel(n, '#ff0000'); b = panel(n, '#00ff00')
    print(f'{n:22s} N1 x={a[0]}-{a[1]} | N2 x={b[0]}-{b[1]}   left-edge diff={abs(a[0]-b[0])} right-edge diff={abs(a[1]-b[1])}')
print("== F6 axes collect: count axis-title words x / y per figure")
for n in ['f6_nocollect', 'f6_axes', 'f6_axes_titles', 'f6_titles_only']:
    W, H, ws = w(n)
    nums = [x for x in ws if x[0].lstrip('-').replace('.', '').isdigit()]
    print(f'{n:16s} x-title={len(find(ws,"x"))} y-title={len(find(ws,"y"))} tick-label words={len(nums)} total words={len(ws)}')
