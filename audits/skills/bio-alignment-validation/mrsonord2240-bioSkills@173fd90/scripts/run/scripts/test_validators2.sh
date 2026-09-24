#!/bin/bash
# Re-auditor's own validator battery for the FIXED examples: exit-code contract, verdict/rc agreement, odd inputs, CRAM,
# spaces in paths, -n sampling, speed on a large file, determinism.  Run in WSL.
RUN=/mnt/openscience/audits/bio-alignment-validation/run
PD=/mnt/openscience/audit-envs/alignment-files/public-data
PY=$RUN/skill/examples/validate_alignment.py
SH=$RUN/skill/examples/validate_alignment.sh
W=$RUN/out/work_v; rm -rf $W; mkdir -p "$W/sp dir"; cd $W
HUM=$PD/human/test.paired_end.sorted.bam
REF=$PD/human/genome.fasta
one() { # label file  -> prints rc/verdict/mapped/stderr-lines for both validators
  local lab="$1" f="$2"
  python $PY "$f" > py.out 2> py.err; prc=$?; bash $SH "$f" > sh.out 2> sh.err; src=$?
  pv=$(grep -E '^(FAIL|WARN):|All metrics' py.out | head -1); sv=$(grep -E '^(FAIL|WARN):|All metrics' sh.out | tail -2 | head -1)
  echo "  [$lab] py rc=$prc '$pv' map=$(grep -m1 '^Mapped' py.out | grep -o '([0-9.]*%)') err=$(grep -c . py.err):$(head -1 py.err | cut -c1-110) | sh rc=$src '$sv' map=$(grep -m1 '^Mapped' sh.out | grep -o '([0-9.]*%)') err=$(grep -c . sh.err):$(head -1 sh.err | cut -c1-110)"
}
echo "== B. odd inputs (contract: 2 = unreadable/empty, single stderr line, no traceback)"
cp $HUM "$W/sp dir/my sample.bam"; one "path with spaces" "$W/sp dir/my sample.bam"
one "missing file" /nonexistent.bam
: > zero.bam; one "zero-byte file" zero.bam
mkdir adir; one "a directory" adir
head -c 5000 /dev/urandom > junk.bam; one "random bytes named .bam" junk.bam
samtools view -h $HUM > plain.sam; one "SAM text input" plain.sam
gzip -c plain.sam > plain.sam.gz; one "gzipped SAM" plain.sam.gz
python $PY > noargs.out 2> noargs.err; echo "  [no args] py rc=$? $(head -c 120 noargs.err | tr '\n' ' ')"; bash $SH > /dev/null 2> na.err; echo "  [no args] sh rc=$? $(head -1 na.err)"
python $PY $HUM -n 1000 > n.out 2>&1; echo "  [-n 1000] rc=$? $(head -1 n.out)"
python $PY $HUM -n 0 > n0.out 2>&1; echo "  [-n 0 = whole] rc=$? $(head -1 n0.out)"
python $PY $HUM -n -5 > nneg.out 2>&1; echo "  [-n -5] rc=$? $(head -2 nneg.out | tr '\n' '/')"
echo "== C. -n bias claim: lowmap_unplaced (true 70.01% mapped; coordinate-sorted, unplaced tail) with -n 1000"
python $PY $RUN/data/lowmap_unplaced.bam -n 1000 2>&1 | grep -E '===|^Mapped|^FAIL|^WARN|All metrics'; echo "  rc=${PIPESTATUS[0]}"
echo "== D. CRAM (real nf-core CRAM, UR points at a non-existent path)"
CR=$PD/human/test.paired_end.sorted.cram
unset REF_PATH REF_CACHE
export REF_PATH=/nonexistent_ref_dir
one "CRAM, no reference resolvable" $CR
# populate an md5-named REF_PATH cache from the FASTA (samtools' documented cache layout)
mkdir -p refcache; python - <<'PY'
import hashlib
seq="".join(l.strip() for l in open("/mnt/openscience/audit-envs/alignment-files/public-data/human/genome.fasta") if not l.startswith(">")).upper()
m=hashlib.md5(seq.encode()).hexdigest(); print("  md5 of chr22 slice:",m)
import os; os.makedirs(f"refcache/{m[:2]}/{m[2:4]}",exist_ok=True); open(f"refcache/{m[:2]}/{m[2:4]}/{m[4:]}","w").write(seq)
PY
export REF_PATH="$W/refcache/%2s/%2s/%s"
one "CRAM with REF_PATH cache (md5 layout)" $CR
samtools view -C -T $REF --output-fmt-option embed_ref=1 -o embed.cram $HUM 2>/dev/null; export REF_PATH=/nonexistent_ref_dir
one "CRAM with embedded reference (self-contained)" embed.cram
echo "  truth for the CRAM: $(samtools flagstat -@0 $HUM | grep 'primary mapped')"
unset REF_PATH
echo "== H. determinism (identical stdout on repeat)"
python $PY $HUM > d1.out 2>&1; python $PY $HUM > d2.out 2>&1; bash $SH $HUM > d3.out 2>&1; bash $SH $HUM > d4.out 2>&1
echo "  py md5: $(md5sum < d1.out | cut -c1-8) $(md5sum < d2.out | cut -c1-8); sh md5: $(md5sum < d3.out | cut -c1-8) $(md5sum < d4.out | cut -c1-8)"
echo "== G. speed on a large file (samtools cat of the real human PE BAM, valid, not sorted)"
for n in 200 1000; do
  samtools cat $(for i in $(seq 1 $n); do echo $HUM; done) -o big$n.bam 2>/dev/null
  recs=$(samtools view -c big$n.bam); sz=$(du -m big$n.bam | cut -f1)
  s=$(date +%s.%N); /usr/bin/time -f "  py peak RSS %M KB" python $PY big$n.bam > bigpy.out 2> bigpy.err; prc=$?; e=$(date +%s.%N)
  echo "  big$n.bam: $recs records, ${sz} MB | py rc=$prc wall $(python -c "print(round($e-$s,1))") s | $(cat bigpy.err | tail -1) | $(grep -m1 '^Mapped' bigpy.out)"
  s=$(date +%s.%N); bash $SH big$n.bam > bigsh.out 2> bigsh.err; src=$?; e=$(date +%s.%N)
  echo "  big$n.bam: sh rc=$src wall $(python -c "print(round($e-$s,1))") s | $(grep -m1 '^Mapped' bigsh.out)"
  s=$(date +%s.%N); samtools flagstat big$n.bam > /dev/null; e=$(date +%s.%N); echo "  reference: samtools flagstat alone $(python -c "print(round($e-$s,1))") s"
done
python $PY big1000.bam -n 100000 > bign.out 2>&1; echo "  old default (-n 100000) on big1000: $(head -1 bign.out)"
rm -f big200.bam big1000.bam
echo "== done"
