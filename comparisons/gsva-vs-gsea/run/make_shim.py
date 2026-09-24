# Minimal GSVA >= 1.50 (param-object API) shim applied to COPIES of the three Open Science skills.
# Only the gsva() call site and msigdbr collection args are touched; no statistics or logic changed.
import re, io
base = r'F:/OpenScience/comparisons/gsva-vs-gsea/shim/'
def sub(path, old, new, count=1):
    s = io.open(path, encoding='utf-8').read()
    assert old in s, (path, old[:40])
    s = s.replace(old, new, count)
    io.open(path, 'w', encoding='utf-8', newline='').write(s)

newcall = '''  em <- as.matrix(exp_mat)
  prm <- if (identical(opt$method, "ssgsea")) {
    GSVA::ssgseaParam(em, gene_sets, alpha = opt$tau, minSize = opt$min_sz, maxSize = opt$max_sz, normalize = TRUE)
  } else {
    GSVA::gsvaParam(em, gene_sets, kcdf = opt$kcdf, tau = opt$tau, minSize = opt$min_sz, maxSize = opt$max_sz, maxDiff = opt$mx_diff)
  }
  GSVA::gsva(prm, verbose = FALSE)
'''
# 1 gsva skill
p = base + 'gsva-analysis-and-visualization/scripts/functions.R'
s = io.open(p, encoding='utf-8').read()
i = s.index('  gsva_args <- list('); j = s.index('  do.call(GSVA::gsva, gsva_args)\n') + len('  do.call(GSVA::gsva, gsva_args)\n')
s = s[:i] + newcall + s[j:]
s = s.replace('category = category,\n    subcategory = subcategory', 'collection = category,\n    subcollection = subcategory')
s = s.replace('msigdbr::msigdbr(\n    species = species,', 'msigdbr::msigdbr(\n    species = species,')
io.open(p, 'w', encoding='utf-8', newline='').write(s)
# 2 immune-pathway skill
p = base + 'immune-pathway-analysis/scripts/functions.R'
s = io.open(p, encoding='utf-8').read()
i = s.index('  gsva_args <- list('); j = s.index('run_limma_diff')
s = s[:i] + newcall + '}\n\n' + s[j:]
io.open(p, 'w', encoding='utf-8', newline='').write(s)
# 3 ssgsea skill
p = base + 'ssgsea-immune-infiltration-analysis/scripts/functions.R'
s = io.open(p, encoding='utf-8').read()
i = s.index('  res <- tryCatch(\n    GSVA::gsva('); j = s.index('  attr(res, "actual_parallel_sz")')
new = '''  em <- as.matrix(exp_mat)
  prm <- if (identical(method, "ssgsea")) {
    GSVA::ssgseaParam(em, genesets, alpha = tau, minSize = min_sz, maxSize = max_sz, normalize = TRUE)
  } else {
    GSVA::gsvaParam(em, genesets, kcdf = kcdf, tau = tau, minSize = min_sz, maxSize = max_sz, maxDiff = mx_diff)
  }
  res <- tryCatch(GSVA::gsva(prm, verbose = FALSE),
    error = function(e) skill_stop("SKILL_INVALID_PARAMETER", paste("GSVA failed:", conditionMessage(e))))
'''
s = s[:i] + new + s[j:]
io.open(p, 'w', encoding='utf-8', newline='').write(s)
print('ok')
