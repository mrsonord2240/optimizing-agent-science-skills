import py4cytoscape as p4c
# Cytoscape desktop must be running

p4c.create_network_from_networkx(G, title='PPI')
p4c.layout_network('force-directed')

# Custom style
style_name = 'DegreeStyle'
p4c.create_visual_style(style_name)
p4c.set_node_size_mapping('degree', [1, 5, 20], [30, 60, 120],
                            mapping_type='c', style_name=style_name)
p4c.set_node_color_mapping('degree', [1, 10, 20], ['#FFFFCC', '#FD8D3C', '#BD0026'],
                             mapping_type='c', style_name=style_name)
p4c.set_visual_style(style_name)

# Export
p4c.export_image('network.pdf', type='PDF')
