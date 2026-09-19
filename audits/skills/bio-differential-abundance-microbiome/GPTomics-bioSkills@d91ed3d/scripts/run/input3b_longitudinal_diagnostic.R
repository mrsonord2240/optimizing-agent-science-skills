# Diagnostic follow-up to input3: does long_phyloseq.rds actually carry a Placebo-vs-
# Treatment abundance signal for the planted taxa at all, or is the "0 hits" result a
# genuine fixture-signal-strength issue rather than a LinDA/random-effect failure?
suppressMessages(library(phyloseq))
lps <- readRDS('F:/OpenScience/audit-envs/microbiome-metagenomics-analyst/datagen/asvtable/long_phyloseq.rds')
truth <- read.delim('F:/OpenScience/audit-envs/microbiome-metagenomics-analyst/datagen/asvtable/truth_da.tsv', stringsAsFactors = FALSE)
meta <- data.frame(as(sample_data(lps), 'data.frame'))
otu <- as.data.frame(otu_table(lps)); if (!taxa_are_rows(lps)) otu <- t(otu)
tss <- sweep(otu, 2, colSums(otu), '/')

check_taxon <- function(tx) {
  role <- truth$role[truth$ASV == tx]
  fc <- truth$true_fc_treated_vs_control[truth$ASV == tx]
  by_arm <- tapply(as.numeric(tss[tx, ]), meta$Arm, mean)
  by_visit <- tapply(as.numeric(tss[tx, ]), meta$visit, mean)
  cat(sprintf('%s (role=%s, cross-sectional truth_fc=%.2f): mean TSS by Arm: placebo=%.5f treatment=%.5f | ratio(treat/placebo)=%.2f\n',
              tx, role, fc, by_arm['placebo'], by_arm['treatment'], by_arm['treatment']/by_arm['placebo']))
  cat('   by visit:', paste(names(by_visit), round(by_visit,5), collapse=' | '), '\n')
}
cat('=== Planted-effect taxa: does the longitudinal fixture show the same Arm effect? ===\n')
for (tx in c('ASV030','ASV086','ASV036','ASV055','ASV073')) check_taxon(tx)

cat('\n=== Null taxa for comparison ===\n')
for (tx in c('ASV001','ASV002','ASV003')) check_taxon(tx)

cat('\nInterpretation: if placebo/treatment ratios for planted taxa are ~1 (no signal) while\n')
cat('phyloseq_object.rds (cross-sectional) showed the true fold-changes, the longitudinal\n')
cat('fixture simply does not encode the same Group/Arm effect -- it likely varies by visit\n')
cat('or subject instead. This determines whether the "0 hits" result blames the fixture or the tool.\n')
