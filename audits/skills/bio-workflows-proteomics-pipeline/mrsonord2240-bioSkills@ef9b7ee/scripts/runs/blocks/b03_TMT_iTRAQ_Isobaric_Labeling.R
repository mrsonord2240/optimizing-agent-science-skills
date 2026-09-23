library(MSnbase)

# Extract reporter ions from spectra (NOT readMSnSet, which loads an existing text matrix)
raw <- readMSData('tmt.mzML', mode = 'onDisk')
tmt_data <- quantify(raw, reporters = TMT10, method = 'max')
# Correct isobaric impurity cross-talk with the LOT-SPECIFIC matrix from the reagent CoA.
# edit=FALSE avoids the interactive editor (default edit=TRUE blocks in scripts); load the CoA
# cross-talk values rather than the near-identity template makeImpuritiesMatrix(10) returns alone.
impurities <- makeImpuritiesMatrix(filename = 'tmt10_coa.csv', edit = FALSE)
tmt_data <- purityCorrect(tmt_data, impurities)

# Multi-batch TMT: do NOT concatenate plexes directly. Use MSstatsTMT, which applies the
# reference-channel (IRS) bridge during summarization:
#   library(MSstatsTMT)
#   summ <- proteinSummarization(msstatstmt_input)   # includes the cross-plex bridge
#   groupComparisonTMT(summ, contrast.matrix = comparison)
