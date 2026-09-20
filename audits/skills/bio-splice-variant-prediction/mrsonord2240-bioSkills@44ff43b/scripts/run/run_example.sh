#!/bin/bash
# INPUT 5b: run the SHIPPED example script unmodified from a copy, on hg38 TP53 records (script hardcodes clinical_variants.vcf, GRCh38.primary_assembly.genome.fa, build='grch38').
export PYTHONDONTWRITEBYTECODE=1
AS=/mnt/openscience/audit-envs/alternative-splicing
PY=/home/sci/micromamba/envs/as-spliceai/bin
cd /mnt/openscience/audits/bio-splice-variant-prediction/run/ex_run
cp ../skill/examples/spliceai_clingen_classify.py .
$PY/python - <<'P'
import pyfaidx
fa = pyfaidx.Fasta('/mnt/openscience/audit-envs/alternative-splicing/public-data/longread/flair_test/genome.fa')
with open('GRCh38.primary_assembly.genome.fa', 'w', newline='\n') as f:
    f.write('>chr17\n'); s = fa['chr17'][:].seq
    for i in range(0, len(s), 60): f.write(s[i:i+60] + '\n')
print('wrote chr17-only hg38 FASTA', len(s))
P
grep -v 'usage_guide_as_written' ../data/tp53_grch38.vcf > clinical_variants.vcf; grep -vc '^#' clinical_variants.vcf
export PATH=$PY:$PATH
$PY/python spliceai_clingen_classify.py > example_stdout.txt 2> example_stderr.txt; echo "example rc=$?"
grep -a -v "absl\|step\|retrac\|pkg_res" example_stderr.txt | tail -8 | cut -c1-200
echo "--- stdout"; cat example_stdout.txt; echo "--- output tsv"; cat spliceai_clingen_classified.tsv; ls
