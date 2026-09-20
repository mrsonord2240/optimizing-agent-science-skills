#!/bin/bash
# Input 5b: Shiba 0.8.2 on the SYNTHETIC 120-gene sim (A vs B truth, A vs C null), strand: XS (BAMs carry XS tags).
export PYTHONDONTWRITEBYTECODE=1
R=/mnt/openscience/audits/bio-differential-splicing/run
S=$R/data/sim
for cmp in AvB AvC; do
  g2=${cmp: -1}
  W=$R/out/in5b_$cmp; rm -rf $W; mkdir -p $W; cd $W
  {
    printf 'sample\tbam\tgroup\ttechnology\n'
    for i in 1 2 3; do printf 'A%s\t%s/A%s.bam\tRef\tshort\n' $i $S $i; done
    for i in 1 2 3; do printf '%s%s\t%s/%s%s.bam\tAlt\tshort\n' $g2 $i $S $g2 $i; done
  } > exp.tsv
  cat > config.yaml <<CFG
workdir: $W/out
gtf: $S/sim_shiba.gtf
experiment_table: $W/exp.tsv
unannotated: False
minimum_anchor_length: 6
minimum_intron_length: 50
maximum_intron_length: 500000
strand: XS
only_psi: False
only_psi_group: False
fdr: 0.05
delta_psi: 0.1
reference_group: Ref
alternative_group: Alt
minimum_reads: 10
individual_psi: True
ttest: False
excel: False
CFG
  echo "=== Shiba $cmp"
  micromamba run -n as-shiba shiba.py -p 4 --mame config.yaml > shiba.log 2>&1; echo "rc=$?"
  tail -5 shiba.log | cut -c1-250
  ls out/results 2>/dev/null | head
  for t in SE; do f=out/results/PSI_$t.txt; [ -f $f ] && echo "$t events: $(($(wc -l < $f)-1))"; head -2 $f | cut -c1-400; done
done
echo "=== SKILL.md snakemake invocation, dry-run with snakemake 9.27 (--use-singularity)"
cd $R/out/in5b_AvB
SMK=/home/sci/micromamba/envs/as-shiba/share/shiba-0.8.2-0/snakeshiba.smk
micromamba run -n as-shiba snakemake -n -s $SMK --configfile config.yaml --cores 8 --use-singularity --singularity-args "--bind $HOME:$HOME" 2>&1 | tail -6 | cut -c1-250
