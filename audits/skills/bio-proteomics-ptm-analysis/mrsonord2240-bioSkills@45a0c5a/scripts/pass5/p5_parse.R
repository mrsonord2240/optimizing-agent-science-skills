source('F:/OpenScience/audits/bio-proteomics-ptm-analysis/rerun/skillblock.R')
b <- skill_r_blocks(); cat('r fences:', length(b), '\n')
for (i in seq_along(b)) cat(' fence', i, ':', class(tryCatch(parse(text=b[[i]]), error=function(e) conditionMessage(e)))[1], '\n')
