# Input 6a: leafviz workflow (SKILL.md block 06) on planted leafcutter output. Prerequisite steps (regtools -> cluster -> leafcutter_ds.R) are not part of the Skill.
source /mnt/openscience/audits/bio-sashimi-plots/run/scripts/env.sh
LC=$SRC/leafcutter; P=$AS/public-data/planted
W=$RUN/out/i6_leafviz; rm -rf $W; mkdir -p $W; cd $W
CORE="micromamba run -n as-core"; RL="micromamba run -n as-rleaf"
for s in G1_rep1 G1_rep2 G1_rep3 G2_rep1 G2_rep2 G2_rep3; do $CORE regtools junctions extract -a 8 -m 50 -M 500000 -s XS -o $s.junc $P/$s.bam > /dev/null 2>&1; done
ls *.junc > juncfiles.txt
printf 'G1_rep1\tG1\nG1_rep2\tG1\nG1_rep3\tG1\nG2_rep1\tG2\nG2_rep2\tG2\nG2_rep3\tG2\n' > groups.txt
$CORE python $LC/clustering/leafcutter_cluster_regtools.py -j juncfiles.txt -m 30 -o leafcutter -l 500000 -k True > cluster.log 2>&1; echo "cluster rc=$?"
$RL Rscript $LC/scripts/leafcutter_ds.R --num_threads 2 -i 3 -g 3 -c 5 -o ds_results leafcutter_perind_numers.counts.gz groups.txt > ds.log 2>&1; echo "ds rc=$?"
ls ds_results_*; echo "effect sizes:"; cat ds_results_effect_sizes.txt
# ---- SKILL.md block 06, literal except paths (leafcutter/ -> clone, annotation.gtf -> planted GTF, /abs/path -> here)
sed -e "s#leafcutter/leafviz#$LC/leafviz#g;s#annotation.gtf#$P/planted.gtf#;s#/abs/path/leafviz.RData#$W/leafviz.RData#" $RUN/blocks/06_*.sh > b06.sh
# split: everything before the 'cd ... run_leafviz' line runs to completion; the app is started in the background and probed
grep -v "run_leafviz.R" b06.sh > b06_pre.sh
echo "--- gtf2leafcutter.pl + prepare_results.R (block 06, first two commands)"
$RL bash b06_pre.sh > b06_pre.log 2>&1; echo "pre rc=$?"; tail -6 b06_pre.log | cut -c1-200
ls -l annot_* leafviz.RData 2>&1 | awk '{print $5,$9}'
echo "--- run_leafviz.R from leafviz/ (as documented)"
( cd $LC/leafviz && timeout 40 $RL Rscript run_leafviz.R $W/leafviz.RData > $W/app.log 2>&1 ) &
for i in $(seq 1 15); do sleep 2; grep -a -q "Listening on" $W/app.log && break; done
tr '\r' '\n' < app.log | grep -a -E "Listening|Error|error" | head -3
PORT=$(grep -a -o "127.0.0.1:[0-9]*" app.log | head -1 | cut -d: -f2)
echo "port=$PORT curl: $(curl -s -o /dev/null -w '%{http_code} %{size_download}' http://127.0.0.1:$PORT/ 2>&1)"
curl -s http://127.0.0.1:$PORT/ | grep -a -o "<title>[^<]*</title>" | head -1
wait
echo "--- run_leafviz.R from the wrong directory (Skill Common Errors row)"
timeout 30 $RL Rscript $LC/leafviz/run_leafviz.R $W/leafviz.RData > wrongdir.log 2>&1; tr '\r' '\n' < wrongdir.log | grep -a -i -E "App dir|Error" | head -2
echo "--- library(leafviz) / run_leafviz() as the old Skill said"
$RL Rscript -e 'cat("leafviz installed:", requireNamespace("leafviz", quietly=TRUE), " leafcutter loads:", requireNamespace("leafcutter", quietly=TRUE), "\n")' 2>&1 | tail -1
