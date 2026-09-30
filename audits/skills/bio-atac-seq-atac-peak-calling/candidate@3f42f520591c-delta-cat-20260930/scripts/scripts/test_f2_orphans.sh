#!/usr/bin/env bash
# Delta test for ATACPC-016: does `samtools view -b -f 2` after the documented idxstats chrM
# recipe remove chr1 reads whose mate maps to chrM, and keep intact pairs?
# Flags come from real aligners (bowtie2 --very-sensitive -X 2000, and bwa mem), not hand-set.
# Reference: real hg38 chr1:10,000,001-10,300,000 named chr1 + a synthetic random 16,569 bp chrM.
# Skill tools (samtools, macs3) run from the Skill env bio-atac-seq-atac-peak-calling;
# aligners from env alignment-files (binaries executed only, env not modified).
set -uo pipefail
export MAMBA_ROOT_PREFIX=/home/sci/micromamba PYTHONDONTWRITEBYTECODE=1
SK=/home/sci/micromamba/envs/bio-atac-seq-atac-peak-calling/bin
AL=/home/sci/micromamba/envs/alignment-files/bin
export PATH=$SK:$PATH
LOGDIR=/mnt/openscience/audits/bio-atac-seq-atac-peak-calling/delta-cat-20260930/logs
W=/home/sci/delta-cat-20260930-apc
rm -rf "$W"; mkdir -p "$W"; cd "$W"
exec > "$W/run.log" 2>&1   # log written on ext4, copied to LOGDIR at the end (drvfs redirect truncated an earlier attempt)
REF=/mnt/openscience/audit-envs/atac-seq/public-data/reference/hg38.chr1.fa

echo "samtools: $(samtools --version | head -1)"; echo "macs3: $(macs3 --version)"
echo "bowtie2: $($AL/bowtie2 --version 2>/dev/null | head -1)"; echo "bwa: $($AL/bwa 2>&1 | grep Version)"

python3 - "$REF" <<'PY'
import random, sys
random.seed(20260930)
# real chr1 slice
seq = []
take = False
start, end = 10_000_000, 10_300_000
pos = 0
with open(sys.argv[1]) as f:
    for line in f:
        if line.startswith('>'):
            take = line[1:].split()[0] == 'chr1'; continue
        if not take: continue
        s = line.strip(); n = len(s)
        if pos + n > start and pos < end:
            a = max(0, start - pos); b = min(n, end - pos); seq.append(s[a:b])
        pos += n
        if pos >= end: break
chr1 = ''.join(seq).upper()
assert len(chr1) == end - start, len(chr1)
chrM = ''.join(random.choice('ACGT') for _ in range(16569))
with open('ref.fa', 'w') as o:
    for name, s in (('chr1', chr1), ('chrM', chrM)):
        o.write(f'>{name}\n')
        for i in range(0, len(s), 60): o.write(s[i:i+60] + '\n')
def rc(s): return s[::-1].translate(str.maketrans('ACGTN', 'TGCAN'))
def ok(s): return s.count('N') == 0
R = 50
peaks = [20_000 + i * 25_000 for i in range(10)]  # 10 accessible sites on chr1
r1, r2 = open('r1.fq', 'w'), open('r2.fq', 'w')
def emit(name, a, b):
    q = 'I' * R
    r1.write(f'@{name}/1\n{a}\n+\n{q}\n'); r2.write(f'@{name}/2\n{b}\n+\n{q}\n')
n = {'conc': 0, 'chrM': 0, 'disc': 0}
# concordant chr1 fragments at peaks (NFR-sized) plus background
while n['conc'] < 3000:
    if random.random() < 0.8:
        c = random.choice(peaks) + int(random.gauss(0, 60)); L = random.randint(60, 180)
    else:
        c = random.randint(1000, len(chr1) - 1000); L = random.randint(60, 600)
    s = c - L // 2; frag = chr1[s:s + L]
    if len(frag) < L or not ok(frag): continue
    emit(f'conc{n["conc"]}', frag[:R], rc(frag)[:R]); n['conc'] += 1
# chrM pairs
while n['chrM'] < 400:
    L = random.randint(60, 400); s = random.randint(0, len(chrM) - L - 1); frag = chrM[s:s + L]
    emit(f'chrM{n["chrM"]}', frag[:R], rc(frag)[:R]); n['chrM'] += 1
# discordant pairs: R1 on chr1 inside a peak, R2 on chrM (chimeric / NUMT-like)
while n['disc'] < 60:
    c = random.choice(peaks) + int(random.gauss(0, 40)); a = chr1[c:c + R]
    m = random.randint(0, len(chrM) - R - 1); b = rc(chrM[m:m + R])
    if not ok(a): continue
    emit(f'disc{n["disc"]}', a, b); n['disc'] += 1
print('simulated pairs', n)
PY

$SK/samtools faidx ref.fa
$AL/bowtie2-build -q ref.fa ref >/dev/null
$AL/bwa index ref.fa 2>/dev/null

for A in bt2 bwa; do
  echo; echo "######## aligner: $A"
  if [ $A = bt2 ]; then
    $AL/bowtie2 --very-sensitive -X 2000 -x ref -1 r1.fq -2 r2.fq 2>$A.align.log | samtools sort -o $A.bam -
  else
    $AL/bwa mem -v 1 ref.fa r1.fq r2.fq 2>$A.align.log | samtools sort -o $A.bam -
  fi
  samtools index $A.bam
  echo "idxstats:"; samtools idxstats $A.bam
  echo "discordant disc* reads by flag (proper-pair bit 0x2 set?):"
  samtools view $A.bam | awk '$1 ~ /^disc/ {k=$3"->"($7=="="?$3:$7)" proper="(and($2,2)?1:0); c[k]++} END{for(k in c) print "  "k, c[k]}'
  echo "concordant conc* reads with proper bit set / total:"
  samtools view $A.bam | awk '$1 ~ /^conc/ && !and($2,4) {t++; if(and($2,2)) p++} END{print "  "p"/"t}'

  # Documented recipe (usage-guide.md), verbatim apart from file names
  samtools idxstats $A.bam | cut -f1 | grep -v -e '^chrM$' -e '^\*$' | xargs samtools view -b -o $A.noM.bam $A.bam
  samtools index $A.noM.bam
  orph=$(samtools view $A.noM.bam | awk '$7=="chrM"' | wc -l)
  echo "after recipe: reads=$(samtools view -c $A.noM.bam) chrM_reads=$(samtools view -c $A.noM.bam chrM 2>/dev/null || echo 0) orphans_mate_on_chrM=$orph"
  # Documented follow-up: keep proper pairs only
  samtools view -b -f 2 -o $A.noM.f2.bam $A.noM.bam; samtools index $A.noM.f2.bam
  orph2=$(samtools view $A.noM.f2.bam | awk '$7=="chrM"' | wc -l)
  unpaired=$(samtools view $A.noM.f2.bam | cut -f1 | sort | uniq -c | awk '$1!=2' | wc -l)
  hdr=$(samtools view -H $A.noM.f2.bam | grep -c '^@SQ')
  echo "after -f 2: reads=$(samtools view -c $A.noM.f2.bam) orphans_mate_on_chrM=$orph2 names_not_seen_exactly_twice=$unpaired @SQ_lines=$hdr"
  echo "concordant pairs lost by -f 2: $(( $(samtools view -c $A.noM.bam) - $(samtools view -c $A.noM.f2.bam) - orph )) reads beyond the orphans"

  for B in noM noM.f2; do
    macs3 callpeak -t $A.$B.bam -f BAMPE -g 3e5 -n ${A}_$B --outdir macs_$A --keep-dup all -q 0.05 >macs_${A}_$B.log 2>&1
    rc=$?
    frags=$(grep -m1 -E 'total fragments in treatment' macs_${A}_$B.log | sed 's/.*INFO  @ [^:]*: *//')
    echo "macs3 callpeak BAMPE on $B: rc=$rc peaks=$(wc -l < macs_$A/${A}_${B}_peaks.narrowPeak 2>/dev/null) $frags"
    grep -iE 'error|warn|mate|unpaired|pair' macs_${A}_$B.log | grep -v -i 'paired-end' | head -3 | sed 's/^/    /'
  done
  for B in noM noM.f2; do
    macs3 hmmratac -i $A.$B.bam -f BAMPE -n hmm_${A}_$B --outdir hmm_$A >hmm_${A}_$B.log 2>&1
    rc=$?
    echo "macs3 hmmratac BAMPE on $B: rc=$rc regions=$(cat hmm_$A/hmm_${A}_${B}_accessible_regions.narrowPeak 2>/dev/null | wc -l)  last: $(tail -1 hmm_${A}_$B.log | cut -c1-160)"
  done
done
cp -f bt2.align.log bwa.align.log macs_*.log hmm_*.log "$LOGDIR"/ 2>/dev/null
mkdir -p "$LOGDIR/f2_fixture"; cp -f bt2.bam bt2.noM.bam bt2.noM.f2.bam bwa.noM.bam bwa.noM.f2.bam "$LOGDIR/f2_fixture/"
echo DONE
cp -f "$W/run.log" "$LOGDIR/test_f2_orphans.log"
