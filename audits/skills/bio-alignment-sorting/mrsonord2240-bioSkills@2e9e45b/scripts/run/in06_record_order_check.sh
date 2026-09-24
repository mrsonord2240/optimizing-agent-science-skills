#!/bin/bash
# INPUT 6 (NEW, adversarial): "A collaborator sent me a folder of BAM/CRAM files labelled SO:coordinate. Verify at RECORD level that each is
#   really coordinate-sorted (no false alarms on the good ones, no misses on planted defects), also on a ~1M-read file, and fix the bad ones."
# Uses the fixed SKILL's pysam `is_coordinate_sorted` / `ensure_coordinate_sorted` extracted VERBATIM from SKILL.md, plus the SKILL's
# `samtools index` test as the second method, plus order_check.py (own independent walker).
source /mnt/openscience/audits/bio-alignment-sorting/run/common.sh
W=$WORK/in6; rm -rf $W; mkdir -p $W; cd $W
python $RUN/extract_block.py "### Check Sort Order in pysam" python skillfns.py
cat > verdicts.py <<'EOP'
# prints "<name> skill_fn=<True|False|ERR:...> " for each path given
import sys, time
from skillfns import is_coordinate_sorted
for p in sys.argv[1:]:
    t=time.time()
    try:
        v = is_coordinate_sorted(p)
    except Exception as e:
        v = "ERR:%s:%s" % (type(e).__name__, str(e)[:70].replace('\n',' '))
    print("%s\t%s\t%.2fs" % (p, v, time.time()-t))
EOP
idx() { rm -f /tmp/chk.bai /tmp/chk.csi; if samtools index "$1" /tmp/chk.bai 2>/dev/null; then echo indexable; else echo not-indexable; fi; }

echo "### 6.1 POSITIVES: every REAL coordinate-sorted alignment file in public-data (must be True; no false alarms)"
mkdir -p pos; cd pos
for f in human/test.paired_end.sorted.bam human/test.rna.paired_end.sorted.bam 1000g/HG00349.chr20_1400000-1500000.bam derived/planted_dups.bam \
         sarscov2/sars-cov-2_v5.3.2.nanopore.bam sarscov2/test.paired_end.sorted.bam sarscov2/test.paired_end.umi.sorted.bam sarscov2/test.single_end.sorted.bam; do
  b=$(echo $f | tr '/' '_'); cp $PD/$f $b
done
for b in *.bam; do echo "$b: records=$(samtools view -c $b) supp/secondary=$(samtools view -c -F 0 -f 0x100 $b)+$(samtools view -c -f 0x800 $b) index-test=$(idx $b)"; done
python ../verdicts.py *.bam | tee ../pos.verdicts
cd ..
awk -F'\t' '$2!="True"{bad++} END{exit bad}' pos.verdicts && echo "  [PASS] all 8 real sorted BAMs -> True (no false positive)" || echo "  [FAIL] at least one real sorted BAM was not True"

echo "### 6.2 CRAM input (SKILL says pysam 'rb'): real sorted CRAM, with and without a reference available"
cp $PD/human/test.paired_end.sorted.cram c.cram; cp $PD/human/test.paired_end.sorted.cram.crai c.cram.crai 2>/dev/null; cp $PD/human/genome.fasta genome.fasta; cp $PD/human/genome.fasta.fai genome.fasta.fai
python verdicts.py c.cram
echo "-- with a reference cache in REF_PATH format (file named by the @SQ M5 md5, populated from genome.fasta):"
M5=$(samtools view -H c.cram 2>/dev/null | grep -a '^@SQ' | grep -o 'M5:[0-9a-f]*' | cut -d: -f2); echo "  header M5 = $M5"
mkdir -p refc/${M5:0:2}/${M5:2:2}; samtools faidx genome.fasta chr22 | tail -n +2 | tr -d '
' | tr a-z A-Z > refc/${M5:0:2}/${M5:2:2}/${M5:4}
REF_PATH=$PWD/refc/%2s/%2s/%s python verdicts.py c.cram
echo "  (first line: no reference resolvable -> the SKILL function raises OSError 'truncated file'; second: cached reference -> a verdict)"

echo "### 6.3 NEGATIVES: shuffled real BAMs, name-sorted (-n, -N), tag-sorted, template-coordinate, mislabelled-header (all must be False)"
mkdir -p neg; cd neg
cp $DATA/shuffled_real.bam shuffled_real.bam; cp $DATA/shuffled_1000g.bam shuffled_1000g.bam
samtools sort -n -o namesort_nat.bam $PD/human/test.paired_end.sorted.bam
samtools sort -N -o namesort_asc.bam $PD/human/test.paired_end.sorted.bam
samtools sort -t RX -o tagsort_rx.bam $PD/human/test.paired_end.umi_unsorted.bam
samtools sort --template-coordinate -o templcoord.bam $PD/human/test.paired_end.sorted.bam
samtools collate -o collated.bam $PD/human/test.paired_end.sorted.bam
python - <<'EOP'
import pysam
for src,dst in (('shuffled_real.bam','liar_real.bam'),('shuffled_1000g.bam','liar_1000g.bam')):
    with pysam.AlignmentFile(src,'rb') as i:
        hd=i.header.to_dict(); rs=list(i)
    hd['HD']={'VN':'1.6','SO':'coordinate'}
    with pysam.AlignmentFile(dst,'wb',header=pysam.AlignmentHeader.from_dict(hd)) as o:
        for r in rs: o.write(r)
EOP
# contig-order violation on REAL multi-contig data: take a real sorted BAM with several contigs? 1000G slice is one contig (chr20). Build a 2-contig real-read file:
python - <<'EOP'
import pysam
# real reads from the sorted human BAM, relabelled to 2 contigs: first half to chrA, second half chrB, then written B-block before A-block (both internally sorted)
src=pysam.AlignmentFile('/mnt/openscience/audit-envs/alignment-files/public-data/human/test.paired_end.sorted.bam','rb')
hd=src.header.to_dict(); rs=list(src)
hd['SQ']=[{'SN':'chrA','LN':40001},{'SN':'chrB','LN':40001}]
h=pysam.AlignmentHeader.from_dict(hd)
half=len(rs)//2
# simple approach: rewrite via query fields
out=[]
for i,r in enumerate(rs):
    tid = 0 if i<half else 1
    a=pysam.AlignedSegment(h); a.query_name=r.query_name; a.flag=r.flag
    a.reference_id=tid if r.reference_id>=0 else -1; a.reference_start=r.reference_start; a.mapping_quality=r.mapping_quality
    a.cigartuples=r.cigartuples; a.query_sequence=r.query_sequence; a.query_qualities=r.query_qualities
    a.next_reference_id=a.reference_id if r.next_reference_id>=0 else -1; a.next_reference_start=r.next_reference_start; a.template_length=r.template_length
    out.append(a)
def key(a): return (a.reference_id if a.reference_id>=0 else 1<<30, a.reference_start)
good=sorted(out,key=key)
bad=[a for a in good if a.reference_id==1]+[a for a in good if a.reference_id!=1]   # chrB block first, unmapped at end
hd['HD']={'VN':'1.6','SO':'coordinate'}; h2=pysam.AlignmentHeader.from_dict(hd)
for name,recs in (('realreads_2contig_good.bam',good),('realreads_2contig_swapped.bam',bad)):
    with pysam.AlignmentFile(name,'wb',header=h2) as o:
        for a in recs:
            o.write(a)
print('2-contig real-read files written', len(good))
EOP
# mutation tests on a real sorted BAM: swap two adjacent records with different POS; move one mapped read after the unmapped block
python - <<'EOP'
import pysam
src='/mnt/openscience/audit-envs/alignment-files/public-data/1000g/HG00349.chr20_1400000-1500000.bam'
with pysam.AlignmentFile(src,'rb') as f:
    h=f.header; rs=list(f)
print('1000G records', len(rs), 'unmapped tail', sum(1 for r in rs if r.is_unmapped and r.reference_id<0))
def write(name, recs):
    with pysam.AlignmentFile(name,'wb',header=h) as o:
        for r in recs: o.write(r)
# 1. single adjacent swap in the middle with different POS
i=next(k for k in range(len(rs)//2,len(rs)-1) if rs[k].reference_id>=0 and rs[k+1].reference_id>=0 and rs[k].reference_start<rs[k+1].reference_start)
m=list(rs); m[i],m[i+1]=m[i+1],m[i]; write('mut_swap_mid.bam',m); print('swap at',i)
# 2. last mapped record moved after the fully-unmapped block (unmapped not last)
mapped=[r for r in rs if r.reference_id>=0]; unm=[r for r in rs if r.reference_id<0]
if unm:
    write('mut_mapped_after_unmapped.bam', mapped[:-1]+unm+[mapped[-1]])
else:
    print('no fully-unmapped reads in this slice; synthesising by appending one mapped record after an unmapped one')
    u=pysam.AlignedSegment(h); u.query_name='u1'; u.flag=4; u.reference_id=-1; u.reference_start=-1; u.query_sequence='ACGT'; u.query_qualities=pysam.qualitystring_to_array('IIII')
    write('mut_mapped_after_unmapped.bam', mapped[:-1]+[u]+[mapped[-1]])
# 3. the very last two mapped records swapped (defect at file end)
m=list(mapped);
j=next(k for k in range(len(m)-2,0,-1) if m[k].reference_start<m[k+1].reference_start)
m[j],m[j+1]=m[j+1],m[j]; write('mut_swap_end.bam',m); print('end swap at',j)
# 4. defect at the very start
j=next(k for k in range(0,len(mapped)-1) if mapped[k].reference_start<mapped[k+1].reference_start)
m=list(mapped); m[j],m[j+1]=m[j+1],m[j]; write('mut_swap_start.bam',m); print('start swap at',j)
EOP
cd ..
for b in neg/*.bam; do echo "$(basename $b): index-test=$(idx $b) | own walker: $(python $RUN/order_check.py $b | grep -a -o 'coordinate_sorted=[A-Za-z]*')"; done | tee neg.second_method
python verdicts.py neg/*.bam | tee neg.verdicts
echo "-- expectations: everything in neg/ except realreads_2contig_good.bam must be False"
python - <<'EOP'
import os
bad=[]
for l in open('neg.verdicts'):
    p,v,_=l.rstrip('\n').split('\t'); b=os.path.basename(p)
    want = (b=='realreads_2contig_good.bam')
    ok = (v=='True')==want and v in ('True','False')
    print(('  [PASS] ' if ok else '  [FAIL] ')+b+' -> '+v+' (expected '+str(want)+')')
    if not ok: bad.append(b)
print('  negatives/false-positive check: %d wrong of %d' % (len(bad), sum(1 for _ in open('neg.verdicts'))))
EOP

echo "### 6.4 Agreement of the SKILL's two record checks (pysam walker vs 'samtools index'): where do they disagree?"
python - <<'EOP'
import re
sec={}
for l in open('neg.second_method'):
    m=re.match(r'(\S+): index-test=(\S+)',l); sec[m.group(1)]=m.group(2)
for l in open('neg.verdicts'):
    p,v,_=l.rstrip('\n').split('\t'); b=p.split('/')[-1]
    flag=''
    if v=='True' and sec[b]=='not-indexable': flag='  <-- pysam True but index fails (would be a pysam false negative)'
    if v=='False' and sec[b]=='indexable': flag='  <-- pysam False, index accepts (documented limit: contig order)'
    print(f'  {b:34s} pysam={v:5s} samtools-index={sec[b]}{flag}')
EOP

echo "### 6.5 Unaligned / no-@SQ BAM and SAM text, empty, unmapped-only (SKILL function robustness)"
mkdir -p edge; cd edge
python - <<'EOP'
import pysam
# uBAM: no @SQ at all
h=pysam.AlignmentHeader.from_dict({'HD':{'VN':'1.6','SO':'unsorted'}})
with pysam.AlignmentFile('ubam.bam','wb',header=h) as o:
    for i in range(3):
        a=pysam.AlignedSegment(h); a.query_name=f'u{i}'; a.flag=4; a.query_sequence='ACGT'; a.query_qualities=pysam.qualitystring_to_array('IIII'); o.write(a)
# empty BAM with SQ
h2=pysam.AlignmentHeader.from_dict({'HD':{'VN':'1.6','SO':'coordinate'},'SQ':[{'SN':'chr1','LN':100}]})
with pysam.AlignmentFile('empty.bam','wb',header=h2): pass
# unmapped only, with SQ
with pysam.AlignmentFile('unmapped_only.bam','wb',header=h2) as o:
    for i in range(3):
        a=pysam.AlignedSegment(h2); a.query_name=f'u{i}'; a.flag=4; a.query_sequence='ACGT'; a.query_qualities=pysam.qualitystring_to_array('IIII'); o.write(a)
EOP
samtools view -h $PD/human/test.paired_end.sorted.bam | head -300 > text.sam
samtools view -h -b -o - text.sam > /dev/null 2>&1
samtools view -b -o sam_as.bam text.sam 2>/dev/null
python ../verdicts.py ubam.bam empty.bam unmapped_only.bam text.sam
cd ..

echo "### 6.6 LARGE file: ~960k records (real 1000G reads x100), sorted vs shuffled; time and memory of the SKILL function"
python - <<'EOP'
import pysam, random
random.seed(6)
with pysam.AlignmentFile('/mnt/openscience/audits/bio-alignment-sorting/run/data/shuffled_1000g.bam','rb') as f:
    h=f.header; rs=list(f)
out=[]
for k in range(100): out.extend(rs)
random.shuffle(out)
with pysam.AlignmentFile('big_shuf.bam','wb',header=h) as o:
    for r in out: o.write(r)
print('big_shuf.bam records', len(out))
EOP
samtools sort -@ 8 -o big_sorted.bam big_shuf.bam
echo "  sorted size $(stat -c %s big_sorted.bam) bytes; records $(samtools view -c big_sorted.bam)"
cat > timeit.py <<'EOP'
import sys, time, resource
from skillfns import is_coordinate_sorted
p=sys.argv[1]; t=time.time(); v=is_coordinate_sorted(p); dt=time.time()-t
print("%s is_coordinate_sorted=%s  %.1fs  maxRSS=%.0f MB" % (p, v, dt, resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024))
EOP
python timeit.py big_sorted.bam; python timeit.py big_shuf.bam
t=$(date +%s.%N); samtools index big_sorted.bam /tmp/big.bai; t2=$(date +%s.%N); python -c "print('  samtools index on the same sorted file: %.1fs' % ($t2-$t))"
t=$(date +%s.%N); python $RUN/order_check.py big_sorted.bam | grep -a -o 'coordinate_sorted=[A-Za-z]*'; t2=$(date +%s.%N); python -c "print('  own walker (loads all records) on sorted: %.1fs' % ($t2-$t))"
echo "-- one mutation in a 960k-record file (swap two adjacent records near the end): does the SKILL function still find it?"
python - <<'EOP'
import pysam
with pysam.AlignmentFile('big_sorted.bam','rb') as f:
    h=f.header; rs=list(f)
j=next(k for k in range(len(rs)-1000,0,-1) if rs[k].reference_id>=0 and rs[k+1].reference_id>=0 and rs[k].reference_start<rs[k+1].reference_start)
rs[j],rs[j+1]=rs[j+1],rs[j]
with pysam.AlignmentFile('big_mut.bam','wb',header=h) as o:
    for r in rs: o.write(r)
print('swapped', j, 'of', len(rs))
EOP
python timeit.py big_mut.bam
rm -f big_shuf.bam big_sorted.bam big_mut.bam

echo "### 6.7 ensure_coordinate_sorted on every negative that a re-sort can fix (must return a path that is_coordinate_sorted + indexes)"
cat > ensure_all.py <<'EOP'
import glob, os, pysam
from skillfns import is_coordinate_sorted, ensure_coordinate_sorted
fixable=[p for p in sorted(glob.glob('neg/*.bam')) if 'templcoord' not in p or True]
bad=0
for p in fixable:
    out='fixed_'+os.path.basename(p)
    r=ensure_coordinate_sorted(p,out)
    ok=is_coordinate_sorted(r)
    idx_ok=True
    try: pysam.index(r)
    except Exception as e: idx_ok=False
    was=is_coordinate_sorted(p)
    print("  %-34s was_sorted=%-5s -> returned %-38s now_sorted=%s indexes=%s" % (os.path.basename(p), was, r, ok, idx_ok))
    if not (ok and idx_ok): bad+=1
print("ensure_coordinate_sorted failures:", bad)
assert bad==0
EOP
python ensure_all.py
summary
