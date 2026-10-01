#!/bin/bash
# Re-audit: candidate scripts/run_tobias.sh, unmodified, on real ENCODE GM12878 (cond1) vs K562 (cond2) ATAC, chr1:1-30 Mb.
#  A  normal run                                           -> expect rc 0, r(corrected, expected) <= 0.2 both conditions
#  N  shim: _uncorrected.bw copied over _corrected.bw      -> expect rc 4 (bias correction absent)
#  S  both BAMs subsampled to 20% (samtools view -s)        -> other uncorrected tracks, lower depth: does the check still pass?
#  SN S + shim                                             -> does the check still catch absent correction at low depth?
#  F  both BAMs NFR-filtered with the SKILL.md awk filter  -> different fragment population
#  FN F + shim
#  X  motif set without CTCF                               -> expect rc 3 (regression)
#  M  missing BAM                                          -> expect rc 2, no outdir
export MAMBA_ROOT_PREFIX=/home/sci/micromamba PYTHONDONTWRITEBYTECODE=1
export PATH=/home/sci/micromamba/envs/bio-atac-seq-footprinting/bin:$PATH
Q=bio-atac-seq-footprinting; SKILL=/mnt/openscience/wt/atac-footprinting/skills/$Q
I=/mnt/openscience/audit-envs/$Q/run_tobias; FA=/mnt/openscience/audit-envs/atac-seq/public-data/reference/hg38.chr1.fa
W=/mnt/openscience/audit-envs/$Q/reaudit-final/rt; rm -rf $W; mkdir -p $W; cd $W
L=/mnt/openscience/audits/$Q/reaudit-final-20260930/logs
TOBIAS --version 2>&1 | tail -1; samtools --version | head -1
# derived inputs
for c in cond1 cond2; do
  samtools view -b -s 42.2 -o sub_$c.bam $I/$c.bam && samtools index sub_$c.bam
  samtools view -h $I/$c.bam | \
    awk 'substr($0,1,1)=="@" || ($9 > 0 && $9 < 100) || ($9 < 0 && $9 > -100)' | \
    samtools view -b > nfr_$c.bam
  samtools index nfr_$c.bam
  echo "$c reads: full $(samtools view -c $I/$c.bam) sub20 $(samtools view -c sub_$c.bam) nfr $(samtools view -c nfr_$c.bam)"
done
awk 'BEGIN{keep=0} /^>/{keep=($2!="CTCF")} keep{print}' $I/motifs_subset.pfm > motifs_noctcf.pfm; grep -c '>' motifs_noctcf.pfm
mkdir shim; cat > shim/TOBIAS <<'S'
#!/bin/bash
# after a successful ATACorrect, overwrite each _corrected.bw with its _uncorrected.bw (bias correction absent)
REAL=/home/sci/micromamba/envs/bio-atac-seq-footprinting/bin/TOBIAS
"$REAL" "$@"; rc=$?
if [ "$1" = ATACorrect ] && [ $rc -eq 0 ]; then
  out=""; for ((i=1;i<=$#;i++)); do [ "${!i}" = "--outdir" ] && { j=$((i+1)); out=${!j}; }; done
  for u in "$out"/*_uncorrected.bw; do cp "$u" "${u%_uncorrected.bw}_corrected.bw"; echo "SHIM: $u -> corrected" >&2; done
fi
exit $rc
S
chmod +x shim/TOBIAS
run() { n=$1; shift; ( START=$(date +%s); "$@" > $L/r3_$n.log 2>&1; rc=$?; echo "$n rc=$rc $(( $(date +%s)-START ))s" | tee -a $L/r3_$n.log ) & }
T="bash $SKILL/scripts/run_tobias.sh"
run A  $T $I/cond1.bam $I/cond2.bam $I/peaks.bed $FA $I/hg38-blacklist.v2.bed $I/motifs_subset.pfm $W/A 3
run N  env PATH=$W/shim:$PATH $T $I/cond1.bam $I/cond2.bam $I/peaks.bed $FA $I/hg38-blacklist.v2.bed $I/motifs_subset.pfm $W/N 3
run S  $T sub_cond1.bam sub_cond2.bam $I/peaks.bed $FA $I/hg38-blacklist.v2.bed $I/motifs_subset.pfm $W/S 3
run SN env PATH=$W/shim:$PATH $T sub_cond1.bam sub_cond2.bam $I/peaks.bed $FA $I/hg38-blacklist.v2.bed $I/motifs_subset.pfm $W/SN 3
run F  $T nfr_cond1.bam nfr_cond2.bam $I/peaks.bed $FA $I/hg38-blacklist.v2.bed $I/motifs_subset.pfm $W/F 3
run FN env PATH=$W/shim:$PATH $T nfr_cond1.bam nfr_cond2.bam $I/peaks.bed $FA $I/hg38-blacklist.v2.bed $I/motifs_subset.pfm $W/FN 3
run X  $T $I/cond1.bam $I/cond2.bam $I/peaks.bed $FA $I/hg38-blacklist.v2.bed motifs_noctcf.pfm $W/X 3
run M  $T $I/nope.bam $I/cond2.bam $I/peaks.bed $FA $I/hg38-blacklist.v2.bed $I/motifs_subset.pfm $W/M 3
wait
[ -e $W/M ] && echo "M outdir created" || echo "M outdir not created"
for n in A N S SN F FN X M; do tail -1 $L/r3_$n.log; grep -h "^Bias check\|^ERROR\|^WARNING" $L/r3_$n.log; done
echo alldone
