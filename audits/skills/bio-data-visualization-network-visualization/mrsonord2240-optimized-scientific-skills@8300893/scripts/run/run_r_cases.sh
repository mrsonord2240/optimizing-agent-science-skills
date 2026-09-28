#!/bin/bash
set -euo pipefail
AUDIT=/f/OpenScience/audits/bio-data-visualization-network-visualization
ENV=/f/OpenScience/audit-envs/data-visualization
mkdir -p "$AUDIT/out/input4_r_layouts"
set +e
"$ENV/r.sh" "$AUDIT/run/skill/scripts/ggraph_layouts.R" \
  "$AUDIT/data/synth_ppi.graphml" "$AUDIT/out/input4_r_layouts" \
  2>&1 | tee "$AUDIT/logs/input4_ggraph.log"
layout_status=${PIPESTATUS[0]}
"$ENV/r.sh" "$AUDIT/run/skill/scripts/edge_bundling.R" \
  "$AUDIT/out/input4_edge_bundling.png" \
  2>&1 | tee "$AUDIT/logs/input4_bundling.log"
bundle_status=${PIPESTATUS[0]}
set -e
printf 'layout_status=%s\nbundle_status=%s\n' "$layout_status" "$bundle_status" | tee "$AUDIT/logs/input4_status.log"
test -s "$AUDIT/out/input4_r_layouts/fr.png"
test -s "$AUDIT/out/input4_r_layouts/kk.png"
test -s "$AUDIT/out/input4_r_layouts/circle.png"
test -s "$AUDIT/out/input4_edge_bundling.png"
