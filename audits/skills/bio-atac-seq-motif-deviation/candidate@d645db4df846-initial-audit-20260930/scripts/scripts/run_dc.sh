source /mnt/openscience/audit-envs/bio-atac-seq-motif-deviation/tools/env.sh
export HOME=$MD/work; cd $MD/work
micromamba run -n bio-atac-seq-motif-deviation-py python $MD/evidence/scripts/smoke_decoupler.py > $MD/logs/smoke_decoupler.log 2>&1; echo exit $?; tail -40 $MD/logs/smoke_decoupler.log
