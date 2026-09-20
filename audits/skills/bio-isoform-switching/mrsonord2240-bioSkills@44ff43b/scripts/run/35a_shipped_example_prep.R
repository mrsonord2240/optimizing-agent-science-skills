# INPUT 3 (part D): the SHIPPED example script (examples/isoform_switch_analysis.R) run from a clean COPY (run/skill/examples).
# D1: as shipped (banner only).  D2: its functions in the order its own comments give, on REAL chrX 2 GBR v 2 YRI.  D3: same chain on SYNTHETIC 6v6.
setwd("F:/OpenScience/audits/bio-isoform-switching/run/work"); source("../helpers.R")
ex <- "../skill/examples/isoform_switch_analysis.R"
cat("### D1 sourcing the shipped example as-is\n"); out <- capture.output(suppressMessages(source(ex))); cat(out, sep = "\n")
chk("D1 Shipped example, run as shipped, produces analysis output (not just a banner)", any(grepl("Switch Summary|significant", out)), paste(tail(out, 1), collapse = " | "))
PD <- "F:/OpenScience/audit-envs/alternative-splicing/public-data"
tf <- function(expr) tryCatch(expr, error = function(e) { cat("  ERROR:", conditionMessage(e), "\n"); NULL })

cat("\n### D2 example functions on REAL chrX (annotation.gtf / transcripts.fa are hard-coded relative names: staged as real GTF/FASTA)\n")
file.copy(file.path(PD, "rnasplice/reference/genes_chrX.gtf"), "annotation.gtf", overwrite = TRUE); file.copy(file.path(PD, "derived/chrX_tx.fa"), "transcripts.fa", overwrite = TRUE)
design <- data.frame(sampleID = c("ERR188383", "ERR188428", "ERR188454", "ERR204916"), condition = c("GBR", "GBR", "YRI", "YRI"))
sl <- suppressWarnings(import_salmon_data("real_salmon/", design))
chk("D2 import_salmon_data() returns a switchAnalyzeRlist", inherits(sl, "switchAnalyzeRlist"), paste(nrow(sl$isoformFeatures), "isoform rows"))
sl2 <- tf(run_switch_analysis(sl))
chk("D2 run_switch_analysis() (example defaults) completes on real 2v2 data", !is.null(sl2), if (is.null(sl2)) "stopped: 'No genes were considered switching' (0 significant with the default scaledTPM import; see 35a3/35a4)" else "ok")

cat("\n### D3 same chain on SYNTHETIC 6v6 (planted switches)\n")
file.copy(file.path(SYN, "annotation.gtf"), "annotation.gtf", overwrite = TRUE); file.copy(file.path(SYN, "transcripts.fa"), "transcripts.fa", overwrite = TRUE)
ids <- c(sprintf("ctrl_%d", 1:6), sprintf("trt_%d", 1:6)); d6 <- data.frame(sampleID = ids, condition = rep(c("control", "treatment"), each = 6))
s3 <- suppressWarnings(import_salmon_data("salmon6v6/", d6))
s3 <- tf(run_switch_analysis(s3))
if (!is.null(s3)) { sc <- score_sl(s3); chk("D3 example run_switch_analysis() on synthetic 6v6 keeps the planted switches", length(sc$tp_planted) >= 18, sprintf("%d/20 planted, %d null FP", length(sc$tp_planted), length(sc$fp_null))) }
s3b <- tf(extract_sequences(s3, "seq_ex_syn/"))
chk("D3 example extract_sequences() works right after run_switch_analysis() (GTF without CDS)", !is.null(s3b), if (is.null(s3b)) "fails: ORFs not yet predicted (example runs analyzeORF only later, in analyze_consequences)" else "ok")

cat("\n### D4 remaining example functions on the SYNTHETIC switch list (annotators = the CPC2 + Pfam results from Input 4, copied to the file names the example expects)\n")
dir.create("ex_annot", showWarnings = FALSE); file.copy("annot/cpc2_result.txt", "ex_annot/cpc2_results.txt", overwrite = TRUE); file.copy("annot/pfam_scanfmt.txt", "ex_annot/pfam_results.txt", overwrite = TRUE)
s4 <- suppressWarnings(analyzeORF(s3, orfMethod = "longest", quiet = TRUE))
r_nodir <- tf(extract_sequences(s4, "seq_ex_syn_missing/")); chk("D4 example extract_sequences() creates a missing output dir", !is.null(r_nodir), if (is.null(r_nodir)) "fails: pathToOutput must already exist; example never calls dir.create()" else "ok")
dir.create("seq_ex_syn", showWarnings = FALSE); s4 <- suppressWarnings(extract_sequences(s4, "seq_ex_syn/"))
s5 <- tf(analyze_consequences(s4, "ex_annot"))
chk("D4 example analyze_consequences() completes with only CPC2 + Pfam imported (its consequence list includes signal_peptide_identified)", !is.null(s5), if (is.null(s5)) "stops: intron_retention needs analyzeAlternativeSplicing()/analyzeIntronRetention() first (SKILL.md calls it; the example does not), and signal_peptide_identified needs SignalP" else "ok")
# patched copy of the example (two edits): add analyzeAlternativeSplicing() before the consequence step, drop signal_peptide_identified (no SignalP here)
txt <- paste(readLines(ex), collapse = "\n")
txt <- sub("'domains_identified',[[:space:]]*'signal_peptide_identified'", "'domains_identified'", txt)
txt <- sub("# Analyze functional consequences", "switchList <- analyzeAlternativeSplicing(switchList, onlySwitchingGenes = TRUE, quiet = TRUE)\n    # Analyze functional consequences", txt)
writeLines(txt, "ex_patched.R"); suppressMessages(source("ex_patched.R")); patched <- analyze_consequences
s5 <- tf(patched(s4, "ex_annot"))
if (!is.null(s5)) {
  r <- tf(summarize_results(s5)); chk("D4 summarize_results() (patched consequence list) returns summary + enrichment", !is.null(r), if (!is.null(r)) paste("summary rows:", nrow(r$summary)) else "")
  pf <- "ex_switch.pdf"; tf(suppressWarnings(plot_gene_switch(s5, "GENE001", "control", "treatment", pf)))
  chk("D4 plot_gene_switch() writes a non-empty PDF", file.exists(pf) && file.size(pf) > 5000, sprintf("%d bytes", if (file.exists(pf)) file.size(pf) else 0)) }
cat("DONE 35a\n")
