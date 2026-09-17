library(goseq)

all_genes <- de$gene_id[!is.na(de$pvalue)]
de_genes  <- as.integer(all_genes %in% sig_genes)   # named binary vector over the tested set
names(de_genes) <- all_genes

pwf <- nullp(de_genes, 'hg38', 'ensGene')           # fits the length PWF; inspect the fit plot
go  <- goseq(pwf, 'hg38', 'ensGene', method = 'Wallenius')   # default; 'Hypergeometric' ignores bias (= standard ORA)
go$padj <- p.adjust(go$over_represented_pvalue, method = 'BH')   # goseq does NOT BH-correct internally
