#!/usr/bin/env bash
# Phase 2 Input 6: execute the exact Startle invocation documented in SKILL.md.
set -euo pipefail
startle large phase2_startle_character_matrix.csv phase2_startle_priors.csv phase2_seed_tree.newick --output phase2_refined --iterations 20
test -s phase2_refined_tree.newick
test -s phase2_refined_info.json
echo "input6 PASS Startle output files created"
