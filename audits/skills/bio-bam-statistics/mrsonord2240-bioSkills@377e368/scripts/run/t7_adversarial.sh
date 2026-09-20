#!/bin/bash
# INPUT 7 (Adversarial, regression of pre-fix input 7): empty BAM, SE BAM, unindexed BAM, Ensembl-style MT contig, file names with spaces, through the fixed recipes.
export LC_ALL=C PYTHONIOENCODING=utf-8
R=/mnt/openscience/audits/bio-bam-statistics/run; cd $R/work; D=$R/data
rm -rf adv; mkdir adv; cd adv
cp $D/empty.bam empty.bam; cp $D/empty.bam.bai empty.bam.bai; cp $D/se.bam se.bam; cp $D/se.bam.bai se.bam.bai; cp $D/noindex.bam noindex.bam; cp $R/work/synth_MT.bam synth_MT.bam
cp $AFDATA/sarscov2/test.single_end.sorted.bam "real se sample.bam"
echo "=== Skill pysam counters (block 028) + qc_report.py vs flagstat, hand counts: empty / SE / real SE / MT / unindexed"
python $R/t3_qc_vs_flagstat.py empty.bam se.bam "real se sample.bam" synth_MT.bam noindex.bam
echo "--- raw outputs on empty.bam"
sed "s#'input.bam'#'empty.bam'#" $R/blocks/028_python.py > c.py; python c.py; echo "block028 rc=$?"
python $R/skill/examples/qc_report.py empty.bam; echo "qc_report rc=$?"
sed "s#'input.bam'#'empty.bam'#" $R/blocks/031_python.py > i.py; python i.py; echo "block031 rc=$?"
echo "--- block 028 on real SE BAM"; sed "s#'input.bam'#'real se sample.bam'#" $R/blocks/028_python.py > c2.py; python c2.py; echo "rc=$?"
echo "=== depth-based recipes on empty.bam (header has 1 contig, 1000 bp, no reads)"
samtools depth -aa empty.bam | awk '
    {s += $3; n++; if ($3 >= 10) c10++; if ($3 >= 20) c20++}
    END {if (!n) {print "no positions (empty BAM or no @SQ)" > "/dev/stderr"; exit 1}
         printf "mean %.2fx  >=10x %.2f%%  >=20x %.2f%%\n", s/n, c10/n*100, c20/n*100}'; echo "rc=$?"
samtools coverage empty.bam | cut -f1-8; mosdepth -t 1 me empty.bam; cat me.mosdepth.summary.txt
python - <<'PY'
import sys; sys.path.insert(0,'/mnt/openscience/audits/bio-bam-statistics/run')
src=open('/mnt/openscience/audits/bio-bam-statistics/run/blocks/030_python.py',encoding='utf-8').read().split('\nstats = region_depth_stats')[0]
ns={}; exec(src,ns)
print('region_depth_stats on empty BAM:', ns['region_depth_stats']('empty.bam','amp',0,1000))
try: ns['region_depth_stats']('empty.bam','amp',0,0)
except Exception as e: print('zero-length region ->', type(e).__name__, e)
try: ns['region_depth_stats']('empty.bam','nosuchcontig',0,100)
except Exception as e: print('bad contig ->', type(e).__name__, str(e)[:90])
PY
echo "=== idxstats mito/sex recipes on empty, SE (contig 'amp'), MT-renamed"
MITO='
    $1 ~ /^(chr)?(M|MT)$/ {mt += $3; found = 1}
    {total += $3}
    END {if (!found) {print "no chrM/MT contig in idxstats" > "/dev/stderr"; exit 1}
         if (!total) {print "no mapped reads" > "/dev/stderr"; exit 1}
         printf "%.2f%% mitochondrial\n", mt/total*100}'
for b in empty.bam se.bam synth_MT.bam; do echo "--- $b"; samtools idxstats $b | awk "$MITO"; echo "rc=$?"; done
echo "--- MT contig with zero reads: recipe must say no mapped reads, not divide by zero"
printf 'MT\t16569\t0\t0\nchr1\t1000\t0\t0\n*\t0\t0\t0\n' | awk "$MITO"; echo "rc=$?"
echo "=== idxstats on unindexed BAM: (a) samtools (b) pysam get_index_statistics (c) mosdepth"
samtools idxstats noindex.bam 2>&1 | head -3; echo "rc=${PIPESTATUS[0]}"
python -c "
import pysam
with pysam.AlignmentFile('noindex.bam') as b:
    try: print(b.get_index_statistics())
    except Exception as e: print('pysam:', type(e).__name__, str(e)[:80])"
mosdepth -t 1 mn noindex.bam 2>&1 | tail -1
echo "=== summary loop with a space in the file name (block 006)"
mkdir -p sp; cp "real se sample.bam" sp/; (cd sp; bash $R/blocks/006_bash.sh; cat summary.tsv)
echo "=== the trap question: flagstat says 99% mapped -- does the Skill say why that is not enough? (section text)"
grep -n -A3 'What Flagstat Does Not Reveal' $R/skill/SKILL.md | cut -c1-200 | head -8
grep -c 'Adapter readthrough\|Off-target enrichment\|Low-complexity pile-up\|Cross-sample contamination\|Wrong reference build' $R/skill/SKILL.md
echo "=== NEW: unaligned BAM (uBAM, only @RG, no @SQ) through flagstat vs the Skill's pysam tools; SAM text input; CRAM input to qc_report"
U=$R/data/edge/ubam_no_sq.bam
samtools flagstat -O tsv $U | head -3 | cut -f1-3
python $R/skill/examples/qc_report.py $U 2>&1 | tail -2; echo "qc_report rc=${PIPESTATUS[0]}"
sed "s#'input.bam'#'$U'#" $R/blocks/028_python.py > cu.py; python cu.py 2>&1 | tail -1; echo "block028 rc=${PIPESTATUS[0]}"
samtools view -h $R/data/se.bam > se.sam; python $R/skill/examples/qc_report.py se.sam 2>&1 | tail -1
CR=$AFDATA/human/test.paired_end.sorted.cram
python $R/skill/examples/qc_report.py $CR 2>&1 | tail -1
REF_PATH=$AFDATA/human REF_CACHE=/tmp/refcache_bs python $R/skill/examples/qc_report.py $CR 2>&1 | tail -4
