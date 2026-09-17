#!/bin/bash
# New input for this re-audit: run the shipped examples/wikipathways_explore.R BYTE-FOR-BYTE,
# unmodified, exactly as the pre-fix audit did (which is how it found the shipped file itself
# halting on the stale date). This is the regression test for BOTH defects the fixer reports:
# (1) the hardcoded stale date -> computed date, and (2) the previously-undiscovered undefined
# entrez_ids/all_entrez bug exposed once (1) was fixed.
set -e
cd "$(dirname "$0")/skill_copy/examples"
F:/OpenScience/audit-envs/crispr-screen-analyst/r.sh wikipathways_explore.R
