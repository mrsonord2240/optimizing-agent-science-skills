#!/bin/bash
# SQ-06 claims: pandas-default header failure message and statsmodels 0.15 breakage.
O=/mnt/openscience/audits/bio-splicing-quantification/run-reaudit-1/out/suppa; cd $O
echo "== pandas default header (as-suppa)"
micromamba run -n as-suppa suppa.py psiPerEvent -i planted_SE_strict.ioe -e planted_tpm_pandas.tsv -o hdr_default 2>&1 | grep -ai -e expected -e error -e buffered | head -3; ls hdr_default.psi 2>&1 | head -1
echo "== write_suppa_tpm header (as-suppa)"
micromamba run -n as-suppa suppa.py psiPerEvent -i planted_SE_strict.ioe -e planted_tpm_suppa.tsv -o hdr_ok 2>&1 | tail -1; cat hdr_ok.psi
echo "== as-core statsmodels / suppa.py"
micromamba run -n as-core python -c "import statsmodels;print('as-core statsmodels',statsmodels.__version__)"
CORE_SUPPA=$(ls /home/sci/micromamba/envs/as-core/bin/suppa.py 2>/dev/null); echo "core suppa: $CORE_SUPPA"
micromamba run -n as-core python /home/sci/micromamba/envs/as-core/bin/suppa.py psiPerEvent -i planted_SE_strict.ioe -e planted_tpm_suppa.tsv -o core_try 2>&1 | tail -3
