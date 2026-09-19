data_dir <- 'F:/OpenScience/audits/bio-single-cell-scatac-analysis/data/reaudit4_20260919'
run_dir <- file.path(data_dir, 'chromvar_runs')

seeded <- lapply(1:4, function(i) readRDS(file.path(run_dir, paste0('seeded_run', i, '.rds'))))

cat('--- Seeded run pairwise identical() checks ---\n')
for (i in 2:4) {
  cat('run1 vs run', i, ': bg_peaks identical =', identical(seeded[[1]]$bg_peaks, seeded[[i]]$bg_peaks),
      ' | z identical =', identical(seeded[[1]]$z, seeded[[i]]$z),
      ' | diff_motifs identical =', identical(seeded[[1]]$diff_motifs, seeded[[i]]$diff_motifs), '\n')
}

unseeded <- lapply(1:2, function(i) readRDS(file.path(run_dir, paste0('unseeded_run', i, '.rds'))))
cat('\n--- Unseeded negative control ---\n')
cat('bg_peaks identical =', identical(unseeded[[1]]$bg_peaks, unseeded[[2]]$bg_peaks), '\n')
cat('fraction of bg_peaks matrix entries differing =', mean(unseeded[[1]]$bg_peaks != unseeded[[2]]$bg_peaks), '\n')
cat('z identical =', identical(unseeded[[1]]$z, unseeded[[2]]$z), '\n')
top10_1 <- rownames(head(unseeded[[1]]$diff_motifs[order(unseeded[[1]]$diff_motifs$p_val_adj),], 10))
top10_2 <- rownames(head(unseeded[[2]]$diff_motifs[order(unseeded[[2]]$diff_motifs$p_val_adj),], 10))
cat('top10 overlap (unseeded run1 vs run2):', length(intersect(top10_1, top10_2)), '/10\n')

cat('\n--- File hash comparison (md5sum of the whole saved object) ---\n')
for (i in 1:4) {
  f <- file.path(run_dir, paste0('seeded_run', i, '.rds'))
  cat('seeded_run', i, ':', tools::md5sum(f), '\n')
}
