#!/bin/bash
# INPUT 4 (variant B): "Merge these per-lane BAMs. Check they are consistently sorted first, dedup @RG/@PG, then merge a region.
#   Also merge the name-sorted versions."  Real (human PE + planted dups, 1000G) + synthetic RG-collision BAMs.
source /mnt/openscience/audits/bio-alignment-sorting/run/common.sh
W=$WORK/in4; rm -rf $W; mkdir -p $W; cd $W
H=$PD/human/test.paired_end.sorted.bam; P=$PD/derived/planted_dups.bam
cp $H h.bam; cp $H.bai h.bam.bai; cp $P p.bam; cp $P.bai p.bam.bai

echo "### 4.1 SKILL: verify sort-order consistency loop (verbatim) -- consistent set then a mixed set"
mkdir -p ok mix; cp h.bam p.bam ok/; cp h.bam mix/; samtools sort -n -o mix/nm.bam p.bam
cat > loop.sh <<'EOF'
#!/bin/bash
cd "$1"
for f in *.bam; do samtools view -H "$f" | head -1; done | sort -u
EOF
echo "-- consistent dir:"; bash loop.sh ok | tee ok.out
eq "consistent set prints exactly ONE line" "$(wc -l < ok.out)" "1"
echo "-- mixed dir:"; bash loop.sh mix | tee mix.out
eq "mixed set prints 2 lines" "$(wc -l < mix.out)" "2"
echo "-- BAM with no @HD (real UMI BAM): what does head -1 print?"; mkdir -p nohd; cp $PD/human/test.paired_end.umi_unsorted.bam nohd/; bash loop.sh nohd | cut -c1-60

echo "### 4.2 SKILL 'Safe Merge' samtools merge -c -p -@ 8 (real, identical @RG @SQ)"
samtools merge -c -p -@ 8 merged.bam h.bam p.bam; echo "rc=$?"
eq "merged record count = 5644+500" "$(nrec merged.bam)" "6144"
eq "merged @HD SO" "$(so merged.bam | grep -o 'SO:[a-z]*')" "SO:coordinate"
python $RUN/order_check.py merged.bam | grep -a n=
echo "  @RG lines: $(samtools view -H merged.bam | grep -ac '^@RG')   @PG lines: $(samtools view -H merged.bam | grep -ac '^@PG')"
echo "  @PG in inputs: h=$(samtools view -H h.bam | grep -ac '^@PG') p=$(samtools view -H p.bam | grep -ac '^@PG')"
samtools merge -@ 4 merged_nocp.bam h.bam p.bam
echo "-- without -c -p (SKILL 'Merge with Threads'):  @RG=$(samtools view -H merged_nocp.bam | grep -ac '^@RG') @PG=$(samtools view -H merged_nocp.bam | grep -ac '^@PG')"
samtools view -H merged_nocp.bam | grep -a '^@RG'
echo "   RG tags carried by reads (nocp): $(samtools view merged_nocp.bam | grep -ao 'RG:Z:[^[:space:]]*' | sort | uniq -c | tr '\n' ' ')"
echo "   RG tags carried by reads (-c -p): $(samtools view merged.bam | grep -ao 'RG:Z:[^[:space:]]*' | sort | uniq -c | tr '\n' ' ')"

echo "### 4.3 RG-ID collision, DIFFERENT read groups (SYNTHETIC rgcollide_A/B: same ID L1, sampleA/lane1 vs sampleB/lane7)"
samtools view -H $DATA/rgcollide_A.bam | grep -a '^@RG'; samtools view -H $DATA/rgcollide_B.bam | grep -a '^@RG'
samtools merge -c -p -f rgc_cp.bam $DATA/rgcollide_A.bam $DATA/rgcollide_B.bam
samtools merge -f rgc_plain.bam $DATA/rgcollide_A.bam $DATA/rgcollide_B.bam
echo "-- with -c -p (SKILL 'Safe Merge'):"; samtools view -H rgc_cp.bam | grep -a '^@RG'
eq "-c collapses two DIFFERENT read groups into ONE header line" "$(samtools view -H rgc_cp.bam | grep -ac '^@RG')" "1"
echo "   B-reads (name B_*) now labelled: $(samtools view rgc_cp.bam | grep -a '^B_' | grep -ao 'RG:Z:[^[:space:]]*' | sort -u) ; header SM kept: $(samtools view -H rgc_cp.bam | grep -a '^@RG' | grep -o 'SM:[^[:space:]]*')"
echo "-- without -c:"; samtools view -H rgc_plain.bam | grep -a '^@RG'
echo "   A-read RG: $(samtools view rgc_plain.bam | grep -a '^A_0' | grep -ao 'RG:Z:[^[:space:]]*')  B-read RG: $(samtools view rgc_plain.bam | grep -a '^B_0' | grep -ao 'RG:Z:[^[:space:]]*')"
echo "-- SKILL remedy: make IDs unique upstream with samtools addreplacerg, then merge -c -p"
samtools addreplacerg -r '@RG\tID:L1B\tSM:sampleB\tPL:ILLUMINA\tPU:lane7' -m overwrite_all -o B_fixed.bam $DATA/rgcollide_B.bam; echo "addreplacerg rc=$?"
samtools merge -c -p -f rgc_fixed.bam $DATA/rgcollide_A.bam B_fixed.bam
samtools view -H rgc_fixed.bam | grep -a '^@RG'
eq "after addreplacerg: two distinct @RG survive -c -p" "$(samtools view -H rgc_fixed.bam | grep -ac '^@RG')" "2"
eq "A reads keep L1, B reads carry L1B" "$(samtools view rgc_fixed.bam | grep -a '^B_0' | grep -ao 'RG:Z:[^[:space:]]*')" "RG:Z:L1B"

echo "### 4.4 SKILL claim: merge does NOT validate sort order; mismatched inputs silently produce a malformed output"
samtools merge -f mixed.bam h.bam mix/nm.bam 2> mixed.err; echo "rc=$? stderr: $(head -2 mixed.err | tr '\n' '|')"
echo "  output header: $(so mixed.bam)"; python $RUN/order_check.py mixed.bam | grep -a n=
python $RUN/order_check.py mixed.bam | grep -q 'coordinate_sorted=True' && echo "  [FAIL?] output is coordinate sorted" || echo "  [PASS] SKILL claim confirmed: exit 0, header still SO:coordinate-labelled=$(so mixed.bam | grep -c coordinate), records NOT coordinate sorted"
samtools index mixed.bam 2>&1 | head -1

echo "### 4.5 Name-sorted merge: SKILL Quick Reference has no -n/-N"
samtools sort -n -o n1.bam h.bam; samtools sort -n -o n2.bam p.bam
samtools merge -f nm_plain.bam n1.bam n2.bam; echo "  plain merge of two name-sorted BAMs rc=$?, header: $(so nm_plain.bam)"
python $RUN/order_check.py nm_plain.bam | grep -a n=
samtools merge -f -n nm_n.bam n1.bam n2.bam; echo "  merge -n rc=$?, header: $(so nm_n.bam)"
python $RUN/order_check.py nm_n.bam | grep -a n=
python $RUN/order_check.py nm_n.bam | grep -q 'qname_natural=True' && echo "  [PASS] merge -n keeps natural name order" || echo "  [FAIL] merge -n"
python $RUN/order_check.py nm_plain.bam | grep -q 'qname_natural=True' && echo "  [INFO] plain merge happened to be name-ordered" || echo "  [FINDING] plain merge (no -n) of name-sorted inputs is NOT name-ordered (silently) -- SKILL never mentions -n/-N for merge"

echo "### 4.6 -b file list; -f overwrite; -R region (SKILL)"
printf 'h.bam\np.bam\n' > files.txt
samtools merge -b files.txt -f merged_b.bam; echo "-b rc=$? records=$(nrec merged_b.bam)"
eq "-b equals positional merge (cols 1-11, RG suffix excluded)" "$(samtools view merged_b.bam | cut -f1-11 | md5sum)" "$(samtools view merged_nocp.bam | cut -f1-11 | md5sum)"
samtools merge -f rep1.bam h.bam p.bam; samtools merge -f rep2.bam h.bam p.bam
echo "  repeat merge w/o -c: @RG suffix run1: $(samtools view -H rep1.bam | grep -a '^@RG' | cut -f2 | tr '
' ' ')  run2: $(samtools view -H rep2.bam | grep -a '^@RG' | cut -f2 | tr '
' ' ')"
[ "$(samtools view rep1.bam | md5sum)" = "$(samtools view rep2.bam | md5sum)" ] && echo "  [INFO] two identical merges gave identical bytes" || echo "  [FINDING] two identical merges (no -c) differ: RG-ID suffix is random unless -s SEED (SKILL does not mention)"
samtools merge -f -s 7 rep3.bam h.bam p.bam; samtools merge -f -s 7 rep4.bam h.bam p.bam
eq "merge -s 7 is reproducible" "$(samtools view rep3.bam | md5sum)" "$(samtools view rep4.bam | md5sum)"
samtools merge merged_b.bam h.bam p.bam 2> nof.err; echo "  no -f onto existing file rc=$? msg: $(head -1 nof.err)"
samtools merge -f merged_region.bam -R chr22:2000-3000 h.bam p.bam; echo "-R rc=$?"
exp=$(( $(samtools view -c h.bam chr22:2000-3000) + $(samtools view -c p.bam chr22:2000-3000) ))
eq "merge -R chr22:2000-3000 count == sum of per-file region counts" "$(nrec merged_region.bam)" "$exp"
mkdir -p noidx; cp h.bam p.bam noidx/
samtools merge -f noidx/reg.bam -R chr22:2000-3000 noidx/h.bam noidx/p.bam 2> noidx.err; echo "  -R on UNINDEXED inputs rc=$? msg: $(head -2 noidx.err | tr '\n' '|')  records=$(nrec noidx/reg.bam 2>/dev/null)"

echo "### 4.7 pysam.merge (SKILL) == CLI; failure raises?"
cat > pymerge.py <<'EOF'
import pysam, subprocess
pysam.merge('-c', '-p', '-f', 'py_merged.bam', 'h.bam', 'p.bam')
def recs(p):
    with pysam.AlignmentFile(p,'rb') as f: return [r.to_string() for r in f.fetch(until_eof=True)]
a, b = recs('py_merged.bam'), recs('merged.bam')
print('pysam.merge == CLI merge:', a == b, 'n=', len(a)); assert a == b and len(a) == 6144
try:
    pysam.merge('-f', 'x.bam', 'nope1.bam', 'nope2.bam')
    print('pysam.merge on missing inputs: NO EXCEPTION')
except Exception as e:
    print('pysam.merge on missing inputs raised', type(e).__name__, '|', str(e)[:90].replace('\n',' '))
EOF
python pymerge.py
summary
