#!/bin/bash
# Why does the BAM->CRAM->BAM round trip differ record-by-record? Diff the SAM text.
cd /mnt/openscience/audits/bio-sam-bam-basics/run/data/conv
REF=$AFDATA/human/genome.fasta
samtools view $AFDATA/human/test.paired_end.sorted.bam > a.txt
samtools view -T $REF o.cram > b.txt
wc -l a.txt b.txt
diff <(cut -f1-11 a.txt) <(cut -f1-11 b.txt) | head -3; echo "core fields (1-11) diff lines: $(diff <(cut -f1-11 a.txt) <(cut -f1-11 b.txt) | wc -l)"
echo "--- record 1 original tags:"; head -1 a.txt | cut -f12-
echo "--- record 1 CRAM->text tags:"; head -1 b.txt | cut -f12-
echo "--- tag SET equality per record (sorted tag lists):"
python - <<'EOF'
a=[l.rstrip('\n').split('\t') for l in open('a.txt')]
b=[l.rstrip('\n').split('\t') for l in open('b.txt')]
same_set=sum(1 for x,y in zip(a,b) if sorted(x[11:])==sorted(y[11:]))
same_order=sum(1 for x,y in zip(a,b) if x[11:]==y[11:])
core=sum(1 for x,y in zip(a,b) if x[:11]==y[:11])
print('records',len(a),len(b),'core fields identical',core,'tag SET identical',same_set,'tag ORDER identical',same_order)
import collections
d=collections.Counter()
for x,y in zip(a,b):
    if sorted(x[11:])!=sorted(y[11:]):
        for t in set(x[11:])^set(y[11:]): d[t.split(':')[0]]+=1
print('tags differing:',dict(d))
EOF
