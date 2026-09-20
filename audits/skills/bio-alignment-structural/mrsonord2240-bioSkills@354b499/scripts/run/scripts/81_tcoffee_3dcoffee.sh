#!/bin/bash
# T-Coffee 3D-Coffee attempts. (a) SKILL.md form with local pdb files in cwd; (b) explicit TMalign_pair method (tooling-agent recipe)
source /mnt/openscience/audit-envs/alignment/wsl_env.sh
R=/mnt/openscience/audits/bio-alignment-structural/run; S=$R/data/real_pdb
cd $R/work/misc; rm -rf tc; mkdir tc; cd tc
for x in 1MBN 1EMY 2LHB; do cp $S/$x.pdb $x.pdb; done
python - <<'PY'
from Bio.PDB import PDBParser, PPBuilder
S='/mnt/openscience/audits/bio-alignment-structural/run/data/real_pdb/'
with open('input.fasta','w') as f, open('templates.txt','w') as t:
    for n in ('1MBN','1EMY','2LHB'):
        ch=[x for x in PDBParser(QUIET=True).get_structure(n,S+n+'.pdb')[0]][0]
        f.write('>%s\n%s\n'%(n,''.join(str(p.get_sequence()) for p in PPBuilder().build_peptides(ch)))); t.write('>%s _P_ %s\n'%(n,n))
PY
echo "== (a) SKILL.md: t_coffee input.fasta -template_file templates.txt -mode 3dcoffee"
timeout 120 t_coffee input.fasta -template_file templates.txt -mode 3dcoffee -output fasta_aln -outfile a.aln </dev/null > a.log 2>&1; echo rc=$?
grep -a -iE "fatal|could not|cannot" a.log | sort | uniq -c | head -5; ls -la a.aln 2>&1 | head -2
echo "== (b) explicit: -method TMalign_pair,mafft_msa"
timeout 120 t_coffee input.fasta -template_file templates.txt -method TMalign_pair,mafft_msa -output fasta_aln -outfile b.aln </dev/null > b.log 2>&1; echo rc=$?
grep -a -iE "cannot be applied" b.log | sort | uniq -c | head -3; ls -la b.aln 2>&1 | head -2; head -c 300 b.aln 2>/dev/null
