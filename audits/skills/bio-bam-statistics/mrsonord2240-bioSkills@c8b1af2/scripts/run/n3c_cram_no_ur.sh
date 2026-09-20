#!/bin/bash
# NEW: a CRAM whose @SQ UR: points at a FASTA that no longer exists (the usual "reference not with the file" case; htslib writes UR: automatically with -T,
# which is why n3b decoded own_ctg.cram without being given a reference). Reference cache bypassed.
export LC_ALL=C PYTHONIOENCODING=utf-8
R=/mnt/openscience/audits/bio-bam-statistics/run; N=$R/data/new; cd $R/work; rm -rf cb3; mkdir -p cb3/tmpref; cd cb3
export REF_PATH=$R/work/cb3/norefs REF_CACHE=$R/work/cb3/nocache; mkdir -p norefs
cp $N/own_ctg.fa $N/own_ctg.fa.fai tmpref/
samtools view -C -T tmpref/own_ctg.fa -o $R/data/new/own_ctg_nourl.cram $N/own_ctg.bam
samtools view -H $R/data/new/own_ctg_nourl.cram | grep '^@SQ' | head -1 | cut -c1-200
rm -rf tmpref
C=$N/own_ctg_nourl.cram; Q="python $R/skill/examples/qc_report.py"
echo "--- samtools flagstat (Skill: needs no reference)"; samtools flagstat -O tsv $C 2>&1 | sed -n '1,2p' | cut -f1-3
echo "--- qc_report.py WITHOUT reference (expect exit 1 + message with the hint)"; timeout 60 $Q $C 2>&1 | tail -1 | cut -c1-300; echo "rc=${PIPESTATUS[0]}"
echo "--- qc_report.py WITH reference (expect equal to flagstat)"; timeout 60 $Q $C $N/own_ctg.fa 2>&1 | sed -n '3,9p'; echo "rc=${PIPESTATUS[0]}"
echo "--- Count Reads snippet (block 027) without reference (Skill: OSError: truncated file)"; sed "s#'input.bam'#'$C'#" $R/blocks/027_python.py > c.py; timeout 60 python c.py 2>&1 | tail -1 | cut -c1-200
echo "--- Count Reads snippet with reference_filename"; sed "s#'input.bam', 'rb', check_sq=False#'$C', 'rb', check_sq=False, reference_filename='$N/own_ctg.fa'#" $R/blocks/027_python.py > c2.py; timeout 60 python c2.py 2>&1 | tail -3
echo "--- samtools stats on it: without --reference, then --reference (Skill: CRAM needs --reference)"
timeout 60 samtools stats $C 2>&1 | grep -c '^SN'; timeout 60 samtools stats $C 2>&1 | grep -E 'E::|W::' | head -2 | cut -c1-160
timeout 60 samtools stats --reference $N/own_ctg.fa $C | grep -E '^SN\s+raw total' | cut -f2-3
echo "--- samtools depth -aa on it without / with --reference"
timeout 60 samtools depth -aa $C 2>&1 | wc -l; timeout 60 samtools depth -aa --reference $N/own_ctg.fa $C | wc -l
