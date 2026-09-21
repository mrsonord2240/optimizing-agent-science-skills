from pyvis.network import Network

net = Network(height='700px', width='100%', bgcolor='white', font_color='black')
net.from_nx(G)

# Per-node styling
for node in G.nodes():
    net.get_node(node)['size'] = 10 + degrees[node] * 5
    net.get_node(node)['color'] = palette[node_to_community[node] % len(palette)]
    net.get_node(node)['title'] = f'{node}\nDegree: {degrees[node]}'

net.toggle_physics(True)
net.set_options('{"physics": {"forceAtlas2Based": {"gravitationalConstant": -50}}}')
net.save_graph('network.html')
