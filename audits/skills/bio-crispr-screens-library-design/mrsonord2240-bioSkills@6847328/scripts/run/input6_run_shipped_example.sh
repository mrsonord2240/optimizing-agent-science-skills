#!/bin/bash
# Input 6 (Stress): run the Skill's own shipped examples/design_library.py unmodified,
# from the copied Skill folder (run/library-design-src/), not the external clone.
# Exact command used for this audit:
cd "$(dirname "$0")/library-design-src/examples"
"F:\OpenScience\audit-envs\crispr-screen-analyst\Scripts\python.exe" design_library.py
echo "EXIT CODE: $?"
# Output verified independently afterward with:
#   pandas.read_csv('library_design/library_design.csv') -> 142 rows, 0 NaN in `sequence`,
#   all genes at 4/gene quota (see run log copied to data/input6_design_library_output.csv)
