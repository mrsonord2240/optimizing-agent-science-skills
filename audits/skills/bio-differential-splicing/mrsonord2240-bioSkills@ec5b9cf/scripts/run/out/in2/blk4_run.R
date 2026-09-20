cluster_sig <- read.table('ds_results_cluster_significance.txt', header = TRUE, sep = '\t')
intron_effects <- read.table('ds_results_effect_sizes.txt', header = TRUE, sep = '\t')

sig_clusters <- subset(cluster_sig, p.adjust < 0.05)
print(sig_clusters); print(intron_effects)
