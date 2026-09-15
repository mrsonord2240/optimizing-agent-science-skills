# Input 4 (Variant B) -- SYNTHETIC 15-taxon protein MSA for a profile HMM; needs original column indices back and a
# reproducible, version-pinned trimAl run. Skill: trimAl -gappyout for hmmbuild; -colnumbering; avoid -automated1 for audits.
set -u
cd "$(dirname "$0")"
T=/f/OpenScience/audit-envs/molecular-phylogenetics-analyst/tools
TRIMAL141=$T/trimal_v1.4.1/trimal.exe
TRIMAL151=$T/trimal_v1.5.1/trimAl_Windows_x86-64/trimal.exe
cp ../../data/deep_super/gene03.aln.fasta input.fasta
$TRIMAL141 --version
echo "== trimAl 1.5.1 (Windows release binary)"; $TRIMAL151 --version; echo "exit $?"
echo "== Skill: gappyout for HMM building"
$TRIMAL141 -in input.fasta -out hmm_gappyout.fasta -gappyout; echo "exit $?"
echo "== Skill command (as written): -gt 0.3 -st 0.5 -cons 60 -colnumbering > columns.txt"
$TRIMAL141 -in input.fasta -out manual.fasta -gt 0.3 -st 0.5 -cons 60 -colnumbering > columns.txt; echo "exit $?"
head -c 400 columns.txt; echo
echo "== Skill column-mapping command (as written): -automated1 -colnumbering > kept_columns.txt"
$TRIMAL141 -in input.fasta -out auto1.fasta -automated1 -colnumbering > kept_columns.txt; echo "exit $?"
head -c 300 kept_columns.txt; echo
echo "== gappyout with -colnumbering"
$TRIMAL141 -in input.fasta -out hmm_gappyout2.fasta -gappyout -colnumbering > gappyout_cols.txt; echo "exit $?"
echo "== -automated1 determinism: 3 repeated runs, and which mode it picked (compare to explicit modes)"
for k in 1 2 3; do $TRIMAL141 -in input.fasta -out auto1_run$k.fasta -automated1; done
for m in gappyout strict strictplus; do $TRIMAL141 -in input.fasta -out mode_$m.fasta -$m; done
md5sum auto1_run*.fasta mode_*.fasta hmm_gappyout.fasta hmm_gappyout2.fasta
echo "== HMMER hmmbuild availability"; command -v hmmbuild || echo "hmmbuild not installed (no Windows build)"
PYTHONIOENCODING=utf-8 /f/OpenScience/audit-envs/molecular-phylogenetics-analyst/Scripts/python.exe in4_report.py
