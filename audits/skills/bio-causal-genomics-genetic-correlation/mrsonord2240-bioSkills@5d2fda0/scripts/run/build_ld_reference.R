# Build a SYNTHETIC single-chromosome LD-score reference in the exact file format
# GenomicSEM::ldsc() / LDSC expect: "<chr>.l2.ldscore.gz" (CHR, SNP, BP, L2) and
# "<chr>.l2.M_5_50" (single integer). No real genotypes or public LD data used --
# this is a planted-truth construction (perfect-LD blocks of varying size), documented
# in eval_viewer_bio-causal-genomics-genetic-correlation.md.
#
# Construction: SNPs are grouped into K contiguous blocks of size s_b (cycling 1..20).
# Within a block, all SNPs are treated as in perfect LD (r=1) with a single latent
# causal signal, so each SNP's true LD score is exactly its block size s_b. This
# reproduces the LDSC generative model exactly: E[chi^2_j] = 1 + N*h2*L2_j/M when the
# block's causal-effect variance is set to h2*s_b/M (done in simulate_gwas_pair.R).

set.seed(20260917)

block_sizes <- rep(1:20, length.out = 24000) # 24000 blocks, sizes 1..20 cycling
M_total <- sum(block_sizes)                   # total SNP count -- 252,000
# (M chosen so that mean_L2/M puts mean chi-square in a realistic 1.0-2.5 range
#  across the N/h2 regimes used in input1-3, rather than the ~100 an M=3150
#  reference produced on a first attempt -- see eval_viewer note.)
cat("Total SNPs (M):", M_total, " Total blocks (K):", length(block_sizes), "\n")

block_id <- rep(seq_along(block_sizes), times = block_sizes)
L2 <- rep(block_sizes, times = block_sizes)
snp_id <- sprintf("rs%06d", seq_len(M_total))
bp <- seq_len(M_total) * 1000L

ldscore_df <- data.frame(CHR = 1L, SNP = snp_id, BP = bp, L2 = L2)

out_dir <- "F:/OpenScience/audits/bio-causal-genomics-genetic-correlation/data/ld"
dir.create(out_dir, showWarnings = FALSE, recursive = TRUE)

gz <- gzfile(file.path(out_dir, "1.l2.ldscore.gz"), "wt")
write.table(ldscore_df, gz, sep = "\t", quote = FALSE, row.names = FALSE)
close(gz)

# M_5_50: count of SNPs with MAF in [0.05, 0.5] used by real LDSC to rescale h2 to M_total.
# Our synthetic SNPs stand in for that whole set, so M_5_50 = M_total.
writeLines(as.character(M_total), file.path(out_dir, "1.l2.M_5_50"))

saveRDS(list(block_id = block_id, block_sizes = block_sizes, L2 = L2,
             snp_id = snp_id, M_total = M_total),
        file.path(out_dir, "block_structure.rds"))

cat("Wrote", file.path(out_dir, "1.l2.ldscore.gz"), "and 1.l2.M_5_50\n")
cat("L2 range:", range(L2), "\n")
