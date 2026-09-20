#!/bin/bash
# tool versions + help pages of the flags the fixed Skill documents
samtools --version | head -2; bcftools --version | head -1; python -c "import pysam;print('pysam',pysam.__version__)"
gatk --version 2>&1 | tail -1; picard CreateSequenceDictionary --version 2>&1 | tail -1
echo ====== samtools help consensus; samtools help consensus 2>&1
echo ====== samtools consensus --help rc; samtools consensus --help >/dev/null 2>&1; echo "rc=$?"
samtools help consensus >/dev/null 2>&1; echo "help rc=$?"
echo ====== seq_cache_populate; which seq_cache_populate.pl seq_cache_populate.py; ls /home/sci/micromamba/envs/alignment-files/bin | grep -i seq_cache
echo ====== samtools reheader --help; samtools reheader --help 2>&1 | head -20
echo ====== faidx help; samtools faidx --help 2>&1 | head -40
