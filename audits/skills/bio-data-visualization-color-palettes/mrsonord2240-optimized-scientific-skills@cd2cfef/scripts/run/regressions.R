# Independent re-audit regressions for inputs 1, 2, 3, 5, and new input 6.
# Inputs are synthetic and were created in the archived pre-fix audit.
args <- commandArgs(trailingOnly = TRUE)
stopifnot(length(args) == 2)
data_dir <- normalizePath(args[[1]], mustWork = TRUE)
fig_dir <- normalizePath(args[[2]], mustWork = TRUE)

suppressPackageStartupMessages({
    library(colorspace)
    library(ggplot2)
    library(ggsci)
    library(patchwork)
    library(RColorBrewer)
    library(scales)
    library(scico)
})

min_lab_distance <- function(palette) {
    min(dist(coords(as(hex2RGB(palette), 'LAB'))))
}

# Input 1: stable named Okabe-Ito mapping, reserve grey, and redundant shape.
umap <- read.csv(file.path(data_dir, 'synthetic_umap_celltypes.csv'))
rename_levels <- c(
    'T cell' = 'T', 'B cell' = 'B', 'NK cell' = 'NK',
    'Monocyte' = 'Monocyte', 'Dendritic' = 'Dendritic',
    'Platelet' = 'Platelet', 'Erythroid' = 'Erythroid',
    'Unassigned' = 'Unassigned'
)
umap$cell_type <- factor(unname(rename_levels[umap$cell_type]),
                         levels = unname(rename_levels))
cell_levels <- levels(umap$cell_type)
okabe_ito <- c('#E69F00', '#56B4E9', '#009E73', '#F0E442',
               '#0072B2', '#D55E00', '#CC79A7')
cell_colors <- c(setNames(okabe_ito, cell_levels[1:7]), Unassigned = '#BBBBBB')
shape_values <- c(setNames(rep(16, 7), cell_levels[1:7]), Unassigned = 4)

full_plot <- ggplot(umap, aes(UMAP1, UMAP2, color = cell_type, shape = cell_type)) +
    geom_point(size = 1.1, alpha = 0.8) +
    scale_color_manual(values = cell_colors, drop = FALSE) +
    scale_shape_manual(values = shape_values, drop = FALSE) +
    labs(title = 'Full mapping', color = 'Cell type', shape = 'Cell type') +
    theme_minimal(base_size = 9)
subset_umap <- droplevels(subset(umap, cell_type != 'T'))
subset_plot <- ggplot(subset_umap,
                      aes(UMAP1, UMAP2, color = cell_type, shape = cell_type)) +
    geom_point(size = 1.1, alpha = 0.8) +
    scale_color_manual(values = cell_colors, drop = FALSE) +
    scale_shape_manual(values = shape_values, drop = FALSE) +
    labs(title = 'Subset without T', color = 'Cell type', shape = 'Cell type') +
    theme_minimal(base_size = 9)

mapping_for <- function(plot, data) {
    built <- ggplot_build(plot)$data[[1]]
    tapply(built$colour, data$cell_type, function(x) unique(toupper(x)))
}
full_mapping <- mapping_for(full_plot, umap)
subset_mapping <- mapping_for(subset_plot, subset_umap)
stopifnot(identical(unname(full_mapping[names(subset_mapping)]),
                    unname(subset_mapping)))

cvd_palettes <- list(deutan = deutan(cell_colors),
                     protan = protan(cell_colors),
                     tritan = tritan(cell_colors))
cvd_min <- vapply(cvd_palettes, min_lab_distance, numeric(1))
stopifnot(all(is.finite(cvd_min)), all(cvd_min > 0))
png(file.path(fig_dir, 'i1_named_okabe_stability.png'), 1500, 700, res = 140)
print(full_plot + subset_plot + plot_layout(guides = 'collect'))
invisible(dev.off())

# Input 2: built-in vik centre is intentional; exact white belongs to a custom ramp.
lfc <- read.csv(file.path(data_dir, 'synthetic_skewed_lfc.csv'))
lfc$x <- as.integer(factor(lfc$sample, levels = unique(lfc$sample)))
lfc$y <- as.integer(factor(lfc$gene, levels = unique(lfc$gene)))
vmax <- quantile(abs(lfc$lfc), 0.99, na.rm = TRUE)
stopifnot(is.finite(vmax), vmax > 0)
vik_plot <- ggplot(lfc, aes(x, y, fill = lfc)) + geom_tile() +
    scale_fill_scico(palette = 'vik', midpoint = 0,
                     limits = c(-vmax, vmax), oob = scales::squish) +
    labs(title = 'vik: symmetric q99, zero anchored') + theme_minimal(base_size = 9)
custom_plot <- ggplot(lfc, aes(x, y, fill = lfc)) + geom_tile() +
    scale_fill_gradient2(low = '#0072B2', mid = '#FFFFFF', high = '#D55E00',
                         midpoint = 0, limits = c(-vmax, vmax),
                         oob = scales::squish) +
    labs(title = 'Custom exact-white centre') + theme_minimal(base_size = 9)
vik_centre <- scico(255, palette = 'vik')[[128]]
stopifnot(vik_centre == '#EBE5E0')
custom <- colorRampPalette(c('#0072B2', '#FFFFFF', '#D55E00'))(101)
stopifnot(custom[[51]] == '#FFFFFF')
png(file.path(fig_dir, 'i2_diverging_centres.png'), 1400, 650, res = 140)
print(vik_plot + custom_plot)
invisible(dev.off())

# Input 3: actual desaturated palette and three independent CVD transforms.
batlow <- scico(10, palette = 'batlow')
batlow_l <- coords(as(hex2RGB(batlow), 'LAB'))[, 'L']
stopifnot(all(diff(batlow_l) >= 0) || all(diff(batlow_l) <= 0))
turbo <- viridis::viridis(256, option = 'turbo')
turbo_l <- coords(as(hex2RGB(turbo), 'LAB'))[, 'L']
stopifnot(!(all(diff(turbo_l) >= 0) || all(diff(turbo_l) <= 0)))
png(file.path(fig_dir, 'i3_grayscale_cvd.png'), 1500, 800, res = 140)
op <- par(mfrow = c(2, 3), mar = c(2, 2, 3, 1))
show_col(batlow); title('batlow')
show_col(desaturate(batlow)); title('batlow desaturated')
show_col(deutan(batlow)); title('batlow deutan')
show_col(protan(batlow)); title('batlow protan')
show_col(tritan(batlow)); title('batlow tritan')
show_col(desaturate(turbo[seq(1, 256, length.out = 10)])); title('turbo desaturated')
par(op)
invisible(dev.off())

# Input 5: journal palettes are imperfect; >8 categories require another encoding.
journal <- list(
    npg = pal_npg('nrc')(10),
    aaas = pal_aaas('default')(10),
    lancet = pal_lancet('lanonc')(9)
)
journal_min <- vapply(journal, function(p) min_lab_distance(deutan(p)), numeric(1))
stopifnot(all(is.finite(journal_min)), all(journal_min > 0))

# New input 6: 30 clusters. Do not assign 30 identity hues; facet and direct-label.
set.seed(20260927)
cluster_levels <- sprintf('C%02d', 1:30)
centres <- expand.grid(col = 1:6, row = 1:5)
many <- do.call(rbind, lapply(seq_along(cluster_levels), function(i) {
    data.frame(
        x = rnorm(35, centres$col[[i]], 0.12),
        y = rnorm(35, centres$row[[i]], 0.12),
        cluster = cluster_levels[[i]]
    )
}))
many$cluster <- factor(many$cluster, levels = cluster_levels)
facet_plot <- ggplot(many, aes(x, y)) +
    geom_point(color = '#0072B2', alpha = 0.55, size = 0.8) +
    facet_wrap(~ cluster, ncol = 6, scales = 'free') +
    labs(title = '30 groups: direct facet labels, one accessible accent') +
    theme_minimal(base_size = 8) +
    theme(axis.text = element_blank(), axis.title = element_blank(),
          panel.grid = element_blank())
stopifnot(length(unique(ggplot_build(facet_plot)$data[[1]]$colour)) == 1,
          nlevels(many$cluster) == 30)
ggsave(file.path(fig_dir, 'i6_thirty_groups_faceted.png'), facet_plot,
       width = 12, height = 9, dpi = 130)

cat('R REGRESSIONS PASS\n')
cat('Input 1 stable named mapping: TRUE; CVD minima:',
    paste(names(cvd_min), round(cvd_min, 2), collapse = '; '), '\n')
cat('Input 2 q99:', unname(vmax), 'vik centre:', vik_centre,
    'custom centre:', custom[[51]], '\n')
cat('Input 3 batlow L* monotonic: TRUE; turbo L* monotonic: FALSE\n')
cat('Input 5 journal deutan minima:',
    paste(names(journal_min), round(journal_min, 2), collapse = '; '), '\n')
cat('Input 6 groups:', nlevels(many$cluster),
    'identity colours used:', length(unique(ggplot_build(facet_plot)$data[[1]]$colour)), '\n')
