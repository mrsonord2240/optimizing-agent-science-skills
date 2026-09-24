# Exact-commit re-audit input 5: bandwidth, trim, N guidance, and direct source checks.
# Run with: r.sh reaudit_i5_nrd_trim.R <SKILL.md>
args <- commandArgs(trailingOnly = TRUE)
stopifnot(length(args) == 1L)
skill <- paste(readLines(args[[1L]], warn = FALSE), collapse = '\n')
set.seed(20260923)
x <- c(rnorm(60, 0, 1), rnorm(60, 4, 1))
stopifnot(stats::bw.nrd(x) > stats::bw.nrd0(x),
          abs(stats::bw.nrd(x) / stats::bw.nrd0(x) - 1.06 / .9) < 1e-10)

# Trim=TRUE is bounded by observed data; this directly verifies the guidance for bounded data.
bounded <- data.frame(group = 'bounded', value = rexp(100, rate = 1))
p_trim <- ggplot2::ggplot(bounded, ggplot2::aes(group, value)) + ggplot2::geom_violin(trim = TRUE)
drawn <- ggplot2::ggplot_build(p_trim)$data[[1L]]$y
stopifnot(min(drawn) >= min(bounded$value) - 1e-12, max(drawn) <= max(bounded$value) + 1e-12)

for (text in c('3-10', '10-29', '30-200', '201-1000', '>1000',
               'N < 30, show every point', 'N >= 201', 'both ordered conditions present and N >= 30 each')) {
  stopifnot(grepl(text, skill, fixed = TRUE))
}
cat(sprintf('PASS i5: bw.nrd/bw.nrd0=%.12f; trim=TRUE observed range [%.4f, %.4f]; consolidated N guidance present\n',
            stats::bw.nrd(x) / stats::bw.nrd0(x), min(drawn), max(drawn)))
