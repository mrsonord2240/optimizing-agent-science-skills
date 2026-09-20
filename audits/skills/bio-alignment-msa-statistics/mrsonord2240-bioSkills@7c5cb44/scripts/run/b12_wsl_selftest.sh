#!/bin/bash
# Same shipped selftest and two shipped examples on the WSL Python (env alignment: numpy 2.5.3, Biopython 1.88), from a COPY.
# Run: wsl_run.sh 'bash /mnt/openscience/audits/bio-alignment-msa-statistics/run/b12_wsl_selftest.sh'
export PYTHONDONTWRITEBYTECODE=1 PYTHONIOENCODING=utf-8
W=/tmp/msastats_wsl_copy; rm -rf $W; mkdir -p $W
cp -r /mnt/openscience/audits/bio-alignment-msa-statistics/run/skill/examples/. $W/
cd $W
python -c "import numpy, Bio; print('numpy', numpy.__version__, 'biopython', Bio.__version__)"
python -B selftest.py 2>&1 | tail -4
echo "selftest exit=${PIPESTATUS[0]}"
python -B identity_matrix.py /mnt/openscience/audits/bio-alignment-msa-statistics/run/data/seed_dot.fasta pid1 2>&1 | tail -2
python -B substitution_counts.py /mnt/openscience/audits/bio-alignment-msa-statistics/run/data/hbb6_mafft_default.fa 2>&1 | tail -4
rm -rf $W
