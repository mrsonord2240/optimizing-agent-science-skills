source /mnt/openscience/audit-envs/alternative-splicing/wsl_env.sh
R=/mnt/openscience/audits/bio-splicing-qc/run
cd $R
echo "--- bash -n on every bash block"
for f in blocks/*.sh; do bash -n $f && echo "$f parses"; done
echo "--- py_compile skill files"
asenv as-core python -c "import ast,sys; [ast.parse(open(f,encoding='utf-8').read()) for f in ['skill/examples/splicing_qc.py','skill/examples/test_splicing_qc.py']]; print('example files parse')"
echo "--- shipped test in as-core (RSeQC on PATH via wrapper dir; maxentpy absent)"
asenv as-core python skill/examples/test_splicing_qc.py; echo rc=$?
echo "--- shipped test in as-maxent (RSeQC via PATH wrapper)"
asenv as-maxent python skill/examples/test_splicing_qc.py; echo rc=$?
