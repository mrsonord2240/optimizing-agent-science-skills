# Common Errors rows not yet reproduced: pyGenomeTracks BAM track / missing file_type; prepare_results.R with a wrong annotation prefix; regtools on an unindexed BAM
source /mnt/openscience/audits/bio-sashimi-plots/run/scripts/env.sh
LC=$SRC/leafcutter; P=$AS/public-data/planted
W=$RUN/out/i10; rm -rf $W; mkdir -p $W; cd $W
cp $P/G1_rep1.bam . ; cp $P/planted.gtf .
cat > t1.ini <<'INI'
[bam]
file = G1_rep1.bam
height = 3
file_type = bam
INI
micromamba run -n as-viz-gg34 pyGenomeTracks --tracks t1.ini --region chrP:1-1200 -o t1.png > t1.log 2>&1; echo "pgt BAM track rc=$? png=$([ -f t1.png ] && echo yes || echo no)"; grep -a -E "Error|error" t1.log | head -2
cat > t2.ini <<'INI'
[genes]
file = planted.gtf
[cov]
file = G1_rep1.bam
INI
micromamba run -n as-viz-gg34 pyGenomeTracks --tracks t2.ini --region chrP:1-1200 -o t2.png > t2.log 2>&1; echo "pgt no file_type rc=$? png=$([ -f t2.png ] && echo yes || echo no)"; grep -a -E "Error|error" t2.log | head -2
cd $RUN/out/i6_leafviz
micromamba run -n as-rleaf Rscript $LC/leafviz/prepare_results.R -o /tmp/x.RData -m groups.txt leafcutter_perind_numers.counts.gz ds_results_cluster_significance.txt ds_results_effect_sizes.txt WRONGPREFIX > $W/pr.log 2>&1; echo "prepare_results wrong prefix rc=$?"; tr '\r' '\n' < $W/pr.log | grep -a -i -E "does not exist|error" | head -2
cd $W; cp $P/G1_rep1.bam u.bam
micromamba run -n as-core regtools junctions extract -s XS -o u.bed u.bam > u.log 2>&1; echo "regtools unindexed rc=$? bed lines=$(wc -l < u.bed 2>/dev/null || echo 0)"; head -3 u.log
micromamba run -n as-core samtools index u.bam; micromamba run -n as-core regtools junctions extract -s XS -o u2.bed u.bam > u2.log 2>&1; echo "regtools indexed rc=$? bed lines=$(wc -l < u2.bed)"
rm -f /tmp/x.RData
