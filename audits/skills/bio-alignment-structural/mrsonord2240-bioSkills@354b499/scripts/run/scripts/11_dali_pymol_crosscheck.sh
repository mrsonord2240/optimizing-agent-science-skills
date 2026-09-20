#!/bin/bash
# Independent cross-check for inputs 1 and 7: DaliLite v5 (local, not the DALI web server) and PyMOL super/cealign.
source /mnt/openscience/audit-envs/alignment/wsl_env.sh
R=/mnt/openscience/audits/bio-alignment-structural/run
S=$R/data/real_pdb
D=$ALN/tools/src/DaliLite.v5
O=$R/work/dali; rm -rf $O; mkdir -p $O/DAT; cd $O
for id in 1mbn 1a3n 1atp 1hck 1ubq 1pga; do
  cp $S/$(echo $id | tr a-z A-Z).pdb $O/$id.pdb
  perl $D/bin/import.pl --pdbfile $O/$id.pdb --pdbid $id --dat $O/DAT > import_$id.log 2>&1
done
ls DAT | tr '\n' ' '; echo
run_dali() { # cd1 cd2 tag ; each in own dir (DaliLite overwrites <cd1>.txt)
  mkdir -p $O/$3; cd $O/$3
  perl $D/bin/dali.pl --cd1 $1 --cd2 $2 --dat1 $O/DAT --dat2 $O/DAT --title $3 --outfmt "summary" > dali.log 2>&1
  echo "=== DALI $3 ($1 vs $2)"; grep -a -B1 -A3 "No:" *.txt | head -8; cd $O
}
run_dali 1mbnA 1a3nA mb_hb
run_dali 1atpE 1hckA pka_cdk2
run_dali 1ubqA 1pgaA ubq_gb1
run_dali 1mbnA 1atpE mb_pka
echo "=== PyMOL (headless) super / cealign on 1MBN vs 1A3N chain A"
cat > $O/pm.py <<'PY'
from pymol import cmd
cmd.load('/mnt/openscience/audits/bio-alignment-structural/run/data/real_pdb/1MBN.pdb','ref')
cmd.load('/mnt/openscience/audits/bio-alignment-structural/run/data/real_pdb/1A3N.pdb','mob')
r = cmd.super('mob and chain A','ref')
print('PYMOL super  RMSD=%.3f n_atoms=%d' % (r[0], r[1]))
r = cmd.cealign('ref','mob and chain A')
print('PYMOL cealign RMSD=%.3f n_aligned=%d' % (r['RMSD'], r['alignment_length']))
PY
python $O/pm.py 2>&1 | grep -a PYMOL
