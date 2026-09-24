#!/bin/bash
export PATH=/tmp/vaca/env/bin:$PATH
echo "bcftools: $(bcftools --version | head -1)"
bash run.sh 2>&1 | grep -v "env.sh\|GATK\|cygpath"
