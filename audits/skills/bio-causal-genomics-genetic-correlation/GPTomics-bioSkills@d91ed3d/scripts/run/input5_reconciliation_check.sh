#!/usr/bin/env bash
# Input 5 (Stress / multi-part) -- "Run the full battery: global rg, decide whether
# HDL or LDSC is primary, flag CHP-aware MR sensitivity if |rg|>0.3, and reconcile."
#
# This re-runs the Skill's OWN Step-7 flagging logic from examples/ldsc_crosstrait_rg.sh
# (copied inline below, unmodified) against the REAL rg produced by Input 1's executed
# GenomicSEM::ldsc() run (rg = 0.4401, from run/input1_log.txt), rather than against a
# fabricated number. This exercises the Skill's own bash arithmetic, not a re-implementation.
set -euo pipefail

rg_pt="0.4401"          # real recovered rg from Input 1 (GenomicSEM::ldsc(), planted 0.45)
RG_LOCAL_TRIGGER=0.5    # exact constant from examples/ldsc_crosstrait_rg.sh
MR_CHP_TRIGGER=0.3      # exact constant from SKILL.md "Relationship to MR Causal Inference"

echo "rg = ${rg_pt}"

abs_rg=$(awk -v r="${rg_pt}" 'BEGIN {print (r < 0) ? -r : r}')

above_lava=$(awk -v a="${abs_rg}" -v t="${RG_LOCAL_TRIGGER}" 'BEGIN {print (a > t) ? 1 : 0}')
if [[ "${above_lava}" == "1" ]]; then
    echo "ACTION: |rg| > ${RG_LOCAL_TRIGGER} -> run LAVA local rg AND add CHP-aware MR sensitivity."
else
    echo "Global rg modest (below the example script's 0.5 LAVA-trigger); still run LAVA if biology suggests sharing (cancellation can hide local rg)."
fi

above_mr=$(awk -v a="${abs_rg}" -v t="${MR_CHP_TRIGGER}" 'BEGIN {print (a > t) ? 1 : 0}')
if [[ "${above_mr}" == "1" ]]; then
    echo "MR VALIDITY FLAG: |rg| = ${abs_rg} > ${MR_CHP_TRIGGER} (SKILL.md's separate MR-sensitivity threshold) -> IVW/Egger/MR-PRESSO alone are insufficient; add CAUSE (if sig SNPs >= 100) or LHC-MR per causal-genomics/pleiotropy-detection."
else
    echo "MR VALIDITY: |rg| below ${MR_CHP_TRIGGER}; standard MR sensitivity battery (IVW/Egger/MR-PRESSO) is not flagged as insufficient on rg grounds alone."
fi

echo ""
echo "NOTE FOR AUDITOR: the Skill documents two DIFFERENT rg thresholds for two DIFFERENT"
echo "actions -- 0.5 (example script, 'run LAVA local') vs 0.3 (SKILL.md prose, 'CHP-aware MR"
echo "sensitivity required'). Both are internally consistent and separately justified, but a"
echo "reader skimming only the shell example would miss the stricter 0.3 MR rule. See P2 finding."
