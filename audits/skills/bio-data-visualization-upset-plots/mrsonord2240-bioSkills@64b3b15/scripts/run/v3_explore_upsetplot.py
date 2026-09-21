import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, numpy as np
from upsetplot import from_contents, UpSet
sets = {'SetA': ['Gene1','Gene2','Gene3','Gene4'], 'SetB': ['Gene2','Gene3','Gene5','Gene6'], 'SetC': ['Gene1','Gene3','Gene6','Gene7']}
data = from_contents(sets)
print(type(data), data.shape); print(data.head(3)); print(data.index.names)
u = UpSet(data, subset_size='count', show_counts=True, sort_by='cardinality', sort_categories_by='cardinality', facecolor='#0072B2', element_size=40)
u.style_subsets(present=['SetA','SetB'], facecolor='#D55E00')
fig = plt.figure(figsize=(8,5)); ax = u.plot(fig=fig)
print(ax.keys())
for k,a in ax.items():
    print(k, 'patches', len(a.patches), 'collections', len(a.collections), 'lines', len(a.lines), 'texts', len(a.texts))
print([round(p.get_height(),2) for p in ax['intersections'].patches])
print([t.get_text() for t in ax['intersections'].texts])
c = ax['matrix'].collections; print([type(x).__name__ for x in c])
for x in c: print(x.get_offsets()[:6].tolist(), x.get_facecolors()[:6].tolist())
print([ (round(p.get_width(),2)) for p in ax['totals'].patches], [t.get_text() for t in ax['matrix'].get_yticklabels()])
print(u.intersections); print(u.totals)
