#!/usr/bin/env bash
# Fresh Phase-2 direct invocations of the shipped R scripts: Inputs 9 and 12.
set -euo pipefail
SK='F:/OpenScience/wt/proteomics-differential-abundance/proteomics/differential-abundance'
DD='F:/OpenScience/audits/bio-proteomics-differential-abundance/data'
OUT='F:/OpenScience/audits/bio-proteomics-differential-abundance/run/phase2_20260923'
RSH='F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/r.sh'
echo '=== INPUT 9 shipped MSstats and msqrob2 scripts ==='
set +e
"$RSH" "$SK/scripts/msstats_group_comparison.R" "$DD/evidence.txt" "$DD/proteinGroups_evidence_subset.txt" "$DD/annotation_msstats.csv" Control Treatment equalizeMedians "$OUT/msstats_equal" | tee "$OUT/input9_msstats_equal.log"; s_equal=${PIPESTATUS[0]}
"$RSH" "$SK/scripts/msstats_group_comparison.R" "$DD/evidence.txt" "$DD/proteinGroups_evidence_subset.txt" "$DD/annotation_msstats.csv" Control Treatment FALSE "$OUT/msstats_none" | tee "$OUT/input9_msstats_none.log"; s_none=${PIPESTATUS[0]}
"$RSH" "$SK/examples/msqrob2_peptide_level.R" "$DD/evidence.txt" "$DD/annotation_msstats.csv" | tee "$OUT/input9_msqrob2.log"; s_msqrob=${PIPESTATUS[0]}
set -e
echo "Input 9 R exit codes: equalizeMedians=$s_equal FALSE=$s_none msqrob2=$s_msqrob"
test -s "$OUT/msstats_equal_tested.csv" && test -s "$OUT/msstats_none_tested.csv"
echo '=== INPUT 12 new deterministic self-contained msqrob2 example ==='
set +e
"$RSH" "$SK/examples/msqrob2_peptide_level.R" > "$OUT/input12_first.log"; s_first=$?
"$RSH" "$SK/examples/msqrob2_peptide_level.R" > "$OUT/input12_second.log"; s_second=$?
set -e
echo "Input 12 R exit codes: first=$s_first second=$s_second"
diff -u "$OUT/input12_first.log" "$OUT/input12_second.log"
grep -q 'planted truth:' "$OUT/input12_first.log"
"F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/Scripts/python.exe" "$OUT/verify_phase2_outputs.py" "$OUT"
echo 'ALL_CLI_ASSERTIONS_PASS'
