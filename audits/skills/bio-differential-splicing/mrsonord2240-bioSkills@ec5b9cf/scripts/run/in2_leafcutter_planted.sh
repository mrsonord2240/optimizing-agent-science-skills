#!/bin/bash
# INPUT 2 (variant A, regression): leafcutter on the PLANTED 3v3 set (SYNTHETIC), following the FIXED SKILL.md step by step, then the shipped R example
# from a clean copy. Truth: skipping intron 200-900 (0-based junc) usage ~0.11 in G1 vs ~0.67 in G2 -> deltapsi (group2 - group1) ~ +0.55.
source /mnt/openscience/audits/bio-differential-splicing/run/common.sh
export LEAFCUTTER=$LC
$CORE python $R/extract_blocks.py get 2 /tmp/blk2.sh
$CORE python $R/extract_blocks.py get 3 /tmp/blk3.sh
$CORE python $R/extract_blocks.py get 4 /tmp/blk4.R
W=$R/out/in2; rm -rf $W; mkdir -p $W; cd $W
cp $P/G*_rep*.bam $P/G*_rep*.bam.bai .   # BAM indexes are required by regtools
echo "=== (1) SKILL.md block 1 (regtools + clustering) VERBATIM, bash, LEAFCUTTER=clone; note BAMs are G1_rep1..G2_rep3, contig chrP"
sed -e 's#^\(\s*\)regtools#\1regtools#' /tmp/blk2.sh > blk2.sh
PATH=$R/bin:$PATH bash blk2.sh > blk2.log 2>&1; echo "rc=$?"; tail -3 blk2.log | cut -c1-200
echo "junc files: $(ls *.junc | tr '\n' ' ')"; echo "G1_rep1.junc:"; cat G1_rep1.junc
echo "counts rows (verbatim, no -k True): $(zcat leafcutter_perind_numers.counts.gz | tail -n +2 | wc -l)  (Skill: contigs other than chr1..22,X,Y are dropped silently -> 0 introns)"
echo "=== (2) same with -k True"
PATH=$R/bin:$PATH python $LC/clustering/leafcutter_cluster_regtools.py -j juncfiles.txt -o lck -m 50 -l 500000 -k True > cl2.log 2>&1; echo "rc=$?"
echo "counts rows (-k True): $(zcat lck_perind_numers.counts.gz | tail -n +2 | wc -l)"; zcat lck_perind_numers.counts.gz | head -4
echo "=== (3) groups file: names must equal counts column names"
printf 'G1_rep1\tcontrol\nG1_rep2\tcontrol\nG1_rep3\tcontrol\nG2_rep1\ttreatment\nG2_rep2\ttreatment\nG2_rep3\ttreatment\n' > groups.txt
echo "--- default flags (Skill: they stop below 5 samples per group)"
$RL Rscript $LC/scripts/leafcutter_ds.R --num_threads 4 -o ds_default lck_perind_numers.counts.gz groups.txt > ds_default.log 2>&1; echo "rc=$?"; tail -2 ds_default.log | cut -c1-200
grep -c 'less than min_samples_per_intron' ds_default.log
echo "--- gtf_to_exons.R as documented (planted.gtf has gene_name), then the SKILL.md ds command (-i 3 -g 3 -c 10 --exon_file)"
gzip -c $P/planted.gtf > annotation.gtf.gz
$RL Rscript $LC/scripts/gtf_to_exons.R annotation.gtf.gz gencode_exons.txt.gz > exons.log 2>&1; echo "gtf_to_exons rc=$?"; zcat gencode_exons.txt.gz | head -4
sed -e 's#^Rscript#micromamba run -n as-rleaf Rscript#' /tmp/blk3.sh | sed -e '/^#/d' > blk3.sh
cat blk3.sh | head -5
sed -i 's#leafcutter_perind_numers.counts.gz#lck_perind_numers.counts.gz#' blk3.sh
LEAFCUTTER=$LC bash blk3.sh > ds_skill.log 2>&1; echo "rc=$?"; tail -2 ds_skill.log | cut -c1-200
cat ds_results_cluster_significance.txt; cat ds_results_effect_sizes.txt
echo "--- SKILL.md R block (block 4) VERBATIM"
cat > blk4_run.R <<'RR'
RR
cat /tmp/blk4.R >> blk4_run.R; echo "print(sig_clusters); print(intron_effects)" >> blk4_run.R
$RL Rscript blk4_run.R 2>&1 | cut -c1-220
$CORE python - <<'PY'
import pandas as pd
s = pd.read_csv('ds_results_cluster_significance.txt', sep='\t'); e = pd.read_csv('ds_results_effect_sizes.txt', sep='\t')
assert (s['status'] == 'Success').sum() == 1 and s['p.adjust'].iloc[0] < 1e-6
skip = e[e['intron'].str.contains(':200:900:') | e['intron'].str.contains(':201:900:') | e['intron'].str.contains(':200:901:')]
print(e[['intron','deltapsi']].to_string())
assert abs(e['deltapsi'].max() - 0.5446) < 0.01, 'deltapsi of skipping intron'
print('ASSERT OK: 1 cluster tested, p.adjust %.2g, max deltapsi %.4f (planted truth ~0.55; TOOLS.md hand value)' % (s['p.adjust'].iloc[0], e['deltapsi'].max()))
PY
echo "=== (4) SKILL.md n<4 caution: default-flag variants -i 3 only (i.e. the old 'pre-filter' flags the Skill now says NOT to add)"
$RL Rscript $LC/scripts/leafcutter_ds.R --num_threads 4 --min_samples_per_intron 5 --min_samples_per_group 3 -o ds_prefilter lck_perind_numers.counts.gz groups.txt > ds_prefilter.log 2>&1; echo "rc=$?"; tail -1 ds_prefilter.log | cut -c1-200

echo "=== (5) shipped examples/diff_splicing_leafcutter.R from a clean COPY (samples control1..3/treatment1..3 = planted G1/G2 BAMs renamed)"
mkdir -p $W/ex; cd $W/ex
i=1; for g in G1; do for r in 1 2 3; do cp $P/${g}_rep$r.bam control$r.bam; cp $P/${g}_rep$r.bam.bai control$r.bam.bai; done; done
for r in 1 2 3; do cp $P/G2_rep$r.bam treatment$r.bam; cp $P/G2_rep$r.bam.bai treatment$r.bam.bai; done
cp $SK/examples/diff_splicing_leafcutter.R example.R
echo "--- (5a) as shipped (NONSTANDARD_CONTIGS <- FALSE; chrP contig)"
mkdir -p a; cd a; cp ../*.bam ../*.bai ../example.R .
LEAFCUTTER_DIR=$AS/tools/src/leafcutter PATH=$R/bin:$PATH Rscript example.R > run.log 2>&1; echo "rc=$?"; tail -6 run.log | cut -c1-220
cd ..
echo "--- (5b) NONSTANDARD_CONTIGS <- TRUE"
mkdir -p b; cd b; cp ../*.bam ../*.bai ../example.R .
sed -i 's/^NONSTANDARD_CONTIGS <- FALSE/NONSTANDARD_CONTIGS <- TRUE/' example.R; grep -n '^NONSTANDARD' example.R
LEAFCUTTER_DIR=$AS/tools/src/leafcutter PATH=$R/bin:$PATH Rscript example.R > run.log 2>&1; echo "rc=$?"; tail -12 run.log | cut -c1-220
cat groups.txt
$CORE python - <<'PY'
import pandas as pd
s = pd.read_csv('differential_cluster_significance.txt', sep='\t'); e = pd.read_csv('differential_effect_sizes.txt', sep='\t')
assert (s['status'] == 'Success').sum() == 1 and s['p.adjust'].iloc[0] < 1e-6 and abs(e['deltapsi'].max() - 0.5446) < 0.01
print('ASSERT OK (shipped R example, NONSTANDARD_CONTIGS=TRUE): 1 cluster, p.adjust %.2g, max deltapsi %.4f' % (s['p.adjust'].iloc[0], e['deltapsi'].max()))
PY
