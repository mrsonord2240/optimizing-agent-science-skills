#!/bin/bash
# NEW: independent check of the two claims the round-2 fixer says the earlier re-audit got wrong, on my own planted BAM (own_del.bam: 20 D reads, 20 spliced N reads, 10 overlapping pairs)
# and on the REAL human and ARTIC BAMs. Also the flag names in the overlap table.
export LC_ALL=C PYTHONIOENCODING=utf-8
R=/mnt/openscience/audits/bio-bam-statistics/run; N=$R/data/new; cd $R/work; rm -f md_*
python $R/n4_overlap_del.py
echo "=== REAL human BAM: bcftools mpileup INFO/DP vs FORMAT/DP with / without -x  (sum over printed positions / 40001)"
H=$AFDATA/human/test.paired_end.sorted.bam; HF=$AFDATA/human/genome.fasta
for opt in "" "-x" "-Q 0" "-B"; do
  echo -n "bcftools mpileup -d 1000000 $opt : "; bcftools mpileup -d 1000000 $opt -a FORMAT/DP -f $HF $H 2>/dev/null | bcftools query -f '%INFO/DP\t[%DP]\n' | awk '{i+=$1; f+=$2} END{printf "INFO/DP mean %.2f  FORMAT/DP mean %.2f\n", i/40001, f/40001}'
done
echo "=== REAL ARTIC BAM: mosdepth default vs --fast-mode vs depth -aa vs depth -aa -J (deletions)"
A=$R/work/art.bam; cp $AFDATA/sarscov2/sars-cov-2_v5.3.2.nanopore.bam $A; samtools index $A
mosdepth -t 1 ma $A; tail -1 ma.mosdepth.summary.txt | cut -f1-4; mosdepth -t 1 --fast-mode mf $A; tail -1 mf.mosdepth.summary.txt | cut -f1-4
echo -n "depth -aa: "; samtools depth -aa $A | awk '{s+=$3;n++} END{printf "%.4f\n", s/n}'; echo -n "depth -aa -J: "; samtools depth -aa -J $A | awk '{s+=$3;n++} END{printf "%.4f\n", s/n}'
echo "=== REAL RNA BAM (spliced): mosdepth default vs --fast-mode vs depth -aa (does fast-mode also count N?)"
RN=$R/work/rna.bam; cp $AFDATA/human/test.rna.paired_end.sorted.bam $RN; samtools index $RN
mosdepth -t 1 mra $RN; tail -1 mra.mosdepth.summary.txt | cut -f1-4; mosdepth -t 1 --fast-mode mrf $RN; tail -1 mrf.mosdepth.summary.txt | cut -f1-4
echo -n "depth -aa: "; samtools depth -aa $RN | awk '{s+=$3;n++} END{printf "%.4f (n=%d)\n", s/n, n}'
echo "=== flag names in the overlap paragraph"
samtools mpileup --help 2>&1 | grep -E -- '--disable-overlap-removal|-x,' | head -2; bcftools mpileup --help 2>&1 | grep -iE -- 'overlap' | head -3
samtools depth --help 2>&1 | grep -E -- '^ +-s' | head -1
