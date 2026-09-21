# SYNTHETIC planted-community graph: 4 blocks x 25 genes, 3 planted hubs, weights, one directed GRN variant
import numpy as np, networkx as nx, json, pandas as pd
rng = np.random.default_rng(7)
blocks = [list(range(i*25,(i+1)*25)) for i in range(4)]
names = {i: f"G{i:03d}" for i in range(100)}
G = nx.Graph()
G.add_nodes_from(names.values())
truth = {}
for b, nodes in enumerate(blocks):
    for n in nodes: truth[names[n]] = b
for i in range(100):
    for j in range(i+1, 100):
        same = truth[names[i]] == truth[names[j]]
        p = 0.30 if same else 0.01
        if rng.random() < p:
            w = rng.uniform(0.6,1.0) if same else rng.uniform(0.1,0.5)
            G.add_edge(names[i], names[j], weight=round(float(w),3), score=int(w*1000))
# planted hubs: one per block 0,1,2 connected to 40 random others each
hubs = [names[0], names[25], names[50]]
for h in hubs:
    others = rng.choice([n for n in names.values() if n != h], 40, replace=False)
    for o in others:
        if not G.has_edge(h,o):
            G.add_edge(h,o,weight=0.55,score=550)
nx.set_node_attributes(G, truth, 'block')
nx.set_node_attributes(G, dict(G.degree()), 'degree')
nx.write_graphml(G, 'data/synth_ppi.graphml')
pd.DataFrame([(u,v,d['weight'],d['score']) for u,v,d in G.edges(data=True)], columns=['a','b','weight','score']).to_csv('data/synth_ppi_edges.tsv', sep='\t', index=False)
pd.DataFrame({'gene':list(truth),'block':list(truth.values()),'degree':[G.degree(n) for n in truth]}).to_csv('data/synth_ppi_nodes.tsv', sep='\t', index=False)
json.dump({'hubs':hubs}, open('data/synth_meta.json','w'))
print('nodes',G.number_of_nodes(),'edges',G.number_of_edges(),'hub degrees',[G.degree(h) for h in hubs],'max non-hub deg',max(d for n,d in G.degree() if n not in hubs))
# directed GRN: 5 TFs -> 60 targets, TF cascade TF0->TF1->TF2->TF3->TF4
D = nx.DiGraph()
tfs=[f"TF{i}" for i in range(5)]
for a,b in zip(tfs,tfs[1:]): D.add_edge(a,b,sign='+')
for t in range(60):
    for tf in rng.choice(tfs, 2, replace=False): D.add_edge(str(tf),f"T{t:02d}",sign=str(rng.choice(['+','-'])))
nx.write_graphml(D,'data/synth_grn.graphml')
print('GRN',D.number_of_nodes(),D.number_of_edges())
