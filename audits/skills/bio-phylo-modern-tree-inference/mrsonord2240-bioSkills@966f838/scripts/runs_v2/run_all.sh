#!/bin/bash
# Re-audit runs against mrsonord2240/bioSkills@966f838 (fixed Skill). IQ-TREE 2.4.0 only on this machine.
source /f/OpenScience/audit-envs/molecular-phylogenetics-analyst/env.sh
A=/f/OpenScience/audits/bio-phylo-modern-tree-inference
D=$A/data; R=$A/runs_v2; OLD=$A/runs
SK=/f/OpenScience/external/mrsonord2240__bioSkills/phylogenetics/modern-tree-inference
mkdir -p $R && cd $R
echo "== literal iqtree3 name check"; (iqtree3 --version) > iqtree3_literal.out 2>&1; echo "exit=$?" >> iqtree3_literal.out
# Resolver the fixed examples use; agent applies same on this machine
IQ=$(command -v iqtree3 || command -v iqtree2 || command -v iqtree); echo "resolved: $IQ" | tee resolver.out

# In1 canonical
mkdir -p in1 && cd in1 && cp $D/gene12_aln.fa .
$IQ -s gene12_aln.fa -m MFP -B 1000 -bnni -alrt 1000 -T AUTO -ntmax 4 --seed 12345 --prefix run1 > run1.stdout 2>&1; echo "in1 exit=$?"
cd $R
# In2 partitions
mkdir -p in2 && cd in2 && cp $OLD/in2/concat10.fasta $OLD/in2/partitions.nex .
$IQ -s concat10.fasta -p partitions.nex -m MFP+MERGE -rcluster 10 -B 1000 -bnni -alrt 1000 -T AUTO -ntmax 4 --seed 12345 --prefix part > part.stdout 2>&1; echo "in2 exit=$?"
cd $R
# In3 tiny
mkdir -p in3 && cd in3 && cp $OLD/in3/isolates6.fa .
$IQ -s isolates6.fa -m MFP -B 1000 -bnni -alrt 1000 -T 1 --seed 12345 --prefix tiny > tiny.stdout 2>&1; echo "in3 exit=$?"
cd $R
# In4 AU test
mkdir -p in4 && cd in4 && cp $D/gene12_aln.fa $OLD/in4/euarchontoglires.constraint .
cp ../in1/run1.treefile ml.treefile
$IQ -s gene12_aln.fa -m K2P+G4 -g euarchontoglires.constraint --seed 12345 --prefix constrained > c.stdout 2>&1; echo "in4a exit=$?"
cat ml.treefile constrained.treefile > trees.nex
$IQ -s gene12_aln.fa -m K2P+G4 -z trees.nex -n 0 -zb 10000 -au --seed 12345 --prefix autest > au.stdout 2>&1; echo "in4b exit=$?"
cd $R
# In5 ILS concordance, commands verbatim from fixed SKILL.md
mkdir -p in5 && cd in5 && cp -r $OLD/in5/loci_dir . && cp $OLD/in5/concat.fasta .
$IQ -s concat.fasta -m MFP -B 1000 -bnni -alrt 1000 -T 4 --seed 12345 --prefix concat > concat.stdout 2>&1; echo "in5a exit=$?"
$IQ -S loci_dir -m MFP -B 1000 -T AUTO --prefix loci > loci.stdout 2>&1; echo "in5b exit=$?"
$IQ -t concat.treefile --gcf loci.treefile --prefix concord_g > cg.stdout 2>&1; echo "in5c exit=$?"
$IQ -te concat.treefile -s concat.fasta --scfl 100 -T 4 --prefix concord_s > cs.stdout 2>&1; echo "in5d exit=$?"
cd $R
# In7 LBA
mkdir -p in7 && cd in7 && cp $OLD/in7/lba_aln.fa $OLD/in7/lba_noC.fa $OLD/in7/AC.constraint .
$IQ -s lba_aln.fa -m JC -B 1000 --seed 12345 --prefix lba_jc > jc.stdout 2>&1; echo "in7a exit=$?"
$IQ -s lba_aln.fa -m MFP -B 1000 -bnni -alrt 1000 --seed 12345 --prefix lba > lba.stdout 2>&1; echo "in7b exit=$?"
$IQ -s lba_aln.fa -m K2P+G4 -g AC.constraint --seed 12345 --prefix AC > ac.out 2>&1; echo "in7c exit=$?"
cat lba.treefile AC.treefile > trees.nex
$IQ -s lba_aln.fa -m K2P+G4 -z trees.nex -n 0 -zb 10000 -au --seed 12345 --prefix au > au.out 2>&1; echo "in7d exit=$?"
$IQ -s lba_noC.fa -m K2P+G4 -B 1000 -bnni -alrt 1000 --seed 12345 --prefix noC > noC.out 2>&1; echo "in7e exit=$?"
cd $R
# In8 NEW: protein PMSF (guide tree, then LG+C20+F+G with -ft)
mkdir -p in8 && cd in8 && cp $D/prot15_true_aln.fa prot15.fa
$IQ -s prot15.fa -m LG+F+G --seed 12345 --prefix guide > guide.stdout 2>&1; echo "in8a exit=$?"
$IQ -s prot15.fa -m LG+C20+F+G -ft guide.treefile -B 1000 -bnni -alrt 1000 --seed 12345 --prefix pmsf > pmsf.stdout 2>&1; echo "in8b exit=$?"
$IQ -s prot15.fa -m MFP -B 1000 -bnni -alrt 1000 --seed 12345 --prefix mfp > mfp.stdout 2>&1; echo "in8c exit=$?"
cd $R
# In9 NEW: concordance with missing taxa in loci
mkdir -p in9 && cd in9
python $R/make_missing.py > missing.out 2>&1; echo "in9 prep exit=$?"
$IQ -S loci_missing -m MFP -B 1000 -T AUTO --prefix locim > locim.stdout 2>&1; echo "in9a exit=$?"
$IQ -t ../in5/concat.treefile --gcf locim.treefile --prefix cgm > cgm.stdout 2>&1; echo "in9b exit=$?"
$IQ -te ../in5/concat.treefile -s ../in5/concat.fasta --scfl 100 -T 4 --seed 12345 --prefix csm > csm.stdout 2>&1; echo "in9c exit=$?"
cd $R
# Shipped examples, as written
mkdir -p examples && cd examples && cp $OLD/examples/gene12_aln.fa $OLD/examples/concatenated.fasta .
bash -n $SK/examples/iqtree_basic.sh && bash -n $SK/examples/partitioned_analysis.sh && bash -n $SK/examples/raxml_analysis.sh && echo "bash -n OK"
bash $SK/examples/iqtree_basic.sh gene12_aln.fa > basic.out 2>&1; echo "ex_basic exit=$?"
bash $SK/examples/partitioned_analysis.sh concatenated.fasta > part.out 2>&1; echo "ex_part exit=$?"
$IQ -h > ../iqtree_help.txt 2>&1
echo ALL DONE
