#!/bin/bash
# INPUT 2b: Pangolin on GRCh38 using the Skill's exact DB recipe: gffutils.create_db('<gencode>.gff3', 'gencode.db', force=True) (GENCODE v45 GFF3 subset to the TP53 locus, chr17:7.6-7.75 Mb, to keep it fast).
export PYTHONDONTWRITEBYTECODE=1 PYTHONUTF8=1
AS=/mnt/openscience/audit-envs/alternative-splicing
FA=$AS/public-data/longread/flair_test/genome.fa
cd /mnt/openscience/audits/bio-splice-variant-prediction/run/data
zcat gencode.v45.annotation.gff3.gz | awk -F'\t' '/^#/ || ($1=="chr17" && $4>=7600000 && $5<=7750000)' > gencode.v45.tp53locus.gff3
echo "subset lines: $(grep -vc '^#' gencode.v45.tp53locus.gff3)"; grep -v '^#' gencode.v45.tp53locus.gff3 | awk -F'\t' '$3=="gene"' | head -2 | cut -c1-300
time /home/sci/micromamba/envs/as-pangolin/bin/python -c "import gffutils; gffutils.create_db('gencode.v45.tp53locus.gff3', 'gencode_skill.db', force=True); print('db ok')" 2>&1 | grep -av pkg_res | tail -3
cd ..
/home/sci/micromamba/envs/as-pangolin/bin/pangolin data/tp53_grch38.vcf $FA data/gencode_skill.db out/pang_tp53 -d 500 -m True -s 0.2 2>&1 | grep -av pkg_res | tail -8 | cut -c1-300
grep -v '^##' out/pang_tp53.vcf | cut -f2-5,8 | cut -c1-300
/home/sci/micromamba/envs/as-pangolin/bin/pangolin data/tp53_grch38.vcf $FA data/gencode_skill.db out/pang_tp53_d50 -d 50 -m True 2>&1 | grep -av pkg_res | tail -5 | cut -c1-300
grep -v '^##' out/pang_tp53_d50.vcf | cut -f2-5,8 | cut -c1-300
