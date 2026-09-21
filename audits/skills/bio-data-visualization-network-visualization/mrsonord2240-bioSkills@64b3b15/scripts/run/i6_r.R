# Input 6: R route -- SKILL blocks 2 (layouts) and 4 (edge bundling) verbatim, then repaired; content assertions; igraph seed/community checks
suppressMessages({library(igraph); library(ggraph); library(ggplot2)})
A <- "F:/OpenScience/audits/bio-data-visualization-network-visualization"
setwd(A)
cat("igraph", as.character(packageVersion("igraph")), "ggraph", as.character(packageVersion("ggraph")), "ggplot2", as.character(packageVersion("ggplot2")), "\n")
ed <- read.delim("data/synth_ppi_edges.tsv"); nd <- read.delim("data/synth_ppi_nodes.tsv")
g <- graph_from_data_frame(ed[, c("a","b","weight")], directed = FALSE, vertices = nd)
cat("g:", vcount(g), "nodes", ecount(g), "edges\n")
b2 <- paste(readLines("run/blocks/b02_r.R", encoding = "UTF-8"), collapse = "\n")
cat("--- block 2 verbatim: parse\n")
r <- try(parse(text = b2), silent = TRUE); if (inherits(r, "try-error")) cat("PARSE ERROR:", conditionMessage(attr(r, "condition")), "\n") else cat("parses,", length(r), "expressions\n")
b2b <- paste(readLines("run/blocks/b02_r.R", encoding = "UTF-8"), collapse = "\n")
# evaluate each ggraph() call separately (as the block intends): add nodes/edges to each so it draws
for (lay in c("fr", "kk", "circle", "graphopt")) {
  set.seed(42)
  p <- ggraph(g, layout = lay) + geom_edge_link(alpha = 0.3) + geom_node_point()
  b <- ggplot_build(p); d <- p$data
  f <- file.path(A, "out", paste0("i6_", lay, ".png")); ggsave(f, p, width = 5, height = 4, dpi = 80)
  cat(sprintf("layout %-9s nodes drawn %d (graph %d) | edge layer rows %d (graph %d) | png %d B\n", lay, nrow(d), vcount(g), nrow(b$data[[1]])/2, ecount(g), file.size(f)))
}
# seed reproducibility
set.seed(42); l1 <- create_layout(g, "fr"); set.seed(42); l2 <- create_layout(g, "fr"); set.seed(43); l3 <- create_layout(g, "fr")
cat("ggraph fr same seed identical:", isTRUE(all.equal(l1[, c("x","y")], l2[, c("x","y")])), "| other seed differs:", !isTRUE(all.equal(l1[, c("x","y")], l3[, c("x","y")])), "\n")
l4 <- create_layout(g, "fr"); l5 <- create_layout(g, "fr"); cat("no set.seed: two calls identical:", isTRUE(all.equal(l4[, c("x","y")], l5[, c("x","y")])), "\n")
set.seed(42); k1 <- create_layout(g, "kk"); set.seed(43); k2 <- create_layout(g, "kk"); cat("kk deterministic across seeds:", isTRUE(all.equal(k1[, c("x","y")], k2[, c("x","y")])), "\n")
# communities: igraph louvain (seeded) vs planted truth and vs networkx result saved by python
set.seed(42); cl <- cluster_louvain(g, weights = E(g)$weight)
tab <- table(nd$block[match(V(g)$name, nd$gene)], membership(cl)); cat("louvain communities:", length(cl), " modularity", round(modularity(cl), 3), "\n"); print(tab)
cg <- cluster_fast_greedy(g); cat("fast_greedy communities:", length(cg), "\n")
# community-coloured ggraph, degree size -- counts and mapping
V(g)$comm <- factor(membership(cl)); V(g)$deg <- degree(g)
set.seed(42); p <- ggraph(g, "fr") + geom_edge_link(aes(width = weight), alpha = 0.3) + scale_edge_width(range = c(0.2, 1.2)) + geom_node_point(aes(size = deg, colour = comm)) + theme_graph()
d <- p$data; cat("node table matches degree:", all(d$deg == degree(g)), " colour col matches louvain:", all(as.integer(as.character(d$comm)) == membership(cl)), "\n")
ggsave("out/i6_comm.png", p, width = 6, height = 5, dpi = 90)
# block 4 verbatim on a proper hierarchy (flare): variables graph/from_idx/to_idx are NOT defined by the block
b4 <- paste(readLines("run/blocks/b04_r.R", encoding = "UTF-8"), collapse = "\n")
cat("--- block 4 verbatim, no variables defined\n")
r <- try(eval(parse(text = b4)), silent = TRUE); cat(if (inherits(r, "try-error")) paste("ERROR:", conditionMessage(attr(r, "condition"))) else "ran", "\n")
cat("--- block 4 with the flare example from ggraph\n")
edges <- flare$edges; vertices <- flare$vertices; imports <- flare$imports
graph <- graph_from_data_frame(edges, vertices = vertices)
from_idx <- match(imports$from, vertices$name); to_idx <- match(imports$to, vertices$name)
p <- ggraph(graph, layout = 'dendrogram', circular = TRUE) +
    geom_conn_bundle(data = get_con(from = from_idx, to = to_idx), alpha = 0.4, tension = 0.8, edge_colour = 'grey60') +
    geom_node_point() + theme_void()
b <- ggplot_build(p); cat("bundle: connections requested", length(from_idx), " paths in layer", length(unique(b$data[[1]]$group)), "\n")
ggsave("out/i6_bundle.png", p, width = 6, height = 6, dpi = 80); cat("bundle png", file.size("out/i6_bundle.png"), "B\n")
