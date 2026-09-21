# Input 3: shipped examples/network_plots.py run from a copy (cwd out/ex_static); capture each figure and assert content
import sys, os, pathlib, numpy as np, matplotlib.pyplot as plt, networkx as nx
ROOT=pathlib.Path('F:/OpenScience/audits/bio-data-visualization-network-visualization')
sys.path.insert(0,str(ROOT/'run')); import figaudit
os.chdir(ROOT/'out/ex_static')
src=(ROOT/'run/skill/data-visualization/network-visualization/examples/network_plots.py').read_text(encoding='utf-8')
figs=[]
_sv=plt.savefig
def sv(fn,*a,**k):
    figs.append((fn,figaudit.audit(plt.gcf()))); return _sv(fn,*a,**k)
plt.savefig=sv
ns={'__name__':'__main__'}
exec(compile(src,'network_plots.py','exec'),ns)
G=ns['G']; print('\nG',G.number_of_nodes(),G.number_of_edges())
for fn,a in figs:
    print(fn,'nodes',a['n_pts'],'edge segs',a['n_edges'],'labels',len(a['labels']),'size min/max',None if a['sizes'] is None else (a['sizes'].min(),a['sizes'].max()), 'exists',os.path.getsize(fn))
deg=dict(G.degree()); order=list(G.nodes())
f1=figs[0][1]
print('P1 size==100+150*deg:',np.allclose(f1['sizes'],[100+150*deg[n] for n in order]),' color array==degree:',np.array_equal(f1['array'],[deg[n] for n in order]))
print('P1 edge widths == 2*weight:',np.allclose(f1['seg_lw'],[G[u][v]['weight']*2 for u,v in G.edges()]))
# P4 edge colours vs thresholds: recompute from figure segment colours
import matplotlib.colors as mc
for fn,a in figs[3:4]:
    pass
# hubs plot
f3=figs[2][1]; top5=sorted(deg,key=deg.get,reverse=True)[:5]
print('P3 labelled == top5 hubs:',sorted(f3['labels'])==sorted(top5),sorted(f3['labels']),top5)
# ties at 5th place?
print('degree tail of top 8:',sorted(deg.values(),reverse=True)[:8])
# community counts in P2 vs independent
from networkx.algorithms.community import greedy_modularity_communities, louvain_communities
c=list(greedy_modularity_communities(G)); print('communities greedy',len(c),sorted(map(len,c)),'| P2 legend on figure -> title communities in ns:',len(ns['communities']))
print('P2 colors == community idx',np.array_equal(figs[1][1]['array'],[ns['node_to_community'][n] for n in order]))
