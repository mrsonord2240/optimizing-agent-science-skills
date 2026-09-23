#!/bin/bash
# NEW: content check for the blocks that only write files (t9 shows rc, not content): stats on a region, depth / depth -a / depth -aa files, idxstats total.
export LC_ALL=C PYTHONIOENCODING=utf-8
R=/mnt/openscience/audits/bio-bam-statistics/run; cd $R/work; rm -rf fb; mkdir fb; cd fb
H=$AFDATA/human/test.paired_end.sorted.bam; cp $H input.bam; cp $H.bai input.bam.bai
sed 's#chr1:1000000-2000000#chr22:1952-2952#' $R/blocks/013_bash.sh > b13.sh; bash b13.sh
echo "region stats raw total sequences: $(grep '^SN' region_stats.txt | grep 'raw total' | cut -f3) ; independent: samtools view -c -F 2304 input.bam chr22:1952-2952 = $(samtools view -c -F 2304 input.bam chr22:1952-2952)"
sed -n '1,4p' $R/blocks/014_bash.sh > /dev/null; bash $R/blocks/014_bash.sh; echo "depth.txt rows $(wc -l < depth.txt) (covered positions 1181)"
sed 's#input.bam >#input.bam >#' $R/blocks/016_bash.sh | bash; echo "depth_with_zeros rows $(wc -l < depth_with_zeros.txt) ; depth_all_contigs rows $(wc -l < depth_all_contigs.txt) (contig 40001 bp)"
echo "block 008 first recipe total mapped: $(samtools idxstats input.bam | awk '{sum += $3} END {print sum}') ; stats 'reads mapped' incl secondary: independent samtools view -c -F 4 = $(samtools view -c -F 4 input.bam)"
bash $R/blocks/009_bash.sh; wc -l < stats.txt | sed 's/^/stats.txt lines: /'
