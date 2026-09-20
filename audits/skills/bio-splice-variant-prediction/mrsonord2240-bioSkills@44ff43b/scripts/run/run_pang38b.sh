#!/bin/bash
# INPUT 2b (cont.): what DO the working recipes give?  (a) Skill recipe + merge_strategy='create_unique'; (b) Pangolin README recipe (scripts/create_db.py on the GTF, default --filter Ensembl_canonical).
export PYTHONDONTWRITEBYTECODE=1 PYTHONUTF8=1
AS=/mnt/openscience/audit-envs/alternative-splicing
FA=$AS/public-data/longread/flair_test/genome.fa
PY=/home/sci/micromamba/envs/as-pangolin/bin
cd /mnt/openscience/audits/bio-splice-variant-prediction/run/data
$PY/python -c "
import gffutils
try:
    gffutils.create_db('gencode.v45.tp53locus.gff3', 'gencode_skill_uniq.db', force=True, merge_strategy='create_unique'); print('(a) create_unique db ok')
except Exception as e: print('(a) FAIL', repr(e)[:200])
" 2>&1 | grep -av pkg_res
zcat gencode.v45.annotation.gtf.gz | awk -F'\t' '/^#/ || ($1=="chr17" && $4>=7600000 && $5<=7750000)' > gencode.v45.tp53locus.gtf
echo "gtf subset lines: $(grep -vc '^#' gencode.v45.tp53locus.gtf)"
cp $AS/tools/src/Pangolin/scripts/create_db.py ./pangolin_create_db.py
$PY/python pangolin_create_db.py gencode.v45.tp53locus.gtf 2>&1 | grep -av pkg_res | tail -2
$PY/python pangolin_create_db.py gencode.v45.tp53locus.gtf --filter None 2>&1 | grep -av pkg_res | tail -1; mv gencode.v45.tp53locus.db gencode_all_tx.db
$PY/python pangolin_create_db.py gencode.v45.tp53locus.gtf 2>&1 | grep -av pkg_res | tail -1; mv gencode.v45.tp53locus.db gencode_canonical.db
cd ..
for db in gencode_skill_uniq gencode_all_tx gencode_canonical; do
  for m in True False; do
    $PY/pangolin data/tp53_grch38.vcf $FA data/$db.db out/pang_tp53_${db}_m$m -d 50 -m $m 2>&1 | grep -a "WARN\|Trace\|Error" | cut -c1-200
    echo "== db=$db mask=$m"; grep -v '^##' out/pang_tp53_${db}_m$m.vcf | cut -f3,8 | cut -c1-300
  done
done
