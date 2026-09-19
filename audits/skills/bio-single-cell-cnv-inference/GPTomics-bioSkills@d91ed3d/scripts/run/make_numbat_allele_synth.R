# Build a minimal, EXPLICITLY SYNTHETIC df_allele table for testing Numbat's
# R API (run_numbat / aggregate_counts) against the code pattern documented
# in bio-single-cell-cnv-inference SKILL.md's "Numbat" section.
#
# IMPORTANT CAVEAT (stated here and in the audit report): a real Numbat run
# needs per-cell allele counts from `pileup_and_phase.R`, which itself needs
# a BAM, cellsnp-lite, Eagle2, and a 1000G phasing panel -- none available in
# this Windows/WSL audit env (TOOLS.md, "Blocked" section). This script does
# NOT test phasing accuracy or biological realism of the allele signal; it
# only tests whether the R-level object construction and run_numbat() call
# documented in SKILL.md execute against the real installed numbat 1.5.2 API
# (a code-usability / M4 check), using fabricated but internally consistent
# AD/DP/GT values matching the same CNV ground truth as the expression data.
suppressMessages(library(numbat))
set.seed(20260919)

data_dir <- "/mnt/openscience/audits/bio-single-cell-cnv-inference/data_realgenes"
out_dir  <- "/mnt/openscience/audits/bio-single-cell-cnv-inference/run/numbat_allele_data"
dir.create(out_dir, showWarnings = FALSE, recursive = TRUE)

genes <- read.table(file.path(data_dir, "gene_ordering.txt"), sep = "\t",
                     col.names = c("gene", "chr", "start", "stop"))
annot <- read.table(file.path(data_dir, "cell_annotations.txt"), sep = "\t",
                     col.names = c("cell", "group"))
truth <- read.table(file.path(data_dir, "ground_truth_clones.txt"), sep = "\t",
                     header = TRUE)

# restrict to chr7/chr10 genes (the CNV-bearing chromosomes) and to reference
# + CloneA cells only, to keep the fabricated pileup small and fast
snp_genes <- genes[genes$chr %in% c("chr7", "chr10"), ]
snp_genes <- snp_genes[seq(1, nrow(snp_genes), by = 6), ]  # ~1 SNP-gene per 6
cells <- truth$cell[truth$true_clone %in% c("Tcell", "Myeloid", "malignant_cloneA")]

rows <- list()
i <- 1
for (cl in seq_len(nrow(snp_genes))) {
  gene <- snp_genes$gene[cl]; chrom_num <- sub("chr", "", snp_genes$chr[cl])
  pos <- snp_genes$start[cl] + 100
  snp_id <- paste0("snp_", gene, "_", cl)   # same SNP identity shared across cells
  for (cell in cells) {
    if (runif(1) > 0.6) next  # sparse coverage, like real scRNA pileups
    grp <- truth$true_clone[truth$cell == cell]
    dp <- rpois(1, 6) + 2
    if (grp %in% c("Tcell", "Myeloid")) {
      # balanced heterozygous SNP in copy-neutral reference cells
      ad <- rbinom(1, dp, 0.5)
      gt <- "1|0"
    } else if (grp == "malignant_cloneA" && snp_genes$chr[cl] == "chr10") {
      # chr10 LOH in cloneA: allele skewed to near-monoallelic
      ad <- rbinom(1, dp, 0.92)
      gt <- "1|0"
    } else {
      # chr7 gain: 3-copy imbalance (~2:1 skew), still het
      ad <- rbinom(1, dp, 0.33)
      gt <- "1|0"
    }
    rows[[i]] <- data.frame(cell = cell, snp_id = snp_id,
                             CHROM = chrom_num, POS = pos, AD = ad, DP = dp, GT = gt,
                             # cM/REF/ALT required by numbat 1.5.2's check_allele_df()
                             # but NOT listed in SKILL.md's documented df_allele column
                             # set ("columns include cell, snp_id, CHROM, POS, AD, DP,
                             # GT") -- added here only so the audit can exercise the
                             # rest of run_numbat(); cM is a crude linear stub
                             # (pos/1e6 cM), not a real genetic-map lookup.
                             cM = pos / 1e6, REF = "A", ALT = "G")
    i <- i + 1
  }
}
df_allele <- do.call(rbind, rows)
write.table(df_allele, file.path(out_dir, "df_allele.tsv"), sep = "\t",
            row.names = FALSE, quote = FALSE)
cat("df_allele rows:", nrow(df_allele), " unique cells:", length(unique(df_allele$cell)),
    " unique snps:", length(unique(df_allele$snp_id)), "\n")
