# Stress/multi-part input: compositionally-aware DA on the PREDICTED MetaCyc pathway
# table (real PICRUSt2 output on real moving-pictures ASVs), gut vs tongue (8 vs 9 real
# samples), per the Skill's own decision-tree row: "DA between groups on predicted table
# -> differential-abundance, run >=2 CoDA tools" and "ALDEx2 wants count-like
# features-as-rows, NOT relab-normalized output".
suppressMessages({
  library(ALDEx2)
  library(Maaslin2)
})

setwd("F:/OpenScience/audits/bio-microbiome-functional-prediction/work")

paths <- read.delim(gzfile("picrust2_out_real/pathways_out/path_abun_unstrat.tsv.gz"),
                     row.names = 1, check.names = FALSE)
cat("Pathway table dims (pathways x samples):", dim(paths), "\n")

meta <- read.delim("F:/OpenScience/audit-envs/microbiome-metagenomics-analyst/public-data/moving-pictures/sample_metadata.tsv")
meta <- meta[-1, ]  # drop the '#q2:types' QIIME2 type-declaration row, not real sample data
colnames(meta)[1] <- "sample_id"
rownames(meta) <- meta$sample_id
cat("Metadata columns:", colnames(meta), "\n")

samples_in_table <- colnames(paths)
meta_sub <- meta[samples_in_table, ]
groups <- meta_sub$body.site
cat("Group counts:\n"); print(table(groups))

keep <- groups %in% c("gut", "tongue")
paths_sub <- as.matrix(paths[, keep])
storage.mode(paths_sub) <- "numeric"
groups_sub <- factor(groups[keep])
cat("Subset dims:", dim(paths_sub), " groups:", table(groups_sub), "\n")

# ALDEx2 -- features as rows (pathways), samples as columns; raw predicted abundances
# (SKILL.md: pass count-like predicted abundances, NOT relab-normalized, features as rows)
set.seed(42)
aldex_counts <- round(paths_sub)  # PICRUSt2 predicted abundances are non-integer; round for aldex's count model
storage.mode(aldex_counts) <- "integer"
rownames(aldex_counts) <- rownames(paths_sub)
aldex_res <- aldex(aldex_counts, as.character(groups_sub), mc.samples = 128, test = "t", effect = TRUE, denom = "all")
sig_aldex <- aldex_res[aldex_res$we.eBH < 0.05, ]
cat("\nALDEx2: ", nrow(sig_aldex), " / ", nrow(aldex_res), " pathways significant at we.eBH<0.05\n")
print(head(sig_aldex[order(sig_aldex$we.eBH), c("effect", "we.eBH")], 10))

# MaAsLin2 -- wants features as COLUMNS, samples as ROWS (opposite of ALDEx2)
maaslin_input <- as.data.frame(t(paths_sub))
maaslin_meta <- data.frame(body_site = as.character(groups_sub), row.names = colnames(paths_sub))
fit <- Maaslin2(
  input_data = maaslin_input,
  input_metadata = maaslin_meta,
  output = "maaslin2_out",
  fixed_effects = "body_site",
  normalization = "TSS",
  transform = "LOG",
  min_prevalence = 0.1,
  plot_heatmap = FALSE,
  plot_scatter = FALSE
)
maaslin_sig <- read.delim("maaslin2_out/significant_results.tsv")
cat("\nMaAsLin2: ", nrow(maaslin_sig), " significant associations (qval<0.25 default)\n")

# Intersection (per Nearing 2022 guidance the skill cites)
aldex_hits <- rownames(sig_aldex)
maaslin_hits <- unique(maaslin_sig$feature)
inter <- intersect(aldex_hits, maaslin_hits)
cat("\nIntersection ALDEx2 & MaAsLin2:", length(inter), "pathways\n")
print(inter)

# Corrected intersection: MaAsLin2 sanitizes feature names via make.names() (hyphens -> dots),
# ALDEx2 preserves the original MetaCyc IDs (with hyphens). A naive intersect() on the raw
# names silently returns empty even when both tools flag the same pathways.
aldex_hits_norm <- make.names(aldex_hits)
maaslin_hits_norm <- make.names(maaslin_hits)
inter_norm <- intersect(aldex_hits_norm, maaslin_hits_norm)
cat("\nCorrected (name-normalized) intersection ALDEx2 & MaAsLin2:", length(inter_norm),
    "/ ALDEx2 hits:", length(aldex_hits_norm), "/ MaAsLin2 hits:", length(maaslin_hits_norm), "\n")
