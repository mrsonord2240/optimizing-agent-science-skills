# Input 5e: which networkx GraphML files does Cytoscape 3.10.4 import? (data/synth_ppi.graphml gave HTTP 500)
import networkx as nx, py4cytoscape as p4c, os, shutil
A='/mnt/openscience/audits/bio-data-visualization-network-visualization'
os.makedirs(A+'/out/cyto5',exist_ok=True); os.chdir(A+'/out/cyto5')
def t(label,G,fn=None,**kw):
    fn=fn or label+'.graphml'; nx.write_graphml(G,fn,**kw)
    try:
        p4c.import_network_from_file(A+'/out/cyto5/'+fn); print(f'{label:28s} OK  cy {len(p4c.get_all_nodes())}/{len(p4c.get_all_edges())} nx {G.number_of_nodes()}/{G.number_of_edges()}')
    except Exception as e: print(f'{label:28s} FAIL',str(e).split("Error processing")[-1][:80])
G=nx.karate_club_graph(); t('karate_raw',G)
H=nx.Graph(G); [H.nodes[n].clear() for n in H]; t('karate_noattr',H)
E=nx.Graph(); E.add_edge('a','b'); t('two_nodes_str',E)
P=nx.read_graphml(A+'/data/synth_ppi.graphml'); t('synth_ppi',P)
Q=nx.Graph(P); [ (Q.nodes[n].pop('degree'),) for n in Q]; t('synth_no_degree',Q)
R=nx.Graph(P); [R.nodes[n].pop('block') for n in R]; [R.nodes[n].pop('degree') for n in R]; t('synth_nodeattrs_removed',R)
S=nx.Graph(P); 
for u,v,d in S.edges(data=True): d.pop('score')
t('synth_noscore',S)
T=nx.Graph(); T.add_edge('a','b',weight=0.5); t('tiny_float_edge',T)
U=nx.Graph(); U.add_edge('a','b',score=5); t('tiny_int_edge',U)
V=nx.Graph(); V.add_node('a',degree=3); V.add_edge('a','b'); t('tiny_int_node',V)
