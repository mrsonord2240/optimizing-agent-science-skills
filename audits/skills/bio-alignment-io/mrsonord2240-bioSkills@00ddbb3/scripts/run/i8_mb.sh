#!/bin/bash
# INPUT 8 part 2 tool stage: MrBayes 3.2.7 on datatype=rna NEXUS files (example as written, and after the SKILL id recipe). stdin closed.
D=/mnt/openscience/audits/bio-alignment-io/run/data/rna_mb; cd $D
RT="micromamba run -n aln-treetools"
for f in rna_example rna_recipe; do
  cat > mb_$f.nex <<NX
begin mrbayes;
  set autoclose=yes nowarn=yes quitonerror=yes;
  execute $f.nex;
  lset nucmodel=4by4 rates=equal;
  mcmc ngen=200 samplefreq=100 printfreq=100 nchains=1 nruns=1 diagnfreq=100 filename=mbout_$f;
  quit;
end;
NX
  timeout 240 $RT mb mb_$f.nex </dev/null > mb_$f.out 2>&1; echo "mrbayes $f exit=$?"
done
