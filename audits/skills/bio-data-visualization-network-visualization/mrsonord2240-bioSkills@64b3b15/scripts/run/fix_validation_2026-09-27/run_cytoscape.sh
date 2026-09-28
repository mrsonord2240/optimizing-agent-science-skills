#!/bin/bash
# Start a private headless Cytoscape process group, run the repaired example, and stop only that group.
set -euo pipefail
export MAMBA_ROOT_PREFIX=/home/sci/micromamba
export HOME=/tmp/cyto_fix_home
export JAVA_HOME=/home/sci/micromamba/envs/dv-cli
export PATH="$JAVA_HOME/bin:$PATH"
mkdir -p "$HOME"
cd /mnt/openscience/audit-envs/data-visualization/tools/cytoscape/cytoscape-unix-3.10.4
setsid bash -c 'sleep 100000 | xvfb-run -a -s "-screen 0 1600x1000x24" ./cytoscape.sh' \
  >/tmp/cyto_fix.log 2>&1 &
cyto_group=$!
cleanup() {
  kill -- "-$cyto_group" 2>/dev/null || true
}
trap cleanup EXIT
for attempt in $(seq 1 60); do
  if curl -s localhost:1234/v1 | grep -q apiVersion; then
    echo "Cytoscape REST up after $((attempt * 3))s"
    break
  fi
  sleep 3
done
curl -sf localhost:1234/v1 >/dev/null
micromamba run -n dv-cli python \
  /mnt/openscience/wt/backlog-network-visualization/skills/bio-data-visualization-network-visualization/examples/cytoscape_automation.py \
  --output-dir /mnt/openscience/wt/backlog-network-visualization/validation/cytoscape-demo
micromamba run -n dv-cli python \
  /mnt/openscience/wt/backlog-network-visualization/skills/bio-data-visualization-network-visualization/examples/cytoscape_automation.py \
  --graphml /mnt/openscience/audits/bio-data-visualization-network-visualization/data/synth_ppi.graphml \
  --output-dir /mnt/openscience/wt/backlog-network-visualization/validation/cytoscape
