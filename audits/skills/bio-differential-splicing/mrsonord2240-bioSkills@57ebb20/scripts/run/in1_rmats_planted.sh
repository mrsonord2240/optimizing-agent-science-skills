#!/bin/bash
# INPUT 1 (canonical, regression): rMATS-turbo 3v3 on the PLANTED exon-skipping set (SYNTHETIC; truth dPSI 0.587, G1 > G2)
# following the FIXED SKILL.md: (a) the rMATS block verbatim (paired/150/firststrand on single-end data -> the Skill says header-only),
# (b) command matched to the data per "Match the command to the data", (c) SKILL.md filter snippet verbatim, (d) shipped example from a clean copy.
source /mnt/openscience/audits/bio-differential-splicing/run/common.sh
python3 $R/extract_blocks.py get 0 /tmp/blk0.sh 2>/dev/null || $CORE python $R/extract_blocks.py get 0 /tmp/blk0.sh
$CORE python $R/extract_blocks.py get 1 /tmp/blk1.py
W=$R/out/in1; rm -rf $W; mkdir -p $W; cd $W
echo "=== (a) SKILL.md rMATS block VERBATIM, on single-end 50 nt unstranded planted BAMs"
mkdir -p a; cd a
cp $P/b1.txt condition1_bams.txt; cp $P/b2.txt condition2_bams.txt; cp $P/planted.gtf annotation.gtf
sed 's/^rmats.py/micromamba run -n as-core rmats.py/' /tmp/blk0.sh > cmd.sh; grep -n 'rmats.py\|-t \|readLength\|libType' cmd.sh
bash cmd.sh > a.log 2>&1; echo "rc=$?"
echo "SE.MATS.JC.txt rows: $(($(wc -l < rmats_output/SE.MATS.JC.txt)-1)) (header only expected: -t paired on single-end reads)"
cd ..
echo "=== (b) matched to the data: -t single --readLength 50 --libType fr-unstranded, everything else as the block"
mkdir -p b; cd b
cp $P/b1.txt condition1_bams.txt; cp $P/b2.txt condition2_bams.txt; cp $P/planted.gtf annotation.gtf
sed -e 's/^rmats.py/micromamba run -n as-core rmats.py/' -e 's/-t paired/-t single/' -e 's/--readLength 150/--readLength 50/' -e 's/fr-firststrand/fr-unstranded/' /tmp/blk0.sh > cmd.sh
bash cmd.sh > b.log 2>&1; echo "rc=$?"
cut -f1-6,13-24 rmats_output/SE.MATS.JC.txt
$CORE python - <<'PY'
import pandas as pd, numpy as np
d = pd.read_csv('rmats_output/SE.MATS.JC.txt', sep='\t')
assert len(d) == 1 and 'FDR' in d.columns, 'table check from SKILL.md'
r = d.iloc[0]
print('IJC1', r.IJC_SAMPLE_1, 'SJC1', r.SJC_SAMPLE_1, 'IJC2', r.IJC_SAMPLE_2, 'SJC2', r.SJC_SAMPLE_2)
assert r.IJC_SAMPLE_1 == '80,80,80' and r.SJC_SAMPLE_1 == '10,10,12' and r.IJC_SAMPLE_2 == '20,20,20' and r.SJC_SAMPLE_2 == '40,40,38'
assert abs(r.IncLevelDifference - 0.587) < 0.002 and r.FDR < 1e-10
print('ASSERT OK: counts equal the planted counts, IncLevelDifference %.4f (truth 0.587), FDR %.2g' % (r.IncLevelDifference, r.FDR))
PY
echo "--- SKILL.md python filter block VERBATIM on this table (reads rmats_output/SE.MATS.JC.txt)"
cat > filt.py <<'PY'
PY
cat /tmp/blk1.py > filt.py; echo "print('significant rows:', len(significant)); print(significant[['GeneID','IncLevelDifference','FDR','coverage_ok']].to_string())" >> filt.py
$CORE python filt.py
cd ..
echo "=== (c) shipped examples/diff_splicing_rmats.sh, from a COPY, clean dir, planted data (single-end 50 nt)"
mkdir -p ex; cd ex
cp $SK/examples/diff_splicing_rmats.sh run.sh; cp $P/planted.gtf annotation.gtf; cp $P/b1.txt condition1_bams.txt; cp $P/b2.txt condition2_bams.txt
bash -n run.sh && echo "bash -n OK"
$CORE bash run.sh > run.log 2>&1; echo "rc=$?"; cat run.log | grep -v '^$' | cut -c1-200 | tail -14
cd ..
echo "=== (d) swapped b1/b2 (sign): IncLevelDifference must be -0.587 (Skill: group 1 - group 2)"
mkdir -p d/tmp d/out
$CORE rmats.py --b1 $P/b2.txt --b2 $P/b1.txt --gtf $P/planted.gtf -t single --readLength 50 --libType fr-unstranded --nthread 4 --od d/out --tmp d/tmp > d.log 2>&1
cut -f1-6,20-24 d/out/SE.MATS.JC.txt
awk -F'\t' 'NR==2{ if ($23+0 < -0.58 && $23+0 > -0.59) print "ASSERT OK: swapped sign -0.587"; else print "ASSERT FAIL: " $23}' d/out/SE.MATS.JC.txt
