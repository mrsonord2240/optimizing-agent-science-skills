#!/bin/bash
# INPUT 4 (Variant B, regression of pre-fix input 4): depth caps. SYNTHETIC 9500x stack (truth by construction: max 9500, mean 1000 over 1000 bp) + REAL ARTIC nanopore BAM.
export LC_ALL=C PYTHONIOENCODING=utf-8
R=/mnt/openscience/audits/bio-bam-statistics/run; cd $R/work
D=$R/data/deep.bam; DF=$R/data/deep.fa
mx(){ awk '{if($NF>m)m=$NF; s+=$NF; n++} END{printf "  max=%d mean(sum/1000)=%.2f rows=%d\n", m, s/1000, n}'; }
echo "=== block 019 table, claim by claim (truth max 9500, mean 1000)"
echo "samtools depth default (claimed: uncapped)";      samtools depth -aa $D | mx
echo "samtools depth -d 100 (claimed: silently ignored)"; samtools depth -aa -d 100 $D 2>&1 | mx
echo "samtools coverage default (claimed -d 1000000)";  samtools coverage $D | cut -f1-7
samtools coverage --help 2>&1 | grep -E -- '-d, --depth|--depth'
echo "samtools coverage -d 8000 (shows the cap is real)"; samtools coverage -d 8000 $D | cut -f1-7
echo "mosdepth (claimed uncapped)"; mosdepth -t 2 mdE $D; tail -1 mdE.mosdepth.summary.txt
echo "samtools mpileup default (claimed 8000)";  samtools mpileup -a -f $DF $D 2>/dev/null | awk '{print $4}' | sort -n | tail -1
echo "samtools mpileup -d 1000000 (claimed fix)"; samtools mpileup -a -d 1000000 -f $DF $D 2>/dev/null | awk '{print $4}' | sort -n | tail -1
echo "bcftools mpileup default (claimed 250)"; bcftools mpileup -a FORMAT/DP -f $DF $D 2>/dev/null | bcftools query -f '[%DP]\n' | sort -n | tail -1
echo "bcftools mpileup -d 1000000 (claimed fix)"; bcftools mpileup -a FORMAT/DP -d 1000000 -f $DF $D 2>/dev/null | bcftools query -f '[%DP]\n' | sort -n | tail -1
echo "pysam pileup default max_depth (claimed 8000) and max_depth=1_000_000"
python - <<'PY'
import pysam
D='/mnt/openscience/audits/bio-bam-statistics/run/data/deep.bam'
with pysam.AlignmentFile(D) as b:
    print('  default:', max(c.n for c in b.pileup('amp')))
    print('  max_depth=1_000_000:', max(c.n for c in b.pileup('amp', max_depth=1_000_000)))
PY
echo "=== block 030 region_depth_stats on the stack vs truth"
python $R/t4_helper.py $D amp 1000 0 1000 100 200 300 400 0 100
echo "=== block 018 (depth -aa recipe) on the stack"; samtools depth -aa $D | awk '
    {s += $3; n++; if ($3 >= 10) c10++; if ($3 >= 20) c20++}
    END {if (!n) {print "no positions (empty BAM or no @SQ)" > "/dev/stderr"; exit 1}
         printf "mean %.2fx  >=10x %.2f%%  >=20x %.2f%%\n", s/n, c10/n*100, c20/n*100}'
echo "  truth: mean 1000.00x; >=10x = 200/1000 = 20.00%"
echo "=== REAL ARTIC nanopore BAM (MN908947.3, 29903 bp): truth from get_blocks vs depth -aa recipe, coverage, mosdepth, pysam recipe"
A=$AFDATA/sarscov2/sars-cov-2_v5.3.2.nanopore.bam; cp $A art.bam; cp $A.bai art.bam.bai 2>/dev/null || samtools index art.bam
python - <<'PY'
import sys; sys.path.insert(0,'/mnt/openscience/audits/bio-bam-statistics/run/')
import pysam
from truth import depth_arrays
with pysam.AlignmentFile('art.bam') as b: c,l=b.references[0],b.lengths[0]
d=depth_arrays('art.bam',c,l)
print(f'TRUTH: {c} len {l} mean {d.sum()/l:.4f} covered {(d>0).sum()} >=10x {100*(d>=10).sum()/l:.4f}% >=20x {100*(d>=20).sum()/l:.4f}% max {d.max()}')
PY
samtools depth -aa art.bam | awk '
    {s += $3; n++; if ($3 >= 10) c10++; if ($3 >= 20) c20++}
    END {printf "recipe mean %.4fx  >=10x %.4f%%  >=20x %.4f%%\n", s/n, c10/n*100, c20/n*100}'
samtools coverage art.bam | cut -f1-7
mosdepth --fast-mode mdF art.bam; tail -1 mdF.mosdepth.summary.txt
python $R/t4_helper.py art.bam MN908947.3 29903 0 29903 1000 3000
