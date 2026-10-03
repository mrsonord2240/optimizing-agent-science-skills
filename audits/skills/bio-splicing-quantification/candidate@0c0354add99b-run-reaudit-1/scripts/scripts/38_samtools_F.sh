#!/bin/bash
# failure-modes ref: 'samtools view -h -F 0x100 -F 0x800' must drop BOTH secondary and supplementary.
O=/mnt/openscience/audits/bio-splicing-quantification/run-reaudit-1/out; cd $O
printf '@HD\tVN:1.6\n@SQ\tSN:c\tLN:1000\nprim\t0\tc\t10\t60\t10M\t*\t0\t0\tACGTACGTAC\tIIIIIIIIII\nsec\t256\tc\t20\t60\t10M\t*\t0\t0\tACGTACGTAC\tIIIIIIIIII\nsupp\t2048\tc\t30\t60\t10M\t*\t0\t0\tACGTACGTAC\tIIIIIIIIII\n' > flags.sam
micromamba run -n as-core samtools --version | head -1
echo "kept read names:"; micromamba run -n as-core samtools view -h -F 0x100 -F 0x800 flags.sam | grep -v '^@' | cut -f1,2
