#!/bin/bash
# INPUT 7 (NEW) part 2: deeper checks for the two claims the fixer left unverified + MrBayes NEXUS naming.
D=/mnt/openscience/audits/bio-alignment-io/run/data/tools; cd $D
R2="micromamba run -n aln-treetools"; R1="micromamba run -n aln-raxml1"
echo "## RAxML-NG '*' : full --parse and a 1-tree search, v1.2.2 and v2.0.3"
for v in 1 2; do R=$R1; [ $v = 2 ] && R=$R2
  for f in pf12_star; do
    timeout 200 $R raxml-ng --parse --msa $f.phy --model LG --data-type AA --prefix rxp${v}_$f </dev/null > rxp${v}_$f.out 2>&1; echo "v$v --parse exit=$?"; grep -aE "ERROR|exception|Alphabet|bad|invalid" rxp${v}_$f.out | head -3
    timeout 300 $R raxml-ng --search1 --msa $f.phy --model LG --data-type AA --threads 2 --seed 1 --prefix rxs${v}_$f </dev/null > rxs${v}_$f.out 2>&1; echo "v$v --search1 exit=$?"; grep -aE "ERROR|exception|Final LogLikelihood|invalid|bad" rxs${v}_$f.out | head -3
  done
done
echo "## RAxML-NG DNA alignment with '*' (nucleotide)"
printf ' 3 8\nA1  ACGT*ACG\nA2  ACGTAACG\nA3  ACGTTACG\n' > dna_star.phy
$R1 raxml-ng --check --msa dna_star.phy --model GTR+G --prefix rxd1 </dev/null 2>&1 | grep -aE "ERROR|exception|successfully|Invalid|invalid" | head
$R2 raxml-ng --check --msa dna_star.phy --model GTR+G --prefix rxd2 </dev/null 2>&1 | grep -aE "ERROR|exception|successfully|Invalid|invalid" | head
echo "## PhyML older build (3.3.20220408?) 138-char names"
micromamba create -y -n aln-phyml-old -c conda-forge -c bioconda "phyml=3.3.20220408" </dev/null 2>&1 | tail -1
micromamba run -n aln-phyml-old phyml --version </dev/null 2>&1 | grep -a "PhyML version" 
timeout 240 micromamba run -n aln-phyml-old phyml -i pf12_longnames.phy -d aa -m LG -o n -b 0 --quiet </dev/null > phold.out 2>&1; echo "old phyml exit=$?"; tail -3 phold.out | cut -c1-150; ls pf12_longnames.phy_phyml_tree.txt
echo "## MrBayes NEXUS: names as written by Biopython vs sanitised"
python3 - <<'PY'
import re
s=open('pf12.nex').read()
open('pf12_clean.nex','w').write(re.sub(r"'([^']+)'", lambda m: re.sub(r'[/-]','_',m.group(1)), s))
PY
for f in pf12 pf12_clean; do
cat > mb_$f.nex <<NX
begin mrbayes;
  set autoclose=yes nowarn=yes quitonerror=yes;
  execute $f.nex;
  lset rates=equal; prset aamodelpr=fixed(wag);
  mcmc ngen=200 samplefreq=100 printfreq=100 nchains=1 nruns=1 diagnfreq=100 filename=mbout_$f;
  quit;
end;
NX
timeout 240 $R2 mb mb_$f.nex </dev/null > mb_$f.out 2>&1; echo "mrbayes $f exit=$?"; grep -aE "Instead found|Error in|Analysis completed|Chain results" mb_$f.out | head -4
done
