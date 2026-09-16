library(MSnbase)

# Extract reporter ions from spectra (NOT readMSnSet, which loads an existing text matrix)
raw <- readMSData('tmt.mzML', mode = 'onDisk')
tmt_data <- quantify(raw, reporters = TMT10, method = 'max')
# Correct isobaric impurity cross-talk with the LOT-SPECIFIC matrix from the reagent CoA.
# makeImpuritiesMatrix(x = 10, edit = FALSE) returns a MANUFACTURER TEMPLATE, not an identity
# matrix -- its diagonal runs 0.928-0.965 and 5% of 126 lands in 127C. It is a shape check only;
# the numbers are lot-specific. (edit = TRUE, the default, opens an editor and blocks in scripts.)
# Do NOT use makeImpuritiesMatrix(filename = ...) for TMT10/TMTpro: it reads a CoA laid out by
# Da OFFSET and places each column k POSITIONS away in the reporter list, which is only correct
# for non-interleaved reagents (TMT6, iTRAQ). TMT10/TMTpro interleave N and C, so the +1 Da
# neighbour of 126 is 127C -- TWO positions away -- and the filename route silently writes the
# bleed into 127N instead. Build the matrix by CHANNEL NAME and hand it to purityCorrect:
# tmt10_coa.csv: a square percentage matrix, rows = SOURCE reagent, columns = OBSERVED channel,
# both labelled with the channel names (126, 127N, 127C, ...); diagonal = the lot's purity.
coa <- as.matrix(read.csv('tmt10_coa.csv', row.names = 1, check.names = FALSE))
stopifnot(nrow(coa) == ncol(coa), setequal(rownames(coa), reporterNames(TMT10)))
coa <- coa[reporterNames(TMT10), reporterNames(TMT10)]   # force the quant's channel order
impurities <- coa / 100                                  # CoA percentages -> fractions
tmt_data <- purityCorrect(tmt_data, impurities)
stopifnot(sum(exprs(tmt_data) < 0, na.rm = TRUE) == 0)         # negatives = transposed/mis-ordered matrix

# Multi-batch TMT: do NOT concatenate plexes directly. Use MSstatsTMT, which applies the
# reference-channel (IRS) bridge during summarization:
#   library(MSstatsTMT)
#   summ <- proteinSummarization(msstatstmt_input)   # includes the cross-plex bridge
#   groupComparisonTMT(summ, contrast.matrix = comparison)
