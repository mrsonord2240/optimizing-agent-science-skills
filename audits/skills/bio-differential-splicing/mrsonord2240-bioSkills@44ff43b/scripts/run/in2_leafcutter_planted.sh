#!/bin/bash
# Input 2: leafcutter on the PLANTED 3v3 set, following SKILL.md 'leafcutter Differential Intron Usage' step by step.
# Truth: skipping intron (201-900 in 1-based; 200-900 0-based junc) ref usage ~0.11 in G1 vs ~0.67 in G2 -> |deltapsi| ~0.55
export PYTHONDONTWRITEBYTECODE=1
AS=/mnt/openscience/audit-envs/alternative-splicing
P=$AS/public-data/planted
LC=$AS/tools/src/leafcutter
CORE="micromamba run -n as-core"
RL="micromamba run -n as-rleaf"
R=/mnt/openscience/audits/bio-differential-splicing/run
W=$R/out/in2; rm -rf $W; mkdir -p $W; cd $W
echo "=== regtools junctions extract (SKILL.md flags: -a 8 -m 50 -s XS)"
for bam in $P/*.bam; do
  b=$(basename ${bam%.bam})
  $CORE regtools junctions extract -a 8 -m 50 -s XS "$bam" -o $b.junc
done
ls *.junc | tr '\n' ' '; echo
echo "G1_rep1.junc:"; cat G1_rep1.junc
ls *.junc > juncfiles.txt
echo "=== (1) clustering exactly as SKILL.md (-m 50 -l 500000), contig chrP"
$CORE python $LC/clustering/leafcutter_cluster_regtools.py -j juncfiles.txt -o leafcutter -m 50 -l 500000 > cl1.log 2>&1; echo "rc=$?"; tail -3 cl1.log | cut -c1-200
ls leafcutter_* 2>/dev/null
echo "counts rows: $(zcat leafcutter_perind_numers.counts.gz 2>/dev/null | tail -n +2 | wc -l)"
echo "=== (2) same with -k True (contig chrP is not chr1..22/X/Y)"
$CORE python $LC/clustering/leafcutter_cluster_regtools.py -j juncfiles.txt -o lc -m 50 -l 500000 -k True > cl2.log 2>&1; echo "rc=$?"
zcat lc_perind_numers.counts.gz | head -5
echo "=== (3) groups file with SKILL.md placeholder names s1..s6 (do not match junc names)"
printf 's1\tcontrol\ns2\tcontrol\ns3\tcontrol\ns4\ttreatment\ns5\ttreatment\ns6\ttreatment\n' > groups_skill.txt
$RL Rscript $LC/scripts/leafcutter_ds.R --num_threads 4 -o ds_skillnames lc_perind_numers.counts.gz groups_skill.txt > ds_skillnames.log 2>&1; echo "rc=$?"; tail -4 ds_skillnames.log | cut -c1-250
echo "=== (4) groups file with correct names, leafcutter_ds.R DEFAULTS (as SKILL.md: only --num_threads, -o, exon_file omitted)"
printf 'G1_rep1\tcontrol\nG1_rep2\tcontrol\nG1_rep3\tcontrol\nG2_rep1\ttreatment\nG2_rep2\ttreatment\nG2_rep3\ttreatment\n' > groups.txt
$RL Rscript $LC/scripts/leafcutter_ds.R --num_threads 4 -o ds_default lc_perind_numers.counts.gz groups.txt > ds_default.log 2>&1; echo "rc=$?"; tail -4 ds_default.log | cut -c1-300
ls ds_default_* 2>/dev/null
echo "=== (5) with -i 3 (min_samples_per_intron=3; other defaults -g 3 -c 20)"
$RL Rscript $LC/scripts/leafcutter_ds.R --num_threads 4 -i 3 -o ds_i3 lc_perind_numers.counts.gz groups.txt > ds_i3.log 2>&1; echo "rc=$?"; tail -3 ds_i3.log | cut -c1-300
echo "--- cluster_significance"; cat ds_i3_cluster_significance.txt
echo "--- effect_sizes"; cat ds_i3_effect_sizes.txt
echo "=== (6) SKILL.md 'Common Errors' pre-filter flags --min_samples_per_intron 5 --min_samples_per_group 3 on 3v3"
$RL Rscript $LC/scripts/leafcutter_ds.R --num_threads 4 --min_samples_per_intron 5 --min_samples_per_group 3 -o ds_prefilter lc_perind_numers.counts.gz groups.txt > ds_prefilter.log 2>&1; echo "rc=$?"; tail -2 ds_prefilter.log | cut -c1-300
echo "=== (7) SKILL.md invokes 'leafcutter_ds.R' via system(): is it on PATH after installing the R package?"
$RL bash -c 'which leafcutter_ds.R || echo "leafcutter_ds.R not on PATH inside as-rleaf"; Rscript -e "cat(system.file(\"scripts\", package=\"leafcutter\"), \"|\", list.files(system.file(package=\"leafcutter\"))[1:12], \"\n\")"'
echo "=== (8) exon_file column-format check, --exon_file with a made-up file"
printf 'chr\tstart\tend\tstrand\tgene_name\nchrP\t101\t200\t+\tG1\nchrP\t501\t600\t+\tG1\nchrP\t901\t1000\t+\tG1\n' > exons.txt
$RL Rscript $LC/scripts/leafcutter_ds.R --num_threads 4 -i 3 -e exons.txt -o ds_exon lc_perind_numers.counts.gz groups.txt > ds_exon.log 2>&1; echo "rc=$?"; tail -3 ds_exon.log | cut -c1-200; cat ds_exon_cluster_significance.txt
