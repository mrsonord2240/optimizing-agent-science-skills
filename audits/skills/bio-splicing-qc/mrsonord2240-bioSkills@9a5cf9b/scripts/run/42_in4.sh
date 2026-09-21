source /mnt/openscience/audit-envs/alternative-splicing/wsl_env.sh
R=/mnt/openscience/audits/bio-splicing-qc/run; D=$R/data
asenv as-core python $R/40_in4_make_edge.py $D
asenv as-core python $R/41_in4_junctions.py $R/skill/examples $D
echo "--- B07 literal (CLI) on se_overhang and edge BAMs"
mkdir -p $R/work/in4; cd $R/work/in4; cp -r $R/skill/examples .
for b in synthetic/se_overhang edge; do cp $D/$b.bam sample.bam; echo "== $b"; asenv as-core bash $R/blocks/B07.sh; done
