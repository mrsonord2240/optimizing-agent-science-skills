# Input 8 regression: verify the Version Compatibility block's gheatmap claim.
# Claim in SKILL.md (line 14): "gheatmap() is call-dependent: a plain gheatmap(ggtree(tr), df)
# succeeds, but calling it after prior geoms plus new_scale_fill() in a composite figure can
# fail (reproduced here: `new_geom_point_g_gtree()` requires the following missing aesthetics: x)."
suppressPackageStartupMessages({library(ggtree); library(ggtreeExtra); library(ggplot2); library(ggnewscale); library(ape)})

tr <- read.tree('data/primates16_true.nwk')
df <- data.frame(row.names = tr$tip.label, trait = seq_along(tr$tip.label))

cat('=== Plain gheatmap(ggtree(tr), df) ===\n')
p_plain <- tryCatch({
  built <- ggplot_build(gheatmap(ggtree(tr), df))
  'OK'
}, error = function(e) paste('ERROR:', conditionMessage(e)))
cat(p_plain, '\n\n')

cat('=== Composite: geom_tippoint + new_scale_fill() + gheatmap ===\n')
p_composite <- tryCatch({
  p <- ggtree(tr) + geom_tippoint(aes(color = 'x')) + new_scale_fill()
  built <- ggplot_build(gheatmap(p, df))
  'OK'
}, error = function(e) paste('ERROR:', conditionMessage(e)))
cat(p_composite, '\n\n')

cat('=== Fallback: geom_fruit on the same composite case ===\n')
p_fruit <- tryCatch({
  p <- ggtree(tr) + geom_tippoint(aes(color = 'x')) + new_scale_fill()
  meta <- data.frame(label = tr$tip.label, trait = seq_along(tr$tip.label))
  built <- ggplot_build(p + geom_fruit(data = meta, geom = geom_tile, mapping = aes(y = label, fill = trait)))
  'OK'
}, error = function(e) paste('ERROR:', conditionMessage(e)))
cat(p_fruit, '\n')
