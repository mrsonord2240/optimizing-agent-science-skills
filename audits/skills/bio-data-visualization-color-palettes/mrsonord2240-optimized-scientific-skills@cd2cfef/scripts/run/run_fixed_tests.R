# Run the fixed Skill's shipped examples while copying visual outputs into this audit.
args <- commandArgs(trailingOnly = TRUE)
stopifnot(length(args) == 2)
skill_dir <- normalizePath(args[[1]], mustWork = TRUE)
fig_dir <- normalizePath(args[[2]], mustWork = TRUE)

# Re-render the four-panel shipped example to a deterministic live-audit path.
old_wd <- getwd()
on.exit(setwd(old_wd), add = TRUE)
setwd(fig_dir)
example_env <- new.env(parent = globalenv())
source(file.path(skill_dir, 'examples', 'palette_examples.R'), local = example_env)
ggplot2::ggsave('i5_palette_examples_fixed.png', example_env$combined,
                width = 12, height = 10, dpi = 120)
stopifnot(file.info('i5_palette_examples_fixed.png')$size > 1000)

pdf('i5_palettes_phd_fixed.pdf', width = 9, height = 7)
source(file.path(skill_dir, 'examples', 'palettes_phd.R'), local = new.env())
invisible(dev.off())
stopifnot(file.info('i5_palettes_phd_fixed.pdf')$size > 1000)

cat('FIXED R TESTS AND EXAMPLES PASS\n')
