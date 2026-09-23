#!/bin/bash
# Phase 2 structural precheck using the mandated skill-auditor helper on the exact worktree path.
set -euo pipefail
/f/OpenScience/audit-envs/untargeted-metabolomics-analyst/Scripts/python.exe \
  /f/OpenScience/skills/skill-auditor/scripts/evaluate_skill.py \
  /f/OpenScience/wt/metabolomics-normalization-qc/metabolomics/normalization-qc --json-only
