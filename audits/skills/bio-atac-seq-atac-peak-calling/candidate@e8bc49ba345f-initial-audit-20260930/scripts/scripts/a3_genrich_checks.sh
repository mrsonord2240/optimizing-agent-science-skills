#!/bin/bash
# Genrich: coordinate-sorted BAM input (Skill never mentions name-sort), and q-cutoff advice "-q 0.01 for parity" from reconciliation table.
source /mnt/openscience/audit-envs/bio-atac-seq-atac-peak-calling/wsl_env.sh
R=$APC/run/genrich_audit; rm -rf $R; mkdir -p $R; cd $R
D=$ATACDATA/encode; E1=$D/GM12878_rep1_filtered.chr1_1-30000000.bam; C=$APC/run/callers
Genrich --version 2>&1 | head -1
echo "== coord-sorted input"; Genrich -t $E1 -o cs.np -j -e chrM -v > cs.log 2>&1; echo rc=$?; tail -5 cs.log; ls -la cs.np 2>&1; wc -l cs.np 2>&1
echo "== name-sorted joint q sweep (Skill: MACS fewer than Genrich -> rerun -q 0.01 for parity)"
for q in 0.05 0.01 0.001; do Genrich -t $C/e1.nsort.bam,$C/e2.nsort.bam -o q$q.np -j -e chrM -q $q > q$q.log 2>&1; echo q=$q rc=$? peaks=$(wc -l < q$q.np); done
echo "MACS3 rep1 peaks: $(wc -l < $C/gm_rep1_macs3_peaks.narrowPeak)"
