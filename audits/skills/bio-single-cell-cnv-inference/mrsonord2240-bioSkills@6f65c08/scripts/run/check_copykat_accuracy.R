pred <- read.csv("/mnt/openscience/audits/bio-single-cell-cnv-inference/run/copykat_out_input2/copykat_prediction.csv")
truth <- read.table("/mnt/openscience/audits/bio-single-cell-cnv-inference/data_realgenes/ground_truth_clones.txt",
                     sep = "\t", header = TRUE)
m <- merge(pred, truth, by.x = "cell.names", by.y = "cell")
cat("=== copyKAT prediction vs true clone ===\n")
print(table(m$true_clone, m$copykat.pred))
