source /mnt/openscience/audit-envs/bio-atac-seq-deep-learning-atac/scripts/env.sh
D=/mnt/openscience/audits/bio-atac-seq-deep-learning-atac/initial-audit-20260930/runs/contribs
cd $D
( time timeout 600 micromamba run -n dlatac-torch modisco motifs -i contrib.counts_scores.h5 -n 2000 -w 500 -o modisco_from_chrombpnet.h5 ) 2>&1 | tail -15
echo "exit=${PIPESTATUS[0]}"
