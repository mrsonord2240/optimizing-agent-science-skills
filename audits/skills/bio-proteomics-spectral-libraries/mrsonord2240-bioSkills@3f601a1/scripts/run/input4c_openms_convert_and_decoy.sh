#!/bin/bash
# Input 4: OpenMS CLI conversion + decoy generation, and the determinism check
# (run twice on identical input and diff the results).
TOOLS="F:\OpenScience\audit-envs\mass-spec-proteomics-analyst\tools\openms\bin"
DATA="F:\OpenScience\audits\bio-proteomics-spectral-libraries\data"

"$TOOLS/TargetedFileConverter.exe" -in "$DATA/input4_library.tsv" -in_type tsv \
    -out "$DATA/input4_library.TraML" -out_type TraML

"$TOOLS/OpenSwathDecoyGenerator.exe" -in "$DATA/input4_library.TraML" \
    -out "$DATA/input4_library_decoy_final.TraML" -method shuffle

# Determinism check: run again on the identical input and diff.
"$TOOLS/OpenSwathDecoyGenerator.exe" -in "$DATA/input4_library.TraML" \
    -out "$DATA/decoy_run_a.TraML" -method shuffle
"$TOOLS/OpenSwathDecoyGenerator.exe" -in "$DATA/input4_library.TraML" \
    -out "$DATA/decoy_run_b.TraML" -method shuffle
diff "$DATA/decoy_run_a.TraML" "$DATA/decoy_run_b.TraML" > "$DATA/decoy_diff.txt"
wc -l "$DATA/decoy_diff.txt"
