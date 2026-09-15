# Shipped examples run as written (byte-identical copies) on the SYNTHETIC prot15 protein MSA named input.fasta.
# Environment "as a user would have it": clipkit on PATH; trimal / BMGE.jar / divvier per each script's assumption.
set -u
export PATH=/f/OpenScience/audit-envs/molecular-phylogenetics-analyst/Scripts:$PATH
T=/f/OpenScience/audit-envs/molecular-phylogenetics-analyst/tools
PY=/f/OpenScience/audit-envs/molecular-phylogenetics-analyst/Scripts/python.exe
SRC=/f/OpenScience/external/GPTomics__bioSkills/alignment/alignment-trimming/examples
cd "$(dirname "$0")"
for s in clipkit_trim trimal_modes bmge_trim divvier_split; do
  mkdir -p $s; cp $SRC/$s.py $s/; cp ../../data/prot15_linsi.fasta $s/input.fasta
  cmp $SRC/$s.py $s/$s.py && echo "$s.py byte-identical copy"
  $PY -m py_compile $s/$s.py && echo "$s.py py_compile OK"
done
echo "===== clipkit_trim.py"; (cd clipkit_trim && PYTHONIOENCODING=utf-8 $PY clipkit_trim.py; echo "exit $?"; ls)
echo "===== trimal_modes.py (as written; trimal not on PATH)"; (cd trimal_modes && PYTHONIOENCODING=utf-8 $PY trimal_modes.py 2>&1 | tail -3; echo "exit ${PIPESTATUS[0]}")
echo "===== trimal_modes.py (trimAl 1.4.1 put on PATH as 'trimal')"; mkdir -p shim; cp $T/trimal_v1.4.1/trimal.exe shim/trimal.exe
(cd trimal_modes && PATH=$PWD/../shim:$PATH PYTHONIOENCODING=utf-8 $PY trimal_modes.py; echo "exit $?"; head -c 200 cols_gappyout.txt; echo)
echo "===== bmge_trim.py with BMGE 1.12 as ./BMGE.jar"; cp $T/BMGE112.jar bmge_trim/BMGE.jar
(cd bmge_trim && PYTHONIOENCODING=utf-8 $PY bmge_trim.py 2>&1 | tr '\r' '\n' | grep -v -E '^ *[0-9.]+%' | tail -8; echo "exit ${PIPESTATUS[0]}")
echo "===== bmge_trim.py with BMGE 2.0 as ./BMGE.jar"; mkdir -p bmge_trim_v2; cp bmge_trim/bmge_trim.py bmge_trim/input.fasta bmge_trim_v2/; cp $T/BMGE200.jar bmge_trim_v2/BMGE.jar
(cd bmge_trim_v2 && PYTHONIOENCODING=utf-8 $PY bmge_trim.py 2>&1 | tail -4; echo "exit ${PIPESTATUS[0]}"; ls)
echo "===== divvier_split.py (no Divvier Windows build)"; (cd divvier_split && PYTHONIOENCODING=utf-8 $PY divvier_split.py 2>&1 | tail -3; echo "exit ${PIPESTATUS[0]}")
