#!/bin/bash
# INPUT 7 (NEW): downstream-tool acceptance of what the SKILL tells the agent to write. Runs in WSL, stdin closed, timeouts on.
# Outputs are asserted afterwards by i7_check.py (judge by output, not exit code).
D=/mnt/openscience/audits/bio-alignment-io/run/data/tools; cd $D
rm -f rx*.log rx*.reduced.phy rx*.phy.* ph_*.log *_phyml_* iq_* mb_* 2>/dev/null
R2="micromamba run -n aln-treetools"; R1="micromamba run -n aln-raxml1"
for v in 1 2; do
  R=$R1; [ $v = 2 ] && R=$R2
  for f in pf12_relaxed pf12_star pf12_starX pf12_longnames pf12_foreign_colon; do
    timeout 120 $R raxml-ng --check --msa $f.phy --model LG --data-type AA --prefix rx${v}_$f </dev/null > rx${v}_$f.out 2>&1; echo "raxml v$v $f exit=$?"
  done
done
for f in pf12_relaxed pf12_longnames pf12_foreign_colon pf12_star; do
  timeout 240 $R2 phyml -i $f.phy -d aa -m LG -o n -b 0 --quiet </dev/null > ph_$f.out 2>&1; echo "phyml $f exit=$?"
done
I="micromamba run -n bio iqtree3"
for f in pf12_relaxed pf12_foreign_colon pf12_wronglen pf12_star; do
  timeout 240 $I -s $f.phy -n 0 -m LG -redo -pre iq_$f </dev/null > iq_$f.out 2>&1; echo "iqtree3 $f exit=$?"
done
timeout 60 $I -s pf12_relaxed.phy --check -pre iq_chk </dev/null > iq_chk.out 2>&1; echo "iqtree3 --check exit=$?"
# MrBayes: does Biopython's NEXUS (molecule_type protein) load, and does a 0-generation-ish run start?
cat > mb.nex <<'NX'
begin mrbayes;
  set autoclose=yes nowarn=yes;
  execute pf12.nex;
  lset rates=equal; prset aamodelpr=fixed(wag);
  mcmc ngen=200 samplefreq=100 printfreq=100 nchains=1 nruns=1 diagnfreq=100;
  quit;
end;
NX
timeout 240 $R2 mb mb.nex </dev/null > mb_pf12.out 2>&1; echo "mrbayes exit=$?"
