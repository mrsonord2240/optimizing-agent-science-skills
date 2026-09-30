source /mnt/openscience/audit-envs/bio-atac-seq-deep-learning-atac/scripts/env.sh
D=/mnt/openscience/audits/bio-atac-seq-deep-learning-atac/initial-audit-20260930
py_torch $D/scripts/inspect_contribs_h5.py $D/runs/contribs/contrib.counts_scores.h5
