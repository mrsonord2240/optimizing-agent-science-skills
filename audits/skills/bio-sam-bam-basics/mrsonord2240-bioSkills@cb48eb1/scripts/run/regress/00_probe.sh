#!/bin/bash
# Probe: tool versions and the exact output of the commands the Skill quotes
cd /mnt/openscience/audits/bio-sam-bam-basics/run
D=$AFDATA/human
echo "== versions"; samtools --version | head -2; python -c "import pysam;print('pysam',pysam.__version__, pysam.__samtools_version__)"
echo "== samtools flags 147"; samtools flags 147
echo "== samtools flags 99"; samtools flags 99
echo "== samtools flags mnemonics"; samtools flags PAIRED,PROPER_PAIR,REVERSE,READ2
echo "== flags 2304 / 0x1000 / 4095"; samtools flags 2304; samtools flags 4096; samtools flags 4095
echo "== seq_cache_populate.pl present?"; which seq_cache_populate.pl; ls $(dirname $(which samtools))/../share/samtools* 2>/dev/null | head
echo "== view help -h/-H/-c/-b/-C/-T/-o/-M/-L/-@"; samtools view --help 2>&1 | grep -E "^\s+-(h|H|c|b|C|T|o|M|L|@|O|q|f|F|x|X|u|1)\b|--no-header|--header-only|--count" | head -40
echo "== samtools head?"; samtools head -h 2>&1 | head -3
echo "== header"; samtools view -H $D/test.paired_end.sorted.bam
echo "== first 3 reads"; samtools view $D/test.paired_end.sorted.bam | head -3 | cut -f1-9,12-
