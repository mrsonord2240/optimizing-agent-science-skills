.libPaths(c('F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/R-lib', .libPaths()))
# Input 4 - SKILL.md lines 129-139 verbatim; only the file name is changed
setwd('F:/OpenScience/audits/bio-proteomics-quantification/data')
library(MSnbase)

raw <- readMSData('tmt10_synthetic.mzML', mode = 'onDisk')
cat('readMSData OK:', length(raw), 'spectra; MS levels:', paste(names(table(msLevel(raw))), table(msLevel(raw)), sep = 'x', collapse = ' '), '\n')
# method='max' for centroided spectra; reporters=TMT10 defines the 126-131 reporter m/z
quant <- quantify(raw, reporters = TMT10, method = 'max')
cat('quantify OK: class', class(quant), 'dim', dim(quant), '\n'); print(head(exprs(quant), 3))
saveRDS(quant, 'F:/OpenScience/audits/bio-proteomics-quantification/runs/in4_quant.rds')

# makeImpuritiesMatrix has manufacturer-default templates; REPLACE with lot-specific Certificate values
cat('calling makeImpuritiesMatrix(x = 10) at', format(Sys.time()), '\n')
imp <- makeImpuritiesMatrix(x = 10)
cat('makeImpuritiesMatrix returned at', format(Sys.time()), '\n')
quant <- purityCorrect(quant, imp)
cat('purityCorrect OK\n')
