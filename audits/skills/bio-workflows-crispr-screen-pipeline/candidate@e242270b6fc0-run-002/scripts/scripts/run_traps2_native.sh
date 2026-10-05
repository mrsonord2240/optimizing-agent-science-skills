export PATH=/f/OpenScience/audit-envs/crispr-screen-analyst/Scripts:$PATH
D=/f/OpenScience/audit-envs/crispr-screen-analyst/public-data/derived/crispr-pipeline
cd "$(dirname "$0")/../work/traps"
tr '\t' ',' < $D/mle/leukemia.count.txt > leukemia.count.csv
mageck mle --count-table leukemia.count.csv --design-matrix $D/mle/designmat.txt --output-prefix T7 --norm-method median --permutation-round 10 > t7.log 2>&1; echo "T7 mle-csv exit $?"; tail -3 t7.log | cut -c1-250
