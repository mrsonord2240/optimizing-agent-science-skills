library(EnhancedVolcano)
EnhancedVolcano(res,
    lab = rownames(res),
    x = 'log2FoldChange',
    y = 'padj',                    # use padj NOT pvalue for the threshold line
    pCutoff = 0.05,
    FCcutoff = 1,
    selectLab = c('TP53', 'MYC', 'BRCA1'),
    drawConnectors = TRUE,
    widthConnectors = 0.3,
    maxoverlapsConnectors = Inf,
    colAlpha = 0.6,
    pointSize = 1.5,
    labSize = 3,
    col = c('grey60', '#0072B2', '#56B4E9', '#D55E00'),
    legendPosition = 'right')
