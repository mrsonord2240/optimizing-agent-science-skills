# Input 1: CVD-safe categorical palette for 7 cell types + grey for unassigned, on a UMAP-like scatter (SYNTHETIC data)
suppressMessages({library(ggplot2);library(colorspace);library(patchwork)})
set.seed(20260920)
types <- c("T cell","B cell","NK cell","Monocyte","Dendritic","Platelet","Erythroid","Unassigned")
ctr <- cbind(x=c(-6,-3,-4,4,6,0,7,0), y=c(4,6,0,5,-1,-6,-6,0))
n <- c(300,200,120,320,80,40,60,150)
df <- do.call(rbind, lapply(seq_along(types), function(i) data.frame(UMAP1=rnorm(n[i],ctr[i,1],1.1), UMAP2=rnorm(n[i],ctr[i,2],1.1), cell_type=types[i])))
df$cell_type <- factor(df$cell_type, levels=types)
write.csv(df, "../data/synthetic_umap_celltypes.csv", row.names=FALSE)   # SYNTHETIC
cat("n cells:", nrow(df), " groups:", nlevels(df$cell_type), "\n")

## --- SKILL block verbatim
okabe_ito <- c('#E69F00','#56B4E9','#009E73','#F0E442','#0072B2','#D55E00','#CC79A7','#000000')
cat("Skill hexes as set == palette.colors(8,'Okabe-Ito') set:", setequal(toupper(okabe_ito), toupper(palette.colors(8,"Okabe-Ito"))), "\n")
cat("same ORDER as palette.colors:", identical(toupper(okabe_ito), toupper(unname(palette.colors(8,"Okabe-Ito")))), "\n")
cat("first colour of palette.colors(8):", palette.colors(8,"Okabe-Ito")[1], " (Skill's first: ", okabe_ito[1], ")\n")

# (A) as the Skill shows: unnamed vector, 8 levels
pA <- ggplot(df, aes(UMAP1, UMAP2, color=cell_type)) + geom_point(size=.8) + scale_color_manual(values=okabe_ito) + ggtitle("A. Skill pattern, unnamed vector")
bA <- ggplot_build(pA)$data[[1]]
mapA <- unique(data.frame(cell_type=df$cell_type[order(as.integer(df$cell_type))], colour=bA$colour[order(as.integer(df$cell_type))]))
print(mapA)

# (B) same pattern after dropping T cells (a subset / a different panel): colours shift?
dfB <- droplevels(subset(df, cell_type != "T cell"))
pB <- ggplot(dfB, aes(UMAP1, UMAP2, color=cell_type)) + geom_point(size=.8) + scale_color_manual(values=okabe_ito) + ggtitle("B. same code, T cells removed")
bB <- ggplot_build(pB)$data[[1]]
mapB <- unique(data.frame(cell_type=dfB$cell_type[order(as.integer(dfB$cell_type))], colour=bB$colour[order(as.integer(dfB$cell_type))]))
print(mapB)
m <- merge(mapA, mapB, by="cell_type", suffixes=c("_A","_B")); m$same <- toupper(m$colour_A)==toupper(m$colour_B)
print(m); cat("cell types whose colour CHANGED between A and B (unnamed vector):", sum(!m$same), "of", nrow(m), "\n")

# (C) named vector (the Skill's custom-palette pattern) with grey reserved for Unassigned
pal <- setNames(c(okabe_ito[1:7], "#999999"), types)
pC <- ggplot(df, aes(UMAP1, UMAP2, color=cell_type)) + geom_point(size=.8) + scale_color_manual(values=pal) + ggtitle("C. named vector, grey = Unassigned")
pD <- ggplot(dfB, aes(UMAP1, UMAP2, color=cell_type)) + geom_point(size=.8) + scale_color_manual(values=pal) + ggtitle("D. named vector, T cells removed")
cC <- unique(ggplot_build(pC)$data[[1]]$colour); cD <- unique(ggplot_build(pD)$data[[1]]$colour)
bC <- ggplot_build(pC)$data[[1]]; bD <- ggplot_build(pD)$data[[1]]
mC <- tapply(bC$colour, df$cell_type, function(z) unique(z)); mD <- tapply(bD$colour, dfB$cell_type, function(z) unique(z))
stopifnot(all(mC[names(mD)] == mD))
cat("Named-vector mapping identical across full and subset data: TRUE\n")
cat("Unassigned colour:", mC[["Unassigned"]], " T cell:", mC[["T cell"]], "\n")

## --- CVD simulation with colorspace, as the Skill directs
cat("\n--- cvd_emulator(palette, type='deutan') exactly as written in SKILL.md:\n")
r <- try(cvd_emulator(pal, type='deutan'), silent=TRUE); cat(class(r), ":", if (inherits(r,"try-error")) conditionMessage(attr(r,"condition")) else "ok", "\n")
cat("--- deutan()/protan() on the palette (works):\n")
print(rbind(normal=pal, deutan=deutan(pal), protan=protan(pal)))
png("../figs/i1_categorical_full_vs_subset.png", 1500, 900, res=150)
print((pA + pB) / (pC + pD) & theme_minimal(base_size=9) & guides(color=guide_legend(override.aes=list(size=3))))
dev.off()
# CVD-simulated version of the good plot
sim_pal <- function(f) setNames(f(pal), names(pal))
png("../figs/i1_categorical_cvd.png", 1800, 500, res=150)
mk <- function(p, t) ggplot(df, aes(UMAP1, UMAP2, color=cell_type)) + geom_point(size=.8) + scale_color_manual(values=p) + ggtitle(t) + theme_minimal(base_size=9) + theme(legend.position="none")
print(mk(pal,"normal") + mk(sim_pal(deutan),"deuteranopia") + mk(sim_pal(protan),"protanopia") + mk(sim_pal(tritan),"tritanopia") + plot_layout(nrow=1))
dev.off()
cat(file.size("../figs/i1_categorical_full_vs_subset.png"), file.size("../figs/i1_categorical_cvd.png"), "\n")
