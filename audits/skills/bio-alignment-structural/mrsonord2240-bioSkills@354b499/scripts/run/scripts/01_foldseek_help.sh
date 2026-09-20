# check Foldseek / Foldmason flags used by the Skill
cd /mnt/openscience/audits/bio-alignment-structural/run/work
for c in easy-search easy-cluster easy-multimersearch easy-multimercluster createdb; do
  foldseek $c -h </dev/null > ../logs/help_foldseek_$c.txt 2>&1; echo "$c: $(wc -l < ../logs/help_foldseek_$c.txt) lines"
done
foldmason easy-msa -h </dev/null > ../logs/help_foldmason_easy-msa.txt 2>&1
foldseek databases </dev/null > ../logs/help_foldseek_databases.txt 2>&1
