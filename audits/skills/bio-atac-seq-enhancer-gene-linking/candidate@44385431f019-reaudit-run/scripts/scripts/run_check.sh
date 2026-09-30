source /mnt/openscience/audit-envs/bio-atac-seq-enhancer-gene-linking/env.sh
cd /mnt/openscience/audits/bio-atac-seq-enhancer-gene-linking/reaudit-run
python scripts/check_case.py "$@"
