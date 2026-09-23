#!/bin/bash
# NEW input 10, step 3: a real Mutect2 run (GATK 4.6.2.0) on the real human PE BAM, after setting MAPQ to 10 on exactly 100 primary reads and
# MAPQ to 0 on 20 others, to see with GATK's own read-filter tally whether Mutect2 removes low-MAPQ reads itself.
# Then the same with HaplotypeCaller for comparison. Output = the "Filtered N total reads" block GATK prints.
set -u
D=/mnt/openscience/audits/bio-alignment-filtering/run/data/w10; mkdir -p $D; cd $D
H=$AFDATA/human
python - <<'PY'
import pysam, os
src = os.environ['AFDATA'] + '/human/test.paired_end.sorted.bam'
n10 = n0 = 0
with pysam.AlignmentFile(src) as fin, pysam.AlignmentFile('lowmq.bam', 'wb', header=fin.header) as fo:
    for r in fin:
        if not r.is_unmapped and not r.is_secondary and not r.is_supplementary and r.mapping_quality >= 30:
            if n10 < 100 and r.reference_start % 7 == 0: r.mapping_quality = 10; n10 += 1
            elif n0 < 20 and r.reference_start % 11 == 0: r.mapping_quality = 0; n0 += 1
        fo.write(r)
print('set MAPQ 10 on', n10, 'reads and MAPQ 0 on', n0, 'reads')
PY
samtools index lowmq.bam
echo "records MAPQ<20 & >0: $(samtools view -c -q 1 lowmq.bam) minus $(samtools view -c -q 20 lowmq.bam)  => $(( $(samtools view -c -q 1 lowmq.bam) - $(samtools view -c -q 20 lowmq.bam) )); MAPQ 0 mapped: $(samtools view -c -F 4 lowmq.bam) - $(samtools view -c -F 4 -q 1 lowmq.bam)"
for t in Mutect2 HaplotypeCaller; do
  echo "===== $t"
  gatk $t -R $H/genome.fasta -I lowmq.bam -O $t.vcf.gz -L chr22:1900-4700 > $t.log 2>&1
  grep -E "Filtered|ReadFilter|total reads|Analyzed|ERROR|Exception" $t.log | head -20
done
