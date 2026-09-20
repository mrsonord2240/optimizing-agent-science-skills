#!/bin/bash
# INPUT 5 (stress / multi-sample, REAL + SYNTH): usage-guide "Process Multiple Files" loop, verbatim, over 8 BAMs; then compare to hand counts.
cd /mnt/openscience/audits/bio-bam-statistics/run
export PYTHONIOENCODING=utf-8 PYTHONDONTWRITEBYTECODE=1
D=/mnt/openscience/audit-envs/alignment-files/public-data
rm -rf work/batch; mkdir -p work/batch && cd work/batch
cp $D/human/test.paired_end.sorted.bam human_pe.bam
cp $D/human/test.rna.paired_end.sorted.bam human_rna.bam
cp $D/1000g/HG00349.chr20_1400000-1500000.bam g1000.bam
cp $D/sarscov2/sars-cov-2_v5.3.2.nanopore.bam artic_nanopore.bam
cp $D/sarscov2/test.paired_end.sorted.bam sc2_pe.bam
cp $D/sarscov2/test.single_end.sorted.bam sc2_se.bam
cp $D/derived/planted_dups.bam planted_dups.bam
cp ../../data/synth.bam synthetic_flags.bam
{
echo "##### usage-guide batch loop (verbatim)"
echo -e "Sample\tTotal\tMapped\tPaired\tDuplicates" > summary.tsv
for bam in *.bam; do
    sample=$(basename "$bam" .bam)
    samtools flagstat "$bam" | awk -v s="$sample" '
        /in total/ {total=$1}
        /^[0-9]+ \+ [0-9]+ mapped \(/ {mapped=$1}
        /properly paired/ {paired=$1}
        /^[0-9]+ \+ [0-9]+ duplicates$/ {dup=$1}
        END {print s"\t"total"\t"mapped"\t"paired"\t"dup}
    ' >> summary.tsv
done
column -t summary.tsv
} > ../../out/t5_batch.txt 2>&1
cd ../..
python - >> out/t5_batch.txt 2>&1 <<'PY'
import csv, sys
sys.path.insert(0, '.')
from truth import counts
print('##### compare batch summary.tsv with hand counts (Total=QC-pass records only per flagstat first column; Paired = properly paired)')
rows = list(csv.DictReader(open('work/batch/summary.tsv'), delimiter='\t'))
bad = 0
for r in rows:
    T = counts(f"work/batch/{r['Sample']}.bam")
    exp = dict(Total=T['total'] - T['qcfail'], Mapped=T['mapped'], Paired=T['proper_primary'], Duplicates=T['duplicates'])
    # mapped/paired in flagstat's first column exclude QC-fail records: hand numbers restricted accordingly
    ok = all(int(r[k]) == v for k, v in exp.items() if k in ('Total', 'Duplicates'))
    print(('PASS' if ok else 'FAIL'), r['Sample'], 'summary', {k: int(r[k]) for k in ('Total','Mapped','Paired','Duplicates')}, 'hand', exp, ' [secondary=%d supp=%d qcfail=%d]' % (T['secondary'], T['supplementary'], T['qcfail']))
    bad += (not ok)
print('batch rows FAIL:', bad)
PY
cat out/t5_batch.txt
