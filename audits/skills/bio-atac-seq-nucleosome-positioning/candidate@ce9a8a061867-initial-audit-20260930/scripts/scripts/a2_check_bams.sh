export PATH=$NPENV/bin:$PATH
B=$NP/work/a2/B
for f in gm_nfr gm_mono; do
  echo "$f records: $(samtools view -c $B/$f.bam)  MAPQ<30: $(samtools view $B/$f.bam | awk '$5<30' | wc -l)  proper-pair flag set: $(samtools view -c -f 2 $B/$f.bam)"
  samtools view $B/$f.bam | awk '{l=$9<0?-$9:$9; n++; if(l<100)a++; if(l>=180&&l<=247)b++} END{print "  frac |TLEN|<100:", a/n, " frac 180-247:", b/n}'
done
echo "input BAM MAPQ<30 read records (chr1 slice): $(samtools view /mnt/openscience/audit-envs/atac-seq/public-data/encode/GM12878_rep1_filtered.chr1_1-30000000.bam | awk '$5<30' | wc -l)"
