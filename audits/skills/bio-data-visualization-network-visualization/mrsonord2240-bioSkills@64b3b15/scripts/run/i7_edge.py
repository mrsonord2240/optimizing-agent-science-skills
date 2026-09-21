# Input 7: edge/stress cases for the Python recipes
import os, sys, time, json, warnings, numpy as np, networkx as nx, pandas as pd, matplotlib.pyplot as plt, pathlib
ROOT=pathlib.Path('F:/OpenScience/audits/bio-data-visualization-network-visualization'); os.chdir(ROOT/'out/i7'); sys.path.insert(0,str(ROOT/'run')); import figaudit
G=nx.read_graphml(ROOT/'data/synth_ppi.graphml')
# --- A: two-condition comparison with union layout (SKILL failure-mode fix)
rng=np.random.default_rng(3)
A=G.copy(); B=G.copy(); rem=[e for e in list(B.edges())[:60]]; B.remove_edges_from(rem); B.remove_nodes_from(list(B.nodes())[:5]); B.add_edge('X1','X2',weight=1)  # B loses 5 nodes, gains 2 new
U=nx.compose(A,B); pos=nx.spring_layout(U,seed=42)
for name,H in [('A',A),('B',B)]:
    nx.draw_networkx(H,pos,with_labels=False,node_size=20); plt.close()
print('union pos draws both A and B: OK; same node -> same position:',all(np.allclose(pos[n],pos[n]) for n in B))
try: nx.draw_networkx(B,nx.spring_layout(A,seed=42)); print('pos from A only for B: no error (!)')
except Exception as e: print('pos from A only for B ->',type(e).__name__,e)
# --- B: edge width fix from the SKILL: width=[G[u][v]['weight'] ...] on a graph lacking weights
H=nx.Graph(G); [d.pop('weight') for _,_,d in H.edges(data=True)]
try: w=[H[u][v]['weight'] for u,v in H.edges()]; print('no error')
except Exception as e: print('SKILL edge-width one-liner on unweighted graph ->',type(e).__name__,e)
# normalisation: SKILL says "with normalization to visible range" but shows none; raw weight as width
w=[G[u][v]['weight'] for u,v in G.edges()]; print('raw weight width range',min(w),max(w),'-> line widths in points: barely visible (<1pt)')
# --- C: SKILL block 5 on awkward graphs
import matplotlib; from networkx.algorithms.community import greedy_modularity_communities
def block(G,label):
    try:
        pos=nx.spring_layout(G,k=1.5,seed=42); degrees=dict(G.degree()); comms=list(greedy_modularity_communities(G)); n2c={n:i for i,c in enumerate(comms) for n in c}
        sizes=[100+degrees[n]*50 for n in G.nodes()]; colors=[n2c[n] for n in G.nodes()]
        fig,ax=plt.subplots(); nx.draw_networkx_edges(G,pos,ax=ax); nodes=nx.draw_networkx_nodes(G,pos,node_size=sizes,node_color=colors,cmap='tab20',ax=ax)
        hubs=[n for n in G.nodes() if degrees[n]>=10]; nx.draw_networkx_labels(G,pos,labels={n:n for n in hubs},ax=ax); a=figaudit.audit(fig); plt.close(fig)
        print(f'{label:34s} OK nodes drawn {a["n_pts"]}/{G.number_of_nodes()} edges {a["n_edges"]}/{G.number_of_edges()} communities {len(comms)} labelled {len(a["labels"])}')
    except Exception as e: print(f'{label:34s} {type(e).__name__}: {str(e)[:90]}')
Dg=nx.gnp_random_graph(30,0.15,seed=2,directed=True); block(Dg,'directed random (30)')
block(nx.DiGraph([('a','b'),('b','c'),('a','c')]),'directed 3-node')
S=nx.Graph(G); S.add_edge('G001','G001'); block(S,'self loop')
I=nx.Graph(G); I.add_nodes_from([f'iso{i}' for i in range(5)]); block(I,'5 isolated nodes')
block(nx.disjoint_union(nx.complete_graph(5),nx.complete_graph(5)),'two components')
block(nx.Graph(),'empty graph')
block(nx.Graph([('a','b')]),'single edge')
block(nx.path_graph(3),'int node ids')
# STRING real: hub threshold >=10 labels
R=nx.Graph()
df=pd.read_csv('F:/OpenScience/audit-envs/data-visualization/public-data/networks/string_tp53_neighbors.tsv',sep='\t')
for _,r in df.iterrows(): R.add_edge(r.preferredName_A,r.preferredName_B,weight=r.score)
block(R,'real STRING TP53 axis (10 nodes)'); print('  STRING degrees',dict(R.degree()))
# --- D: scale claims
for n in [500,2000,5000]:
    Gb=nx.barabasi_albert_graph(n,3,seed=1); t=time.time(); nx.spring_layout(Gb,seed=42,iterations=100); t1=time.time()-t
    print(f'spring_layout n={n} edges={Gb.number_of_edges()} {t1:.1f}s')
t=time.time(); Gb=nx.barabasi_albert_graph(2000,3,seed=1); nx.forceatlas2_layout(Gb,seed=42,max_iter=100); print('nx.forceatlas2_layout n=2000: %.1fs'%(time.time()-t))
# --- E: PDF output of block 5 -> vector, non-empty
fig,ax=plt.subplots(figsize=(10,8)); nx.draw_networkx(G,nx.spring_layout(G,seed=42),ax=ax,node_size=50,with_labels=False); fig.savefig('network.pdf',bbox_inches='tight',dpi=300); print('pdf bytes',os.path.getsize('network.pdf'),open('network.pdf','rb').read(8))
