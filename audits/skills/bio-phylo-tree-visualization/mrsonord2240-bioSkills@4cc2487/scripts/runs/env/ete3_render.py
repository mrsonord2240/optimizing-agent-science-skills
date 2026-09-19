"""ETE check: can ete3 3.1.3 (installed) render a tree headlessly? ete4 pip build failed (Cython compile error, pip_ete4*.log)."""
import os
os.environ.setdefault('QT_QPA_PLATFORM', 'offscreen')
from ete3 import Tree, TreeStyle, NodeStyle, TextFace
t = Tree(open('../../data/iq/primates16.treefile').read(), format=1)
ts = TreeStyle(); ts.mode = 'c'; ts.show_leaf_name = True; ts.show_scale = True
for n in t.traverse():
    ns = NodeStyle(); ns['size'] = 0
    if n.is_leaf() and n.name.split('_')[0] in ('Homo', 'Pan', 'Gorilla', 'Pongo'):
        ns['hz_line_color'] = 'red'
    n.set_style(ns)
out = t.render('ete3_circular.png', w=600, units='px', tree_style=ts)
print('rendered', out, os.path.getsize('ete3_circular.png'), 'bytes')
