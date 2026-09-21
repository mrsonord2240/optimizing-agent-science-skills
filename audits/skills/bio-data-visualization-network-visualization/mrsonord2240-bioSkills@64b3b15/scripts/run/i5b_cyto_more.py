# Input 5b: shipped cytoscape_automation.py run for real (Cytoscape up), degree-less graph, TP53 STRING real network, GRN directed, layout seed, export/re-import GraphML+SIF
import networkx as nx, py4cytoscape as p4c, os, pathlib, pandas as pd, numpy as np, io, contextlib, traceback
A='/mnt/openscience/audits/bio-data-visualization-network-visualization'
os.makedirs(A+'/out/cyto2',exist_ok=True); os.chdir(A+'/out/cyto2')
for f in os.listdir('.'): os.remove(f)
print('=== shipped cytoscape_automation.py')
src=pathlib.Path(A+'/run/skill/data-visualization/network-visualization/examples/cytoscape_automation.py').read_text(encoding='utf-8')
ns={'__name__':'__main__'}; buf=io.StringIO()
try:
    with contextlib.redirect_stdout(buf): exec(compile(src,'cytoscape_automation.py','exec'),ns)
except Exception: traceback.print_exc()
print(buf.getvalue()); G=ns['G']
print('files',sorted(os.listdir('.')),[os.path.getsize(f) for f in sorted(os.listdir('.'))])
print('cy nodes',len(p4c.get_all_nodes()),'edges',len(p4c.get_all_edges()),'graph',G.number_of_nodes(),G.number_of_edges())
t=p4c.get_table_columns('node',['name','gene_type','degree'])
print('gene_type column ok', all((r.gene_type=='kinase')==(r['name'] in ['ATM','CHEK2','CDK2','AKT1','MAPK1']) for _,r in t.iterrows()))
for n,sh in [('ATM',None),('TP53',None)]:
    if n in list(t['name']): print(n,'shape',p4c.get_node_property(node_names=[n],visual_property='NODE_SHAPE'),'size',p4c.get_node_property(node_names=[n],visual_property='NODE_SIZE'),'deg',G.degree(n))
et=p4c.get_table_columns('edge',['score']); 
e0=list(G.edges(data=True))[0]
w=p4c.get_edge_property(visual_property='EDGE_WIDTH')
ws=sorted(set(round(v,2) for v in w.values())); print('edge widths distinct',len(ws),'min',min(ws),'max',max(ws),'(mapping 400->1, 1000->4)')
# layout reproducibility: run force-directed twice
p4c.layout_network('force-directed'); a=p4c.get_node_position(['TP53','MDM2']) if 'TP53' in G else None
p4c.layout_network('force-directed'); b=p4c.get_node_position(['TP53','MDM2']) if 'TP53' in G else None
print('force-directed twice, same positions?',a.equals(b) if a is not None else 'n/a', a.values.tolist() if a is not None else '', b.values.tolist() if b is not None else '')
print('=== graph WITHOUT degree attribute (SKILL block 7 does not add it)')
G2=nx.read_graphml(A+'/data/synth_ppi.graphml')
for n in G2: del G2.nodes[n]['degree']
p4c.create_network_from_networkx(G2,title='nodeg')
try:
    p4c.create_visual_style('S2'); p4c.set_node_size_mapping('degree',[1,5,20],[30,60,120],mapping_type='c',style_name='S2'); print('no error raised for missing column')
    s=p4c.get_node_property(node_names=['G000'],visual_property='NODE_SIZE') ; print('G000 size with default style after mapping on absent column set',s)
except Exception as e: print('ERR',type(e).__name__,str(e)[:150])
print('=== real STRING TP53 network')
df=pd.read_csv('/mnt/openscience/audit-envs/data-visualization/public-data/networks/string_tp53_neighbors.tsv',sep='\t')
R=nx.Graph()
for _,r in df.iterrows(): R.add_edge(r.preferredName_A,r.preferredName_B,weight=r.score)
for n in R: R.nodes[n]['degree']=R.degree(n)
print('STRING rows',len(df),'graph',R.number_of_nodes(),R.number_of_edges(),'min score',df.score.min())
p4c.create_network_from_networkx(R,title='STRING'); p4c.layout_network('circular')
print('cy',len(p4c.get_all_nodes()),len(p4c.get_all_edges()))
p4c.export_image('string.png',type='PNG',resolution=100); p4c.export_image('string.pdf',type='PDF'); p4c.export_image('string.svg',type='SVG')
print('exports',{f:os.path.getsize(f) for f in ['string.png','string.pdf','string.svg']})
print('=== directed GRN + hierarchical + arrows')
D=nx.read_graphml(A+'/data/synth_grn.graphml'); p4c.create_network_from_networkx(D,title='GRN')
try: p4c.layout_network('hierarchical'); print('hierarchical layout ok')
except Exception as e: print('hierarchical ERR',str(e)[:150])
ed=p4c.get_table_columns('edge',['interaction']); print('edge count',len(p4c.get_all_edges()),'directed flag in Cytoscape:',p4c.get_network_info() if False else 'n/a')
p4c.export_image('grn.png',type='PNG',resolution=100)
print('=== export/re-import round trip')
p4c.set_current_network('STRING')
p4c.export_network('string.graphml',type='GraphML'); p4c.export_network('string.sif',type='SIF'); p4c.export_network('string.cx',type='CX') if False else None
print({f:os.path.getsize(f) for f in os.listdir('.') if f.startswith('string.')})
H=nx.read_graphml('string.graphml'); print('graphml re-read nodes/edges',H.number_of_nodes(),H.number_of_edges(),'vs',R.number_of_nodes(),R.number_of_edges())
sif=[l.split('\t') if '\t' in l else l.split() for l in open('string.sif',encoding='utf-8').read().splitlines() if l.strip()]
print('sif lines',len(sif),'sample',sif[:2])
p4c.import_network_from_file(A+'/out/cyto2/string.graphml'); print('cytoscape re-import from graphml: current nodes/edges',len(p4c.get_all_nodes()),len(p4c.get_all_edges()))
p4c.import_network_from_file(A+'/out/cyto2/string.sif'); print('cytoscape re-import from sif: nodes/edges',len(p4c.get_all_nodes()),len(p4c.get_all_edges()))
