#!/bin/bash
# Re-audit: build the usage-guide env recipes verbatim (env names ra-*), each mutating step under the shared lock.
export MAMBA_ROOT_PREFIX=/home/sci/micromamba PATH=/home/sci/.local/bin:$PATH PYTHONDONTWRITEBYTECODE=1
export PIP_CACHE_DIR=/mnt/openscience/audit-envs/bio-atac-seq-footprinting/reaudit-run/pipcache
L=/mnt/openscience/audits/bio-atac-seq-footprinting/reaudit-run/logs
LK=/mnt/openscience/runtime/locks/micromamba-mutate.lock
mkdir -p $PIP_CACHE_DIR
lk() { flock $LK "$@"; }
lk micromamba create -y -n ra-footprint -c conda-forge -c bioconda python=3.10 pip pybigwig pysam samtools=1.19 bedtools numpy deeptools > $L/r1_footprint_create.log 2>&1; echo "footprint create rc=$?"
lk micromamba run -n ra-footprint pip install tobias > $L/r1_footprint_pip.log 2>&1; echo "footprint pip tobias rc=$?"
lk micromamba create -y -n ra-footprint-rgt -c conda-forge -c bioconda rgt > $L/r1_rgt_create.log 2>&1; echo "rgt create rc=$?"
lk micromamba create -y -n ra-footprint-pydnase -c conda-forge -c bioconda pydnase > $L/r1_pydnase_create.log 2>&1; echo "pydnase create rc=$?"
lk micromamba create -y -n ra-footprint-scprinter -c conda-forge -c bioconda python=3.11 pip git bedtools > $L/r1_scp_create.log 2>&1; echo "scp create rc=$?"
lk micromamba run -n ra-footprint-scprinter pip install torch --index-url https://download.pytorch.org/whl/cu128 > $L/r1_scp_torch.log 2>&1; echo "scp torch rc=$?"
lk micromamba run -n ra-footprint-scprinter pip install "git+https://github.com/buenrostrolab/scPrinter@v1.2.0" "tangermeme==0.4.4" "snapatac2==2.8.0" ema_pytorch > $L/r1_scp_pins.log 2>&1; echo "scp pins rc=$?"
echo "done $(date -Is)"
