#!/bin/bash
# Windows Git Bash (network + python 3). Spot-check of the SKILL contig-naming table's mitochondrion claims against independent public sequences:
#   "UCSC hg38 chrM (16,569 bp, same sequence as Ensembl MT)"   and   "UCSC hg19 chrM (16,571 bp, NC_001807 -- NOT the sequence of GRCh37 MT, 16,569 bp)".
# Also greps the 1000G README for the hs38DH / bwakit provenance claim.
cd "$(dirname "$0")/ncbi"
grep -n -i -E 'hs38DH|bwakit|decoy' README_1000G.txt | head -6
u(){ curl -sSL --max-time 90 -o "$1" "$2" && echo "$1 $(wc -c <"$1")"; }
u ucsc_hg38_chrM.json "https://api.genome.ucsc.edu/getData/sequence?genome=hg38;chrom=chrM"
u ucsc_hg19_chrM.json "https://api.genome.ucsc.edu/getData/sequence?genome=hg19;chrom=chrM"
u ens38_MT.txt "https://rest.ensembl.org/sequence/region/human/MT:1..16569:1?coord_system_version=GRCh38;content-type=text/plain"
u ens37_MT.txt "https://grch37.rest.ensembl.org/sequence/region/human/MT:1..16569:1?content-type=text/plain"
PYTHONIOENCODING=utf-8 python - <<'EOF'
import json
h38 = json.load(open('ucsc_hg38_chrM.json'))['dna'].upper(); h19 = json.load(open('ucsc_hg19_chrM.json'))['dna'].upper()
e38 = open('ens38_MT.txt').read().strip().upper(); e37 = open('ens37_MT.txt').read().strip().upper()
print('lengths hg38 chrM / hg19 chrM / Ensembl GRCh38 MT / Ensembl GRCh37 MT:', len(h38), len(h19), len(e38), len(e37))
print('CHECK hg38 chrM == Ensembl GRCh38 MT (same sequence):', h38 == e38)
print('CHECK hg19 chrM (16,571 bp) is a different sequence from GRCh37 MT:', h19 != e37 and len(h19) == 16571)
print('INFO GRCh37 MT == GRCh38 MT:', e37 == e38)
EOF
