S=/mnt/openscience/wt/atac-enhancer-gene-linking/skills/bio-atac-seq-enhancer-gene-linking/scripts/run_abc.sh
E=/mnt/openscience/audit-envs/bio-atac-seq-enhancer-gene-linking/src/abc-head
t(){ echo "--- $1"; shift; env "$@" bash $S 2>&1 | tail -2; echo "rc=${PIPESTATUS[0]}"; }
t "no ABC_REPO" ACCESS_BAM=a OUTDIR=/tmp/x
t "hic without file" ABC_REPO=$E ACCESS_BAM=a OUTDIR=/tmp/x HIC_TYPE=hic
t "file with HIC_TYPE none" ABC_REPO=$E ACCESS_BAM=a OUTDIR=/tmp/x HIC_FILE=f
t "bad ACCESS_TYPE" ABC_REPO=$E ACCESS_BAM=a OUTDIR=/tmp/x ACCESS_TYPE=ATACX
t "bad ABC_REPO" ABC_REPO=/nonexistent ACCESS_BAM=a OUTDIR=/tmp/x
t "bad HIC_TYPE" ABC_REPO=$E ACCESS_BAM=a OUTDIR=/tmp/x HIC_TYPE=cooler HIC_FILE=f
