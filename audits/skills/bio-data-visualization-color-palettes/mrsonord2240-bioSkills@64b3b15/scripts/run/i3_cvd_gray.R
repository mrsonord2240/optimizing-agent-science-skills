# Input 3: audit candidate palettes for CVD and grayscale readability, running the SKILL.md check blocks verbatim
suppressMessages({library(viridis);library(scico);library(colorspace);library(scales);library(khroma);library(RColorBrewer)})
Lstar <- function(cols) coords(as(hex2RGB(cols), "LAB"))[,"L"]
mono <- function(L) all(diff(L) >= -1e-6) || all(diff(L) <= 1e-6)
cands <- list(viridis=viridis(10), cividis=viridis(10,option="cividis"), magma=viridis(10,option="magma"), turbo=viridis(10,option="turbo"),
              batlow=scico(10,palette="batlow"), rainbow=rainbow(10), heat=heat.colors(10), rdbu=brewer.pal(10,"RdBu"))
cands$rdbu <- colorRampPalette(brewer.pal(11,"RdBu"))(10)
cat("L* (CIELAB) monotonic along the 10-colour ramp (R colorspace, independent of the Python run):\n")
for (n in names(cands)) { L <- Lstar(cands[[n]]); cat(sprintf("%-8s mono=%-5s L*: %s\n", n, mono(L), paste(round(L), collapse=" "))) }
cat("\nSKILL.md grayscale block: 'grey(seq(0,1,length=10))' is presented as the 'equivalent grayscale gradient' of viridis(10).\n")
Lg <- Lstar(grey(seq(0,1,length=10))); Lv <- Lstar(viridis(10)); Ld <- Lstar(desaturate(viridis(10)))
cat("L* of grey ramp        :", round(Lg), "\nL* of viridis(10)      :", round(Lv), "\nL* of desaturate(viridis(10)):", round(Ld), "\n")
cat("max |L*(viridis) - L*(grey ramp)| =", round(max(abs(Lv-Lg)),1), "  vs desaturate:", round(max(abs(Lv-Ld)),1), "\n")
cat("\ndesaturate(rainbow(10)) L*:", round(Lstar(desaturate(rainbow(10)))), " mono:", mono(Lstar(desaturate(rainbow(10)))), "\n")
cat("desaturate(turbo)   L*:", round(Lstar(desaturate(cands$turbo))), " mono:", mono(Lstar(desaturate(cands$turbo))), "\n")

cat("\n=== SKILL.md CVD block, verbatim ===\n")
palette <- cands$viridis
for (t in c("deutan","protan","tritan")) { r <- try(cvd_emulator(palette, type = t), silent=TRUE); cat("cvd_emulator(palette, type='", t, "') -> ", if (inherits(r,"try-error")) paste("ERROR:", trimws(conditionMessage(attr(r,"condition")))) else "ok", "\n", sep="") }
cat("what cvd_emulator really takes: file =", names(formals(cvd_emulator))[1], "(an image file; launches a Shiny app)\n")
png("../figs/i3_demoplot.png", 1600, 900, res=150)
op <- par(mfrow=c(2,3)); on.exit(par(op))
demoplot(scico(8,palette="batlow"), type="heatmap"); demoplot(deutan(scico(8,palette="batlow")), type="heatmap"); demoplot(protan(scico(8,palette="batlow")), type="heatmap")
demoplot(rainbow(8), type="heatmap"); demoplot(deutan(rainbow(8)), type="heatmap"); demoplot(protan(rainbow(8)), type="heatmap")
dev.off(); cat("demoplot PNG bytes:", file.size("../figs/i3_demoplot.png"), "\n")
png("../figs/i3_showcol_gray.png", 1600, 1000, res=150)
op <- par(mfrow=c(2,3)); show_col(viridis(10)); show_col(grey(seq(0,1,length=10))); show_col(desaturate(viridis(10)))
show_col(rainbow(10)); show_col(desaturate(rainbow(10))); show_col(desaturate(cands$turbo)); dev.off()
cat("show_col PNG bytes:", file.size("../figs/i3_showcol_gray.png"), "\n")
cat("\n=== SKILL.md python snippet: from colorspacious import cspace_converter ===\n(see i3_python_snippet.py)\n")
