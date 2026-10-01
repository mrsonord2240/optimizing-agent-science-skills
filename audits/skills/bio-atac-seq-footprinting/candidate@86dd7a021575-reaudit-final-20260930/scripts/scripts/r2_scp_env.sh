#!/bin/bash
# Build the usage-guide scPrinter recipe in a fresh env. The three lines are EXTRACTED from the candidate's usage-guide.md
# (not retyped), run under the shared micromamba lock with a new empty pip cache. Env removed later by r9_cleanup.sh.
export MAMBA_ROOT_PREFIX=/home/sci/micromamba PATH=/home/sci/.local/bin:$PATH PYTHONDONTWRITEBYTECODE=1
Q=bio-atac-seq-footprinting; SKILL=/mnt/openscience/wt/atac-footprinting/skills/$Q
L=/mnt/openscience/audits/$Q/reaudit-final-20260930/logs
W=/mnt/openscience/audit-envs/$Q/reaudit-final; mkdir -p $W
export PIP_CACHE_DIR=$W/pipcache; rm -rf $PIP_CACHE_DIR; mkdir -p $PIP_CACHE_DIR
LK=/mnt/openscience/runtime/locks/micromamba-mutate.lock
micromamba env list | grep -q '^ *footprint-scprinter ' && { echo "footprint-scprinter already exists; refusing"; exit 1; }
awk "/^## Environments/{s=1} /^### RGT/{s=0} s" $SKILL/references/usage-guide.md | grep -E "^micromamba (create -n|run -n) footprint-scprinter" | sed "s/ *#.*$//" > $W/scp_recipe.sh
echo "recipe lines:"; cat -A $W/scp_recipe.sh | cut -c1-200
[ "$(wc -l < $W/scp_recipe.sh)" = 3 ] || { echo "expected 3 recipe lines"; exit 1; }
echo "start $(date -Is)"
i=0; while IFS= read -r line; do i=$((i+1))
  line=${line/micromamba create /micromamba create -y }
  flock $LK bash -c "$line" > $L/r2_env_step$i.log 2>&1; echo "step $i rc=$? $(date -Is)"; tail -2 $L/r2_env_step$i.log | cut -c1-200
done < $W/scp_recipe.sh
micromamba run -n footprint-scprinter python -c "import torch, scprinter, tangermeme, snapatac2; print('torch', torch.__version__, 'cuda', torch.cuda.is_available(), 'scprinter', scprinter.__version__, 'tangermeme', tangermeme.__version__, 'snapatac2', snapatac2.__version__)" 2>&1 | tail -1
micromamba run -n footprint-scprinter pip check 2>&1 | tail -3
micromamba run -n footprint-scprinter python -c "import sys; print(sys.executable)"
echo "end $(date -Is)"
