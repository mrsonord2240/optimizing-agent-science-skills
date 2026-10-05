export HOME=/home/sci
SK=/mnt/openscience/wt/recut-crispr-pipeline/skills/bio-workflows-crispr-screen-pipeline
cd /mnt/openscience/fix-evidence/recut-crispr-pipeline/audit-initial/run-002/work/traps
/home/sci/micromamba/envs/crispr-ccr/bin/Rscript $SK/scripts/cn_correction.R ../cn/screen_cleanr_corrected_counts.txt T6 > t6.log 2>&1; echo "T6 cn-on-noninteger exit $?"; tail -2 t6.log
