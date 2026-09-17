#!/bin/sh
# New finding (this audit pass): SKILL.md's PRIDICT2 batch CLI example never
# mentions the CLI's --input-dir flag or its default value (./input). Following
# the documented recipe literally -- write the CSV to the current directory,
# then run the documented command -- crashes.
#
# Reproduction (run from a clean scratch directory containing ONLY the CSV
# SKILL.md tells you to create, exactly as its heredoc example shows):

set -e
SCRATCH=$(mktemp -d)
cd "$SCRATCH"
cat > variants.csv <<EOF
sequence_name,editseq
BRCA1_R71X,AGCAGCCT(C/T)CTGAATGCCC$(python -c "print('N'*100)")
EOF

# Exactly SKILL.md's documented command (Step 2 of "Run PRIDICT2 on a Custom
# pegRNA Library"), no --input-dir:
"$PRIDICT2_PY" batch --input-fname variants.csv --output-dir predictions/ --cores 1 --summarize K562
# Real result: FileNotFoundError: [Errno 2] No such file or directory:
#   '<scratch>/input/variants.csv'
# (argparse default: --input-dir ./input, joined with --input-fname via os.path.join;
#  SKILL.md's own heredoc writes variants.csv to the CURRENT directory, not ./input/)
#
# Workaround (undocumented in SKILL.md): mkdir input && mv variants.csv input/
# then the identical command succeeds and writes real predictions -- confirmed
# this pass (see predictions_round2/ in this folder, produced exactly this way).
