#!/bin/bash
# Small-edge battery for the fixed validators + static syntax checks (no __pycache__ written).
RUN=/mnt/openscience/audits/bio-alignment-validation/run; PD=/mnt/openscience/audit-envs/alignment-files/public-data
PY=$RUN/skill/examples/validate_alignment.py; SH=$RUN/skill/examples/validate_alignment.sh
W=$RUN/out/work_v3; rm -rf $W; mkdir -p $W; cd $W
HUM=$PD/human/test.paired_end.sorted.bam
one() { python $PY "$2" > py.out 2> py.err; p=$?; bash $SH "$2" > sh.out 2> sh.err; s=$?
  echo "  [$1] py rc=$p '$(grep -E '^(FAIL|WARN):|All metrics' py.out | head -1)' | sh rc=$s '$(grep -E '^(FAIL|WARN):|All metrics' sh.out | head -1)' | truth: $2 -> primary $(samtools view -c -F 2304 $2 2>/dev/null) mapped $(samtools view -c -F 2308 $2 2>/dev/null)"; }
samtools view -b -f 4 $HUM > allunm.bam 2>/dev/null; one "all-unmapped BAM with @SQ (2 reads)" allunm.bam
samtools view -b $HUM chr22:1952-1960 2>/dev/null | samtools view -b -s 1.001 - > /dev/null 2>&1
samtools view -H $HUM > h.sam; samtools view $HUM | head -1 >> h.sam; samtools view -b h.sam > one.bam; one "single mapped read (unpaired flags off? one read of a pair)" one.bam
samtools view -H $HUM > h2.sam; samtools view $HUM | head -2 >> h2.sam; samtools view -b h2.sam > two.bam; one "two reads" two.bam
python - <<'PY'
# static checks without writing __pycache__
import ast,sys
src=open("/mnt/openscience/audits/bio-alignment-validation/run/skill/examples/validate_alignment.py",encoding="utf-8").read()
ast.parse(src); print("  ast.parse validate_alignment.py: OK")
PY
bash -n $SH && echo "  bash -n validate_alignment.sh: OK"
which shellcheck >/dev/null 2>&1 && shellcheck -S warning $SH | head -20 || echo "  shellcheck not installed"
find $RUN/skill -name __pycache__ | wc -l | sed 's/^/  __pycache__ dirs under run\/skill: /'
