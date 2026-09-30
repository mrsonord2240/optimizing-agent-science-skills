#!/bin/bash
# Re-audit: run_tobias.sh unmodified in the FRESH ra-footprint env (usage-guide recipe).
# A full+CTCF | B no-CTCF default (expect rc 3) | C no-CTCF + ALLOW_NO_CTCF=1 (rc 0) | D missing input (rc 2)
# E spaces in every path | N negative control: TOBIAS shim makes ATACorrect emit corrected==uncorrected (bias correction absent)
export MAMBA_ROOT_PREFIX=/home/sci/micromamba PYTHONDONTWRITEBYTECODE=1
export PATH=/home/sci/micromamba/envs/ra-footprint/bin:$PATH
SKILL=/mnt/openscience/wt/atac-footprinting/skills/bio-atac-seq-footprinting
I=/mnt/openscience/audit-envs/bio-atac-seq-footprinting/run_tobias
D=/mnt/openscience/audit-envs/atac-seq/public-data
W=/mnt/openscience/audit-envs/bio-atac-seq-footprinting/reaudit-run/rt; rm -rf $W; mkdir -p $W; cd $W
L=/mnt/openscience/audits/bio-atac-seq-footprinting/reaudit-run/logs
which TOBIAS; TOBIAS --version 2>&1 | head -1; samtools --version | head -1
awk 'BEGIN{keep=0} /^>/{n=$2; keep=(n=="GATA1"||n=="IRF4"||n=="EBF1")} keep{print}' $I/motifs_subset.pfm > motifs_noctcf.pfm
grep -c '^>' $I/motifs_subset.pfm motifs_noctcf.pfm
# spaces in every path
mkdir "in put"; for f in cond1.bam cond1.bam.bai cond2.bam cond2.bam.bai peaks.bed hg38-blacklist.v2.bed motifs_subset.pfm; do cp $I/$f "in put/$f" 2>/dev/null; done
cp $D/reference/hg38.chr1.fa "in put/hg 38.fa"; cp $D/reference/hg38.chr1.fa.fai "in put/hg 38.fa.fai" 2>/dev/null
# shim: real ATACorrect, then corrected := uncorrected
mkdir shim; cat > shim/TOBIAS <<'S'
#!/bin/bash
REAL=$(PATH=${PATH#*shim:} which TOBIAS)
"$REAL" "$@"; rc=$?
if [ "$1" = ATACorrect ] && [ $rc -eq 0 ]; then
  out=""; for ((i=1;i<=$#;i++)); do [ "${!i}" = "--outdir" ] && { j=$((i+1)); out=${!j}; }; done
  for u in "$out"/*_uncorrected.bw; do cp "$u" "${u%_uncorrected.bw}_corrected.bw"; done
fi
exit $rc
S
chmod +x shim/TOBIAS
run() { n=$1; shift; ( "$@" > $L/r2_$n.log 2>&1; echo "$n rc=$?" | tee -a $L/r2_$n.log ) & }
run A bash $SKILL/scripts/run_tobias.sh $I/cond1.bam $I/cond2.bam $I/peaks.bed $D/reference/hg38.chr1.fa $I/hg38-blacklist.v2.bed $I/motifs_subset.pfm $W/A 4
run B bash $SKILL/scripts/run_tobias.sh $I/cond1.bam $I/cond2.bam $I/peaks.bed $D/reference/hg38.chr1.fa $I/hg38-blacklist.v2.bed $W/motifs_noctcf.pfm $W/B 4
run C env ALLOW_NO_CTCF=1 bash $SKILL/scripts/run_tobias.sh $I/cond1.bam $I/cond2.bam $I/peaks.bed $D/reference/hg38.chr1.fa $I/hg38-blacklist.v2.bed $W/motifs_noctcf.pfm $W/C 4
run D bash $SKILL/scripts/run_tobias.sh $I/cond1.bam $I/cond2.bam $I/peaks.bed $D/reference/hg38.chr1.fa $I/hg38-blacklist.v2.bed $W/nonexistent.pfm $W/Dout 4
run E bash $SKILL/scripts/run_tobias.sh "$W/in put/cond1.bam" "$W/in put/cond2.bam" "$W/in put/peaks.bed" "$W/in put/hg 38.fa" "$W/in put/hg38-blacklist.v2.bed" "$W/in put/motifs_subset.pfm" "$W/out dir" 4
run N env PATH=$W/shim:$PATH bash $SKILL/scripts/run_tobias.sh $I/cond1.bam $I/cond2.bam $I/peaks.bed $D/reference/hg38.chr1.fa $I/hg38-blacklist.v2.bed $I/motifs_subset.pfm $W/N 4
wait; echo alldone
