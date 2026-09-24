# Exact-commit re-audit input 1: current R encodings and supplied focused test.
# Run with: F:/OpenScience/audit-envs/data-visualization/r.sh reaudit_i1_r_current.R <example>
args <- commandArgs(trailingOnly = TRUE)
stopifnot(length(args) == 1L)
example_path <- normalizePath(args[[1L]], mustWork = TRUE)

source(example_path)
stopifnot(requireNamespace('ggbeeswarm', quietly = TRUE), requireNamespace('ggdist', quietly = TRUE))

# Re-run the current inline box+jitter, guarded violin, and quasirandom patterns.
df <- data.frame(group = factor(rep(c('Control', 'Treated'), each = 40L)),
                 value = c(seq(1, 4, length.out = 40L), seq(2, 6, length.out = 40L)))
p_box <- ggplot2::ggplot(df, ggplot2::aes(group, value, fill = group)) +
  ggplot2::geom_boxplot(outlier.shape = NA) +
  ggplot2::geom_point(position = ggplot2::position_jitter(width = .2, height = 0, seed = 20260923))
p_violin <- ggplot2::ggplot(df, ggplot2::aes(group, value, fill = group)) +
  ggplot2::geom_violin(trim = TRUE, bw = safe_violin_bw(df))
p_quasi <- ggplot2::ggplot(df, ggplot2::aes(group, value, colour = group)) +
  ggbeeswarm::geom_quasirandom(method = 'quasirandom', width = .3) +
  ggplot2::stat_summary(fun = median, geom = 'crossbar', width = .5)
stopifnot(nrow(ggplot2::ggplot_build(p_box)$data[[2L]]) == nrow(df),
          nrow(ggplot2::ggplot_build(p_violin)$data[[1L]]) > 0L,
          nrow(ggplot2::ggplot_build(p_quasi)$data[[1L]]) == nrow(df))
ggplot2::ggsave('reaudit_i1_current_r.png', p_box + ggplot2::ggtitle('current R box + seeded points'), width = 5, height = 3, dpi = 120)
stopifnot(file.info('reaudit_i1_current_r.png')$size > 2000L)
cat('PASS i1: current inline R encodings; png=', file.info('reaudit_i1_current_r.png')$size, '\n', sep = '')
