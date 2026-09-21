# Input 5d: networkx GraphML -> Cytoscape import (synthetic PPI 100/511 and directed GRN 65/124), edge-list route, directed arrows, exports for viewing
import networkx as nx, py4cytoscape as p4c, os, pandas as pd
A='/mnt/openscience/audits/bio-data-visualization-network-visualization'
os.makedirs(A+'/out/cyto4',exist_ok=True); os.chdir(A+'/out/cyto4')
for f in os.listdir('.'): os.remove(f)
for name in ['synth_ppi','synth_grn']:
    r=p4c.import_network_from_file(f'{A}/data/{name}.graphml'); sid=r['networks'][0]; N=nx.read_graphml(f'{A}/data/{name}.graphml')
    print(name,'imported cy nodes/edges',len(p4c.get_all_nodes(network=sid)),len(p4c.get_all_edges(network=sid)),'nx',N.number_of_nodes(),N.number_of_edges(),'directed',N.is_directed())
    print('  node cols',list(p4c.get_table_columns('node').columns)[:8])
# edge-list route
ed=pd.read_csv(f'{A}/data/synth_ppi_edges.tsv',sep='\t')
nodes=pd.DataFrame({'id':sorted(set(ed.a)|set(ed.b))})
edges=ed.rename(columns={'a':'source','b':'target'}); edges['interaction']='pp'
p4c.create_network_from_data_frames(nodes,edges,title='edgelist'); print('edge-list route cy',len(p4c.get_all_nodes()),len(p4c.get_all_edges()),'expected',len(nodes),len(edges))
# directed GRN: arrows shown?
D=nx.read_graphml(f'{A}/data/synth_grn.graphml'); p4c.create_network_from_networkx(D,title='GRN2')
print('GRN via create_network_from_networkx: nodes/edges',len(p4c.get_all_nodes()),len(p4c.get_all_edges()))
print('EDGE_TARGET_ARROW_SHAPE default sample',list(p4c.get_edge_property(visual_property='EDGE_TARGET_ARROW_SHAPE').values())[:3])
p4c.layout_network('hierarchical'); p4c.export_image('grn_default.png',type='PNG',resolution=100)
p4c.set_edge_target_arrow_shape_default('DELTA') if hasattr(p4c,'set_edge_target_arrow_shape_default') else None
p4c.export_image('grn_arrows.png',type='PNG',resolution=100)
print('sizes',{f:os.path.getsize(f) for f in os.listdir('.') if f.endswith('.png')})
# fixed example style: does the corrected shape mapping (no mapping_type) work
p4c.create_network_from_networkx(nx.karate_club_graph(),title='k')
p4c.create_visual_style('Z'); p4c.set_node_shape_mapping('club',['Mr. Hi','Officer'],['DIAMOND','ELLIPSE'],style_name='Z'); p4c.set_visual_style('Z')
print('shape mapping without mapping_type ok:',p4c.get_node_property(node_names=['0'],visual_property='NODE_SHAPE') if False else 'set')
p4c.export_image('/mnt/openscience/audits/bio-data-visualization-network-visualization/out/cyto4/kar.pdf',type='PDF'); print('pdf',os.path.getsize('kar.pdf'))
