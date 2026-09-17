# Input 1 (Canonical) -- "I ran enrichGO on my DE hit list (BP ontology) and got a bunch of
# significant terms, but the default dotplot looks like the same theme repeated 20 times.
# Simplify the redundancy and make a clean dotplot, and tell me how many terms survived and how
# many were in the raw result."
suppressMessages({
  library(clusterProfiler)
  library(enrichplot)
  library(org.Hs.eg.db)
  library(ggplot2)
})

d <- readRDS("../data/gene_data.rds")

ego <- enrichGO(gene = d$entrez, OrgDb = org.Hs.eg.db, ont = 'BP',
                 pvalueCutoff = 0.05, qvalueCutoff = 0.2, readable = TRUE)

n_raw <- nrow(as.data.frame(ego))
cat("Raw significant terms:", n_raw, "\n")

# Show what the SKILL warns about: raw top-20 is one theme repeated.
p_raw <- dotplot(ego, showCategory = 20) + ggtitle('Raw top-20 (redundant)')

# The Skill's prescribed fix: simplify() collapses GO-DAG redundancy before plotting.
ego_simple <- simplify(ego, cutoff = 0.7, by = 'p.adjust', select_fun = min)
n_simple <- nrow(as.data.frame(ego_simple))
cat("After simplify(cutoff=0.7):", n_simple, "terms survived (of", n_raw, "raw)\n")

p_simple <- dotplot(ego_simple, showCategory = 20) + ggtitle('Simplified (redundancy collapsed)')

out <- "input1_output.pdf"
pdf(out, width = 10, height = 8)
print(p_raw)
print(p_simple)
dev.off()

cat("Wrote", out, "\n")
cat("Raw top-3 terms (by orderBy=x default, i.e. GeneRatio):\n")
print(head(as.data.frame(ego)[order(-as.data.frame(ego)$Count),]$Description, 5))
