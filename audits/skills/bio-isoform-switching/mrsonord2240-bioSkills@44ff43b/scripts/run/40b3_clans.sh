#!/bin/bash
# accession -> clan map from the Pfam-A.hmm text (needed to build the pfam_scan-style table analyzePFAM() expects)
AS=/mnt/openscience/audit-envs/alternative-splicing
awk '/^ACC /{acc=$2} /^CL /{print acc"\t"$2}' $AS/public-data/reference_dbs/Pfam-A.hmm > /mnt/openscience/audits/bio-isoform-switching/run/work/annot/pfam_clans.tsv
wc -l /mnt/openscience/audits/bio-isoform-switching/run/work/annot/pfam_clans.tsv; grep -P "^PF00240|^PF11976|^PF14560" /mnt/openscience/audits/bio-isoform-switching/run/work/annot/pfam_clans.tsv
