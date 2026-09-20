#!/bin/bash
# Run the SKILL.md bash snippets VERBATIM (only file names substituted, "java -jar picard.jar" -> picard wrapper, same jar)
# and ASSERT on their printed output against independently computed truth.  Run in WSL via wsl_run.sh.
RUN=/mnt/openscience/audits/bio-alignment-validation/run
PD=/mnt/openscience/audit-envs/alignment-files/public-data
SN=$RUN/snip
W=$RUN/out/work            # scratch (deleted at the end)
G=$RUN/out/gen             # generated (substituted) copies of the snippets, kept as evidence
mkdir -p $W $G
cd $W
HUMAN=$RUN/data/idx/real_human_PE.bam            # indexed copy of the real human PE BAM
RNA=$RUN/data/idx/real_human_RNA.bam
G1K=$RUN/data/idx/real_1000g_chr20.bam
SE=$RUN/data/idx/real_sars_SE.bam
REF=$PD/human/genome.fasta
gen() {  # gen <snippet> <bam> <ref> -> $G/<snippet>.<tag>.sh
  local s=$1 b=$2 r=$3 tag=$4
  sed -e "s#java -jar picard.jar#picard#g" -e "s#in\.bam#$b#g" -e "s#input\.bam#$b#g" -e "s#ref\.fa#$r#g" -e "s#reference\.fa#$r#g" $SN/$s.txt > $G/$s.$tag.sh
  echo $G/$s.$tag.sh
}
A() { if [ "$2" = "1" ]; then echo "  ASSERT PASS: $1"; else echo "  ASSERT FAIL: $1"; fi; }

echo "================ T1  SKILL_02 CI one-liner (verbatim logic) ================"
for f in $RUN/data/ctl_valid.bam $RUN/data/no_eof.bam $RUN/data/trunc_tail.bam $RUN/data/bitflip_mid.bam $RUN/data/drop_block_mid.bam $RUN/data/orphans.bam $PD/sarscov2/test.paired_end.sorted.bam $PD/derived/planted_dups.bam /nonexistent.bam; do
  s=$(gen SKILL_02_bash $f $REF ci)
  out=$(bash $s 2>&1 | tail -1); rc=${PIPESTATUS[0]}
  rc=$(bash $s >/dev/null 2>&1; echo $?)
  echo "  $(basename $f): rc=$rc  last-line='$out'"
done
echo "  (ground truth: ctl_valid must PASS rc0; no_eof, trunc_tail, bitflip_mid must FAIL; drop_block_mid/orphans are corrupt but structurally decodable; the two sarscov2/planted files are VALID but only 200/500 reads)"

echo "================ T2  SKILL_01 quickcheck -v > fofn ================"
cd $RUN/data
s=$(gen SKILL_01_bash x.bam $REF qc)
samtools quickcheck -v ctl_valid.bam no_eof.bam trunc_tail.bam bitflip_mid.bam drop_block_mid.bam > $W/bad.fofn 2>/dev/null; echo "  rc=$? fofn contents: $(tr '\n' ' ' < $W/bad.fofn)"
cd $W

echo "================ T3  SKILL_03 M5 diff (verbatim) ================"
R=$RUN/data/ref
m5diff() { # bam ref
  diff <(samtools view -H $1 | grep '^@SQ' | tr '\t' '\n' | grep '^M5:' | sort) <(samtools dict $2 | grep '^@SQ' | tr '\t' '\n' | grep '^M5:' | sort) >$W/m5.out 2>&1; echo "rc=$? difflines=$(grep -c '^[<>]' $W/m5.out)"
}
echo "  human real BAM (NO M5 tags in header) vs its own reference genome.fasta:  $(m5diff $HUMAN $PD/human/genome.fasta)   <- truth: same sequence, should be 'no difference'"
echo "  BAM with M5 (header from ref_exact) vs ref_exact:      $(m5diff $R/bam_m5.bam $R/ref_exact.fa)   <- truth: identical"
echo "  BAM with M5 vs ref_softmask (lowercase 10 kb):         $(m5diff $R/bam_m5.bam $R/ref_softmask.fa)   <- truth: SKILL says M5 case-insensitive -> identical"
echo "  BAM with M5 vs ref_hardmask (first 1 kb -> N):         $(m5diff $R/bam_m5.bam $R/ref_hardmask.fa)   <- truth: differ"
echo "  BAM with M5 vs ref_onebase (one base changed):         $(m5diff $R/bam_m5.bam $R/ref_onebase.fa)   <- truth: differ"
echo "  BAM with M5 (SN chr22) vs ref_renamed (SN 22, same seq): $(m5diff $R/bam_m5.bam $R/ref_renamed.fa)   <- truth: names differ (downstream would break), M5 same; the diff cannot see names"
echo "  BAM two contigs, M5s SWAPPED between chrA/chrB vs correct ref_two: $(m5diff $R/bam_two_swapped.bam $R/ref_two.fa)   <- truth: wrong contig<->sequence assignment"
echo "  1000g real BAM (3366 contigs with M5) vs padded chr20 fasta (only chr20):  $(m5diff $G1K $PD/1000g/chr20_padded_1500000.fa)   <- truth: BAM is on full GRCh38, FASTA is a slice"
echo "  sarscov2 BAM (MT192765.1, no M5) vs human ref: $(m5diff $SE $PD/human/genome.fasta)   <- truth: different genome"

echo "================ T4  SKILL_05 samtools stats IS -> insert_sizes.txt ================"
s=$(gen SKILL_05_bash $HUMAN $REF is); bash $s >/dev/null 2>&1
echo "  insert_sizes.txt lines: $(wc -l < insert_sizes.txt); head: $(head -3 insert_sizes.txt | tr '\n' ' ')"
python - <<'PY'
import numpy as np, pysam
rows=[l.split() for l in open("insert_sizes.txt")]
sz=np.array([int(r[0]) for r in rows]); ct=np.array([int(r[1]) for r in rows])
mean_is=(sz*ct).sum()/ct.sum()
sizes=[]
with pysam.AlignmentFile("/mnt/openscience/audits/bio-alignment-validation/run/data/idx/real_human_PE.bam") as b:
    for r in b.fetch():
        if r.is_proper_pair and not r.is_secondary and r.template_length>0: sizes.append(r.template_length)
print(f"  IS-table mean {mean_is:.1f} (n={ct.sum()})  vs pysam mean {np.mean(sizes):.1f} (n={len(sizes)})")
print("  ASSERT", "PASS" if abs(mean_is-np.mean(sizes))<1.0 else "FAIL", ": samtools-stats IS table reproduces pysam insert-size mean (inward pairs only)")
PY

echo "================ T5  SKILL_06 Picard CollectInsertSizeMetrics (verbatim, java -jar -> picard, legacy KEY=VALUE) ================"
s=$(gen SKILL_06_bash $HUMAN $REF ins); bash $s >$W/ins.log 2>&1; echo "  rc=$?"
grep -E 'Exception|ERROR|Rscript|R script' $W/ins.log | head -3
ls -la insert_metrics.txt insert_histogram.pdf 2>&1 | awk '{print "  "$0}' | cut -c1-120
if [ -f insert_metrics.txt ]; then grep -A2 '^MEDIAN_INSERT_SIZE' insert_metrics.txt | cut -f1-6 | head -3; fi

echo "================ T6  SKILL_09 Calculate Pairing Rate (verbatim) vs flagstat ================"
for lab in "$HUMAN human_PE" "$RNA human_RNA" "$G1K 1000g" ; do
  set -- $lab; b=$1
  s=$(gen SKILL_09_bash $b $REF pr); out=$(bash $s 2>&1)
  fs=$(samtools flagstat $b | grep 'properly paired')
  echo "  $2: skill => $out | flagstat => $fs"
done

echo "================ T7  SKILL_12 Strand ratio (verbatim) vs the 0.48-0.52 table ================"
s=$(gen SKILL_12_bash $HUMAN $REF sr); bash $s 2>&1 | sed 's/^/  /'
echo "  (SKILL 'Strand Balance' text + 'Quality Thresholds Summary' say Good = 0.48-0.52; the snippet prints F/R, ~1.0 when balanced)"

echo "================ T8  SKILL_13 per-chromosome strand loop (verbatim: chr1 chr2 chr3) ================"
echo "  -- on human chr22-slice BAM (contig chr22 only):"; s=$(gen SKILL_13_bash $HUMAN $REF pc); bash $s 2>&1 | head -6 | sed 's/^/    /'
echo "  -- on 1000g BAM (header has chr1..; reads only on chr20):"; s=$(gen SKILL_13_bash $G1K $REF pc2); bash $s 2>&1 | head -6 | sed 's/^/    /'

echo "================ T9  SKILL_14/15 MAPQ distribution + mean MAPQ ================"
s=$(gen SKILL_14_bash $HUMAN $REF mq); bash $s 2>&1 | head -6 | sed 's/^/  /'
s=$(gen SKILL_15_bash $HUMAN $REF mq2); echo "  $(bash $s 2>&1)   (truth: mean over mapped only = $(samtools view -F 4 $HUMAN | awk '{s+=$5;n++} END{printf "%.2f", s/n}'))"
LM=$RUN/data/idx/planted_lowmap_placed.bam
s=$(gen SKILL_15_bash $LM $REF mq3); echo "  lowmap_placed: $(bash $s 2>&1)   (truth mean over mapped only = $(samtools view -F 4 $LM | awk '{s+=$5;n++} END{printf "%.2f", s/n}'))"

echo "================ T10 SKILL_16 idxstats awk (verbatim) ================"
s=$(gen SKILL_16_bash $HUMAN $REF ix); bash $s > $W/ix.out 2> $W/ix.err; echo "  rc=$? stdout: $(cat $W/ix.out | tr '\n' ';') stderr: $(head -2 $W/ix.err | tr '\n' ' ')"
echo "  idxstats itself: $(samtools idxstats $HUMAN | tr '\t' ' ' | tr '\n' ';')"

echo "================ T11 SKILL_17 aneuploidy awk (verbatim), gawk vs mawk ================"
s=$(gen SKILL_17_bash $G1K $REF an)
echo "  -- 1000g real BAM, gawk:"; bash $s 2>&1 | head -4 | sed 's/^/    /'
echo "  -- 1000g real BAM, mawk (Debian/Ubuntu default awk):"; sed 's#| awk#| /usr/bin/mawk#' $s > $G/SKILL_17_mawk.sh; echo "    mawk-substituted lines: $(grep -c mawk $G/SKILL_17_mawk.sh)"; bash $G/SKILL_17_mawk.sh 2>&1 | head -3 | sed 's/^/    /'
echo "  -- human BAM (single contig), gawk:"; s=$(gen SKILL_17_bash $HUMAN $REF an2); bash $s 2>&1 | head -3 | sed 's/^/    /'

echo "================ T12 SKILL_18 Picard CollectAlignmentSummaryMetrics (verbatim) ================"
s=$(gen SKILL_18_bash $HUMAN $REF as); bash $s >$W/as.log 2>&1; echo "  rc=$?"; grep -E 'Exception|ERROR' $W/as.log | head -3
python - <<'PY'
rows=[l.rstrip("\n").split("\t") for l in open("alignment_summary.txt") if not l.startswith("#") and l.strip()]
h=rows[0];
for r in rows[1:]:
    d=dict(zip(h,r)); print("  ",d["CATEGORY"],{k:d[k] for k in ("PCT_PF_READS_ALIGNED","PF_MISMATCH_RATE","PF_INDEL_RATE","STRAND_BALANCE") if k in d})
print("   names present in header:", all(k in h for k in ("PCT_PF_READS_ALIGNED","PF_MISMATCH_RATE","PF_INDEL_RATE","STRAND_BALANCE")))
PY

echo "================ T13 SKILL_10 Picard CollectGcBiasMetrics (verbatim) ================"
s=$(gen SKILL_10_bash $HUMAN $REF gc); bash $s >$W/gc.log 2>&1; echo "  rc=$?"; grep -E 'Exception|ERROR|R script|Rscript' $W/gc.log | head -3; ls gc_bias_metrics.txt gc_summary.txt gc_bias_chart.pdf 2>&1 | sed 's/^/  /'

echo "================ T14 SKILL_11 deepTools computeGCBias (verbatim flags; 2bit = human genome.2bit) ================"
sed -e "s#input\.bam#$HUMAN#" -e "s#hg38.2bit#$PD/human/genome.2bit#" $SN/SKILL_11_bash.txt > $G/SKILL_11_bash.gc.sh
bash $G/SKILL_11_bash.gc.sh >$W/cgc.log 2>&1; echo "  rc=$?"; tail -3 $W/cgc.log | cut -c1-200 | sed 's/^/  /'; ls gc_bias.txt gc_bias.pdf 2>&1 | sed 's/^/  /'

echo "================ T15 samtools view -s 42.01 (SKILL 'Python Validation Module' note) ================"
n_all=$(samtools view -c -F 2304 $HUMAN); n_s=$(samtools view -c -F 2304 -s 42.10 $HUMAN)
n_names=$(samtools view -F 2304 -s 42.10 $HUMAN | cut -f1 | sort | uniq -c | awk '$1!=2' | wc -l)
n_s2=$(samtools view -c -F 2304 -s 42.10 $HUMAN)
echo "  primary=$n_all subsample(-s 42.10)=$n_s repeat=$n_s2 names-not-in-both-mates=$n_names"
echo "  ASSERT $( [ "$n_s" = "$n_s2" ] && [ "$n_names" = 0 ] && echo PASS || echo FAIL): -s INT.FRAC is reproducible and keeps mates together"

echo "================ T16 contamination / swap commands: flag acceptance ================"
echo "  -- verifybamid2 with the SKILL's literal prefix pattern (1000g.b38.vcf.gz.SVD):"
verifybamid2 --SVDPrefix $PD/resources/1000g.b38.vcf.gz.SVD --Reference $PD/human/genome.fasta --BamFile $HUMAN --Output $W/vb1 2>&1 | grep -viE 'systemd' | head -4 | cut -c1-160 | sed 's/^/    /'
echo "  -- verifybamid2 with the real repo prefix ...1000g.phase3.10k.b38.vcf.gz.dat:"
verifybamid2 --SVDPrefix $PD/resources/1000g.phase3.10k.b38.vcf.gz.dat --Reference $PD/human/genome.fasta --BamFile $HUMAN --Output $W/vb2 2>&1 | grep -viE 'systemd' | tail -4 | cut -c1-160 | sed 's/^/    /'
echo "  -- somalier extract (flags -d -s -f as in SKILL) on human PE BAM:"
mkdir -p $W/extracted; somalier extract -d $W/extracted/ -s $PD/resources/somalier.sites.hg38.vcf.gz -f $PD/human/genome.fasta $HUMAN 2>&1 | tail -3 | cut -c1-160 | sed 's/^/    /'
echo "  -- somalier relate --infer (flag exists):"; somalier relate --help 2>&1 | grep -E '\-\-infer' | sed 's/^/    /'
echo "  -- picard CrosscheckFingerprints: HAPLOTYPE_MAP + I x2 accepted syntax (no map available: parse only)"
picard CrosscheckFingerprints I=$HUMAN I=$HUMAN HAPLOTYPE_MAP=/nonexistent.map 2>&1 | grep -E 'Exception|Unrecognized|Invalid|Cannot|not found|No such' | head -2 | cut -c1-160 | sed 's/^/    /'

echo "================ T17 usage-guide 'Comprehensive Validator' class vs truth ================"
python - <<'PY'
import re, sys, io, contextlib
src=open("/mnt/openscience/audits/bio-alignment-validation/run/snip/usage-guide_08_python.txt",encoding="utf-8").read()
ns={}; exec(src, ns)
V=ns["AlignmentValidator"]
D="/mnt/openscience/audits/bio-alignment-validation/run/data/idx/"
for lab,fn,truth in [("human_PE","real_human_PE.bam","mapped 99.96 (5642/5642 primary+2 unplaced unmapped)"),("lowmap_unplaced","planted_lowmap_unplaced.bam","mapped 70.0"),("lowmap_placed","planted_lowmap_placed.bam","mapped 70.0")]:
    v=V(D+fn); buf=io.StringIO()
    with contextlib.redirect_stdout(buf):
        r=v.report()
    v.close()
    print(f"  {lab}: return={r!r}; printed: {buf.getvalue().strip().splitlines()[0]} | truth: {truth}")
PY
echo "================ done ================"
