#!/bin/bash
# Misc SKILL.md / usage-guide claims: PyMOL headless one-liner, bioconda tmalign, T-Coffee 3D-Coffee / expresso, MUSTANG, cross-skill refs.
source /mnt/openscience/audit-envs/alignment/wsl_env.sh
R=/mnt/openscience/audits/bio-alignment-structural/run; S=$R/data/real_pdb
mkdir -p $R/work/misc && cd $R/work/misc && rm -f *
cp $S/1MBN.pdb reference.pdb; cp $S/1A6M.pdb mobile.pdb
echo "== PyMOL one-liner from SKILL.md (with png)"
timeout 120 pymol -cq -d "load reference.pdb; load mobile.pdb; super mobile, reference; ray 800,600; png fig.png" </dev/null 2>&1 | grep -aiE "rms|error|executive" | head -5
ls -la fig.png 2>&1
echo "== bioconda tmalign package binary (usage-guide: conda install -c bioconda ... tmalign)"
ls /home/sci/micromamba/envs/alignment/bin | grep -i -E "^tmalign|^TMalign" ; /home/sci/micromamba/envs/alignment/bin/TMalign 2>&1 | head -3
echo "== T-Coffee 3D-Coffee (SKILL line 236) on 4 real structures"
python - <<'PY'
from Bio.PDB import PDBParser, PPBuilder
import os
S='/mnt/openscience/audits/bio-alignment-structural/run/data/real_pdb/'
recs=[('1MBN','1MBN.pdb','A'),('1EMY','1EMY.pdb','A'),('1A3N_A','1A3N.pdb','A'),('2LHB','2LHB.pdb','A')]
with open('input.fasta','w') as f, open('templates.txt','w') as t:
    for n,p,c in recs:
        st=PDBParser(QUIET=True).get_structure(n,S+p)
        ch=[x for x in st[0]][0]
        seq=''.join(str(pp.get_sequence()) for pp in PPBuilder().build_peptides(ch))
        f.write('>%s\n%s\n'%(n,seq)); t.write('>%s _P_ %s\n'%(n,S+p))
PY
timeout 300 t_coffee input.fasta -template_file templates.txt -mode 3dcoffee -outfile 3d.aln -output fasta_aln </dev/null > tc3d.log 2>&1; echo "rc=$?"; grep -a -iE "cannot be applied|error|fatal" tc3d.log | sort | uniq -c | head -5; ls -la 3d.aln 2>&1; head -c 400 3d.aln 2>/dev/null
echo "== T-Coffee expresso (SKILL line 234)"
timeout 120 t_coffee input.fasta -mode expresso -output fasta_aln -outfile ex.fasta </dev/null 2>&1 | grep -a -iE "fatal|error|blast" | head -3; ls -la ex.fasta 2>&1 | head -2
echo "== MUSTANG (table row only)"; mustang-3.2.3 -i $S/1MBN.pdb $S/1A6M.pdb $S/1MBO.pdb -o m -F fasta </dev/null > m.log 2>&1; ls m* | tr '\n' ' '; echo
echo "== cross-skill paths referenced in SKILL.md 'Related Skills'"
B=/mnt/openscience/external/mrsonord2240__bioSkills
for p in alignment/multiple-alignment alignment/pairwise-alignment alignment/msa-parsing alignment/msa-statistics alignment/alignment-io alignment/alignment-trimming structural-biology/modern-structure-prediction structural-biology/alphafold-predictions structural-biology/structure-navigation phylogenetics/modern-tree-inference; do [ -d $B/$p ] && echo "EXISTS  $p" || echo "MISSING $p"; done
