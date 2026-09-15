#!/bin/bash
export PATH=/tmp/vaca/env/bin:$PATH
bgzip -c ../../data/callerB.vcf > callerB.vcf.gz; bcftools index -f callerB.vcf.gz
bash run_py.sh
