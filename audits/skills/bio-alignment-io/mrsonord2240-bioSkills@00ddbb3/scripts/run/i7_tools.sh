#!/bin/bash
# INPUT 7 (Adversarial): does what the SKILL says about downstream tools hold on the real tools? WSL, stdin closed, timeouts on.
# Reads files made by i7_prep.py and i7b_prep.py; outputs are asserted by i7_check.py (judge by output text, never exit code).
D=/mnt/openscience/audits/bio-alignment-io/run/data/tools; cd $D
R2="micromamba run -n aln-treetools"; R1="micromamba run -n aln-raxml1"; RO="micromamba run -n aln-phyml-old"; I="micromamba run -n bio iqtree3"
rm -f a7_* 2>/dev/null
echo "versions:"; $R1 raxml-ng --version </dev/null 2>&1 | grep -a "RAxML-NG v"; $R2 raxml-ng --version </dev/null 2>&1 | grep -a "RAxML-NG v"
$R2 phyml --version </dev/null 2>&1 | grep -a "PhyML version"; $RO phyml --version </dev/null 2>&1 | grep -a "PhyML version"; $I --version </dev/null 2>&1 | head -1
# --- RAxML-NG '*' : protein (accepted), nucleotide (rejected), both builds; likelihood equivalence of '*', '-' and 'X'
for v in 1 2; do R=$R1; [ $v = 2 ] && R=$R2
  for f in pf12_star pf12_star_dash pf12_star_X; do
    timeout 300 $R raxml-ng --search1 --msa $f.phy --model LG --data-type AA --threads 2 --seed 1 --prefix a7_rxs${v}_$f </dev/null > a7_rxs${v}_$f.out 2>&1; echo "raxml v$v search1 $f exit=$?"
  done
  timeout 100 $R raxml-ng --check --msa dna_star.phy --model GTR+G --prefix a7_rxd$v </dev/null > a7_rxd$v.out 2>&1; echo "raxml v$v dna star exit=$?"
  for f in pf12_longnames pf12_name_colon pf12_name_comma pf12_name_paren pf12_name_bracket pf12_name_pipe; do
    timeout 100 $R raxml-ng --check --msa $f.phy --model LG --data-type AA --prefix a7_rxc${v}_$f </dev/null > a7_rxc${v}_$f.out 2>&1
  done
done
# --- PhyML: 138-char names (two builds), and one punctuation character per file (new build)
for tag in new old; do
  R=$R2; [ $tag = old ] && R=$RO
  rm -f pf12_longnames.phy_phyml_tree.txt
  timeout 300 $R phyml -i pf12_longnames.phy -d aa -m LG -o n -b 0 --quiet </dev/null > a7_phl_$tag.out 2>&1
  cp pf12_longnames.phy_phyml_tree.txt a7_phyml_${tag}_tree.txt
done
for c in colon comma paren bracket pipe; do
  rm -f pf12_name_$c.phy_phyml_tree.txt
  timeout 300 $R2 phyml -i pf12_name_$c.phy -d aa -m LG -o n -b 0 --quiet </dev/null > a7_ph_$c.out 2>&1; echo "phyml $c exit=$?"
  [ -f pf12_name_$c.phy_phyml_tree.txt ] && cp pf12_name_$c.phy_phyml_tree.txt a7_phyml_${c}_tree.txt
done
# --- IQ-TREE 3.1.3
for f in pf12_relaxed pf12_name_colon pf12_wronglen pf12_longnames; do
  timeout 240 $I -s $f.phy -n 0 -m LG -redo -pre a7_iq_$f </dev/null > a7_iq_$f.out 2>&1; echo "iqtree $f exit=$?"
done
timeout 60 $I -s pf12_relaxed.phy --check -pre a7_iq_chk </dev/null > a7_iq_chk.out 2>&1; echo "iqtree --check exit=$?"
# --- MrBayes 3.2.7: Biopython NEXUS (quoted Pfam ids) vs the SKILL recipe's output (i7_recipe.py writes pf12_recipe.nex)
for f in pf12 pf12_recipe; do
  cat > a7_mb_$f.nex <<NX
begin mrbayes;
  set autoclose=yes nowarn=yes quitonerror=yes;
  execute $f.nex;
  lset rates=equal; prset aamodelpr=fixed(wag);
  mcmc ngen=200 samplefreq=100 printfreq=100 nchains=1 nruns=1 diagnfreq=100 filename=a7_mbout_$f;
  quit;
end;
NX
  timeout 240 $R2 mb a7_mb_$f.nex </dev/null > a7_mb_$f.out 2>&1; echo "mrbayes $f exit=$?"
done
