#!/bin/bash
# Input 1: rMATS-turbo 3v3 on the PLANTED exon-skipping set (synthetic; truth: IncLevelDifference +0.587, G1 > G2)
# (a) Skill's SKILL.md command verbatim (paired/150/fr-firststrand) on single-end unstranded data
# (b) same command adapted to the data (-t single --readLength 50 --libType fr-unstranded)
export PYTHONDONTWRITEBYTECODE=1
AS=/mnt/openscience/audit-envs/alternative-splicing
P=$AS/public-data/planted
R=/mnt/openscience/audits/bio-differential-splicing/run
O=$R/out/in1
rm -rf $O; mkdir -p $O; cd $O
echo "=== (a) SKILL.md command verbatim"
mkdir -p a/tmp a/out
micromamba run -n as-core rmats.py --b1 $P/b1.txt --b2 $P/b2.txt --gtf $P/planted.gtf -t paired --readLength 150 --variable-read-length --libType fr-firststrand --nthread 4 --od a/out --tmp a/tmp --novelSS --cstat 0.05 > a.log 2>&1
echo "rc=$?"; tail -8 a.log | cut -c1-220
echo "SE.MATS.JC.txt rows (a): $(($(wc -l < a/out/SE.MATS.JC.txt 2>/dev/null)-1))"
cat a/out/SE.MATS.JC.txt 2>/dev/null | cut -f1-6,13-24
echo "=== (b) adapted: single-end, 50nt, unstranded, --novelSS --cstat 0.05"
mkdir -p b/tmp b/out
micromamba run -n as-core rmats.py --b1 $P/b1.txt --b2 $P/b2.txt --gtf $P/planted.gtf -t single --readLength 50 --libType fr-unstranded --nthread 4 --od b/out --tmp b/tmp --novelSS --cstat 0.05 > b.log 2>&1
echo "rc=$?"; tail -4 b.log | cut -c1-220
echo "SE.MATS.JC.txt (b):"
head -1 b/out/SE.MATS.JC.txt | tr '\t' '\n' | cat -n | tr '\n' ' '; echo
cat b/out/SE.MATS.JC.txt
echo "other event files rows:"; for e in A3SS A5SS MXE RI; do echo "$e $(($(wc -l < b/out/$e.MATS.JC.txt)-1))"; done
echo "=== (c) default --cstat (0.0001) for comparison"
mkdir -p c/tmp c/out
micromamba run -n as-core rmats.py --b1 $P/b1.txt --b2 $P/b2.txt --gtf $P/planted.gtf -t single --readLength 50 --nthread 4 --od c/out --tmp c/tmp > c.log 2>&1
echo "rc=$?"; cut -f1-6,19-24 c/out/SE.MATS.JC.txt
echo "=== (d) swapped b1/b2: sign check"
mkdir -p d/tmp d/out
micromamba run -n as-core rmats.py --b1 $P/b2.txt --b2 $P/b1.txt --gtf $P/planted.gtf -t single --readLength 50 --nthread 4 --od d/out --tmp d/tmp > d.log 2>&1
echo "rc=$?"; cut -f1-6,19-24 d/out/SE.MATS.JC.txt
