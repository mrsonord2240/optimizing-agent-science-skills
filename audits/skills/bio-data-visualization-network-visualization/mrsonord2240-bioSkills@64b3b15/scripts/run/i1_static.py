# Input 1: SKILL.md "NetworkX + matplotlib -- Standard Static" block run VERBATIM on the synthetic planted graph, then content assertions
import sys, json, numpy as np, networkx as nx, matplotlib.pyplot as plt, pathlib
sys.path.insert(0,'run'); import figaudit
from sklearn.metrics import adjusted_rand_score
G = nx.read_graphml('data/synth_ppi.graphml'); meta=json.load(open('data/synth_meta.json'))
src = pathlib.Path('run/blocks/b05_python.py').read_text(encoding='utf-8')
cap={}
_sv = plt.savefig
def sv(*a,**k):
    cap['fig']=plt.gcf(); cap['a']=figaudit.audit(plt.gcf()); return _sv('out/i1_static.png',**{kk:v for kk,v in k.items() if kk!='dpi'}, dpi=100)
plt.savefig = sv
ns={'G':G}
exec(compile(src,'b05','exec'),ns)
a=cap['a']
print('drawn nodes',a['n_pts'],'graph nodes',G.number_of_nodes())
print('drawn edge segments',a['n_edges'],'graph edges',G.number_of_edges())
deg=dict(G.degree()); order=list(G.nodes())
exp_sizes=np.array([100+deg[n]*50 for n in order]); print('size mapping exact:',np.allclose(a['sizes'],exp_sizes))
# community colors vs independent computation (same algorithm)
comms=list(nx.algorithms.community.greedy_modularity_communities(G))
n2c={n:i for i,c in enumerate(comms) for n in c}
print('n communities',len(comms), 'sizes',sorted(len(c) for c in comms))
arr=np.array(a['array']); print('color array equals community idx:', np.array_equal(arr,[n2c[n] for n in order]))
truth=[G.nodes[n]['block'] for n in order]
print('ARI vs planted blocks', round(adjusted_rand_score(truth,[n2c[n] for n in order]),3))
# independent algorithm: louvain seed 42 and igraph
lv=nx.algorithms.community.louvain_communities(G,seed=42); l2={n:i for i,c in enumerate(lv) for n in c}
print('louvain n',len(lv),'ARI greedy vs louvain', round(adjusted_rand_score([n2c[n] for n in order],[l2[n] for n in order]),3))
# hubs labels: SKILL threshold degrees>=10
hubs_lbl=[n for n in G.nodes() if deg[n]>=10]
print('labels drawn',len(a['labels']),'nodes with degree>=10',len(hubs_lbl),'planted hubs',meta['hubs'],'labelled?',[h in a['labels'] for h in meta['hubs']])
# layout reproducibility
p1=nx.spring_layout(G,k=1.5,seed=42); p2=nx.spring_layout(G,k=1.5,seed=42)
print('layout reproducible same seed:',all(np.allclose(p1[n],p2[n]) for n in G))
p3=nx.spring_layout(G,k=1.5,seed=43); print('layout differs other seed:',not all(np.allclose(p1[n],p3[n]) for n in G))
pos_drawn=a['offsets']; print('drawn positions equal spring_layout(seed=42):',np.allclose(pos_drawn,[p1[n] for n in order]))
# edge width uniform in SKILL block (width=0.5) vs weights
print('edge widths unique',np.unique(a['seg_lw']))
# pdf output
import os; print('network.pdf exists',os.path.exists('network.pdf'),os.path.getsize('network.pdf') if os.path.exists('network.pdf') else 0)
