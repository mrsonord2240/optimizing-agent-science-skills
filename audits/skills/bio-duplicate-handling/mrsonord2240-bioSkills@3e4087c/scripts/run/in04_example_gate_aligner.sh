#!/bin/bash
# Input 4 (variant B, regression of pre-fix input 5): the fixer's rewritten examples/markdup_pipeline.sh, run from the COPY.
# Asserts by output: a VALID run exits 0 with truth counts + index + stats beside the output; every failing run exits non-zero and leaves no
# half-written out.bam; the assay gate refuses. Then the "Alternative: From Aligner" bwa-mem2 -R | samblaster block (verbatim) on 100 real
# pairs + 20 SYNTHETIC clone pairs, and Picard on its output (the pre-fix block had no @RG and Picard NPE'd).
source /mnt/openscience/audit-envs/alignment-files/wsl_env.sh
source /mnt/openscience/audits/bio-duplicate-handling/run/common.sh
cd $W; rm -rf in04; mkdir in04; cd in04
EX=$SK/examples/markdup_pipeline.sh
bash -n $EX && echo "[bash -n OK]"; ls -l $EX | awk '{print $1, $5}'
run() { # name, env-assay, input, output, [threads] -> prints exit code
  local nm=$1 assay=$2 in=$3 out=$4 th=${5:-}
  ASSAY=$assay bash $EX $in $out $th > $nm.out 2> $nm.err; local rc=$?
  echo "  [$nm] exit=$rc  out exists: $([ -e $out ] && echo yes || echo no)"
  return 0
}
echo "== 4a valid runs (ASSAY=wgs), truth: planted 100, human 1656"
run planted wgs $D/planted_dups.bam p_out.bam 2
echo "     flagged $(flagged p_out.bam)  records $(samtools view -c p_out.bam)/$(samtools view -c $D/planted_dups.bam)  index: $(ls p_out.bam.bai 2>&1)  stats: $(ls p_out.markdup_stats.txt 2>&1) ($(grep -c 'DUPLICATE TOTAL' p_out.markdup_stats.txt) DUP TOTAL lines)  cwd stray files: $(ls | grep -c '^markdup_stats.txt$')"
grep -E 'total|duplicates' planted.out
run human wgs $D/test.paired_end.sorted.bam h_out.bam
echo "     flagged $(flagged h_out.bam)  records $(samtools view -c h_out.bam)/5644  index: $(ls h_out.bam.bai 2>&1)"
echo "== 4b OPTICAL_DIST=100 override and threads arg"
OPTICAL_DIST=100 ASSAY=wes bash $EX $D/planted_dups.bam o100.bam 1 > o100.out 2>&1; echo "  exit=$? flagged $(flagged o100.bam); header line: $(head -1 o100.out)"
echo "== 4c failure modes: exit must be non-zero and no half-written output"
run missing wgs nonexistent.bam m_out.bam; head -c 300 missing.err | grep -m1 -iE 'fail|error|no such'
head -c 6000 $D/test.paired_end.sorted.bam > trunc.bam
run trunc wgs trunc.bam t_out.bam; grep -m1 -iE 'truncat|fail|error' trunc.err
samtools view -H -b $D/planted_dups.bam > empty.bam 2>/dev/null || samtools view -H $D/planted_dups.bam | samtools view -b -o empty.bam -
echo "  (empty.bam records: $(samtools view -c empty.bam))"
run empty wgs empty.bam e_out.bam; cat empty.err | head -2
mkdir -p ro; chmod 555 ro
run unwritable wgs $D/planted_dups.bam ro/x.bam; grep -m1 -iE 'permission|cannot|fail|error' unwritable.err; chmod 755 ro
run nodir wgs $D/planted_dups.bam nonexist_dir/x.bam; grep -m1 -iE 'no such|cannot|fail|error' nodir.err
echo "== 4d assay gate: unset / refused assays (exit 2), unknown assay"
env -u ASSAY bash $EX $D/planted_dups.bam g0.bam > g0.out 2> g0.err; echo "  ASSAY unset: exit=$? out exists: $([ -e g0.bam ] && echo yes || echo no): $(head -1 g0.err)"
for a in rnaseq scrna umi amplicon longread 16s its bogus; do
  ASSAY=$a bash $EX $D/planted_dups.bam g_$a.bam > /dev/null 2> g_$a.err; echo "  ASSAY=$a: exit=$? out exists: $([ -e g_$a.bam ] && echo yes || echo no)"
done
echo "== 4e wrong-assay detection: amplicon BAM declared as wgs -> >50% warning (SYNTHETIC amplicon BAM: 10 amplicons x 100 pairs)"
python $RUN/00b_make_synth2.py > /dev/null
ASSAY=wgs bash $EX $D/synth_amplicon.bam a_out.bam > a.out 2> a.err; echo "  exit=$? flagged $(flagged a_out.bam)/2000"; grep -i warning a.err
echo "== 4f real RNA-seq BAM under ASSAY=wgs (user mis-declares): does anything warn? (38% flagged, below the 50% threshold)"
ASSAY=wgs bash $EX $D/test.rna.paired_end.sorted.bam r_out.bam > r.out 2> r.err; echo "  exit=$? flagged $(flagged r_out.bam)/$(samtools view -c r_out.bam); warnings: $(grep -c WARNING r.err)"
echo "== 4g real single-end long-read (ARTIC nanopore) BAM under ASSAY=pacbio-amplicon (the gate allows it)"
ASSAY=pacbio-amplicon bash $EX $D/sars-cov-2_v5.3.2.nanopore.bam n_out.bam > n.out 2> n.err; echo "  exit=$? flagged $(flagged n_out.bam)/$(samtools view -c n_out.bam 2>/dev/null); $(grep -m2 -iE 'warning|error' n.err | tr '\n' '|')"

echo "== 4h 'Alternative: From Aligner' bwa-mem2 -R | samblaster | sort block, verbatim, on 100 real pairs + 20 SYNTHETIC clone pairs"
P=/mnt/openscience/audit-envs/alignment-files/public-data/sarscov2
mkdir -p al; cd al
cp $D/genome.fasta ref.fa
python - <<PY
import gzip
for n in (1, 2):
    with gzip.open("$D/test_%d.fastq.gz" % n, "rt") as f: lines = f.read().splitlines()
    recs = [lines[i:i+4] for i in range(0, len(lines), 4)]
    out = open("R%d.fq" % n, "w")
    for r in recs: out.write("\n".join(r) + "\n")
    for i, r in enumerate(recs[:20]):
        out.write("\n".join([r[0].split()[0] + "_clone%d" % i, r[1], r[2], r[3]]) + "\n")
print("R1/R2: 100 real pairs + 20 SYNTHETIC clone pairs (truth 40 flagged reads)")
PY
bwa-mem2 index ref.fa >/dev/null 2>&1
blk "### BWA-MEM2 with samblaster" 1 > aln.sh
echo "[extracted block]"; cat aln.sh
bash -o pipefail aln.sh 2>/dev/null; echo "exit=$?"
echo "  @RG in header: $(samtools view -H marked.bam | grep -c '^@RG'); records $(samtools view -c marked.bam); flagged $(flagged marked.bam); flagged names that are clones: $(samtools view -f 1024 marked.bam | cut -f1 | grep -c clone)"
blk "### Picard MarkDuplicates" 1 | sed 's#java -jar picard.jar#picard#; s#I=input.bam#I=marked.bam#; s#O=marked.bam#O=pic_out.bam#' > pic.sh
cat pic.sh | head -3
bash pic.sh >/dev/null 2>pic.err; echo "  picard on the -R aligner output: exit=$? flagged $(flagged pic_out.bam) ; library in metrics: $(grep -A1 '^LIBRARY' metrics.txt | tail -1 | cut -f1-2 | tr '\t' ' ')"
