#!/bin/bash
# Public downloads used by run_pang38.sh / run_pang38b.sh (GENCODE v45 human, GRCh38). Deleted after use (110 MB); subsets stay in data/.
cd /mnt/openscience/audits/bio-splice-variant-prediction/run/data
curl -s -L -o gencode.v45.annotation.gff3.gz https://ftp.ebi.ac.uk/pub/databases/gencode/Gencode_human/release_45/gencode.v45.annotation.gff3.gz
curl -s -L -o gencode.v45.annotation.gtf.gz  https://ftp.ebi.ac.uk/pub/databases/gencode/Gencode_human/release_45/gencode.v45.annotation.gtf.gz
