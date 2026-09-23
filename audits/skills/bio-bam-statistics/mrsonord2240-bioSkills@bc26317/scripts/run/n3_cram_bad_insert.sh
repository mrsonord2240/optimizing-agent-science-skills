#!/bin/bash
# NEW INPUTS: (a) CRAM variants (reference / embedded reference / no index / no reference / WRONG reference) and bad files through qc_report.py, the Count Reads snippet and flagstat;
# (b) insert-size window boundary (own_insert.bam) against samtools stats -i.
export LC_ALL=C PYTHONIOENCODING=utf-8
R=/mnt/openscience/audits/bio-bam-statistics/run; N=$R/data/new; cd $R/work; rm -rf cb; mkdir cb; cd cb
Q="python $R/skill/examples/qc_report.py"
show(){ sed -n '1,4p;/Mapped/p;/Properly/p;/Duplicates/p;/Insert/p' | cut -c1-230; }
echo "########## (a) own_ctg CRAM/BAM variants. flagstat truth: total 1105 (1098+7 failed), primary 1098, passed primary 1091, mapped 1085, dup 5"
for f in own_ctg.bam own_ctg.cram own_ctg_embed.cram own_ctg_noidx.cram; do
  echo "--- $f : samtools flagstat (no reference given)"; timeout 60 samtools flagstat -O tsv $N/$f 2>&1 | sed -n '1,2p' | cut -f1-3
  echo "--- $f : qc_report.py WITHOUT reference"; timeout 120 $Q $N/$f 2>&1 | show; echo "rc=${PIPESTATUS[0]}"
  echo "--- $f : qc_report.py WITH reference own_ctg.fa"; timeout 120 $Q $N/$f $N/own_ctg.fa 2>&1 | show; echo "rc=${PIPESTATUS[0]}"
done
echo "--- own_ctg.cram : qc_report.py with the WRONG reference (same names/lengths, other bases)"; timeout 120 $Q $N/own_ctg.cram $N/wrong.fa 2>&1 | show; echo "rc=${PIPESTATUS[0]}"
echo "--- own_ctg.cram : REF_PATH pointing at the right FASTA dir, no 2nd argument (documented alternative is the 2nd argument only)"; mkdir -p rp; cp $N/own_ctg.fa rp/; REF_PATH=$R/work/cb/rp/%2s/%2s/%s:$R/work/cb/rp REF_CACHE=$R/work/cb/rc timeout 60 $Q $N/own_ctg.cram 2>&1 | head -2 | cut -c1-200
echo "--- Count Reads snippet (block 027) on the CRAM variants: no reference argument in the snippet"
for f in own_ctg.cram own_ctg_embed.cram; do sed "s#'input.bam'#'$N/$f'#" $R/blocks/027_python.py > c_$f.py; echo "[$f]"; timeout 60 python c_$f.py 2>&1 | tail -3 | cut -c1-200; done
echo "--- region_depth_stats on the unindexed CRAM (Skill: region/pileup need a .crai)"
python - <<'PY' 2>&1 | tail -2 | cut -c1-200
import os
R='/mnt/openscience/audits/bio-bam-statistics/run'
src=open(R+'/blocks/029_python.py',encoding='utf-8').read().split('\nstats = region_depth_stats')[0]; ns={}; exec(src,ns)
try: print(ns['region_depth_stats'](R+'/data/new/own_ctg_noidx.cram','ctgA',0,1000,reference=R+'/data/new/own_ctg.fa'))
except Exception as e: print('region_depth_stats on unindexed CRAM ->', type(e).__name__, str(e)[:120])
PY
echo "########## bad files: flagstat vs qc_report.py vs block 027"
for f in truncated.bam text_named.bam zero_byte.bam; do
  echo "--- $f ($(stat -c %s $N/$f) bytes)"; echo "[flagstat]"; timeout 60 samtools flagstat $N/$f 2>&1 | head -3 | cut -c1-160; echo "rc=${PIPESTATUS[0]}"
  echo "[qc_report]"; timeout 60 $Q $N/$f 2>&1 | head -8 | cut -c1-220; echo "rc=${PIPESTATUS[0]}"
  sed "s#'input.bam'#'$N/$f'#" $R/blocks/027_python.py > bad_$f.py; echo "[block 027]"; timeout 60 python bad_$f.py 2>&1 | tail -2 | cut -c1-200; echo "rc=${PIPESTATUS[0]}"
done
echo "--- samtools quickcheck on the bad files (independent detector)"; for f in truncated.bam text_named.bam zero_byte.bam; do samtools quickcheck -v $N/$f 2>&1 | cut -c1-120; echo "$f quickcheck rc=$?"; done
echo "########## (b) insert-size boundary: template lengths 300x10, 7000x3, 7999, 8000, 8001, 8500x2 (all proper pairs)"
python - <<'PY'
import json,statistics
t=json.load(open('/mnt/openscience/audits/bio-bam-statistics/run/data/new/own_insert.truth.json'))['tlens']
lt=[x for x in t if 0<x<8000]; le=[x for x in t if 0<x<=8000]
print('TRUTH qc_report rule (0 < tlen < 8000): n=%d mean=%.1f median(upper)=%d | rule <=8000: n=%d mean=%.1f | all pairs: n=%d mean=%.1f'%(len(lt),sum(lt)/len(lt),sorted(lt)[len(lt)//2],len(le),sum(le)/len(le),len(t),sum(t)/len(t)))
PY
echo "[qc_report.py]"; $Q $N/own_insert.bam | sed -n '/Insert/p'
echo "[samtools stats default -i]"; samtools stats $N/own_insert.bam | grep -E '^SN\s+(insert size average|insert size standard|inward|outward)' | cut -f2-3
echo "[samtools stats -i 20000]"; samtools stats -i 20000 $N/own_insert.bam | grep -E '^SN\s+insert size average' | cut -f2-3
echo "[block 030 snippet (no cap)]"; sed "s#'input.bam'#'$N/own_insert.bam'#" $R/blocks/030_python.py > ins.py; python ins.py
