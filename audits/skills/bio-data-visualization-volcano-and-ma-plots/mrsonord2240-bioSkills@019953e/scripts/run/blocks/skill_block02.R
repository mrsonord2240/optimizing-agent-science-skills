library(ggplot2)
library(ggrepel)
library(dplyr)

volcano_plot <- function(res, fdr = 0.05, lfc_threshold = 1, label_genes = NULL, top_n = 10) {
    res <- as.data.frame(res) %>%
        tibble::rownames_to_column('gene') %>%
        mutate(
            significance = case_when(
                is.na(padj) ~ 'NS',
                padj < fdr & log2FoldChange > lfc_threshold ~ 'Up',
                padj < fdr & log2FoldChange < -lfc_threshold ~ 'Down',
                TRUE ~ 'NS'
            ),
            neg_log10_p = -log10(pvalue)
        )

    if (is.null(label_genes)) {
        label_genes <- res %>%
            filter(significance != 'NS') %>%
            mutate(rank_score = -log10(pvalue) * abs(log2FoldChange)) %>%
            arrange(desc(rank_score)) %>%
            head(top_n) %>%
            pull(gene)
    }
    res$label <- ifelse(res$gene %in% label_genes, res$gene, '')

    okabe_ito <- c(Up = '#D55E00', Down = '#0072B2', NS = '#999999')

    ggplot(res, aes(log2FoldChange, neg_log10_p, color = significance)) +
        geom_point(alpha = 0.6, size = 1.3) +
        scale_color_manual(values = okabe_ito, name = NULL) +
        geom_vline(xintercept = c(-lfc_threshold, lfc_threshold),
                   linetype = 'dashed', color = 'grey40', linewidth = 0.3) +
        geom_hline(yintercept = -log10(fdr), linetype = 'dashed',
                   color = 'grey40', linewidth = 0.3) +
        geom_text_repel(aes(label = label), color = 'black', size = 3,
                        max.overlaps = Inf, box.padding = 0.4, segment.size = 0.2,
                        min.segment.length = 0) +
        labs(x = expression(log[2]~'fold change (shrunken)'),
             y = expression(-log[10]~italic(p))) +
        theme_classic(base_size = 10) +
        theme(panel.grid = element_blank())
}
