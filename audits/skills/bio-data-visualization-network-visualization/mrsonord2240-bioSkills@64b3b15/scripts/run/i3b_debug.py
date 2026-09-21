import sys, os, pathlib, numpy as np, matplotlib.pyplot as plt
ROOT=pathlib.Path('F:/OpenScience/audits/bio-data-visualization-network-visualization')
sys.path.insert(0,str(ROOT/'run')); import figaudit
os.chdir(ROOT/'out/ex_static')
src=(ROOT/'run/skill/data-visualization/network-visualization/examples/network_plots.py').read_text(encoding='utf-8')
figs=[]; _sv=plt.savefig
def sv(fn,*a,**k):
    figs.append((fn,figaudit.audit(plt.gcf()),plt.gcf())); return _sv('x.png',dpi=50)
plt.savefig=sv; ns={'__name__':'__main__'}; import io,contextlib
with contextlib.redirect_stdout(io.StringIO()): exec(compile(src,'np','exec'),ns)
G=ns['G']; a=figs[0][1]; exp=np.array([G[u][v]['weight']*2 for u,v in G.edges()])
print(a['seg_lw'][:6],exp[:6], len(a['seg_lw']),len(exp))
print('sorted equal',np.allclose(np.sort(a['seg_lw']),np.sort(exp)))
# edge colours in P4 by threshold
fig=figs[3][2]; import matplotlib.colors as mc
lc=[c for c in fig.axes[0].collections if type(c).__name__=='LineCollection'][0]
cols=[mc.to_hex(c[:3]).lower() for c in lc.get_colors()]
exp_c=['#e64b35' if G[u][v]['score']>=900 else '#f39b7f' if G[u][v]['score']>=700 else '#cccccc' for u,v in G.edges()]
print('P4 edge colours match thresholds:',cols==exp_c, {c:cols.count(c) for c in set(cols)})
