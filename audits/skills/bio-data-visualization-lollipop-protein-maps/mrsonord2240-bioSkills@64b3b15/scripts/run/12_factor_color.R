# Why are the 175/248/273 missense lollipops pink in the example's trackViewer section? class_col[<factor>] indexes by integer code.
suppressMessages({library(maftools); library(data.table)})
maf <- read.maf("F:/OpenScience/audits/bio-data-visualization-lollipop-protein-maps/run/out/ex/clean.maf", verbose = FALSE)
class_col <- c(Missense_Mutation='#D55E00', Nonsense_Mutation='#000000', Frame_Shift_Del='#0072B2', Frame_Shift_Ins='#56B4E9', Splice_Site='#CC79A7', In_Frame_Del='#009E73', In_Frame_Ins='#F0E442')
ms <- maf@data[Hugo_Symbol == 'TP53', .(count = .N, class = Variant_Classification[1]), by = .(aa_pos = as.numeric(sub('p\\.[A-Z](\\d+).*', '\\1', HGVSp_Short)))]
cat("class(Variant_Classification):", class(maf@data$Variant_Classification), "\n"); print(levels(maf@data$Variant_Classification))
top <- ms[aa_pos %in% c(175, 248, 273)]
top[, `:=`(by_factor = unname(class_col[class]), by_name = unname(class_col[as.character(class)]))]
print(top)
cat("Hotspot colour from the example's indexing == intended class colour:", all(top$by_factor == top$by_name), "\n")
cat("rows whose colour is wrong under factor indexing:", sum(unname(class_col[ms$class]) != unname(class_col[as.character(ms$class)]), na.rm = TRUE), "of", nrow(ms), "\n")
