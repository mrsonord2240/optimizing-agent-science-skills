#!/bin/bash
# Public unauthenticated downloads the SKILL's SQANTI3 block points at (CAGE peaks + polyA motif list, Magdoll/images_public). Into out/dl (never public-data).
D=/f/OpenScience/audits/bio-long-read-splicing/run/out/dl; mkdir -p $D; cd $D
for u in SQANTI2_support_data/hg38.cage_peak_phase1and2combined_coord.bed.gz SQANTI2_support_data/human.polyA.list.txt; do
  curl -sSL -o $(basename $u) -w "%{http_code} %{size_download} $u\n" https://raw.githubusercontent.com/Magdoll/images_public/master/$u; done
