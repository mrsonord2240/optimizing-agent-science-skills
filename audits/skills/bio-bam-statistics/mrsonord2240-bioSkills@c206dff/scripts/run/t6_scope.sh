#!/bin/bash
# INPUT 6 (scope boundary, REAL+SYNTH): insert-size caveats, adapter-readthrough grep, Picard CollectHsMetrics fields, MultiQC, dict/M5, verifybamid2 attempt
cd /mnt/openscience/audits/bio-bam-statistics/run
export PYTHONIOENCODING=utf-8 PYTHONDONTWRITEBYTECODE=1
D=/mnt/openscience/audit-envs/alignment-files/public-data
{
echo "##### (a) Insert Size Caveats: RF mate-pair library (synthetic, insert 2000, 100 pairs)"
for b in data/rf.bam data/rf_noproper.bam; do
  echo "== $b  (flagstat properly paired:"; samtools flagstat $b | grep "properly paired"; echo ")"
  samtools stats $b > work/$(basename $b).stats
  grep -E "^SN\s(insert size|inward|outward|pairs with other)" work/$(basename $b).stats | cut -f2-3
  echo "IS rows with count>0: $(grep '^IS' work/$(basename $b).stats | awk '$3>0' | wc -l)  (first: $(grep '^IS' work/$(basename $b).stats | awk '$3>0' | head -1))"
  python skill/examples/qc_report.py $b | tail -4
done
echo "##### (b) Skill: samtools stats | grep 'bases soft-clipped' (adapter readthrough detector)"
echo "human BAM has $(python - <<'PY'
import sys; sys.path.insert(0,'.')
from truth import counts
print(counts('work/test.paired_end.sorted.bam')['softclipped_bases'])
PY
) soft-clipped bases by CIGAR hand-count"
echo "grep count in 'samtools stats' (whole output, case-insens 'soft'): $(samtools stats work/test.paired_end.sorted.bam | grep -ci 'soft')"
echo "synthetic (400 soft-clipped bases planted): $(samtools stats data/synth.bam | grep -ci 'soft')"
echo "SN keys containing 'clip' or 'trim':"; samtools stats work/test.paired_end.sorted.bam | grep '^SN' | grep -Ei 'clip|trim' | cut -f2-3
echo "##### (c) Picard CollectHsMetrics fields on human BAM (synthetic bait/target = chr22:1900-4700)"
cp $D/human/genome.fasta* $D/human/genome.dict work/ 2>/dev/null
( grep '^@' work/genome.dict; printf "chr22\t1900\t4700\t+\tt1\n" ) > work/targets.interval_list
picard CollectHsMetrics I=work/test.paired_end.sorted.bam O=work/hs.txt R=work/genome.fasta BAIT_INTERVALS=work/targets.interval_list TARGET_INTERVALS=work/targets.interval_list VALIDATION_STRINGENCY=SILENT > work/hs.log 2>&1
python - <<'PY'
lines = [l for l in open('work/hs.txt') if not l.startswith('#') and l.strip()]
h = lines[0].rstrip('\n').split('\t'); v = lines[1].rstrip('\n').split('\t')
d = dict(zip(h, v))
for k in ('PCT_OFF_BAIT', 'PCT_SELECTED_BASES', 'FOLD_80_BASE_PENALTY', 'AT_DROPOUT', 'GC_DROPOUT', 'MEAN_TARGET_COVERAGE', 'TOTAL_READS'):
    print(f'  {k:24s} present={k in d}  value={d.get(k)}')
PY
echo "##### (d) @SQ M5 vs samtools dict"
samtools view -H work/test.paired_end.sorted.bam | grep '^@SQ'
samtools dict work/genome.fasta | grep '^@SQ' | cut -f1-4
echo "##### (e) MultiQC ingests samtools stats/flagstat/idxstats"
mkdir -p work/mq && cp work/test.paired_end.sorted.bam.stats work/mq/ 2>/dev/null; samtools stats work/test.paired_end.sorted.bam > work/mq/human.stats; samtools flagstat work/test.paired_end.sorted.bam > work/mq/human.flagstat; samtools idxstats work/test.paired_end.sorted.bam > work/mq/human.idxstats
multiqc -f -q -o work/mq/out work/mq 2>&1 | tail -3; ls work/mq/out; grep -o 'samtools' work/mq/out/multiqc_data/multiqc_sources.txt | sort | uniq -c
echo "##### (f) verifybamid2 as Skill lists it (10k SVD panel, 100kb slice)"
verifybamid2 --SVDPrefix $D/resources/1000g.phase3.10k.b38.vcf.gz.dat --Reference work/genome.fasta --BamFile work/test.paired_end.sorted.bam --Output work/vb2 2>&1 | tail -4
} > out/t6_scope.txt 2>&1
cat out/t6_scope.txt
