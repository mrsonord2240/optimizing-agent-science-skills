#!/bin/bash
# Input 2/M4: check the SKILL.md Install block. Fresh venv in WSL /tmp (not the shared envs). pip --dry-run resolves without installing.
export PYTHONDONTWRITEBYTECODE=1
PY=/home/sci/micromamba/envs/as-spvp/bin/python
rm -rf /tmp/rea_venv && $PY -m venv /tmp/rea_venv && . /tmp/rea_venv/bin/activate
pip --version
echo "=== SKILL.md line: pip install spliceai tensorflow \"setuptools<81\" (dry run)"
pip install --dry-run spliceai tensorflow "setuptools<81" 2>&1 | grep -E "Would install|ERROR" | tr ' ' '\n' | grep -E "^(spliceai|tensorflow|setuptools|keras|numpy|pyvcf|pysam)-"
echo "=== Pangolin line: pip install torch gffutils pyfaidx pyfastx biopython pandas PyVCF3==1.0.0 (dry run)"
pip install --dry-run torch gffutils pyfaidx pyfastx biopython pandas "PyVCF3==1.0.0" 2>&1 | grep -E "Would install|ERROR" | tr ' ' '\n' | grep -E "^(torch|gffutils|pyfaidx|pyfastx|biopython|pandas|PyVCF3|numpy|nvidia-cudnn)"
echo "=== git clone https://github.com/tkzeng/Pangolin && pip install ./Pangolin (--no-deps real install to check the entry points)"
rm -rf /tmp/Pangolin_rea && git clone -q https://github.com/tkzeng/Pangolin /tmp/Pangolin_rea && git -C /tmp/Pangolin_rea log -1 --format='%h %ci'
pip install -q --no-deps /tmp/Pangolin_rea 2>&1 | tail -2
ls /tmp/rea_venv/bin | grep -iE "pangolin|create_db"
pip show -f pangolin 2>/dev/null | grep -E "^(Name|Version|Requires)"
echo "=== weights inside package:"; ls /tmp/rea_venv/lib/python3.10/site-packages/pangolin/models | wc -l
echo "=== mmsplice line (dry run)"
pip install --dry-run mmsplice 2>&1 | grep -E "Would install|ERROR" | tr ' ' '\n' | grep -E "^(mmsplice|cyvcf2|tensorflow|numpy|keras|kipoiseq)-"
echo "=== CI-SpliceAI line (dry run)"
pip install --dry-run "tensorflow-cpu==2.15.*" "keras<3" cispliceai 2>&1 | grep -E "Would install|ERROR" | tr ' ' '\n' | grep -E "^(cispliceai|tensorflow|keras|numpy)"
echo "=== SpliceTransformer line (dry run)"
pip install --dry-run torch sinkhorn-transformer "axial-positional-embedding==0.2.1" "PyVCF3==1.0.0" pyensembl gffutils pyfaidx pandas tqdm gdown 2>&1 | grep -E "Would install|ERROR" | tr ' ' '\n' | grep -E "^(sinkhorn|axial|pyensembl|gdown|PyVCF3)"
