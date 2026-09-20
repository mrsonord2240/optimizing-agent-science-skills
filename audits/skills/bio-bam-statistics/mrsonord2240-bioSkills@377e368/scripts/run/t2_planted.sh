#!/bin/bash
# INPUT 2 (NEW, SYNTHETIC planted depth): zero-coverage regions, a contig with no reads, contig-end stack, deletions, spliced reads,
# default-excluded reads, overlapping pairs. Truth by construction (make_depth.py). Every mean-depth / >=Nx / breadth recipe vs truth.
export LC_ALL=C PYTHONIOENCODING=utf-8
R=/mnt/openscience/audits/bio-bam-statistics/run; cd $R/work
B=$R/data/planted_depth.bam; BED=$R/data/planted_depth.regions.bed
python - <<'PY'
import json
t = json.load(open('/mnt/openscience/audits/bio-bam-statistics/run/data/planted_depth.truth.json'))
L = t['total_bases']
print(f"TRUTH all 4 contigs ({L} bp): mean {t['mean_depth_default_all_contigs']:.6f} ge10 {100*t['ge10_default']/L:.4f}% ge20 {100*t['ge20_default']/L:.4f}% covered {t['covered_default']} max {t['max_default']}")
print(f"TRUTH mates once: mean {t['mean_depth_mates_once']:.6f}; ge10 {100*t['ge10_once']/L:.4f}% ge20 {100*t['ge20_once']/L:.4f}%")
Lc = t['covered_contigs_only_len']
print(f"TRUTH if the denominator is only contigs with reads ({Lc} bp): mean {t['sum_depth_default']/Lc:.6f}   ge10 {100*t['ge10_default']/Lc:.4f}%")
PY
echo "=== block 018 verbatim (depth -aa, every @SQ position)"
sed 's#input.bam#'$B'#' ../blocks/018_bash.sh > b018.sh; bash b018.sh
echo "=== same recipe but with -a (SKILL: -a omits contigs that have no reads)"; sed 's/depth -aa/depth -a/' b018.sh > b018a.sh; bash b018a.sh
echo "row counts: depth (no -a) / -a / -aa  (all @SQ = 22000, without chrC = 19000)"; for o in "" "-a" "-aa"; do samtools depth $o $B | wc -l; done
echo "contigs present in -a / -aa output"; samtools depth -a $B | cut -f1 | uniq -c; samtools depth -aa $B | cut -f1 | uniq -c
echo "=== samtools coverage per contig and depth-weighted overall"
samtools coverage $B | cut -f1-8 | tee cov.tsv
awk -F'\t' 'NR>1{len=$3-$2+1; s+=$7*len; l+=len; c+=$5} END{printf "coverage-weighted mean over all contigs = %.6f ; covbases=%d\n", s/l, c}' cov.tsv
echo "=== mosdepth (default, fast-mode) summary"; mosdepth -t 2 mdG $B; cat mdG.mosdepth.summary.txt; mosdepth --fast-mode -t 2 mdH $B; grep -E 'chrA|chrD|total' mdH.mosdepth.summary.txt
echo "=== mosdepth --by BED --thresholds (block 021 form) vs truth"
mosdepth --by $BED --thresholds 1,10,20,30,100 --no-per-base mdI $B; zcat mdI.thresholds.bed.gz; zcat mdI.regions.bed.gz
echo "=== block 022: samtools depth -a -b BED row count (truth 1000+500+500+100+300+110+600 = 3110)"; samtools depth -a -b $BED $B | wc -l
echo "=== block 026 coverage-from-BED loop (verbatim, extra BED columns, chrC no reads, contig end, start=0)"
sed 's#regions.bed#'$BED'#; s#input.bam#'$B'#' ../blocks/026_bash.sh > b026.sh; bash b026.sh
echo "=== BED with a header line (track/browser), the way real BEDs often arrive"
( echo 'track name=targets'; head -2 $BED ) > hdr.bed; sed 's#regions.bed#hdr.bed#; s#input.bam#'$B'#' ../blocks/026_bash.sh > b026h.sh; bash b026h.sh 2>&1 | head -5
echo "=== overlap: depth -aa -s over chrA:7001-7150 vs default (truth by construction: default 10 pairs*200 bases/150 = 13.33; -s 10*150/150 = 10)"
samtools depth -a -r chrA:7001-7150 $B | awk '{s+=$3;n++} END{print "default mean", s/n, "rows", n}'; samtools depth -a -s -r chrA:7001-7150 $B | awk '{s+=$3;n++} END{print "-s mean", s/n}'
echo "=== block 030 region_depth_stats vs truth-by-construction arrays and samtools depth -a"
python ../t2_region_vs_truth.py
echo "=== pysam pileup DEFAULTS vs the recipe on chrA[3000,3100) (7 reads incl 4 low-BQ + 3 MAPQ0 on top of 8x): truth 15"
python - <<'PY'
import pysam
B='/mnt/openscience/audits/bio-bam-statistics/run/data/planted_depth.bam'
with pysam.AlignmentFile(B) as b:
    d = {c.reference_pos: c.n for c in b.pileup('chrA', 3000, 3100, truncate=True)}
    print('pysam pileup defaults n at 3050:', d.get(3050), '| n over deletions region chrD[550,560) default:', [c.n for c in b.pileup('chrD', 550, 560, truncate=True)][:3], '(pileup.n counts deletions; recipe excludes them)')
PY
echo "=== follow-up: block 022 (depth -a -b) rows and chrC handling; mosdepth summary total"
echo "depth -a  -b : $(samtools depth -a  -b $BED $B | wc -l) rows (truth 3110 if zeros incl.)"; echo "depth -aa -b : $(samtools depth -aa -b $BED $B | wc -l) rows"
echo "chrC rows with -a : $(samtools depth -a -b $BED $B | grep -c '^chrC')   with -aa : $(samtools depth -aa -b $BED $B | grep -c '^chrC')"
echo "mosdepth summary total row: $(grep total mdG.mosdepth.summary.txt)"
echo "=== block 025 coverage -r region (chrA:1001-2000 truth mean 30) and block 023 large-file idioms"
samtools coverage -r chrA:1001-2000 $B | cut -f1-7
samtools view -s 42.1 -b -o sub.bam $B && samtools index sub.bam && samtools depth -a sub.bam | awk '{s+=$3;n++} END{print "subsample 10% depth -a rows", n, "mean", s/n}'
