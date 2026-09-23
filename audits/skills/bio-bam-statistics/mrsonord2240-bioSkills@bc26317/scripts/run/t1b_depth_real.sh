#!/bin/bash
# INPUT 1 part B (REAL human BAM): every mean-depth / >=Nx recipe in the fixed Skill vs truth from alignment blocks (no pileup engine)
export LC_ALL=C PYTHONIOENCODING=utf-8
R=/mnt/openscience/audits/bio-bam-statistics/run; D=/mnt/openscience/audit-envs/alignment-files/public-data
H=$D/human/test.paired_end.sorted.bam; cd $R/work
python - <<'PY'
import sys; sys.path.insert(0,'/mnt/openscience/audits/bio-bam-statistics/run')
import depth_truth as T, truth
H='/mnt/openscience/audit-envs/alignment-files/public-data/human/test.paired_end.sorted.bam'
d=T.truth.depth_arrays(H,'chr22',40001); s=T.summarize(d)
print('TRUTH default (mates twice): mean %.4f  >=10x %.4f%%  >=20x %.4f%%  covered %d (%.3f%%) max %d'%(s['mean'],s['ge10'],s['ge20'],s['covered'],s['pct_cov'],s['mx']))
d1=T.truth.depth_arrays(H,'chr22',40001,no_overlap=True); s1=T.summarize(d1)
print('TRUTH mates once          : mean %.4f  >=10x %.4f%%  >=20x %.4f%%'%(s1['mean'],s1['ge10'],s1['ge20']))
print('TRUTH mean over covered positions only (the OLD wrong denominator): %.3f'%(d.sum()/(d>0).sum()))
PY
echo "=== block 017 (Mean Depth and Breadth, verbatim, -aa)"; bash $R/rb.sh 17 $H
echo "=== block 017 with region (as the comment says: -a -r region in the same pipe)"
sed 's#samtools depth -aa input.bam#samtools depth -a -r chr22:1-40001 input.bam#; s#input\.bam#'$H'#' $R/blocks/017_bash.sh | bash
echo "=== block 014 warning: raw depth average (must reproduce the 568x claim)"; samtools depth $H | awk '{s+=$3;n++} END{print "raw depth avg over covered positions:", s/n}'
echo "=== samtools coverage meandepth / mosdepth default / --fast-mode / --by thresholds (block 020)"
samtools coverage $H | cut -f1-7
mosdepth -t 2 mA $H; cat mA.mosdepth.summary.txt | tr '\t' ' '
mosdepth -t 2 --fast-mode mB $H; grep total mB.mosdepth.summary.txt | tr '\t' ' '
printf 'chr22\t0\t40001\n' > all.bed
mosdepth -t 2 --by all.bed --thresholds 1,10,20,30,100 --no-per-base mC $H; zcat mC.thresholds.bed.gz; zcat mC.regions.bed.gz
echo "=== overlap table (SKILL 'What Each Tool Counts'): mean depth per tool"
mm() { awk '{s+=$3;n++} END{printf "%.2f\n", s/40001}'; }
echo -n "depth -a default: "; samtools depth -a $H | mm
echo -n "depth -a -s     : "; samtools depth -a -s $H | mm
echo -n "mpileup default (-Q13): "; samtools mpileup -a -d 1000000 -f $D/human/genome.fasta $H 2>/dev/null | mm_dummy=1 awk '{s+=$4;n++} END{printf "%.2f\n", s/40001}'
echo -n "mpileup -x      : "; samtools mpileup -a -x -d 1000000 -f $D/human/genome.fasta $H 2>/dev/null | awk '{s+=$4;n++} END{printf "%.2f\n", s/40001}'
echo -n "mpileup -Q 0    : "; samtools mpileup -a -Q 0 -d 1000000 -f $D/human/genome.fasta $H 2>/dev/null | awk '{s+=$4;n++} END{printf "%.2f\n", s/40001}'
echo -n "bcftools mpileup default DP sum/40001 (only positions printed: use -a DP): "; bcftools mpileup -a FORMAT/DP -d 1000000 -f $D/human/genome.fasta $H 2>/dev/null | bcftools query -f '[%DP]\n' | awk '{s+=$1} END{printf "%.2f\n", s/40001}'
echo -n "bcftools mpileup -x  : "; bcftools mpileup -x -a FORMAT/DP -d 1000000 -f $D/human/genome.fasta $H 2>/dev/null | bcftools query -f '[%DP]\n' | awk '{s+=$1} END{printf "%.2f\n", s/40001}'
echo "=== block 029 region_depth_stats verbatim (region substituted) + comparison to truth and to samtools depth -a"
python - <<'PY'
import sys, subprocess; sys.path.insert(0,'/mnt/openscience/audits/bio-bam-statistics/run')
import depth_truth as T
H='/mnt/openscience/audit-envs/alignment-files/public-data/human/test.paired_end.sorted.bam'
f=T.load_block030()
d=T.truth.depth_arrays(H,'chr22',40001)
for (s,e) in [(0,40001),(1950,4700),(2999,3000),(30000,40001)]:
    r=f(H,'chr22',s,e); t=T.summarize(d[s:e])
    ok = abs(r['mean_depth']-t['mean'])<1e-9 and r['covered']==t['covered'] and r['max_depth']==t['mx'] and abs(r['pct_ge_10x']-t['ge10'])<1e-9 and abs(r['pct_ge_20x']-t['ge20'])<1e-9
    out=subprocess.run(['samtools','depth','-a','-r',f'chr22:{s+1}-{e}',H],capture_output=True,text=True).stdout.split('\n')
    v=[int(l.split('\t')[2]) for l in out if l]
    ok2 = abs(sum(v)/len(v)-r['mean_depth'])<1e-9
    print(f"[{'OK' if ok and ok2 else 'BAD'}] region [{s},{e}) mean {r['mean_depth']:.4f} (truth {t['mean']:.4f}, samtools depth -a {sum(v)/len(v):.4f}) covered {r['covered']}/{t['covered']} max {r['max_depth']}/{t['mx']} >=10x {r['pct_ge_10x']:.3f}/{t['ge10']:.3f} >=20x {r['pct_ge_20x']:.3f}/{t['ge20']:.3f}")
PY
echo "=== block 029 verbatim call line executed (chr22 0..40001)"
sed "s#input\.bam#$H#; s#'chr1', 1000000, 2000000#'chr22', 0, 40001#" $R/blocks/029_python.py > b030.py; python b030.py
