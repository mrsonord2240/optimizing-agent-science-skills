# NEW input N2 (auditor-made scenario): "my novel-junction rate is high: annotation gap, mapping artifact, or biology?" on planted libraries.
# A = clean library scored against a gene model missing half the genes (annotation gap); B = novel-rich library (many low-count novel junctions) vs full model.
source /mnt/openscience/audit-envs/alternative-splicing/wsl_env.sh
R=/mnt/openscience/audits/bio-splicing-qc/run; D=$R/data/synthetic
mkdir -p $R/work/n2; cd $R/work/n2; cp -r $R/skill/examples .
head -30 $D/synth.bed12 > half.bed12; wc -l half.bed12
for sc in A B; do
  mkdir -p $sc; cd $sc; cp -r ../examples .
  if [ $sc = A ]; then cp $D/se_clean.bam sample.bam; cp $D/se_clean.bam.bai sample.bam.bai; cp ../half.bed12 genes.bed12; else cp $D/se_novelrich.bam sample.bam; cp $D/se_novelrich.bam.bai sample.bam.bai; cp $D/synth.bed12 genes.bed12; fi
  echo "=========== scenario $sc"
  asenv as-core bash $R/blocks/B05.sh > /dev/null 2>&1
  asenv as-core python $R/blocks/B06.py
  asenv as-core python - <<'PY'
import pandas as pd
j = pd.read_csv('sample_junc_annot.junction.xls', sep='\t'); j['annotation'] = j['annotation'].str.strip()
print(j.groupby('annotation')['read_count'].agg(['count', 'median', 'sum']).round(1).to_string())
PY
  asenv as-core python examples/splicing_qc.py junctions sample.bam --min-overhang 8
  cd ..
done
echo "=========== scenario A after the Skill's remedy (full annotation)"
mkdir -p A2; cd A2; cp ../A/sample.bam* .; cp $D/synth.bed12 genes.bed12; cp -r ../examples .
asenv as-core bash $R/blocks/B05.sh > /dev/null 2>&1; asenv as-core python $R/blocks/B06.py
