set.seed(43)
options(timeout = 120)

eco_url <- "https://rest.kegg.jp/link/eco/eco00010"
eco_txt <- readLines(eco_url, warn = FALSE)
eco_locus <- unique(sub(".*eco:", "", sapply(strsplit(eco_txt, "\t"), `[`, 2)))
cat("E. coli glycolysis (eco00010) genes:", length(eco_locus), "\n")

# Build universe from a handful of other eco metabolic pathways (lighter than whole genome list)
other_pids <- c("eco00020","eco00030","eco00040","eco00051","eco00052","eco00061",
                 "eco00190","eco00230","eco00240","eco00250","eco00260","eco00270",
                 "eco00280","eco00290","eco00300","eco00310","eco00330","eco00340",
                 "eco00350","eco00360","eco00380","eco00400","eco00410","eco00430",
                 "eco00450","eco00460","eco00470","eco00480","eco00500","eco00520",
                 "eco00540","eco00550","eco00561","eco00562","eco00564","eco00565",
                 "eco00590","eco00592","eco00600","eco00620","eco00630","eco00640",
                 "eco00650","eco00660","eco00670","eco00680","eco00730","eco00740",
                 "eco00750","eco00760","eco00770","eco00780","eco00785","eco00790",
                 "eco00860","eco00900","eco00910","eco00920","eco00970","eco01100",
                 "eco02010","eco02020","eco02024","eco02030","eco02040","eco02060",
                 "eco03010","eco03018","eco03020","eco03030","eco03060","eco03070",
                 "eco03410","eco03420","eco03430","eco03440","eco04122")
bg_locus <- character(0)
for (pid in other_pids) {
  url <- paste0("https://rest.kegg.jp/link/eco/", pid)
  txt <- tryCatch(readLines(url, warn = FALSE), error = function(e) character(0))
  if (length(txt) == 0) next
  ids <- unique(sub(".*eco:", "", sapply(strsplit(txt, "\t"), `[`, 2)))
  bg_locus <- union(bg_locus, ids)
  if (length(bg_locus) > 1200) break
}
bg_locus <- setdiff(bg_locus, eco_locus)
cat("Background eco genes collected from other pathways:", length(bg_locus), "\n")

eco_log2fc <- c(rnorm(length(eco_locus), mean = 2.5, sd = 0.5), rnorm(length(bg_locus), mean = 0, sd = 0.4))
eco_pval   <- c(runif(length(eco_locus), 1e-8, 1e-3), runif(length(bg_locus), 0.05, 0.99))
eco_padj   <- p.adjust(eco_pval, method = "BH")
eco_df <- data.frame(locus_tag = c(eco_locus, bg_locus), log2FoldChange = eco_log2fc, pvalue = eco_pval, padj = eco_padj)
write.csv(eco_df, "SYNTHETIC_eco_de_results.csv", row.names = FALSE)
writeLines(eco_locus, "planted_eco00010_locus.txt")
cat("Wrote", nrow(eco_df), "eco rows. sig:", sum(eco_df$padj<0.05 & eco_df$log2FoldChange>1), "\n")
