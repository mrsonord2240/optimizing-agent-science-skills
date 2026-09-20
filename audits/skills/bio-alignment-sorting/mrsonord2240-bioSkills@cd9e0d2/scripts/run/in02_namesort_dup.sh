#!/bin/bash
# INPUT 2 (variant A, REGRESSION of first audit input 2 + the fix's -n natural / -N ASCII claims re-verified independently):
# "Sort by read name and run the duplicate-marking workflow, then extract paired FASTQ.
#   Is `sort -n` a strict lexicographic order? What do I use for Picard?"
# Real data: derived/planted_dups.bam (real reads, 50 planted pairs -> 100 dup reads; Picard=50 pairs), human PE BAM,
# real RNA PE BAM, real 1000G BAM; synthetic read1..read1000 names (SYNTHETIC) to distinguish natural vs ASCII order.
source /mnt/openscience/audits/bio-alignment-sorting/run/common.sh
W=$WORK/in2; rm -rf $W; mkdir -p $W; cd $W
PL=$PD/derived/planted_dups.bam
ndup() { samtools view -c -f 1024 "$1"; }
echo "planted: records=$(nrec $PL) dup-flagged-in-input=$(ndup $PL) SO=$(so $PL)"

echo "### 2.1 old SKILL workflow (4 commands; -n then fixmate -m) - REGRESSION; new SKILL now says fixmate takes -n or -N"
samtools sort -n -o namesorted.bam $PL
samtools fixmate -m namesorted.bam fixmate.bam
samtools sort -o sorted.bam fixmate.bam
samtools markdup -s sorted.bam marked.bam 2> markdup_stats.txt; head -12 markdup_stats.txt
eq "-n workflow: duplicate reads flagged" "$(ndup marked.bam)" "100"
eq "final @HD SO" "$(so marked.bam | grep -o 'SO:[a-z]*')" "SO:coordinate"
echo "-- same with -N (SKILL table: fixmate accepts -n or -N)"
samtools sort -N -o namesortedN.bam $PL
samtools fixmate -m namesortedN.bam fixmateN.bam && samtools sort -o sortedN.bam fixmateN.bam && samtools markdup sortedN.bam markedN.bam
eq "-N workflow: duplicate reads flagged" "$(ndup markedN.bam)" "100"
echo "-- Picard 3.5.0 ground truth on the SAME input:"
picard MarkDuplicates -I $PL -O picard_marked.bam -M picard_metrics.txt --VALIDATION_STRINGENCY SILENT > picard.log 2>&1
grep -a -A1 '^LIBRARY' picard_metrics.txt | cut -f1-9 | head -3
eq "Picard flags same number of reads" "$(ndup picard_marked.bam)" "100"

echo "### 2.2 SKILL 'Duplicate Marking' collate pipeline (verbatim from new SKILL)"
samtools collate -O -u $PL tmp_prefix | \
    samtools fixmate -m -u - - | \
    samtools sort -u - | \
    samtools markdup - out.bam
samtools index out.bam
eq "collate pipeline: duplicate reads flagged" "$(ndup out.bam)" "100"
eq "collate pipeline final SO" "$(so out.bam | grep -o 'SO:[a-z]*')" "SO:coordinate"
check "out.bam.bai exists" test -s out.bam.bai
echo "-- SKILL comment: 'sort -n / sort -N work in its place' of collate in that pipeline"
samtools sort -n -u $PL | samtools fixmate -m -u - - | samtools sort -u - | samtools markdup - out_nat.bam
samtools sort -N -u $PL | samtools fixmate -m -u - - | samtools sort -u - | samtools markdup - out_asc.bam
eq "sort -n in place of collate: dup reads" "$(ndup out_nat.bam)" "100"
eq "sort -N in place of collate: dup reads" "$(ndup out_asc.bam)" "100"

echo "### 2.3 fixmate on coordinate input (SKILL table + Common Errors)"
samtools fixmate -m $PL nofix.bam 2> nofix.err; head -2 nofix.err
grep -q 'Coordinate sorted, require grouped/sorted by queryname' nofix.err && echo "  [PASS] fixmate -m on coordinate-sorted input REFUSES with the quoted message" || echo "  [FAIL] message not as quoted"

echo "### 2.4 Real human PE BAM: samtools workflow vs Picard"
H=$PD/human/test.paired_end.sorted.bam
samtools sort -n -o h_n.bam $H && samtools fixmate -m h_n.bam h_f.bam && samtools sort -o h_s.bam h_f.bam && samtools markdup h_s.bam h_m.bam
picard MarkDuplicates -I $H -O h_pic.bam -M h_pic.txt --VALIDATION_STRINGENCY SILENT > h_pic.log 2>&1
eq "samtools dup-flagged == Picard dup-flagged (real data)" "$(ndup h_m.bam)" "$(ndup h_pic.bam)"

echo "### 2.5 -n vs -N on names read1..read1000 (SYNTHETIC). Distinguishing set: read1 read2 read10 read100 read1000"
S=$DATA/synth_multi.unsorted.bam
samtools sort -n -o n_nat.bam $S; samtools sort -N -o n_asc.bam $S
picard SortSam -I $S -O n_pic.bam -SORT_ORDER queryname > pic_sort.log 2>&1
for f in n_nat n_asc n_pic; do echo "-- $f: $(so $f.bam)"; python $RUN/order_check.py $f.bam | grep n=; done
samtools view n_nat.bam | cut -f1 | uniq | head -14 | tr '\n' ' '; echo "   <- sort -n first 14 names"
samtools view n_asc.bam | cut -f1 | uniq | head -14 | tr '\n' ' '; echo "   <- sort -N first 14 names"
samtools view n_pic.bam | cut -f1 | uniq | head -14 | tr '\n' ' '; echo "   <- Picard SortSam queryname first 14 names"
samtools view n_nat.bam | cut -f1 > nat.names; samtools view n_asc.bam | cut -f1 > asc.names; samtools view n_pic.bam | cut -f1 > pic.names
cmp -s nat.names asc.names && echo "  [FAIL] -n order == -N order" || echo "  [PASS] -n order differs from -N order (SKILL: -n natural, -N ASCII)"
cmp -s asc.names pic.names && echo "  [PASS] -N order == Picard queryname order (name column; SKILL: -N is what Picard writes)" || echo "  [FAIL] -N differs from Picard order"
grep -a -m3 -n -E '^read(1|2|10)$' nat.names | head -3 | tr '\n' ' '; echo "(read1/read2/read10 line numbers in natural order)"
echo "-- header lines exactly as SKILL table claims:"
echo "  -n : $(so n_nat.bam)"; echo "  -N : $(so n_asc.bam)"; echo "  Picard: $(so n_pic.bam)"
so n_nat.bam | grep -q 'SO:queryname.SS:queryname:natural' && echo "  [PASS] -n header SO:queryname SS:queryname:natural" || echo "  [FAIL] -n header"
so n_asc.bam | grep -q 'SO:queryname.SS:queryname:lexicographical' && echo "  [PASS] -N header SO:queryname SS:queryname:lexicographical" || echo "  [FAIL] -N header"
echo "-- pysam second method: are the two name orders what a plain Python sort says?"
python - <<'EOP'
import pysam, re
def names(p):
    with pysam.AlignmentFile(p,'rb') as f:
        out=[]
        for r in f.fetch(until_eof=True):
            if not out or out[-1]!=r.query_name: out.append(r.query_name)
        return out
nat=names('n_nat.bam'); asc=names('n_asc.bam'); pic=names('n_pic.bam')
key=lambda s:[(0,int(t),'') if t.isdigit() else (1,0,t) for t in re.findall(r'\d+|\D+',s)]
print('  -n  natural sequence  ==  python natural key sort:', nat==sorted(set(nat),key=key))
print('  -N  == python ASCII (bytes) sort:', asc==sorted(set(asc)))
print('  Picard == python ASCII sort:', pic==sorted(set(pic)))
i=lambda L,n: L.index(n)
print('  read2 before read10 in -n:', i(nat,'read2')<i(nat,'read10'), '| read10 before read2 in -N:', i(asc,'read10')<i(asc,'read2'))
assert nat==sorted(set(nat),key=key) and asc==sorted(set(asc)) and pic==asc
print('  PASS')
EOP
echo "-- Picard consumers of -n and -N output (SKILL: -n dies with 'Alignments added out of order ... Sort order is queryname'; ValidateSamFile RECORD_OUT_OF_ORDER):"
picard ValidateSamFile -I n_nat.bam --MODE SUMMARY > val_nat.txt 2>&1; echo "  ValidateSamFile -n:"; grep -a -v '^\[' val_nat.txt | grep -a -E 'ERROR|No errors|RECORD' | head -4
picard ValidateSamFile -I n_asc.bam --MODE SUMMARY > val_asc.txt 2>&1; echo "  ValidateSamFile -N:"; grep -a -v '^\[' val_asc.txt | grep -a -E 'ERROR|No errors|RECORD' | head -4
grep -a -q 'RECORD_OUT_OF_ORDER' val_nat.txt && echo "  [PASS] -n -> RECORD_OUT_OF_ORDER" || echo "  [FAIL] -n not flagged"
grep -a -q -E 'No errors found|^\[.*ValidateSamFile done' val_asc.txt; echo "  -- full ValidateSamFile -N summary (non-INFO lines):"; grep -a -v -E "^(\[|INFO|WARNING: (A restricted|java|Use|Restricted))|setlocale" val_asc.txt | grep -a . ; grep -a -q "^ERROR" val_asc.txt && echo "  [FAIL] -N: ValidateSamFile ERROR lines present" || echo "  [PASS] -N -> no ERROR lines (only the NM warning: no reference given); 'No errors found' text appears only when nothing at all is reported"
samtools sort -n -o pl_nat.bam $PL; samtools sort -N -o pl_asc.bam $PL   # NOTE distinct names: /mnt/openscience is case-insensitive (n.bam == N.bam)
[ "$(samtools view -H pl_nat.bam | grep -c natural)" = 1 ] && echo "  (pl_nat.bam header really is natural: $(so pl_nat.bam))"
picard MarkDuplicates -I pl_nat.bam -O pic_nat.bam -M pic_nat.txt --VALIDATION_STRINGENCY SILENT > pic_nat.log 2>&1; echo "  Picard MarkDuplicates on planted -n rc=$?"
grep -a -m2 -E 'Alignments added out of order|Sort order is queryname|Exception' pic_nat.log | cut -c1-240
picard MarkDuplicates -I pl_asc.bam -O pic_asc.bam -M pic_asc.txt --VALIDATION_STRINGENCY SILENT > pic_asc.log 2>&1; echo "  Picard MarkDuplicates on planted -N rc=$?"
grep -a -A1 '^LIBRARY' pic_asc.txt | cut -f1-9 | head -2
eq "Picard on -N: dup reads flagged" "$(ndup pic_asc.bam)" "100"
grep -q 'READ_PAIR_DUPLICATES' pic_asc.txt && eq "Picard on -N: READ_PAIR_DUPLICATES" "$(grep -a -A1 '^LIBRARY' pic_asc.txt | tail -1 | cut -f7)" "50"

echo "-- REAL names: nf-core name-sorted BAM and real RNA / 1000G BAMs: does -n differ from -N, and does Picard accept -n?"
for label in human/test.rna.paired_end.sorted.bam 1000g/HG00349.chr20_1400000-1500000.bam human/test.paired_end.sorted.bam; do
  b=$(basename $label .bam | tr '.' '_'); src=$PD/$label
  samtools sort -n -o r_$b.nat.bam $src; samtools sort -N -o r_$b.asc.bam $src
  samtools view r_$b.nat.bam | cut -f1 > r.nat.names; samtools view r_$b.asc.bam | cut -f1 > r.asc.names
  cmp -s r.nat.names r.asc.names && same="-n order == -N order for these names" || same="-n order != -N order"
  picard ValidateSamFile -I r_$b.nat.bam --MODE SUMMARY > v.nat.txt 2>&1; picard ValidateSamFile -I r_$b.asc.bam --MODE SUMMARY > v.asc.txt 2>&1
  echo "  $label: $same | Picard Validate: -n=[$(grep -a -o -E 'RECORD_OUT_OF_ORDER|No errors found' v.nat.txt | sort -u | tr '\n' ' ')] -N=[$(grep -a -o -E 'RECORD_OUT_OF_ORDER|No errors found' v.asc.txt | sort -u | tr '\n' ' ')]"
done
echo "-- fixed-width names: natural == ASCII order. Does Picard accept -n output then (SKILL table: '-n output is rejected')?"
python - <<'EOP'
import pysam
h=pysam.AlignmentHeader.from_dict({'HD':{'VN':'1.6','SO':'unsorted'},'SQ':[{'SN':'c1','LN':5000}],'RG':[{'ID':'g','SM':'s','LB':'l','PL':'ILLUMINA'}]})
import random; random.seed(3)
names=[f"q{i:03d}" for i in range(1,41)]; recs=[]
for n in names:
    for fl,pos in ((99,100),(147,300)):
        a=pysam.AlignedSegment(h); a.query_name=n; a.flag=fl; a.reference_id=0; a.reference_start=pos+random.randrange(0,3)
        a.mapping_quality=60; a.cigarstring='50M'; a.query_sequence=''.join(random.choice('ACGT') for _ in range(50)); a.query_qualities=pysam.qualitystring_to_array('I'*50)
        a.next_reference_id=0; a.next_reference_start=300 if fl==99 else 100; a.template_length=250 if fl==99 else -250; a.set_tag('RG','g'); a.set_tag('MC','50M')
        recs.append(a)
random.shuffle(recs)
with pysam.AlignmentFile('fw.bam','wb',header=h) as o:
    for r in recs: o.write(r)
EOP
samtools sort -n -o fw_n.bam fw.bam
picard ValidateSamFile -I fw_n.bam --MODE SUMMARY > v_fw.txt 2>&1; echo "  fixed-width -n output: $(so fw_n.bam)"; grep -a -E 'No errors|ERROR|RECORD' v_fw.txt | head -3
picard MarkDuplicates -I fw_n.bam -O fw_md.bam -M fw_md.txt > fw_md.log 2>&1; echo "  MarkDuplicates on fixed-width -n output rc=$? (0 = accepted although header says natural) $(grep -a -m1 -E 'out of order|Exception' fw_md.log | cut -c1-120)"

echo "### 2.6 Real name.sorted.bam from nf-core: which order?"
python $RUN/order_check.py $PD/human/test.paired_end.name.sorted.bam | grep -a -E 'HD|n='

echo "### 2.7 collate properties + FASTQ extraction (SKILL 'Paired FASTQ extraction', verbatim)"
samtools collate -O $PL tmp2 > collated.bam
echo "  collated @HD: $(so collated.bam)"
eq "QNAMEs appearing in >1 non-contiguous block" "$(samtools view collated.bam | cut -f1 | uniq | sort | uniq -d | wc -l)" "0"
eq "collate preserves record multiset" "$(recmd5 collated.bam)" "$(recmd5 $PL)"
samtools collate -O -u $PL tmp_prefix | \
    samtools fastq -1 R1.fq.gz -2 R2.fq.gz -0 /dev/null -s /dev/null -n - 2> fq.log; tail -2 fq.log
r1=$(zcat R1.fq.gz | awk 'NR%4==1' | wc -l); r2=$(zcat R2.fq.gz | awk 'NR%4==1' | wc -l)
eq "R1 reads == 250 pairs" "$r1" "250"; eq "R2 reads == 250 pairs" "$r2" "250"
zcat R1.fq.gz | awk 'NR%4==1' | tr -d '@' > r1.names; zcat R2.fq.gz | awk 'NR%4==1' | tr -d '@' > r2.names
cmp -s r1.names r2.names && echo "  [PASS] R1/R2 names pair in identical order" || echo "  [FAIL] R1/R2 names misordered"
summary
