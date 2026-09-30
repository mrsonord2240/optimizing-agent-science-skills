source /mnt/openscience/audits/bio-atac-seq-atac-peak-calling/reaudit-run/scripts/env.sh
G=$R/guards; rm -rf $G; mkdir -p $G; cd $G
g() { label=$1; shift; out=$("$@" 2>&1); rc=$?; echo "GUARD $label rc=$rc :: $(echo "$out" | tail -1)"; ls $G/o_* >/dev/null 2>&1 && echo "  (outdir created: $(ls -d $G/o_* | tr '\n' ' '))"; rm -rf $G/o_*; }
g missing_genome bash $S $E1 $E2 "" $BL $G/o_a
g missing_arg4 bash $S $E1 $E2 2.8e9
g missing_bam bash $S $E1 $G/nope.bam 2.8e9 $BL $G/o_b
g missing_blacklist bash $S $E1 $E2 2.8e9 $G/nope.bed $G/o_c
cp $E1 $G/noidx.bam
g unindexed bash $S $E1 $G/noidx.bam 2.8e9 $BL $G/o_d
samtools sort -n -o $G/nsort.bam $E2; cp $G/nsort.bam $G/nsort.bam.tmp; cp $E2.bai $G/nsort.bam.bai 2>/dev/null || cp ${E2%.bam}.bai $G/nsort.bam.bai
g unsorted bash $S $E1 $G/nsort.bam 2.8e9 $BL $G/o_e
g missing_tool env IDR=/nonexistent/idr bash $S $E1 $E2 2.8e9 $BL $G/o_f
g bad_chromsizes bash $S $E1 $E2 2.8e9 $BL $G/o_g $G/nope.sizes
# chrM: synthetic BAM with 3 chrM reads (planted) and real header @SQ chrM
samtools view -h $E1 chr1:1-200000 > a.sam
samtools view -H a.sam | head -3
grep -c '^@SQ.SN:chrM' a.sam || true
echo "source idxstats chrM:"; samtools idxstats $E1 | awk '$1=="chrM"'
(cat a.sam; for i in 1 2 3; do printf "mm$i\t0\tchrM\t$((100+i))\t60\t50M\t*\t0\t0\t%s\t%s\n" $(printf 'A%.0s' $(seq 50)) $(printf 'I%.0s' $(seq 50)); done) | samtools sort -o m.bam -; samtools index m.bam
samtools idxstats m.bam | awk '$1=="chrM"'
g chrM_reads bash $S m.bam $E2 2.8e9 $BL $G/o_h
# recipe from usage-guide on a chrM-bearing BAM with a chr1 read whose mate maps chrM (paired)
cat > pair.sam <<'S'
@HD	VN:1.6	SO:coordinate
@SQ	SN:chr1	LN:1000
@SQ	SN:chrM	LN:1000
p1	97	chr1	100	60	10M	chrM	200	0	ACGTACGTAC	IIIIIIIIII
p2	65	chr1	300	60	10M	chr1	400	200	ACGTACGTAC	IIIIIIIIII
p2	129	chr1	400	60	10M	chr1	300	-200	ACGTACGTAC	IIIIIIIIII
p1	145	chrM	200	60	10M	chr1	100	0	ACGTACGTAC	IIIIIIIIII
S
samtools sort -o pair.bam pair.sam; samtools index pair.bam
echo "recipe usage-guide (idxstats contig selection):"
samtools idxstats pair.bam | cut -f1 | grep -v -e '^chrM$' -e '^\*$' | xargs samtools view -b -o noM.bam pair.bam; echo rc=$?
samtools view noM.bam | cut -f1-4,7; echo "header SQ:"; samtools view -H noM.bam | grep -c '^@SQ'
echo "old recipe (grep -v chrM on SAM text) for contrast:"; samtools view -h pair.bam | grep -v chrM | samtools view -b 2>&1 | samtools view -c 2>&1 | head -2
