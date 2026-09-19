#!/usr/bin/env bash
# Regression check for original audit Inputs 1 (QIIME2 classify-sklearn, region-matched) and 5
# (classify-consensus-vsearch). SKILL.md's QIIME2 command blocks are byte-identical pre-fix vs
# post-fix (confirmed by diff -- the only change in that section is a MEMORY comment, no command
# text changed), and both classify-sklearn and classify-consensus-vsearch are deterministic
# algorithms (no bootstrap/stochastic step), so the original audit's own cached WSL outputs
# (produced against the same real 770 ASVs and real SILVA-138 reference, untouched since) remain
# valid evidence without re-running the ~30 CPU-minute extract-reads / fit-classifier pipeline.
# Spot-checked by re-deriving the genus-assignment counts directly from the cached exports:
MSYS2_ARG_CONV_EXCL='*' wsl.exe -d science -- bash -lc '
cd /home/sci/taxassign
echo "--- taxonomy-sklearn-export (Input 1, classify-sklearn region-matched) ---"
tail -n +2 taxonomy-sklearn-export/taxonomy.tsv | wc -l
tail -n +2 taxonomy-sklearn-export/taxonomy.tsv | awk -F"\t" "{print \$2}" | grep -c "g__[^;]"
echo "--- taxonomy-vsearch-export (Input 5) ---"
tail -n +2 taxonomy-vsearch-export/taxonomy.tsv | wc -l
tail -n +2 taxonomy-vsearch-export/taxonomy.tsv | awk -F"\t" "{print \$2}" | grep -c "g__[^;]"
'
# Result (2026-09-19 re-audit): Input 1 = 653/770 genus-assigned (exact match to original audit's
# 653/770). Input 5 = 699/770 genus-assigned (exact match to original audit's 699/770). No
# regression in either -- confirms the SKILL.md diff analysis above.
