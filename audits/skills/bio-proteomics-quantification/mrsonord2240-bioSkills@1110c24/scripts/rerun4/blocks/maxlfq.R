library(iq)

# peptide_long: one row per peptide ion per run, RAW intensities (protein, ion, run, intensity)
norm <- preprocess(peptide_long, primary_id = 'protein', secondary_id = 'ion', sample_id = 'run',
                   intensity_col = 'intensity', median_normalization = TRUE, pdf_out = NULL)
protein_list  <- create_protein_list(norm)    # one run-normalized log2 matrix per protein
protein_table <- create_protein_table(protein_list, method = 'maxLFQ')
protein_matrix <- protein_table$estimate      # proteins x samples

# maxLFQ solves per-protein least squares only within CONNECTED sample sets; a non-empty annotation
# marks proteins whose samples split into groups that are NOT on one common scale
disconnected <- rownames(protein_matrix)[nzchar(protein_table$annotation)]

# one protein at a time: rows = peptide ions, columns = samples, values = RUN-NORMALIZED log2 intensities
result <- maxLFQ(protein_list[[1]])
# $estimate is an UNNAMED vector in the input column order; name it or samples silently transpose
protein_estimate <- setNames(result$estimate, colnames(protein_list[[1]]))
