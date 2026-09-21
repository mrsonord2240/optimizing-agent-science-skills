#!/bin/bash
# usage: i5_run.sh <python script>  -- start Cytoscape headless, run script in dv-cli, stop ONLY our own Cytoscape/Xvfb (Xvfb pids not present before start)
export MAMBA_ROOT_PREFIX=/home/sci/micromamba
BEFORE=$(pgrep Xvfb | tr '\n' ' ')
bash /mnt/openscience/audit-envs/data-visualization/tools/wsl_cytoscape.sh start || exit 1
micromamba run -n dv-cli python "$@" > /tmp/i5_out.txt 2>&1
cat /tmp/i5_out.txt
pkill -f 'java.*CytoscapeStartup|java.*cytoscape' 
for p in $(pgrep Xvfb); do case " $BEFORE " in *" $p "*) ;; *) kill $p;; esac; done
echo cleaned
