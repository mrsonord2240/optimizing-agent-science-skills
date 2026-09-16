library(MSnbase)

raw <- readMSData('experiment.mzML', mode = 'onDisk')
# method='max' for centroided spectra; reporters=TMT10 defines the 126-131 reporter m/z.
# TMTpro 16plex uses reporters = TMT16 (126..134N); MSnbase 2.32.0 has no TMT18 set.
quant <- quantify(raw, reporters = TMT10, method = 'max')

# edit = FALSE: the default edit = TRUE calls edit(M) and blocks under Rscript / on a cluster.
# x = is a MANUFACTURER TEMPLATE and MSnbase ships templates only for x = 4, 6, 8, 10; any other x
# (TMTpro 16) falls through to an unnamed diag(x) and stops with "length of 'dimnames' [1] not equal
# to array extent". REPLACE with lot-specific Certificate of Analysis values -- for TMTpro the only route:
# imp <- makeImpuritiesMatrix(filename = 'lot_coa.csv', edit = FALSE)  # layout as MSnbase extdata
#   TMT6plexPurityCorrections.csv: one row per channel, one column per neighbour OFFSET
#   (-n/2..-1, +1..+n/2) in percent, so a 16plex CoA needs 16 offset columns
imp <- makeImpuritiesMatrix(x = 10, edit = FALSE)
quant <- purityCorrect(quant, imp)
