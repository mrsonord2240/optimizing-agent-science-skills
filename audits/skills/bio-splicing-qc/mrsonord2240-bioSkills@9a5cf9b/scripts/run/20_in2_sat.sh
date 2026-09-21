# Input 2: junction saturation. B04 literal (RSeQC + helper) on planted deep/mid/shallow libraries (synthetic; truth.json lambda_A) and real chrX.
# B04 is run inside as-core (its `python` must have pandas/pysam) via `asenv as-core bash B04.sh`.
source /mnt/openscience/audit-envs/alternative-splicing/wsl_env.sh
R=/mnt/openscience/audits/bio-splicing-qc/run; D=$R/data/synthetic
P=/mnt/openscience/audit-envs/alternative-splicing/public-data/rnasplice
mkdir -p $R/work/in2; cd $R/work/in2
runlib() { asenv as-core bash $R/blocks/B04.sh 2>&1 | grep -v '^sampling\|^reading\|^Load\|^shuffling' | cut -c1-700; }
for lib in se_sat_deep se_sat_mid se_sat_shallow; do
  mkdir -p $lib; cd $lib; cp $D/$lib.bam sample.bam; cp $D/$lib.bam.bai sample.bam.bai; cp $D/synth.bed12 genes.bed12; cp -r $R/skill/examples .
  echo "=========== $lib (run 1)"; runlib
  for k in 2 3; do echo "--- repeat $k"; asenv as-core python examples/splicing_qc.py saturation sample.bam genes.bed12 rep$k | python3 -c "import sys,ast; d=ast.literal_eval(sys.stdin.read().strip().splitlines()[-1]); print('growth', d['growth_80_100'], d['verdict'], 'known@100', d['known'][-1], 'known@80', d['known'][15])"; done
  cd ..
done
mkdir -p real; cd real; cp $P/bam/ERR188383.Aligned.out.bam sample.bam; cp $P/bam/ERR188383.Aligned.out.bam.bai .; cp $R/work/in1/real/genes.bed12 .; cp -r $R/skill/examples .
echo "=========== real chrX"; runlib
