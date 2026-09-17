#!/usr/bin/env bash
# Runs the Skill's OWN unmodified example script (examples/multi_evidence_integration.R)
# against a hand-built 8-row synthetic locus_candidates.tsv (data/locus_candidates.tsv)
# covering: a near-certain concordant locus (PCSK9, all 6 streams pass), an L2G-vs-PoPS
# discordant locus (by construction), a "high" 3-of-6 locus, an associational-only
# locus, and a second near-certain locus. All tier assignments were hand-calculated
# against the Skill's own documented thresholds table before running, then compared to
# the script's real output -- exact match (see eval_viewer).
set -euo pipefail
RSH="F:/OpenScience/audit-envs/mendelian-randomization-analyst/r.sh"
SCRIPT="F:/OpenScience/audits/bio-causal-genomics-effector-gene-prioritization/run/skill_copy/examples/multi_evidence_integration.R"

"$RSH" "$SCRIPT"
# Real stdout:
#   Effector-gene prioritization complete.
#   High-confidence candidates (concordance >= 3): 3
#   L2G + PoPS concordant loci: 4 of 5
# (matches hand calculation exactly: PCSK9=6/near_certain, GENE_STRONG=6/near_certain,
#  GENE_SUGGESTIVE=3/high are the three >=3 rows; locus2_discordant is the only locus
#  where the L2G-top and PoPS-top genes differ, i.e. 4 of 5 loci concordant)
