a <- deparse(parse('F:/OpenScience/audits/bio-data-visualization-volcano-and-ma-plots/delta-dv1-20261003/scratch/bio-data-visualization-volcano-and-ma-plots/scripts/volcano_phd.R', keep.source = FALSE))
b <- deparse(parse('F:/OpenScience/wt/normalize-dv-lane1/skills/bio-data-visualization-volcano-and-ma-plots/scripts/volcano_phd.R', keep.source = FALSE))
cat('R parsed expressions identical (comments dropped):', identical(a, b), ' lines:', length(a), '\n')
