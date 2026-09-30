source /mnt/openscience/audit-envs/bio-atac-seq-motif-deviation/tools/env.sh
micromamba create -y -n bio-atac-seq-motif-deviation-dc2 -c conda-forge python=3.12 pip > $MD/logs/mkdc2.log 2>&1
micromamba run -n bio-atac-seq-motif-deviation-dc2 pip install 'decoupler==2.2.0' omnipath >> $MD/logs/mkdc2.log 2>&1
micromamba run -n bio-atac-seq-motif-deviation-dc2 python -c "
import decoupler as dc
print(dc.__version__)
print({n:hasattr(dc,n) for n in ['run_ulm','run_mlm','run_consensus','get_collectri']})
print({n:hasattr(dc.mt,n) for n in ['ulm','mlm','consensus']}, hasattr(dc.op,'collectri'))
"
