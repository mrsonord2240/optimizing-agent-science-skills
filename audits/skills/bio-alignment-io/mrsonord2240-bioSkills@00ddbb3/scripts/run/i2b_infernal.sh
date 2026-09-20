#!/bin/bash
# INPUT 2b downstream: do Infernal cmbuild / HMMER hmmbuild accept the ORIGINAL Stockholm vs the AlignIO round-trip (SKILL: "keep the original as master copy")
source /mnt/openscience/audit-envs/alignment/wsl_env.sh
D=/mnt/openscience/audits/bio-alignment-io/run/data; cd $D; mkdir -p inf; cd inf
which cmbuild hmmbuild
echo "== cmbuild ORIGINAL Rfam"; timeout 200 cmbuild -F rf_orig.cm ../rfam_RF00005.sto </dev/null 2>&1 | tail -6 | cut -c1-160; ls -l rf_orig.cm 2>&1 | awk '{print $5,$9}'
echo "== cmbuild AlignIO ROUND-TRIP (GF header lines dropped, SS_cons kept)"; timeout 200 cmbuild -F rf_rt.cm ../rfam_roundtrip.sto </dev/null 2>&1 | tail -6 | cut -c1-160; ls -l rf_rt.cm 2>&1 | awk '{print $5,$9}'
echo "== cmbuild round-trip with -n name"; timeout 200 cmbuild -F -n tRNA rf_rt2.cm ../rfam_roundtrip.sto </dev/null 2>&1 | tail -4 | cut -c1-160; ls -l rf_rt2.cm 2>&1 | awk '{print $5,$9}'
grep -E '^(NAME|ACC|DESC|CLEN|NSEQ)' rf_orig.cm rf_rt2.cm 2>/dev/null
P=/mnt/openscience/audit-envs/alignment/public-data/msa
python - <<'PY'
from Bio import AlignIO
a = AlignIO.read('/mnt/openscience/audit-envs/alignment/public-data/msa/PF00042_seed.sto', 'stockholm'); AlignIO.write(a, 'pf_rt.sto', 'stockholm')
PY
echo "== hmmbuild ORIGINAL Pfam"; hmmbuild --amino pf_orig.hmm $P/PF00042_seed.sto </dev/null 2>&1 | grep -aE "^1 |Error|error" | cut -c1-140
echo "== hmmbuild AlignIO ROUND-TRIP Pfam"; hmmbuild --amino pf_rt.hmm pf_rt.sto </dev/null 2>&1 | grep -aE "^1 |Error|error|FAILED" | cut -c1-160; ls -l pf_rt.hmm 2>&1 | awk '{print $5,$9}'
grep -E '^(NAME|ACC|DESC|LENG)' pf_orig.hmm pf_rt.hmm 2>/dev/null
