#!/usr/bin/env bash
# Fresh Phase-2 dynamic execution for bio-proteomics-ptm-analysis.
# Run from this directory with Git Bash. Each invoked skill script is copied here verbatim.
set -uo pipefail
ROOT='F:/OpenScience'
ENV="$ROOT/audit-envs/mass-spec-proteomics-analyst"
PY="$ENV/Scripts/python.exe"
RSH="$ENV/r.sh"
DATA="$ROOT/audits/bio-proteomics-ptm-analysis/data/phospho"
TMT="$ROOT/audits/bio-proteomics-ptm-analysis/pass5/tmt"
KSEA="$ROOT/audits/bio-proteomics-ptm-analysis/pass5/ksea"

"$PY" phospho_analysis.py > in1_example.out 2>&1
"$RSH" msstatsptm_labelfree.R "dir=$DATA" fasta=synthetic.fasta out=in2_labelfree > in2_labelfree.out 2>&1
"$PY" motif_enrichment.py --sites "$DATA/Phospho (STY)Sites.txt" --fasta "$DATA/synthetic.fasta" --out in3_motif.csv > in3_motif.out 2>&1
"$RSH" ksea_scores.R adjusted=in2_labelfree/adjusted_sites.csv "proteinGroups=$DATA/proteinGroups_global.txt" "prior=$KSEA/PSP&NetworKIN_Kinase_Substrate_Dataset.csv" out=in4_ksea.csv > in4_ksea.out 2>&1
if "$RSH" ksea_scores.R adjusted=in2_labelfree/adjusted_sites.csv "proteinGroups=$DATA/proteinGroups_global.txt" "prior=$DATA/kinase_substrate_SYNTHETIC.tsv" out=in5_guard.csv > in5_guard.out 2>&1; then
  echo 'expected KSEA coverage guard did not stop' >&2
  echo 'UNEXPECTED_SUCCESS' >> in5_guard.out
else
  echo 'EXPECTED_GUARD_STOP' >> in5_guard.out
fi
rm -rf in6_no_global
mkdir in6_no_global
cp "$DATA/evidence_phospho.txt" "$DATA/annotation_ptm.csv" "$DATA/synthetic.fasta" in6_no_global/
if "$RSH" msstatsptm_labelfree.R dir=in6_no_global fasta=synthetic.fasta use_unmod=TRUE out=in6_no_global_out > in6_no_global.out 2>&1; then
  echo 'UNEXPECTED_SUCCESS_NO_GLOBAL' >> in6_no_global.out
else
  echo 'EXPECTED_NO_GLOBAL_FAILURE' >> in6_no_global.out
fi
"$PY" build_guard_prior.py > in5_build_guard.out 2>&1
if "$RSH" ksea_scores.R adjusted=in2_labelfree/adjusted_sites.csv "proteinGroups=$DATA/proteinGroups_global.txt" prior=in5_one_row_prior.csv out=in5_guard.csv > in5_guard.out 2>&1; then
  echo 'expected valid-prior KSEA coverage guard did not stop' >&2
  echo 'UNEXPECTED_SUCCESS_VALID_PRIOR' >> in5_guard.out
else
  echo 'EXPECTED_VALID_PRIOR_GUARD_STOP' >> in5_guard.out
fi
"$RSH" msstatsptm_tmt.R "dir=$TMT" fasta=synthetic.fasta out=in7_tmt > in7_tmt.out 2>&1
"$PY" build_ptmsea_fixture.py > in7_build.out 2>&1
"$PY" ptmsea.py write-gct --sites ptmsea_sites.tsv --out in7_sites.gct > in7_write.out 2>&1
SSG="$ENV/tools/ssGSEA2.0"
DB="$SSG/db/ptmsigdb/v1.9.1/ptm.sig.db.all.flanking.human.v1.9.1.gmt"
mkdir -p in8_ptmsea
"$RSH" "$SSG/ssgsea-cli.R" -i in7_sites.gct -o in8_ptmsea/run -d "$DB" -z "$SSG" -n rank -w 0.75 -c z.score -t area.under.RES -s NES -p 1000 -m 10 -x TRUE -e FALSE -l FALSE > in8_ssgsea.out 2>&1
"$PY" ptmsea.py read --prefix in8_ptmsea/run --out in8_ptmsea_scores.csv > in8_read.out 2>&1
