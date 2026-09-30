# usage: run_generic.sh r|py <script in reaudit-10x/scripts>
source /mnt/openscience/audit-envs/bio-atac-seq-single-cell-atac/tools/env.sh
export CACHE=/mnt/openscience/audit-envs/bio-atac-seq-co-accessibility/public-cache
export MACS3=/home/sci/micromamba/envs/bio-atac-seq-single-cell-atac-py/bin/macs3
cd $SCA/work
if [ $1 = r ]; then time micromamba run -n bio-atac-seq-single-cell-atac-r Rscript /mnt/openscience/audits/bio-atac-seq-single-cell-atac/reaudit-10x/scripts/$2
else time micromamba run -n bio-atac-seq-single-cell-atac-py python /mnt/openscience/audits/bio-atac-seq-single-cell-atac/reaudit-10x/scripts/$2; fi
echo EXIT $?
