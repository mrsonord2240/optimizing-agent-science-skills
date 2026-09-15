#!/bin/bash
# Re-audit of bio-phylo-bayesian-inference at mrsonord2240/bioSkills@966f838. MrBayes 3.2.7a (Windows serial).
# All data SYNTHETIC (data/make_data.py, AliSim). ngen scaled down from the Skill's 10,000,000 as recorded per file.
set -u
source /f/OpenScience/audit-envs/molecular-phylogenetics-analyst/env.sh
MB=/f/OpenScience/audit-envs/molecular-phylogenetics-analyst/tools/bin/mb.exe
PY=/f/OpenScience/audit-envs/molecular-phylogenetics-analyst/Scripts/python.exe
B=/f/OpenScience/audits/bio-phylo-bayesian-inference; R=$B/runs_v2; D=$B/data; OLD=$B/runs
SK=/f/OpenScience/external/mrsonord2240__bioSkills/phylogenetics/bayesian-inference
DIAG="$PY $OLD/setup/mbdiag.py"; RF="$PY $OLD/setup/rf_truth.py"
RRUN="pwsh -NoProfile -File /f/OpenScience/audit-envs/molecular-phylogenetics-analyst/rrun.ps1 -Script"
mbrun() { local t0=$(date +%s); timeout 7200 $MB "$1" > "${1%.nex}.stdout" 2>&1; echo "mb $1 exit $? ($(( $(date +%s) - t0 )) s)"; }

block() { # $1 filename  $2 ngen  $3 extra mcmc opts ; fixed Skill block, ngen/samplefreq/printfreq scaled
cat <<EOF
    set seed=12345 swapseed=67890;                      [ record seeds for reproducibility ]
    lset nst=6 rates=invgamma;                          [ GTR+I+G; nst=mixed = rjMCMC model averaging ]
    prset brlenspr=unconstrained:gammadir(1,0.1,1,1);   [ compound Dirichlet, NOT exp(10): avoids tree-length inflation ]
    mcmc ngen=$2 nruns=2 nchains=4 temp=0.1 $3
         samplefreq=100 printfreq=10000 diagnfreq=5000
         stoprule=no filename=$1;                       [ run the full ngen; do NOT auto-halt on ASDSF ]
    sump burninfrac=0.25 relburnin=yes filename=$1;
    sumt burninfrac=0.25 relburnin=yes filename=$1;
EOF
}

echo "######## IN1 canonical d12: fixed block 100k, then 'mcmc append=yes ngen=<new total>' to 300k"
mkdir -p $R/in1 && cd $R/in1 && cp $D/d12.nex .
{ echo "#NEXUS"; echo "[ auditor: Skill block, ngen 10000000->100000, samplefreq 1000->100 ]"; echo "set autoclose=yes nowarn=yes;"; echo "execute d12.nex;"; echo "begin mrbayes;"; block in1 100000 ""; echo "end;"; } > in1a.nex
mbrun in1a.nex; $DIAG in1 > diag_100k.txt; grep -E "WORST|GATE" diag_100k.txt; grep -E "samples of which" in1a.stdout | head -1
{ echo "#NEXUS"; echo "[ Skill extension: mcmc append=yes ngen=<new total> ]"; echo "set autoclose=yes nowarn=yes;"; echo "execute d12.nex;"; echo "begin mrbayes;";
  echo "    set seed=12345 swapseed=67890;"; echo "    lset nst=6 rates=invgamma;"; echo "    prset brlenspr=unconstrained:gammadir(1,0.1,1,1);";
  echo "    mcmc append=yes ngen=300000 nruns=2 nchains=4 temp=0.1 samplefreq=100 printfreq=10000 diagnfreq=5000 stoprule=no filename=in1;";
  echo "    sump burninfrac=0.25 relburnin=yes filename=in1;"; echo "    sumt burninfrac=0.25 relburnin=yes filename=in1;"; echo "end;"; } > in1b.nex
mbrun in1b.nex; $DIAG in1 > diag_300k.txt; cat diag_300k.txt | grep -E "WORST|GATE|ASDSF|lstat"; grep -E "samples of which|Continuing|append" in1b.stdout | head -3
$RF in1.con.tre $D/d12_true.nwk
cat > rwty.R <<'EOF'
suppressMessages({library(rwty)})
setwd("F:/OpenScience/audits/bio-phylo-bayesian-inference/runs_v2/in1")
run1 <- load.trees("in1.run1.t", type = "nexus", format = "mb")
run2 <- load.trees("in1.run2.t", type = "nexus", format = "mb")
cat("trees per run:", length(run1$trees), length(run2$trees), " burnin(trees):", round(0.25 * length(run1$trees)), "\n")
set.seed(1)
res <- tryCatch(analyze.rwty(list(run1 = run1, run2 = run2), burnin = round(0.25 * length(run1$trees))),  # Skill verbatim
                error = function(e) {cat("analyze.rwty ERROR:", conditionMessage(e), "\n"); NULL})
cat("analyze.rwty returned:", !is.null(res), "\n")
ts <- makeplot.treespace(list(run1 = run1, run2 = run2), burnin = round(0.25 * length(run1$trees)), n.points = 100)
png("treespace.png", width = 900, height = 450); print(ts$treespace.heatmap); dev.off()
cat("approx topological ESS:\n"); print(topological.approx.ess(run1, burnin = round(0.25 * length(run1$trees))))
EOF
$RRUN $R/in1/rwty.R > rwty.log 2>&1; echo "rwty exit $?"; grep -E "trees per run|returned|ERROR|operating|ess" rwty.log | head -8

echo "######## IN2 under-run user files (regression): example + sump + rwty with the fixed burnin expression"
mkdir -p $R/in2 && cd $R/in2 && cp $OLD/in2/user.run?.[pt] $OLD/in2/many60.nex $OLD/in2/agent_diag.nex .
mbrun agent_diag.nex; $DIAG user | grep -E "WORST|GATE|ASDSF"
$PY $SK/examples/bayesian_convergence.py user.run1.p user.run2.p 0.25 > example.txt 2>&1; echo "example exit $?"; tail -4 example.txt
sed -e 's#runs_v2/in1#runs_v2/in2#; s#in1.run#user.run#g' $R/in1/rwty.R > rwty.R
$RRUN $R/in2/rwty.R > rwty.log 2>&1; echo "rwty exit $?"; grep -E "trees per run|returned|ERROR" rwty.log

echo "######## IN3 star8 near-polytomy: fixed block 300k"
mkdir -p $R/in3 && cd $R/in3 && cp $D/star8.nex .
{ echo "#NEXUS"; echo "set autoclose=yes nowarn=yes;"; echo "execute star8.nex;"; echo "begin mrbayes;"; block in3 300000 ""; echo "end;"; } > in3.nex
mbrun in3.nex; $DIAG in3 | grep -E "WORST|GATE|ASDSF"; $PY $OLD/setup/split_pp.py in3 E,F,G,H; $RF in3.con.tre $D/star8_true.nwk

echo "######## IN4 stepping-stone GTR+G vs JC (Skill ss line, ngen 1000000->250000)"
mkdir -p $R/in4 && cd $R/in4 && cp $D/d12.nex .
for m in gtrg jc; do
  if [ $m = gtrg ]; then L="lset nst=6 rates=gamma; prset brlenspr=unconstrained:gammadir(1,0.1,1,1);"; else L="lset nst=1 rates=equal; prset statefreqpr=fixed(equal) brlenspr=unconstrained:gammadir(1,0.1,1,1);"; fi
  printf "#NEXUS\nset autoclose=yes nowarn=yes;\nexecute d12.nex;\nbegin mrbayes;\n    set seed=12345 swapseed=67890;\n    $L\n    ss ngen=250000 nsteps=50 samplefreq=100 diagnfreq=1000 printfreq=25000 filename=ss_$m;\nend;\n" > ss_$m.nex
  mbrun ss_$m.nex; grep -a -E "steps will be used|samples\) within each step|Mean:|Run +[12]|Marginal" ss_$m.stdout | head -8
done

echo "######## IN5 prior-only check (Skill verbatim 'mcmc data=no ngen=... filename=prioronly')"
mkdir -p $R/in5 && cd $R/in5 && cp $D/many60.nex .
for p in gdir exp10; do
  if [ $p = gdir ]; then P="unconstrained:gammadir(1,0.1,1,1)"; else P="unconstrained:exp(10)"; fi
  printf "#NEXUS\nset autoclose=yes nowarn=yes;\nexecute many60.nex;\nbegin mrbayes;\n    set seed=12345 swapseed=67890;\n    lset nst=2 rates=gamma;\n    prset brlenspr=$P;\n    mcmc data=no ngen=200000 filename=prioronly_$p;\n    sump filename=prioronly_$p;\nend;\n" > prior_$p.nex
  mbrun prior_$p.nex; grep -a -E "Running without data|TL" prior_$p.stdout | head -3
  echo "data run (pre-fix audit, same model/prior, 200k gens):"; $DIAG $OLD/in5/$p | grep -E " TL "
done

echo "######## IN7 HME adversarial (regression): 2 replicate MCMCs per model, sump HME"
mkdir -p $R/in7 && cd $R/in7 && cp $D/d12.nex .
for m in gtrg jc; do for rep in a b; do
  if [ $m = gtrg ]; then L="lset nst=6 rates=gamma; prset brlenspr=unconstrained:gammadir(1,0.1,1,1);"; else L="lset nst=1 rates=equal; prset statefreqpr=fixed(equal) brlenspr=unconstrained:gammadir(1,0.1,1,1);"; fi
  S=$([ $rep = a ] && echo 7101 || echo 7201)
  printf "#NEXUS\nset autoclose=yes nowarn=yes;\nexecute d12.nex;\nbegin mrbayes;\n    set seed=$S swapseed=$((S+1));\n    $L\n    mcmc ngen=100000 nruns=2 nchains=4 temp=0.1 samplefreq=100 printfreq=20000 diagnfreq=10000 stoprule=no filename=mc_${m}_$rep;\n    sump burninfrac=0.25 relburnin=yes filename=mc_${m}_$rep;\nend;\n" > mc_${m}_$rep.nex
  mbrun mc_${m}_$rep.nex; grep -a -E "harmonic|TOTAL" mc_${m}_$rep.stdout | head -3
done; done

echo "######## IN8 NEW: nst=mixed rjMCMC model averaging on d12 (200k)"
mkdir -p $R/in8 && cd $R/in8 && cp $D/d12.nex .
printf "#NEXUS\nset autoclose=yes nowarn=yes;\nexecute d12.nex;\nbegin mrbayes;\n    set seed=12345 swapseed=67890;\n    lset nst=mixed rates=gamma;\n    prset brlenspr=unconstrained:gammadir(1,0.1,1,1);\n    mcmc ngen=200000 nruns=2 nchains=4 temp=0.1 samplefreq=100 printfreq=20000 diagnfreq=5000 stoprule=no filename=mixed;\n    sump burninfrac=0.25 relburnin=yes filename=mixed;\n    sumt burninfrac=0.25 relburnin=yes filename=mixed;\nend;\n" > mixed.nex
mbrun mixed.nex; $DIAG mixed | grep -E "WORST|GATE|ASDSF"; grep -a -i -A14 "model probabilities\|gtrsubmodel" mixed.stdout | head -30; $RF mixed.con.tre $D/d12_true.nwk

echo "######## IN9 NEW: single run (nruns=1) and 'prove convergence'"
mkdir -p $R/in9 && cd $R/in9 && cp $D/d12.nex .
printf "#NEXUS\nset autoclose=yes nowarn=yes;\nexecute d12.nex;\nbegin mrbayes;\n    set seed=12345 swapseed=67890;\n    lset nst=6 rates=gamma;\n    prset brlenspr=unconstrained:gammadir(1,0.1,1,1);\n    mcmc ngen=100000 nruns=1 nchains=4 temp=0.1 samplefreq=100 printfreq=20000 stoprule=no filename=single;\n    sump burninfrac=0.25 relburnin=yes filename=single;\n    sumt burninfrac=0.25 relburnin=yes filename=single;\nend;\n" > single.nex
mbrun single.nex; grep -a -E "PSRF|ESS|standard deviation" single.stdout | head -5; $DIAG single | grep -E "WORST|GATE|pstat" | head -3
echo "-- example with one .p file"; $PY $SK/examples/bayesian_convergence.py single.p > example_one.txt 2>&1; echo "exit $?"; head -3 example_one.txt

echo "######## EXAMPLE self-test"
cd $R && $PY -m py_compile $SK/examples/bayesian_convergence.py && echo "py_compile OK"; $PY $SK/examples/bayesian_convergence.py > selftest.txt 2>&1; echo "selftest exit $?"; head -4 selftest.txt; grep -E "FAIL|OK" selftest.txt | head -5
echo ALL DONE
