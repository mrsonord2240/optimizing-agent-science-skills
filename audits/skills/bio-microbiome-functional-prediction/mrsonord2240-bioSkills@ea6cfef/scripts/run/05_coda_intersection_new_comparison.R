# Re-audit new input: independently re-derive the CoDA cross-tool ID-mismatch finding on a
# DIFFERENT comparison than the fix log used (fixer used gut(8) vs tongue(9) with
# ALDEx2 + MaAsLin2; this uses gut(8) vs left palm(8) -- a comparison the fixer never ran --
# on MY OWN freshly-generated PICRUSt2 pathway table (not the original audit's cached
# picrust2_out_real). Also adds LinDA as a third tool -- a negative control, since LinDA
# (like ALDEx2) does NOT sanitize feature names via make.names(), so its naive vs normalized
# intersection with ALDEx2 should already agree, isolating the mismatch to MaAsLin2's
# make.names() behavior specifically.
# NOTE: an earlier run of this script used left palm vs right palm, which turned out to be a
# degenerate test -- all three tools returned 0 significant hits (those two skin sites are too
# similar), so naive == normalized trivially and it exercised nothing. Switched to gut vs left
# palm for real signal.
.libPaths(c("F:/OpenScience/audit-envs/microbiome-metagenomics-analyst/R-lib", .libPaths()))
suppressMessages({
  library(ALDEx2)
  library(Maaslin2)
  library(MicrobiomeStat)
})

setwd("F:/OpenScience/audits/bio-microbiome-functional-prediction/work")

paths <- read.delim(gzfile("picrust2_out_reaudit/pathways_out/path_abun_unstrat.tsv.gz"),
                     row.names = 1, check.names = FALSE)
cat("Pathway table dims (pathways x samples):", dim(paths), "\n")

meta <- read.delim("F:/OpenScience/audit-envs/microbiome-metagenomics-analyst/public-data/moving-pictures/sample_metadata.tsv")
meta <- meta[-1, ]  # drop the '#q2:types' QIIME2 type-declaration row
colnames(meta)[1] <- "sample_id"
rownames(meta) <- meta$sample_id

samples_in_table <- colnames(paths)
meta_sub <- meta[samples_in_table, ]
groups <- meta_sub$body.site
cat("Group counts:\n"); print(table(groups))

keep <- groups %in% c("gut", "left palm")
paths_sub <- as.matrix(paths[, keep])
storage.mode(paths_sub) <- "numeric"
groups_sub <- factor(groups[keep])
cat("Subset dims:", dim(paths_sub), " groups:\n"); print(table(groups_sub))

## ALDEx2 -- features as rows, raw predicted (count-like) abundances, per SKILL.md's warning
set.seed(123)
aldex_counts <- round(paths_sub)
storage.mode(aldex_counts) <- "integer"
rownames(aldex_counts) <- rownames(paths_sub)
aldex_res <- aldex(aldex_counts, as.character(groups_sub), mc.samples = 128, test = "t", effect = TRUE, denom = "all")
sig_aldex <- aldex_res[aldex_res$we.eBH < 0.05, ]
cat("\nALDEx2: ", nrow(sig_aldex), " / ", nrow(aldex_res), " pathways significant at we.eBH<0.05\n")

## MaAsLin2 -- features as columns, samples as rows
maaslin_input <- as.data.frame(t(paths_sub))
maaslin_meta <- data.frame(body_site = as.character(groups_sub), row.names = colnames(paths_sub))
fit <- Maaslin2(
  input_data = maaslin_input,
  input_metadata = maaslin_meta,
  output = "maaslin2_out_gut_leftpalm",
  fixed_effects = "body_site",
  normalization = "TSS",
  transform = "LOG",
  min_prevalence = 0.1,
  plot_heatmap = FALSE,
  plot_scatter = FALSE
)
maaslin_sig <- read.delim("maaslin2_out_gut_leftpalm/significant_results.tsv")
cat("\nMaAsLin2: ", nrow(maaslin_sig), " significant associations (qval<0.25 default)\n")

## LinDA -- features as rows, plain data.frame metadata (wrapped: a real, new crash was found
## on this comparison -- see note printed below -- and must not block the ALDEx2/MaAsLin2
## intersection re-derivation which is the actual point of this new input)
feature_df <- as.data.frame(paths_sub)
meta_df <- data.frame(body_site = as.character(groups_sub), row.names = colnames(paths_sub))
sig_linda <- data.frame()
linda_ok <- tryCatch({
  linda_fit <- linda(feature.dat = feature_df, meta.dat = meta_df, formula = "~body_site",
                      feature.dat.type = "proportion", prev.filter = 0.0)
  linda_res <- linda_fit$output[[1]]
  sig_linda <<- linda_res[!is.na(linda_res$padj) & linda_res$padj < 0.05, ]
  cat("\nLinDA: ", nrow(sig_linda), " / ", nrow(linda_res), " pathways significant at padj<0.05\n")
  TRUE
}, error = function(e) {
  cat("\nLinDA CRASHED on gut vs left palm (new finding, being noted separately):", conditionMessage(e), "\n")
  FALSE
})

## --- Reproduce the P1 on new data: ALDEx2 vs MaAsLin2 ---
aldex_hits <- rownames(sig_aldex)
maaslin_hits <- unique(maaslin_sig$feature)
cat("\nSample raw ALDEx2 hit names (hyphens expected):\n"); print(head(aldex_hits, 5))
cat("Sample raw MaAsLin2 hit names (dots expected, make.names sanitized):\n"); print(head(maaslin_hits, 5))

inter_naive_am <- intersect(aldex_hits, maaslin_hits)
cat("\n[ALDEx2 vs MaAsLin2] naive intersection (raw names):", length(inter_naive_am), "\n")
inter_norm_am <- intersect(make.names(aldex_hits), make.names(maaslin_hits))
cat("[ALDEx2 vs MaAsLin2] normalized intersection (make.names):", length(inter_norm_am),
    "/ ALDEx2 hits:", length(aldex_hits), "/ MaAsLin2 hits:", length(maaslin_hits), "\n")

## --- Negative control: ALDEx2 vs LinDA (neither sanitizes names) ---
if (linda_ok) {
  linda_hits <- rownames(sig_linda)
  inter_naive_al <- intersect(aldex_hits, linda_hits)
  inter_norm_al <- intersect(make.names(aldex_hits), make.names(linda_hits))
  cat("\n[ALDEx2 vs LinDA, negative control] naive intersection (raw names):", length(inter_naive_al), "\n")
  cat("[ALDEx2 vs LinDA, negative control] normalized intersection (make.names):", length(inter_norm_al), "\n")
  cat("(Expect naive == normalized here since LinDA does not sanitize names -- if so, this confirms\n")
  cat(" the mismatch is specifically MaAsLin2's make.names() behavior, not a general R-tools issue.)\n")
} else {
  cat("\n[ALDEx2 vs LinDA negative control skipped -- LinDA crashed on this comparison, see above]\n")
}
