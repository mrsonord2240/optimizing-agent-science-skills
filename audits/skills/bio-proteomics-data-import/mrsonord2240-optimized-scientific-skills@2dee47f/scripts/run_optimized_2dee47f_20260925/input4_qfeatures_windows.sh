#!/usr/bin/env bash
set -uo pipefail

/f/OpenScience/audit-envs/mass-spec-proteomics-analyst/r.sh \
  /f/OpenScience/audits/bio-proteomics-data-import/reaudit-optimized-scientific-skills@2dee47f-20260925/run/source_examples/load_maxquant_qfeatures.R \
  /f/OpenScience/audits/bio-proteomics-data-import/reaudit-optimized-scientific-skills@2dee47f-20260925/data/proteinGroups.txt
