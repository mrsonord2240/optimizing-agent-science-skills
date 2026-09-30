# Re-audit: RESUME=1 rerun on the completed OUTDIR from ra_pipe_run1 (all training steps skipped; gate + variants rerun)
source /mnt/openscience/audit-envs/bio-atac-seq-deep-learning-atac/scripts/env.sh
export PATH=/home/sci/micromamba/envs/dlatac-tf/bin:$PATH
S=/mnt/openscience/wt/atac-deep-learning-atac/skills/bio-atac-seq-deep-learning-atac/scripts
P=$ME/public-cache/pseudo; R=$ME/run/reaudit; O=$R/pipe; mkdir -p $R/tmp; export TMPDIR=$R/tmp
sha256sum $S/*
CAP=${CAP:-900}
date -Is
RESUME=1 TEST_CHROMS=chrP1 VALID_CHROMS=chrP2 TRAIN_ARGS="-e 1 -es 1" ALLOW_FAILED_QC=1 VARIANTS=$ME/run/skillscript/variants_pseudo.tsv VARIANT_SCORER=$ME/src/variant-scorer \
  timeout $CAP bash $S/chrombpnet_pipeline.sh $P/pseudo.bam $P/pseudo.narrowPeak $P/pseudo.fa $P/pseudo.chrom.sizes $O ATAC 0.5 2>&1 | grep -v -E "it/s\]|^[0-9]+it \[|Warning|I0000|W0000|ETA:|step - loss|━|\[=" | tail -60
echo "exit=${PIPESTATUS[0]}"; date -Is
