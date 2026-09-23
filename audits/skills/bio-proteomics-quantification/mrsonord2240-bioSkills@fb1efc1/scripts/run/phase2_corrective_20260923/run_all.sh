#!/usr/bin/env bash
# Fresh corrective Phase-2 matrix. Inputs 1,2,4,8,9 use the approved private R 4.4.3 stack.
set -euo pipefail
ENV=/mnt/openscience/audit-envs/mass-spec-proteomics-analyst/tools/quantification-r443-conda
RUN=/mnt/openscience/audits/bio-proteomics-quantification/run/phase2_corrective_20260923
DATA=/mnt/openscience/audits/bio-proteomics-quantification/data
SKILL=/mnt/openscience/wt/proteomics-quantification/proteomics/quantification/scripts
OLD=/mnt/openscience/audits/_final_pass/bio-proteomics-quantification/run/phase1_abi_repair
micromamba run -p "$ENV" Rscript "$SKILL/msstats_summarize.R" "$DATA/evidence.txt" "$DATA/proteinGroups.txt" "$DATA/annotation_msstats.csv" "$RUN/protein_abundance.csv" > "$RUN/input1_msstats.out" 2>&1
micromamba run -p "$ENV" Rscript "$SKILL/maxlfq_iq.R" "/mnt/openscience/audits/bio-proteomics-quantification/run/phase2_20260923/peptide_long.csv" "$RUN/protein_maxlfq.csv" > "$RUN/input2_maxlfq.out" 2>&1
micromamba run -p "$ENV" Rscript "$OLD/run_tmt_inputs.R" > "$RUN/inputs4_8_tmt.out" 2>&1
micromamba run -p "$ENV" Rscript "$OLD/run_diann_maxlfq.R" > "$RUN/input9_diann_maxlfq.out" 2>&1
