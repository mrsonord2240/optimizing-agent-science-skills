library(MARVEL); library(Seurat); library(data.table)

seurat_obj <- readRDS('cells.rds')   # meta.data: one row per cell, cell-type column 'cell.type'

# Build wide SJ matrix: first column 'coord.intron' (e.g. 'chr1:100007082:100022621'),
# subsequent columns are per-cell sample IDs with junction counts as values.
# This is constructed from STAR SJ.out.tab files (one per cell) merged on intron coord.
sj_files <- list.files('star_pass2/', pattern='SJ.out.tab$', full.names=TRUE)
sj_long <- rbindlist(lapply(sj_files, function(f) {
    d <- fread(f, sep='\t', header=FALSE,
               col.names=c('chr','start','end','strand','motif','annot','unique','multi','overhang'))
    d$coord.intron <- paste(d$chr, d$start, d$end, sep=':')
    d$sample <- gsub('_SJ.out.tab$', '', basename(f))
    d[, .(coord.intron, sample, unique)]
}))
sj <- dcast(sj_long, coord.intron ~ sample, value.var='unique', fill=0)

# SpliceFeature is a NAMED LIST keyed by event class (tables from Preprocess_rMATS above)
df.feature.list <- list(
    SE   = read.table('events_SE.txt',   header=TRUE, sep='\t'),
    A5SS = read.table('events_A5SS.txt', header=TRUE, sep='\t'),
    A3SS = read.table('events_A3SS.txt', header=TRUE, sep='\t'),
    MXE  = read.table('events_MXE.txt',  header=TRUE, sep='\t'),
    RI   = read.table('events_RI.txt',   header=TRUE, sep='\t')
)

# SplicePheno: per-cell metadata; sample.id column maps to SpliceJunction column names
df.pheno <- seurat_obj@meta.data
df.pheno$sample.id <- rownames(df.pheno)

marvel <- CreateMarvelObject(
    SpliceJunction = sj,
    SplicePheno    = df.pheno,
    SpliceFeature  = df.feature.list,
    GeneFeature    = read.table('gene_features.tsv', header=TRUE, sep='\t'),   # gene_id, gene_short_name, gene_type
    Exp            = read.table('tpm.tsv', header=TRUE, sep='\t'),   # non-log TPM; NOT row.names=1: first column must stay gene_id
    GTF            = fread('annotation.gtf', header=FALSE, sep='\t', quote='', data.table=FALSE)   # data.frame, no header (V1..V9)
)

marvel <- CheckAlignment(marvel, level='SJ')
marvel <- ComputePSI(marvel, CoverageThreshold=10, EventType='SE')   # one event class per call; PSI matrix in marvel$PSI$SE is 0-1
marvel <- CheckAlignment(marvel, level='splicing')
marvel <- CheckAlignment(marvel, level='gene')
marvel <- TransformExpValues(marvel, offset=1, transformation='log2', threshold.lower=1)

neurons <- df.pheno$sample.id[df.pheno$cell.type == 'neuron']
glia    <- df.pheno$sample.id[df.pheno$cell.type == 'glia']

# Modality is assigned per cell group (one call per group)
marvel <- AssignModality(marvel, sample.ids=neurons, min.cells=5, seed=1)
head(marvel$Modality$Results)

marvel <- CompareValues(
    marvel,
    cell.group.g1 = neurons, cell.group.g2 = glia,
    min.cells = 5, method = 'wilcox', method.adjust = 'fdr',
    level = 'splicing', event.type = 'SE'
)
res <- marvel$DE$PSI$Table[['wilcox']]   # p.val.adj = FDR; mean.g1, mean.g2, mean.diff = mean.g2 - mean.g1, all in PSI x 100
head(res[order(res$p.val.adj), c('tran_id', 'gene_short_name', 'mean.g1', 'mean.g2', 'mean.diff', 'p.val', 'p.val.adj')])
