#!/bin/bash
# SKILL 'Production: ignore expected-but-noisy' Picard command, verbatim (java -jar picard.jar -> picard)
RUN=/mnt/openscience/audits/bio-alignment-validation/run
D=$RUN/data; REF=/mnt/openscience/audit-envs/alignment-files/public-data/human/genome.fasta
for f in flag_mate_neg_strand unmapped_mapq60 strand_all_forward ctl_valid; do
  echo "--- $f (planted: $(python -c "import json;print(json.load(open('$D/fixtures.json'))['$f.bam']['defect'][:70])" 2>/dev/null))"
  echo -n "   plain:  "; picard ValidateSamFile I=$D/$f.bam MODE=SUMMARY R=$REF 2>&1 | grep -E '^(ERROR|WARNING):[A-Z_]+|No errors' | tr '\n' ' '; echo
  echo -n "   IGNORE: "; picard ValidateSamFile I=$D/$f.bam MODE=SUMMARY R=$REF IGNORE=INVALID_MAPPING_QUALITY IGNORE=MISMATCH_FLAG_MATE_NEG_STRAND 2>&1 | grep -E '^(ERROR|WARNING):[A-Z_]+|No errors' | tr '\n' ' '; echo
done
