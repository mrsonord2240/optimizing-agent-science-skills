# Input 4: the SKILL.md "MARVEL Plate-Based Workflow" block executed LITERALLY (only 'neurons'/'glia' defined, since the Skill leaves them undefined).
# Each top-level statement is wrapped so a failure is recorded and the run continues.
setwd('F:/OpenScience/audits/bio-single-cell-splicing/run/data/marvel_star')
step <- function(label, expr) { r <- tryCatch({ force(expr); cat('[OK]   ', label, '\n'); TRUE }, error=function(e) { cat('[FAIL] ', label, ' -> ', conditionMessage(e), '\n'); FALSE }); invisible(r) }
suppressMessages({library(MARVEL); library(Seurat); library(data.table)})
seurat_obj <- readRDS('cells.rds')
neurons <- rownames(seurat_obj@meta.data)[seurat_obj@meta.data$cell.type=='iPSC']     # stand-ins for the Skill's undefined groups
glia    <- rownames(seurat_obj@meta.data)[seurat_obj@meta.data$cell.type=='Endoderm']

# ---- verbatim from SKILL.md ----
sj_files <- list.files('star_pass2/', pattern='SJ.out.tab$', full.names=TRUE)
sj_long <- rbindlist(lapply(sj_files, function(f) {
    d <- fread(f, sep='\t', header=FALSE,
               col.names=c('chr','start','end','strand','motif','annot','unique','multi','overhang'))
    d$coord.intron <- paste(d$chr, d$start, d$end, sep=':')
    d$sample <- gsub('_SJ.out.tab$', '', basename(f))
    d[, .(coord.intron, sample, unique)]
}))
sj <- dcast(sj_long, coord.intron ~ sample, value.var='unique', fill=0)
cat('SJ matrix dim', dim(sj), ' class', class(sj), '\n')

df.feature.list <- list(
    SE   = read.table('events_SE.txt',   header=TRUE, sep='\t'),
    A5SS = read.table('events_A5SS.txt', header=TRUE, sep='\t'),
    A3SS = read.table('events_A3SS.txt', header=TRUE, sep='\t'),
    MXE  = read.table('events_MXE.txt',  header=TRUE, sep='\t'),
    RI   = read.table('events_RI.txt',   header=TRUE, sep='\t')
)
df.pheno <- seurat_obj@meta.data
df.pheno$sample.id <- rownames(df.pheno)
marvel <- NULL
step('CreateMarvelObject (Skill args)', { marvel <<- CreateMarvelObject(
    SpliceJunction = sj,
    SplicePheno    = df.pheno,
    SpliceFeature  = df.feature.list,
    GeneFeature    = read.table('gene_features.tsv', header=TRUE, sep='\t'),
    Exp            = read.table('tpm.tsv', header=TRUE, sep='\t', row.names=1),
    GTF            = rtracklayer::import('annotation.gtf')
) })
cat('Exp colnames head:', head(colnames(marvel$Exp),3), '; Exp class(GTF):', class(marvel$GTF)[1], '\n')
step('ComputePSI(CoverageThreshold=10, EventType=SE)  [Skill]', { marvel <<- ComputePSI(marvel, CoverageThreshold=10, EventType='SE') })
cat('PSI SE dim:', if(is.null(marvel$PSI$SE)) 'NULL' else paste(dim(marvel$PSI$SE), collapse='x'), '\n')
step('AssignModality(marvel, EventType=SE)  [Skill]', { marvel2 <- AssignModality(marvel, EventType='SE') })
step('CompareValues(... n.cells=25 ...)  [Skill]', { marvel2 <- CompareValues(marvel, cell.group.g1 = neurons, cell.group.g2 = glia, method = 'wilcox', n.cells = 25, psi.delta = 0.1) })

# ---- extra: does the Skill's Exp (read.table(row.names=1) drops the gene_id column that MARVEL requires) survive MARVEL's own pre-flight checks?
cat('\nExp first column after Skill read.table(row.names=1):', colnames(marvel$Exp)[1], '(MARVEL expects gene_id)\n')
step('TransformExpValues on Skill-built Exp', { marvel3 <<- TransformExpValues(marvel, offset=1, transformation='log2', threshold.lower=1) })
step('CheckAlignment(level="gene") on Skill-built object', { CheckAlignment(marvel, level='gene') })
step('CheckAlignment(level="splicing") on Skill-built object', { CheckAlignment(marvel, level='splicing') })
# ---- corrected chain on the same (real demo) data: AssignModality + CompareValues per the installed signature
marvel$PSI$SE  # already computed above
step('AssignModality(sample.ids=..., min.cells=5) [installed signature]', { marvel4 <<- AssignModality(marvel, sample.ids = neurons, min.cells = 5, seed = 1) })
step('CompareValues(level="splicing", event.type="SE", method="wilcox", min.cells=5) [installed signature]', { marvel5 <<- CompareValues(marvel, cell.group.g1 = neurons, cell.group.g2 = glia, min.cells = 5, method = 'wilcox', level = 'splicing', event.type = 'SE', show.progress = FALSE) ; print(dim(marvel5$DE$PSI$Table[[1]])) })
