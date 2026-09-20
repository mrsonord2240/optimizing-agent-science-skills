#!/bin/bash
# Input 2b: run the shipped examples/diff_splicing_leafcutter.R from a COPY (as-rleaf R, leafcutter 0.2.9 loads),
# then exercise its load_leafcutter_results() on real leafcutter output from in2 (planted 3v3).
export PYTHONDONTWRITEBYTECODE=1
AS=/mnt/openscience/audit-envs/alternative-splicing
LC=$AS/tools/src/leafcutter
CORE="micromamba run -n as-core"
RL="micromamba run -n as-rleaf"
R=/mnt/openscience/audits/bio-differential-splicing/run
W=$R/out/in2b; rm -rf $W; mkdir -p $W; cd $W
cp $R/out/in2/*.junc .
cp $R/skill/examples/diff_splicing_leafcutter.R example.R
echo "=== run the shipped script as-is (Rscript example.R)"
$RL Rscript example.R 2>&1 | tail -8
echo "--- juncfiles.txt written by the example:"; cat juncfiles.txt
echo "--- groups.txt written by the example:"; cat groups.txt
echo "=== cluster with the juncfiles.txt produced by the example (paths './x.junc'), -k True"
$CORE python $LC/clustering/leafcutter_cluster_regtools.py -j juncfiles.txt -o leafcutter -m 50 -l 500000 -k True > cl.log 2>&1; echo "rc=$?"
echo "column names in counts table:"; zcat leafcutter_perind_numers.counts.gz | head -2
echo "=== then leafcutter_ds.R with the groups.txt the example wrote (sample1..sample6)"
$RL Rscript $LC/scripts/leafcutter_ds.R -i 3 -o differential leafcutter_perind_numers.counts.gz groups.txt > ds.log 2>&1; echo "rc=$?"; tail -3 ds.log | cut -c1-200
echo "=== load_leafcutter_results() from the example on real output (in2 ds_i3, planted)"
cp $R/out/in2/ds_i3_cluster_significance.txt differential_cluster_significance.txt
cp $R/out/in2/ds_i3_effect_sizes.txt differential_effect_sizes.txt
cat > call_example_fn.R <<'EOF'
# source only the function definitions of the shipped example (skip its top-level side effects) by eval-ing its parsed exprs
exprs <- parse('example.R')
for (e in exprs) {
  if (is.call(e) && identical(e[[1]], as.name('<-')) && is.call(e[[3]]) && identical(e[[3]][[1]], as.name('function'))) eval(e, globalenv())
}
res <- load_leafcutter_results('differential_cluster_significance.txt', 'differential_effect_sizes.txt')
print(res)
stopifnot(nrow(res) == 3, all(res$p.adjust < 0.05))
stopifnot(abs(max(res$deltapsi) - 0.5446) < 0.01)
cat('ASSERT OK: example merge returns 3 introns, max deltapsi 0.545 (truth ~0.55)\n')
ann <- annotate_clusters(res, 'exons.txt')
print(ann[, c('intron','chr','start','end')])
EOF
printf 'chr\tstart\tend\tstrand\tgene_name\nchrP\t101\t200\t+\tG1\n' > exons.txt
$RL Rscript call_example_fn.R 2>&1 | tail -25
