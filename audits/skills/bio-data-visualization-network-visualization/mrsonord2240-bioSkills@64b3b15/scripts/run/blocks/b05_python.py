import networkx as nx
import matplotlib.pyplot as plt
from networkx.algorithms.community import greedy_modularity_communities
import numpy as np

# Layout with fixed seed for reproducibility
pos = nx.spring_layout(G, k=1.5, seed=42)

# Compute attributes
degrees = dict(G.degree())
communities = list(greedy_modularity_communities(G))
node_to_community = {n: i for i, c in enumerate(communities) for n in c}

# Sizes scaled to degree
sizes = [100 + degrees[n] * 50 for n in G.nodes()]
colors = [node_to_community[n] for n in G.nodes()]

# Render in layers
fig, ax = plt.subplots(figsize=(10, 8))
nx.draw_networkx_edges(G, pos, alpha=0.3, edge_color='grey', width=0.5, ax=ax)
nodes = nx.draw_networkx_nodes(G, pos, node_size=sizes, node_color=colors,
                                cmap='tab20', edgecolors='black', linewidths=0.5, ax=ax)
# Label only high-degree (hub) nodes
hubs = [n for n in G.nodes() if degrees[n] >= 10]
nx.draw_networkx_labels(G, pos, labels={n: n for n in hubs}, font_size=8, ax=ax)
ax.axis('off')
plt.tight_layout()
plt.savefig('network.pdf', bbox_inches='tight', dpi=300)
