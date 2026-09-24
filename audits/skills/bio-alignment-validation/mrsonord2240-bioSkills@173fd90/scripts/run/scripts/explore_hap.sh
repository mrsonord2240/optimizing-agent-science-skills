#!/bin/bash
# what does Picard say about the haplotype map format?
picard ConvertHaplotypeDatabaseToVcf -h 2>&1 | grep -v '^\*' | grep -v -E 'setlocale|WARNING' | head -20 | cut -c1-200
echo ---
picard CrosscheckFingerprints -h 2>&1 | grep -i -B1 -A4 'HAPLOTYPE_MAP' | head -14 | cut -c1-200
