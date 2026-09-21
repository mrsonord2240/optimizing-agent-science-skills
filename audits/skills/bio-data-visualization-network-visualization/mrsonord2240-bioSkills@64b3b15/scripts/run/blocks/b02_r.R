library(ggraph)
ggraph(g, layout = 'fr') +                          # Fruchterman-Reingold
    geom_edge_link(alpha = 0.3) +
    geom_node_point()

ggraph(g, layout = 'kk') +                          # Kamada-Kawai
ggraph(g, layout = 'circle') +
ggraph(g, layout = 'graphopt') +                    # OpenOrd-style for large
