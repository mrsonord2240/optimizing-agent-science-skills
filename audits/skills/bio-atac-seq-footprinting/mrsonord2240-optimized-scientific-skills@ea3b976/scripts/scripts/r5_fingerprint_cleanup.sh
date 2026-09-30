#!/bin/bash
# fingerprints of the fresh ra-* envs, version facts, then removal (under lock); live env fingerprint recheck
export MAMBA_ROOT_PREFIX=/home/sci/micromamba PATH=/home/sci/.local/bin:$PATH
L=/mnt/openscience/audits/bio-atac-seq-footprinting/reaudit-run/logs
for n in ra-footprint ra-footprint-rgt ra-footprint-pydnase ra-footprint-scprinter bio-atac-seq-footprinting bio-atac-seq-footprinting-rgt bio-atac-seq-footprinting-pydnase bio-atac-seq-footprinting-scprinter; do
  { micromamba list -n $n --explicit --md5; micromamba run -n $n pip freeze; } > $L/env_$n.txt 2>&1
  echo "$n $(sha256sum < $L/env_$n.txt | cut -c1-16)"
done | tee $L/r5_fingerprints.txt
micromamba run -n ra-footprint TOBIAS --version; micromamba run -n ra-footprint samtools --version | head -1
micromamba run -n ra-footprint-rgt rgt-hint --version 2>&1 | head -1; micromamba run -n ra-footprint-pydnase python -c "import pyDNase;print('pyDNase',pyDNase.__version__)"
micromamba run -n ra-footprint-scprinter python -c "import torch,scprinter,tangermeme,snapatac2;print('scprinter',scprinter.__version__,'torch',torch.__version__,torch.cuda.is_available(),'tangermeme',tangermeme.__version__,'snapatac2',snapatac2.__version__)" 2>&1 | tail -1
micromamba run -n ra-footprint-scprinter pip check | tail -3
exec 9>/mnt/openscience/runtime/locks/micromamba-mutate.lock; flock 9
for n in ra-footprint ra-footprint-rgt ra-footprint-pydnase ra-footprint-scprinter; do micromamba env remove -y -n $n > /dev/null 2>&1; echo "removed $n rc=$?"; done
micromamba env list | grep -E "ra-footprint" || echo "no ra-* envs remain"
