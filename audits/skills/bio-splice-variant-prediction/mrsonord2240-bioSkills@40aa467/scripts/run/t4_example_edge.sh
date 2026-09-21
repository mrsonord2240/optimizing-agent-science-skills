#!/bin/bash
# Input 4: the shipped example on the edge VCFs (multi-allelic/mismatch/long deletion mixed; then one symbolic <DEL> mixed with good records)
export PYTHONDONTWRITEBYTECODE=1
cd /mnt/openscience/audits/bio-splice-variant-prediction/run
rm -rf ex_edge && mkdir ex_edge && cp skill/examples/*.py ex_edge/ && cp data/edge_grch37.vcf ex_edge/ && cd ex_edge
FA=/mnt/openscience/audit-envs/alternative-splicing/public-data/derived/X.fa
{ cat ../data/edge_grch37.vcf; printf 'X\t193062\tsymbolic_DEL\tG\t<DEL>\t.\t.\t.\n'; } > edge_with_del.vcf
f() { micromamba run -n as-spliceai python spliceai_clingen_classify.py "$@" 2>&1 | tr '\r' '\n' | grep -av "━\|tf.function\|cuda\|cpu_feature\|To enable\|absl\|^I0000\|^W0000\|pkg_resources\|^$"; }
echo "=== example on edge_grch37.vcf (no symbolic ALT)"; f edge_grch37.vcf $FA --build grch37 --out-prefix e1 | cut -c1-200; echo "rc=$?"; cut -f1-2,3-4,9-12 e1_classified.tsv 2>/dev/null | cut -c1-220
echo "=== example on the same + one <DEL> record"; f edge_with_del.vcf $FA --build grch37 --out-prefix e2 | tail -6 | cut -c1-200
