# Build SYNTHETIC input data for the enrichment-visualization audit.
# Real (public) human Entrez gene IDs; fabricated hit-list membership and fold-change values.
suppressMessages(library(org.Hs.eg.db))

set.seed(42)

# A cell-cycle / DNA-replication-biased gene set (real Entrez IDs for real human genes),
# chosen because it reliably produces the GO-DAG redundancy this Skill is about
# ("cell cycle", "cell cycle process", "mitotic cell cycle", "cell division", ...).
entrez <- c('1029','1019','1021','890','983','991','993','4085','4174','5111',
            '1869','1871','7027','4171','4172','4175','4176','4998','5424','5425',
            '9133','701','595','1017')

# Synthetic log2 fold-change for the same genes (fabricated, for color-by-FC plots).
set.seed(1)
fc <- setNames(round(rnorm(length(entrez), mean = 1.2, sd = 1.0), 2), entrez)

# A synthetic full-"transcriptome" ranked list for GSEA: 3000 real Entrez IDs, with the
# cell-cycle set above pushed to the top of the ranking so gseGO returns real, significant,
# directional (positive NES) results instead of an empty run.
all_genes <- keys(org.Hs.eg.db, keytype = 'ENTREZID')
set.seed(7)
bg <- sample(setdiff(all_genes, entrez), 3000 - length(entrez))
set.seed(8)
ranked <- c(setNames(rnorm(length(entrez), mean = 4, sd = 0.5), entrez),
            setNames(sort(rnorm(length(bg), mean = 0, sd = 1), decreasing = TRUE), bg))
ranked <- sort(ranked, decreasing = TRUE)

saveRDS(list(entrez = entrez, fc = fc, ranked = ranked), "../data/gene_data.rds")
cat("Wrote ../data/gene_data.rds\n")
