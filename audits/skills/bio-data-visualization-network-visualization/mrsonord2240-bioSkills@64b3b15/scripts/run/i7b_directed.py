# Input 7b: directed GRN drawn with the SKILL's networkx layered calls: arrowheads, hierarchical layout needs pydot (absent on Windows venv)
import sys, networkx as nx, matplotlib.pyplot as plt, numpy as np
sys.path.insert(0,'run'); import figaudit
D=nx.read_graphml('data/synth_grn.graphml'); pos=nx.spring_layout(D,seed=42)
fig,ax=plt.subplots(figsize=(9,7)); nx.draw_networkx_edges(D,pos,alpha=0.4,ax=ax); nx.draw_networkx_nodes(D,pos,node_size=[300 if n.startswith('TF') else 60 for n in D],node_color=['#E64B35' if n.startswith('TF') else '#4DBBD5' for n in D],ax=ax)
nx.draw_networkx_labels(D,pos,labels={n:n for n in D if n.startswith('TF')},ax=ax); a=figaudit.audit(fig)
print('directed GRN: nodes',a['n_pts'],'/',D.number_of_nodes(),'arrow patches',a['n_arrows'],'/',D.number_of_edges(),' undirected LineCollection edges',a['n_edges'])
fig.savefig('out/i7/grn_spring.png',dpi=80)
try: nx.nx_pydot.graphviz_layout(D,prog='dot'); print('graphviz layout ok')
except Exception as e: print('graphviz_layout on Windows venv ->',type(e).__name__,str(e)[:60])
# edge sign attribute ('+'/'-') is not encoded by any Skill recipe: count
print('activating/repressing edges',sum(1 for *_,d in D.edges(data=True) if d['sign']=='+'),sum(1 for *_,d in D.edges(data=True) if d['sign']=='-'))
