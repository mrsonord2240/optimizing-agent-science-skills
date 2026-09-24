# Exact-commit re-audit input 3: tied/all-zero fallback and split-violin guards/sides.
# Run with: r.sh reaudit_i3_split_edges.R <example>
args <- commandArgs(trailingOnly = TRUE)
stopifnot(length(args) == 1L)
source(normalizePath(args[[1L]], mustWork = TRUE))

# Both tied and all-zero strata select the one panel-wide nrd0 fallback and still render.
tied <- data.frame(group = rep(c('Zero', 'Tied', 'Variable'), each = 12L),
                   value = c(rep(0, 12L), rep(c(0, 1), 6L), seq(-1, 1, length.out = 12L)))
stopifnot(identical(safe_violin_bw(tied), 'nrd0'))
tied_plot <- ggplot2::ggplot(tied, ggplot2::aes(group, value, fill = group)) +
  ggplot2::geom_violin(bw = safe_violin_bw(tied), trim = TRUE) +
  ggplot2::geom_point(position = ggplot2::position_jitter(seed = 1))
tied_build <- ggplot2::ggplot_build(tied_plot)
ggplot2::ggsave('reaudit_i3_tied.png', tied_plot, width = 5, height = 3, dpi = 120)
stopifnot(nrow(tied_build$data[[1L]]) > 0L, file.info('reaudit_i3_tied.png')$size > 2000L)

# Input is deliberately incomplete / low-N: only three complete 40x40 clusters survive.
raw <- df_paired_raw
prepared <- prepare_split_violin_data(raw, min_n = 30L)
stopifnot(identical(levels(prepared$cluster), c('Cluster 1', 'Cluster 2', 'Cluster 3')),
          all(table(prepared$cluster, prepared$condition) == 40L))

# Invalid condition type and a valid-but-empty eligibility set both fail safely / result empty.
bad_condition <- raw
bad_condition$condition <- factor(as.character(bad_condition$condition))
bad <- try(prepare_split_violin_data(bad_condition, min_n = 30L), silent = TRUE)
stopifnot(inherits(bad, 'try-error'))
low <- raw[raw$cluster == 'Too small', ]
low$condition <- ordered(low$condition, levels = c('Control', 'Treatment'))
stopifnot(nrow(prepare_split_violin_data(low, min_n = 30L)) == 0L)

# The filtered data maintains an ordered condition factor. With every cluster complete, group order
# is stable (Control then Treatment within each cluster) before the geom receives it.
split_groups <- interaction(prepared$cluster, prepared$condition, lex.order = TRUE)
expected_groups <- rep(c('Cluster 1.Control', 'Cluster 1.Treatment', 'Cluster 2.Control',
                         'Cluster 2.Treatment', 'Cluster 3.Control', 'Cluster 3.Treatment'), each = 40L)
stopifnot(identical(as.character(split_groups), expected_groups))
plot <- ggplot2::ggplot(prepared, ggplot2::aes(cluster, expression, fill = condition,
                group = interaction(cluster, condition, lex.order = TRUE))) +
  introdataviz::geom_split_violin(trim = TRUE, bw = safe_violin_bw(
    transform(prepared, g = split_groups), 'g', 'expression')) +
  ggplot2::geom_boxplot(width = .15, position = ggplot2::position_dodge(.5), outlier.shape = NA)
build <- ggplot2::ggplot_build(plot)
ggplot2::ggsave('reaudit_i3_split.png', plot, width = 6, height = 4, dpi = 120)
stopifnot(nrow(build$data[[1L]]) > 0L, nrow(build$data[[2L]]) == 6L,
          file.info('reaudit_i3_split.png')$size > 2000L)
cat('PASS i3: all-zero/tied fallback, missing/low-N split guards, and stable complete-grid group order\n')
