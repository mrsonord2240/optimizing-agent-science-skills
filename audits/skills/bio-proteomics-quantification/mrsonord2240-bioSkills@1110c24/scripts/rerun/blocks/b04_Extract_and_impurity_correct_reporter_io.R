library(MSnbase)

raw <- readMSData('experiment.mzML', mode = 'onDisk')
# method='max' for centroided spectra; reporters=TMT10 defines the 126-131 reporter m/z
quant <- quantify(raw, reporters = TMT10, method = 'max')

# edit = FALSE: the default edit = TRUE calls edit(M) and blocks under Rscript / on a cluster.
# x = 10 is the manufacturer template; REPLACE with lot-specific Certificate of Analysis values, e.g.
# imp <- makeImpuritiesMatrix(filename = 'lot_coa.csv', edit = FALSE)  # layout as MSnbase extdata TMT6plexPurityCorrections.csv
imp <- makeImpuritiesMatrix(x = 10, edit = FALSE)
quant <- purityCorrect(quant, imp)
