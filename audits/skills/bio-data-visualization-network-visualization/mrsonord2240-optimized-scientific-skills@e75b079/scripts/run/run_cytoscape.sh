#!/bin/bash
# Start one private Cytoscape process group, run Input 6, and stop only that group.
set -euo pipefail
AUDIT=/mnt/openscience/audits/bio-data-visualization-network-visualization
CYTO=/mnt/openscience/audit-envs/data-visualization/tools/cytoscape/cytoscape-unix-3.10.4
export MAMBA_ROOT_PREFIX=/home/sci/micromamba
export HOME="$AUDIT/run/cytoscape-home"
export JAVA_HOME=/home/sci/micromamba/envs/dv-cli
export PATH="$JAVA_HOME/bin:$PATH"
mkdir -p "$HOME"
if curl --max-time 2 -sf localhost:1234/v1 >/dev/null 2>&1; then
  echo "REST port 1234 already belongs to another process; refusing to reuse or stop it" >&2
  exit 90
fi
cd "$CYTO"
setsid bash -c 'sleep 100000 | xvfb-run -a -s "-screen 0 1600x1000x24" ./cytoscape.sh' \
  >"$AUDIT/logs/cytoscape_server.log" 2>&1 &
cyto_group=$!
cleanup() {
  kill -TERM -- "-$cyto_group" 2>/dev/null || true
  for _ in $(seq 1 20); do
    if ! curl --max-time 2 -sf localhost:1234/v1 >/dev/null 2>&1; then
      echo "private Cytoscape stopped; REST port is down"
      return
    fi
    sleep 1
  done
  echo "REST port remained up after stopping private process group" >&2
  return 1
}
trap cleanup EXIT
for attempt in $(seq 1 60); do
  if curl --max-time 2 -s localhost:1234/v1 | grep -q apiVersion; then
    echo "Cytoscape REST up after $((attempt * 3))s; process group $cyto_group"
    break
  fi
  sleep 3
done
curl --max-time 2 -sf localhost:1234/v1 >/dev/null
micromamba run -n dv-cli python "$AUDIT/run/cytoscape_check.py" \
  2>&1 | tee "$AUDIT/logs/cytoscape_check.log"
