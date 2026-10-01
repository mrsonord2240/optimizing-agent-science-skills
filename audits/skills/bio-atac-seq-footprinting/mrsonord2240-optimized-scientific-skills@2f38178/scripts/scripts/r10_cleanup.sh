#!/bin/bash
# Fingerprint and remove the fresh recipe env (under the shared lock), drop the pip cache, recheck the live envs.
export MAMBA_ROOT_PREFIX=/home/sci/micromamba PATH=/home/sci/.local/bin:$PATH PYTHONDONTWRITEBYTECODE=1
L=/mnt/openscience/audits/bio-atac-seq-footprinting/reaudit-final-20260930/logs
{ micromamba list -n footprint-scprinter --explicit --md5; micromamba run -n footprint-scprinter pip freeze; } > $L/env_fresh_footprint-scprinter.txt 2>&1
echo "footprint-scprinter (fresh) $(sha256sum < $L/env_fresh_footprint-scprinter.txt | cut -c1-16)"
exec 9>/mnt/openscience/runtime/locks/micromamba-mutate.lock; flock 9
micromamba env remove -y -n footprint-scprinter > /dev/null 2>&1; echo "removed footprint-scprinter rc=$?"
micromamba env list | grep -E "^ *footprint-scprinter " || echo "no footprint-scprinter env remains"
rm -rf /mnt/openscience/audit-envs/bio-atac-seq-footprinting/reaudit-final/pipcache
for n in bio-atac-seq-footprinting bio-atac-seq-footprinting-rgt bio-atac-seq-footprinting-pydnase bio-atac-seq-footprinting-scprinter; do
  echo "$n $( { micromamba list -n $n --explicit --md5; micromamba run -n $n pip freeze; } 2>&1 | sha256sum | cut -c1-16)"
done
du -sh /mnt/openscience/audit-envs/bio-atac-seq-footprinting/reaudit-final
ps -eo pid,args | grep -E "seq2print|scprinter_footprint|run_tobias" | grep -v grep || echo "no run-owned processes"
