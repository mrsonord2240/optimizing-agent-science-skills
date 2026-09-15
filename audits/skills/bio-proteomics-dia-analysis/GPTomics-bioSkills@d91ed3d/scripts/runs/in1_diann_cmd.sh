#!/bin/bash
# Input 1 - agent output following SKILL.md "DIA-NN -- Predicted-Library (directDIA) Route" (NOT executed: no DIA-NN here).
set -e
FASTA=uniprot_human_reviewed_2026_03.fasta
args=(); for f in C1 C2 C3 C4 T1 T2 T3 T4; do args+=(--f "${f}_DIA.mzML"); done
diann "${args[@]}" \
    --lib "" --fasta "$FASTA" --fasta-search \
    --gen-spec-lib --predictor \
    --out diann_out/report.parquet \
    --out-lib diann_out/report-lib.tsv \
    --qvalue 0.01 \
    --matrices \
    --mass-acc 0 \
    --reanalyse --smart-profiling \
    --cut K*,R* --missed-cleavages 1 \
    --min-pep-len 7 --max-pep-len 30 \
    --unimod4 --var-mods 1 --var-mod UniMod:35,15.994915,M \
    --threads 8
# then: python in1_skill_filter.py  (Skill filter block on diann_out/report.parquet)
