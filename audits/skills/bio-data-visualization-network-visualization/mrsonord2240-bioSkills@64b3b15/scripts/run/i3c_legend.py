# Input 3 (cont): does the shipped community legend match the drawn node colours? (network_plots.py plot 2)
import sys, os, pathlib, io, contextlib, numpy as np, matplotlib.pyplot as plt, matplotlib.colors as mc
ROOT=pathlib.Path('F:/OpenScience/audits/bio-data-visualization-network-visualization')
sys.path.insert(0,str(ROOT/'run')); import figaudit
os.chdir(ROOT/'out/ex_static')
src=(ROOT/'run/skill/data-visualization/network-visualization/examples/network_plots.py').read_text(encoding='utf-8')
figs=[]; _sv=plt.savefig
def sv(fn,*a,**k): figs.append(plt.gcf()); return _sv('x.png',dpi=40)
plt.savefig=sv; ns={'__name__':'__main__'}
with contextlib.redirect_stdout(io.StringIO()): exec(compile(src,'np','exec'),ns)
fig=figs[1]; ax=fig.axes[0]
pc=[c for c in ax.collections if type(c).__name__=='PathCollection' and len(c.get_offsets())==30][0]
order=list(ns['G'].nodes()); n2c=ns['node_to_community']
node_col={}
for n,fc in zip(order,pc.get_facecolor()): node_col.setdefault(n2c[n],set()).add(mc.to_hex(fc))
leg=[mc.to_hex(ns['palette'](i)) for i in range(4)]
for i in range(4): print('community',i+1,'node colour',node_col[i],'legend colour',leg[i],'MATCH' if {leg[i]}==node_col[i] else 'MISMATCH')
