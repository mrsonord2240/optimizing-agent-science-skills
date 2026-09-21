import networkx as nx

# Spring / Fruchterman-Reingold (general)
pos = nx.spring_layout(G, k=1/np.sqrt(len(G)), iterations=100, seed=42)

# Kamada-Kawai (better for small dense)
pos = nx.kamada_kawai_layout(G)

# Circular
pos = nx.circular_layout(G)

# Shell (hub at center, periphery outside)
pos = nx.shell_layout(G, nlist=[hub_nodes, periphery_nodes])

# Spectral (reveals clusters)
pos = nx.spectral_layout(G)

# Bipartite (two sets)
pos = nx.bipartite_layout(G, top_nodes)

# Hierarchical (DAG)
pos = nx.nx_pydot.graphviz_layout(G, prog='dot')   # requires graphviz
