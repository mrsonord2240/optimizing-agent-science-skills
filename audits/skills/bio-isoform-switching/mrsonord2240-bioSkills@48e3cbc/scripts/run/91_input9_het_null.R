# INPUT 9 (NEW, Stress): individual-level heterogeneity null at several n, then the Skill's own permutation block on planted+heterogeneous data.
# 9A: PURE-NULL synthetic set (no planted switch; 20% of genes carry per-sample isoform shifts). Random condition labels at n = 2, 3, 4, 6 per group
#     (3 random draws each), SKILL.md workflow block (blocks/r_01.R) verbatim -> every switching gene is a false positive by construction.
# 9B: planted (20 genes) + heterogeneity (20% of nulls), true labels at 3v3 (DEXSeq branch) and 6v6 (satuRn branch): workflow block, then the permutation
#     block (blocks/r_02.R) verbatim -> observed vs permuted counts; are the planted genes recovered, are the het genes false-called, does the block separate them?
setwd("F:/OpenScience/audits/bio-isoform-switching/run/work"); source("../helpers.R"); source("../helpers2.R")
suppressPackageStartupMessages(library(IsoformSwitchAnalyzeR)); set.seed(909)
D <- "F:/OpenScience/audits/bio-isoform-switching/run/data"
quiet <- function(expr) invisible(capture.output(suppressMessages(suppressWarnings(expr))))
stage_sub <- function(src, wd, ids, cond) {   # copy chosen samples; metadata rows shuffled; annotation copied
  unlink(wd, recursive = TRUE); dir.create(file.path(wd, "salmon_quant"), recursive = TRUE)
  for (s in ids) { dir.create(file.path(wd, "salmon_quant", s)); file.copy(file.path(src, "salmon_quant", s, "quant.sf"), file.path(wd, "salmon_quant", s, "quant.sf")) }
  m <- data.frame(sample_id = ids, condition = cond, stringsAsFactors = FALSE); m <- m[sample(nrow(m)), ]
  write.table(m, file.path(wd, "sample_metadata.tsv"), sep = "\t", quote = FALSE, row.names = FALSE)
  file.copy(file.path(src, c("annotation.gtf", "transcripts.fa")), wd) }
calls <- function(sl) { f <- sl$isoformFeatures; f <- f[!is.na(f$isoform_switch_q_value), ]; unique(f$gene_id[f$isoform_switch_q_value < 0.05 & abs(f$dIF) > 0.1]) }

cat("### 9A pure-null heterogeneity set, 6+6 subjects, hetfrac 0.2\n")
tn <- read.delim(file.path(D, "het_null/truth_genes.tsv"), stringsAsFactors = FALSE)
all_ids <- list.files(file.path(D, "het_null/salmon_quant"))
resA <- data.frame()
for (n in c(2, 3, 4, 6)) for (r in 1:3) {
  ids <- sample(all_ids, 2 * n); cond <- sample(rep(c("A", "B"), each = n))
  stage_sub(file.path(D, "het_null"), "w9a", ids, cond); setwd("w9a")
  quiet(run_block("r_01.R")); g <- calls(aSwitchList); setwd("..")
  cat(sprintf("n=%d draw %d: branch %s | genes called %d (all false positives) | of them het genes %d | tested genes %d\n", n, r, if (n > 5) "satuRn" else "DEXSeq",
              length(g), length(intersect(g, tn$gene_id[tn$is_het])), length(unique(aSwitchList$isoformFeatures$gene_id))))
  resA <- rbind(resA, data.frame(n = n, draw = r, called = length(g), het = length(intersect(g, tn$gene_id[tn$is_het]))))
}
print(aggregate(called ~ n, resA, function(v) paste(v, collapse = "/")))
saveRDS(resA, "res9A.rds")

cat("\n### 9B planted + heterogeneity, true labels, workflow block then the Skill's permutation block\n")
for (cfg in list(list(nm = "3v3", n = 3, seed = 9102), list(nm = "6v6", n = 6, seed = 9103))) {
  src <- file.path(D, paste0("het_", cfg$nm))
    tt <- read.delim(file.path(src, "truth_genes.tsv"), stringsAsFactors = FALSE)
  wd <- paste0("w9b_", cfg$nm); unlink(wd, recursive = TRUE); dir.create(wd); file.copy(file.path(src, c("salmon_quant", "annotation.gtf", "transcripts.fa", "sample_metadata.tsv")), wd, recursive = TRUE)
  setwd(wd); quiet(run_block("r_01.R")); g <- calls(aSwitchList)
  cat(sprintf("[%s] workflow: branch %s | called %d genes | planted %d/20 | het-null called %d/%d | other null called %d\n", cfg$nm, if (cfg$n > 5) "satuRn" else "DEXSeq", length(g),
      length(intersect(g, tt$gene_id[tt$true_switch])), length(intersect(g, tt$gene_id[tt$is_het])), sum(tt$is_het), length(setdiff(g, c(tt$gene_id[tt$true_switch], tt$gene_id[tt$is_het])))))
  chk(paste0("9B ", cfg$nm, " planted recovered >= 19/20"), length(intersect(g, tt$gene_id[tt$true_switch])) >= 19)
  t0 <- Sys.time(); quiet(run_block("r_02.R")); cat(sprintf("[%s] permutation block ran in %.0f s\n", cfg$nm, as.numeric(difftime(Sys.time(), t0, units = "secs"))))
  cat(sprintf("[%s] SKILL BLOCK OUTPUT -> observed %d genes; label-permuted: %s\n", cfg$nm, observed, paste(permuted, collapse = " ")))
  cat(sprintf("[%s] number of alternative splits produced: %d\n", cfg$nm, length(perms)))
  assign(paste0("obs_", cfg$nm), observed); assign(paste0("perm_", cfg$nm), permuted)
  setwd("..")
}
cat("DONE 91\n")
