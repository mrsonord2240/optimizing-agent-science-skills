library(iq)

# rows = peptide ions, columns = samples, values = RUN-NORMALIZED log2 intensities for ONE protein group
result <- maxLFQ(peptide_log2_matrix)
protein_estimate <- result$estimate    # one MaxLFQ value per sample
