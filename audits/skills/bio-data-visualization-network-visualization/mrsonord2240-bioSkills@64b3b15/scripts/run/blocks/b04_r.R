library(ggraph)
ggraph(graph, layout = 'dendrogram', circular = TRUE) +
    geom_conn_bundle(data = get_con(from = from_idx, to = to_idx),
                     alpha = 0.4, tension = 0.8, edge_colour = 'grey60') +
    geom_node_point() +
    theme_void()
