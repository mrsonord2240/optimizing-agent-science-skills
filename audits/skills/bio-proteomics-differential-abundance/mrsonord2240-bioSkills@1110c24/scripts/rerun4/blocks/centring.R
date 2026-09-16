offset <- median(tested$log2FC, na.rm = TRUE)          # msqrob2: median(res$logFC)
if (abs(offset) > 0.05) stop(sprintf(
  'median log2FC = %+.3f: the contrast is not centred. Re-normalize (proteomics/quantification) before reading this table.',
  offset))
