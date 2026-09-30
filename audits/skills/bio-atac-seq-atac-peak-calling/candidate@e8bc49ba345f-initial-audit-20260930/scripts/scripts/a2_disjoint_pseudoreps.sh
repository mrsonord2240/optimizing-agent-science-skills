#!/bin/bash
# ENCODE-style disjoint pseudoreps (samtools -s + -U complement) and Np/N1/N2 vs the Skill script's single-rep overlapping halves.
source /mnt/openscience/audit-envs/bio-atac-seq-atac-peak-calling/wsl_env.sh
D=$ATACDATA/encode; R=$APC/run/disjoint; rm -rf $R; mkdir -p $R; cd $R
R1=$D/GM12878_rep1_filtered.chr1_1-30000000.bam; R2=$D/GM12878_rep2_filtered.chr1_1-30000000.bam
call() { macs2 callpeak -t $1 -f BAM -g 2.7e9 -n $2 --outdir . --nomodel --shift -75 --extsize 150 --keep-dup all -p 0.01 > $2.log 2>&1; sort -k8,8nr ${2}_peaks.narrowPeak > $2.s.np; }
idrn() { idr --samples $1 $2 --input-file-type narrowPeak --rank p.value --output-file $3.idr --idr-threshold $4 --log-output-file $3.log > /dev/null 2>&1; awk -v t=$5 '$5>=t' $3.idr | wc -l; }
samtools view -b -s 1.5 -U r1b.bam -o r1a.bam $R1
samtools view -b -s 1.5 -U r2b.bam -o r2a.bam $R2
samtools merge -f pool.bam $R1 $R2
samtools view -b -s 1.5 -U poolb.bam -o poola.bam pool.bam
echo shared_r1_halves=$(comm -12 <(samtools view r1a.bam|cut -f1|sort -u) <(samtools view r1b.bam|cut -f1|sort -u) | wc -l)
for n in r1a r1b r2a r2b poola poolb; do call $n.bam $n; done
p=$APC/run/script_default
N1=$(idrn r1a.s.np r1b.s.np r1 0.05 540); N2=$(idrn r2a.s.np r2b.s.np r2 0.05 540); Np=$(idrn poola.s.np poolb.s.np pool 0.05 540)
N1_10=$(idrn r1a.s.np r1b.s.np r1_10 0.10 415)
Nt=$(awk '$5>=540' $p/idr/true_reps.idr | wc -l)
echo "Nt=$Nt N1=$N1 N2=$N2 Np=$Np  N1@0.10=$N1_10"
python - <<P
Nt,N1,N2,Np=$Nt,$N1,$N2,$Np
r=lambda a,b:max(a,b)/max(1,min(a,b))
print("rescue=%.3f self=%.3f"%(r(Np,Nt),r(N1,N2)))
P
