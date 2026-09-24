#!/bin/bash
# Run every runnable SKILL.md block of the FIXED Skill (extracted verbatim into run/snip by extract_snippets.py; only file
# names substituted: in.bam / input.bam / ref.fa / reference.fa / sample.bam) and ASSERT on their printed output against an
# independently computed truth (samtools flagstat, pysam, samtools calmd, Picard).  Run in WSL:
#   bash test_snippets.sh > ../out/test_snippets.txt 2>&1
RUN=/mnt/openscience/audits/bio-alignment-validation/run
PD=/mnt/openscience/audit-envs/alignment-files/public-data
SN=$RUN/snip
W=$RUN/out/work; rm -rf $W; mkdir -p $W $RUN/out/gen; G=$RUN/out/gen
cd $W
HUM=$PD/human/test.paired_end.sorted.bam
HUMN=$PD/human/test.paired_end.name.sorted.bam
RNA=$PD/human/test.rna.paired_end.sorted.bam
G1K=$PD/1000g/HG00349.chr20_1400000-1500000.bam
REF=$PD/human/genome.fasta
NEW=$RUN/data/new
gen() { # gen <snippet> <bam> <ref> <tag> -> path of substituted copy
  sed -e "s#in\.bam#$2#g" -e "s#input\.bam#$2#g" -e "s#sample\.bam#$2#g" -e "s#ref\.fa#$3#g" -e "s#reference\.fa#$3#g" $SN/$1.txt > $G/$1.$4.sh; echo $G/$1.$4.sh; }
A() { if [ "$2" = "1" ]; then echo "  ASSERT PASS: $1"; else echo "  ASSERT FAIL: $1"; fi; }

echo "=== T01 SKILL_01 quickcheck (file check + fofn)"
D=$RUN/data
out=$(samtools quickcheck -v $D/ctl_valid.bam $D/no_eof.bam $D/trunc_tail.bam $D/bitflip_mid.bam 2>/dev/null); rc=$?
echo "  -v output: $(echo $out | sed 's#[^ ]*/##g'); rc=$rc"
A "fofn lists exactly the two quickcheck-detectable files (no_eof, trunc_tail); rc non-zero (quickcheck uses rc 16)" "$([ "$(echo "$out" | sed 's#.*/##' | sort | tr '\n' ' ')" = "no_eof.bam trunc_tail.bam " ] && [ $rc != 0 ] && echo 1)"

echo "=== T02 SKILL_02 CI one-liner, default MIN_READS and MIN_READS=1000"
ci() { sed "s#in\.bam#$1#g" $SN/SKILL_02_bash.txt > $G/ci.sh; if [ -n "$2" ]; then MIN_READS=$2 bash $G/ci.sh >/dev/null 2>&1; else bash $G/ci.sh >/dev/null 2>&1; fi; echo $?; }
for f in $HUM $PD/sarscov2/test.single_end.sorted.bam $PD/sarscov2/test.paired_end.sorted.bam $PD/derived/planted_dups.bam $G1K; do
  r=$(ci $f); echo "  valid $(basename $f) ($(samtools view -c -F 2304 $f) primary): rc=$r"; A "valid file passes" "$([ $r = 0 ] && echo 1)"; done
for f in no_eof trunc_tail bitflip_mid cigar_seq_mismatch empty_records no_sq_unmapped; do r=$(ci $D/$f.bam); A "$f fails (rc 1)" "$([ $r = 1 ] && echo 1)"; done
r=$(ci $PD/derived/planted_dups.bam 1000); A "MIN_READS=1000 on the 500-read file fails" "$([ $r = 1 ] && echo 1)"
r=$(ci $HUM 5000); A "MIN_READS=5000 on 5642 primary passes" "$([ $r = 0 ] && echo 1)"
r=$(ci "/nonexistent/x.bam"); A "missing file fails" "$([ $r = 1 ] && echo 1)"
r=$(ci "$NEW/n_all_secondary.bam"); A "all-secondary BAM fails (0 primary < MIN_READS 1)" "$([ $r = 1 ] && echo 1)"
mkdir -p "$W/sp dir"; cp $HUM "$W/sp dir/my sample.bam"; r=$(ci "$W/sp dir/my sample.bam"); echo "  (info only: the block is a template with an unquoted in.bam; a spaced path must be quoted by the user. The shipped validators quote their variables and handle spaces, see test_validators2.sh. rc unquoted=$r)"

echo "=== T03 SKILL_03 dictionary diff, M5/SN/LN"
R=$RUN/data/ref
d() { sed -e "s#in\.bam#$1#g" -e "s#ref\.fa#$2#g" $SN/SKILL_03_bash.txt > $G/dict.sh; bash $G/dict.sh > $W/d.out 2>&1; rc=$?; echo "rc=$rc msg=$(head -2 $W/d.out | tr '\n' '/')"; return $rc; }
chk() { # label bam ref expected_rc
  res=$(d $2 $3); rc=$?; echo "  $1: $res"; A "$1 -> rc $4" "$([ $rc = $4 ] && echo 1)"; }
chk "BAM with M5 vs identical ref"               $R/bam_m5.bam $R/ref_exact.fa 0
chk "soft-masked ref (lowercase)"                $R/bam_m5.bam $R/ref_softmask.fa 0
chk "hard-masked ref (first 1kb N)"              $R/bam_m5.bam $R/ref_hardmask.fa 1
chk "one base changed"                           $R/bam_m5.bam $R/ref_onebase.fa 1
chk "renamed contig (chr22 -> 22)"               $R/bam_m5.bam $R/ref_renamed.fa 1
chk "two contigs M5-swapped"                     $R/bam_two_swapped.bam $R/ref_two.fa 1
chk "real human BAM (no M5) vs its FASTA"        $HUM $REF 0
grep -q "no M5 in BAM header" $W/d.out && A "the no-M5 notice is printed" 1 || A "the no-M5 notice is printed" 0
chk "1000G BAM (GRCh38 full header) vs 1.5Mb chr20 slice FASTA" $G1K $PD/1000g/chr20_padded_1500000.fa 1
chk "sarscov2 nanopore BAM (MN908947.3) vs MN908947.3.fasta" $PD/sarscov2/sars-cov-2_v5.3.2.nanopore.bam $PD/sarscov2/MN908947.3.fasta 0
chk "sarscov2 PE BAM (MT192765.1) vs MN908947.3.fasta (contig-name trap from public-data README)" $PD/sarscov2/test.paired_end.sorted.bam $PD/sarscov2/MN908947.3.fasta 1
chk "sarscov2 PE BAM vs genome.fasta (MT192765.1)" $PD/sarscov2/test.paired_end.sorted.bam $PD/sarscov2/genome.fasta 0
chk "sarscov2 BAM vs human ref (different genome)" $PD/sarscov2/test.single_end.sorted.bam $REF 1
# NEW: same names, LN differs by 1 (reference with one extra base at the end); ref is a SUPERSET (extra contig) of the BAM
python - <<'PY'
R="/mnt/openscience/audits/bio-alignment-validation/run/data/ref/"
s=[l.strip() for l in open(R+"ref_exact.fa") if not l.startswith(">")]; body="".join(s)
def w(fn,recs):
    with open(fn,"w") as f:
        for h,b in recs:
            f.write(">"+h+"\n")
            for i in range(0,len(b),60): f.write(b[i:i+60]+"\n")
w(R+"ref_plus1.fa",[("chr22",body+"A")])
w(R+"ref_superset.fa",[("chr22",body),("chrEXTRA",body[:5000])])
PY
chk "NEW ref chr22 one base longer (LN differs)" $R/bam_m5.bam $R/ref_plus1.fa 1
chk "NEW ref superset (BAM header is a subset)" $R/bam_m5.bam $R/ref_superset.fa 0
cp $R/ref_exact.fa "$W/sp dir/ref exact.fa"; res=$(sed -e "s#in\.bam#$R/bam_m5.bam#g" -e "s#ref\.fa#'$W/sp dir/ref exact.fa'#g" $SN/SKILL_03_bash.txt > $G/dict_sp.sh; bash $G/dict_sp.sh >/dev/null 2>&1; echo $?); A "NEW quoted spaced reference path works" "$([ $res = 0 ] && echo 1)"

echo "=== T04 SKILL_05 samtools stats IS"
s=$(gen SKILL_05_bash $HUM $REF is); bash $s >/dev/null 2>&1
python - <<'PY'
import numpy as np, pysam
rows=[l.split() for l in open("insert_sizes.txt")]
sz=np.array([int(r[0]) for r in rows]); ct=np.array([int(r[1]) for r in rows])
mean_is=(sz*ct).sum()/ct.sum()
v=[r.template_length for r in pysam.AlignmentFile("/mnt/openscience/audit-envs/alignment-files/public-data/human/test.paired_end.sorted.bam") if r.is_proper_pair and not r.is_secondary and r.template_length>0]
print(f"  IS-table mean {mean_is:.1f} n={ct.sum()} | pysam mean {np.mean(v):.1f} n={len(v)}")
print("  ASSERT", "PASS" if abs(mean_is-np.mean(v))<1.5 else "FAIL", ": IS table mean ~ pysam mean")
PY

echo "=== T05 SKILL_06 Picard CollectInsertSizeMetrics"
s=$(gen SKILL_06_bash $HUM $REF ins); bash $s > ins.log 2>&1; echo "  rc=$?"
med=$(grep -A1 '^MEDIAN_INSERT_SIZE' insert_metrics.txt | tail -1 | cut -f1); echo "  Picard median insert: $med"; A "median 123 (matches pysam/smoke value) and PDF written" "$([ "$med" = 123 ] && [ -s insert_histogram.pdf ] && echo 1)"
echo "  --- without Rscript on PATH (the Skill never says the PDF needs R):"
rm -f insert_metrics.txt insert_histogram.pdf
NOR=$(echo "$PATH" | tr ':' '\n' | while read p; do [ -x "$p/Rscript" ] || echo "$p"; done | paste -sd:)
env PATH="$NOR" bash $s > ins_noR.log 2>&1; echo "  rc=$? Rscript visible: $(env PATH="$NOR" which Rscript 2>&1 | head -1)"; grep -E 'Exception|Rscript|R script|ERROR' ins_noR.log | head -3 | cut -c1-200; ls -la insert_metrics.txt insert_histogram.pdf 2>&1 | cut -c1-100

echo "=== T06 SKILL_07 Python insert size (unindexed name-sorted BAM and coordinate BAM)"
for b in $HUMN $HUM $PD/human/test.paired_end.umi_unsorted.bam; do
  sed -e "s#sample\.bam#$b#" -e "s#plt.savefig('insert_size_dist.pdf')#plt.savefig('/dev/null', format='pdf')#" $SN/SKILL_07_python.txt > $G/py7.py; MPLBACKEND=Agg python $G/py7.py 2>&1 | tr '\n' ' '; echo " <- $(basename $b)"; done

echo "=== T07 SKILL_09 pairing rate == flagstat"
for b in $HUM $RNA $G1K $PD/human/test.paired_end.name.sorted.bam; do
  s=$(gen SKILL_09_bash $b $REF pr); out=$(bash $s 2>&1); fs=$(samtools flagstat $b)
  pp=$(echo "$fs" | grep 'properly paired' | sed 's/.*(\([0-9.]*\)%.*/\1/'); wm=$(echo "$fs" | grep 'with itself and mate mapped' | awk '{print $1}'); sg=$(echo "$fs" | grep singletons | awk '{print $1}'); prpm=$(echo "$fs" | grep 'primary mapped' | awk '{print $1}')
  echo "  $(basename $b): skill => $out | flagstat properly paired (of paired-in-sequencing) $pp%"
  python - "$out" $b <<'PY'
import sys,re,pysam
out,b=sys.argv[1],sys.argv[2]
p=t=0
for r in pysam.AlignmentFile(b,check_sq=False).fetch(until_eof=True):
    if r.is_paired and not r.is_unmapped and not r.is_secondary and not r.is_supplementary:
        t+=1; p+=r.is_proper_pair
v=float(re.search(r"([\d.]+)%",out).group(1))
print(f"    pysam independent: {100*p/t:.2f}% ->","ASSERT PASS" if abs(v-100*p/t)<0.006 else "ASSERT FAIL")
PY
done
echo "  99.96% arithmetic (the fix's claimed bc trap):"; A "script prints 99.96 not 99.00/90.0 for human PE" "$(bash $(gen SKILL_09_bash $HUM $REF pr2) | grep -q '99.96%' && echo 1)"

echo "=== T08 SKILL_12 strand fraction, SKILL_13 per-chrom loop"
s=$(gen SKILL_12_bash $HUM $REF sf); out=$(bash $s 2>&1); echo "$out" | sed 's/^/  /'
python - <<'PY'
import pysam
f=r=0
for x in pysam.AlignmentFile("/mnt/openscience/audit-envs/alignment-files/public-data/human/test.paired_end.sorted.bam"):
    if x.is_unmapped or x.is_secondary or x.is_supplementary: continue
    if x.is_reverse: r+=1
    else: f+=1
print(f"  pysam independent F={f} R={r} fraction={f/(f+r):.3f}")
PY
for b in $HUM $G1K $RNA; do s=$(gen SKILL_13_bash $b $REF pc); echo "  loop on $(basename $b): $(bash $s 2>&1 | head -3 | tr '\n' ';')"; done
cp $RNA rna_idx.bam; samtools index rna_idx.bam; s=$(gen SKILL_13_bash $W/rna_idx.bam $REF pcr); echo "  loop on the RNA BAM after samtools index: $(bash $s 2>&1 | head -3 | tr '
' ';')"
echo "  loop on the unindexed name-sorted BAM (documented as needing an index):"; s=$(gen SKILL_13_bash $HUMN $REF pcn); bash $s 2>&1 | head -2 | cut -c1-150 | sed 's/^/    /'

echo "=== T09 SKILL_14 MAPQ hist, SKILL_15 mean MAPQ, SKILL_16 density, SKILL_17 aneuploidy"
s=$(gen SKILL_14_bash $HUM $REF mq); bash $s 2>&1 | head -4 | sed 's/^/  /'
s=$(gen SKILL_15_bash $HUM $REF mq2); o=$(bash $s 2>&1); echo "  $o (pysam truth: $(python -c "
import pysam
v=[r.mapping_quality for r in pysam.AlignmentFile('$HUM') if not r.is_unmapped and not r.is_secondary and not r.is_supplementary]
print(round(sum(v)/len(v),3), len(v))"))"
s=$(gen SKILL_16_bash $HUM $REF ix); bash $s > ix.out 2> ix.err; echo "  density awk rc=$? out=$(tr '\n' ';' < ix.out) stderr=$(head -1 ix.err)"
s=$(gen SKILL_17_bash $G1K $REF an); echo "  aneuploidy (gawk, 1000G slice): $(bash $s 2>&1 | head -3 | tr '\n' ';')"
sed 's#| awk#| /usr/bin/mawk#g' $s > $G/an_mawk.sh; echo "  aneuploidy (mawk):              $(bash $G/an_mawk.sh 2>&1 | head -3 | tr '\n' ';')  [mawk substitutions: $(grep -c mawk $G/an_mawk.sh)]"
printf 'chr1\t1000\t100\t0\nchr2\t1000\t100\t0\nchr3\t1000\t150\t0\nchrX\t1000\t50\t0\nchr1_alt\t500\t900\t0\n*\t0\t0\t7\n' > idx_syn.txt
echo "  synthetic idxstats (chr1/chr2 density 0.1, chr3 0.15, chrX/alt excluded):"
sed -e 's#samtools idxstats in.bam#cat idx_syn.txt#' $SN/SKILL_17_bash.txt > $G/an_syn.sh; bash $G/an_syn.sh 2>&1 | tr '\n' ';' | sed 's/^/    /'; echo

echo "=== T10 SKILL_18 Picard alignment summary, SKILL_10 GC bias, SKILL_11 computeGCBias"
s=$(gen SKILL_18_bash $HUM $REF as); bash $s > as.log 2>&1; python - <<'PY'
rows=[l.rstrip("\n").split("\t") for l in open("alignment_summary.txt") if not l.startswith("#") and l.strip()]
h=[r for r in rows if r[0]=="CATEGORY"][0]
for r in rows:
    if r[0]=="CATEGORY" or len(r)!=len(h): continue
    d=dict(zip(h,r)); print("  ",d["CATEGORY"],{k:d[k] for k in ("PCT_PF_READS_ALIGNED","PF_MISMATCH_RATE","PF_INDEL_RATE","STRAND_BALANCE")})
PY
s=$(gen SKILL_10_bash $HUM $REF gc); bash $s > gc.log 2>&1; echo "  GC rc=$?"; ls gc_bias_metrics.txt gc_summary.txt gc_bias_chart.pdf 2>&1 | tr '\n' ' '; echo
grep -E '^ACCUMULATION_LEVEL' -A2 gc_summary.txt | cut -f1-12 | head -3
sed -e "s#input\.bam#$HUM#" -e "s#hg38.2bit#$PD/human/genome.2bit#" -e "s#--effectiveGenomeSize 2913022398#--effectiveGenomeSize 40001#" $SN/SKILL_11_bash.txt > $G/cgc.sh; bash $G/cgc.sh > cgc.log 2>&1; echo "  computeGCBias rc=$? files: $(ls gc_bias.txt gc_bias.pdf 2>&1 | tr '\n' ' ')"

echo "=== T11 SKILL_20 python validator usage lines and 'samtools view -s' note"
n1=$(samtools view -c -F 2304 -s 42.10 $HUM); n2=$(samtools view -c -F 2304 -s 42.10 $HUM); nn=$(samtools view -F 2304 -s 42.10 $HUM | cut -f1 | sort | uniq -c | awk '$1!=2' | wc -l)
A "-s 42.10 reproducible ($n1 == $n2) and keeps mates together (unmatched names: $nn)" "$([ $n1 = $n2 ] && [ $nn = 0 ] && echo 1)"
echo "=== done"
