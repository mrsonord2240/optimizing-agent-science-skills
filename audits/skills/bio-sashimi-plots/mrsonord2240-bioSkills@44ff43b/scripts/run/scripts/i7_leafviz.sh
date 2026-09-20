source /mnt/openscience/audits/bio-sashimi-plots/run/scripts/env.sh
L=$AS/tools/src/leafcutter
echo "== library(leafviz) / run_leafviz() in as-rleaf"
micromamba run -n as-rleaf Rscript -e 'r <- requireNamespace("leafviz", quietly=TRUE); cat("requireNamespace(leafviz):", r, "\n"); cat("exists run_leafviz():", exists("run_leafviz"), "\n"); cat("leafcutter pkg has run_leafviz:", "run_leafviz" %in% getNamespaceExports("leafcutter"), "\n")' 2>&1 | tr '\r' '\n' | tail -4
echo "== run_leafviz.R usage"; sed -n 1,25p $L/leafviz/run_leafviz.R
echo "== prepare_results.R --help"; micromamba run -n as-rleaf Rscript $L/leafviz/prepare_results.R --help 2>&1 | tr '\r' '\n' | head -14
echo "== prepare_results.R with Skill's exact (missing files) args: exit code + message"
cd $RUN/data; touch groups.txt
micromamba run -n as-rleaf Rscript $L/leafviz/prepare_results.R -o leafviz -m groups.txt leafcutter_perind_numers.counts.gz ds_results_cluster_significance.txt ds_results_effect_sizes.txt annotation_codes 2>&1 | tr '\r' '\n' | tail -4; echo "rc=${PIPESTATUS[0]}"
