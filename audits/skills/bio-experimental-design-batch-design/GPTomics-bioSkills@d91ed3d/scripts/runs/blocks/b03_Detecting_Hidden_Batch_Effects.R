library(sva)
mod  <- model.matrix(~ condition, data = colData)   # full model
mod0 <- model.matrix(~ 1, data = colData)           # null model
n_sv <- num.sv(expr_normalized, mod)                # estimate number of hidden batches
svobj <- sva(expr_normalized, mod, mod0, n.sv = n_sv)
# Add svobj$sv to the design used by differential-expression/de-results; do NOT subtract them
# from the data for the test (subtracting is for visualization only).
