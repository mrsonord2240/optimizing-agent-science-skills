#!/usr/bin/env bash
# Final-pass Phase 2 regression replay for bio-alignment-structural.
# Runs only against the copied source snapshot and writes only under this audit's run/ tree.
set -euo pipefail

source /mnt/openscience/audit-envs/alignment/wsl_env.sh
ROOT=/mnt/openscience/audits/bio-alignment-structural/run
SRC="$ROOT/source"
DATA=/mnt/openscience/audit-envs/alignment/public-data/structures
WORK="$ROOT/work"
LOG="$ROOT/logs"
mkdir -p "$WORK" "$LOG"

require_file() { test -s "$1" || { echo "ASSERT FAIL: missing/nonempty $1"; exit 1; }; }
require_match() { grep -Eq "$2" "$1" || { echo "ASSERT FAIL: $1 lacks /$2/"; exit 1; }; }

# The Windows-side provenance script records and asserts the worktree tip. WSL cannot
# resolve this worktree's Windows absolute gitdir with interop disabled.

# Input 1, prior canonical: pairwise globin alignment and the shipped parser.
mkdir -p "$WORK/in1"; pushd "$WORK/in1" >/dev/null
python "$SRC/examples/tm_align_pairwise.py" "$DATA/1MBN.pdb" "$DATA/1A3N.pdb" > "$LOG/01_pairwise_example.txt"
TMalign "$DATA/1MBN.pdb" "$DATA/1A3N.pdb" -outfmt 2 >> "$LOG/01_pairwise_example.txt"
USalign "$DATA/1MBN.pdb" "$DATA/1A3N.pdb" -mol prot -outfmt 2 >> "$LOG/01_pairwise_example.txt"
require_file superposed.pdb; require_match "$LOG/01_pairwise_example.txt" '0\.8356|0\.9000'; popd >/dev/null

# Input 2, prior Foldseek search: local real-structure target, both documented alignment types.
mkdir -p "$WORK/in2/targets"; cp "$DATA"/{1A3N,1A6M,1EMY,1HCK,1ATP,1MBO}.pdb "$WORK/in2/targets/"
pushd "$WORK/in2" >/dev/null
python "$SRC/examples/foldseek_search.py" "$DATA/1MBN.pdb" targets 2 > "$LOG/02_foldseek_type2.txt"
python "$SRC/examples/foldseek_search.py" "$DATA/1MBN.pdb" targets 1 > "$LOG/02_foldseek_type1.txt"
require_file result.m8; require_match "$LOG/02_foldseek_type2.txt" 'Confident structural hits'; require_match "$LOG/02_foldseek_type1.txt" 'alnTM > 0\.5'; popd >/dev/null

# Input 3, prior correspondence edge: supported co-numbered pair and refusal of offset numbering.
mkdir -p "$WORK/in3"; pushd "$WORK/in3" >/dev/null
python "$SRC/examples/biopython_superimposer.py" "$DATA/1MBN.pdb" "$DATA/1A6M.pdb" > "$LOG/03_superimposer_ok.txt"
if python "$SRC/examples/biopython_superimposer.py" "$DATA/1MBN.pdb" "$DATA/1A3N.pdb" > "$LOG/03_superimposer_refusal.txt" 2>&1; then echo 'ASSERT FAIL: offset numbering unexpectedly accepted'; exit 1; fi
require_file mobile_superposed.pdb; require_match "$LOG/03_superimposer_ok.txt" '151 CA pairs'; require_match "$LOG/03_superimposer_refusal.txt" 'different names'; popd >/dev/null

# Input 4, prior structural MSA: seeded Foldmason and JSON LDDT output.
mkdir -p "$WORK/in4/structures"; cp "$DATA"/{1MBN,1A6M,1HCK}.pdb "$WORK/in4/structures/"
pushd "$WORK/in4" >/dev/null
python "$SRC/examples/foldmason_msa.py" structures > "$LOG/04_foldmason.txt"
require_file family_msa_aa.fa; require_file family_msa.json; require_match "$LOG/04_foldmason.txt" 'Per-column LDDT'; popd >/dev/null

# Input 5, prior multimer path: dimer contained in tetramer and Foldseek report.
mkdir -p "$WORK/in5/complexes"; cp "$DATA"/{1A3N,1IRD,1HBA,2LHB}.pdb "$WORK/in5/complexes/"
USalign "$DATA/1IRD.pdb" "$DATA/1A3N.pdb" -mm 1 -ter 0 -outfmt 2 > "$LOG/05_usalign_multimer.txt"
foldseek easy-multimersearch "$DATA/1IRD.pdb" "$WORK/in5/complexes" "$WORK/in5/mm" "$WORK/in5/tmp" -v 1 > "$LOG/05_foldseek_multimer.txt" 2>&1
require_file "$WORK/in5/mm_report"; require_match "$LOG/05_usalign_multimer.txt" '0\.9769|0\.4943'; test "$(awk 'END{print NR}' "$WORK/in5/mm_report")" -ge 1

# Input 6, prior model-quality path: TMscore sequence matching produces GDT-TS.
TMscore "$DATA/1MBN.pdb" "$DATA/1A6M.pdb" -seq > "$LOG/06_tmscore.txt"
require_match "$LOG/06_tmscore.txt" 'GDT-TS-score'; require_match "$LOG/06_tmscore.txt" 'TM-score'

# Input 7, prior adversarial/short-chain guard: the library rejects unalignable input rather than returning a score.
mkdir -p "$WORK/in7"; printf 'ATOM      1  CA  ALA A   1       0.000   0.000   0.000  1.00 20.00           C\nEND\n' > "$WORK/in7/one_residue.pdb"
pushd "$WORK/in7" >/dev/null
if python "$SRC/examples/tm_align_pairwise.py" "$DATA/1MBN.pdb" one_residue.pdb > "$LOG/07_degenerate.txt" 2>&1; then echo 'ASSERT FAIL: one-residue input unexpectedly aligned'; exit 1; fi
require_match "$LOG/07_degenerate.txt" 'produced no alignment'; popd >/dev/null

# Input 8, prior remote-homology variant: kinase pair plus DaliLite re-alignment.
mkdir -p "$WORK/in8/dali/DAT"; cp "$DATA"/{1ATP,1HCK}.pdb "$WORK/in8/dali/"
TMalign "$DATA/1ATP.pdb" "$DATA/1HCK.pdb" -outfmt 2 > "$LOG/08_kinase_tmalign.txt"
pushd "$WORK/in8/dali" >/dev/null
import.pl --pdbfile 1atp.pdb --pdbid 1atp --dat DAT/ > "$LOG/08_dali.txt" 2>&1
import.pl --pdbfile 1hck.pdb --pdbid 1hck --dat DAT/ >> "$LOG/08_dali.txt" 2>&1
dali.pl --cd1 1atpE --cd2 1hckA --dat1 DAT/ --dat2 DAT/ --title kinase --outfmt summary >> "$LOG/08_dali.txt" 2>&1
require_file 1atpE.txt; require_match 1atpE.txt '24\.'; popd >/dev/null
require_match "$LOG/08_kinase_tmalign.txt" '0\.6805|0\.7659'

# Input 9, prior structural search preparation: pLDDT masking database creation has index output.
mkdir -p "$WORK/in9"; cp "$DATA/1MBN.pdb" "$WORK/in9/"
pushd "$WORK/in9" >/dev/null
foldseek createdb --mask-bfactor-threshold 70.0 1MBN.pdb masked > "$LOG/09_masked_createdb.txt" 2>&1
require_file masked.dbtype; require_file masked.index; popd >/dev/null

# Input 10, fresh: MUSTANG's documented three-structure MSA produces a parsable FASTA.
mkdir -p "$WORK/in10"; pushd "$WORK/in10" >/dev/null
mustang-3.2.3 -i "$DATA/1MBN.pdb" "$DATA/1A6M.pdb" "$DATA/1MBO.pdb" -o mustang -F fasta > "$LOG/10_mustang.txt" 2>&1
require_file mustang.afasta; test "$(grep -c '^>' mustang.afasta)" -eq 3; popd >/dev/null

# Input 11, fresh: headless PyMOL superposition creates a rendered structural inspection artifact.
mkdir -p "$WORK/in11"; pushd "$WORK/in11" >/dev/null
pymol -cq -d "load $DATA/1A6M.pdb, mobile; load $DATA/1MBN.pdb, reference; super mobile, reference; ray 300,200; png super.png" > "$LOG/11_pymol.txt" 2>&1
require_file super.png; require_match "$LOG/11_pymol.txt" 'RMSD'; popd >/dev/null

echo 'ALL_PHASE2_ASSERTIONS_PASS' | tee "$LOG/summary.txt"
