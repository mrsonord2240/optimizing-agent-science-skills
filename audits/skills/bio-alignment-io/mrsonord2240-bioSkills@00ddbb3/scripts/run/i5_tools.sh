#!/bin/bash
# INPUT 5 tool stage (WSL): MrBayes 3.2.7 on the NEXUS the shipped example wrote (real ids) vs the NEXUS after the SKILL's id recipe; IQ-TREE 3.1.3 and RAxML-NG 2.0.3 on the
# PHYLIP-relaxed the example wrote; codeml (PAML 4.10.10) on phylip-sequential vs phylip-relaxed. stdin closed everywhere. Judged by i5_check.py (output text), not exit codes.
D=/mnt/openscience/audits/bio-alignment-io/run/data/e2e; cd $D
RT="micromamba run -n aln-treetools"
rm -f mb_*.out mbout_* iq_*  rx_* 2>/dev/null
for f in hbb6_example hbb6_recipe globins8_example globins8_recipe; do
  cat > mb_$f.nex <<NX
begin mrbayes;
  set autoclose=yes nowarn=yes quitonerror=yes;
  execute $f.nex;
  lset rates=equal;
  mcmc ngen=200 samplefreq=100 printfreq=100 nchains=1 nruns=1 diagnfreq=100 filename=mbout_$f;
  quit;
end;
NX
  timeout 240 $RT mb mb_$f.nex </dev/null > mb_$f.out 2>&1; echo "mrbayes $f exit=$?"
done
I="micromamba run -n bio iqtree3"
timeout 200 $I -s hbb6_relaxed.phy -n 0 -m GTR -redo -pre iq_hbb6 </dev/null > iq_hbb6.out 2>&1; echo "iqtree hbb6 exit=$?"
timeout 200 $I -s globins8_relaxed.phy -n 0 -m LG -redo -pre iq_globins8 </dev/null > iq_globins8.out 2>&1; echo "iqtree globins8 exit=$?"
timeout 100 $RT raxml-ng --check --msa hbb6_relaxed.phy --model GTR+G --prefix rx_hbb6 </dev/null > rx_hbb6.out 2>&1; echo "raxml hbb6 exit=$?"
timeout 100 $RT raxml-ng --check --msa globins8_relaxed.phy --model LG --data-type AA --prefix rx_globins8 </dev/null > rx_globins8.out 2>&1; echo "raxml globins8 exit=$?"
timeout 100 $RT raxml-ng --check --msa hbb6_recipe.phy --model GTR+G --prefix rx_hbb6_recipe </dev/null > rx_hbb6_recipe.out 2>&1; echo "raxml hbb6 recipe exit=$?"
source /mnt/openscience/audit-envs/alignment/wsl_env.sh
for tag in seq rel; do
  cd $D/codeml_$tag || exit 1
  rm -f mlc rst rub rlf 2lnf 4fold.nei lnf
  timeout 120 codeml codeml.ctl </dev/null > stdout.txt 2>&1
  echo "== codeml $tag (exit $?)"; tail -2 stdout.txt
done
