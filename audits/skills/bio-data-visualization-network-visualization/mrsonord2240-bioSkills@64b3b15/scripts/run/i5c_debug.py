# Input 5c: why did the shipped example export nothing (bare except), and the GraphML re-import 14-node oddity
import networkx as nx, py4cytoscape as p4c, os, pathlib, traceback, pandas as pd
A='/mnt/openscience/audits/bio-data-visualization-network-visualization'
os.makedirs(A+'/out/cyto3',exist_ok=True); os.chdir(A+'/out/cyto3')
for f in os.listdir('.'): os.remove(f)
src=pathlib.Path(A+'/run/skill/data-visualization/network-visualization/examples/cytoscape_automation.py').read_text(encoding='utf-8')
# same source but the trailing bare-except replaced by a printing one -> shows the swallowed exception
src2=src.replace("except Exception:\n    pass","except Exception:\n    traceback.print_exc()")
assert src2!=src
ns={'__name__':'__main__','traceback':traceback}
exec(compile(src2,'cytoscape_automation.py','exec'),ns)
print('files after example',os.listdir('.'))
print('shape ATM',p4c.get_node_property(node_names=['ATM'],visual_property='NODE_SHAPE'))
print('--- graphml re-import oddity')
df=pd.read_csv('/mnt/openscience/audit-envs/data-visualization/public-data/networks/string_tp53_neighbors.tsv',sep='\t')
R=nx.Graph()
for _,r in df.iterrows(): R.add_edge(r.preferredName_A,r.preferredName_B,weight=float(r.score))
suid=p4c.create_network_from_networkx(R,title='STRING2'); print('created',suid,len(p4c.get_all_nodes()))
p4c.export_network('s.graphml',type='GraphML',network=suid)
before=p4c.get_network_list(); r=p4c.import_network_from_file(A+'/out/cyto3/s.graphml'); print('import result',r)
print('networks',p4c.get_network_list(),'current nodes/edges',len(p4c.get_all_nodes()),len(p4c.get_all_edges()), 'name col', sorted(p4c.get_table_columns('node',['name'])['name'].tolist()))
print('original network nodes',len(p4c.get_all_nodes(network=suid)))
