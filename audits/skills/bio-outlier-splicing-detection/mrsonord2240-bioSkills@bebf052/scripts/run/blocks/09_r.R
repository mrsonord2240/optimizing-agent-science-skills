fds <- estimateBestQ(fds, type = 'jaccard', plot = FALSE)    # FRASER 2.6.1: optimal hard threshold, fast
bestQ(fds, 'jaccard')
# exhaustive injected-outlier grid (FRASER 2.2.0: optimHyperParams(fds, type = 'jaccard', q_param = ...)):
fds <- estimateBestQ(fds, type = 'jaccard', useOHT = FALSE, q_param = c(2, 5, 10, 15), plot = FALSE)
plotEncDimSearch(fds, type = 'jaccard', plotType = 'auc')    # plotType = 'loss' also works
