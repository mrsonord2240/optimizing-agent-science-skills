# Input 5a: SKILL.md Cytoscape block VERBATIM (block 7) on the synthetic PPI graph, with content assertions against Cytoscape's own state
import networkx as nx, py4cytoscape as p4c, os, pathlib, json, numpy as np
A='/mnt/openscience/audits/bio-data-visualization-network-visualization'
os.chdir(A+'/out/cyto')
G = nx.read_graphml(A+'/data/synth_ppi.graphml')
src = pathlib.Path(A+'/run/blocks/b07_python.py').read_text(encoding='utf-8')
ns={'G':G}
try:
    exec(compile(src,'b07','exec'),ns); print('BLOCK RAN')
except Exception as e:
    import traceback; traceback.print_exc()
nodes=p4c.get_all_nodes(); edges=p4c.get_all_edges()
print('cytoscape nodes',len(nodes),'graph',G.number_of_nodes(),'| edges',len(edges),'graph',G.number_of_edges())
nt=p4c.get_table_columns('node',['name','degree'])
deg=dict(G.degree()); print('degree column matches nx degree:',all(int(r.degree)==deg[r['name']] for _,r in nt.iterrows()))
# visual style: size per node vs mapping [1,5,20]->[30,60,120]
sizes=p4c.get_node_property(visual_property='NODE_SIZE',node_names=list(nt['name'])) if False else None
import pandas as pd
for n in [ 'G000','G001','G030']:
    s=p4c.get_node_property(node_names=[n],visual_property='NODE_SIZE'); c=p4c.get_node_property(node_names=[n],visual_property='NODE_FILL_COLOR')
    print(n,'degree',deg[n],'NODE_SIZE',s,'FILL',c)
print('current style',p4c.get_current_style() if hasattr(p4c,'get_current_style') else None)
for f in ['network.pdf']:
    print(f,'in caller cwd:',os.path.exists(f), os.path.getsize(f) if os.path.exists(f) else 0)
print('files in cwd',os.listdir('.'))
