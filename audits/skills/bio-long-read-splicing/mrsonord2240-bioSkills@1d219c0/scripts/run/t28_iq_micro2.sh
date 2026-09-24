#!/bin/bash
# SKILL: "IsoQuant then counted 0 reads for the inclusion isoform" on plain alignments; rescued alignments (recipe) should give counts near truth (150 per isoform).
# IsoQuant 4.0.0 --genedb ref_full.gtf --bam <alignment> on my micro2 set: hifi plain vs --junc-bed; ONT unstranded plain vs --junc-bed --junc-bonus 16.
R=/mnt/openscience/audits/bio-long-read-splicing/run; D=$R/data/micro2; O=$R/out/iq_micro2; rm -rf $O; mkdir -p $O; cd $O; export PYTHONDONTWRITEBYTECODE=1
cp $D/chrM2.fa ref.fa
run() { # tag bam datatype
  isoquant --reference ref.fa --genedb $D/ref_full.gtf --bam $2 --data_type $3 --output iq_$1 --threads 4 --prefix q > iq_$1.log 2>&1; echo "IsoQuant $1 rc=$?"
  asenv as-lr python $R/iq_micro2_score.py iq_$1/q/q.transcript_counts.tsv $D/truth_chains.tsv "$1"
}
run hifi_plain $R/out/micro2_hifi/plain.bam pacbio_ccs
run hifi_juncbed $R/out/micro2_hifi/juncbed.bam pacbio_ccs
run ont_plain $R/out/micro2_ontunstr/plain.bam nanopore
run ont_bonus16 $R/out/micro2_ontunstr/bonus16.bam nanopore
run ont_juncbed_only $R/out/micro2_ontunstr/juncbed.bam nanopore
