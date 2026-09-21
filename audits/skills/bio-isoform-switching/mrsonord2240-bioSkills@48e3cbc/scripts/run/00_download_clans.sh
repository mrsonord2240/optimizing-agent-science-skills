#!/bin/bash
# Pfam-A.clans.tsv.gz, the file the Skill's own bash block downloads (public, unauthenticated); used by 40b_external.sh
mkdir -p F:/OpenScience/audits/bio-isoform-switching/run/work/annot_dl
curl -sS -L --max-time 200 -o F:/OpenScience/audits/bio-isoform-switching/run/work/annot_dl/Pfam-A.clans.tsv.gz https://ftp.ebi.ac.uk/pub/databases/Pfam/current_release/Pfam-A.clans.tsv.gz
ls -la F:/OpenScience/audits/bio-isoform-switching/run/work/annot_dl/
