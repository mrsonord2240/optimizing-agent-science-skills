import networkx as nx, numpy as np
D=nx.read_graphml('/mnt/openscience/audits/bio-data-visualization-network-visualization/data/synth_grn.graphml')
pos=nx.nx_pydot.graphviz_layout(D,prog='dot')
print('graphviz dot layout n',len(pos)); ys={n:pos[n][1] for n in D}
tf=[ys[f'TF{i}'] for i in range(5)]; print('TF cascade y (TF0..TF4) strictly decreasing top->bottom:',all(tf[i]>tf[i+1] for i in range(4)),tf)
print('every regulator->target edge points downward in dot layout:',all(ys[u]>ys[v] for u,v in D.edges()))
pos2=nx.nx_pydot.graphviz_layout(D,prog='dot'); print('dot layout deterministic:',pos==pos2)
